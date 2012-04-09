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
from ibm.teal.analyzer.gear.common import GearTrace
from abc import ABCMeta, abstractmethod
from ibm.teal.util.teal_thread import ThreadKilled

class GearEngine(GearTrace):
    ''' Base class for GEAR engines '''
    
    __metaclass__ = ABCMeta
        
    def __init__(self, name, number, trace=None, checkpoint=None):
        ''' Initialize the context '''
        GearTrace.__init__(self, name, number, trace)
        self.event_pool = None
        self.alert_pool = None
        self.pool_force_closure = False
        self.checkpoint = checkpoint
        return
    
    def validate_event_id(self, comp, event_id, trace_id):
        ''' Validate that the event id is one that is possible to get
        
            twists:
               Need component to validate 
               Maybe GEAR variables which cannot be validated
               
            Throws an exception if not valid
        '''
        # Check if component can be resolved
        if not comp.is_set() or not event_id.is_set():
            # This should not happen
            get_logger().error('Cannot validate comp {0} event id {1}'.format(str(comp.in_str), str(event_id.in_str)))
            raise ValueError
        try:
            comp_val = comp.get_value()
            event_id_val = event_id.get_value()
        except ThreadKilled:
            raise
        except:
            get_logger().debug('Unable to validate comp {0} event id {1}'.format(str(comp.in_str)), str(event_id.in_str))
        if not self.will_analyze_event_validation(comp_val, event_id_val):
            self.parse_error(trace_id[0], 'Component {0} event id {1} ({2}) is not one that will be evaluated.'.format(comp_val, event_id_val, event_id.in_str))
        return
    
    def validate_event_ids(self, comp, event_ids, trace_id):
        ''' Validate that the event id entries in the set of event ids is possible to get 
        
            Throws an exception is not valid
        '''
        # Check if component can be resolved
        if not comp.is_set() or not event_ids.is_set():
            # This should not happen
            get_logger().error('Cannot validate comp {0} event ids {1}'.format(str(comp.in_str), str(event_ids.in_str)))
            raise ValueError
        try:
            comp_val = comp.get_value()
            # TODO: This makes it so that a list containing a dynamic element won't be validated
            #       which means the static elements are not going to be validated!
            event_id_list = event_ids.get_list()
        except ThreadKilled:
            raise
        except:
            get_logger().debug('Unable to validate comp {0} event id {1}'.format(str(comp.in_str), str(event_ids.in_str)))
        else:
            for event_id_val in event_id_list:
                if not self.will_analyze_event_validation(comp_val, event_id_val):
                    self.parse_error(trace_id[0], 'Component {0} event id {1} in list {2} is not one that will be evaluated.'.format(comp_val, event_id_val, event_ids.in_str))
        return
    
    @abstractmethod  
    def will_analyze_event_validation(self, comp, event_id):
        ''' Validate that the specified comp, event_id will be analyzed 
            used to validate rules '''
        pass
    