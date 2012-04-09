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

import os
from collections import defaultdict
from datetime import datetime
from string import upper
from time import sleep

from ibm.teal.analyzer.analysis_info import AnalysisInfo, AI_MIN_TIME_IN_POOL,\
    AI_POOL_EXT_TIME
from ibm.teal.analyzer.gear.common import GRSE_GEAR_CTL, GRSE_EVENTS, GRSE_CONSTANTS, \
          GRSE_TEMPLATES, GRSE_ANALYZE, GRSE_POOL_CTL
from ibm.teal.analyzer.gear.constants import GearConstants, GCON_EVENT_ID
from ibm.teal.analyzer.gear.control import GearControl
from ibm.teal.analyzer.gear.pool_control import GearPoolControl,\
    GPCL_INIT_DURATION, GPCL_MAX_DURATION, GPCL_ARRIVAL_RATE_EXTENSION
from ibm.teal.analyzer.gear.rule import GearRule
from ibm.teal.analyzer.pool.incident_pool import POOL_MODE_OCCURRED,\
    POOL_MODE_LOGGED, IncidentPool, POOL_CLOSE_REASON_AS_STRING,\
    POOL_CLOSE_REASON_SHUTDOWN, \
    IncidentPoolStateTransitionError, IncidentPoolClosedError,\
    POOL_CLOSE_REASON_RULE, IncidentPoolEventCheckpoint
from ibm.teal.registry import get_logger, get_service, SERVICE_RUN_MODE, RUN_MODE_REALTIME,\
    SERVICE_ALERT_MGR, SERVICE_TIME_MODE
from ibm.teal.util.xml_file_reader import read_xml_file
from ibm.teal.analyzer.gear.templates import GearTemplates
from ibm.teal.analyzer.gear.engine import GearEngine
from ibm.teal.metadata import META_ALERT_PRIORITY
from ibm.teal.analyzer.gear.error_handlers import GearErrorHandlers 
from ibm.teal.util.msg_target import MsgTargetLogger
from ibm.teal.analyzer.gear.rule_value import _parse_gear_variable
from ibm.teal.util.teal_thread import ThreadKilled

TEAL_ALERT_PRIORITIZATION = 'TEAL_ALERT_PRIORITIZATION'
TEAL_TEST_POOL_TIMERS_OFF = 'TEAL_TEST_POOL_TIMERS_OFF'
TEAL_TEST_GEAR_RULE_DEBUG = 'TEAL_TEST_GEAR_RULE_DEBUG'

