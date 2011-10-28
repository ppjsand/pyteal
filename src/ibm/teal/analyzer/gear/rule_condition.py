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
from collections import defaultdict
from ibm.teal.analyzer.gear.common import GRSE_TEMPLATES, GRUL_PART_EXTERNAL
from ibm.teal.analyzer.gear.instance_helper import Comparitor
from ibm.teal.analyzer.gear.rule_value import GRVA_TYPE_COMP, GRVA_TYPE_SCOPE, \
    GRVA_TYPE_EVENT_ID, GRVA_TYPE_BOOLEAN, \
    GRVA_TYPE_NONZERO_UINT, GRVA_TYPE_SET_OF_EVENT_IDS, GRVA_TYPE_SET_OF_LOCS, \
    RuleParms, GRVA_TYPE_LOCATION_MATCH, GRVA_TYPE_STRING, \
    GRVA_TYPE_LOCATION_MATCH_IGNORE, GRVA_TYPE_LOCATION_MATCH_IDENTICAL, \
    GRVA_TYPE_LOCATION_MATCH_UNIQUE, read_from_xml_rule_value, init_rule_values,\
    resolve_and_validate_rule_values, dump_rule_values, GRVA_TYPE_SCOPE_DEF
from ibm.teal.registry import get_logger
from ibm.teal.teal_error import XMLParsingError
import itertools
from ibm.teal.analyzer.gear.external_base_classes import ExtEvaluate
from ibm.teal.analyzer.gear.rule_condition_data import ConditionData,\
    InstanceError

GCON_TYPE_CONDITION = 'condition'
GCON_TYPE_ALL_EVENTS = 'all_events'
GCON_TYPE_AND = 'and'
GCON_TYPE_ANY_EVENTS = 'any_events'
GCON_TYPE_EVENT_EQUALS = 'event_equals'
GCON_TYPE_EVENT_OCCURRED = 'event_occurred'
GCON_TYPE_NOT = 'not'
GCON_TYPE_OR = 'or'
GCON_TYPE_EVALUATE = 'evaluate'

GCON_IGNORE_KEY = 'ignore'

# Variables supported on each condition -- controls initialization, reading from XML, and validation
#     Entries in bottom dictionary are var name: (type, required, static_only)
GCON_VALUES = {GCON_TYPE_CONDITION:      {
                                           'default_scope': (GRVA_TYPE_SCOPE_DEF, None, False, True), 
                                           'default_event_comp': (GRVA_TYPE_COMP, None, False, True)
                                         },
               GCON_TYPE_ALL_EVENTS:     {
                                            'ids': (GRVA_TYPE_SET_OF_EVENT_IDS, None, True, False),
                                            'comp': (GRVA_TYPE_COMP, None, True, True),
                                            'scope': (GRVA_TYPE_SCOPE_DEF, None, False, True) ,
                                            'location_match': (GRVA_TYPE_LOCATION_MATCH, None, False, True)
                                          },
                GCON_TYPE_AND:            {
                                            'scope': (GRVA_TYPE_SCOPE_DEF, None, False, True),
                                            'location_match': (GRVA_TYPE_LOCATION_MATCH, None, False, True)
                                          },
                GCON_TYPE_ANY_EVENTS:     {
                                            'num': (GRVA_TYPE_NONZERO_UINT, None, True, False),
                                            'ids': (GRVA_TYPE_SET_OF_EVENT_IDS, None, True, False),
                                            'comp': (GRVA_TYPE_COMP, None, True, True),
                                            'unique_id': (GRVA_TYPE_BOOLEAN, 'false', False, True),
                                            'scope': (GRVA_TYPE_SCOPE_DEF, None, False, True),
                                            'locations': (GRVA_TYPE_SET_OF_LOCS, None, False, False),
                                            'instance_loc_comp': (GRVA_TYPE_SCOPE, None, False, True),
                                            'location_match': (GRVA_TYPE_LOCATION_MATCH, None, False, True),
                                            'unique_instance': (GRVA_TYPE_BOOLEAN, 'false', False, True),
                                            'instance_scope': (GRVA_TYPE_SCOPE, None, False, True)
                                            # instance
                                          },
                GCON_TYPE_EVENT_EQUALS:   {
                                            'id': (GRVA_TYPE_EVENT_ID, None, True, False),
                                            'comp': (GRVA_TYPE_COMP, None, True, True),
                                            'scope': (GRVA_TYPE_SCOPE_DEF, None, False, True),
                                            'location_match': (GRVA_TYPE_LOCATION_MATCH, None, False, True)
                                          },
                GCON_TYPE_EVENT_OCCURRED: {
                                            'num': (GRVA_TYPE_NONZERO_UINT, None, True, False),
                                            'id': (GRVA_TYPE_EVENT_ID, None, True, False),
                                            'comp': (GRVA_TYPE_COMP, None, True, True),
                                            'scope': (GRVA_TYPE_SCOPE_DEF, None, False, True),
                                            'location_match': (GRVA_TYPE_LOCATION_MATCH, None, False, True)
                                          },
                GCON_TYPE_NOT:            { 
                                           # Gets scope and location_match from the contained evaluatable
                                          },
                GCON_TYPE_OR:             {
                                            'scope': (GRVA_TYPE_SCOPE_DEF, None, False, True),
                                            'location_match': (GRVA_TYPE_LOCATION_MATCH, None, False, True)
                                          },
                GCON_TYPE_EVALUATE:       {
                                            'name':  (GRVA_TYPE_STRING, None, True, True), 
                                            'ext_class': (GRVA_TYPE_STRING, None, True, True)
                                            # init parms
                                          }
               }


