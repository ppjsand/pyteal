# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

# System imports
from threading import Thread
import os
from datetime import datetime, timedelta 

# TEAL imports
from ibm.teal import registry
from ibm.teal.registry import get_logger, SERVICE_EVENT_Q, SERVICE_DB_INTERFACE, \
                              SERVICE_NOTIFIER, SERVICE_CHECKPOINT_MGR,\
    SERVICE_SHUTDOWN_MODE, SHUTDOWN_MODE_IMMEDIATE
from ibm.teal import Event
from ibm.teal.event import EVENT_COLS
from ibm.teal.database import db_interface
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.monitor.event_monitor import EventMonitor
from ibm.teal.checkpoint_mgr import CheckpointListener
from ibm.teal.util.teal_thread import TealThread
from ibm.teal.control_msg import inject_update_checkpoint_msg

TEAL_TEST_NOTIFIER_CONFIG = 'TEAL_TEST_NOTIFIER_CONFIG'
CFG_KEY_NOTIFIER = 'notifier'
CFG_KEY_RECOVERY = 'recovery_mode'
TEAL_UPDATE_CHECKPOINT_FREQUENCY = 'TEAL_UPDATE_CHECKPOINT_FREQUENCY'
DEFAULT_UPDATE_CHECKPOINT_FREQUENCY = 5000
    
class RealtimeMonitor(EventMonitor):
    '''
    This is a "realtime" event query based on using a generic notifier as
    the notification of database changes. 
    '''
    
    def __init__(self, config_dict):
        '''Constructor.
        '''
        # Validate configuration parameters
        if config_dict['enabled'] != 'realtime':
            raise ConfigurationError('Realtime monitor can only enabled for realtime use.  Unsupported value specified: {0}'.format(config_dict['enabled']))

        temp_frequency = os.environ.get(TEAL_UPDATE_CHECKPOINT_FREQUENCY, None)
        if temp_frequency is None: 
            self.update_checkpoint_frequency = DEFAULT_UPDATE_CHECKPOINT_FREQUENCY
        else:     
            try:   
                self.update_checkpoint_frequency = long(temp_frequency)
            except:
                get_logger().warning('Environment variable \'{0}\' was invalid: \'{1}\'. Default value used'.format(TEAL_UPDATE_CHECKPOINT_FREQUENCY, str(temp_frequency)))
                self.update_checkpoint_frequency = DEFAULT_UPDATE_CHECKPOINT_FREQUENCY

        cfg_notifier = os.environ.get(TEAL_TEST_NOTIFIER_CONFIG, None)
        if cfg_notifier is None:
            if CFG_KEY_NOTIFIER not in config_dict: 
                raise ConfigurationError('RealtimeMonitor requires notifier be specified in the configuration file or as an environment variable')
            else:
                cfg_notifier = config_dict[CFG_KEY_NOTIFIER]
        # create notifier class
        try:
            module_name, class_name = cfg_notifier.rsplit('.', 1)
            module = __import__(module_name, globals(), locals(), [class_name])
        except ImportError,ie:
            get_logger().error(ie)
            raise # throw the ImportError up the chain
        plugin_class = getattr(module, class_name)
        self.notifier = plugin_class()
        registry.register_service(SERVICE_NOTIFIER, self.notifier)
        get_logger().info('Notifier {0} configured'.format(cfg_notifier))
                        
        self.checkpointL = CheckpointListener('monitor_event_queue')

        # generate queries for later      
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        self.sql_runtime_query = dbi.gen_select(EVENT_COLS, db_interface.TABLE_EVENT_LOG, where='$rec_id > ?', where_fields=['rec_id'], order='rec_id') 
        self.sql_max_event = dbi.gen_select_max('rec_id', db_interface.TABLE_EVENT_LOG)
        
        override_recovery_mode = None
        if CFG_KEY_RECOVERY in config_dict:
            override_recovery_mode = config_dict[CFG_KEY_RECOVERY]
            get_logger().info('Overriding restart mode with specified recovery mode = {0}'.format(override_recovery_mode))

        checkpoint_mgr = registry.get_service(SERVICE_CHECKPOINT_MGR)
        self.start_recid, mode_used = checkpoint_mgr.get_starting_event_rec_id(override_recovery_mode)

        get_logger().info('Restarting at rec_id = {0} with mode = {1};  '.format(self.start_recid, mode_used))
        self.checkpointL.set_data('{0} {1}'.format(mode_used, str(self.start_recid)))
        
        # Do this after logging so we can tell from log if it was 0 or None
        if self.start_recid is None:
            self.start_recid = 0
        
        self.running = True # Set here so we don't run into timing issues in shutdown
        self.monitor_thread = TealThread(group=None, target=self.start, name='event_monitor')
        self.monitor_thread.setDaemon(True)
        self.monitor_thread.start()

    def start(self):
        '''Start the notifier-based event monitor running.
        '''
        try:
            event_queue =  registry.get_service(SERVICE_EVENT_Q)
            dbi = registry.get_service(SERVICE_DB_INTERFACE)
            next_failure_log = None
            rc = 0   
            
            while self.running:
                if rc == 0:
                    get_logger().debug('Processing events in monitor event injection thread. startRecid = {0}'.format(self.start_recid))
                    try:
                        cnxn = dbi.get_connection()
                        cursor = cnxn.cursor()
                        for row in cursor.execute(self.sql_runtime_query, self.start_recid):
                            get_logger().debug('Processing row, rec_id = {0} time_occurred = {1}, time_logged = {2}'.format(row[0], row[2],row[3]))
                            e = Event.fromDB(row)
                            event_queue.put(e)
                            self.start_recid = row[0] 
                            if self.running == False: 
                                get_logger().info('Monitor event injection thread interrupted.  last recid = {0}'.format(self.start_recid))
                                break
                            if self.start_recid % self.update_checkpoint_frequency == 0:
                                inject_update_checkpoint_msg(self.start_recid)
                        cnxn.close()
                    except:
                        cur_time = datetime.now()
                        if next_failure_log is None or  cur_time > next_failure_log:
                            get_logger().exception('Failure in monitor event injection thread')
                            next_failure_log = cur_time + timedelta(minutes=10)
                rc = self.notifier.wait()
        except:
            get_logger().exception('Monitor event injection thread failure')
        get_logger().debug('Exiting monitor event injection thread.  Last recid = {0}'.format(self.start_recid))    

    def shutdown(self):
        '''Stop running the event monitor. 
        '''
        get_logger().debug('Starting shutdown')
        self.running = False
        self.notifier.post()
        
        get_logger().debug('Joining thread')
        self.monitor_thread.join()
        
        last_processed_recid = self.start_recid 
        if registry.get_service(SERVICE_SHUTDOWN_MODE) == SHUTDOWN_MODE_IMMEDIATE:
            # If immediate use the last one that was processed
            last_processed_recid = self.checkpointL.event_checkpoint.start_rec_id
        registry.get_service(SERVICE_CHECKPOINT_MGR).monitor_shutdown(last_processed_recid)
        get_logger().debug('Shutdown complete')

