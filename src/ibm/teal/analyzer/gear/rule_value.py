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
from ibm.teal.analyzer.gear.common import GRSE_CONSTANTS, gearstr2scope,\
    gearstr2loc, GRUL_PART_ACTION, GRUL_PART_CONDITION, GRUL_PART_EXTERNAL
#from ibm.teal.analyzer.gear.constants import GCON_ALERT_ID
from ibm.teal.analyzer.gear.constants import GCON_EVENT_ID
from ibm.teal.analyzer.gear.control import GCTL_DEFAULT_EVENT_COMP
from ibm.teal.registry import get_logger
from ibm.teal.teal_error import XMLParsingError
import re

GRVA_TYPE_AS_STRING = ['event_id', 'alert_id', 'comp', 'scope', 'loc', 'ext_dict', 
                       'event', 'set_of_events', 'set_of_event_ids', 'mode', 
                       'string', 'execute', 'any', 'unknown', 'nonzero_uint', 'duration', 'boolean', 
                       'set_of_locs', 'config_dict', 'location_match', 'scope_def']
GRVA_TYPE_EVENT_ID = 0
GRVA_TYPE_ALERT_ID = 1
GRVA_TYPE_COMP = 2
GRVA_TYPE_SCOPE = 3   # Non-defaulting scope
GRVA_TYPE_LOC = 4
GRVA_TYPE_EXT_DICT = 5
GRVA_TYPE_EVENT = 6
GRVA_TYPE_SET_OF_EVENTS = 7
GRVA_TYPE_SET_OF_EVENT_IDS = 8
GRVA_TYPE_MODE = 9
GRVA_TYPE_STRING = 10
GRVA_TYPE_EXECUTE = 11
GRVA_TYPE_ANY = 12
GRVA_TYPE_UNKNOWN = 13
GRVA_TYPE_NONZERO_UINT = 14
GRVA_TYPE_DURATION = 15
GRVA_TYPE_BOOLEAN = 16
GRVA_TYPE_SET_OF_LOCS = 17
GRVA_TYPE_CONFIG_DICT = 18
GRVA_TYPE_LOCATION_MATCH = 19
GRVA_TYPE_SCOPE_DEF = 20  # Defaulting scope

GRVA_TYPE_LOCATION_MATCH_VALID_VALUES = ['identical', 'ignore', 'unique']
GRVA_TYPE_LOCATION_MATCH_IDENTICAL = 'identical'
GRVA_TYPE_LOCATION_MATCH_IGNORE = 'ignore'
GRVA_TYPE_LOCATION_MATCH_UNIQUE = 'unique'


# Map from first keyword to tuple of OK in external, OK in condition, OK in action, min size, max size, type and dict of 2nd keywords
GRVA_VAR_VALID = {'cur_event': (False, True, False, 1, 3, GRVA_TYPE_EVENT,                     
                                 {'event_id': GRVA_TYPE_EVENT_ID,
                                  'src_loc': GRVA_TYPE_LOC,      
                                  'rpt_loc': GRVA_TYPE_LOC,      
                                  'ext': GRVA_TYPE_EXT_DICT            
                                 }                            
                                ),                            
                  'all_condition_events': (False, False, True, 1, 3, GRVA_TYPE_SET_OF_EVENTS,          
                                 {'event_id': GRVA_TYPE_SET_OF_EVENT_IDS,
                                  'src_loc': GRVA_TYPE_SET_OF_LOCS,      
                                  'rpt_loc': GRVA_TYPE_SET_OF_LOCS,      
                                  'ext': GRVA_TYPE_EXT_DICT            
                                 }                            
                                ),                            
                  'last_condition_event': (False, False, True, 1, 3, GRVA_TYPE_EVENT,          
                                 {'event_id': GRVA_TYPE_EVENT_ID,
                                  'src_loc': GRVA_TYPE_LOC,      
                                  'rpt_loc': GRVA_TYPE_LOC,      
                                  'ext': GRVA_TYPE_EXT_DICT            
                                 }                            
                                ),                            
                  'condition_events': (False, False, True, 1, 1, GRVA_TYPE_SET_OF_EVENTS, {}),
                  'condition_event_ids': (False, False, True, 1, 1, GRVA_TYPE_SET_OF_EVENT_IDS, {}),
                  'conf_dict': (True, True, True, 1, 2, GRVA_TYPE_CONFIG_DICT, {}),  
                  'mode': (True, True, True, 1, 1, GRVA_TYPE_MODE, {}),
                  'name': (True, True, True, 1, 1, GRVA_TYPE_STRING, {}),
                  'version_id': (True, True, True, 1, 1, GRVA_TYPE_STRING, {}),
                  'executed': (False, False, False, 3, 3, GRVA_TYPE_EXECUTE, {})
                 }

