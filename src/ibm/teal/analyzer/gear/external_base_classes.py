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
from ibm.teal.alert import ALERT_ATTR_RAW_DATA, raw_data2dict, dict2raw_data,\
    ALERT_ATTR_ALERT_ID, ALERT_ATTR_SUBST_DICT, ALERT_ATTR_CONDITION_EVENTS
from ibm.teal.registry import SERVICE_ALERT_METADATA, get_service
from ibm.teal.metadata import META_ALERT_FRU_LIST, META_ALERT_FRU_CLASS
from ibm.teal.teal_error import TealError


class ExtFatalError(TealError):
    ''' A fatal error occurred in the external class that should terminate the analyzer '''
    pass


class ExtEvaluate(object):
    '''This is an abstract base class for classes used to implement a class for use 
    on a GEAR evaluate element
    '''
    
    def __init__(self, parm_dict):
        ''' Initialize the evaluation class using the parms specified on the evaluate element ''' 
        return
     
    __metaclass__ = ABCMeta
    
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
        ''' Get the set of truth points (loc, truth events) that make the condition true '''
        pass
        
    @abstractmethod
    def reset(self):
        '''Reset the condition'''
        pass
    
    def get_cross_ref(self):
        ''' return even ids analyzed -- OPTIONAL '''
        return []
   
  
class ExtExecute(object):
    '''This is an abstract base class for classes used to implement a class for use 
    on a GEAR execute element
    '''
    
    __metaclass__ = ABCMeta
    
    def __init__(self, parm_dict):
        ''' Initialize the evaluation class using the parms specified on the evaluate element ''' 
        return
    
    @abstractmethod
    def execute_accumulate_suppression_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate suppression stage actions '''
        pass
    
    @abstractmethod
    def execute_finalize_suppression_stage(self, pool, rule):
        ''' Execute the finalize suppression stage actions '''
        pass
            
    @abstractmethod
    def execute_accumulate_alert_stage(self, truth_point, pool, rule):
        ''' Execute the accumulate alert stage actions '''
        pass
    
    @abstractmethod
    def execute_create_alert_stage(self, pool, rule):
        ''' Execute the create alert stage actions '''
        pass
    
    @abstractmethod
    def reset(self):
        ''' Reset for use with a new pool '''
        pass
    

class ExtInitAlert(object):
    '''This is an abstract base class for classes used to implement a class for use 
    on a GEAR create alert element for alert initialization data modification
    '''
    
    __metaclass__ = ABCMeta
        
    @abstractmethod
    def update_init_data(self):
        ''' This method is called by update_init_data_main which does setup to simplify the 
        coding of this method.  
       
        This method should modify how the alert should be created by modifying self.init_dict which
        will be filled in prior to it being called and will be returned after this method returns
        ''' 
        pass

    # The following helper methods depend on initialization done in update_init_data_main
    # If it is overridden then they shouldn not be used
    
    def get_fru_class(self):
        ''' Get the fru class from the metadata '''
        if self.metadata_cache is None:
            mds = get_service(SERVICE_ALERT_METADATA)
            if self.init_dict[ALERT_ATTR_ALERT_ID] not in mds:
                return None
            self.metadata_cache = mds[self.init_dict[ALERT_ATTR_ALERT_ID]]
        return self.metadata_cache[META_ALERT_FRU_CLASS]    
    
    def get_fru_list(self):
        ''' Get the fru list from the metadata '''
        if self.metadata_cache is None:
            mds = get_service(SERVICE_ALERT_METADATA)
            if self.init_dict[ALERT_ATTR_ALERT_ID] not in mds:
                return None
            self.metadata_cache = mds[self.init_dict[ALERT_ATTR_ALERT_ID]]
        return self.metadata_cache[META_ALERT_FRU_LIST]
    
    def get_events(self):
        ''' Get the condition events '''
        if ALERT_ATTR_CONDITION_EVENTS in self.init_dict:
            return list(self.init_dict[ALERT_ATTR_CONDITION_EVENTS])
        else:
            return list()
    
    def add_loc_substitutions(self, loc, prefix):
        ''' Add the keywords for the specified location to
        the substitution dictionary used with the msg_template
        to create the reason.
        
        prefix is added to each entry, since non-prefixed
        entries will be ignored because the values from the event_loc
        value will be used.
        '''
        sub_dict = loc.get_substitution_dict()
        n_dict = dict(map(lambda x, y: (prefix+x,y), sub_dict.keys(), sub_dict.values()))
        if ALERT_ATTR_SUBST_DICT not in self.init_dict:
            self.init_dict[ALERT_ATTR_SUBST_DICT] = n_dict
        else:
            self.init_dict[ALERT_ATTR_SUBST_DICT].update(n_dict)
        return
    
    # Method called by GEAR
    def update_init_data_main(self, init_dict):
        ''' This is the method that is called to process the alert init dictionary
        It puts the init dictionary into self.init dictionary and sets self.raw_data_dict
        and processes them to correctly return them before it returns
        
        While this method can be overridden, it is recommended to override update_init_data
        instead.
        '''
        self.metadata_cache = None
        self.init_dict = init_dict
        if ALERT_ATTR_RAW_DATA in init_dict:
            self.raw_data_dict = raw_data2dict(init_dict[ALERT_ATTR_RAW_DATA])
        else:
            self.raw_data_dict = {}
        self.update_init_data() 
        if len(self.raw_data_dict) != 0:
            self.init_dict[ALERT_ATTR_RAW_DATA] = dict2raw_data(self.raw_data_dict)
        return self.init_dict
    
