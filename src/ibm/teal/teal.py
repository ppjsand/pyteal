#!/usr/bin/env python
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

# locale setup
import os
import gettext
from ibm.teal.checkpoint_mgr import CheckpointMgr
from ibm.teal.event import Event
curdir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(curdir, '..', 'locale')
t = gettext.translation('messages', localedir, fallback=True)
_ = t.lgettext

import logging
#from logging.handlers import RotatingFileHandler
import sys
import stat
import errno
import signal
import glob
import string
import time
from datetime import datetime
from stat import S_IWUSR

from ibm.teal.alert import create_teal_alert, TEAL_ALERT_ID_TEAL_STARTED
from ibm.teal import registry
from ibm.teal.teal_error import TealError, ConfigurationError
from ibm.teal.registry import get_logger, SERVICE_LOGGER, SERVICE_LOG_FILE, SERVICE_MSG_LEVEL,\
    SERVICE_EVENT_METADATA, SERVICE_RUN_MODE, RUN_MODE_REALTIME,\
    RUN_MODE_HISTORIC, SERVICE_ALERT_MGR, SERVICE_CHECKPOINT_MGR,\
    SERVICE_TIME_MODE
from ibm.teal.registry import SERVICE_EVENT_Q, SERVICE_ALERT_ANALYZER_Q, SERVICE_ALERT_DELIVERY_Q, SERVICE_ALERT_DELIVERY, SERVICE_CONFIGURATION, SERVICE_ALERT_METADATA 
from ibm.teal.registry import SERVICE_EVENT_MONITOR, SERVICE_DB_INTERFACE, SERVICE_LOCATION, SERVICE_SHUTDOWN, SERVICE_HISTORIC_QUERY
from ibm.teal.registry import TEAL_LOG_DIR, TEAL_CONF_DIR, TEAL_ROOT_DIR, TEAL_DATA_DIR  
from ibm.teal.util.listenable_queue import ListenableQueue
from ibm.teal.configuration import Configuration 
from ibm.teal.configuration import CONFIG_EVENT_ANALYZERS, CONFIG_ALERT_ANALYZERS, CONFIG_ALERT_FILTERS,CONFIG_ALERT_LISTENERS, CONFIG_DB_INTERFACE,CONFIG_EVENT_MONITORS,CONFIG_LOCATION, CONFIG_PACKAGE
from ibm.teal.alert_delivery import AlertDelivery
from ibm.teal.location import LocationService
from ibm.teal.metadata import Metadata, META_TYPE_EVENT, META_TYPE_ALERT
from ibm.teal.shutdown import Shutdown
from ibm.teal.alert_mgr import AlertMgr
from ibm.teal.util import command

TEAL_CONF_FILE = 'teal.conf'
TEAL_LOG_FILE = 'teal.log'
TEAL_RUN_MODE_REALTIME = 'realtime'
TEAL_RUN_MODE_HISTORIC = 'historic'

# Query fields, operations and list information for command line parser
qry_info = [('rec_id',command.EQUALITY_OPS,True,command.FIELD_TYPE_INT),
        ('event_id',['='],True,command.FIELD_TYPE_STRING),
        ('time_occurred',command.EQUALITY_OPS,False,command.FIELD_TYPE_TIMESTAMP),
        ('time_logged',command.EQUALITY_OPS,False,command.FIELD_TYPE_TIMESTAMP),
        ('src_comp',['='],True,command.FIELD_TYPE_STRING),
        ('src_loc',['='],False,command.FIELD_TYPE_STRING),
        ('src_scope',['='],False,command.FIELD_TYPE_STRING),
        ('rpt_comp',['='],True,command.FIELD_TYPE_STRING),
        ('rpt_loc',['='],False,command.FIELD_TYPE_STRING),
        ('rpt_scope',['='],False,command.FIELD_TYPE_STRING),
       ]
    
class TealLogger(logging.Logger):
    ''' Simple logger class so that we only register one handler at a time.
    
    If this class is not used, it is possible to get multiple handlers enabled
    which will duplicate every logging statement in the framework
    '''
    def __init__(self,name):
        ''' Constructor '''
        self.handler = None
        logging.Logger.__init__(self, name)
    
    def addHandler(self, hdlr):
        ''' Remove the current handler and replace with the requested handler '''
        if (self.handler is not None):
            logging.Logger.removeHandler(self, self.handler)

        self.handler = hdlr
        logging.Logger.addHandler(self, hdlr)    