def init_rule_values(owner, value_defs):
    ''' Initialize the rule values defined in value_defs as attributes of the owner'''
    for val_name, val_info in value_defs.items():
        setattr(owner, val_name, gear_value_init(val_info[0], val_info[1]))
    return

def read_from_xml_rule_value(owner, att_key, att_value, value_defs):
    ''' Read the rule values defined in values_def in from XML into attributes of the owner '''
    if att_key in value_defs.keys():
        setattr(owner, att_key, rule_value_factory(att_value, value_defs[att_key][0], static_only=value_defs[att_key][3]))
        return True
    return False

def resolve_and_validate_rule_values(owner, ruleset, rule, value_defs, rule_part=GRUL_PART_CONDITION):
    ''' Resolve and validate rule values defined in values_def'''
    try:
        for name, info in value_defs.items():
            tmp_name = name
            getattr(owner, name).resolve_and_validate(ruleset, rule, rule_part=rule_part, required=info[2])
    except XMLParsingError as e:
        raise XMLParsingError('{0} attribute: {1}'.format(tmp_name, e.msg))
    return

def dump_rule_values(owner, value_defs):
    ''' Return a string with the values in value defs and there values in it '''
    outstr = ''
    for name in value_defs:
        try:
            attr = getattr(owner, name)
            if attr.is_set():
                outstr += ' {0}="{1}"'.format(name, attr.in_str)
        except:
            pass
    return outstr
    
def rule_value_factory(value_str, usage_type, static_only=False):
    ''' Look at the type to determine which factory should be called '''
    if usage_type == GRVA_TYPE_SET_OF_EVENTS: 
        return rule_value_list_factory(value_str, usage_type, GRVA_TYPE_EVENT, static_only)
    if usage_type == GRVA_TYPE_SET_OF_EVENT_IDS: 
        return rule_value_list_factory(value_str, usage_type, GRVA_TYPE_EVENT_ID, static_only)
    if usage_type == GRVA_TYPE_SET_OF_LOCS: 
        return rule_value_list_factory(value_str, usage_type, GRVA_TYPE_LOC, static_only)
    return rule_value_single_factory(value_str, usage_type, static_only)

def rule_value_single_factory(value_str, usage_type, static_only=False):
    ''' Create the correct rule value for the given string '''
    rule_value = None
    loc_str = value_str.strip()
    if not _contains_gear_variable(loc_str):
        rule_value = RuleValueStatic(loc_str, usage_type)
    else:
        if not static_only:
            rule_value = RuleValueDynamic(loc_str, _parse_gear_variable(loc_str), usage_type)
        else:
            raise XMLParsingError('GEAR variable is not allowed')
    if rule_value == None:
        raise XMLParsingError('unable to process value string \'{0}\''.format(loc_str))
    return rule_value

def gear_value_init(type, init_str):
    ''' Return the appropriate None type for the specified type '''
    if type == GRVA_TYPE_COMP:
        return RuleValueStatic(None, GRVA_TYPE_COMP)
    if type == GRVA_TYPE_SCOPE:
        return RuleValueStatic(None, GRVA_TYPE_SCOPE)
    if type == GRVA_TYPE_SCOPE_DEF:
        return RuleValueStatic(None, GRVA_TYPE_SCOPE_DEF)
    if type == GRVA_TYPE_LOCATION_MATCH:
        return RuleValueStatic(GRVA_TYPE_LOCATION_MATCH_IDENTICAL, GRVA_TYPE_LOCATION_MATCH)
    if type == GRVA_TYPE_BOOLEAN:
        return RuleValueStatic(init_str, GRVA_TYPE_BOOLEAN)
    return RuleValueNone()


