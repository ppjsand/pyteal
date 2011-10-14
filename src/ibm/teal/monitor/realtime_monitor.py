# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2011
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

# System imports
from threading import Thread
import os

# TEAL imports
from ibm.teal import registry
from ibm.teal.registry import get_logger, SERVICE_EVENT_Q, SERVICE_DB_INTERFACE, \
                              SERVICE_NOTIFIER,\
    SERVICE_CHECKPOINT_MGR

from ibm.teal import Event
from ibm.teal.event import EVENT_ATTR_RAW_DATA, \
                           EVENT_ATTR_REC_ID, EVENT_ATTR_TIME_LOGGED, EVENT_ATTR_EVENT_ID, \
                           EVENT_ATTR_SRC_COMP, EVENT_ATTR_SRC_LOC, \
                           EVENT_ATTR_SRC_LOC_TYPE, EVENT_ATTR_TIME_OCCURRED, \
                           EVENT_ATTR_RPT_COMP, EVENT_ATTR_RPT_LOC, EVENT_ATTR_RPT_LOC_TYPE, \
                           EVENT_ATTR_ELAPSED_TIME,EVENT_ATTR_EVENT_CNT,EVENT_ATTR_RAW_DATA_FMT

from ibm.teal.database.db_interface import TABLE_EVENT_LOG
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.monitor.event_monitor import EventMonitor
from ibm.teal.checkpoint_mgr import CheckpointListener


