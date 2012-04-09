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

from abc import ABCMeta, abstractmethod
from ibm.teal.control_msg import  ControlMsg, CONTROL_MSG_TYPE_END_OF_DATA
from ibm.teal.registry import get_logger
from ibm.teal.util.listenable_queue import QueueListener
import Queue
import threading
from ibm.teal.alert import TEAL_ALERT_ID_ANALYZER_FAILURE, create_teal_alert
import traceback
from ibm.teal.checkpoint_mgr import EventCheckpoint, CheckpointRecoveryComplete,\
    CHECKPOINT_STATUS_FAILED, CHECKPOINT_STATUS_RUNNING,\
    CHECKPOINT_STATUS_INTERRUPTED
from ibm.teal.util.teal_thread import TealThread, ThreadKilled

ANALYZER_STATE_AS_STRING = ['running', 'failed', 'shutdown', 'shutdown_immediate']
ANALYZER_STATE_RUNNING = 0
ANALYZER_STATE_FAILED = 1
ANALYZER_STATE_SHUTDOWN = 2
ANALYZER_STATE_SHUTDOWN_IMMEDIATE = 3

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
        self.process_control_msg = self.process_control_msg_NORMAL
        
        self.base_will_analyze_event = self.will_analyze_event
        self.base_analyze_event = self.analyze_event
        self.base_will_analyze_alert = self.will_analyze_alert
        self.base_analyze_alert = self.analyze_alert
        self.base_handle_control_msg = self.handle_control_msg
        
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
    
    # Methods required to define an analyzer
    @abstractmethod
    def will_analyze_event(self, event):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the event's id to the 
           list of event ids processed'''
        pass
    
    @abstractmethod
    def analyze_event(self, event):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.
        
        This is what will normally be overridden'''
        pass
    
    @abstractmethod
    def will_analyze_alert(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the alert's id to the 
           list of alert ids processed'''
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
    
    # Group: process_event 
    ## uses:  will_analyze_event and analyze_event 
    def process_event_NORMAL(self, event, context):
        '''Handle double dispatch from an event '''
        analyzed = self.base_will_analyze_event(event)
        if analyzed == True:
            if self.asynch:
                self.queue.put((self.base_analyze_event, event))
            else:
                try:
                    self.base_analyze_event(event)
                except ThreadKilled:
                    raise 
                except:
                    self.failure()
        return analyzed 
    
    def process_event_FAILED(self, event, context):
        ''' Failed so not processing anything '''
        return False
    
    def process_event_SHUTDOWN(self, event, context):
        ''' Shutdown so not processing anything '''
        try: 
            get_logger().debug('Analyzer {0} received Event {0} after shutdown'.format(self.name, event.brief_str()))
        except ThreadKilled:
            raise
        except:
            pass
        return False
    
    # Group: process_alert
    ## uses: will_analyze_alert and analyze_alert 
    def process_alert_NORMAL(self, alert, context):
        '''Handle double dispatch from an alert '''
        analyzed = self.base_will_analyze_alert(alert)
        if analyzed == True:
            if self.asynch:
                self.queue.put((self.base_analyze_alert, alert))
            else:
                try:
                    self.base_analyze_alert(alert)
                except ThreadKilled:
                    raise 
                except:
                    self.failure()
        return analyzed
    
    def process_alert_FAILED(self, alert, context):
        ''' Failed so not processing anything '''
        return False
    
    def process_alert_SHUTDOWN(self, alert, context):
        ''' Shutdown so not processing anything '''
        try: 
            get_logger().debug('Analyzer {0} received Alert {0} after shutdown'.format(self.name, alert.brief_str()))
        except ThreadKilled:
            raise
        except:
            pass

        return False
    
    # Group: process_control_msg
    ## uses: handle_control_msg 
    def process_control_msg_NORMAL(self, control_msg, context):
        ''' Process control messages  '''
        if self.asynch:
            self.queue.put((self.base_handle_control_msg, control_msg))
        else:
            self.base_handle_control_msg(control_msg)
            
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            self.shutdown()
        return True
    
    def process_control_msg_FAILED(self, control_msg, context):
        ''' Failed no longer processing '''
        try: 
            get_logger().debug('Analyzer {0} received Control Message {0} after failure'.format(self.name, control_msg.brief_str()))
        except ThreadKilled:
            raise
        except:
            pass
        return False 
    
    def process_control_msg_SHUTDOWN(self, control_msg, context):
        ''' Shutdown no longer processing  '''
        try: 
            get_logger().debug('Analyzer {0} received Control Message {0} after shutdown'.format(self.name, control_msg.brief_str()))
        except ThreadKilled:
            raise
        except:
            pass
        return False 
    
    # State control 
    def failure(self):
        ''' Processing of an item failed 
              Stop processing incoming incidents
        '''
        get_logger().error('Analyzer {0} failed'.format(self.name))
        self.set_state(ANALYZER_STATE_FAILED)
        if self.asynch:
            self.t1.running = False
        self.process_event = self.process_event_FAILED
        self.process_alert = self.process_alert_FAILED
        self.process_control_msg = self.process_control_msg_FAILED
        self.create_analyzer_alert(TEAL_ALERT_ID_ANALYZER_FAILURE,'Analyzer {0} failed'.format(self.name), traceback.format_exc(),
                          severity='E')
        if self.asynch: 
            del self.queue
        return
    
    def shutdown(self):
        ''' Shutdown processing ... join the asynch thread if there is one'''
        if self.asynch:
            try:
                self.t1.join()
                self.set_state(ANALYZER_STATE_SHUTDOWN)
            except:
                get_logger().debug('unable to join during shutdown in analyzer {0}'.format(self.name))
                
        self.process_event = self.process_event_SHUTDOWN
        self.process_alert = self.process_alert_SHUTDOWN
        self.process_control_msg = self.process_control_msg_SHUTDOWN
        return
    
    def shutdown_immediate(self):
        ''' Shutdown processing as fast as possible ''' 
        if self.asynch:
            self.t1.running = False
            # Workaround until Python 3.x
            self.t1.kill_thread_using_exception()
        self.set_state(ANALYZER_STATE_SHUTDOWN_IMMEDIATE)
        self.process_event = self.process_event_SHUTDOWN
        self.process_alert = self.process_alert_SHUTDOWN
        self.process_control_msg = self.process_control_msg_SHUTDOWN
        return
    
    # Access
    def get_name(self):
        ''' Get the name of the analyzer.'''
        return self.name
    
    def set_state(self, new_state):
        ''' Set the analyzer state
            This allows subclasses to do special processing when the state is changed
        '''
        self.state = new_state
        return 
    
    # Helpers 
    def send_alert(self, alert):
        ''' Send the alert to the output queue'''
        self.outQueue.put(alert)
        return
            
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


class AnalyzerAsynch(TealThread):
    '''This class is used to spawn a separate thread to run the analyzer in 
    '''
    
    def __init__(self, analyzer):
        '''Constructor
        '''
        self.analyzer = analyzer
        self.running = True
        TealThread.__init__(self)
        return
    
    def run(self):
        '''Wait on the input queue
        '''
        try:
            while self.running:
                func, item = self.analyzer.queue.get()
                try:
                    func(item)
                except ThreadKilled:
                    raise
                except:
                    get_logger().exception('Analyzer {0} failed'.format(self.name))
                    self.analyzer.failure()
            
                if isinstance(item,ControlMsg) and (item.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
                    break
        except ThreadKilled:
            return 
        except:
            get_logger().exception('run exception')
        get_logger().debug('Run method ended')
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
        self.inEventQueue.register_listener_method(self.notifyFromEventQ)  # register
        if checkpoint is None:
            self.checkpoint = EventAnalyzerCheckpoint(name)
        else:
            self.checkpoint = checkpoint
        
        self.last_before_analyze = None
        self.process_event = self.process_event_RECOVERY
        self.base_analyze_event = self.base_analyze_event_RECOVERY
        return
    
    # QueueListener method to register which uses the processable aspect of the events, alerts, and control msgs
    def notifyFromEventQ(self, item):
        '''Handle incoming items'''
        get_logger().debug('Notify called with {0}'.format(str(item)))
        #self.notify_lock.acquire()
        result = item.process(self, None)
        #self.notify_lock.release()
        return result
    
    # Methods required to define an analyzer
    ## Still need will_analyze_event, analyze_event and handle_control_msg (from Analyzer)
    ##
    ## Event analyzers don't analyze alerts, so implement the required alert methods appropriately
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
    
    # Used to allow subclasses to add function before or after methods that define analysis     
    def base_analyze_event_RECOVERY(self, event):   
        ''' Add record of last before analyzed ''' 
        self.last_before_analyze = event 
        self.analyze_event(event)
        return
    
    def base_analyze_event_CHECKPOINT(self, event):
        ''' Add checkpointing after analyze event'''
        self.last_before_analyze = event 
        self.analyze_event(event)
        self.checkpoint.set_checkpoint(event.rec_id)
        return     
    
    # Group: process_event
    ## Have to be able to return true for will_analyze even when checkpoint says we don't
    def process_event_RECOVERY(self, event, context):
        ''' process event when recovering with a checkpoint ''' 
        will_result = self.base_will_analyze_event(event)
        try: 
            need_result = self.checkpoint.need_to_analyze(event)
        except CheckpointRecoveryComplete: 
            need_result = will_result
            self.process_event = self.process_event_NORMAL
            self.base_analyze_event = self.base_analyze_event_CHECKPOINT
            self.checkpoint.set_status(CHECKPOINT_STATUS_RUNNING)
            
        if need_result == True: 
            if self.asynch:
                self.queue.put((self.base_analyze_event, event))
            else:
                try:
                    self.base_analyze_event(event)
                except ThreadKilled:
                    raise 
                except:
                    self.failure()
        self.last_event_processed = event
        return will_result
    
    # State control 
    def shutdown(self): 
        ''' Shutdown ... add unregistering from Event Queue '''
        Analyzer.shutdown(self)
        self.inEventQueue.unregister_listener_method(self.notifyFromEventQ)
        
    def shutdown_immediate(self): 
        ''' Shutdown immediate... add unregistering from Event Queue '''
        Analyzer.shutdown_immediate(self)
        self.inEventQueue.unregister_listener_method(self.notifyFromEventQ)
        
    def failure(self):
        ''' Failusre ... add unregistering from Event Queue '''
        Analyzer.failure(self)
        self.inEventQueue.unregister_listener_method(self.notifyFromEventQ)
  
    # Helpers 
    ## Add update of checkpoint when state changes 
    def set_state(self, new_state):
        ''' Change state
            If using checkpoint then need to update it
        '''
        self.state = new_state
        if self.state == ANALYZER_STATE_FAILED:
            self.checkpoint.set_status(CHECKPOINT_STATUS_FAILED)
        elif self.state == ANALYZER_STATE_SHUTDOWN:
            if self.checkpoint.get_status() == CHECKPOINT_STATUS_RUNNING:
                self.checkpoint.shutdown()
            else:
                get_logger().debug('Checkpoint status was not updated to shutdown because not running {0}'.format(str(self.checkpoint)))
        elif self.state == ANALYZER_STATE_SHUTDOWN_IMMEDIATE:
            if self.checkpoint.get_status() == CHECKPOINT_STATUS_RUNNING:
                if self.is_not_processing() == True:
                    self.checkpoint.shutdown_immediate()
                else:
                    self.checkpoint.set_status(CHECKPOINT_STATUS_INTERRUPTED)
            else:
                get_logger().debug('Checkpoint status was not updated to shutdown (immediate) because not running {0}'.format(str(self.checkpoint)))
        #else:
        #    pass
        return 
    
    def is_not_processing(self):
        ''' Return true if the analyzer is processing an event or events '''
        if self.asynch == True and not self.queue.empty():
            return False 
        if self.last_before_analyze is None or self.checkpoint.is_checkpoint_rec_id(self.last_before_analyze.rec_id):
            return True
        return False 

class EventAnalyzerCheckpointInterface(object):
    ''' Interface for Event Analyzer Checkpoint 
        This was pulled out to enablee creation of a class that does not
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
    
    def prepare_for_restart(self, restart_mode, restart_rec_id, max_start):        
        ''' If prepare for restart determines value is None, then don't need to analyze'''
        EventCheckpoint.prepare_for_restart(self, restart_mode, restart_rec_id, max_start)
        if self.start_rec_id is None or restart_rec_id >= self.get_checkpoint()[0]:
            self.need_to_analyze = self.need_to_analyze_COMPLETE
        return
            
    def need_to_analyze_COMPLETE(self, event):
        ''' If at or after checkpointed rec_id then don't need to process '''
        raise CheckpointRecoveryComplete(self.start_rec_id, '{0}'.format(self.name))
    
    def need_to_analyze(self, event):
        ''' If before my checkpointed rec_id then need to process '''
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
    
    def is_checkpoint_rec_id(self, value):
        ''' check if the starting value is equal to the specified value '''
        return True 
    

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
        self.inEventQueue.register_listener_method(self.notifyFromEventQ)   
        self.inAlertQueue = inAlertQueue
        self.inAlertQueue.register_listener_method(self.notifyFromAlertQ)   
        return
    
    # QueueListener methods to register which uses the processable aspect of the events, alerts, and control msgs
    def notifyFromEventQ(self, item):
        '''Handle incoming items'''
        get_logger().debug('notifyFromEventQ called with {0}'.format(str(item)))
        result = item.process(self, 'eventq')
        return result
    
    def notifyFromAlertQ(self, item):
        '''Handle incoming items'''
        get_logger().debug('notifyFromAlertQ called with {0}'.format(str(item)))
        result = item.process(self, 'alertq')
        return result
        
    # Change to use context to know which queue is shutting down
    def process_control_msg_NORMAL(self, control_msg, context):
        '''Handle double dispatch from a control msg '''
        if self.asynch:
            self.queue.put((self.base_handle_control_msg, control_msg))
        else:
            self.base_handle_control_msg(control_msg)
        # If there are no more events to process, shut down this
        # analyzer
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            if context == 'eventq':
                self.inEventQueue.unregister_listener_method(self.notifyFromEventQ)        
            else: # alertq
                self.shutdown()
                self.inAlertQueue.unregister_listener_method(self.notifyFromAlertQ)        
        return True
    
