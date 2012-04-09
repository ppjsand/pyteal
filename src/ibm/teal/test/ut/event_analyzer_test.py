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

import unittest
import multiprocessing
import time
from datetime import datetime

from ibm import teal
from ibm.teal.alert import ALERT_ATTR_CREATION_TIME
from ibm.teal.analyzer.analysis_info import AnalysisInfo
from ibm.teal.analyzer.analyzer import EventAnalyzer
from ibm.teal.analyzer.gear.ruleset import GearRuleset
from ibm.teal.analyzer.pool.incident_pool import IncidentPool, POOL_MODE_OCCURRED, IncidentPoolClosedError
from ibm.teal.analyzer.pool.incident_pool import POOL_CLOSE_REASON_FLUSH, POOL_STATE_RUNNING
from ibm.teal.control_msg import CONTROL_MSG_TYPE_FLUSH
from ibm.teal.registry import get_logger
from ibm.teal.util.listenable_queue import ListenableQueue, QueueListener
from ibm.teal.event import EVENT_ATTR_REC_ID, EVENT_ATTR_TIME_OCCURRED,\
    EVENT_ATTR_EVENT_ID
from ibm.teal.test.teal_unittest import TealTestCase

class SampleQueueListenerT(QueueListener):
    def __init__(self, name):
        self.name = name
        self.notifications = []
        QueueListener.__init__(self)
        return
    
    def get_name(self):
        return self.name
    
    def notify(self, item):
        self.notifications.append(item)
        return True

class SampleAlert(teal.Alert):
    '''Sample alert to enable testing
    '''
    
    def __init__(self, rec_id, alert_id, ts):
        ''' ctor '''
        teal.Alert.__init__(self, rec_id, alert_id, {ALERT_ATTR_CREATION_TIME:ts})


