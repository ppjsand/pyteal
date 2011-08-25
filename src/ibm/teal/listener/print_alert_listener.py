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

import sys

from ibm.teal.registry import get_logger
from ibm.teal.listener.alert_listener import AlertListener

class PrintAlertListener(AlertListener):
    '''
    classdocs
    '''

    def __init__(self, name, config_dict):
        '''
        Constructor
        '''
        if config_dict is not None and 'prefix' in config_dict:
            self.prefix = config_dict['prefix']
        else:
            self.prefix = ''
        get_logger().debug('Creating PrintAlertListner with prefix {0}'.format(self.prefix))
        AlertListener.__init__(self, name, config_dict)
        return
    
    def process_alert(self, alert):
        get_logger().debug('PrintAlertListener processing alert {0}'.format(repr(alert)))
        print self.prefix + repr(alert) + ' ' + str(alert.raw_data) + ' ' + str(alert.src_name)
        sys.stdout.flush()
        return
        