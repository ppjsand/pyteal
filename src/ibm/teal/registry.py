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
"""Static class that is a service registry for the framework
"""
import exceptions

registry = dict()

SERVICE_LOGGER = 'logger'
SERVICE_EVENT_Q = 'event_q'
SERVICE_ALERT_ANALYZER_Q = 'alert_analyzer_q'
SERVICE_ALERT_DELIVERY_Q = 'alert_filter_q'
SERVICE_ALERT_DELIVERY = 'alert_listener'
SERVICE_LOG_FILE = 'log_file'
SERVICE_MSG_LEVEL = 'msg_level'
SERVICE_CONFIGURATION = 'configuration'
SERVICE_EVENT_MONITOR = 'event_monitor'
SERVICE_DB_INTERFACE = 'db_interface'
SERVICE_EVENT_METADATA = 'event_metadata'
SERVICE_ALERT_METADATA = 'alert_metadata'
SERVICE_LOCATION = 'location'
SERVICE_SHUTDOWN = 'shutdown'
SERVICE_RUN_MODE = 'run_mode'
SERVICE_ALERT_MGR = 'alert_mgr'
SERVICE_EVENT_MGR = 'event_mgr'
SERVICE_NOTIFIER = 'notifier'
SERVICE_HISTORIC_QUERY = 'historic_query'
SERVICE_CHECKPOINT_MGR = 'checkpoint_mgr'
SERVICE_TIME_MODE = 'time_mode'
SERVICE_SHUTDOWN_MODE = 'shutdown_mode'

# These are the valid run modes
RUN_MODE_REALTIME = 'realtime'
RUN_MODE_HISTORIC = 'historic' 

# These are the valid shutdown modes
SHUTDOWN_MODE_DEFERRED = 'deferred'
SHUTDOWN_MODE_IMMEDIATE = 'immediate'

# These services must match their environment variables
TEAL_ROOT_DIR = 'TEAL_ROOT_DIR'
TEAL_DATA_DIR = 'TEAL_DATA_DIR'
TEAL_CONF_DIR = 'TEAL_CONF_DIR'
TEAL_LOG_DIR = 'TEAL_LOG_DIR'

class DuplicateKeyError(exceptions.ValueError):
    ''' Exception to throw on attempt to override a registered service
    '''
    def __init__(self,msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

def register_service(name, service):
    ''' To register a service.
    '''
#    if(name != 'logger'):
#        get_logger().info('Registering {0}'.format(name))
#    else:
#        service.info('Registering {0}'.format(name))
    if (name not in registry):
        registry[name] = service
    else:
        # Cannot use a TealError here because that would cause a circular dependency
        # since TealError uses the logger and must get it through the registry
        raise DuplicateKeyError("Cannot override service '{0}'".format(name))
    return

def unregister_service(name):
    ''' To unregister a service.
    '''
    if name in registry:
        del registry[name]
    return

def get_service(name):
    ''' To get a service from registry.
    '''
    if name in registry:
        return registry[name]
    return None

def clear():
    ''' Remove any residual entries in the registry '''
    registry.clear()

def get_logger():
    '''Helper to get the logger '''
    return get_service(SERVICE_LOGGER)