class GearRuleset(dict, GearEngine):
    '''
    Dictionary of ruleset sections
    '''
    def __init__(self, xml_ruleset_file, config_dict=None, event_input=False, alert_input=False, number=0, name='unnamed', trace=None, send_alert=None, use_checkpoint=True):
        '''
        Load the list of specified xml ruleset file
        '''
        dict.__init__(self)
        if use_checkpoint == True: 
            self.checkpoint = RulesetEventCheckpoint(name, self)
        else:
            self.checkpoint = None
        GearEngine.__init__(self, name, number, trace, self.checkpoint)
        self.version_id = None
        self.trace_id = (0, str(self.number))  #line 0, trace level 1
        self.conf_dict = config_dict
        self.send_alert = send_alert
        self.alert_input = alert_input
        self.event_input = event_input 
        
        # See if debug environment variable
        temp_debug = upper(os.environ.get(TEAL_TEST_GEAR_RULE_DEBUG, 'NO'))
        if  temp_debug == 'YES' or temp_debug == 'NORMAL':
            self.gear_rule_debug = 'N'
        elif temp_debug == 'VERBOSE':
            self.gear_rule_debug = 'V'
        else:
            self.gear_rule_debug = None
        
        if self.alert_input:
            get_logger().warning('Only event analyzers are supported by GEAR at this time')
            raise ValueError 
        if not event_input: # and not alert_input
            get_logger().warning('GEAR analyzer must be an event analyzer')
            raise ValueError

        self.trace_debug(self.trace_id[1], 'Initializing ruleset id={0} name={1} file={2}'.format(self.number, self.name, xml_ruleset_file))

        ## Determine mode
        if get_service(SERVICE_TIME_MODE) is not None and get_service(SERVICE_TIME_MODE) == 'time_logged':
            self.mode = POOL_MODE_LOGGED
        else: 
            self.mode = POOL_MODE_OCCURRED
        # See if overridden in config dict
        if config_dict is not None and SERVICE_TIME_MODE in config_dict:
            conf_rm = config_dict[SERVICE_TIME_MODE]
            if conf_rm == 'time_logged':
                if self.mode != POOL_MODE_LOGGED:
                    self.trace_info(self.trace_id[1], 'Time mode forced to time_logged')
                    self.mode = POOL_MODE_LOGGED
            elif conf_rm == 'time_occurred':
                if self.mode != POOL_MODE_OCCURRED:
                    self.trace_info(self.trace_id[1], 'Time mode forced to time_occurred')
                    self.mode = POOL_MODE_OCCURRED
            else:
                self.config_error('Invalid configuration specification for {0}: {1}'.format(SERVICE_TIME_MODE, config_dict[SERVICE_TIME_MODE]))
            
        self[GRSE_GEAR_CTL] = GearControl(self)
        self[GRSE_EVENTS] = AnalysisInfo(self)
        self[GRSE_CONSTANTS] = GearConstants(self)
        self[GRSE_POOL_CTL] = GearPoolControl(config_dict, self)
        self[GRSE_ANALYZE] = GearAnalyzeRules(self)
        self[GRSE_TEMPLATES] = GearTemplates(self)
        
        self.xml_ruleset_file = xml_ruleset_file
        self.description = 'Loaded from file {0}'.format(str(xml_ruleset_file))
        self._parse_file(xml_ruleset_file)
        
        # Check how to determine how to decided if will analyze
        if self[GRSE_GEAR_CTL].use_event_regx:
            self.will_analyze_event = self.will_analyze_event_regx
            self.will_analyze_event_validation = self.will_analyze_event_validation_regx
    
        # Templates don't resolve and validate
        self[GRSE_CONSTANTS].resolve_and_validate()
        self[GRSE_ANALYZE].resolve_and_validate()
        #self[GRSE_POOL_CLOSURE].resolve_and_validate()
        self[GRSE_POOL_CTL].resolve_and_validate()
        
        if self.event_input:
            if (not self[GRSE_GEAR_CTL].use_event_regx) and \
               len(self[GRSE_EVENTS].event_info) == 0:
                self.parse_error(self.trace_id[0], 'events to analyze must be specified either using the \'events\' element or the \'will_analyze\' element')
        
        # Setup the initial pool
        #   Only use timers if in realtime mode
        if get_service(SERVICE_RUN_MODE) is not None and get_service(SERVICE_RUN_MODE) == RUN_MODE_REALTIME:
            t_use_timer = True
            if os.environ.get(TEAL_TEST_POOL_TIMERS_OFF, 'NO') == 'YES':
                get_logger().warning('Timers were turned off by environment variable: {0}'.format(TEAL_TEST_POOL_TIMERS_OFF))
                t_use_timer = False
        else: 
            t_use_timer = False
        # create the pool
        self.event_pool = IncidentPool.new_pool(self.mode, self._get_init_duration(), 
                                                    self._get_max_duration(), 
                                                    self.close_event_pool_callback, 
                                                    msg_target=MsgTargetLogger(self.get_tracer(), prefix='GTP[{0}.P]'.format(self.number)),
                                                    use_timer=t_use_timer,
                                                    arrival_check_ctl=self[GRSE_POOL_CTL][GPCL_ARRIVAL_RATE_EXTENSION])
    
        # Check environment variable to see if alert prioritization should be done
        if upper(os.environ.get(TEAL_ALERT_PRIORITIZATION, 'YES')) == 'YES':
            self.prioritize_and_send_alerts = self._prioritize_and_send_alerts_ACTIVE
        else:
            get_logger().info('Alert prioritization has been turned off')
            self.prioritize_and_send_alerts = self._prioritize_and_send_alerts_NO_PRIORITY
                     
        return   
           
    def _get_init_duration(self):
        ''' helper to get the initial pool duration '''
        return self[GRSE_POOL_CTL][GPCL_INIT_DURATION]
    
    def _get_max_duration(self):
        ''' helper to get the maximum pool duration '''
        return self[GRSE_POOL_CTL][GPCL_MAX_DURATION]
   
    def _parse_file(self, file):
        '''Parse the xml metadata file
        '''
        top_elem, trace_dict = read_xml_file(file, self.number-1)
        if top_elem.tag.split('}')[-1] != 'gear_ruleset':
            self.parse_error(self.trace_id[0], 'root element must be \'gear_ruleset\'')
        # attributes
        for att_key in top_elem.attrib:
            if att_key == 'version_id':
                self.version_id = top_elem.attrib['version_id']
            elif att_key == 'schema_version':
                if top_elem.attrib['schema_version'] != '1.0':
                    self.parse_error(self.trace_id[0], 'gear_ruleset element schema_version was {0} but only 1.0 is currently supported'.format(top_elem.attrib['schema_version']))
            else:
                self.parse_error(self.trace_id[0], 'gear_ruleset element encountered an unexpected attribute: {0}'.format(att_key))
        # elements
        # Have to do the templates first
        template_list = top_elem.findall(GRSE_TEMPLATES)
        if len(template_list) > 0:
            if len(template_list) > 1:
                self.parse_error(self.trace_id[0], 'gear_ruleset element encountered multiple template sub-elements')
            self[GRSE_TEMPLATES].read_from_xml(template_list[0], trace_dict)
        # Now do the rest of the elements
        for event_entry in top_elem:
            entry_name = event_entry.tag.split('}')[-1]
            if entry_name == GRSE_EVENTS:
                if not self.event_input:
                    self.parse_error(self.trace_id[0], 'gear ruleset element \'{0}\' is not supported for this analyzer'.format(GRSE_EVENTS))
                self[GRSE_EVENTS].add_event_info_xml(event_entry, trace_dict)
                if len(self[GRSE_EVENTS].event_info) == 0:
                    self.parse_error(trace_dict[event_entry][0], 'events element specified with no \'event\' elements')
                self[GRSE_CONSTANTS].add_constants(GCON_EVENT_ID, self[GRSE_EVENTS].get_constants(GCON_EVENT_ID))
            elif entry_name == GRSE_CONSTANTS:
                self[GRSE_CONSTANTS].add_constants_xml(event_entry, trace_dict)
            elif entry_name == GRSE_GEAR_CTL:
                self[GRSE_GEAR_CTL].read_xml(event_entry, trace_dict)
            elif entry_name == GRSE_POOL_CTL:
                self[GRSE_POOL_CTL].read_xml(event_entry, trace_dict)
            elif entry_name == GRSE_ANALYZE:
                self[GRSE_ANALYZE].read_from_xml(event_entry, trace_dict)
            elif entry_name == GRSE_TEMPLATES:
                # Handled up front, so skip it
                pass 
            elif entry_name == 'description':
                self.description = event_entry.text
            else:
                # Unexpected element
                self.parse_error(self.trace_id[0], 'unexpected element {0}'.format(entry_name))
        return
    
    def close_event_pool_callback(self, reason, last_rec_id):
        '''
        Close callback
        '''
        self.trace_info(str(self.number), 'Pool closed.  Reason = {0}   Last event = {1}'.format(POOL_CLOSE_REASON_AS_STRING[reason], str(last_rec_id)))
        get_logger().debug('Close_callback called')
        get_logger().debug('     Pool closing: {0}'.format(str(self.event_pool)))
        
        new_alerts = self.close_pool(self.event_pool)
        for alert in new_alerts:
            get_logger().debug('       ALERT: creating {0}'.format(str(alert)))
            alert_mgr = get_service(SERVICE_ALERT_MGR)
            alert_mgr.add_suppressions(alert, self.event_pool.get_suppressed(alert))
        self.prioritize_and_send_alerts(new_alerts)
        
        if self.checkpoint is not None:
            self.checkpoint.set_checkpoint_from_pool()
            
        if reason != POOL_CLOSE_REASON_SHUTDOWN:
            new_pool = IncidentPool.next_pool(self.event_pool)
            for event in new_pool.moved_forward:
                self.prime_event(event, new_pool)
            self.event_pool = new_pool
        return   
    
    def _prioritize_and_send_alerts_ACTIVE(self, alerts): 
        ''' Prioritize and send the alerts '''
        alert_mgr = get_service(SERVICE_ALERT_MGR)
        alerts_to_pri_by_pri = defaultdict(list)
        for alert in alerts:
            if alert.priority is None:
                try:
                    alert.priority = alert.get_metadata()[META_ALERT_PRIORITY]
                except ThreadKilled:
                    raise
                except:
                    get_logger().debug('Unable to get alert metadata for {0}'.format(str(alert.alert_id)))
                    
                if alert.priority is None:
                    get_logger().debug('       Alert with no priority: creating {0}'.format(str(alert)))
                    alert_mgr.commit(alert)
                    self.send_alert(alert)
                    continue
            get_logger().debug('       Alert {0} with priority {1} will be processed'.format(str(alert),alert.priority))
            alerts_to_pri_by_pri[alert.priority].append(alert)
        get_logger().debug('alert_to_prioritize = {0}'.format(str(alerts_to_pri_by_pri)))
        if len(alerts_to_pri_by_pri) == 0:
            return 
        
        # For each priority compare with ones below it
        pri_list = alerts_to_pri_by_pri.keys()
        pri_list.sort()
        idx = 0
        while idx < len(pri_list)-1:
            in_idx = idx + 1
            while in_idx < len(pri_list):
                for h_alert in alerts_to_pri_by_pri[pri_list[idx]]:
                    remove_alerts = []
                    for l_alert in alerts_to_pri_by_pri[pri_list[in_idx]]:
                        get_logger().debug(' Comparing {0}({1}) with {2}({3})'.format(str(h_alert.brief_str()), str(h_alert.priority), str(l_alert.brief_str()), str(l_alert.priority)))
                        if l_alert.condition_events.issubset(h_alert.condition_events):
                            self.trace_info(self.trace_id[1],' Alert {0} with priority {1} subsumed by {2} with priority {3}'.format(str(l_alert.alert_id), str(l_alert.priority), str(h_alert.alert_id), str(h_alert.priority)))
                            alert_mgr.add_suppressions(h_alert, l_alert.supresses)
                            remove_alerts.append(l_alert)
                    for r_alert in remove_alerts:
                        alerts_to_pri_by_pri[pri_list[in_idx]].remove(r_alert)
                in_idx += 1
            idx += 1 
        
        for alert_list in alerts_to_pri_by_pri.values():
            for m_alert in alert_list:
                get_logger().debug('  creating {0}({1})'.format(str(m_alert), str(m_alert.priority)))
                alert_mgr.commit(m_alert)
                self.send_alert(m_alert)
        return    
    
    def _prioritize_and_send_alerts_NO_PRIORITY(self, alerts): 
        ''' Prioritize and send the alerts '''
        alert_mgr = get_service(SERVICE_ALERT_MGR)
        get_logger().debug('Alert priority processing turned off -- just create alerts')
        for m_alert in alerts:
            get_logger().debug('  creating {0}({1})'.format(str(m_alert), str(m_alert.priority)))
            alert_mgr.commit(m_alert)
            self.send_alert(m_alert)
        return    
            
    def will_analyze_alert(self, alert):
        '''Will it analyze the given alert? ''' 
        # No alert support at this time 
        return False
    
    def will_analyze_event(self, event):
        '''Will it analyze the given event?
        Use the fact that there was an event in the events section'''
        return (self[GRSE_EVENTS].check_for_analysis_info_event(event.get_src_comp(), event.get_event_id()))
    
    def will_analyze_event_validation(self, comp, event_id):
        ''' Validate that the specified comp, event_id will be analyzed 
            used to validate rules '''
        return self[GRSE_EVENTS].check_for_analysis_info_event(comp, event_id)
    
    def will_analyze_event_regx(self, event):
        '''Will it analyze the given event use the reg exp'''
        return self[GRSE_GEAR_CTL].event_id_regx.search(event.get_event_id()) is not None and \
                 self[GRSE_GEAR_CTL].event_comp_regx.search(event.get_src_comp()) is not None
    
    def will_analyze_event_validation_regx(self, comp, event_id):
        ''' validate when reg expressions are used '''
        return self[GRSE_GEAR_CTL].event_id_regx.search(event_id) is not None and \
                 self[GRSE_GEAR_CTL].event_comp_regx.search(comp) is not None
                 
    def analyze_event(self, event, pool):
        '''Analyze the event by firing the rules'''
        self.trace_debug(self.trace_id[1], 'Analyzing event: {0}'.format(event.brief_str()))
        self[GRSE_ANALYZE].analyze_event(event, pool, self[GRSE_GEAR_CTL])
        return
    
    def is_not_processing_addition(self):
        ''' Return true if the previous checkpoint didn't move anything forward 
            Cheat by checking if the current pool has any moved forward elements
        '''
        return len(self.event_pool.moved_forward) == 0
    
    def prime_event(self, event, pool):
        ''' Prime the event -- get the conditions setup with it, but don't take actions '''
        self.trace_debug(self.trace_id[1], 'Priming event: {0}'.format(event.brief_str()))
        # Priming is all about making sure that alerts aren't created by just primed events
        # however, suppressed events can never cause an alert to be created, so when a
        # primed event is suppressed, it doesn't need to be treated in a special way
        # This is beneficial because processing of primes is typically very expensive
        # when getting the truth space
        if event in pool.get_suppressed_incidents():
            self[GRSE_ANALYZE].analyze_event(event, pool, self[GRSE_GEAR_CTL])
        else:
            self[GRSE_ANALYZE].prime(event, pool, self[GRSE_GEAR_CTL])
        return
    
    def get_default_event_component(self):
        ''' Shorthand to get the default event component'''
        return self[GRSE_GEAR_CTL]['default_event_comp']
           
    def add_event(self, event):
        ''' add an event to those being processed ''' 
        a_info = self[GRSE_EVENTS].get_analysis_info_event(event)
        min_time = a_info[AI_MIN_TIME_IN_POOL]
        pool_ext = a_info[AI_POOL_EXT_TIME]
        try:
            self.event_pool.add_incident(event, pool_ext, min_time)
        except IncidentPoolClosedError:
            worked = False
            fail_count = 290  # Want to log after first 10 seconds of delay and then 5 min after that
            term_cnt_down = 12 # Terminate after this number of failures
            while not worked:
                try:
                    self.event_pool.add_incident(event, pool_ext, min_time)
                    worked = True
                except IncidentPoolClosedError:
                    sleep(1)
                    worked = False
    
                    if fail_count >= 300:
                        fail_count = 0
                        get_logger().info('Unable to add event to pool because pool is closed')
                        term_cnt_down -= 1 
                    else:
                        fail_count += 1
                        
                    if term_cnt_down <= 0:
                        get_logger().warning('Pool closure processing did not complete within allowed time')
                        self.event_pool.failed()
                        raise
                        
        # Now analyze the event
        self.analyze_event(event, self.event_pool)
        if self.pool_force_closure:
            self.pool_force_closure = False
            right_now = datetime.now()
            self.pool.close( right_now, right_now, POOL_CLOSE_REASON_RULE)
        self.event_pool.lock.release()
        return
    
    def flush(self, flush_time):
        ''' flush the ruleset '''
        try:
            self.event_pool.flush(flush_time)
        except IncidentPoolStateTransitionError:
            get_logger().info('Tried to Flush a closed pool')
        return
    
    def end_of_events(self):
        ''' handle the end of events ''' 
        right_now = datetime.now()
        reason = POOL_CLOSE_REASON_SHUTDOWN
        try:  
            self.event_pool.close(right_now, reason )
        except IncidentPoolStateTransitionError:
            # Pool may have been created with a timer or nothing moved forward to it
            pass     
        return

    def close_pool(self, pool):
        ''' close pool processing '''
        new_alerts = self[GRSE_ANALYZE].close_pool(pool, self[GRSE_GEAR_CTL])
        # reset the rules
        self[GRSE_ANALYZE].reset()
        return new_alerts
 
     