class RuleValue(object):
    ''' Represent a value in '''
    
    __metaclass__ = ABCMeta
  
    def __init__(self, in_str, usage_type):
        ''' constructor '''
        self.in_str = in_str
        self.usage_type = usage_type
        return
    
    @abstractmethod
    def get_value(self):
        ''' return the value '''
        pass
    
    @abstractmethod
    def is_set(self):
        ''' Return True if the value has been set '''
        pass
    
    @abstractmethod
    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        ''' resolve and validate the value '''
        pass
    
       
class RuleValueStatic(RuleValue):
    ''' Value that does not change dynamically'''
    
    def __init__(self, in_str, usage_type):
        ''' constructor '''
        self.value = None
        RuleValue.__init__(self, in_str, usage_type)
        return
    
    def get_value(self):
        ''' return the value '''
        return self.value
    
    def is_set(self):
        ''' Return True if the value has been set '''
        if self.usage_type == GRVA_TYPE_SCOPE or self.usage_type == GRVA_TYPE_SCOPE_DEF:
            if self.value is None:
                return False
            if self.value[1] is None:
                return False
            return True
        return self.value is not None

    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        ''' resolve and validate the value '''
        if self.usage_type == GRVA_TYPE_EVENT_ID:
            # resolve constants
            self.value = ruleset[GRSE_CONSTANTS].get_constant(self.in_str, GCON_EVENT_ID)
#        elif self.usage_type == GRVA_TYPE_ALERT_ID:
#            # resolve constants
#            self.value = ruleset[GRSE_CONSTANTS].get_constant(self.in_str, GCON_ALERT_ID)
        elif self.usage_type == GRVA_TYPE_SCOPE_DEF:
            if self.in_str is None:
                if rule_part == GRUL_PART_CONDITION:
                    if rule.condition.default_scope.in_str is not None:
                        # Get default scope (if specified)
                        self.value = rule.condition.default_scope.value
                    else:
                        self.value = (None, None)
            else:
                # parse
                self.value = gearstr2scope(self.in_str)
        elif self.usage_type == GRVA_TYPE_SCOPE:
            if self.in_str is None:
                self.value = (None, None)
            else:
                self.value = gearstr2scope(self.in_str)
        elif self.usage_type == GRVA_TYPE_LOC:
            # parse
            self.value = gearstr2loc(self.in_str) 
        elif self.usage_type == GRVA_TYPE_COMP:
            if self.in_str is None:
                self.value = ruleset['gear_control'][GCTL_DEFAULT_EVENT_COMP]
                if rule_part == GRUL_PART_CONDITION and rule.condition.default_event_comp.is_set() == True:
                        self.value = rule.condition.default_event_comp.value
            else:
                self.value = self.in_str
        elif self.usage_type == GRVA_TYPE_BOOLEAN:
            if self.in_str == 'true':
                self.value = True
            else:
                self.value = False
        elif self.usage_type == GRVA_TYPE_NONZERO_UINT or self.usage_type == GRVA_TYPE_DURATION:
            try:
                self.value = int(self.in_str)
            except:
                raise XMLParsingError('numeric value string \'{0}\' cannot be converted'.format(self.in_str))
            if self.value == 0:
                raise XMLParsingError('numeric value cannot be zero')
            if self.value < 0:
                raise XMLParsingError('numeric value cannot be negative')
        elif self.usage_type == GRVA_TYPE_LOCATION_MATCH:
            self.value = self.in_str
            if self.value not in GRVA_TYPE_LOCATION_MATCH_VALID_VALUES:
                raise XMLParsingError('invalid location match value of {0}'.format(self.value))
        else:
            self.value = self.in_str
            
        if required and not self.is_set():
            raise XMLParsingError('required value not set')
        return

class RuleValueDynamic(RuleValue):
    ''' Value that does not change dynamically'''
    
    def __init__(self, in_str, name, usage_type):
        ''' constructor '''
        self.names = [n.strip() for n in name.split('.')]
        self.rule = None
        self.ruleset = None
        self.actual_type = GRVA_TYPE_UNKNOWN
        RuleValue.__init__(self, in_str, usage_type)
        return
    
    def get_value(self):
        ''' return the value '''
