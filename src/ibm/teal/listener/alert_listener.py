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

from abc import ABCMeta, abstractmethod
from ibm.teal.alert import create_teal_alert

class AlertListener(object):
    '''The Listener class is given alerts that should be reported
    so they can report them 
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, name, config_dict=None):
        '''The constructor'''
        self.name = name
        if config_dict is not None and 'filters' in config_dict:
            self.filters = [f.strip() for f in config_dict['filters'].split(',')]
        else:
            self.filters = []
        return
    
    def get_name(self):
        '''Get the name of the listener.'''
        return self.name
    
    @abstractmethod
    def process_alert(self, alert):
        '''The alert for the listener to process is passed'''
        return
    
    def create_listener_alert(self, alert_id, reason, raw_data, src_name=None, severity='I', urgency='N', 
                              loc_instance=None, recommendation='Contact next level of support'):
        ''' Create an alert for this listener in the alert log and add it to the delivery queue
        
            loc_instance will be added to the end of the TEAL location, if specified and if appropriate to the location type used
            src_name will default to 'TEAL:listener:<name>'
        '''
        if src_name is None:
            src_name = 'TEAL:listener:{0}'.format(self.get_name())
        create_teal_alert(alert_id, reason, raw_data, src_name=src_name, severity=severity,
                          urgency=urgency, loc_instance=loc_instance, recommendation=recommendation)
        return
        
