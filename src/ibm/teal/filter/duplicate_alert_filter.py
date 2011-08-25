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

from ibm.teal.filter import alert_filter
from ibm.teal import registry

class DuplicateAlertFilter(alert_filter.AlertFilter):
    '''
    This filter will filter out any alert that is a duplicate of an already
    active alert. It uses the Alert Manager, which maintains the lifecycle of 
    the alerts to make the determination
    '''
    
    def __init__(self, name, config_dict=None):
        '''
        Constructor
        '''
        alert_filter.AlertFilter.__init__(self, name, config_dict)

    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on.
        '''
        am = registry.get_service(registry.SERVICE_ALERT_MGR)
        return am.is_duplicate(alert.get_rec_id())
        
    def resolve_and_validate(self, info_dict):
        ''' Resolve and validate any configuration information
        '''
        pass