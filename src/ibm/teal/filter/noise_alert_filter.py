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

import re

from ibm.teal.filter import alert_filter
from ibm.teal import registry, alert

NOISE_FILTER_MSG_LEVEL = 'msg_level'
NOISE_FILTER_MSG_LEVEL_DEFAULT = 'debug'
NOISE_FILTERS = [alert.ALERT_ATTR_ALERT_ID,
                 alert.ALERT_ATTR_SEVERITY,
                 alert.ALERT_ATTR_URGENCY,
                 alert.ALERT_ATTR_EVENT_LOC_TYPE,
                 alert.ALERT_ATTR_EVENT_LOC,
                 alert.ALERT_ATTR_FRU_LOC,
                 alert.ALERT_ATTR_SRC_NAME]

class NoiseAlertFilter(alert_filter.AlertFilter):
    '''
    This alert filter will filter out any alerts that match the regular expressions for the alert fields
    in the conf file. The fields that can be filtered are
    
    alert_id, severity, urgency, event_loc, event_loc_type, fru_loc, src_name
    
    If multiple fields are specified, the behavior is an AND of all of the listed conditions for the filter
    '''


    def __init__(self, name, config_dict=None):
        '''
        Constructor
        '''
        
        # Get the proper level of logging
        if NOISE_FILTER_MSG_LEVEL in config_dict:
            msg_level = config_dict[NOISE_FILTER_MSG_LEVEL]
        else:
            msg_level = 'debug'
         
        if msg_level == 'error':            
            self.logging_func = registry.get_logger().error
        elif msg_level == 'warn':
            self.logging_func = registry.get_logger().warn
        elif msg_level == 'info':
            self.logging_func = registry.get_logger().info
        else:
            # Default logging is debug level
            msg_level = 'debug'
            self.logging_func = registry.get_logger().debug
            
        registry.get_logger().debug('Noise filter message level: {0}'.format(msg_level))
        
        # Compile all the selected filter fields regx
        self.filters = {}
        for alert_field in NOISE_FILTERS:
            if alert_field in config_dict:
                self.filters[alert_field] = re.compile(config_dict[alert_field])

        alert_filter.AlertFilter.__init__(self, name, config_dict)

    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on.
        '''
        is_filtered = False
        
        # Apply all of the user defined filters
        alert_dict = alert.write_to_dictionary()
        for key in self.filters:
            value = alert_dict.get(key,None)
            if value is not None and self.filters[key].match(value) is not None:
                is_filtered = True
                self.logging_func('{0}: {1} filter true for value {2}'.format(self.get_name(), key, value))
            else:
                is_filtered = False
                self.logging_func('{0}: {1} filter false for value {2}'.format(self.get_name(), key, value))
                break
            
        # Log the fact that the alert was filtered
        if is_filtered:
            self.logging_func('{0} filtered'.format(alert))
            
        return is_filtered
        
    def resolve_and_validate(self, info_dict):
        ''' Resolve and validate any configuration information
        '''
        pass    