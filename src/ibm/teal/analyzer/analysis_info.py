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
from ibm.teal.teal_error import XMLParsingError
from ibm.teal.analyzer.gear.common import GRSE_GEAR_CTL
from ibm.teal.analyzer.gear.control import GCTL_DEFAULT_EVENT_COMP

# Common analysis info
AI_ID = 'id'
AI_COMP = 'comp'
AI_NAME = 'name'
AI_MIN_TIME_IN_POOL = 'min_time_in_pool'
AI_POOL_EXT_TIME = 'pool_extension_time'


class AnalysisInfo(object): 
    '''
    Dictionary of analysis info
    '''

    def __init__(self, ruleset):
        '''
        Initialize the Analysis info dictionaries
        '''
        get_logger().debug('Creating Analysis Info')
        self.ruleset = ruleset
        self.event_info = {}  # key is (comp, id)
        self.alert_info = {}
        self.event_trace_id = (0, 'EventAnalysisInfo')
        self.alert_trace_id = (0, 'AlertAnalysisInfo')
        self.event_default = AnalysisInfoEvent('DEFAULT', 'DUMMY')
        return
    
    def __str__(self):
        '''Print out the analysis info'''
        outstr = 'Event Analysis Info: \n'
        if len(self.event_info) == 0:
            outstr += '  No entries\n'
        else:
            for key in self.event_info:
                outstr += '  ' + str(key) + ' = ' + str(self.event_info[key])
        outstr += 'Alert Analysis Info: \n'
        if len(self.alert_info) == 0:
            outstr += '  No entries\n'
        else:
            for key in self.alert_info:
                outstr += '  ' + str(self.alert_info[key])
        return outstr
    
    def get_constants(self, type):
        '''Get constants defined in the analysis info for the specified type
        
        returns dictionary: { constant:event_id, ... },
         'alert_id': { constant:alert_id, ... }}
         where the first key is the type of the constant entry
        '''
        out_dict = {}
        if type == 'event_id':
            for key in self.event_info:
                info = self.event_info[key]
                if info[AI_NAME] is not None:
                    # TODO: URGENT: should this return the component?!
                    out_dict[info[AI_NAME]] = info[AI_ID]
#        elif type == 'alert_id':
#            for alert in self.alert_info:
#                info = self.alert_info[alert]
#                if info[AI_NAME] is not None:
#                    out_dict[info[AI_NAME]] = info[AI_ID]
        else:
            get_logger().warning('Unexpected type {0}'.format(type))
        return out_dict
    
    def get_analysis_info_event(self, event):
        '''Get the info dictionary for the event'''
        key = (event.get_src_comp(), event.get_event_id())
        # These are required on an event, so assume they are good
        if key not in self.event_info:
            return self.event_default
        return self.event_info[key]
    
    def check_for_analysis_info_event(self, comp, event_id):
        ''' check if entry for the specified comp and event id exists'''
        key = (comp, event_id)
        if key not in self.event_info:
            return False
        return True
        
#    def get_analysis_info_alert(self, alert):
#        '''Get the info dictionary for the alert'''
#        id = alert.get_alert_id()
#        if id is None or id not in self.alert_info:
#            return None
#        return self.alert_info[id]        
        
    def add_event_info(self, event_id, comp, pool_extension, min_time_in_pool):
        '''Add and event entry directly '''
        key = (comp, event_id)
        info = AnalysisInfoEvent(event_id, comp)
        if pool_extension is not None:
            info.update_entry(AI_POOL_EXT_TIME, pool_extension)
        if min_time_in_pool is not None:
            info.update_entry(AI_MIN_TIME_IN_POOL, min_time_in_pool)
        info.check_validity()
        # TODO More validation?
        # p rint 'adding event_id ' + str(event_id)
        self.event_info[key] = info
        return
        
    def add_event_info_xml(self, xml_events_element, trace_dict):
        '''Add event info defined in an XML events element'''
        self.event_trace_id = trace_dict[xml_events_element]
        default_comp = self.ruleset[GRSE_GEAR_CTL][GCTL_DEFAULT_EVENT_COMP]
        for event_entry in xml_events_element:
            entry_name = event_entry.tag.split('}')[-1]
            if entry_name != 'event':
                raise XMLParsingError('Event analysis info error: unexpected element {0}'.format(entry_name))
            event_id = event_entry.attrib['id']
            info = AnalysisInfoEvent(event_id, default_comp)
            for attr_id in event_entry.attrib:
                info.update_entry(attr_id, event_entry.attrib[attr_id])
            info.check_validity()
            key = (info[AI_COMP],info[AI_ID])
            if key in self.event_info:
                get_logger().warning('Duplicate analysis info, ignoring entry in for id {0}'.format(event_id))
                continue
            else:
                pass
                #get_logger().debug('Found event entry key={0}'.format(key))
            self.event_info[key] = info
        return
 