class GearAnalyzeRules(object):
    ''' The rules that do the analysis of the events '''
    
    def __init__(self, context):
        ''' Constructor '''
        trace_id = (0, 'Analyze')
        self.description = ''
        self.rules = []
        self.new_alerts = []
        self.trace_id = trace_id
        self.ruleset = context
        self.error_handlers = GearErrorHandlers(context)
        self.always_gets_event = []
        self.gets_event_by_key = defaultdict(set)
        return
    
    def __str__(self):
        outstr = ''
        for rule in self.rules:
            outstr += str(rule)
        return outstr
    
    def read_from_xml(self, xml_element, trace_dict):
        '''Add event info defined in an XML events element'''
        self.trace_id = trace_dict[xml_element]
        for rule_entry in xml_element:
            entry_name = rule_entry.tag.split('}')[-1]
            if entry_name == 'rule':
                self.rules.append(GearRule(rule_entry, trace_dict, self.ruleset))
            elif entry_name == 'on_error':
                self.error_handlers.read_from_xml_element(rule_entry, trace_dict)
            elif entry_name == 'description':
                self.description = rule_entry.text
            else:
                self.parse_error(self.trace_id[0], 'unexpected element {0}'.format(entry_name))
        return
    
    def resolve_and_validate(self):
        '''Resolve and validate the rules using the gear control info'''
        self.error_handlers.resolve_and_validate()
        if len(self.rules) == 0:
            self.ruleset.parse_error(self.trace_id[0], 'analyze element must contain at least one \'rule\' element')
        for rule in self.rules:
            rule.resolve_and_validate()
            event_checked_info = rule.get_checked_event_info()
            if event_checked_info is None:
                self.always_gets_event.append(rule)
            else:
                for ec in event_checked_info:
                    self.gets_event_by_key[ec].add(rule)

        if self.ruleset[GRSE_ANALYZE].error_handlers.check_locations() == True: 
            # Get the locations to check
            used_locs = set()
            for rule in self.rules:
                t_used_locs = rule.get_used_locations()
                if t_used_locs is not None:
                    used_locs.update(t_used_locs)
            self.chk_rpt_loc = False
            self.chk_ext_data = set()
            for used_loc in used_locs:
                gear_var_parts = _parse_gear_variable(used_loc.strip()).split('.')
                if gear_var_parts[1] == 'ext':
                    self.chk_ext_data.add(gear_var_parts[2])
                elif gear_var_parts[1] == 'rpt_loc':
                    self.chk_rpt_loc = True
                elif gear_var_parts[1] == 'src_loc':
                    pass  # assuming this one 
                else:
                    get_logger().debug('Unexpected value in location: {0}'.format(used_loc))
            if len(self.chk_ext_data) == 0:
                self.chk_ext_data = None
            
            self.prime = self.prime_CHECK_LOC
            self.analyze_event = self.analyze_event_CHECK_LOC
        else:
            self.prime = self.prime_NO_CHECK
            self.analyze_event = self.analyze_event_NO_CHECK
           
        #self.print_cross_ref()
        #print str(self.gets_event_by_key)
        return
    
    def _check_loc_ok(self, event):
        ''' Check the location '''
        if event.src_loc.is_unprocessable() == True:
            self.error_handlers.location_error(event, event.src_loc)
            return False
            
        if self.chk_rpt_loc == True \
         and event.rpt_loc is not None \
         and event.rpt_loc.is_unprocessable() == True:
            self.error_handlers.location_error(event, event.rpt_loc)
            return False
            
        if self.chk_ext_data is not None:
            for ext_var in self.chk_ext_data:
                if event.raw_data is not None \
                 and ext_var in event.raw_data \
                 and event.raw_data[ext_var] is not None \
                 and event.raw_data[ext_var].is_unprocessable() == True:
                    self.error_handlers.location_error(event, event.raw_data[ext_var])
                    return False
        return True
    
    def prime_CHECK_LOC(self, event, pool, gear_ctl):
        if self._check_loc_ok(event) == True:
            self.prime_NO_CHECK(event, pool, gear_ctl)
        return
    
    def analyze_event_CHECK_LOC(self, event, pool, gear_ctl):
        if self._check_loc_ok(event) == True:
            self.analyze_event_NO_CHECK(event, pool, gear_ctl)
        return
    
    def analyze_event_NO_CHECK(self, event, pool, gear_ctl):
        ''' Fire the events ''' 
        get_logger().debug('Accumulating event {0}'.format(str(event)))