class Teal:
    """ The Toolkit for Event Analysis and Logging
    
        This class is responsible for setting up and running the entire 
        environment for running event analysis
    """
    
    def __init__(self, 
                 configFile, 
                 logFile=None, 
                 msgLevel='info',
                 restart=None, 
                 run_mode=TEAL_RUN_MODE_REALTIME, 
                 commit_alerts=True,
                 data_only=False,
                 historic_qry=None,
                 daemon_mode=False,
                 extra_log_id='',
                 commit_checkpoints=None,
                 use_time_occurred=False):
        """ Construct the ELA framework
        
        @param configFile: the TEAL configuration file. This is mandatory
        @param logFile: the full pathname of the logging file. If no logging file is
        specified, logging will be to stdout
        @param msgLevel: the lowest message level that will be logged. The default is
        informational messages and above
        @param restart: determines how teal will start processing events in realtime mode
        @param run_mode: how the monitor will be configured - realtime or historic
        @param commit_alerts: Certain run modes may want to not commit alerts if they are created
        because the user is debugging rules or trying to determine relationships
        @param data_only: do not initialize the processing pipeline Only the data that is
        configured for TEAL should be set up and used
        @param history_query: The query to use to get the events to do historic analysis on
        @param daemon_mode: run in daemon mode
        @param extra_log_id: additional string to add to all log entries for this instance of TEAL
        @param commit_checkpoints: control whether checkpoints should be committed or not
        @param use_time_occurred: Use time occurred instead of time logged for analysis 
        
        """
        
        log_str_list = []

        self.data_only = data_only
        self.daemon_mode = daemon_mode
        
        # Initialize the registry. This will be used by subsequent initialization
        self.init_reg_service()

        # Register a shutdown service for users
        registry.register_service(SERVICE_SHUTDOWN, Shutdown(self.shutdown))

        # Initialize the TEAL directories and environment
        self.init_environment()
        
        # Initialize the logging for the environment
        if run_mode == TEAL_RUN_MODE_HISTORIC:
            if commit_alerts == True:
                extra_log_id = 'C' + extra_log_id
            else:
                extra_log_id = 'H' + extra_log_id
        self.init_log_service(logFile, msgLevel, extra_log_id)
        get_logger().info("******* TEAL({0}) Startup initiated on {1}".format(id(self), datetime.now()))
        log_str_list.append('\tMessage level: {0}'.format(repr(registry.get_service(SERVICE_MSG_LEVEL))))
        log_str_list.append('\tLog file: {0}'.format(repr(registry.get_service(SERVICE_LOG_FILE))))
        
        try:
            # Initialize the mode
            self.init_run_mode(run_mode, historic_qry)
            log_str_list.append('\tRun mode: {0}'.format(registry.get_service(SERVICE_RUN_MODE)))
            if historic_qry is not None and len(historic_qry) > 0:
                log_str_list.append('\t   Query: {0}'.format(historic_qry))
                
            if use_time_occurred == True:
                registry.register_service(SERVICE_TIME_MODE, 'time_occurred')
                log_str_list.append('\t   Time mode = time occurred')
            else:
                registry.register_service(SERVICE_TIME_MODE, 'time_logged')
            
            # Read in the configuration files and prepare it for use
            config_str = self.init_cfg_service(configFile)
            log_str_list.append('\tConfiguration: {0}'.format(config_str))
    
            # Create the location code service
            self.init_location_service()
                
            # Load the metadata
            self.init_metadata_service()
            
            # Initialize the DB interface so persistence and monitor can use
            self.init_db_interface()
            
            # Initialize the persistence services
            self.init_persistence_services(commit_alerts)
    
            if (not data_only):
                # Initialize Checkpointing service
                self.init_checkpoint_service(commit_checkpoints, restart)
                
                # Build the TEAL event/alert processing pipeline
                pipe_str_list = self.init_processing_pipe()
                if len(pipe_str_list) > 0:
                    log_str_list.append('\tPipeline plug-ins: {0}'.format(', '.join(pipe_str_list)))
                else:
                    log_str_list.append('\tPipeline plug-ins: --None--')
                
            # Record startup information
            #   Note before monitor because monitor may start processing immediately 
            # Record in log 
            for log_str in log_str_list:
                get_logger().info(log_str)

            if ((daemon_mode == True) and not data_only) or (commit_alerts == True and run_mode == TEAL_RUN_MODE_HISTORIC):
                # Create TEAL started alert
                create_teal_alert(TEAL_ALERT_ID_TEAL_STARTED, 'TEAL started', '; '.join(log_str_list), recommendation='None')

            if (not data_only):
                # Start the monitor.
                self.init_monitor(restart)
                
            get_logger().info('TEAL startup complete')
            
        except:
            get_logger().exception('TEAL startup failed')
            raise 
        
        return
    
    def init_reg_service(self):
        """ Initialize the registry service
        """
        registry.clear()
        return

    def test_dir(self, aDir, perm=stat.S_IRUSR):
        mode = os.stat(aDir).st_mode
        if (stat.S_ISDIR(mode)):
            if ((mode & perm)== perm):
                pass
            else:
                raise IOError, (errno.EACCES,"No Permission: {0}".format(aDir))
        else:
            raise IOError, (errno.ENOTDIR,"Not directory: {0}".format(aDir))
            
        
    def init_environment(self):
        ''' Initialize the directory paths used within TEAL'''
        # Get any overrides from the environment first
        root_dir = os.environ.get(TEAL_ROOT_DIR, os.path.join(os.sep,'opt','teal'))
        abs_root_dir = os.path.abspath(root_dir)
        self.test_dir(abs_root_dir)
               
        conf_dir = os.environ.get(TEAL_CONF_DIR, os.path.join(os.sep,'etc'))
        abs_conf_dir = os.path.abspath(conf_dir)
        self.test_dir(abs_conf_dir)
    
        data_dir = os.environ.get(TEAL_DATA_DIR, os.path.join(root_dir,'data'))
        abs_data_dir = os.path.abspath(data_dir)
        self.test_dir(abs_data_dir)
        
        log_dir =  os.environ.get(TEAL_LOG_DIR,  os.path.join(os.sep,'var','log','teal'))
        abs_log_dir = os.path.abspath(log_dir)
        self.test_dir(abs_log_dir, stat.S_IRUSR|S_IWUSR)
        
        # Log them in the registry for usage throughout the framework
        registry.register_service(TEAL_ROOT_DIR, abs_root_dir)
        registry.register_service(TEAL_CONF_DIR, abs_conf_dir)
        registry.register_service(TEAL_DATA_DIR, abs_data_dir)
        registry.register_service(TEAL_LOG_DIR, abs_log_dir)
        return 

    def init_run_mode(self, run_mode, qry):
        # Validate the run mode
        if run_mode != RUN_MODE_REALTIME and run_mode != RUN_MODE_HISTORIC:
            raise ConfigurationError('Unrecognized run mode specified: {0}'.format(run_mode))
        
        # Save in registry
        registry.register_service(SERVICE_RUN_MODE, run_mode)
        
        # Configure any additional mode data
        if run_mode == RUN_MODE_HISTORIC:
            registry.register_service(SERVICE_HISTORIC_QUERY, qry)
        return

                
    def init_cfg_service(self, config_file):
        """ Initialize the configuration service
        """
        conf_str = ''
        # Go get the configuration files from the default location
        if config_file is None:
            config_file = os.path.join(registry.get_service(TEAL_CONF_DIR),'teal')
            conf_str += 'None -> '
        # Need to create the list of files to pass to the configuration service
        # so determine if this is a file or directory to recover the proper set
        if os.path.isfile(config_file):
            conf_files = [config_file]
            conf_str += 'File -> {0}'.format(repr(config_file))
        elif os.path.isdir(config_file):
            # Find all the configuration files in the specified directory
            conf_qry =  os.path.join(config_file,'*.conf')
            conf_files = glob.glob(conf_qry)
            conf_str = 'Dir -> {0}'.format(repr(config_file))
        else:
            conf_files = []    
 
        if not conf_files:
            print 'Configuration file(s) not found ' + config_file
            raise ValueError, 'Configuration file(s) not found: {0}'.format(config_file)
                
        registry.register_service(SERVICE_CONFIGURATION, Configuration(conf_files))
        return conf_str
    
    def init_log_service(self, log_file, msg_level, extra_log_id):
        """ Initialize the logging service.
        """
        
        # Create and register the logger
        logging.setLoggerClass(TealLogger)
        logger = logging.getLogger('tealLogger')
        
        # If log file is not specified, set to default path/file
        if log_file is None:
            log_dir = registry.get_service(TEAL_LOG_DIR)
            log_file = os.path.join(log_dir,TEAL_LOG_FILE)
            # TODO: python bug 4749 in RotatingFileHandler
            #hdlr = RotatingFileHandler(log_file, maxBytes=1*1024*1024, backupCount=5)
            hdlr = logging.FileHandler(log_file)
        elif log_file == 'stderr':
            hdlr = logging.StreamHandler(sys.stderr)
        elif log_file == 'stdout':
            hdlr = logging.StreamHandler(sys.stdout)
        else:
            # Allow the user to symbolically specify the TEAL_LOG_DIR in their file name
            template_file = string.Template(log_file)
            log_dir = registry.get_service(TEAL_LOG_DIR)
            full_filename = template_file.substitute({TEAL_LOG_DIR:log_dir})
            hdlr = logging.FileHandler(full_filename)

        # Set the logging format for this logger
        use_eli = extra_log_id
        if len(use_eli) != 0:
            use_eli = extra_log_id[:4]
            use_eli = use_eli.strip()
            use_eli = use_eli + ':'
            
        log_format =  "%(asctime)-15s [%(process)d:%(thread)d] {0}%(module)s - %(levelname)s: %(message)s".format(use_eli)
        formatter = logging.Formatter(log_format)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        
        
        # Define the string levels and set them in the logger
        levels = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}
        
        # Set the lowest level of message to log
        level = levels.get(msg_level, logging.NOTSET)
        logger.setLevel(level)
        registry.register_service(SERVICE_LOGGER, logger)
        registry.register_service(SERVICE_MSG_LEVEL, msg_level)
        registry.register_service(SERVICE_LOG_FILE, log_file)
                
        return logger
    
    def init_location_service(self):
        ''' Load the Location Service based on the XML configuration in the configuration file
        '''
        cfg_reg = registry.get_service(SERVICE_CONFIGURATION)
        for (section,name) in cfg_reg.get_entries(CONFIG_LOCATION):
            location_file = cfg_reg.get(section,'config')
            data_dir = registry.get_service(TEAL_DATA_DIR)
            teal_loc_file_path = os.path.join(data_dir,location_file)
            registry.register_service(SERVICE_LOCATION,LocationService(teal_loc_file_path))
        return
            
    def init_metadata_service(self):
        ''' Load the Location Service based on the XML configuration in the configuration file
        '''
        event_metadata = Metadata(META_TYPE_EVENT, [])
        registry.register_service(SERVICE_EVENT_METADATA, event_metadata)
        alert_metadata = Metadata(META_TYPE_ALERT, [])
        registry.register_service(SERVICE_ALERT_METADATA, alert_metadata)
        cfg_reg = registry.get_service(SERVICE_CONFIGURATION)
        # Get the package entries
        for (section, name) in cfg_reg.get_entries(CONFIG_PACKAGE):
            get_logger().debug('Loading metadata from config package entry %s' % name)
            for option in cfg_reg.options(section):
                if option == 'alert_metadata':
                    alert_files = cfg_reg.get(section,'alert_metadata')
                    if alert_files is not None: 
                        alert_metadata.add_files(alert_files.split(','))
                elif option == 'event_metadata':
                    event_files = cfg_reg.get(section, 'event_metadata')
                    if event_files is not None:
                        event_metadata.add_files(event_files.split(','))
                else:
                    # Only those two options right now
                    pass
        return
    
    def init_persistence_services(self, commit_alerts):
        ''' Initialize the services to persist and work with Events and Alerts
        '''
        alert_mgr = AlertMgr(commit_alerts)
        registry.register_service(SERVICE_ALERT_MGR, alert_mgr)
        return
          
    def init_checkpoint_service(self, commit_checkpoints, restart):
        ''' Initialize the checkpoint service 
        '''
        if commit_checkpoints is None:
            use_db = (registry.get_service(SERVICE_RUN_MODE)=='realtime')
        else:
            use_db = commit_checkpoints
            
        checkpoint_mgr = CheckpointMgr(use_db=use_db, restart_mode=restart)  
        registry.register_service(SERVICE_CHECKPOINT_MGR, checkpoint_mgr)
        return 

    def load_plugins(self,plugins):
        ''' Load the class from the module as defined in the configuration file
        
        This function will yield after each class is loaded to allow the calling
        routine to do the proper construction of the class that is loaded. It pass
        a tuple back that includes the class object, the name of the object and
        the section of the configuration file it is loading so it can pass any additional
        constructor configuration information
        '''
        cf_reg = registry.get_service(SERVICE_CONFIGURATION)
        for (section, name) in cf_reg.get_entries(plugins):
            enabled_val = cf_reg.get(section, 'enabled')
            if  enabled_val == 'false':
                continue
            elif enabled_val == 'realtime':
                if registry.get_service(SERVICE_RUN_MODE) != RUN_MODE_REALTIME:
                    continue
            elif enabled_val == 'historic':
                if registry.get_service(SERVICE_RUN_MODE) != RUN_MODE_HISTORIC:
                    continue
            elif enabled_val != 'all':
                raise ConfigurationError('Unrecognized value for enabled keyword: {0}'.format(enabled_val))

            try:
                module_name, class_name = cf_reg.get(section,'class').rsplit('.', 1)
                module = __import__(module_name, globals(), locals(), [class_name])
            except ImportError,ie:
                get_logger().error(ie)
                raise # throw the ImportError up the chain
            plugin_class = getattr(module, class_name)
            yield (plugin_class, name, section)

    
    def init_processing_pipe(self):
        '''Setup the pipe to process the events through the analyzers,
        Filters and Listeners
        '''
        pipe_str_list = []
        #Setup the queues
        event_q = ListenableQueue('Event input Q', self.event_not_analyzed_callback)
        registry.register_service(SERVICE_EVENT_Q, event_q)
        
        alert_analyzer_q = ListenableQueue('Alert Analyzer input Q', self.alert_not_analyzed_callback)
        registry.register_service(SERVICE_ALERT_ANALYZER_Q, alert_analyzer_q)        
        
        alert_delivery_q = ListenableQueue('Alert Delivery Q', self.event_not_analyzed_callback)
        registry.register_service(SERVICE_ALERT_DELIVERY_Q, alert_delivery_q)
        
        # Get configuration
        cf_reg = registry.get_service(SERVICE_CONFIGURATION)

        # Setup the event analyzers
        # For each configured event analyzer
        #   create using inQ as event_q and outQ as alert_analyzer_q
        count = 0
        analyzer_names = [] # All (event and alert)
        for (analyzer, analyzer_name, section) in self.load_plugins(CONFIG_EVENT_ANALYZERS):
            count += 1
            pipe_str_list.append('EA:{0}'.format(analyzer_name))
            get_logger().debug('adding event analyzer: {0}'.format(analyzer_name))
            analyzer_names.append(analyzer_name)
            analyzer(analyzer_name, event_q, alert_analyzer_q, dict(cf_reg.items(section)), count) 
        
        # For each configured alert analyzer
        #   create using inQ as event_q, alert_analyzer_q and outQ as alert_filter_q
        count = 0
        for (analyzer, analyzer_name, section) in self.load_plugins(CONFIG_ALERT_ANALYZERS):
            count += 1
            pipe_str_list.append('AA:{0}'.format(analyzer_name))
            get_logger().debug('adding alert analyzer: {0}'.format(analyzer_name))
            analyzer_names.append(analyzer_name)
            analyzer(analyzer_name, event_q, alert_analyzer_q, alert_delivery_q, dict(cf_reg.items(section)), count)
        # Configure Filters and Listeners
        alert_delivery = AlertDelivery(alert_delivery_q)
        registry.register_service(SERVICE_ALERT_DELIVERY, alert_delivery)

        # Add Filters
        for (aFilter, filter_name, section) in self.load_plugins(CONFIG_ALERT_FILTERS):
            pipe_str_list.append('F:{0}'.format(filter_name))
            get_logger().debug('adding filter: {0}'.format(filter_name))
            alert_delivery.add_filter(aFilter(filter_name, dict(cf_reg.items(section))))
            
        # Add Listeners
        for (listener, listener_name, section) in self.load_plugins(CONFIG_ALERT_LISTENERS):
            pipe_str_list.append('L:{0}'.format(listener_name))
            get_logger().debug('adding listener: {0}'.format(listener_name))
            alert_delivery.add_listener(listener(listener_name, dict(cf_reg.items(section))))

        # Resolve and validate delivery
        get_logger().debug('Resolve and validate alert delivery')
        alert_delivery.resolve_and_validate(analyzer_names)
        
        get_logger().debug('Completed loading of pipeline')
        return pipe_str_list
    
    def init_db_interface(self):
        ''' Setup the underlying data store connection '''
        cf_reg = registry.get_service(SERVICE_CONFIGURATION)

        singleton_created = False
        for data_store in self.load_plugins(CONFIG_DB_INTERFACE):
            if (not singleton_created):
                registry.register_service(SERVICE_DB_INTERFACE, data_store[0](dict(cf_reg.items(data_store[2]))))
                singleton_created = True
            else:
                raise TealError('Invalid secondary data store configured - {0}'.format(data_store[1]))
            
        if self.daemon_mode:
            # Make sure the DB is up and running before we continue, since this might be 
            # being invoked during IPL and order of startup is not guaranteed
            timeout = 180
            db_exception = None
            dbi = registry.get_service(SERVICE_DB_INTERFACE)
            while (timeout > 0):
                try:
                    cnxn = dbi.get_connection()
                    cnxn.close()
                    break
                except Exception, e:
                    db_exception = e
                    time.sleep(3)
                    timeout -= 3
                    
            if timeout <= 0:
                raise TealError("Cannot connect to database: {0}".format(db_exception))
                    
                    
        return
    
    def init_monitor(self,restart):
        ''' Setup the event monitor. 
        
            There must only be one monitor configured and must be called 
            after the processing pipeline is set up so that

            1) There is an queue to connect up to
            2) Events will be processed and not dropped
        '''
        cf_reg = registry.get_service(SERVICE_CONFIGURATION)

        singleton_created = False
        for monitor in self.load_plugins(CONFIG_EVENT_MONITORS):
            if (not singleton_created):
                tmp_mon_class = monitor[0]
                tmp_conf_dict = dict(cf_reg.items(monitor[2]))
                singleton_created = True
            else:
                raise TealError('Invalid secondary monitor configured - {0}'.format(monitor[1]))
        registry.register_service(SERVICE_EVENT_MONITOR, tmp_mon_class(restart, tmp_conf_dict))
        return

    def event_not_analyzed_callback(self, event):
        '''When the event is not handled by any analyzer this will be called'''
        if isinstance(event, Event):
            get_logger().warning('Event {0} was not analyzed in Event Queue'.format(event.brief_str()))
        else:
            get_logger().debug('Command {0} was not analyzed in Event Queue'.format(event.brief_str()))
        return
    
    def alert_not_analyzed_callback(self, alert):
        ''' When an alert is not handled in the alert analyzer queue pass it to the filter queue'''
        get_logger().debug('Alert not handled by alert analyzer, move to filter q')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).put_nowait(alert)
        return
    
    def shutdown(self):
        logger = get_logger()
        logger.info('TEAL({0}) shutting down'.format(id(self)))
        
        if (not self.data_only):
            # Cleanup the monitor which will start the rest of the pipeline to shutdown
            monitor = registry.get_service(SERVICE_EVENT_MONITOR)
            if monitor is not None:
                monitor.shutdown()
                
            # Cleanup the processing pipeline from front to back
            event_q = registry.get_service(SERVICE_EVENT_Q)
            if event_q is not None:
                event_q.shutdown()
        
            aa_q = registry.get_service(SERVICE_ALERT_ANALYZER_Q)
            if aa_q is not None:
                aa_q.shutdown()
        
            ad_q = registry.get_service(SERVICE_ALERT_DELIVERY_Q)
            if ad_q is not None:
                ad_q.shutdown()
        
        # Cleanup the Metadata Services
        pass # Nothing to do at this time
    
        # Cleanup the Location Service
        pass # Nothing to do at this time

        # Cleanup the Configuration Service
        pass # Nothing to do at this time
        
        # Cleanup the environment
        pass # Nothing to do at this time
    
        # Cleanup persistance services
        c_mgr = registry.get_service(SERVICE_CHECKPOINT_MGR)
        if c_mgr is not None:
            c_mgr.shutdown()
        alert_mgr = registry.get_service(SERVICE_ALERT_MGR)
        if alert_mgr is not None:
            alert_mgr.shutdown()
    
        # Cleanup the registry       
        registry.clear()

        # Clean up the log service 
        # NOTE: out-of-order from construction so final goodbye can be logged
        logger.info('TEAL({0}) shutdown complete'.format(id(self)))        