#        TODO: Should we do this check only after we know it isn't one that doesn't need this?
#              and should we do checks for the others ... or just let the exception flow?
#        if self.rule is None:
#            get_logger().fatal('rule was not set for value \'{0}\''.format(self.in_str))
        if self.names[0] == 'cur_event':
            return self._get_event_value(self.rule.cur_event)
        elif self.names[0] == 'last_condition_event':
            return self._get_event_value(list(self.rule.action.truth_point[1])[-1])
        elif self.names[0] == 'condition_events':
            return self.rule.action.truth_point[1]
        elif self.names[0] == 'condition_event_ids':
            return [e.get_event_id() for e in self.rule.action.truth_point[1]]
        elif self.names[0] == 'executed':
            idx = self.rule.action.execute_names.index(self.names[1])
            return self.rule.action.actionables['execute'][idx].rtn_dict[self.names[2]]
        elif self.names[0] == 'mode':
            return self.ruleset.mode
        elif self.names[0] == 'conf_dict':
            if len(self.names) == 1:
                return self.ruleset.conf_dict
            else:
                return self.ruleset.conf_dict[self.names[1]]
        elif self.names[0] == 'name':
            return self.ruleset.name
        elif self.names[0] == 'version_id':
            return self.ruleset.version_id
        elif self.names[0] == 'all_condition_events':
            values = set()
            for c_event in self.rule.action.truth_point[1]:
                value = self._get_event_value(c_event)
                if value is not None:
                    values.add(value)
            return list(values)
        return
    
    def is_set(self):
        ''' Return True if the value has been set '''
        return True
    
    def _get_event_value(self, event):
        ''' Get the specified value from the event'''
        if len(self.names) == 1:
            return event
        if self.names[1] == 'src_loc':
            return event.get_src_loc()
        elif self.names[1] == 'rpt_loc':
            return event.get_rpt_loc()
        elif self.names[1] == 'ext':
            try:
                result = event.raw_data[self.names[2]]
            except:
                get_logger().exception('Unable to get {0} for event {1}'.format(self.in_str, event.brief_str()))
                result = None
            return result
        elif self.names[1] == 'event_id':
            return event.get_event_id()
        return
       
    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        ''' resolve and validate the value '''
        self.rule = rule
        self.ruleset = ruleset
        get_logger().debug('Start: actual = {0}  usage = {1}'.format(GRVA_TYPE_AS_STRING[self.actual_type], GRVA_TYPE_AS_STRING[self.usage_type]))
        # Currently we don't support anything bigger than 3
        if len(self.names) > 3:
                raise XMLParsingError('GEAR variable specification unrecognized (depth) variable name \'{0}\''.format(self.in_str))                   
        # See if starts with one of the valid keys
        if self.names[0] in GRVA_VAR_VALID:
            ext_ok, cond_ok, action_ok, min_size, max_size, self.actual_type, lvl_2_dict = GRVA_VAR_VALID[self.names[0]]
            # Check if OK in specified rule part 
            if rule_part == GRUL_PART_EXTERNAL and not ext_ok:
                raise XMLParsingError('GEAR variable specification of \'{0}\' cannot use \'{1}\' in external call parameter portion of a rule'.format(self.in_str, self.names[0]))                   
            if rule_part == GRUL_PART_CONDITION and not cond_ok:
                raise XMLParsingError('GEAR variable specification of \'{0}\' cannot use \'{1}\' in condition portion of a rule'.format(self.in_str, self.names[0]))                   
            if rule_part == GRUL_PART_ACTION and not action_ok:
                raise XMLParsingError('GEAR variable specification of \'{0}\' cannot use \'{1}\' in action portion of a rule'.format(self.in_str, self.names[0]))                   
            # Check size
            if len(self.names) > max_size or len(self.names) < min_size:
                raise XMLParsingError('GEAR variable specification unrecognized (depth) variable name \'{0}\''.format(self.in_str))                   
            # Special handling for all_condition_events
            if self.names[0] == 'all_condition_events':
                if len(self.names) != 1:
                    if self.names[1] not in lvl_2_dict:
                        raise XMLParsingError('GEAR variable specification unrecognized variable name \'{0}\' (2nd)'.format(self.names[1]))                   
                    self.actual_type = lvl_2_dict[self.names[1]]
                    if lvl_2_dict[self.names[1]] == GRVA_TYPE_EXT_DICT:
                        # Can't validate types in dictionary at this point, so assume it is right
                        if len(self.names) != 3:
                            raise XMLParsingError('GEAR variable specification incomplete (must be 3)')                   
            # Execute
            if self.actual_type == GRVA_TYPE_EXECUTE:
                if self.names[1] not in rule.action.execute_names:
                    raise XMLParsingError('GEAR variable specification unrecognized execute name \'{0}\''.format(self.names[1]))
            # dict -- no special checks 
            #     TODO: Should we try to make sure keys are available?  Executable could have a validate method
            # event
            elif self.actual_type == GRVA_TYPE_EVENT:
                if len(self.names) != 1:
                    if self.names[1] not in lvl_2_dict:
                        raise XMLParsingError('GEAR variable specification unrecognized variable name \'{0}\' (2nd)'.format(self.names[1]))                   
                    self.actual_type = lvl_2_dict[self.names[1]]
                    if lvl_2_dict[self.names[1]] == GRVA_TYPE_EXT_DICT:
                        # Can't validate types in dictionary at this point, so assume it is right
                        if len(self.names) != 3:
                            raise XMLParsingError('GEAR variable specification incomplete (must be 3)')                   
            elif self.actual_type == GRVA_TYPE_CONFIG_DICT:
                if ruleset.conf_dict is None or self.names[1] not in ruleset.conf_dict:
                    raise XMLParsingError('GEAR variable reference to config dict invalid.  \'{0}\' not specified in configuration'.format(self.names[1]))
            
            # else -- other have no special checking
            
            ## Validate type
            # Any type is acceptable
            if self.usage_type == GRVA_TYPE_ANY:
                return 
            # Type not know, so assign whatever we determined
            elif self.usage_type == GRVA_TYPE_UNKNOWN:
                self.usage_type = self.actual_type
            # if not a dictionary make sure types match
            elif self.actual_type != GRVA_TYPE_CONFIG_DICT and self.actual_type != GRVA_TYPE_EXT_DICT and          \
                 self.actual_type != self.usage_type:
                XMLParsingError('GEAR variable type does not match {0} is not {1}'.format(GRVA_TYPE_AS_STRING[self.actual_type], GRVA_TYPE_AS_STRING[self.usage_type]))
        else:
            raise XMLParsingError('GEAR variable name not supported \'{0}\''.format(self.names[0]))
        
        if required and not self.is_set():
            raise XMLParsingError('Required value not specified')
        get_logger().debug('End: actual = {0}  usage = {1}'.format(GRVA_TYPE_AS_STRING[self.actual_type], GRVA_TYPE_AS_STRING[self.usage_type]))
        return


