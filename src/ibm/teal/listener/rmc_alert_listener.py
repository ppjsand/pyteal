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

import subprocess
import os

from ibm.teal.util import command
from ibm.teal.listener.alert_listener import AlertListener
from ibm.teal.registry import get_logger

class RmcAlertListener(AlertListener):
    '''
    This class is responsible for receiving alerts and putting them out into the RMC 
    ether for other interested parties. The users can register conditions and responses
    based on the sensor used here and receive the alert as a JSON formatted output string
    '''

    def __init__(self, name, config_dict=None):
        '''
        Constructor
        '''
        self.sensor = 'TealSendAlert'
        AlertListener.__init__(self, name, config_dict)
    
    def process_alert(self, alert):
        ''' Send the alert to the RMC sensor as a JSON formatted string 
        '''
        writer = command.JSONEventEncoder()
        alert_str = writer.encode(alert.write_to_dictionary())
        
        try:
            with open(os.devnull, 'w') as fnull:
                subprocess.check_call(['/usr/bin/refsensor', self.sensor,'String=\'{0}\''.format(alert_str)], stderr=subprocess.STDOUT, stdout=fnull)
        except subprocess.CalledProcessError, cpe:
            get_logger().info('Failed to update sensor({0}): {1}'.format(self.sensor,cpe))
        except OSError, ose:
            get_logger().info('Failed to update sensor({0}): {1}'.format(self.sensor,ose))
        