def app_terminate(sig,stack_frame):
    ''' Initiate application termination on signal from the user '''
    shutdown = registry.get_service(SERVICE_SHUTDOWN)
    if (shutdown is not None):
        shutdown.notify()
    
def main():
    """ Main function entry point for application
    """
    parser = command.TealOptionParser(qry_info,epilog='')
    
    # Common options
    parser.add_option('-c', '--configfile', help=_('fully qualified TEAL config file/directory - optional'), dest='config_file', default=None)
    parser.add_option('-l', '--logfile', help=_('fully qualified log file'), dest='log_file', default=None)
    parser.add_option('-m', '--msglevel',
                      help=_('<debug | info | warning | error | critical> - optional [default: info]'),
                      choices=['debug','info', 'warning', 'error', 'critical'],
                      dest='msg_level',
                      default='info')
    
    # Realtime options
    parser.add_option('', '--realtime', help=_('Run TEAL in realtime mode'), action='store_true', dest='realtime', default=False)
    parser.add_option('-d', '--daemon', help=_('run as a daemon'), action='store_true', dest='daemon', default=False)
    parser.add_option('-r', '--restart',
                      help=_('<now | begin | recovery | lastproc> [default: recovery]'),
                      choices=['now', 'begin', 'recovery', 'lastproc'],
                      dest='restart',
                      default=None)

    # Historic options
    parser.add_option('', '--historic', help=_('Run TEAL in historic mode'), action='store_true', dest='historic', default=False)
    parser.add_option('-q', '--query',
                      type='string',
                      action='callback',
                      callback=parser.query_str_check,
                      dest='query',
                      default='',
                      help=_('Query parameters used to limit the range of events.'))
    parser.add_option('', '--commit', help=_('Commit alerts in historic mode [default=False]'), action='store_true', dest='commit', default=None)
    parser.add_option('', '--occurred', help=_('Use time occurred instead of time logged [default=False]'), action='store_true', dest='occurred', default=False)

    # Parse and validate options    
    (options, args) = parser.parse_args()
    
    if args:
        parser.error(_("Arguments '{0}' cannot be specified").format(','.join(args)))
        
    if (options.historic and options.daemon):
        parser.error(_('--historic and --daemon are mutually exclusive'))
    
    if options.daemon or options.realtime:
        # Set default values
        mode = RUN_MODE_REALTIME

        # Test for invalid options combinations
        if options.query != '':
            parser.error(_('Query option is only valid in historic mode'))
            
        if options.commit is not None: 
            parser.error(_('Commit option is only valid in historic mode'))
        else:
            options.commit = True
            
        if options.occurred:
            parser.error(_('Occurred option is only valid in historic mode'))
    else:
        # Set default values
        mode = RUN_MODE_HISTORIC
            
        if options.commit is None: 
            options.commit = False

        # Test for invalid options combinations            
        if options.restart is not None:
            parser.error(_('Restart option is only valid in realtime mode'))
            
    if options.daemon:
        # Do the necessary processing to spin off as a daemon
        command.daemonize('teal')
    else:
        # Allow the user to CTRL-C application and shutdown cleanly        
        signal.signal(signal.SIGINT, app_terminate)    # CTRL-C
            
    # Allow termination to shutdown cleanly        
    signal.signal(signal.SIGTERM, app_terminate)   # Process Termination

    # Create the TEAL object - it will start running autonomously                        
    Teal(options.config_file,
         logFile=options.log_file, 
         msgLevel=options.msg_level, 
         restart=options.restart, 
         run_mode=mode, 
         historic_qry=options.query,
         commit_alerts=options.commit,
         daemon_mode=options.daemon,
         use_time_occurred=options.occurred)
    
    # Wait for Teal to shutdown before exiting
    shutdown = registry.get_service(SERVICE_SHUTDOWN)
    shutdown.wait()

    return

if __name__ == '__main__':   
    main()
    
