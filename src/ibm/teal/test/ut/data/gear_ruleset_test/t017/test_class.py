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

from ibm.teal.analyzer.gear.external_base_classes import ExtEvaluate, ExtExecute, ExtInitAlert
from ibm.teal.alert import ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY,\
    ALERT_ATTR_RECOMMENDATION, ALERT_ATTR_REASON, ALERT_ATTR_RAW_DATA,\
    ALERT_ATTR_SRC_NAME, ALERT_ATTR_EVENT_LOC,\
    ALERT_ATTR_EVENT_LOC_TYPE
from ibm.teal.registry import get_service, SERVICE_ALERT_MGR


class Evaluate017(ExtEvaluate):
    def __init__(self, parm_dict):
        ''' Initialize the evaluation class using the parms specified on the evaluate element ''' 
        # Make sure passe information is right
        expected = {'evaluate_name':'testev', 'Elvis':'is in the building', 'from_conf': 'information', 'name':'AnalyzerTest017', 'mode': 1}
        if len(expected) + 2 != len(parm_dict):
            print 'Length mismatch'
            raise ValueError
        for key, value in expected.items():
            if parm_dict[key] != value:
                print 'Key {0} did not have value {1}'.format(key, value)
                raise ValueError
        self.event_id = parm_dict['id']
        self.count = parm_dict['count']
        self.result_space = set()
        return
     
    def prime(self, event):
        ''' Prime the condition '''
        self.accumulate(event)
        return

    def accumulate(self, event):
        ''' Accumulate events '''
        if event.event_id == self.event_id:
            self.result_space.add((frozenset([event.src_loc]), frozenset([event])))
        return 
    
    def get_truth_space(self, exclude_events, exclude_primes=False):
        ''' Get the set of truth points (loc, truth events) that make the condition true '''
        return self.result_space
        
    def reset(self):
        '''Reset the condition'''
        self.result_space.clear()
        return

class Execute017(ExtExecute):
    def __init__(self, parm_dict):
        ''' Initialize the evaluation class using the parms specified on the evaluate element ''' 
        self.events = []
        self.raw_data = ''
        return
    
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate suppression stage actions '''
        for event in truth_point[1]:
            if event is not None:
                self.events.append(event)
        return
    
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Execute the finalize suppression stage actions '''
        self.raw_data += 'sup = ' + ','.join([e.brief_str() for e in self.events])
        return
            
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate alert stage actions '''
        for event in truth_point[1]:
            if event not in self.events:
                print 'Did not find event!'
                raise ValueError
            else:
                self.events.remove(event)
        return 
    
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        if len(self.events) != 0:
            print 'events left over'
            raise ValueError
        alert_dict = {ALERT_ATTR_SEVERITY:'I',
                      ALERT_ATTR_URGENCY:'N',
                      ALERT_ATTR_RECOMMENDATION:'sleep',
                      ALERT_ATTR_REASON:'tired',
                      ALERT_ATTR_RAW_DATA:self.raw_data,
                      ALERT_ATTR_SRC_NAME: 'TEST017',
                      ALERT_ATTR_EVENT_LOC: 'AA##BB##CC##test017',
                      ALERT_ATTR_EVENT_LOC_TYPE: 'A'
                      }
        amgr = get_service(SERVICE_ALERT_MGR)
        new_alert = amgr.allocate('NOTREAL1', alert_dict)
        return [new_alert]
    
    def reset(self):
        ''' Reset for use with a new pool '''
        pass


class InitAlert017(ExtInitAlert):
    def update_init_data(self):
        self.raw_data_dict['add_me'] = 'stuff added'
        self.raw_data_dict['events'] = ','.join([e.event_id for e in self.get_events()])
        return