BASIC_EVENTLOG_SELECT_COLS = ['rec_id', 'event_id', 'time_occurred', 'time_logged', 'src_comp', 'src_loc_type', 'src_loc', 'rpt_comp', 'rpt_loc_type', 'rpt_loc', 'event_cnt', 'elapsed_time', 'raw_data_fmt', 'raw_data']
TEAL_TEST_NOTIFIER_CONFIG = 'TEAL_TEST_NOTIFIER_CONFIG'

    
class RealtimeMonitor(EventMonitor):
    '''
    This is a "realtime" event query based on using a generic notifier as
    the notification of database changes. 
    '''
    
    def __init__(self,restart,config_dict):
        '''Constructor.
        '''
        
        # Validate configuration parameters
        if config_dict['enabled'] != 'realtime':
            raise ConfigurationError('Realtime monitor can only enabled for realtime use.  Unsupported value specified: {0}'.format(config_dict['enabled']))

        self.running = False
        CONFIG_KEY = 'notifier'
        if CONFIG_KEY not in config_dict:
            raise ConfigurationError('RealtimeMonitor requires notifier be specified in the configuration file')
        # See if configuration overridden with environment variable
        config_dict[CONFIG_KEY] = os.environ.get(TEAL_TEST_NOTIFIER_CONFIG, config_dict[CONFIG_KEY])
        # create configuration class
        try:
            module_name, class_name = config_dict[CONFIG_KEY].rsplit('.', 1)
            module = __import__(module_name, globals(), locals(), [class_name])
        except ImportError,ie:
            get_logger().error(ie)
            raise # throw the ImportError up the chain
        plugin_class = getattr(module, class_name)
        self.notifier = plugin_class()
        registry.register_service(SERVICE_NOTIFIER, self.notifier)
        get_logger().info('Notifier {0} configured'.format(config_dict[CONFIG_KEY]))
                        
        self.restart = restart
        self.checkpointL = CheckpointListener('monitor_event_queue')

        # generate queries for later      
        db = registry.get_service(SERVICE_DB_INTERFACE)
        self.sql_runtime_query = db.gen_select(BASIC_EVENTLOG_SELECT_COLS, TABLE_EVENT_LOG, where='$rec_id > ?', where_fields=['rec_id'], order='rec_id') 
        self.sql_max_event = db.gen_select_max('rec_id', TABLE_EVENT_LOG)
        
        get_logger().info('restart mode = {0}'.format(self.restart))
        override_recovery_mode = None
        if 'recovery_mode' in config_dict:
            override_recovery_mode = config_dict['recovery_mode']
            get_logger().info('Overriding restart mode with specified recovery mode = {0}'.format(override_recovery_mode))

        checkpoint_mgr = registry.get_service(SERVICE_CHECKPOINT_MGR)
        self.startRecid, mode_used = checkpoint_mgr.get_starting_event_rec_id(override_recovery_mode)

        get_logger().info('Restarting at rec_id = {0} with mode = {1};  '.format(self.startRecid, mode_used))
        self.checkpointL.set_data('{0} {1}'.format(mode_used, str(self.startRecid)))
        
        # Process any backlog of events
        new_startRecid = self.process_events(self.sql_runtime_query, self.startRecid)

        if(new_startRecid is not None):
            self.startRecid = new_startRecid

        self.running = True # Set here so we don't run into timing issues in shutdown
        self.monitor_thread = Thread(group=None,target=self.start,name='event_monitor',args=[restart])
        self.monitor_thread.setDaemon(True)
        self.monitor_thread.start()
        return

    def start(self,args):
        '''Start the notifier-based event monitor running.
        '''
        # This is the standard monitor loop; wait on the notifier
        # and then grab everything since the last time.
        while self.running:
            items = self.notifier.wait()
            if items == 0:
                get_logger().debug('Processing events in monitor thread. startRecid = {0}'.format(self.startRecid))
                self.startRecid = self.process_events(self.sql_runtime_query, self.startRecid)
        return

    def process_events(self, query, *args):
        rtn_recid = 0
    
        get_logger().debug('process_events: Enter.{0}'.format(query))
    
        eventQueue = registry.get_service(SERVICE_EVENT_Q)
        try:
            db = registry.get_service(SERVICE_DB_INTERFACE)
            cnxn = db.get_connection()
            cursor = cnxn.cursor()
            for r in cursor.execute(query, args):
                get_logger().debug('process_events: Processing row, rec_id = {0}'.format(r[0]))
                get_logger().debug('process_events: time_occurred = {0}, time_logged = {1}'.format(r[2],r[3]))
                recid_rd = r[0]
                event_id_rd = r[1].strip()
                time_occurred_rd = r[2]
                time_logged_rd = r[3]
                src_comp_rd = r[4].strip()
                src_loc_type_rd = r[5].strip()
                src_loc_rd = r[6].strip()
                if r[7] is not None:
                    rpt_comp_rd = r[7].strip()
                else:
                    rpt_comp_rd = r[7]
                if r[8] is not None:
                    rpt_loc_type_rd = r[8].strip()
                else:
                    rpt_loc_type_rd = r[8]
                if r[9] is not None:
                    rpt_loc_rd = r[9].strip()
                else:
                    rpt_loc_rd = r[9]
                    
                event_cnt_rd = r[10]
                elapsed_time_rd = r[11]
                raw_data_fmt_rd = r[12]
                raw_data_rd = r[13]
                
                my_dict = ({EVENT_ATTR_REC_ID:recid_rd,
                            EVENT_ATTR_TIME_OCCURRED:time_occurred_rd,
                            EVENT_ATTR_TIME_LOGGED:time_logged_rd,
                            EVENT_ATTR_EVENT_ID:event_id_rd,
                            EVENT_ATTR_SRC_COMP:src_comp_rd,
                            EVENT_ATTR_SRC_LOC_TYPE:src_loc_type_rd, 
                            EVENT_ATTR_SRC_LOC:src_loc_rd,
                            EVENT_ATTR_RPT_COMP:rpt_comp_rd,
                            EVENT_ATTR_RPT_LOC_TYPE:rpt_loc_type_rd,
                            EVENT_ATTR_RPT_LOC:rpt_loc_rd,
                            EVENT_ATTR_EVENT_CNT:event_cnt_rd,
                            EVENT_ATTR_ELAPSED_TIME:elapsed_time_rd,    
                            EVENT_ATTR_RAW_DATA_FMT:raw_data_fmt_rd,
                            EVENT_ATTR_RAW_DATA:raw_data_rd})
                e = Event(in_dict=my_dict);
                # This is a blocking put. We don't expect the queue
                # to ever block as it does not have a set size.
                eventQueue.put(e)
                rtn_recid = recid_rd

            if(rtn_recid == 0):
                cursor.execute(self.sql_max_event)
                row = cursor.fetchone()
                if row and row[0]:
                    rtn_recid = row[0]
                
            cnxn.close()
        except StandardError,e:
            get_logger().error('Checkpoint table event recid retrieval failed. {0}'.format(e))
    
        get_logger().debug('process_events: Exit. rtn_recid = {0}'.format(rtn_recid))    
        return rtn_recid

    def shutdown(self):
        '''Stop running the event monitor. 
        '''
        get_logger().debug('Starting shutdown')
        self.running = False
        self.notifier.post()
        
        get_logger().debug('Joining thread')
        self.monitor_thread.join()

        get_logger().debug('Shutdown complete')
        return

# end class SemaphoreRASEventMonitor

