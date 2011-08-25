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

from ibm.teal.alert import ALERT_ATTR_MSG_TEMPLATE, ALERT_ATTR_SUBST_DICT,\
    ALERT_ATTR_CONDITION_EVENTS
from ibm.teal.analyzer.gear.external_base_classes import ExtInitAlert

class Class062InitAlert3(ExtInitAlert):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def update_init_data(self):
        ''' '''
        self.init_dict[ALERT_ATTR_MSG_TEMPLATE] += ' HERE $replaceMe HERE'
        self.init_dict[ALERT_ATTR_SUBST_DICT] = {'replaceMe':'*V*'}
        events = self.get_events()
        if events is not None and len(events) > 0 and 'neighbor' in events[0].raw_data:
            self.add_loc_substitutions(events[0].raw_data['neighbor'], 'neighbor_')
            self.init_dict[ALERT_ATTR_MSG_TEMPLATE] += ' NEIGHBOR $neighbor_motherboard $neighbor_port NEIGHBOR'
        return
    
class Class062InitAlertUS(ExtInitAlert):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def update_init_data(self):
        ''' '''
        #p rint list(self.init_dict[ALERT_ATTR_CONDITION_EVENTS])[0].raw_data
        self.init_dict[ALERT_ATTR_MSG_TEMPLATE] = ' US $replacableMe $thisOneToo US'
        self.init_dict[ALERT_ATTR_SUBST_DICT] = {'replacableMe':'*U*', 'thisOneToo':'Aardvark'}
        if 'neighbor' in list(self.init_dict[ALERT_ATTR_CONDITION_EVENTS])[0].raw_data:
            #p rint 'neighbor found'
            self.add_loc_substitutions(list(self.init_dict[ALERT_ATTR_CONDITION_EVENTS])[0].raw_data['neighbor'], 'neighbor_')
            self.init_dict[ALERT_ATTR_MSG_TEMPLATE] += ' NEIGHBOR $neighbor_motherboard $neighbor_port NEIGHBOR'
        return
