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
from ibm.teal.analyzer.gear.rule_condition import GearCondition,\
    _dump_truth_space
from ibm.teal.analyzer.gear.rule_action import GearAction


class GearRule(object):
    '''
    Gear rule 
    '''
    
    def __init__(self, init_xml_element, trace_dict, context):
        '''
        Constructor
        '''
        self.name = ''
        self.description = ''
        self.condition = None
        self.action = None
        self.cur_event = None
        #self.cur_event = None
        self.trace_id = (0, 'rule')   # will be completed when read in name
        self.context = context
        if init_xml_element is not None:
            self._read_from_xml(init_xml_element, trace_dict)
        return
     
    def __str__(self):
        # TODO: Put in xml format?
        outstr = 'Rule ' + self.name + '\n'
        outstr += '  Desc: ' + self.description + '\n'
        outstr += '  Condition:\n'
        if self.condition is None:
            outstr += ' None'
        else:
            outstr += str(self.condition) + '\n'
        outstr += '  Action:\n'
        if self.action is None:
            outstr += ' None'
        else:
            outstr += str(self.action) + '\n'
        return outstr
    
    def _read_from_xml(self, xml_element, trace_dict):
        '''Add event info defined in an XML events element'''
        self.trace_id = trace_dict[xml_element]
        # attributes
        for att_key in xml_element.attrib:
            if att_key == 'name':
                self.name = xml_element.attrib['name'].strip()
            else:
                self.context.parse_error(self.trace_id[0], 'rule element encountered an unexpected attribute: {0}'.format(att_key))
        # elements
        for rule_element in xml_element:
            element_name = rule_element.tag.split('}')[-1]
            element_value = rule_element.text
            if element_name == 'condition':
                self.condition = GearCondition(rule_element, trace_dict, self.context)
            elif element_name == 'action':
                self.action = GearAction(rule_element, trace_dict, self.context)
            elif element_name == 'description':
                self.description = element_value
            else:
                self.context.parse_error(self.trace_id[0], 'rules element encountered an unexpected element \'{0}\''.format(element_name))
        return
    
    def resolve_and_validate(self):
        ''' Resolve and validate the rules '''
        if self.condition is None or self.action is None:
            self.context.parse_error(self.trace_id[0], '\'rule\' element requires both the \'condition\' and \'action\' sub-elements')
        self.condition.resolve_and_validate(self)
        self.action.resolve_and_validate(self)
        return
       
    def prime(self, event):
        ''' prime the condition ''' 
        #get_logger().debug('priming rule {0} with event {1}'.format(self.name, str(event)))
        self.cur_event = event
        self.condition.prime(event)
        return
    
    def accumulate(self, event):
        ''' Accumulate events '''
        #get_logger().debug('priming rule {0} with event {1}'.format(self.name, str(event)))
        self.cur_event = event
        self.condition.accumulate(event)
        return
    
    def execute_suppression_stage(self, pool, gear_ctl):
        ''' execute the rules '''
        self.cur_event = None
        truth_space = self.condition.get_truth_space(None)
        if truth_space is None or len(truth_space) == 0:
            return 
        # Accumulate suppressions
        for truth_point in truth_space:
            self.action.truth_point = truth_point   # Required to make GEAR variables work
            self.action.execute_accumulate_suppression_stage(truth_point, pool, self)
        # Finalize suppressions
        self.action.execute_finalize_suppression_stage(pool, self)
        return
    
    def execute_alert_stage(self, pool, gear_ctl):
        ''' execute the rules '''
        self.cur_event = None
        # Process create alerts
        if self.action.will_create_alerts() == False:
            return 
        # Not get the true values removing the events that were suppressed
        truth_space = self.condition.get_truth_space(pool.get_suppressed_incidents(), exclude_primes=True)
        if truth_space is None or len(truth_space) == 0:
            return None
        for truth_point in truth_space:
            self.action.truth_point = truth_point   # Required to make GEAR variables work
            self.action.execute_accumulate_alert_stage(truth_point, pool, self)
        return self.action.execute_create_alert_stage(pool, self)
    
    def reset(self):
        '''Reset the rule'''
        self.condition.reset()
        self.action.reset()
        return
    
    def get_cross_ref(self):
        ''' Get a cross reference for this rule
            [ [event_ids_used_in_conditions], [event_ids_used_in_suppressions], [alert_ids]] '''
        result = []
        result.append(self.condition.get_cross_ref())
        result.extend(self.action.get_cross_ref())
        return result
    
    def get_used_locations(self):
        ''' get the used locations '''
        used_locs = set()
        t_used_locs = self.condition.get_used_locations()
        if t_used_locs is not None:
            used_locs.update(t_used_locs)
        t_used_locs = self.action.get_used_locations()
        if t_used_locs is not None:
            used_locs.update(t_used_locs)
        return used_locs
    
    def get_checked_event_info(self):
        ''' Return a list of (comp, event ids) that are processed by this rules condition
            return None if not deterministic (GEAR variable)
        '''
        return self.condition.get_checked_event_info()
    