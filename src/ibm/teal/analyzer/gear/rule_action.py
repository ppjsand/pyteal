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
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from ibm.teal.alert import ALERT_ATTR_ALERT_ID, \
           ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY, ALERT_ATTR_EVENT_LOC, ALERT_ATTR_EVENT_LOC_TYPE, \
           ALERT_ATTR_FRU_LOC, ALERT_ATTR_RECOMMENDATION, \
           ALERT_ATTR_RAW_DATA, ALERT_ATTR_SRC_NAME, ALERT_ATTR_CONDITION_EVENTS,\
    ALERT_ATTR_MSG_TEMPLATE, ALERT_ATTR_PRIORITY
from ibm.teal.analyzer.gear.common import GRUL_PART_ACTION, GRUL_PART_EXTERNAL
from ibm.teal.analyzer.gear.rule_value import \
    GRVA_TYPE_SET_OF_EVENT_IDS, GRVA_TYPE_SET_OF_EVENTS, \
    GRVA_TYPE_COMP, GRVA_TYPE_SCOPE, GRVA_TYPE_LOC, \
    RuleParms, GRVA_TYPE_ANY, GRVA_TYPE_BOOLEAN,\
    GRVA_TYPE_NONZERO_UINT, GRVA_TYPE_STRING, init_rule_values,\
    resolve_and_validate_rule_values, read_from_xml_rule_value, dump_rule_values,\
    GRVA_TYPE_SET_OF_LOCS
from ibm.teal.registry import get_logger, SERVICE_ALERT_METADATA, get_service,\
    SERVICE_ALERT_MGR
from ibm.teal.teal_error import XMLParsingError
from ibm.teal.analyzer.gear.control import GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS
from ibm.teal.analyzer.gear.external_base_classes import ExtExecute,\
    ExtInitAlert, ExtFatalError

GACT_TYPE_CREATE_ALERT = 'create_alert'
GACT_TYPE_SUPPRESS_EVENTS = 'suppress_events'
GACT_TYPE_EXECUTE = 'execute'

# Variables supported on each action -- controls initialization, reading from XML, and validation
#     Entries in bottom dictionary are var name: (type, init_str, required, static_only)
GACT_VALUES = {GACT_TYPE_CREATE_ALERT:   {
                                           'id':              (GRVA_TYPE_ANY, None, False, False),
                                           'severity':        (GRVA_TYPE_ANY, None, False, False),
                                           'urgency':         (GRVA_TYPE_ANY, None, False, False),
                                           'event_loc':       (GRVA_TYPE_LOC, None, False, False),
                                           'event_loc_scope': (GRVA_TYPE_SCOPE, None, False, True),
                                           'recommendation':  (GRVA_TYPE_ANY, None, False, False),
                                           # reason is not supported because generated from msg_template
                                           'msg_template':    (GRVA_TYPE_ANY, None, False, False),
                                           'fru_loc':         (GRVA_TYPE_ANY, None, False, False),
                                           'raw_data':        (GRVA_TYPE_ANY, None, False, False),
                                           'use_metadata':    (GRVA_TYPE_BOOLEAN, 'true', False, True),
                                           'init_class':      (GRVA_TYPE_STRING, None, False, True),
                                           'priority':        (GRVA_TYPE_NONZERO_UINT, None, False, False),                                        'scope': (GRVA_TYPE_SCOPE, False, False), 
                                         },
               GACT_TYPE_SUPPRESS_EVENTS:{
                                           'ids':        (GRVA_TYPE_SET_OF_EVENT_IDS, None, False, False), 
                                           'events':     (GRVA_TYPE_SET_OF_EVENTS, None, False, False),
                                           'comp':       (GRVA_TYPE_COMP, None, False, True),
                                           'scope':      (GRVA_TYPE_SCOPE, None, False, True),
                                           'locations':  (GRVA_TYPE_SET_OF_LOCS, None, False, False),
                                           'ignore_loc': (GRVA_TYPE_BOOLEAN, 'false', False, True)
                                         },
               GACT_TYPE_EXECUTE:        {
                                           'name':  (GRVA_TYPE_STRING, None, True, True), 
                                           'ext_class': (GRVA_TYPE_STRING, None, True, True)
                                         }
               }


