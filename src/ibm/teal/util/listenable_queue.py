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


from threading import Event
from Queue import Queue, Empty
from abc import ABCMeta, abstractmethod
from ibm.teal.registry import get_logger, SHUTDOWN_MODE_DEFERRED,\
    SERVICE_SHUTDOWN_MODE
from ibm.teal.control_msg import ControlMsg, CONTROL_MSG_TYPE_END_OF_DATA,\
    CONTROL_MSG_TYPE_UPDATE_CHECKPOINT
from ibm.teal import registry
from ibm.teal.util.teal_thread import TealThread

class QueueListener(object):
    '''The QueueListener class is the base class for modules that
    want to listen for events on a ListenableQueue
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod    
    def get_name(self):
        '''Get the name of the analyzer.'''
        return 
       
    def notify(self, item):
        '''Notify the listener with the new item in the queue.
        
        NOTE: Other methods can be used ... but should have the same parms
        
        returns boolean to indicate if listener will process'''
        return False
    
    def shutdown_immediate(self):
        ''' Shutdown immediately 
            Note: non-immediate shutdown is done by calling notify with an End of Data control message
        ''' 
        return


class ListenableQueue(Queue):
    '''This class is a Listenable queue.  QueueListeners can be registered
    and will be notified for each item added to the queue
    '''
    
    def __init__(self, name, no_process_callback=None):
        '''Constructor
        
           name -- name of the queue
           no_proces_callback -- called if none of the listeners process
        '''
        get_logger().debug('Creating Listenable Queue {0}'.format(name))
        self.name = name
        self.no_process_callback = no_process_callback
        self.listener_methods = []
        self.no_listeners_event = Event()
        self.no_listeners_event.set()
        Queue.__init__(self)
        self.watcher = ListenableQueueWatcher(self)
        self.watcher.setDaemon(True)
        self.watcher.start()
        return
        
    def register_listener(self, listener):
        '''Register a new listener'''
        if listener is None:
            get_logger().error('tried to register None')
            raise ValueError
        if listener.notify not in self.listener_methods:
            get_logger().debug('Adding listener {0} to {1}'.format(listener.get_name(), self.name))
            self.no_listeners_event.clear()
            self.listener_methods.append(listener.notify)
        return
            
    def register_listener_method(self, listener_method):
        '''Register a new listener'''
        if listener_method is None:
            get_logger().error('tried to register None')
            raise ValueError
        if listener_method not in self.listener_methods:
            get_logger().debug('Adding listener {0} to {1}'.format(listener_method.__self__.get_name(), self.name))
            self.no_listeners_event.clear()
            self.listener_methods.append(listener_method)   
        return         
            
    def unregister_listener(self, listener):
        ''' Unregister a listener'''
        if listener.notify in self.listener_methods:
            get_logger().debug('Removing listener {0} to {1}'.format(listener.get_name(), self.name))
            self.listener_methods.remove(listener.notify)
            if (not self.listener_methods):
                self.no_listeners_event.set()
        else:
            get_logger().fatal('Listener {0} not registered'.format(listener.get_name()))
        return
        
    def unregister_listener_method(self, listener_method):
        ''' Unregister a listener'''
        if listener_method in self.listener_methods:
            get_logger().debug('Removing listener {0} to {1}'.format(listener_method.__self__.get_name(), self.name))
            self.listener_methods.remove(listener_method)
            if (not self.listener_methods):
                self.no_listeners_event.set()
        else:
            get_logger().fatal('Listener {0} not registered'.format(listener_method.__self__.get_name()))
        return
        
    def notify_listeners(self, item):
        '''Notify all of the registered listeners
        '''
        get_logger().debug('Notifying listeners of {0}'.format(self.name))
        processed = False
        # Have to copy the list because call may cause an unregister
        for listener_method in self.listener_methods[:]:
            processed = listener_method(item) or processed
        if processed == False and self.no_process_callback is not None:
            self.no_process_callback(item)
        return
    
    def notify_listeners_SHUTDOWN(self, item):
        ''' Once shutdown no longer notify '''
        get_logger().info('{0} received the following item after shutdown: {1}'.format(self.name, str(item)))
        return
    
    def shutdown(self):
        ''' Shutdown the Listenable Queue
        The Queue must wait for its watcher to end and all the
        listeners to leave before it is totally shutdown
        '''
        get_logger().debug('{0}: Stopping ListenableQueue Watcher'.format(self.name))
        self.watcher.stop()
        
        if registry.get_service(SERVICE_SHUTDOWN_MODE) == SHUTDOWN_MODE_DEFERRED:   
            get_logger().debug('{0}: Joining ListenableQueue Watcher'.format(self.name))
            self.watcher.join()
            
            get_logger().debug('{0}: Waiting for all listeners to leave'.format(self.name))
            while(not self.no_listeners_event.is_set()):
                self.no_listeners_event.wait()
            
        self.notify_listeners = self.notify_listeners_SHUTDOWN
        get_logger().debug('{0}: Shutdown complete'.format(self.name))
        return
        
class ListenableQueueWatcher(TealThread):
    ''' Class to watch the queue and call back when an item is added'''
    
    def __init__(self, queue_to_watch):
        '''Constructor
        '''
        self.queue_to_watch = queue_to_watch
        self.running = True
        TealThread.__init__(self)
        return
    
    def run(self):
        '''Wait for something to come into queue and then call the queue to notify the listeners
        '''
        try:
            try:
                msg = None
                while self.running:
                    msg = self.queue_to_watch.get()
                    self.queue_to_watch.notify_listeners(msg)
                    if isinstance(msg, ControlMsg) and msg.msg_type == CONTROL_MSG_TYPE_UPDATE_CHECKPOINT and not self.queue_to_watch.empty():
                        get_logger().info('{0}: queue depth is {1}'.format(self.queue_to_watch.name, self.queue_to_watch.qsize()))
                
                # If deferred shutdown, continue processing messages until indication is received that
                # no more events will be coming
                if registry.get_service(SERVICE_SHUTDOWN_MODE) == SHUTDOWN_MODE_DEFERRED:
                    while(True):
                        if (isinstance(msg, ControlMsg) and 
                            msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
                            break
                        try:
                            msg = self.queue_to_watch.get(True,1)
                            self.queue_to_watch.notify_listeners(msg)                
                        except Empty:   # Race condition: running could go false before the EOD msg is put 
                            pass   
                # else:  Told to shutdown_immediately by the stop method
            except:
                get_logger().exception('Exception in run method')
            get_logger().debug('End of run method')
        except:
            pass
        return

    def stop(self):
        ''' Prepare to stop watching for events '''
        self.running = False
        
        if registry.get_service(SERVICE_SHUTDOWN_MODE) == SHUTDOWN_MODE_DEFERRED:
            # put EOD message on the end of the queue 
            self.queue_to_watch.put(ControlMsg(CONTROL_MSG_TYPE_END_OF_DATA))
        else: 
            # Tell listeners to shutdown immediately
            for listener_method in self.queue_to_watch.listener_methods[:]:
                listener_method.__self__.shutdown_immediate()
            # TODO: Workaround until Python 3.x
            self.kill_thread_using_exception()
        return
            
    
    
        