def rule_value_list_factory(value_list_str, usage_type, usage_contained_type, static_only=False):
    ''' Create the correct rule value list for the given string '''
    # Get the as a list
    as_list = [value_str.strip() for value_str in value_list_str.split(',')]
    # Shortcut -- if no GEAR variables at all its a static
    if not _contains_gear_variable(value_list_str):
        #print 'did not contain a GEAR variable!  ', as_list
        return RuleValueListStatic(value_list_str, as_list, usage_type, usage_contained_type)
    if static_only:
        XMLParsingError('GEAR variable not allowed')
    return RuleValueListDynamic(value_list_str, as_list, usage_type, usage_contained_type)


class RuleValueList(object):
    ''' Represent a value in '''
    
    __metaclass__ = ABCMeta
  
    def __init__(self, in_str_list, usage_type, usage_contained_type):
        ''' constructor '''
        self.in_str = in_str_list
        self.usage_type = usage_type
        self.usage_contained_type = usage_contained_type
        return
    
    @abstractmethod
    def get_list(self):
        ''' return the list '''
        pass
    
    @abstractmethod 
    def is_set(self):
        ''' Return True if the value has been set '''
        pass
    
    @abstractmethod
    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        ''' resolve and validate the value '''
        pass


  
class RuleValueListStatic(RuleValueList):
    ''' Static list '''
    
    def __init__(self, in_str_list, as_list, usage_type, usage_contained_type):
        ''' constructor '''
        if usage_contained_type == GRVA_TYPE_LOC:
            self.list = [RuleValueStatic(loc_str, GRVA_TYPE_LOC) for loc_str in as_list]
        else:
            self.list = as_list
        RuleValueList.__init__(self, in_str_list, type, usage_contained_type)
        return
    
    def get_list(self):
        ''' return the static list '''
        return self.list
     
    def is_set(self):
        ''' Return True if the value has been set '''
        return self.list is not None
    
    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        ''' resolve and validate the value '''
        ## Resolve
        # constants
        if self.usage_contained_type == GRVA_TYPE_EVENT_ID:
            self.list = ruleset[GRSE_CONSTANTS].resolve_id_set_constants(self.list, GCON_EVENT_ID)
