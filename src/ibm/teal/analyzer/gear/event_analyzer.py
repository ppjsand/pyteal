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

from ibm.teal.analyzer.analyzer import EventAnalyzer
from ibm.teal.control_msg import CONTROL_MSG_TYPE_FLUSH, CONTROL_MSG_TYPE_END_OF_DATA
from ibm.teal.registry import get_logger
from ibm.teal.analyzer.gear.engine_factory import engine_factory


class GearEventAnalyzer(EventAnalyzer):
    '''
    Gear Event Analyzer
    
    This implements an event analyzer using a GEAR rules engine
    '''

    def __init__(self, name, inQueue, outQueue, config_dict=None, number=0):
        '''The constructor.'''
        get_logger().debug('Creating GEAR event analyzer named {0}'.format(name))
        
        self.engine = engine_factory(name, config_dict, event_input=True, number=number, send_alert=self.send_alert)
        EventAnalyzer.__init__(self, name, inQueue, outQueue, config_dict, number, checkpoint=self.engine.checkpoint)
        self.base_analyze_event_CHECKPOINT = self.analyze_event   # Manages checkpoints via pool checkpointer
        return
    
    def will_analyze_event(self, event):
        '''See if the item will be processed by this analyzer'''
        result = self.engine.will_analyze_event(event)
        if not result:
            self.engine.trace_debug(str(self.number),'Will NOT analyze event: {0}'.format(event.brief_str()))
        return result
    
    def analyze_event(self, event):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        get_logger().debug('analyze_event called' + str(event))  
        self.engine.add_event(event)
        return
      
    def handle_control_msg(self, control_msg):
        ''' Handle control messages '''
        self.engine.trace_info(str(self.number),'Received control message {0}'.format(control_msg.brief_str()))
        if control_msg.msg_type == CONTROL_MSG_TYPE_FLUSH:
            self.engine.flush(control_msg.creation_time)
        elif control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA:
            self.engine.end_of_events()
        return
    
    def is_not_processing(self):
        ''' Return true if the analyzer is processing an event or events '''
        return EventAnalyzer.is_not_processing(self) and self.engine.is_not_processing_addition()