#        for rule in self.rules:
#            rule.accumulate(event)
        for rule in self.always_gets_event:
            rule.accumulate(event)
        for rule in self.gets_event_by_key[(event.src_comp, event.event_id)]:
            rule.accumulate(event)
        return
    
    def prime_NO_CHECK(self, event, pool, gear_ctl):
        ''' Prime the condition with the event '''
        get_logger().debug('Priming rule group with event {0}'.format(str(event)))
#        for rule in self.rules:
#            rule.prime(event)
        for rule in self.always_gets_event:
            rule.prime(event)
        for rule in self.gets_event_by_key[(event.src_comp, event.event_id)]:
            rule.prime(event)
        return
    
    def get_new_alerts(self):
        ''' Get any new alerts created by the actions '''
        ret_alerts = list(self.new_alerts)
        self.new_alerts = []
        return ret_alerts
    
    def reset(self):
        ''' reset the rules '''
        get_logger().debug('Reset rule group')
        for rule in self.rules:
            rule.reset()
        return
    
    def get_cross_ref(self):
        ''' get cross reference information ''' 
        condition_cref = defaultdict(list)
        suppression_cref = defaultdict(list)
        alert_cref = defaultdict(list)
        for rule in self.rules:
            conditions, suppressions, alerts = rule.get_cross_ref()
            line_num = rule.trace_id[0]
            for condition in conditions:
                condition_cref[condition].append(line_num)
            for suppression in suppressions:
                suppression_cref[suppression].append(line_num)
            for alert in alerts:
                alert_cref[alert].append(line_num)
        return {'condition': condition_cref, 'suppression': suppression_cref, 'create alert': alert_cref}

    def print_cross_ref(self):
        ''' print the cross reference '''
        cref_dict = self.get_cross_ref()
        cref_keys = cref_dict.keys()
        cref_keys.sort()
        for cref_key in cref_keys:
            print '\nCross reference where id is referenced by {0} (list of rule start line numbers)'.format(cref_key)
            entry_keys = cref_dict[cref_key].keys()
            entry_keys.sort()
            for entry_key in entry_keys:
                print '   {0}: {1}'.format(str(entry_key), str(cref_dict[cref_key][entry_key]))
        return 

    def close_pool(self, pool, gear_ctl):
        ''' Close pool processing '''
        alerts = []
        for rule in self.rules:
            rule.execute_suppression_stage(pool, gear_ctl)
        for rule in self.rules:
            new_alerts = rule.execute_alert_stage(pool, gear_ctl)
            if new_alerts is not None and len(new_alerts) != 0:
                alerts.extend(new_alerts)
        #print 'returning alerts ' + str(alerts)
        return alerts


class RulesetEventCheckpoint(IncidentPoolEventCheckpoint):
    
    def __init__(self, name, ruleset, msg_target=None):
        IncidentPoolEventCheckpoint.__init__(self, name, msg_target)
        self.ruleset = ruleset
        return 
    
    def get_pool(self):
        return self.ruleset.event_pool
    
    def _start_pool(self):
        ''' start the pool and then prime the events '''
        IncidentPoolEventCheckpoint._start_pool(self)
        # Prime the pool with the events moved forward
        pool = self.get_pool()
        for event in pool.moved_forward:
            self.ruleset.prime_event(event, pool)
        return
    
    