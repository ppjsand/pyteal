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
from ibm.teal.util.listenable_queue import QueueListener
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.control_msg import CONTROL_MSG_TYPE_END_OF_DATA


class AlertDelivery(QueueListener):
    '''The Analyzer class is the base class for modules that
    analyze events to determine if an alert should be raised.
    '''
    
    def __init__(self, inQueue):
        '''The constructor.'''
        self.filters = []
        self.listeners = []
        self.filter_to_listeners = {}
        self.inQueue = inQueue
        #Register to get notified by queue
        self.inQueue.register_listener(self)
        return
    
    def get_name(self):
        return 'AlertDelivery'
    
    def notify(self, item):
        '''Handle incoming item by invoking a callback'''
        get_logger().debug('Notify called')
        item.process(self, None)
        return True
    
    def shutdown_immediate(self):
        ''' Shutdown immediately 
            Note: non-immediate shutdown is done by calling notify with an End of Data control message
        ''' 
        self.inQueue.unregister_listener(self)        
    
    def process_alert(self, alert, context):
        '''Callback when incoming item is an alert
           Check the filters and call the listeners as appropriate
        '''
        # Run each filter and if False, remove listener from candidate set
        l_set = set(self.listeners)
        get_logger().debug('Starting set of listeners is: {0}'.format(str(l_set)))
        idx = 0
        while len(l_set) > 0 and len(self.filters) > idx:
            f = self.filters[idx]
            idx += 1
            keep_from_listeners = True
            try:
                keep_from_listeners = f.keep_from_listeners(alert)
            except:
                get_logger().exception('Filter {0} failed processing alert {1}({2})'.format(f.get_name(), alert.alert_id, alert.rec_id))
            if keep_from_listeners == True:
                get_logger().debug('Filter {0} kept  alert {1}({2}) from listener.  Eliminating listeners: {3}'.format(f.get_name(), alert.alert_id, alert.rec_id, str(self.filter_to_listeners[f.get_name()])))
                l_set.difference_update(self.filter_to_listeners[f.get_name()])
            else:
                get_logger().debug('Filter {0} did not keep alert {1}({2}) from listener.'.format(f.get_name(), alert.alert_id, alert.rec_id))
                
        # Whatever listeners are left did not have the alert filtered so send to them
        get_logger().debug('Remaining listener set is: {0}'.format(str(l_set)))
        if len(l_set) != 0:
            names = []
            for l in l_set:
                try:
                    l.process_alert(alert)
                except:
                    get_logger().exception('Listener {0} failed processing alert {1}({2})'.format(l.get_name(), alert.alert_id, alert.rec_id))
                names.append(l.get_name())
            get_logger().debug('Listeners {0} were called for alert id {1}({2})'.format(','.join(names), alert.alert_id, alert.rec_id ))
        return

    def process_control_msg(self, msg, context):
        '''Callback when incoming items is control message'''
        if (msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            self.inQueue.unregister_listener(self)        
            # TODO: Need to pass shutdown on to filters and listeners
        return
    
    def add_filter(self, filter):
        '''Add filter and ignore duplicates '''
        if filter not in self.filters:
            self.filters.append(filter)
        return
            
    def add_listener(self, listener):
        '''Add listener and ignore duplicates'''
        if listener not in self.listeners:
            self.listeners.append(listener)
            
    def resolve_and_validate(self, analyzer_names):
        ''' All enabled listeners and filters are loaded now, so resolve references and 
        validate them. ''' 
        # Resolve references
        for f in self.filters:
            self.filter_to_listeners[f.get_name()] = set()
            f.resolve_and_validate({'analyzer_names': analyzer_names})
        for l in self.listeners:
            for f_name in l.filters:
                if f_name in self.filter_to_listeners:
                    self.filter_to_listeners[f_name].add(l)
                else:
                    raise ConfigurationError('Listener {0} references filter {1} which is either disabled or not specified'.format(l.get_name(), f_name))
        # Validate that all filters are used
        for f in self.filters:
            if len(self.filter_to_listeners[f.get_name()]) == 0:
                get_logger().warning('Filter {0} is not configured to be used by any enabled listener'.format(f.get_name()))
                del self.filter_to_listeners[f.get_name()]
                self.filters.remove(f)
                     
        return