class SimpleEventAnalyzerAllAlert(EventAnalyzer):
    '''Analyzer that simple creates an alert from every event it gets
    '''
    
    def __init__(self, name, inQueue, outQueue, config_dict=None, number=0):
        '''The constructor.'''
        self.count = 0  # start with 1
        get_logger().debug('Creating SimpleEventAnalyzerAllAlert')
        EventAnalyzer.__init__(self, name, inQueue, outQueue, config_dict=config_dict, number=number)
        return
        
    def will_analyze_event(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the event's id to the 
           list of event ids processed'''
        get_logger().debug('will_analyze_event called')
        return True
    
    def will_analyze_alert(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the alert's id to the 
           list of alert ids processed'''
        get_logger().debug('will_analyze_alert called')
        return True
        
    def analyze_event(self, event):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        get_logger().debug('analyze_event called' + str(event))  
        self.count += 1
        alert = SampleAlert(self.count, 'Alert 01', datetime.now())
        # Removed below to match current GEAR support
        # TODO: Put back?
        #alert.raw_data = event.get_event_id() + '(' + str(event.get_rec_id()) + ')'
        #alert.event_loc = Location('C', 'MB-PR2' )
        #if event.raw_data is not None:
        #    alert.raw_data += ' ' + event.raw_data
        self.send_alert(alert)
        return
    
    def analyze_alert(self, alert):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        get_logger().error('analyze_alert not supported')
        return
    
    def handle_control_msg(self, control_msg):
        get_logger().error('control msg not supported')
        return
    
    
class SimpleEventAnalyzerWithPool(EventAnalyzer):
    '''Analyzer that simple creates an alert from every event it gets
    '''
    
    def __init__(self, name, inQueues, outQueue, config_dict=None, number=0):
        '''The constructor.'''
        get_logger().debug('metadata = %s', config_dict['events_metadata'])
        # TODO: Should really parse by comma into list 
        #self.event_meta = EventsMetadata([config_dict['events_metadata']])
        # Dummy Analysis info
        self.ai1 = AnalysisInfo('location_test')
        self.ai1.add_event_info('Example0', 1, 2, 3)
        self.ai1.add_event_info('Example1', 3, 3, 5)
        self.ai1.add_event_info('Example2', 3, None, None)        
        self.ai1.add_event_info('Example3', 3, None, None) 
        self.ai1.add_event_info('Example4', 3, None, None) 
        self.ai1.add_event_info('Example5', 3, None, None) 
        # TODO: Handle alert metadata 
        if 'mode' in config_dict:
            self.mode = config_dict['mode']
        else:
            self.mode = POOL_MODE_OCCURRED
        if 'initial_pool_duration' in config_dict:
            self.duration = int(config_dict['initial_pool_duration'])
            get_logger().debug('Duration override %s', str(self.duration))
        else:
            self.duration = 20
        self.pool = IncidentPool.new_pool(self.mode, self.duration, None, self.close_callback)
        # TODO: creation of alerts
        self.count = 0  # start with 1
        get_logger().debug('Creating SimpleEventAnalyzerAllAlert')
        EventAnalyzer.__init__(self, name, inQueues, outQueue, config_dict=config_dict, number=number)
        return
        
    def close_callback(self, reason):
        '''Process pool being closed ''' 
        get_logger().debug('close_callback called')
        move_forward, make_alerts = self.pool.get_active_incidents()
        for event in make_alerts:
            self.count += 1
            alert = SampleAlert(self.count, 'Alert 02', datetime.now())
            alert.raw_data = 'From ' + str(event.rec_id) + ':' + event.event_id
            self.send_alert(alert)
        new_pool = IncidentPool.new_pool(self.duration, self.mode, self.close_callback)
        for event in move_forward:
            new_pool.add_incident(event)
        self.pool = new_pool
        return            
        
    def will_analyze_event(self, event):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the event's id to the 
           list of event ids processed'''
        if event.get_event_id() in self.ai1.event_info:
            get_logger().debug('will_analyze_event for %s called -- True', event.get_event_id())
            return True
        else:
            get_logger().debug('will_analyze_event for %s called -- False', event.get_event_id())
            return False
    
    def will_analyze_alert(self, alert):
        '''See if the item will be processed by this analyzer
        
           True is yes it will be
           
           For example this could compare the alert's id to the 
           list of alert ids processed'''
        get_logger().debug('will_analyze_alert called -- False')
        return False
        
    def analyze_event(self, event):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        get_logger().debug('analyze_event called' + str(event))  
        worked = False
        while worked == False:
            try:
                self.pool.add_incident(event)
                worked = True
            except IncidentPoolClosedError:
                time.sleep(2)
                worked = False
        # Now process the pool
        self.process_pool(event, self.pool)
        return
    
    def process_pool(self, event, pool):
        if event.get_event_id() == 'Example5':
            suppress_these = pool.get_incidents(event.get_type(), 'Example2')
            pool.suppresses(event, suppress_these)
        return
  
    def analyze_alert(self, alert):
        '''The analyze method performs the analysis and determines if alerts
        should be created for conditions that require administrator action.'''
        return
    
    def handle_control_msg(self, control_msg):
        ''' Handle control messages '''
        get_logger().debug('Recieved control message %s',str(control_msg))
        if control_msg.msg_type == CONTROL_MSG_TYPE_FLUSH and self.pool.state == POOL_STATE_RUNNING:
            right_now = datetime.now()
            self.pool.close(right_now, right_now, POOL_CLOSE_REASON_FLUSH )
            
class SimpleEventAnalyzerWithPoolGEAR1(SimpleEventAnalyzerWithPool):
    '''Expand to use GEAR'''
    
    def __init__(self, name, inQueues, outQueue, config_dict=None, number=0):
        ''' CTOR '''
        self.grs1 = GearRuleset('data/GEAR_rule_example_001.xml')
        SimpleEventAnalyzerWithPool.__init__(self, name, inQueues, outQueue, config_dict, number)
        return
    
    def process_pool(self, event, pool):
        self.grs1['analyze'].fire(event, pool)
        return


class AnalyzerBasicTest(TealTestCase):

    def setUp(self):
        '''Setup for logging, an event and an timer to use for testing
        '''
        self.teal = teal.Teal('data/event_analyzer_test/load_config_01.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        return
    
    def tearDown(self):
        ''' delete TEAL
        '''
        self.teal.shutdown()
        return
    
    def testAnalyzerBasicS(self):
        '''Test basic Analyzer creation using a Sample analyzer synch'''
        inQ1 = ListenableQueue('inQ1')
        outQ1 = ListenableQueue('outQ1')
        outQL1 = SampleQueueListenerT('outQL1')
        outQ1.register_listener(outQL1)
        config_dict = {}
        config_dict['asynch'] = False
        SimpleEventAnalyzerAllAlert('TestAnalyzer1', inQ1, outQ1, config_dict=config_dict, number=2)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, EVENT_ATTR_EVENT_ID:'E1', EVENT_ATTR_TIME_OCCURRED: right_now})
        inQ1.put_nowait(te1)
        time.sleep(2)
        self.assertEqual(len(outQL1.notifications), 1)
        alert = outQL1.notifications[0]
        self.assertEquals(alert.get_rec_id(), 1)
        self.assertEquals(alert.alert_id, 'Alert 01')
        return

    def testAnalyzerBasicA(self):
        '''Test basic Analyzer creation using a Sample analyzer asynch'''
        inQ1 = ListenableQueue('inQ1')
        outQ1 = ListenableQueue('outQ1')
        outQL1 = SampleQueueListenerT('outQL1')
        outQ1.register_listener(outQL1)
        SimpleEventAnalyzerAllAlert('TestAnalyzer1', inQ1, outQ1, number=3)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, EVENT_ATTR_EVENT_ID:'E1', EVENT_ATTR_TIME_OCCURRED: right_now})
        inQ1.put_nowait(te1)
        time.sleep(2)
        self.assertEqual(len(outQL1.notifications), 1)
        alert = outQL1.notifications[0]
        self.assertEquals(alert.get_rec_id(), 1)
        self.assertEquals(alert.alert_id, 'Alert 01')
        return


if __name__ == "__main__":
    unittest.main()