# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

from ibm.teal.analyzer.gear.external_base_classes import ExtInitAlert
from ibm.teal.analyzer.gear.external_base_classes import ExtEvaluate
from ibm.teal.alert import ALERT_ATTR_REASON, ALERT_ATTR_SEVERITY, ALERT_ATTR_RAW_DATA, dict2raw_data, ALERT_ATTR_RECOMMENDATION
from ibm.teal.connector.tlipmitraphandler import IPMI_EVENT_MSG, IPMI_EVENT_SEVERITY, IPMI_INVALID_EVENT, IPMI_INVALID_EVENT_ID, IPMI_INVALID_LOCATION 
from ibm.teal.connector.tlammtraphandler import AMM_MSG_TEXT, AMM_PRIORITY, AMM_INVALID_EVENT
from ibm.teal.configuration import ConfigurationError
from ibm.teal.registry import get_logger

VALID_SEVERITIES = ['fatal', 'error', 'warning', 'info']
SNMP_IPMI ='IPMI'
SNMP_AMM = 'AMM'

SNMP_UNEXPECTED_EVENTS = [IPMI_INVALID_EVENT, IPMI_INVALID_EVENT_ID, IPMI_INVALID_LOCATION, AMM_INVALID_EVENT]
SNMP_UNEXPECTED_REASON_MSG = "An unexpected error has occurred"
SNMP_UNEXPECTED_RECOMMENDATION = "Call your next level of support"

def _map_ipmi_severity(event_severity):
    ''' Map severity to common value
         INFO:
             0x00 = unspecified
             0x01 = Monitor 00_0001b
             0x02 = Information 00_0010b
             0x04 = OK (return to OK condition) 00_0100b
        
         WARNING:
             0x08 = Non-critical condition 00_1000b a.k.a.warning
        
         ERROR:
             0x10 = Critical condition 01_0000b
        
         FATAL:
             0x20 = Non-recoverable condition    
    '''
    if (event_severity < 0x08):
        severity = 'I'
    elif (event_severity < 0x10):
        severity = 'W'
    elif (event_severity < 0x20):
        severity = 'E'
    else:
        severity = 'F'
        
    return severity

def _map_amm_severity(event_severity):
    ''' Map event severity to common value
    '''
    if (event_severity <= 4):
        severity = 'I'
    elif (event_severity < 8):
        severity = 'W'
    else:
        severity = 'E'
        
    return severity

class MMSeverityFilter(ExtEvaluate):
    ''' This class is responsible for filter events based on the severity configured in the rules file
    '''
    def __init__(self, parm_dict):
        ExtEvaluate.__init__(self, parm_dict)
        self.comps = [SNMP_IPMI, SNMP_AMM]
        self.primes = set()
        self.events = set()
        self.severity_filter = ['F']
        
        if 'severity' not in parm_dict or parm_dict['severity'] is None or parm_dict['severity'] is '':
            raise ConfigurationError('\'severity\' parm is required when using the SeverityFilter evaluate class')
        
        cfg_severity = parm_dict['severity'].strip().lower()
        if (cfg_severity not in VALID_SEVERITIES):
            raise ConfigurationError("'severity' parm is must be one of 'critical, 'error', 'warning', or 'info'")
        elif (cfg_severity == 'error'):
            self.severity_filter.append('E')
        elif (cfg_severity == 'warning'):
            self.severity_filter.extend(('E','W'))
        else:
            self.severity_filter.extend(('E','W','I'))
             
        get_logger().debug('Filtering on severity: {0} '.format(str(self.severity_filter)))

        
    def prime(self, event):
        ''' Prime the condition based on severity
        '''
        if ((event.event_id in SNMP_UNEXPECTED_EVENTS) or
            ((event.src_comp == SNMP_IPMI) and 
             (_map_ipmi_severity(event.raw_data[IPMI_EVENT_SEVERITY]) in self.severity_filter)) or
            ((event.src_comp == SNMP_AMM) and 
             (_map_amm_severity(event.raw_data[AMM_PRIORITY]) in self.severity_filter))):
            self.primes.add(event)
            self.events.add(event)
        else:
            return 

    def accumulate(self, event):
        ''' Accumulate events based on severity
        '''        
        if ((event.event_id in SNMP_UNEXPECTED_EVENTS) or
            ((event.src_comp == SNMP_IPMI) and 
             (_map_ipmi_severity(event.raw_data[IPMI_EVENT_SEVERITY]) in self.severity_filter)) or
            ((event.src_comp == SNMP_AMM) and 
             (_map_amm_severity(event.raw_data[AMM_PRIORITY]) in self.severity_filter))):
            self.events.add(event)
        else:
            return 
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the set of truth points (loc, truth events) that make the condition true '''
        truth_space = set()

        if self.events:
            if exclude_events:
                exclude_set = set(exclude_events)
            else:
                exclude_set = set()
            
            if exclude_primes:
                exclude_set |= self.primes    
             
            candidate_events = self.events - exclude_set 
            
            # Make every event a separate Alert. If two alerts with the same id match the location,
            # they will be consolidated by GEAR
            for e in candidate_events:
                truth_space.add((frozenset((e.src_loc,)), frozenset((e,))))
             
        else:
            # No events to process
            pass
         
        return truth_space;    
        
    def reset(self):
        '''Reset the condition'''
        self.events.clear()
        self.primes.clear()
    

class MMSeverityAlertInit(ExtInitAlert):
    ''' This class is responsible for initializing the Alert for the collected events.
    '''
    
    def update_init_data(self):
        ''' This method is called by update_init_data_main which does setup to simplify the 
        coding of this method.  
       
        This method should modify how the alert should be created by modifying self.init_dict which
        will be filled in prior to it being called and will be returned after this method returns
        ''' 
        
        # Assumes that all the events have the same event id.
        events = self.get_events()
        primary_event = events[0]
        
        # Determine where to get the message based on the event component
        src_comp = primary_event.get_src_comp()
        
        if (primary_event.event_id in SNMP_UNEXPECTED_EVENTS):
            # Set the reason message based on the event data
            self.init_dict[ALERT_ATTR_REASON] = SNMP_UNEXPECTED_REASON_MSG
            self.init_dict[ALERT_ATTR_RECOMMENDATION] = SNMP_UNEXPECTED_RECOMMENDATION            
            self.init_dict[ALERT_ATTR_SEVERITY] = 'E'
            
            # Include any special data in the raw data section
            self.init_dict[ALERT_ATTR_RAW_DATA] = primary_event.raw_data['raw_data']
            
        elif (src_comp == SNMP_IPMI):
            # Set the reason message based on the event data
            self.init_dict[ALERT_ATTR_REASON] = primary_event.raw_data[IPMI_EVENT_MSG]            
            self.init_dict[ALERT_ATTR_SEVERITY] = _map_ipmi_severity(primary_event.raw_data[IPMI_EVENT_SEVERITY])
            
            # Include any special data in the raw data section
            self.init_dict[ALERT_ATTR_RAW_DATA] = dict2raw_data(primary_event.raw_data)
                            
        elif (src_comp == SNMP_AMM):
            # Set the reason message based on the event data
            self.init_dict[ALERT_ATTR_REASON] = primary_event.raw_data[AMM_MSG_TEXT]
            self.init_dict[ALERT_ATTR_SEVERITY] = _map_amm_severity(primary_event.raw_data[AMM_PRIORITY])

            # Include any special data in the raw data section
            self.init_dict[ALERT_ATTR_RAW_DATA] = dict2raw_data(primary_event.raw_data)
                        
        else:
            # Unknown event source, ignore event and do no additional processing
            pass
