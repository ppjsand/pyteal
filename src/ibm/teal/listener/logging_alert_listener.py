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

from ibm.teal.registry import get_logger
from ibm.teal.listener.alert_listener import AlertListener

class LoggingAlertListener(AlertListener):
    '''
    This listener logs the alerts
    '''

    def __init__(self, name, config_dict):
        '''
        Constructor
        '''
        if config_dict is not None and 'prefix' in config_dict:
            self.prefix = config_dict['prefix']
        else:
            self.prefix = ''
        if config_dict is not None and 'log_level' in config_dict:
            self.log_level = config_dict['log_level']
        else:
            self.log_level = 'debug'
            
        get_logger().debug('Creating LoggingAlertListner with prefix {0}'.format(self.prefix))
        AlertListener.__init__(self, name, config_dict)
        return
    
    def process_alert(self, alert):
        ''' process the alert by logging it '''
        msgout = self.prefix + repr(alert) + ' ' + str(alert.raw_data) + ' ' + str(alert.src_name)
        if self.log_level == 'info':
            get_logger().info(msgout)
        elif self.log_level == 'warning':
            get_logger().warning(msgout)
        elif self.log_level == 'error':
            get_logger().error(msgout)
        elif self.log_level == 'critical':
            get_logger().critical(msgout)
        else:
            get_logger().debug(msgout)
        return
        