def evaluatable_creator(xml_element, trace_dict, ruleset, trace_id):
    '''Create and return the correct Evaluatable from the xml_element'''
    new_evaluatable = None
    element_name = xml_element.tag.split('}')[-1]
    if element_name == GCON_TYPE_EVENT_EQUALS:
        if not ruleset.event_input:
            ruleset.parse_error(trace_id[0], 'gear condition element \'{0}\' is not supported for this analyzer'.format(element_name))
        return GearEvaluatableEventEquals(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_EVENT_OCCURRED:
        if not ruleset.event_input:
            ruleset.parse_error(trace_id[0], 'gear condition element \'{0}\' is not supported for this analyzer'.format(element_name))
        return GearEvaluatableEventOccurred(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_OR:
        return GearEvaluatableOr(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_AND:
        return GearEvaluatableAnd(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_NOT:
        return GearEvaluatableNot(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_ANY_EVENTS:
        if not ruleset.event_input:
            ruleset.parse_error(trace_id[0], 'gear condition element \'{0}\' is not supported for this analyzer'.format(element_name))
        return GearEvaluatableAnyEvents(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_ALL_EVENTS:
        if not ruleset.event_input:
            ruleset.parse_error(trace_id[0], 'gear condition element \'{0}\' is not supported for this analyzer'.format(element_name))
        return GearEvaluatableAllEvents(xml_element, trace_dict, ruleset)
    elif element_name == GCON_TYPE_EVALUATE:
        return GearEvaluatableEvaluate(xml_element, trace_dict, ruleset)
    elif element_name == 'use_template':
        return ruleset[GRSE_TEMPLATES].use_condition_template(xml_element, trace_dict, ruleset)
    else:
        ruleset.parse_error(trace_id[0],'\'condition\' element encountered an unexpected subelement \'{0}\''.format(element_name))
    return new_evaluatable
        
        
class GearEvaluatable(object):
    '''Class to represent an individual evaluation in a condition
    '''
    
    __metaclass__ = ABCMeta
    
    def __init__(self, itype, xml_element, trace_dict, ruleset):
        ''' Constructor ''' 
        self.ev_type = itype
        self.trace_id = (0, itype) 
        self.description = None
        self.ruleset = ruleset
        
        # Initialize values
        init_rule_values(self, GCON_VALUES[self.ev_type])
        # Read the xml
        self._read_from_xml(xml_element, trace_dict)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the evaluatable'''
        try:
            resolve_and_validate_rule_values(self, self.ruleset, rule, GCON_VALUES[self.ev_type])
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], '\'{0}\' element {1}'.format(self.ev_type, e.msg))
        return
    
    @abstractmethod
    def prime(self, event):
        ''' Prime the condition '''
        pass

    @abstractmethod
    def accumulate(self, event):
        ''' Accumulate events '''
        pass
    
    @abstractmethod
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the sets of events that make the condition true '''
        pass
        
    @abstractmethod
    def reset(self):
        '''Reset the condition'''
        pass
    
    def _read_from_xml(self, xml_element, trace_dict):
        ''' Read in the evaluatable form the input XML
        '''
        self.trace_id = trace_dict[xml_element]
        # attributes
        for att_key in xml_element.attrib:
            att_value = xml_element.attrib[att_key]
            if read_from_xml_rule_value(self, att_key, att_value, GCON_VALUES[self.ev_type]):
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
                    self.ruleset.parse_error(self.trace_id[0], '{0} element encountered an unexpected subelement: {1}'.format(self.ev_type, element_name))
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
        outstr += dump_rule_values(self, GCON_VALUES[self.ev_type])
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
    
    def _state_str(self, exclude_events=None):
        ''' Duplicate of str that includes the state ... attributes don't have state so reuse str support for those '''
        outstr = '<{0} gtp="{1}"'.format(self.ev_type, self.trace_id)
        outstr += dump_rule_values(self, GCON_VALUES[self.ev_type])
        outstr += self._str_attribute_additions()
        outstr += '>\n'
        if self.description is not None and len(self.description) > 0:
            outstr += '<description>{0}</description>\n'.format(self.description)
        outstr += '<state>'
        outstr += self._state_str_state_additions(exclude_events)
        outstr += '</state>'
        outstr += self._state_str_subelement_additions(exclude_events)
        outstr += '</{0}>\n'.format(self.ev_type)
        return outstr     
    
    def _state_str_subelement_additions(self, exclude_events):
        ''' Additions to the output state str from subelements'''
        return ''
    
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        return ''
    
    @abstractmethod
    def get_cross_ref(self):
        ''' return a list of incident ids used in the conditions '''
        pass
    
    def get_used_locations(self):
        ''' Get a set of used locations '''
        return None

    @abstractmethod
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        pass
    
    
class GearEvaluatableContainer(GearEvaluatable): 
    ''' Evaluatable that contains other evaluatables '''
    
    def __init__(self, itype, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        self.evaluatables = []
        GearEvaluatable.__init__(self, itype, xml_element, trace_dict, ruleset)
        return
    
    def resolve_and_validate(self, rule, imin=None, imax=None):
        ''' Resolve and validate the condition 
        
            NOTE: method adds optional parameters
        ''' 
        GearEvaluatable.resolve_and_validate(self, rule)
        
        # check limits
        if imin is not None and len(self.evaluatables) < imin:
            self.ruleset.parse_error(self.trace_id[0], '\'{0}\' element must contain at least {1} condition sub-elements'.format(self.ev_type, imin))
        if imax is not None and len(self.evaluatables) > imax:
            self.ruleset.parse_error(self.trace_id[0], '\'{0}\' element cannot contain more than {1} condition sub-elements'.format(self.ev_type, imax))

        # validate contained
        for evaluatable in self.evaluatables:
            evaluatable.resolve_and_validate(rule)
        return
    
    def prime(self, event):
        ''' Prime the condition ... pass on to contained '''
        for evaluatable in self.evaluatables:
            evaluatable.prime(event)
        return 
    
    def accumulate(self, event):
        ''' Accumulate events '''
        for evaluatable in self.evaluatables:
            evaluatable.accumulate(event)
        return
    
    def reset(self):
        '''Reset the condition'''
        GearEvaluatable.reset(self)
        for evaluatable in self.evaluatables:
            evaluatable.reset()
        return 
    
    def _read_from_xml_other_subelements(self, xml_element, trace_dict):
        ''' Read in the contained conditions ''' 
        new_eval = evaluatable_creator(xml_element, trace_dict, self.ruleset, self.trace_id)
        if new_eval is None:
            return False
        self.evaluatables.append(new_eval)
        return True
    
    def _str_subelement_additions(self):
        ''' Additions to the output str '''
        outstr = ''
        for evaluatable in self.evaluatables:
            outstr += str(evaluatable)
        return outstr
    
    def _state_str_subelement_additions(self, exclude_events):
        ''' Additions to the output state str from subelements'''
        outstr = ''
        for evaluatable in self.evaluatables:
            outstr += evaluatable._state_str(exclude_events)
        return outstr
    
    def get_cross_ref(self):
        ''' get list of incident ids using in conditions '''
        result = []
        for evaluatable in self.evaluatables:
            result.extend(evaluatable.get_cross_ref())
        return result
    
    def get_used_locations(self):
        ''' Get a set of used locations '''
        used_locs = set()
        for evaluatable in self.evaluatables:
            t_used_locs = evaluatable.get_used_locations()
            if t_used_locs is not None:
                used_locs.update(t_used_locs)
        return used_locs
        
    
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        result = []
        for evaluatable in self.evaluatables:
            tmp_events = evaluatable.get_checked_event_info()
            # If any return None then indeterminate
            if tmp_events is None:
                return None
            result.extend(tmp_events)
        return result
    
class GearCondition(GearEvaluatableContainer):
    '''Class to represent a rule condition '''
  
    def __init__(self, init_xml_element, trace_dict, ruleset):
        ''' Constructor '''
        self.primes = []
        GearEvaluatableContainer.__init__(self, GCON_TYPE_CONDITION, init_xml_element, trace_dict, ruleset)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition''' 
        GearEvaluatableContainer.resolve_and_validate(self, rule, imin=1, imax=1)
        return
    
   
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the sets of events that make the condition true 
        
            NOTE: This class adds optional parameters 
        '''
        try:
            results = self.evaluatables[0].get_truth_space(exclude_events, exclude_primes)
            if results is not None and len(results) != 0: 
                get_logger().debug('Condition: {0}'.format(_dump_truth_space(results)))
            #else:
            #    print "Results is " + str(results)
        except:
            get_logger().fatal('Condition {0} failed getting truth space'.format(self.trace_id))
            raise
        return results

    
class GearEvaluatableEventEquals(GearEvaluatable):
    '''Evaluate if the current event matches the specified event values'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearEvaluatable.__init__(self, GCON_TYPE_EVENT_EQUALS, xml_element, trace_dict, ruleset)
        self.event_list = []
        self.primes = []
        return 
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition'''
        GearEvaluatable.resolve_and_validate(self, rule)
   
        if not self.id.is_set():
            self.ruleset.parse_error(self.trace_id[0], '\'event_equals\' element requires \'id\' attribute')
        if not self.comp.is_set():
            self.ruleset.parse_error(self.trace_id[0], '\'event_equals\' element requires component to be specified or defaulted')
        self.ruleset.validate_event_id(self.comp, self.id, self.trace_id)
        
        return
    
    def prime(self, event):
        ''' prime with the events '''
        if event.match(self.id.get_value(), self.comp.get_value(), None, None, None) == True:
            self.primes.append(event)
            get_logger().debug('event_equals primed event {0}'.format(str(event)))
        else:
            pass
            #get_logger().debug('event_equals {0} DID NOT prime event {1}'.format(self.id.get_value(),str(event)))
        return 
        
    def accumulate(self, event):
        ''' Accumulate events '''
        if event.match(self.id.get_value(), self.comp.get_value(), None, None, None) == True:
            self.event_list.append(event)
            get_logger().debug('event_equals accumulated event {0}'.format(str(event)))
        else:
            pass
            #get_logger().debug('event_equals {0} DID NOT accumulate event {1}'.format(self.id.get_value(),str(event)))
        return
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the sets of events that make the condition true '''
        result_set = set()
        tmp_events = self.event_list[:]
        if exclude_primes == False:
            tmp_events.extend(self.primes)
        if exclude_events is not None:
            for event in exclude_events:
                if event in tmp_events:
                    tmp_events.remove(event)
                    
        if len(tmp_events) == 0:
            return None
        
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            result_set.add((frozenset(), frozenset(tmp_events)))
            get_logger().debug('event_equals {0}'.format(_dump_truth_space(result_set)))
            return result_set
        
        for event in tmp_events:
            if self.scope.is_set() and self.scope.get_value()[1] is not None:
                try:
                    sc_loc = event.src_loc.new_location_by_scope(self.scope.get_value()[1])
                except:
                    get_logger().exception('event_equals exception!')
            else:
                sc_loc = event.src_loc
            result_set.add((frozenset([sc_loc]), frozenset([event])))
            
        get_logger().debug('event_equals {0}'.format(_dump_truth_space(result_set)))
        return result_set
    
    def reset(self):
        ''' Reset the condition '''
        del self.event_list[:]
        del self.primes[:]
        return
        
    def get_cross_ref(self):
        ''' Return the id in a list '''
        try:
            result = [self.id.get_value()]
        except:
            result = [self.id.in_str]
        return result

    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        try:
            result = [(self.comp.get_value(), self.id.get_value())]
        except:
            result = None
        return result
 
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        
        verbose = self.ruleset.gear_rule_debug == 'V'
        outstr = '{0} = {1}\n'.format(self.id.in_str, self.id.get_value())

        if exclude_events is None:
            ck_exclude = []
        else:
            ck_exclude = exclude_events
        tmp_events = self.event_list[:]
        tmp_events.extend(self.primes)
                    
        events_by_loc = defaultdict(list)
        exclude_by_loc = defaultdict(list)
        locs = set()
        tot_events = 0
        tot_exclude = 0 
        for e in tmp_events:
            # Get location
            if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
                use_loc = None
            else:
                use_loc = e.src_loc
                if self.scope.is_set() and self.scope.get_value()[1] is not None:
                    try:
                        use_loc = e.src_loc.new_location_by_scope(self.scope.get_value()[1])
                    except:
                        get_logger().exception('event_equals exception!')
            locs.add(use_loc)
            if e in ck_exclude:
                exclude_by_loc[use_loc].append(e)
                tot_exclude += 1 
            else:
                events_by_loc[use_loc].append(e)
                tot_events += 1
        
        loc_included = len(locs)
        for loc in locs:
            outstr += '  {0}\n'.format(str(loc) )
            if len(exclude_by_loc[loc]) != 0 or (verbose == True and exclude_events is not None):
                outstr += '          suppressed: '
                outstr += str(len(exclude_by_loc[loc])) + '> '
                outstr += ','.join([e.brief_str() for e in exclude_by_loc[loc]]) + '\n'
            if len(events_by_loc[loc]) != 0 or verbose == True:
                outstr += '          ' 
                outstr += str(len(events_by_loc[loc])) + '> '
                outstr += ','.join([e.brief_str() for e in events_by_loc[loc]]) + '\n'
            if len(events_by_loc[loc]) == 0:
                loc_included -= 1 
            
        if exclude_events is None:
            outstr += '  SUMMARY matched locs: total = {0}'.format(len(locs))
            outstr += '  events: total = {0}'.format(tot_events)
        else:
            outstr += '  SUMMARY matched locs: total = {0} included = {1}  suppressed = {2}'.format(len(locs), loc_included, len(locs) - loc_included)
            outstr += '  events: total = {0} included = {1}  suppressed = {2}'.format(tot_events + tot_exclude, tot_events, tot_exclude)
        outstr +='\n'  
        return outstr
    
    
class GearEvaluatableOr(GearEvaluatableContainer):
    '''Evaluate if the current event matches the specified event values'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearEvaluatableContainer.__init__(self, GCON_TYPE_OR, xml_element, trace_dict, ruleset)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition''' 
        GearEvaluatableContainer.resolve_and_validate(self, rule, imin=1)
        # Resolve get_truth_space method 
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            self.get_truth_space = self._get_truth_space_IGNORE
        else:
            self.get_truth_space = self._get_truth_space_IDENTICAL_and_UNIQUE
        return
        
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Must be defined because abstract -- will never be used because
            get_truth_space is set to one of the following during init '''
        pass 
    
    def _get_truth_space_IDENTICAL_and_UNIQUE(self, exclude_events, exclude_primes=False):
        ''' Get the sets that make the condition true when location match is identical or unique '''
        result_space = set()
        for evaluatable in self.evaluatables:
            ev_space = evaluatable.get_truth_space(exclude_events, exclude_primes)
            #print 'or element From contained evaluatable {0}'.format(_dump_truth_space(ev_space))
            if ev_space is not None:
                if self.scope.is_set():
                    #print 'scope = ' + str(self.scope.get_value())
                    ev_space = _scope_truth_space(ev_space, self.scope)
                if ev_space is not None:
                    result_space = result_space.union(ev_space)
                
        #print 'or element Final {0}'.format(_dump_truth_space(result_space))
        get_logger().debug('or element {0}'.format(_dump_truth_space(result_space)))
        return result_space
    
    def _get_truth_space_IGNORE(self, exclude_events, exclude_primes=False):
        ''' Get the sets that make the condition true when location match is ignore '''
        all_events = set()
        for evaluatable in self.evaluatables:
            ev_set = evaluatable.get_truth_space(exclude_events, exclude_primes)
            if ev_set is not None:
                for t_point in ev_set:
                    all_events.update(t_point[1])
        if len(all_events) == 0:
            return None
        result_space = set()
        result_space.add((frozenset(), frozenset(all_events)))
        return result_space
       

class GearEvaluatableAnd(GearEvaluatableContainer):
    '''Evaluate if the current event matches the specified event values'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearEvaluatableContainer.__init__(self, GCON_TYPE_AND, xml_element, trace_dict, ruleset)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition''' 
        GearEvaluatableContainer.resolve_and_validate(self, rule, imin=1)
        # Resolve the accumulate method
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            self.get_truth_space = self._get_truth_space_IGNORE
        elif self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_UNIQUE:
            self.get_truth_space = self._get_truth_space_UNIQUE
        else:
            self.get_truth_space = self._get_truth_space_IDENTICAL

        return

    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Must be defined because abstract -- will never be used because
            get_truth_space is set to one of the following during init '''
        pass 
    
    def _get_truth_space_IDENTICAL(self, exclude_events, exclude_primes=False):
        ''' Get the sets that make the condition true when location match is identical '''
        result_space = set()
        t_events_by_t_locs = defaultdict(list)
        # Collect from all the evaluatables
        for evaluatable in self.evaluatables:
            ev_space = evaluatable.get_truth_space(exclude_events, exclude_primes)
            #print 'and element From contained evaluatable {0}'.format(_dump_truth_space(ev_space))
            if ev_space is None or len(ev_space) == 0:
                # All have to be true, one isn't
                return result_space
            if self.scope.is_set():
                #print 'scope = ' + str(self.scope.get_value())
                ev_space = _scope_truth_space(ev_space, self.scope)
            #print 'and element From contained evaluatable SCOPED {0}'.format(_dump_truth_space(ev_space))
            # Add to the list for each location
            for ev_locs, ev_events in ev_space:
                t_events_by_t_locs[ev_locs].append(ev_events)
    
        # Now see which locations have enough to move forward
        for ev_locs, ev_events_list in t_events_by_t_locs.items():
            if len(ev_events_list) != len(self.evaluatables):
                continue
            # Collect all the events for that location 
            ev_events_all = set()
            for ev_events in ev_events_list:
                ev_events_all.update(ev_events)

            # Add the truth point of the location and the collected events
            result_space.add((ev_locs, frozenset(ev_events_all)))
            
        return result_space 
    
    def _get_truth_space_UNIQUE(self, exclude_events, exclude_primes=False):
        ''' Get the sets that make the condition true when location match is unique '''
        result_space = set()
        t_events_by_t_locs_by_ev = {}
        # Collect from all the evaluatables
        for ev_idx, evaluatable in enumerate(self.evaluatables):
            t_events_by_t_locs_by_ev[ev_idx] = defaultdict(list)
            ev_space = evaluatable.get_truth_space(exclude_events, exclude_primes)
            if ev_space is None:
                # All have to be true, one isn't
                return result_space
            # Scope to the scope specified on this and
            ev_space = _scope_truth_space(ev_space, self.scope)
            # Add to the list for each location
            for ev_locs, ev_events in ev_space:
                t_events_by_t_locs_by_ev[ev_idx][ev_locs].append(ev_events)

        # Now have to look at all of the evaluatables to see if any 
        #  product of the locations where they were true will work
        # Build the list of locations lists
        ev_locs_lists_list = []
        for ev_t_events_by_locs in t_events_by_t_locs_by_ev.values():
            ev_locs_lists_list.append(list(ev_t_events_by_locs.keys()))
        
        # Generate a list of unique key lists
        #   product of all loc lists with any that have duplicates removed
        good_loc_lists = [loc_list for loc_list in itertools.product(*ev_locs_lists_list) if len(set(loc_list)) == len(self.evaluatables)]

        for u_locs_list in good_loc_lists:
            t_events_complete = set()
            for ev_idx, t_events_by_t_locs in t_events_by_t_locs_by_ev.items():
                for add_t_events in t_events_by_t_locs[u_locs_list[ev_idx]]:
                    t_events_complete.update(add_t_events)
            t_locs_complete = set()
            for t_locs in u_locs_list:
                t_locs_complete.update(t_locs)
            result_space.add((frozenset(t_locs_complete), frozenset(t_events_complete)))
        return result_space
    
    def _get_truth_space_IGNORE(self, exclude_events, exclude_primes=False):
        ''' Get the sets that make the condition true when location match is ignore '''
        all_events = set()
        for evaluatable in self.evaluatables:
            ev_space = evaluatable.get_truth_space(exclude_events, exclude_primes)
            # If one of the contained has nothing, then not true
            if ev_space is None:
                return None
            for t_point in ev_space:
                all_events.update(t_point[1])
        return (frozenset(), frozenset(all_events))


class GearEvaluatableNot(GearEvaluatableContainer):
    '''Evaluate if the current event matches the specified event values'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearEvaluatableContainer.__init__(self, GCON_TYPE_NOT, xml_element, trace_dict, ruleset)
        # Not's location match and scope is the same as what it contains 
        self.scope = self.evaluatables[0].scope
        self.location_match = self.evaluatables[0].location_match
        self.events_by_loc = defaultdict(list)
        self.primed_events_by_loc = defaultdict(list)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition''' 
        GearEvaluatableContainer.resolve_and_validate(self, rule, imin=1, imax=1)
        
        # Doesn't support location match of unique at this point
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_UNIQUE:
            self.ruleset.parse_error(self.trace_id[0], '\'not\' element does not support containment of elements with \'location_match\' attribute being set to \'unique\'')
        return
    
    def prime(self, event):
        ''' Prime with events moving forward '''
        self.primed_events_by_loc[self._get_loc(event)].append(event)
        self.evaluatables[0].prime(event)
        return 
    
    def accumulate(self, event):
        ''' Accumulate all events '''
        self.events_by_loc[self._get_loc(event)].append(event)
        self.evaluatables[0].accumulate(event)
        return
    
    def _get_loc(self, event):
        ''' Get the event loc to use to track it '''
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            new_loc = None
        elif self.scope.is_set():
            try:
                new_loc = event.src_loc.new_location_by_scope(self.scope.get_value()[1])
            except:
                # If can't scope then ignore it
                self.ruleset.debug(self.trace_id[0], 'Event ignored because cannot scope {0} using {1}'.format(str(event.src_loc.get_location()), self.scope.in_str))
                return 
        else:
            new_loc =  event.src_loc
        return new_loc
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the truth space '''
        result_space = set()
        ev_truth_space = self.evaluatables[0].get_truth_space(exclude_events, exclude_primes)
        self.ruleset.trace_debug(self.trace_id[0], 'Not contained: {0}'.format(_dump_truth_space(result_space)))

        # Don't have to re-scope because scope is the same 
        
        # location match: IGNORE
        #    If contained was true at all then we are false
        #    else return everything as the truth space
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            # If contained was true at all, this is false
            if ev_truth_space is not None and len(ev_truth_space) != 0:
                return None
            
            # It was false so we are true --> truth space is everything (in the pool)
            if exclude_events is not None:
                all_events = [event for event in self.events_by_loc[None] if event not in exclude_events]
            else:
                all_events = self.events_by_loc[None][:]
            if exclude_primes == False:
                all_events.extend(self.primed_events_by_loc[None])
            # Make sure that didn't end up with nothing
            if len(all_events) == 0:
                return None
            result_space.add((frozenset(),frozenset(all_events))) 
            
        # location match: IDENTICAL
        #    if a location has an entry then it should not be in the result
        #    else all the values for the location should be returned
        elif self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IDENTICAL:
            # Figure out which locations have truth points
            remove_locs = set()
            if ev_truth_space is not None:
                for t_point in ev_truth_space:
                    remove_locs.update(t_point[0])
            # Add NOT truth points for each that wasn't
            for t_loc, t_list in self.events_by_loc.items():
                if t_loc not in remove_locs:
                    if exclude_primes == False:
                        t_list.extend(self.primed_events_by_loc[t_loc])
                    if exclude_events is not None:
                        t_list = [event for event in t_list if event not in exclude_events]
                    result_space.add((frozenset([t_loc]), frozenset(t_list)))

        # location match: UNIQUE
        else:
            self.ruleset.trace_debug(self.trace_id[0], 'Unsupported option -- should never occur')
            
        self.ruleset.trace_debug(self.trace_id[0], 'Not returned: {0}'.format(_dump_truth_space(result_space)))
        return result_space             
    
    def reset(self):
        ''' Reset the condition '''
        self.events_by_loc.clear()
        self.primed_events_by_loc.clear()
        return 
    
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        # Need to get all events
        return None
    
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        return 'NOT SUPPORTED YET'

class GearEvaluatableEventOccurred(GearEvaluatable):
    '''Evaluate if the event specified has occurred the specified number of times'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearEvaluatable.__init__(self, GCON_TYPE_EVENT_OCCURRED, xml_element, trace_dict, ruleset)
        self.prime_truth_space = set()
        self.truth_space = set()
        self.events_by_loc = defaultdict(list)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition'''
        GearEvaluatable.resolve_and_validate(self, rule)

        ## Validation
        # Make sure that the specified comp, id can actually occur
        self.ruleset.validate_event_id(self.comp, self.id, self.trace_id)

        # scope isn't allowed if location match is ignore
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE and self.scope.in_str is not None:
            self.ruleset.parse_error(self.trace_id[0], 'event_occurred element does not allow the \'scope\' attribute and \'ignore_loc\' attribute to be specified at the same time')            

        # Resolve accumulate method
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            self.accumulate = self._accumulate_IGNORE
        elif self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_UNIQUE:
            self.accumulate = self._accumulate_UNIQUE
        else:
            self.accumulate = self._accumulate_IDENTICAL
        return
    
    def prime(self, event):
        ''' prime with the events '''
        if event.match(self.id.get_value(), self.comp.get_value(), None, None, None) == True:
            self.accumulate(event)
            self.prime_truth_space = self.truth_space.copy()
            get_logger().debug('event_occurred primed event {0}'.format(str(event)))
        else:
            pass
            #get_logger().debug('event_occurred  {0} DID NOT prime event {1}'.format(self.id.get_value(),str(event)))
        return 
        
    def accumulate(self, event):
        ''' Accumulate events is actually implemented based on the location match.  The correct method 
            below is assigned in __init__.'''
        pass
    
    def _accumulate_IDENTICAL(self, event):
        ''' Get the sets that make the condition true when location match is identical '''
        if event.match(self.id.get_value(), self.comp.get_value(), None, None, None) == False:
            return 
        get_logger().debug('event_occurred accumulated (_identical) event {0}'.format(str(event)))
        
        if self.scope.is_set():
            try:
                new_loc = event.src_loc.new_location_by_scope(self.scope.get_value()[1])
            except:
                # If can't scope then ignore it
                get_logger().debug('Event ignored because cannot scope {0} using {1}'.format(str(event.src_loc.get_location()), self.scope.in_str))
                return 
        else:
            new_loc =  event.src_loc
        
        if self.num.get_value() == 1:
            self.truth_space.add((frozenset(new_loc), frozenset(event)))
            return 
        
        can_events = self.events_by_loc[new_loc]
        if len(can_events) >= self.num.get_value() - 1:
            # Get things this event can be combined with to be true
            for t_events in itertools.combinations(can_events, self.num.get_value()-1):
                tmp_events = list(t_events)
                tmp_events.append(event)
                self.truth_space.add((frozenset([new_loc]), frozenset(tmp_events)))
        
        self.events_by_loc[new_loc].append(event)
        return   
    
    def _accumulate_UNIQUE(self, event):
        ''' Get the sets that make the condition true when location match is unique '''
        # Make sure there are enough unique locations to start with
        if event.match(self.id.get_value(), self.comp.get_value(), None, None, None) == False:
            return 
        get_logger().info('event_occurred accumulated (_unique) event {0}'.format(str(event)))
        if self.scope.is_set():
            try:
                new_loc = event.src_loc.new_location_by_scope(self.scope.get_value()[1])
            except:
                # If can't scope then ignore it
                get_logger().debug('Event ignored because cannot scope {0} using {1}'.format(str(event.src_loc.get_location()), self.scope.in_str))
                return 
        else:
            new_loc =  event.src_loc

        if self.num.get_value() == 1:
            self.truth_space.add((frozenset(new_loc), frozenset(event)))
            return 

        can_locs = self.events_by_loc.keys()
        if new_loc in can_locs:
            can_locs.remove(new_loc)
        
        if len(can_locs) >= self.num.get_value() -1:
            for t_locs in itertools.combinations(can_locs, self.num.get_value() - 1):
                event_lists_list = []
                for t_loc in t_locs:
                    event_lists_list.append(self.events_by_loc[t_loc])
                for t_events in itertools.product(*event_lists_list):
                    tmp_events = list(t_events)
                    tmp_events.append(event)
                    tmp_locs = list(t_locs)
                    tmp_locs.append(new_loc)
                    self.truth_space.add((frozenset(tmp_locs), frozenset(tmp_events)))
        
        self.events_by_loc[new_loc].append(event)
        return 
    
    def _accumulate_IGNORE(self, event):
        ''' Get the sets that make the condition true when location match is identical or unique '''
        if event.match(self.id.get_value(), self.comp.get_value(), None, None, None) == False:
            return 
        get_logger().debug('event_occurred accumulated (_ignore) event {0}'.format(str(event)))
        
        self.events_by_loc[None].append(event)
        if self.num.get_value() >= self.num.get_value():
            self.truth_space.clear()
            self.truth_space.add((frozenset(), frozenset(self.events_by_loc[None])))
        return 
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Return the truth space removing the truth points that depend on execluded events and
            that contain truths from the primes '''
        result_space = self.truth_space.copy()
        if exclude_primes == True:
            result_space.difference_update(self.prime_truth_space)
        if exclude_events is not None:
            # Figure out what we really need to consider
            really_exclude = set()
            for event in exclude_events:
                if event.event_id == self.id.get_value():
                    really_exclude.add(event)
                   
            if len(really_exclude) == 0:
                return result_space
            
            # Look for true sets that contain the excluded events
            del_points = set()
            for truth_point in result_space:
                if truth_point[1].isdisjoint(really_exclude) == False:
                    del_points.add(truth_point)
            result_space.difference_update(del_points)
        get_logger().debug('result of any_event {0}: {1}'.format(self.trace_id, _dump_truth_space(result_space)))
        return result_space
    
    def reset(self):
        ''' Reset the condition '''
        self.prime_truth_space.clear()
        self.truth_space.clear()
        self.events_by_loc.clear()
        return
        
    def get_cross_ref(self):
        ''' Return the id in a list '''
        try:
            result = [self.id.get_value()]
        except:
            result = [self.id.in_str]
        return result
    
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        try:
            result = [(self.comp.get_value(), self.id.get_value())]
        except:
            result = None
        return result
    
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        return 'NOT SUPPORTED YET'
    
    
class GearEvaluatableAllEvents(GearEvaluatable):
    '''Evaluate if all of the specified events have occurred'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        GearEvaluatable.__init__(self, GCON_TYPE_ALL_EVENTS, xml_element, trace_dict, ruleset)
        self.prime_truth_space = set()
        self.truth_space = set()
        self.events_by_loc_by_id = {}
        self.events_by_id_by_loc = defaultdict(list)
        self.events_by_id = defaultdict(list)
        self.primed_events_by_id = defaultdict(list)
        return
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition'''
        GearEvaluatable.resolve_and_validate(self, rule)

        ## Validation
        # Make sure that the specified comp, id in the id list can actually occur
        self.ruleset.validate_event_ids(self.comp, self.ids, self.trace_id)

        # scope isn't allowed if location match is ignore
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE and self.scope.in_str is not None:
            self.ruleset.parse_error(self.trace_id[0], '\'all_events\' element does not allow the \'scope\' attribute with the \'location_match\' attribute specified as \'ignore\'')            

        # Resolve accumlate method
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            self.prime = self._prime_IGNORE
            self.accumulate = self._accumulate_IGNORE
            self.get_truth_space = self._get_truth_space_IGNORE
        elif self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_UNIQUE:
            self.prime = self._prime_IDENTICAL_UNIQUE
            self.accumulate = self._accumulate_UNIQUE
            self.get_truth_space = self._get_truth_space_IDENTICAL_UNIQUE
        else:
            self.prime = self._prime_IDENTICAL_UNIQUE
            self.accumulate = self._accumulate_IDENTICAL
            self.get_truth_space = self._get_truth_space_IDENTICAL_UNIQUE
            
        self.num_ids = len(self.ids.get_list())

        return     
    
    def prime(self, event): 
        ''' Place holder '''
        pass
    
    def _prime_IDENTICAL_UNIQUE(self, event):
        ''' prime with the events '''
        if event.event_id not in self.ids.get_list() or event.src_comp != self.comp.get_value():
            return 
        self.accumulate(event)
        self.prime_truth_space = self.truth_space.append(event)
        get_logger().debug('event_occurred primed (_identical_unique) event {0}'.format(str(event)))
        return 
    
    def _prime_IGNORE(self, event):
        ''' prime with the events '''
        if event.event_id not in self.ids.get_list() or event.src_comp != self.comp.get_value():
            return 
        self.primed_events_by_id[event.event_id]
        get_logger().debug('event_occurred primed (_ignore) event {0}'.format(str(event)))
        return 
        
    def accumulate(self, event):
        ''' Accumulate events is actually implemented based on the location match.  The correct method 
            below is assigned in __init__.'''
        pass
  
    def _accumulate_IDENTICAL(self, event):
        ''' Get the sets that make the condition true when location match is identical or unique '''
        if event.event_id not in self.ids.get_list() or event.src_comp != self.comp.get_value():
            return 
        get_logger().debug('all_events accumulated (_identical) event {0}'.format(str(event)))
        
        if self.scope.is_set():
            try:
                new_loc = event.src_loc.new_location_by_scope(self.scope.get_value()[1])
            except:
                # If can't scope then ignore it
                get_logger().debug('Event ignored because cannot scope {0} using {1}'.format(str(event.src_loc.get_location()), self.scope.in_str))
                return 
        else:
            new_loc =  event.src_loc
        
        if len(self.ids.get_list()) == 1:
            self.truth_space.add((frozenset([new_loc]), frozenset([event])))
            return 
        if new_loc in self.events_by_loc_by_id:
            can_events_by_id = self.events_by_loc_by_id[new_loc]
            can_ids = can_events_by_id.keys()
            if event.event_id in can_ids:
                can_ids.remove(event.event_id)
            # Make sure with this one we cover them all
            if len(can_ids) == len(self.ids.get_list()) - 1:
                event_lists_list = []
                for t_id in can_ids:
                    event_lists_list.append(can_events_by_id[t_id])
                for t_events in itertools.product(*event_lists_list):
                    tmp_events = list(t_events)
                    tmp_events.append(event)
                    self.truth_space.add((frozenset([new_loc]), frozenset(tmp_events)))
        else:
            self.events_by_loc_by_id[new_loc] = defaultdict(list)
        
        if event.event_id not in self.events_by_loc_by_id[new_loc]:
            self.events_by_loc_by_id[new_loc][event.event_id] = [event]
        self.events_by_loc_by_id[new_loc][event.event_id].append(event)
        return   
    
    def _accumulate_UNIQUE(self, event):
        ''' Get the sets that make the condition true when location match is identical or unique '''
        # Make sure there are enough unique locations to start with
        if event.event_id not in self.ids.get_list() or event.src_comp != self.comp.get_value():
            return 
        get_logger().debug('all_events accumulated (_unique) event {0}'.format(str(event)))
        if self.scope.is_set():
            try:
                new_loc = event.src_loc.new_location_by_scope(self.scope.get_value()[1])
            except:
                # If can't scope then ignore it
                get_logger().debug('Event ignored because cannot scope {0} using {1}'.format(str(event.src_loc.get_location()), self.scope.in_str))
                return 
        else:
            new_loc =  event.src_loc

        if len(self.ids.get_list()) == 1:
            self.truth_space.add((frozenset([new_loc]), frozenset([event])))
            return 
        # w_events_by_id_by_loc means it is a dictionary by id of a dictionary by location of events
        w_events_by_id_by_loc = self.events_by_id_by_loc.copy()
        if event.event_id in w_events_by_id_by_loc.keys():
            del w_events_by_id_by_loc[event.event_id]
        
        # Make sure with this one we cover all the ids
        if len(w_events_by_id_by_loc.keys()) == self.num_ids - 1:  
            events_by_locs_list = w_events_by_id_by_loc.values()
            loc_lists_list = [l.keys() for l in events_by_locs_list]
            for t_loc_list in itertools.product(*loc_lists_list):
                if new_loc in t_loc_list or len(set(t_loc_list)) != self.num_ids -1:
                    continue
                event_lists_list = []
                for t_loc, t_events_by_loc in zip(t_loc_list, events_by_locs_list):
                    event_lists_list.append(t_events_by_loc[t_loc])
                for t_events in itertools.product(*event_lists_list):
                    tmp_events = list(t_events)
                    tmp_events.append(event)
                    self.truth_space.add((frozenset(_get_scoped_locs(tmp_events, self.scope)), frozenset(tmp_events)))
         
        # Accumulate the event
        if event.event_id not in self.events_by_id_by_loc.keys():
            self.events_by_id_by_loc[event.event_id] = {}
        if new_loc not in self.events_by_id_by_loc[event.event_id].keys():
            self.events_by_id_by_loc[event.event_id][new_loc] = []
        self.events_by_id_by_loc[event.event_id][new_loc].append(event)
        return   
    
    def _accumulate_IGNORE(self, event):
        ''' Get the sets that make the condition true when location match is identical or unique '''
        if event.event_id not in self.ids.get_list() or event.src_comp != self.comp.get_value():
            return 
        get_logger().debug('all_events accumulated (_ignore) event {0}'.format(str(event)))
        
        self.events_by_id[event.event_id].append(event)
        return 
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Place holder '''
        pass
    
    def _get_truth_space_IDENTICAL_UNIQUE(self, exclude_events, exclude_primes=False):
        ''' Return the truth space removing the truth points that depend on excluded events and
            that contain truths from the primes '''
        result_space = self.truth_space.copy()
        if exclude_primes == True:
            result_space.difference_update(self.prime_truth_space)
        if exclude_events is not None:
            # Figure out what we really need to consider
            really_exclude = set()
            for event in exclude_events:
                if event.event_id in self.ids.get_list() and event.src_comp == self.comp.get_value():
                    really_exclude.add(event)
                   
            if len(really_exclude) == 0:
                return result_space
            
            # Look for true sets that contain the excluded events
            del_points = set()
            for truth_point in result_space:
                if truth_point[1].isdisjoint(really_exclude) == False:
                    del_points.add(truth_point)
            result_space.difference_update(del_points)
        get_logger().debug('result of any_event {0}: {1}'.format(self.trace_id, _dump_truth_space(result_space)))
        return result_space
    
    def _get_truth_space_IGNORE(self, exclude_events, exclude_primes=False):
        ''' Return the truth space when ignoring location ''' 
        # Nothing matched or didn't match all of the ids return None (false)
        tmp_events_by_id = self.events_by_id.copy()
        if exclude_primes == False:
            for p_id, p_list in self.primed_events_by_id:
                tmp_events_by_id[p_id].extend(p_list)
        if exclude_events is not None:
            for e_event in exclude_events:
                if e_event in tmp_events_by_id[e_event.event_id]:
                    tmp_events_by_id[e_event.event_id].remove(e_event)
                    if len(tmp_events_by_id[e_event.event_id]) == 0:
                        del tmp_events_by_id[e_event.event_id]
        
        if len(tmp_events_by_id.keys()) == 0 or len(tmp_events_by_id.keys()) < self.num_ids:
            return None
        
        all_events = []
        for event_list in self.events_by_id.values():
            all_events.extend(event_list)
        if len(all_events) == 0:
            return None
        result_set = set()
        result_set.add((frozenset(), frozenset(all_events)))
        return result_set
    
    def reset(self):
        ''' Reset the condition '''
        self.prime_truth_space.clear()
        self.truth_space.clear()
        self.events_by_loc_by_id.clear()
        return
        
    def get_cross_ref(self):
        ''' Return the id in a list '''
        try:
            result = self.ids.get_list()
        except:
            result = self.ids.in_str.split(',')
        return result
    
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        try:
            comp = self.comp.get_value()
            result = [(comp, tid) for tid in self.ids.get_list()]
        except:
            result = None
        return result
    
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        return 'NOT SUPPORTED YET'


class GearEvaluatableAnyEvents(GearEvaluatable):
    '''Evaluate if all of the specified events have occurred'''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        self.instance_comparitor = None
        GearEvaluatable.__init__(self, GCON_TYPE_ANY_EVENTS, xml_element, trace_dict, ruleset)
        self.max_dups = 1
        self.prime_set = set()
        self.data = ConditionData(self)
        return

    def _str_attribute_additions(self):
        ''' Add instance attribute to output '''
        if self.instance_comparitor is not None:
            return str(self.instance_comparitor)
        return ''       

    def _read_from_xml_other_attributes(self, att_key, xml_element):
        ''' Read in the instances attribute '''
        if att_key == 'instances':
            self.instance_comparitor = Comparitor(xml_element.attrib['instances'], self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_UNIQUE)
            return True
        return False
    
    def resolve_and_validate(self, rule):
        '''Resolve and validate the condition'''
        GearEvaluatable.resolve_and_validate(self, rule)
        
        ## Validate
        # Make sure that the specified comp, ids in list can actually occur
        self.ruleset.validate_event_ids(self.comp, self.ids, self.trace_id)
        # if instances then must have instance loc comp
        if self.instance_comparitor is not None and self.instance_loc_comp.get_value()[1] is None:
            self.ruleset.parse_error(self.trace_id[0], '\'any_events\' element: \'instance_loc_comp\' attribute required when \'instances\' attribute is used')
        # if unique_instance then must NOT have instance loc comp
        if self.unique_instance.get_value() == True and self.instance_loc_comp.get_value()[1] is not None:
            self.ruleset.parse_error(self.trace_id[0], '\'any_events\' element: \'instance_loc_comp\' attribute cannot be used with \'unique_instance\' attribute is used')
        # Don't allow instance_loc_comp to be specified without one of the others
        if self.instance_loc_comp.get_value()[1] is not None and self.instance_comparitor is None:
            self.ruleset.parse_error(self.trace_id[0], '\'any_events\' element: \'instance_loc_comp\' attribute cannot be specified without \'instances\' attribute being used')
        # instance_scope can only be specified if unique_instances specified
        if self.instance_scope.get_value() is not None and self.unique_instance.get_value() is None:
            self.ruleset.parse_error(self.trace_id[0], '\'any_events\' element: \'instance_scope\' attribute cannot be specified without \'unique_instance\' attribute being used')
        # if match location is ignore then scope can't be specified 
        if self.location_match.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            if self.scope.in_str is not None:
                self.ruleset.parse_error(self.trace_id[0], '\'any_events\' element the \'scope\' attribute cannot be used when \'location_match\' is ignore')
        # Can't say unique and specify which instances
        if self.unique_instance.get_value() == True and self.instance_comparitor is not None:
            self.ruleset.parse_error(self.trace_id[0], '\'any_events\' element: \'instance\' and \'unique_instance\' attributes cannot be specified at the same time')

        # Configure data based on parameters
        self.data.use_loc(self.location_match.get_value(), self.scope.get_value()[1])
        if self.unique_id.get_value() == True:
            self.data.use_unique_id()
        if self.unique_instance.get_value() == True:
            self.data.use_unique_instance(self.instance_scope.get_value()[1])
        elif self.instance_comparitor is not None:
            self.data.use_comp_instance(self.instance_loc_comp.get_value()[1], self.instance_comparitor)
        
        return
    
    def prime(self, event):
        ''' prime events '''
        if event.event_id not in self.ids.get_list():
            # Not in list of events interested in, so do not accumulate it
            return 
        self.prime_set.add(event)
        self.accumulate(event)
        return 
    
    def accumulate(self, event):
        ''' Accumulate events '''
        # First See if it is in the list of ids -- if not nothing to do
        if event.event_id not in self.ids.get_list() or event.src_comp != self.comp.get_value():
            return 
        
        # Get the locations for this event 
        if self.locations.is_set():
            locs = self.locations.get_list()
        else:
            locs = [event.src_loc]
            
        for loc in locs: 
            try:
                self.data.accumulate(event, loc)
            except InstanceError:
                pass
        self.max_dups = max(self.max_dups, len(locs))
        return  
    
    def get_truth_space(self, exclude_events, exclude_primes):
        ''' Get the sets of events that make the condition true '''
        if exclude_events is not None:
            self.data.remove_events(exclude_events)
        if exclude_primes == True:
            use_primes = self.prime_set
        else:
            use_primes = None
        return self.data.get_truth_space(use_primes, self.num.get_value(), self.max_dups)
    
    def reset(self):
        '''reset the condition'''
        self.prime_set.clear()
        self.data.clear()
        return
    
    def get_cross_ref(self):
        ''' return ids used '''
        try:
            result = self.ids.get_list()
        except:
            result = self.ids.in_str.split(',')
        return result
    
    def get_used_locations(self):
        ''' Need to return locations if set ''' 
        if self.locations.is_set():
            return set(self.locations.in_str.split(','))
        return None
    
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        try:
            comp = self.comp.get_value()
            result = [(comp, tid) for tid in self.ids.get_list()]
        except:
            result = None
        return result
    
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        outstr = '{0} = {1}\n'.format(self.ids.in_str, ','.join(sorted(list(self.ids.get_list()))))
        # Print out the primes
        if len(self.prime_set) == 0:
            outstr += '  primed 0>\n'
        else:
            primed_exl = []
            primed = []
            if exclude_events is None:
                primed = self.prime_set   
            else:  
                for e in self.prime_set:
                    if e in exclude_events:
                        primed_exl.append(e)
                    else:
                        primed.append(e)
            if len(primed) != 0:
                outstr += '  primed {0}> {1}\n'.format(len(primed), ','.join([e.brief_str() for e in primed]))
            if len(primed_exl) != 0:
                outstr += '  primed suppressed {0}> {1}\n'.format(len(primed_exl), ','.join([e.brief_str() for e in primed_exl]))
            
        # Print out other events 
        outstr += self.data._state_str(excluded=exclude_events)
        return outstr
        

class GearEvaluatableEvaluate(GearEvaluatable):
    ''' Call external Python routine to evaluate the condition '''

    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Constructor '''
        self.parms = RuleParms()
        GearEvaluatable.__init__(self, GCON_TYPE_EVALUATE, xml_element, trace_dict, ruleset)

        # Construct the external class
        class_spec = self.ext_class.in_str
        if class_spec is None or class_spec == '':
            self.ruleset.parse_error(self.trace_id[0], 'evaluate element requires the \'ext_class\' attribute')
        try:
            module_name, class_name = class_spec.rsplit('.', 1)
            module = __import__(module_name, globals(), locals(), [class_name])
            tmp_class = getattr(module, class_name)
        except:
            self.ruleset.parse_error(self.trace_id[0], 'evaluate element was unable to load specified the class: {0}'.format(self.class_spec))
        
        # Get parameters to pass to init 
        try:
            self.parms.resolve_and_validate(self.ruleset, None, rule_part=GRUL_PART_EXTERNAL)
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], 'evaluate element parm error: {0}'.format(e.msg))
        init_dict = self.parms.get_dict()
        init_dict['evaluate_name'] = self.name.in_str
    
        try:
            self.call_class = tmp_class(init_dict)
        except BaseException as e:
            get_logger().exception('evaluate element with name {0} failed during initialization'.format(self.name.in_str))
            raise
        
        if isinstance(self.call_class, ExtEvaluate) == False:
            self.ruleset.parse_error(self.trace_id[0], 'evaluate ext_class must be a subclass of ExtEvaluate')
        return

    def _str_subelement_additions(self):
        ''' Add instance subelements to output '''
        if self.parms is not None:
            return str(self.parms)
        return ''       

    def _read_from_xml_other_subelements(self, xml_element, trace_dict):
        ''' Read in the instances attribute '''
        try:
            self.parms.read_from_xml(xml_element)
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], 'evaluate element parameter error: {0}'.format(e.msg))
        return True
    
    def prime(self, event):
        ''' Prime the condition '''
        try:
            self.call_class.prime(event)
        except:
            self.ruleset.trace_error(self.trace_id[1], 'evaluate {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return

    def accumulate(self, event):
        ''' Accumulate events '''
        try:
            self.call_class.accumulate(event)
        except:
            self.ruleset.trace_error(self.trace_id[1], 'evaluate {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the set of truth points (loc, truth events) that make the condition true '''
        result_space = set()
        try:
            # paranoid so make sure get set back
            tmp_result = self.call_class.get_truth_space(exclude_events, exclude_primes)
            if tmp_result is not None:
                result_space.update(tmp_result)
        except:
            self.ruleset.trace_error(self.trace_id[1], 'evaluate {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        if len(result_space) == 0:
            return None
        return result_space
        
    def reset(self):
        '''Reset the condition'''
        try:
            self.call_class.reset()
        except:
            self.ruleset.trace_error(self.trace_id[1], 'evaluate {0} call failed with exception'.format(self.name))
            get_logger().exception('')
        return
    
    def get_cross_ref(self):
        ''' return ids used '''
        try:
            result = self.call_class.get_cross_ref()
        except:
            result = []
        return result
    
    def get_checked_event_info(self):
        ''' Return list of (comp, event id) checked by this condition
            return None if indeterminant (GEAR variable)
        '''
        try:
            # TODO: Is this the right way to do this or should we add a new interface?
            comp = self.comp.get_value()
            result = [(comp, tid) for tid in self.call_class.get_cross_ref()]
        except:
            result = None
        return result
    
    def _state_str_state_additions(self, exclude_events):
        ''' Additions to the output state str for the state'''
        return 'NOT SUPPORTED YET'



#################################################### 
# Helper functions for working with locations
# 
 
def _get_scoped_loc(loc, scope_val, location_match_val):
    ''' Get the correct scoped location based on the scope and location_match '''
    if location_match_val.get_value() == GRVA_TYPE_LOCATION_MATCH_IGNORE:
        return None
    return loc.new_location_by_scope(scope_val.get_value()[1])

def _get_scoped_locs(events, scope_val):
    ''' Get a set of scoped locations from the events starting with init_locs '''
    result_locs = set()
    for event in events:
        try:
            result_locs.add(event.src_loc.new_location_by_scope(scope_val.get_value()[1]))
        except:
            continue
    return result_locs
 
####################################################   
# Helper functions for working with truth
#
#   truth_events = set( event, ... )
#   truth_point = tuple(truth_locs, truth_events)  where contained sets are frozen
#   truth_space = set( truth_point, ... ) 
#   truth_locs = set(scoped_loc)
#

def _scope_truth_space(truth_space, scope_var):
    ''' scope the locations in a true space and return a new true space with those locations '''
    if truth_space is None or len(truth_space) == 0:
        return None
    events_by_loc = defaultdict(list)
    for t_locs, t_events in truth_space:
        events_by_loc[_scope_truth_locs(t_locs, scope_var)].extend(t_events)
        
    result_space = set()
    for frz_t_locs, t_events_list in events_by_loc.items():
        result_space.add((frz_t_locs, frozenset(t_events_list)))
    return result_space
        
def _scope_truth_locs(truth_locs, scope_var):
    ''' scope the truth locs to the specified scope '''
    if scope_var is None or scope_var.is_set() == False:
        return truth_locs
    new_t_locs = set()
    for sc_loc in truth_locs:
        try:
            new_t_locs.add(sc_loc.new_location_by_scope(scope_var.get_value()[1]))
        except:
            continue
    return frozenset(new_t_locs)
                 
            
def _get_truth_space_truth_locs(truth_space, scope_var=None):
    ''' return the locations (optionally scoped) used in a truth space '''
    result = []
    if truth_space is None or len(truth_space) == 0:
        return result
    for t_point in truth_space:
        result.append(_scope_truth_locs(t_point[0], scope_var))
    return result

def _get_truth_events_by_truth_locs(truth_space, t_locs):
    ''' Find the entry in the truth_space for the specified location and 
        return the truth events associated with it 
        
        If not found returns an empty set '''
    for c_locs, c_events in truth_space:
        if t_locs == c_locs:
            return c_events
    return frozenset()
            
def _dump_truth_space(truth_space, name=None, prefix=''):
    ''' dump a truth space to string '''
    if name is None:
        outstr = ''
    else:
        outstr = '{0}Truth space for {1}\n'.format(prefix, name)
    prefix += '    '
    if truth_space is None or len(truth_space) == 0:
        outstr = '{0}-empty-\n'.format(prefix)
    else:
        for truth_point in truth_space:
            outstr += _dump_truth_point(truth_point, prefix=prefix)
    return outstr

def _dump_truth_point(truth_point, prefix=''):
    ''' dump a truth point to string '''
    return '{0}({1}): [ {2} ]'.format(prefix, ','.join([str(loc) for loc in truth_point[0]]), 
                                              ','.join([t.brief_str() for t in truth_point[1]]))