#    def add_alert_info_xml(self, xml_alerts_element, trace_dict):
#        '''Add alert info defined in an XML alerts element'''
#        self.alert_trace_id = trace_dict[xml_alerts_element]
#        for alert_entry in xml_alerts_element:
#            entry_name = alert_entry.tag.split('}')[-1]
#            if entry_name != 'alert':
#                raise XMLParsingError('Alert analysis info error: unexpected element {0}'.format(entry_name))
#            alert_id = alert_entry.attrib['id']
#            if alert_id in self.alert_info:
#                get_logger().warning('Duplicate analysis info, ignoring entry in for id {0}'.format(alert_id))
#                continue
#            else:
#                pass
#                #get_logger().debug('Found entry {0}'.format(alert_id))
#            info = AnalysisInfoAlert(alert_id)
#            for attr_id in alert_entry.attrib:
#                info.update_entry(attr_id, alert_entry.attrib[attr_id])
#            info.check_validity()
#            self.alert_info[alert_id] = info
#        return
    
    def check_min_lt(self, max_value):
        ''' Check that all entries that have a min time in pool value have
        a value less than the specified value'''
        result = True
        for key in self.event_info:
            if self.event_info[key][AI_MIN_TIME_IN_POOL] is not None and  \
               self.event_info[key][AI_MIN_TIME_IN_POOL] > max_value:
                get_logger().error('Event info value for {0} is {1} which exceeds {2}'.format(str(key),str(self.event_info[key][AI_MIN_TIME_IN_POOL]),str(max_value)))
                result = False
#        for key in self.alert_info:
#            if self.alert_info[key][AI_MIN_TIME_IN_POOL] is not None and  \
#               self.alert_info[key][AI_MIN_TIME_IN_POOL] > max_value:
#                get_logger().error('Event info value for {0} is {1} which exceeds {2}'.format(str(key),str(self.alert_info[key][AI_MIN_TIME_IN_POOL]),str(max_value)))
#                result = False
        return result
                 
        
