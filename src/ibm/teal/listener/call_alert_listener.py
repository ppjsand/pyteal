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

import subprocess
import threading
import os.path

from ibm.teal import registry
from ibm.teal.util import command
from ibm.teal.alert import ALERT_COLS_SELECT
from ibm.teal.registry import get_logger
from ibm.teal.listener.alert_listener import AlertListener

class CallAlertListener(AlertListener):
    '''
    This alert listener will call an external program. The program must reside in the
    data directoroy stucture to maintain security.
    '''

    def __init__(self, name, config_dict=None):
        '''
        Constructor
        '''
        if config_dict is None or 'program' not in config_dict:
            raise ValueError, '{0}: must configure a program to call'.format(name)

        self.program = config_dict['program']
        if not os.path.isabs(self.program):
            raise ValueError, '{0} must be specified with an absolute path'.format(self.program)
        
        AlertListener.__init__(self, name, config_dict)

    def external_call(self, args):
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError, cpe:
            get_logger().error('External program failed: {0}'.format(cpe))
        except OSError, ose:  
            get_logger().error('{0} failed: {1}'.format(args[0], ose))

    def process_alert(self, alert):
        ''' Take the alert and call the external program. The program will be called with the 
        TEAL_DATA_DIR as the "root" dir, if a path is specified.
        '''
        
        data_dir = registry.get_service(registry.TEAL_DATA_DIR)
        program_to_call = [data_dir + self.program]

        alert_dict = alert.write_to_dictionary()
        program_parms = [str(alert_dict.get(key,'None')) for key in ALERT_COLS_SELECT]
        program_to_call.extend(program_parms)
        
        # Spawn it into a thread so it doesn't hold up other listeners
        ext_call = threading.Thread(target=self.external_call, args=(program_to_call,))
        ext_call.daemon = True
        ext_call.start()
        
