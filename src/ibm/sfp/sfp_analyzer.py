# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

'''
Service Focal Point Connector Analyzers
'''

from ibm.teal import registry, alert
from ibm.teal.analyzer.analyzer import EventAnalyzer 

SFP_SRC_COMP = 'SFP'
SFP_REASON = 'description'
SFP_FRU_LIST = 'fru_list'
SFP_PROB_NUM = 'prob_num'

SFP_RECOMMENDATION = "Contact your next level of support. " \
 "For more detail, sign on to the hardware management console (HMC) specified to the right of the 'SFP' keyword in the raw_data field. " \
 "List the serviceable events using the 'Manage Serviceable Events' panels and find the problem number specified to the right of the 'Problem Number' keyword in the raw_data field."

class SFPEventAnalyzer(EventAnalyzer):
    '''
    This event analyzer analyzes events that have been reported by the Service
    Focal Point connector. 
    
    The current implementation is to create an alert for every event that
    has been reported
    '''

    def will_analyze_event(self, event):
        ''' Indicate this analyzer handles all events from the SFP connector
        '''
        if event.get_src_comp() == SFP_SRC_COMP:
            return True
        else:
            return False
        
    def analyze_event(self, event):
        ''' Turn every event from the SFP into an Alert
        '''
        # Build the Alert directly from the event information
        raw_data_dict = {'Problem Number':event.raw_data[SFP_PROB_NUM],
                         'FRU List':eval(event.raw_data[SFP_FRU_LIST]),
                         'SFP':event.get_rpt_loc().get_comp_value('node')}
        
        alert_dict = {alert.ALERT_ATTR_SEVERITY:'E',
                      alert.ALERT_ATTR_URGENCY:'N',
                      alert.ALERT_ATTR_EVENT_LOC_OBJECT:event.get_src_loc(),
                      alert.ALERT_ATTR_RECOMMENDATION:SFP_RECOMMENDATION,
                      alert.ALERT_ATTR_REASON:event.raw_data[SFP_REASON],
                      alert.ALERT_ATTR_RAW_DATA:str(raw_data_dict),
                      alert.ALERT_ATTR_SRC_NAME:self.get_name(),
                      alert.ALERT_ATTR_CONDITION_EVENTS:set((event,))
                      }
        
        # Get the alert manager to create/allocate/commit the alert
        amgr = registry.get_service(registry.SERVICE_ALERT_MGR)
        sfp_alert = amgr.allocate(event.get_event_id(), in_dict=alert_dict)
        
        # Duplicate alerts are already handled by the HMC/SFP so we should not
        # dup them again since they are always different alerts
        amgr.commit(sfp_alert, disable_dup=True)
        
        # Now the alert is created and can be reported through the pipeline
        self.send_alert(sfp_alert)

    def handle_control_msg(self, control_msg):
        ''' Handle any control messages that have been sent. No special action
        required
        '''
        registry.get_logger().debug('Control message received: {0}'.format(control_msg))