#        elif self.usage_contained_type == GRVA_TYPE_ALERT_ID:
#            self.list = ruleset[GRSE_CONSTANTS].resolve_id_set_constants(self.list, GCON_ALERT_ID)
        elif self.usage_contained_type == GRVA_TYPE_LOC:
            # TO DO: Should I do this?  Should it be a list of RuleValues?
            # Resolve them then put the locations directly into the list
            new_list = []
            for rv_loc in self.list:
                rv_loc.resolve_and_validate(ruleset, rule, rule_part, required)
                new_list.append(rv_loc.get_value())
            self.list = new_list
        ## Validate
        # at least one entry left
        if len(self.list) == 0:
            raise XMLParsingError('empty list specified')
        
        if required and not self.is_set():
            raise XMLParsingError('required attribute not specified')
        return

  
class RuleValueListDynamic(RuleValueList):
    ''' Dynamic list '''
    
    def __init__(self, in_str_list, as_list, usage_type, usage_contained_type):
        ''' constructor '''
        self.static_list = []
        self.dynamic_values = []
        self.dynamic_list = []
        self.dynamic_unknown = []
        RuleValueList.__init__(self, in_str_list, usage_type, usage_contained_type)
        for value_str in as_list:
            if _contains_gear_variable(value_str) == True:
                # Type will be checked/updated as part of being resolved
                self.dynamic_list.append(RuleValueDynamic(value_str, _parse_gear_variable(value_str), GRVA_TYPE_UNKNOWN))
            else:
                self.static_list.append(value_str)
        return
    
    def get_list(self):
        ''' return the static list '''
        ret_list = list(self.static_list)
        for d_list in self.dynamic_list: 
            ret_list.extend(d_list.get_value())
            
        for dynamic_value in self.dynamic_values:
            if dynamic_value.actual_type == GRVA_TYPE_CONFIG_DICT:
                ret_list.extend([value_str.strip() for value_str in dynamic_value.get_value().split(',')])
            else:
                ret_list.append(dynamic_value.get_value())
        for unknown_value in self.dynamic_unknown:
            value = unknown_value.get_value()
            if value is None:
                continue
            if isinstance(value, list) or isinstance(value, tuple):
                ret_list.extend(value)
            else:
                ret_list.append(value)
        return ret_list
       
    def is_set(self):
        ''' Return True if the value has been set '''
        return True

    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        ''' resolve and validate the value '''
        ## Resolve
        # constants in static list of lists case
        if self.usage_contained_type == GRVA_TYPE_EVENT_ID:
            self.static_list = ruleset[GRSE_CONSTANTS].resolve_id_set_constants(self.static_list, GCON_EVENT_ID)