class AnalysisInfoEvent(dict):
    '''Event Analysis Info 
    '''

    def __init__(self, event_id, default_comp, pool_ext=0, min_time_in_pool=0):
        '''Construct the event info from the id and set defaults
        '''
        dict.__init__(self)
        # Required
        self[AI_ID] = event_id
        self[AI_COMP] = default_comp  
        # Optional with default values
        self[AI_NAME] = None
        self[AI_POOL_EXT_TIME] = pool_ext
        self[AI_MIN_TIME_IN_POOL] = min_time_in_pool
        return
    
    def __str__(self):
        '''Print out the event analysis info '''
        outstr = 'id=' + str(self['id']) 
        if self[AI_COMP] is not None:
            outstr += ' comp=' + str(self[AI_COMP])
        if self[AI_NAME] is not None:
            outstr += ' name=' + self[AI_NAME]
        if self[AI_POOL_EXT_TIME] != 0:
            outstr += ' ext=' + str(self[AI_POOL_EXT_TIME])
        if self[AI_MIN_TIME_IN_POOL] is not None:
            outstr += ' min=' + str(self[AI_MIN_TIME_IN_POOL])
        outstr += '\n'
        return outstr         
        
    def update_entry(self, key, value):
        '''Update the entry ... if entry for key does not exist then fail'''
        if (key in self):
            # Conversions if necessary
            if key == AI_NAME or key == 'id' or key == AI_COMP:
                self[key] = value
            else: 
                self[key] = int(value)
        else:
            raise XMLParsingError('Event analysis info error: unexpected element {0}'.format(key))
        return
        
    def check_validity(self):
        '''Make sure all of the required fields were specified
        '''
        # No required fields at this time
        if len(self[AI_ID]) > 8:
            raise XMLParsingError('Event id {0} is longer than 8 characters'.format(self[AI_ID]))
        if len(self[AI_ID]) == 0:
            raise XMLParsingError('Event id {0} must be at least 1 character'.format(self[AI_ID]))
        if self[AI_NAME] is not None and len(self[AI_NAME]) == 0:
            raise XMLParsingError('Event id {0} name must be at least 1 character'.format(self[AI_ID]))   
        if self[AI_MIN_TIME_IN_POOL] is not None and self[AI_MIN_TIME_IN_POOL] < 0:
            raise XMLParsingError('Event id {0} minimum time in pool must be positive'.format(self[AI_ID]))                                                                 
        if self[AI_POOL_EXT_TIME] < 0:
            raise XMLParsingError('Event id {0} pool extension time must be positive'.format(self[AI_ID])) 
        if self[AI_COMP] is None:
            raise XMLParsingError('Event {0} in events section must have a component specified'.format(self[AI_ID]))                                                                                                                                                                                                                
        return
    
        
#class AnalysisInfoAlert(dict):
#    '''Alert Analysis Info 
#    '''
#
#    def __init__(self, alert_id):
#        '''Construct the alert info from the id and set defaults
#        '''
#        dict.__init__(self)
#        # Required
#        self['id'] = alert_id
#        # Optional with default values   
#        self[AI_NAME] = None
#        self[AI_POOL_EXT_TIME] = 0
#        self[AI_MIN_TIME_IN_POOL] = None
#        return
#    
#    def __str__(self):
#        '''Print out the alert analysis info '''
#        outstr = 'id=' + str(self['id'])
#        if self[AI_NAME] is not None:
#            outstr += ' name=' + self[AI_NAME]
#        if self[AI_POOL_EXT_TIME] != 0:
#            outstr += ' ext=' + str(self[AI_POOL_EXT_TIME])
#        if self[AI_MIN_TIME_IN_POOL] is not None:
#            outstr += ' min=' + str(self[AI_MIN_TIME_IN_POOL])
#        outstr += '\n'
#        return outstr         
#    
#    def update_entry(self, key, value):
#        '''Update the entry ... if entry for key donesn't exist then fail'''
#        if (key in self):
#            # Conversion if necessary
#            if key == AI_NAME or key == 'id':
#                self[key] = value
#            else: 
#                self[key] = int(value)
#        else:
#            raise XMLParsingError('Alert analysis info error: unexpected element {0}'.format(key))
#        return
#        
#    def check_validity(self):
#        '''Make sure the entry is valid
#        '''
#        # No required fields at this time
#        if len(self[AI_ID]) > 8:
#            raise XMLParsingError('Alert id {0} is longer than 8 characters'.format(self[AI_ID]))
#        if len(self[AI_ID]) == 0:
#            raise XMLParsingError('Alert id {0} must be at least 1 character'.format(self[AI_ID]))
#        if self[AI_NAME] is not None and len(self[AI_NAME]) == 0:
#            raise XMLParsingError('Alert id {0} name must be at least 1 character'.format(self[AI_ID])) 
#        if self[AI_MIN_TIME_IN_POOL] is not None and self[AI_MIN_TIME_IN_POOL] < 0:
#            raise XMLParsingError('Alert id {0} minimum time in pool must be positive'.format(self[AI_ID]))                                                                 
#        if self[AI_POOL_EXT_TIME] < 0:
#            raise XMLParsingError('Alert id {0} pool extension time must be positive'.format(self[AI_ID]))                                                                 
#        return
#    