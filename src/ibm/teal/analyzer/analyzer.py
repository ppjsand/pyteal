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
from ibm.teal.control_msg import  ControlMsg, CONTROL_MSG_TYPE_END_OF_DATA
from ibm.teal.registry import get_logger
from ibm.teal.util.listenable_queue import QueueListener
import Queue
import threading
from ibm.teal.alert import TEAL_ALERT_ID_ANALYZER_FAILURE, create_teal_alert
import traceback
from ibm.teal.checkpoint_mgr import EventCheckpoint, CheckpointRecoveryComplete,\
    CHECKPOINT_STATUS_FAILED, CHECKPOINT_STATUS_SHUTDOWN,\
    CHECKPOINT_STATUS_RUNNING

ANALYZER_STATE_AS_STRING = ['running', 'failed', 'shutdown']
ANALYZER_STATE_RUNNING = 0
ANALYZER_STATE_FAILED = 1
ANALYZER_STATE_SHUTDOWN = 2

ANALYZER_CONF_ASYNCH = 'asynch'

class Analyzer(QueueListener):
    '''The Analyzer class is the base class for modules that
    analyze events and/or alerts to determine if an alert should be raised.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, name, outQueue, config_dict=None, number=0):
        '''The constructor.
        
           name -- name of the analyzer
           inQueue -- queue to listen to to get input from
           outQueue -- queue to send any alerts that are produced
           config_dict -- dictionary of configuration information (from config file)
                        asynch indicates if should run asynchronously ... default is True 
        '''
        self.set_state(ANALYZER_STATE_RUNNING)
        self.name = name
        self.number = number
        self.outQueue = outQueue
        self.process_event = self.process_event_NORMAL
        self.process_alert = self.process_alert_NORMAL
        self.base_analyze_event = self.base_analyze_event_NORMAL
        if config_dict is not None and ANALYZER_CONF_ASYNCH in config_dict and config_dict[ANALYZER_CONF_ASYNCH] == 'false':
            get_logger().debug('Analyzer {0} forced by configuration to run synchronously'.format(name))
            self.asynch = False
        else:
            self.asynch = True
        #self.notify_lock = threading.Lock()
        if self.asynch:
            self.queue = Queue.Queue()
            self.t1 = AnalyzerAsynch(self)
            self.t1.setDaemon(True)
            self.t1.start()
        return
    
    def set_state(self, new_state):
        ''' Set the analyzer state
            This allows subclasses to do special processing when the state is changed
        '''
        self.state = new_state
        return 
    
    def failure(self):
        ''' Processing of an item failed 
              Stop processing incoming incidents
        '''
        get_logger().error('Analyzer {0} failed'.format(self.name))
        self.set_state(ANALYZER_STATE_FAILED)
        self.t1.running = False
        self.process_event = self.process_event_FAILED
        self.process_alert = self.process_alert_FAILED
        self.base_process_control_msg = self.base_process_control_msg_FAILED
        self.create_analyzer_alert(TEAL_ALERT_ID_ANALYZER_FAILURE,'Analyzer {0} failed'.format(self.name), traceback.format_exc(),
                          severity='E')
        del self.queue
        return
            
    def process_event_NORMAL(self, event, context):
        '''Handle double dispatch from an event '''
        if self.will_analyze_event(event):
            if self.asynch:
                self.queue.put((self.base_analyze_event,event))
            else:
                try:
                    self.base_analyze_event(event)
                except:
                    self.failure()
            return True
        return False 
    
    def process_event_FAILED(self, event, context):
        ''' Failed so not processing anything '''
        return False
    
    def process_alert_NORMAL(self, alert, context):
        '''Handle double dispatch from an alert '''
        
        if self.will_analyze_alert(alert):
            if self.asynch:
                self.queue.put((self.base_analyze_alert,alert))
            else:
                try:
                    self.base_analyze_alert(alert)
                except:
                    self.failure()
            return True
        return False
    
    def process_alert_FAILED(self, alert, context):
        ''' Failed so not processing anything '''
        return False
    
    def base_process_control_msg(self, control_msg, context):
        '''Handle double dispatch from a control msg '''
        if self.asynch:
            self.queue.put((self.handle_control_msg,control_msg))
        else:
            self.handle_control_msg(control_msg)
        return True
    
    def base_process_control_msg_FAILED(self, control_msg, context):
        ''' Failed processing immediately -- to handle shutdown correctly '''
        self.handle_control_msg(control_msg)
        return True
    
    def shutdown(self):
        ''' Shutdown processing ... join the asynch thread if there is one'''
        if self.asynch:
            try:
                # TODO: Add timeout ?!
                self.t1.join()
                self.set_state(ANALYZER_STATE_SHUTDOWN)
            except:
                get_logger().debug('unable to join during shutdown in analyzer {0}'.format(self.name))
        return
 
    def send_alert(self, alert):
        ''' Send the alert to the output queue'''
        self.outQueue.put(alert)
        return
    
    def get_name(self):
        ''' Get the name of the analyzer.'''
        return self.name
    
    def create_analyzer_alert(self, alert_id, reason, raw_data=None, src_name=None, severity='I', urgency='N', 
                              loc_instance=None, recommendation='Contact next level of support'):
        ''' Create an alert for this analyzer in the alert log and add it to the alert analysis queue
        
            loc_instance will be added to the end of the TEAL location, if specified and if appropriate to 
            the location type used src_name will default to 'TEAL:listener:<name>'
        '''
        if src_name is None:
            src_name = 'TEAL:analyzer:{0}'.format(self.get_name())
        if loc_instance is None:
            loc_instance=self.name
        create_teal_alert(alert_id, reason, raw_data, src_name=src_name, severity=severity,
                          urgency=urgency, loc_instance=loc_instance, recommendation=recommendation)
        return

    @abstractmethod
    def will_analyze_event(self, event):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the event's id to the 
           list of event ids processed'''
        pass
    
    @abstractmethod
    def will_analyze_alert(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the alert's id to the 
           list of alert ids processed'''
        pass
           
    @abstractmethod
    def analyze_event(self, event):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.
        
        This is what will normally be overridden'''
        pass
    
    def base_analyze_event_NORMAL(self, event):
        ''' Allow parent to add stuff around a child analyze_event '''
        self.analyze_event(event)
        return 
    
    @abstractmethod
    def analyze_alert(self, alert):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        pass
    
    def base_analyze_alert(self, alert):
        ''' Allow parent to do things around child analyze_alert '''
        self.analyze_alert(alert)
        return
    
    @abstractmethod
    def handle_control_msg(self, control_msg):
        '''The analyzer method performs the correct operation '''
        pass
    

class AnalyzerAsynch(threading.Thread):
    '''This class is used to spawn a separate thread to run the analyzer in 
    '''
    
    def __init__(self, analyzer):
        '''Constructor
        '''
        self.analyzer = analyzer
        self.running = True
        threading.Thread.__init__(self)
        return
    
    def run(self):
        '''Wait on the input queue
        '''
        while self.running:
            func, item = self.analyzer.queue.get()
            try:
                func(item)
            except:
                get_logger().exception('Analyzer {0} failed'.format(self.name))
                self.analyzer.failure()
        
            if isinstance(item,ControlMsg) and (item.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
                break
        return
    
    
class EventAnalyzer(Analyzer):
    '''The Analyzer class is the base class for event analyzer classes
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, name, inEventQueue, outQueue, config_dict=None, number=0, checkpoint=None):
        '''The constructor.
        
           name -- name of the analyzer
           inEventQueue -- queue to listen to to get input from
           outQueue -- queue to send any alerts that are produced
           config_dict -- dictionary of configuration information (from config file)
           number -- identification number
           checkpoint -- checkpoint to use ... if None an EventAnalyzerCheckpoint will be used
                         to not use checkpointing, create and pass a EventAnalyzerCheckpointDisabled
                         instance
        '''
        Analyzer.__init__(self, name, outQueue, config_dict, number)
        self.inEventQueue = inEventQueue
        self.inEventQueue.register_listener_method(self.notifyEventQ)  # register
        if checkpoint is None:
            self.checkpoint = EventAnalyzerCheckpoint(name)
        else:
            self.checkpoint = checkpoint
        self.process_event = self.process_event_CHECKPOINT
        self.base_analyze_event = self.base_analyze_event_WITH_CHECKPOINT
        return
    
    def notifyEventQ(self, item):
        '''Handle incoming items'''
        get_logger().debug('Notify called with {0}'.format(str(item)))
        #self.notify_lock.acquire()
        result = item.process(self, None)
        #self.notify_lock.release()
        return result
  
    def set_state(self, new_state):
        ''' Change state
            If using checkpoint then need to update it
        '''
        self.state = new_state
        if self.state == ANALYZER_STATE_FAILED:
            self.checkpoint.set_status(CHECKPOINT_STATUS_FAILED)
        elif self.state == ANALYZER_STATE_SHUTDOWN:
            if self.checkpoint.get_status() == CHECKPOINT_STATUS_RUNNING:
                self.checkpoint.set_status(CHECKPOINT_STATUS_SHUTDOWN)
                # Move the checkpoint forward so it aligns with the monitor checkpoint
                self.checkpoint.set_checkpoint(None)
            else:
                get_logger().debug('Checkpoint status was not updated to shutdown because not running {0}'.format(str(self.checkpoint)))
        else:
            pass
        return 
        
    def process_event_CHECKPOINT(self, event, context):
        ''' Process event when checkpoint recovery is in process '''
        result = self.will_analyze_event(event)
        if result == True:
            try:
                result = self.checkpoint.need_to_analyze(event)
            except CheckpointRecoveryComplete:
                # If recovery is complete don't need to check with checkpoint anymore
                result = True
                self.process_event = self.process_event_NORMAL
                
            if result == True: 
                if self.asynch:
                    self.queue.put((self.base_analyze_event,event))
                else:
                    try:
                        self.base_analyze_event(event)
                    except:
                        self.failure
            return True
        return False 
      
    def process_alert(self, alert, context):
        '''Handle double dispatch from an alert 
        
        Event analyzers do not process alerts
        '''
        get_logger().error('Event analyzer was given an alert to process')
        return False
    
    def process_control_msg(self, control_msg, context):
        '''Handle double dispatch from a control msg '''
        self.base_process_control_msg(control_msg, context)
        # If there are no more events to process, shut down this
        # analyzer
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            self.shutdown()
            # We have received all events we are going to process so
            # we can unregister ourselves from queue    
            self.inEventQueue.unregister_listener_method(self.notifyEventQ)        
        return True
    
    def will_analyze_event_CHECKPOINT(self, event):
        ''' Check if will analyze an event when using the checkpoint '''
        try:
            return self.checkpoint.will_analyze_event(event)
        except CheckpointRecoveryComplete:
            # No longer need to call checkpoint 
            self.will_analyze_event = self.will_analyze_event_NORMAL
        
        
    def base_analyze_event_WITH_CHECKPOINT(self, event):
        ''' Add checkpointing after analyze event'''
        self.analyze_event(event)
        self.checkpoint.set_checkpoint(event.rec_id)
        return     
   
    def will_analyze_alert(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the alert's id to the 
           list of alert ids processed'''
        get_logger().error('Event Analyzer does not process alerts')
        return False
            
    def analyze_alert(self, alert):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        get_logger().error('Event Analyzer does not process alerts')
        return
     

class EventAnalyzerCheckpointInterface(object):
    ''' Interface for Event Analyzer Checkpoint 
        This was pulled out to enable creation of a class that does not
        actually create a checkpoint
    '''
    
    def need_to_analyze(self, event):
        ''' Determine if the specified rec_id needs to be analyzed or not '''
        pass
    
class EventAnalyzerCheckpoint(EventCheckpoint, EventAnalyzerCheckpointInterface):
    ''' Event Analyzer Checkpoint ... keeps track of last rec_id processed '''
    
    def __init__(self, name):
        EventCheckpoint.__init__(self, name)
        return
    
    def prepare_for_restart(self, restart_mode, restart_rec_id):        
        ''' If prepare for restart determines value is None, then don't need to analyze'''
        EventCheckpoint.prepare_for_restart(self, restart_mode, restart_rec_id)
        if self.start_rec_id is None:
            self.need_to_analyze = self.need_to_analyze_COMPLETE
        return
            
    def need_to_analyze_COMPLETE(self, event):
        ''' If before my checkpointed rec_id then don't need to process '''
        raise CheckpointRecoveryComplete(self.start_rec_id, '{0}'.format(self.name))
    
    def need_to_analyze(self, event):
        ''' If before my checkpointed rec_id then don't need to process '''
        if event.rec_id > self.start_rec_id:
            raise CheckpointRecoveryComplete(self.start_rec_id,'{0}'.format(self.name))
        return False
    
class EventAnalyzerCheckpointDisable(EventAnalyzerCheckpointInterface):
    ''' Used when Event Analyzer should not checkpoint '''
       
    def need_to_analyze(self, event):
        raise CheckpointRecoveryComplete(None, 'disabled')
    
    def set_checkpoint(self, rec_id, data=None):
        return 
    
    def set_status(self, status):
        return
    
    
class AlertAnalyzer(Analyzer):
    '''The Analyzer class is the base class for modules that
    analyze events and/or alerts to determine if an alert should be raised.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, name, inEventQueue, inAlertQueue, outQueue, config_dict=None, number=0):
        '''The constructor.
        
           name -- name of the analyzer
           inQueue -- queue to listen to to get input from
           outQueue -- queue to send any alerts that are produced
           config_dict -- dictionary of configuration information (from config file)
           asynch -- should the analyzer run asynchronously'''
        Analyzer.__init__(self, name, outQueue, config_dict, number)
        self.inEventQueue = inEventQueue
        self.inEventQueue.register_listener_method(self.notifyEventQ)  # register
        self.inAlertQueue = inAlertQueue
        self.inAlertQueue.register_listener_method(self.notifyAlertQ)  # register
        return
        
    def notifyEventQ(self, item):
        '''Handle incoming items'''
        get_logger().debug('NotifyEventQ called with {0}'.format(str(item)))
        #TODO: Locking
        result = item.process(self, 'eventq')
        return result
    
    def notifyAlertQ(self, item):
        '''Handle incoming items'''
        get_logger().debug('NotifyAlertQ called with {0}'.format(str(item)))
        #TODO: Locking
        result = item.process(self, 'alertq')
        return result
    
    def process_event(self, event, context):
        '''Handle double dispatch from an event '''
        will_analyze = self.will_analyze_event(event)
        if will_analyze == True:
            if self.asynch == True:
                self.queue.put((self.analyze_event,event))
            else:
                self.analyze_event(event)
        return True
    
    def process_alert(self, alert, context):
        '''Handle double dispatch from an alert '''
        will_analyze = self.will_analyze_alert(alert)
        if will_analyze == True:
            if self.asynch == True:
                self.queue.put((self.analyze_alert,alert))
            else:
                self.analyze_alert(alert)
        return True
    
    def process_control_msg(self, control_msg, context):
        '''Handle double dispatch from a control msg '''
        self.base_process_control_msg(control_msg, context)
        # If there are no more events to process, shut down this
        # analyzer
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            if context == 'eventq':
                self.inEventQueue.unregister_listener_method(self.notifyEventQ)        
            else: # alertq
                self.shutdown()
                self.inAlertQueue.unregister_listener_method(self.notifyAlertQ)        
        return True
    
    def shutdown(self):
        ''' Shutdown processing ... join the asynch thread if there is one'''
        if self.asynch:
            self.t1.join()
        return
 
    def send_alert(self, alert):
        '''Send the alert to the output queue'''
        self.outQueue.put(alert)
        return
    
    def get_name(self):
        '''Get the name of the analyzer.'''
        return self.name
    
    @abstractmethod
    def will_analyze_event(self, event):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the event's id to the 
           list of event ids processed'''
        pass
    
    @abstractmethod
    def will_analyze_alert(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the alert's id to the 
           list of alert ids processed'''
        pass
           
    @abstractmethod
    def analyze_event(self, event):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        pass
    
    @abstractmethod
    def analyze_alert(self, alert):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        pass
    
    @abstractmethod
    def handle_control_msg(self, control_msg):
        '''The analyzer method performs the correct operation '''
        pass