#        elif self.usage_contained_type == GRVA_TYPE_ALERT_ID:
#            self.static_list = ruleset[GRSE_CONSTANTS].resolve_id_set_constants(self.static_list, GCON_ALERT_ID)
        # Figure out which of the entries in the dynamic list are for lists and which are for single values
        tmp_dynamic_list = []
        for gv in self.dynamic_list:
            gv.resolve_and_validate(ruleset, rule, rule_part, required)
            if gv.usage_type == self.usage_type:
                tmp_dynamic_list.append(gv)
            elif gv.usage_type == self.usage_contained_type:
                self.dynamic_values.append(gv)
            elif gv.usage_type == GRVA_TYPE_CONFIG_DICT or gv.usage_type == GRVA_TYPE_EXECUTE or gv.usage_type == GRVA_TYPE_EXT_DICT:
                self.dynamic_unknown.append(gv)
            elif gv.usage_type == GRVA_TYPE_UNKNOWN:
                raise XMLParsingError('GEAR element type {0} not supported.  Expected {1}'.format(GRVA_TYPE_AS_STRING[gv.usage_type],GRVA_TYPE_AS_STRING[self.usage_type]))
            else:
                raise XMLParsingError('GEAR element type {0} does not match variable type {1}'.format(GRVA_TYPE_AS_STRING[gv.usage_type],GRVA_TYPE_AS_STRING[self.usage_type]))
        self.dynamic_list = tmp_dynamic_list
 
        ## Validate
        # Check for zero
        if len(self.static_list) == 0 and len(self.dynamic_list) == 0 and len(self.dynamic_values) == 0 and len(self.dynamic_unknown) == 0:
            raise XMLParsingError('empty list specified')
        
        if required and not self.is_set():
            raise XMLParsingError('required attribute not specified')
        return


class RuleValueNone(RuleValueList, RuleValue):
    ''' Place holder for an unset value '''
    
    def __init__(self):
        self.in_str = None
        self.usage_type = GRVA_TYPE_UNKNOWN
        return
    
    def get_value(self):
        return None
    
    def get_list(self):
        return None
    
    def is_set(self):
        ''' Return True if the value has been set '''
        return False
    
    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        if required:
            raise XMLParsingError('Required attribute not set')
        return
    
    
def _contains_gear_variable(field):
    ''' Check if the field contains a GEAR variable.
    If the variable is contained but incorrectly formed an exception will be raised
    '''
    p_any = re.compile(".*GEAR.*\[.*")    
    if p_any.match(field) is not None:
        return True
    return False

def _parse_gear_variable(field):
    ''' Parse the gear variable and return the name '''
    p_val = re.compile("^GEAR\[(.*)\]$")
    m_val = p_val.match(field)
    if m_val is None:
        raise XMLParsingError('invalid GEAR variable specification: \'{0}\''.format(field))
    else:
        tmp_name_str = m_val.group(1)
        tmp_name_str.strip()
        if len(tmp_name_str) == 0:
            raise XMLParsingError('GEAR variable specification requires a variable name')
        return tmp_name_str
    return None
  

class RuleParms(object):
    '''Class to manage parm sub-elements used in a rule (evaluate and execute)'''
    
    def __init__(self):
        '''Parse the parm sub-elements of the passed xml parent element'''
        self.parm_dict = {}
        return
    
    def read_from_xml(self, parm_element):
        ''' parse a single param element '''
        if 'name' not in parm_element.attrib:
            raise XMLParsingError('parm element must have a \'name\' attribute')
        if 'value' not in parm_element.attrib:
            raise XMLParsingError('parm element must have a \'value\' attribute')
        parm_name = parm_element.attrib['name']
        if _contains_gear_variable(parm_name) == True:
            raise XMLParsingError('parm element \'name\' attribute does not support GEAR variables')
        if parm_name in self.parm_dict:
            raise XMLParsingError('parm element name \'{0}\' has already been used'.format(parm_name))
        self.parm_dict[parm_name] = rule_value_factory(parm_element.attrib['value'], GRVA_TYPE_UNKNOWN)
        return
    
    def __str__(self):
        ''' put out as a string '''
        outstr = ''
        for key in self.parm_dict:
            outstr += '<parm name="{0}" value="{1}"/>\n'.format(key, self.parm_dict[key].in_str)
        return outstr
    
    def get_dict(self):
        '''Return a copy of the dictionary that is suitable to use when making the call'''
        out_dict = {}
        for key in self.parm_dict:
            try:
                out_dict[key] = self.parm_dict[key].get_value()
            except:
                out_dict[key] = None
        return out_dict
        
    def is_set(self):
        '''True if the value has been set'''
        return len(self.out_dict) > 0

    def resolve_and_validate(self, ruleset, rule, rule_part=GRUL_PART_CONDITION, required=False):
        '''Resolve and validate the parameters'''
        # parms are optional
        for key in self.parm_dict:
            self.parm_dict[key].resolve_and_validate(ruleset, rule, rule_part, required)
        return
