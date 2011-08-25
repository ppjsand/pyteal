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

from ibm.teal.analyzer.gear.external_base_classes import ExtEvaluate, ExtExecute, ExtInitAlert,\
    ExtFatalError
from ibm.teal.alert import ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY,\
    ALERT_ATTR_RECOMMENDATION, ALERT_ATTR_REASON, ALERT_ATTR_RAW_DATA,\
    ALERT_ATTR_SRC_NAME, ALERT_ATTR_EVENT_LOC,\
    ALERT_ATTR_EVENT_LOC_TYPE
from ibm.teal.registry import get_service, SERVICE_ALERT_MGR


class ExecuteBad(ExtExecute):
    def __init(self, parm_dict):
        return
    
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        return
    
    def execute_finalize_suppression_stage(self, pool, rule):
        return
            
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate alert stage actions '''
        return 
    
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        raise ExtFatalError('Test Failure Init Alert')
        return []
    
    def reset(self):
        ''' Reset for use with a new pool '''
        pass


class InitAlertBad(ExtInitAlert):
    def update_init_data(self):
        raise ExtFatalError('Test Failure Init Alert')