class GearAction(object):
    '''Class to represent a rule action
    '''
    
    def __init__(self, init_xml_element, trace_dict, ruleset):
        '''
        Constructor
        '''
        self.description = ''
        self.actionables = {'execute':[], 'suppress_events':[], 'suppress_alerts':[], 'create_alert':[]}
        self.execute_names = []
        self.suppressions = []
        self.future_suppressions = []
        self.trace_id = (0, 'Action')
        self.ruleset = ruleset
        self.truth_point = None
        if init_xml_element is not None:
            self._read_from_xml(init_xml_element, trace_dict)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the action'''
        for actionable_list_key in self.actionables:
            for actionable in self.actionables[actionable_list_key]:
                actionable.resolve_and_validate(rule)
        return
    
    def will_create_alerts(self):
        ''' Return True if this action will create alerts '''
        return (len(self.actionables['create_alert']) + len(self.actionables['execute']) != 0)
    
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        ''' Execute the suppression stage actions '''
        for key in ['execute', 'suppress_events']:
            for action in self.actionables[key]:
                action.execute_accumulate_suppression_stage(truth_point, pool, rule) 
        return 
    
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Execute the suppression stage actions '''
        for key in ['execute', 'suppress_events']:
            for action in self.actionables[key]:
                action.execute_finalize_suppression_stage(pool, rule) 
        return 
            
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the create alert stage actions '''
        for key in ['execute', 'create_alert']:
            for action in self.actionables[key]:
                action.execute_accumulate_alert_stage(truth_point, pool, rule)
        return
    
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        alerts = []
        for key in ['execute', 'create_alert']:
            for action in self.actionables[key]:
                tmp_alerts = action.execute_create_alert_stage(pool, rule)
                if tmp_alerts is not None and len(tmp_alerts) != 0:
                    alerts.extend(tmp_alerts)
        return alerts
    
    def reset(self):
        '''reset the action'''
        self.new_alerts = []
        self.suppressions = []
        self.future_suppressions = []
        for action in self.actionables['create_alert']:
            action.reset()
        # Nothing more to do because other actionables have no state
        return
    
    def __str__(self):
        outstr = '   Desc: ' + self.description + '\n'
        outstr += '   > ' + str(self.actionables)
        return outstr       
   
    def _read_from_xml(self, xml_element, trace_dict):
        '''Add event info defined in an XML events element'''
        self.trace_id = trace_dict[xml_element]
        # attributes
        if len(xml_element.attrib) != 0:
            att_key = xml_element.attrib[0] #report first one
            self.ruleset.parse_error(self.trace_id[0], 'action element encountered an unexpected attribute: {0}'.format(att_key))
        # elements
        self.trace_id = trace_dict[xml_element]
        for rule_element in xml_element:
            element_name = rule_element.tag.split('}')[-1]
            element_value = rule_element.text
            if element_name == 'description':
                self.description = element_value
            else:
                if element_name in self.actionables:
                    actionable = actionable_creator(rule_element, trace_dict, self.ruleset, self.trace_id)
                    self.actionables[element_name].append(actionable)
                    if element_name == 'execute':
                        self.execute_names.append(actionable.name)
                else:
                    self.ruleset.parse_error(self.trace_id[0],'\'action\' element encountered unexpected sub-element \'{0}\''.format(element_name))
        total_actions = 0
        for actionable_list_key in self.actionables:
            total_actions += len(self.actionables[actionable_list_key])
        if total_actions == 0:
            self.ruleset.parse_error(self.trace_id[0],'\'action\'element must have at least one actionable sub-element')
        return
    
    def get_cross_ref(self):
        ''' Get cross reference information
            [[event_ids_suppressed], [alert_ids_created]] '''
        sup_result = []
        for action in self.actionables['suppress_events']:
            sup_result.extend(action.get_cross_ref())
        ca_result = []
        for action in self.actionables['create_alert']:
            ca_result.extend(action.get_cross_ref())
        return [sup_result, ca_result]
    
    def get_used_locations(self):
        ''' return a set of locations used '''
        used_locs = set()
        for action in self.actionables['suppress_events']:
            t_used_locs = action.get_used_locations()
            if t_used_locs is not None:
                used_locs.update(t_used_locs)
        for action in self.actionables['create_alert']:
            t_used_locs = action.get_used_locations()
            if t_used_locs is not None:
                used_locs.update(t_used_locs)
        return used_locs

def actionable_creator(xml_element, trace_dict, ruleset, trace_id):
    '''Create and return the correct actionable from the xml_element'''
    new_actionable = None
    element_name = xml_element.tag.split('}')[-1]
    if element_name == 'suppress_events':
        if not ruleset.event_input:
            ruleset.parse_error(trace_id[0], 'gear condition element \'{0}\' is not supported for this analyzer'.format(element_name))
        return GearActionableSuppressEvents(xml_element, trace_dict, ruleset)
    elif element_name == 'create_alert':
        return GearActionableCreateAlert(xml_element, trace_dict, ruleset)
    elif element_name == 'execute':
        return GearActionableExecute(xml_element, trace_dict, ruleset)
    else:
        ruleset.parse_error(trace_id[0], 'action element encountered unexpected sub-element \'{0}\''.format(element_name))
    return new_actionable
        
        
class GearActionable(object):
    '''Class to represent an individual evaluation in a condition
    '''
    
    __metaclass__ = ABCMeta
         
    def __init__(self, type, xml_element, trace_dict, ruleset):
        ''' Constructor ''' 
        self.ev_type = type
        self.trace_id = (0, type) 
        self.description = None
        self.ruleset = ruleset
        
        # Initialize values
        init_rule_values(self, GACT_VALUES[self.ev_type])
        # Read the xml
        self._read_from_xml(xml_element, trace_dict)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the evaluatable'''
        try:
            resolve_and_validate_rule_values(self, self.ruleset, rule, GACT_VALUES[self.ev_type], rule_part=GRUL_PART_ACTION)
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], '\'{0}\' element {1}'.format(self.ev_type, e.msg))
        return
    
    @abstractmethod
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate suppression stage actions '''
        pass
   
    @abstractmethod
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Execute the create suppression stage actions '''
        pass
            
    @abstractmethod
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate alert stage actions '''
        pass
    
    @abstractmethod
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        pass

    def _read_from_xml(self, xml_element, trace_dict):
        ''' Read in the evaluatable form the input XML
        '''
        self.trace_id = trace_dict[xml_element]
        # attributes
        for att_key in xml_element.attrib:
            att_value = xml_element.attrib[att_key]
            if read_from_xml_rule_value(self, att_key, att_value, GACT_VALUES[self.ev_type]):
                continue
            elif self._read_from_xml_other_attributes(att_key, xml_element) == True:
                continue
            else:
                self.ruleset.parse_error(self.trace_id[0], '\'{0}\' element encountered an unexpected attribute \'{1}\''.format(self.ev_type, att_key))
        # elements
        # Get description ... if specified
        for rule_element in xml_element:
            element_name = rule_element.tag.split('}')[-1]
            element_value = rule_element.text
            if element_name == 'description':
                self.description = element_value
            else:
                if self._read_from_xml_other_subelements(rule_element, trace_dict) == True:
                    continue
                else:
                    self.ruleset.parse_error(self.trace_id[0], '\'{0}\' element encountered an unexpected subelement: {1}'.format(self.ev_type, element_name))
        return
    
    def _read_from_xml_other_attributes(self, att_key, xml_element):
        ''' Process other attributes '''
        # Default is not processed
        return False
    
    def _read_from_xml_other_subelements(self, xml_element, trace_dict):
        ''' Process other elements '''
        # Default is not processed
        return False
    
    def __str__(self):
        outstr = '<{0} gtp="{1}"'.format(self.ev_type, self.trace_id)
        outstr += dump_rule_values(self, GACT_VALUES[self.ev_type])
        outstr += self._str_attribute_additions()
        outstr += '>\n'
        if self.description is not None and len(self.description) > 0:
            outstr += '<description>{0}</description>\n'.format(self.description)
        outstr += self._str_subelement_additions()
        outstr += '</{0}>\n'.format(self.ev_type)
        return outstr     
    
    def _str_attribute_additions(self):
        ''' Additions to the output str '''
        return ''
    
    def _str_subelement_additions(self):
        ''' Additions to the output str '''
        return ''
    
    def get_cross_ref(self):
        ''' Get cross reference information '''
        pass
    
    def get_used_locations(self):
        return None
    
class GearActionableSuppressEvents(GearActionable):
    '''Evaluate if the current event matches the specified event values'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearActionable.__init__(self, GACT_TYPE_SUPPRESS_EVENTS, xml_element, trace_dict, ruleset)
        return
    
    # __str__ from parent is sufficient
    
    # _read_from_xml from parent is sufficient    
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the action'''
        GearActionable.resolve_and_validate(self, rule)
            
        ## Validate usage (combinations)
        if self.ids.is_set():
            # comp is required if id is used
            if not self.comp.is_set():
                self.ruleset.parse_error(self.trace_id[0], 'suppress_events element requires component to be specified')
            # Make sure that the specified comp, id in the id list can actually occur
            self.ruleset.validate_event_ids(self.comp, self.ids, self.trace_id)
        # Make sure we were asked to do something
        if not self.ids.is_set() and not self.locations.is_set() and not self.events.is_set():
                self.ruleset.parse_error(self.trace_id[0], 'suppress_events element did not specify anything to suppress')
        # Make sure not asked to do more than one something
        if (self.ids.is_set() or self.locations.is_set()) and self.events.is_set():
                self.ruleset.parse_error(self.trace_id[0], 'suppress_events element must specify ids, locations, or events attribute')
        # validate events
        if self.events.is_set():
            if self.scope.in_str is not None:
                self.ruleset.parse_error(self.trace_id[0], 'suppress_events element does not allow scope attribute to be specified with events attribute')
            # Make sure GEAR variable(s)
            if len(self.events.static_list) != 0:
                    self.ruleset.parse_error(self.trace_id[0], 'suppress_events element only supports GEAR variables for the \'events\' attribute')
        # Make sure we aren't given a location and told to ignore it
        if self.ignore_loc.get_value() and self.locations.is_set():
            self.ruleset.parse_error(self.trace_id[0], 'suppress_events element cannot have both \'ignore_loc\' set to true and the \'locations\' attribute set')
        return
        
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        '''Suppress the specified events'''
        sup_events = []
        # if a list was specified, use that 
        if self.events.get_list() is not None:
            sup_events = self.events.get_list()
        else:
            # Get what was specified
            sup_locs = self.locations.get_list()
            # None or empty so either not set or GEAR variable that returned None
            if sup_locs is None or len(sup_locs) == 0:
                # Check if set
                if self.locations.is_set() == True:
                    # GEAR variable so ignore 
                    self.ruleset.trace_debug(self.trace_id[1], 'Locations was set and was None -- GEAR variable so skip suppression')
                    return None
                if self.ignore_loc.get_value() == True:
                    sup_locs = None
                else:
                    # Default to using truth locs
                    sup_locs = list(truth_point[0])
                    # See if really have anything
                    if len(sup_locs) == 0 or sup_locs[0] is None:
                        # Don't, so use the events
                        sup_locs_set = set()
                        for c_event in list(truth_point[1]):
                            sup_locs_set.add(c_event.src_loc)
                        sup_locs = list(sup_locs_set)
                        
            # At this point sup_locs is either a list or None
            id_list = self.ids.get_list()
            use_comp = self.comp.get_value()
            if sup_locs is None:
                # ignore location -- must have ids
                for id in id_list:
                    sup_events.extend([event for event in pool.get_incidents(incident_id=id) if event.get_type() == 'E' and 
                                       event.match(id, use_comp, None, None, None)])
                
            else:
                # use locations  
                use_scope = self.scope.get_value()[1]
                if id_list is None:
                    tmp_event_list = [event for event in pool.get_incidents() if event.get_type() == 'E']
                    for use_loc in sup_locs:
                        sup_events.extend( [event for event in tmp_event_list 
                                            if event.match(None, use_comp, use_loc, None, use_scope)])
                else: 
                    for use_id in id_list:
                        tmp_event_list = [event for event in pool.get_incidents(incident_id=use_id) if event.get_type() == 'E']
                        for use_loc in sup_locs:
                            sup_events.extend( [event for event in tmp_event_list
                                                if event.match(use_id, use_comp, use_loc, None, use_scope)])
      
        # Record the suppression 
        evt_str = ','.join([e.brief_str() for e in truth_point[1]])
        if len(sup_events) == 0:
            sup_str = '-nothing-'
            self.ruleset.trace_debug(self.trace_id[1], '{0} suppressed {1}'.format(evt_str, sup_str))
        else:
            sup_str = ','.join([e.brief_str() for e in sup_events])
            self.ruleset.trace_info(self.trace_id[1], '{0} suppressed {1}'.format(evt_str, sup_str))

        # Associate with the event
        for event in truth_point[1]:
            pool.suppresses(event, set(sup_events))

        return None
    
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Excute the create suppression stage '''
        # All suppressions done during accumulate stage, so nothing to do
        return

    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the create alert stage actions '''
        self.ruleset.trace_warning(self.trace_id[1], 'Error')
        return
    
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        self.ruleset.trace_warning(self.trace_id[1], 'Error')
        return []
    
    def get_cross_ref(self):
        ''' return a list of suppressed event ids '''
        if self.ids.is_set() == True:
            try:
                result = self.ids.get_list()
            except:
                result = self.ids.in_str.split(',')
        else:
            result = []
        return result
    
    def get_used_locations(self):
        ''' If ignore, doesn't use any
            If locations set, then return those
            Otherwise uses whatever conditions used so nothing to add '''
        if self.ignore_loc.get_value() == True:
            return None
        if self.locations.is_set() == True:    
            return set(self.locations.in_str.split(','))
        return None
            
class GearActionableCreateAlert(GearActionable):
    '''Create an alert'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        self.src_name = None
        self.trace_id = (0, 'CreateAlert')
        GearActionable.__init__(self, GACT_TYPE_CREATE_ALERT, xml_element, trace_dict, ruleset)
        self.init_class_callable = None
        self.potential_alerts = defaultdict(dict)
        return
   
    # _read_from_xml from parent is sufficient

    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition'''
        self.src_name = self.ruleset.name
        GearActionable.resolve_and_validate(self, rule)
        
        # Process init class
        if self.init_class.is_set() == False:
            self.init_class_callable = self.ruleset['gear_control'][GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS]
        else:
            try:
                module_name, class_name = self.init_class.get_value().rsplit('.', 1)
                module = __import__(module_name, globals(), locals(), [class_name])
            except ImportError, ie:
                get_logger().error(ie)
                self.ruleset.parse_error(self.trace_id[0], 'gear create alert unable to load specified init class: {0}'.format(self.init_class))
                raise ie
            self.init_class_callable = getattr(module, class_name)
            
            tmp_instance = self.init_class_callable()
            if isinstance(tmp_instance, ExtInitAlert) == False:
                self.ruleset.parse_error(self.trace_id[0], 'create_alert element init class must be a subclass of ExtInitAlert')

        # validate
        # alert_id is required
        if not self.id.is_set():
            self.ruleset.parse_error(self.trace_id[0],'create_alert element requires the \'id\' attribute')
        # if using metadata, make sure id has metadata
        if self.use_metadata.get_value() == True:
            try:
                metadata = get_service(SERVICE_ALERT_METADATA)
            except:
                metadata = None
            if metadata is None or len(metadata) == 0:
                self.ruleset.parse_error(self.trace_id[0], 'create_alert element alert id validation failed trying to retrieve the alert metadata')
            try:
                tmp_value = self.id.get_value()
            except:
                # Happens if can't get a value from the alert_id (GEAR variable case)
                get_logger().debug('Exception checking alert id {0}: {1}'.format(self.id.in_str,str(sys.exc_info()[0])))
                tmp_value = None
            if tmp_value is not None and tmp_value not in metadata:
                    self.ruleset.parse_error(self.trace_id[0], 'create_alert element alert id {0} does not have metadata'.format(self.id.get_value()))
        elif not (self.severity.is_set() and self.urgency.is_set() and self.recommendation.is_set() and self.msg_template.is_set()):
            self.ruleset.parse_error(self.trace_id[0],'create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false')

        return
        
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        ''' Suppress the specified events '''
        self.ruleset.trace_warning(self.trace_id[1], 'Error')
        return
        
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Suppress the specified events '''
        self.ruleset.trace_warning(self.trace_id[1], 'Error')
        return
        
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Accumulate alerts to be created'''
        alert_id = self.id.get_value()
        # Get event location 
        if self.event_loc.is_set():
            con_loc_key = set([self.event_loc.get_value()])
        else:
            # Use locations from the truth point
            if self.event_loc_scope.is_set() == True and self.event_loc_scope.get_value()[1] is not None:
                con_loc_key = set()
                for s_loc in truth_point[0]:
                    try:
                        con_loc_key.add(s_loc.new_location_by_scope(self.event_loc_scope.get_value()[1]))
                    except:
                        get_logger().exception('scoping failure')
                        continue
            else: # No scope
                con_loc_key = set(truth_point[0])
        # Now have a set with the locations in it for this alert 
        # Get the first one 
        if len(con_loc_key) == 0:
            event_loc_key = None
        else:
            event_loc_key = list(con_loc_key)[0]
        self.ruleset.trace_info(self.trace_id[1], '              Accumulation key = ({0})'.format(','.join([str(l) for l in con_loc_key])))
        # Do we already have an alert at that event location?
        if alert_id in self.potential_alerts.keys():
            if event_loc_key in self.potential_alerts[alert_id].keys():
                get_logger().debug('Combining alerts with alert id {0} at location {1}'.format(alert_id,str([','.join([str(l) for l in con_loc_key])])))
                self.potential_alerts[alert_id][event_loc_key][0].update(con_loc_key)
                self.potential_alerts[alert_id][event_loc_key][1][ALERT_ATTR_CONDITION_EVENTS].update(set(truth_point[1]))
                return

        self.ruleset.trace_info(self.trace_id[1], 'Accumulating alert {0}'.format(alert_id))
        alert_dict = {}
        alert_dict[ALERT_ATTR_SRC_NAME] = self.src_name
        alert_dict[ALERT_ATTR_ALERT_ID] = alert_id
        if self.severity.is_set():
            alert_dict[ALERT_ATTR_SEVERITY] = self.severity.get_value()
        if self.urgency.is_set():
            alert_dict[ALERT_ATTR_URGENCY] = self.urgency.get_value()
        if self.fru_loc.is_set():
            alert_dict[ALERT_ATTR_FRU_LOC] = self.fru_loc.get_value()
        if self.recommendation.is_set():
            alert_dict[ALERT_ATTR_RECOMMENDATION] = self.recommendation.get_value()
        if self.raw_data.is_set():
            alert_dict[ALERT_ATTR_RAW_DATA] = self.raw_data.get_value()
        if self.msg_template.is_set():
            alert_dict[ALERT_ATTR_MSG_TEMPLATE] = self.msg_template.get_value()
        if self.priority.is_set():
            alert_dict[ALERT_ATTR_PRIORITY] = self.priority.get_value()
        alert_dict[ALERT_ATTR_CONDITION_EVENTS] = set(truth_point[1])

        self.potential_alerts[alert_id][event_loc_key] = (con_loc_key, alert_dict)
        return
        
    def execute_create_alert_stage(self, pool, rule):
        ''' process the potential alerts '''
        new_alerts = []
        for alert_id in self.potential_alerts.keys():
            # Consolidate overlaps
            tmp_pot_alerts = self.potential_alerts[alert_id].copy()
            for event_loc_key, pot_alert_info in self.potential_alerts[alert_id].items():
                del tmp_pot_alerts[event_loc_key]
                combined = False
                for tmp_event_loc_key, tmp_pot_alert_info in tmp_pot_alerts.items():
                    if pot_alert_info[0].isdisjoint(tmp_pot_alert_info[0]) == False:
                        tmp_pot_alerts[tmp_event_loc_key][0].update(pot_alert_info[0])
                        tmp_pot_alerts[tmp_event_loc_key][1][ALERT_ATTR_CONDITION_EVENTS].update(pot_alert_info[1][ALERT_ATTR_CONDITION_EVENTS])
                        combined = True
                        break
                # If didn't colapse further, then create the alert
                if combined == False:
                    alert_dict = pot_alert_info[1]
                    if event_loc_key is None:
                        # Get the location to use from the first condition element with a non-None src loc
                        for event in list(alert_dict[ALERT_ATTR_CONDITION_EVENTS]):
                            try:
                                loc = event.src_loc
                                if self.event_loc_scope.is_set() and self.event_loc_scope.get_value()[1] is not None:
                                    loc = loc.new_location_by_scope(self.event_loc_scope.get_value()[1])
                            except:
                                continue
                            if loc is not None:
                                break
                        # Might still fail if None of them had one
                        # TODO: Should we have special handling of this case?
                    else:
                        loc = event_loc_key
                    
                    alert_dict[ALERT_ATTR_EVENT_LOC] = loc.get_location()
                    alert_dict[ALERT_ATTR_EVENT_LOC_TYPE] = loc.get_id()
            
                    # Call init routine if specified 
                    if self.init_class_callable is not None:
                        try:
                            alert_dict = self.init_class_callable().update_init_data_main(alert_dict)
                        except ExtFatalError:
                            get_logger().exception('FATAL ERROR raised --> kill analyzer')
                            raise
                        except:
                            self.ruleset.trace_error(self.trace_id[1], 'Error in update_init_data_main')
                            get_logger().exception('')
            
                    # Allocate the potential alert 
                    self.ruleset.trace_info(self.trace_id[1], 'Allocating alert {0} at {1}:{2}'.format(str(self.id.get_value()), alert_dict[ALERT_ATTR_EVENT_LOC_TYPE], alert_dict[ALERT_ATTR_EVENT_LOC]))
                    amgr = get_service(SERVICE_ALERT_MGR)
                    new_alert = amgr.allocate(self.id.get_value(), alert_dict)
                    # Add suppressions based on the condition events 
                    new_suppressions = set()
                    for event in new_alert.condition_events:
                        new_suppressions.update(pool.get_suppressed(event))
                    if len(new_suppressions) != 0:
                        amgr.add_suppressions(new_alert, new_suppressions)
                    new_alerts.append(new_alert)
                
        return new_alerts
    
    def reset(self):
        ''' reset the alert ''' 
        self.potential_alerts.clear()
        return
    
    def get_cross_ref(self):
        ''' return alert id in a list '''
        try:
            result = self.id.get_value()
        except:
            result = self.id.in_str
        return [result]
    
    def get_used_locations(self):
        ''' If ignore, doesn't use any
            If locations set, then return those
            Otherwise uses whatever conditions used so nothing to add '''
        if self.event_loc.is_set() == True:    
            return set([self.event_loc.in_str])
        return None

    
class GearActionableExecute(GearActionable):
    '''Execute the execute function on the specified class '''

    def __init__(self, xml_element, trace_dict, ruleset):
        '''
        Constructor
        '''
        self.name = None
        self.parms = RuleParms()
        GearActionable.__init__(self, GACT_TYPE_EXECUTE, xml_element, trace_dict, ruleset)
        
        # Construct the external class
        class_spec = self.ext_class.in_str
        if class_spec is None or class_spec == '':
            self.ruleset.parse_error(self.trace_id[0], 'execute element requires the \'ext_class\' attribute')
        try:
            module_name, class_name = class_spec.rsplit('.', 1)
            module = __import__(module_name, globals(), locals(), [class_name])
            tmp_class = getattr(module, class_name)
        except:
            self.ruleset.parse_error(self.trace_id[0], 'execute element was unable to load specified the class: {0}'.format(self.class_spec))
            get_logger().exception('execute element exception')
        
        # Get parameters to pass to init 
        try:
            self.parms.resolve_and_validate(self.ruleset, None, rule_part=GRUL_PART_EXTERNAL)
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], 'execute element parm error: {0}'.format(e.msg))
            get_logger().exception('execute element parm error exception')
    
        init_dict = self.parms.get_dict()
        init_dict['execute_name'] = self.name.in_str
        try:
            self.call_class = tmp_class(init_dict)
        except:
            self.logger().exception('execute element with name {0} failed during initialization'.format(self.name.in_str))
            raise

        if isinstance(self.call_class, ExtExecute) == False:
            self.ruleset.parse_error(self.trace_id[0], 'execute ext_class must be a subclass of ExtExecute')
        return
    
    def _str_subelement_additions(self):
        ''' Add instance subelements to output '''
        if self.parms is not None:
            return str(self.parms)
        return ''       

    def _read_from_xml_other_subelements(self,xml_element, trace_dict):
        ''' Read in the instances attribute '''
        try:
            self.parms.read_from_xml(xml_element)
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], 'execute element parameter error: {0}'.format(e.msg))
        return True
    
    # resolve_and_validate is not needed ... done in init

    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        ''' Execute the suppression stage actions '''
        try:
            self.call_class.execute_accumulate_suppression_stage(truth_point, pool, rule)
        except ExtFatalError:
            get_logger().exception('FATAL ERROR raised --> kill analyzer')
            raise
        except:
            self.ruleset.trace_error(self.trace_id[1], 'execute {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return
            
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Execute the suppression stage actions '''
        try:
            self.call_class.execute_finalize_suppression_stage(pool, rule)
        except ExtFatalError:
            get_logger().exception('FATAL ERROR raised --> kill analyzer')
            raise
        except:
            self.ruleset.trace_error(self.trace_id[1], 'execute {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return
            
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate alert stage actions '''
        try:
            self.call_class.execute_accumulate_alert_stage(truth_point, pool, rule)
        except ExtFatalError:
            get_logger().exception('FATAL ERROR raised --> kill analyzer')
            raise
        except:
            self.ruleset.trace_error(self.trace_id[1], 'execute {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return
    
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        new_alerts = []
        try:    
            # Extending because paranoid that won't get list back
            new_alerts.extend(self.call_class.execute_create_alert_stage(pool, rule))
        except ExtFatalError:
            get_logger().exception('FATAL ERROR raised --> kill analyzer')
            raise
        except:
            self.ruleset.trace_error(self.trace_id[1], 'execute {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return new_alerts
    
    def reset(self):
        '''Reset the condition'''
        try:
            self.call_class.reset()
        except:
            self.ruleset.trace_error(self.trace_id[1], 'execute {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return

