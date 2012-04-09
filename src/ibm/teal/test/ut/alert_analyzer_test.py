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

from ibm.teal import Teal
from ibm.teal.registry import get_service, \
    SERVICE_ALERT_DELIVERY, SERVICE_ALERT_MGR, get_logger, SERVICE_EVENT_Q,\
    SERVICE_ALERT_ANALYZER_Q
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.util.journal import Journal
import unittest
from ibm.teal.analyzer.analyzer import AlertAnalyzer

class AlertAnalyzerSubclass(AlertAnalyzer):
    ''' Alert listener that creates alerts '''
    
    def __init__(self, name, inEventQueue, inAlertQueue, outQueue, config_dict=None, number=0):
        ''' save some stuff for testing '''
        AlertAnalyzer.__init__(self, name, inEventQueue, inAlertQueue, outQueue, config_dict, number)
        self.alerts = []
        self.events = []
        self.control_msgs  = []
    
    def will_analyze_event(self, event):
        ''' '''
        self.events.append(event)
        return True
    
    def will_analyze_alert(self, alert):
        ''' '''
        self.alerts.append(alert)
        return True
           
    def analyze_event(self, event):
        ''' '''
        if event not in self.events:
            get_logger().error('Event mismatch')
            raise ValueError
        self.create_analyzer_alert('AATST001', 'test of alert analyzer - event {0}'.format(event.event_id))
    
    def analyze_alert(self, alert):
        ''' '''
        if alert not in self.alerts:
            get_logger().error('Event mismatch')
            raise ValueError
        self.create_analyzer_alert('AATST002', 'test of alert analyzer - alert {0}'.format(alert.alert_id))
    
    def handle_control_msg(self, control_msg):
        '''The analyzer method performs the correct operation '''
        self.control_msgs.append(control_msg)
        self.create_analyzer_alert('AATST003', 'test of alert analyzer - control msg {0}'.format(control_msg.msg_type))

class AlertAnalyzerSubclassTest(TealTestCase):
    '''Test the alert analyzer can be subclassed '''

    def setUp(self):
        '''Setup Teal'''
        self.keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'No')
        self.teal = Teal('data/alert_analyzer_test/test01.conf', "stderr", msgLevel='warning', commit_alerts=False, commit_checkpoints=False)
    
    def tearDown(self):
        '''Teardown teal'''
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', self.keep_ADC)

    def testAlertAnalyzerSubclassing01(self):
        ''' Test that the alert analyzer subclass works properly '''
        # Get the alert listener
        for listener in get_service(SERVICE_ALERT_DELIVERY).listeners:
            if listener.get_name() == 'AllAlerts':
                j_out_all = listener.journal
                
        # Pump in some events
        j_in_event = Journal('j_in_events', 'data/alert_analyzer_test/inject_events01.json')
        j_in_event.inject_queue(get_service(SERVICE_EVENT_Q))
        
        # Check that the analyzer got them -- only len because can't compare locations
        self.assertTrue(j_out_all.wait_for_entries(27))

        # Pump in some alerts
        j_in_alert = Journal('j_in_events', 'data/alert_analyzer_test/inject_alerts01.json')
        j_in_alert.inject_queue(get_service(SERVICE_ALERT_ANALYZER_Q))
        
        # Check that the analyzer got them -- only len because can't compare locations
        self.assertTrue(j_out_all.wait_for_entries(34))

        alertmgr = get_service(SERVICE_ALERT_MGR)
        self.assertEqual(len(alertmgr.in_mem_alerts_duplicate), 0)

class AlertAnalyzerSubclassTest2(TealTestCase):
    '''Test the alert analyzer can be subclassed '''

    def setUp(self):
        '''Setup Teal'''
        self.keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'Yes')   # Set to No in configuration file will be ignored
        self.teal = Teal('data/alert_analyzer_test/test02.conf', "stderr", msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
    
    def tearDown(self):
        '''Teardown teal'''
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', self.keep_ADC)

    def testAlertAnalyzerSubclassing01_2(self):
        ''' Test that the alert analyzer subclass works properly and that environment section in configuration works correctly  '''
        # Get the alert listener
        for listener in get_service(SERVICE_ALERT_DELIVERY).listeners:
            if listener.get_name() == 'AllAlerts':
                j_out_all = listener.journal
                
        # Pump in some events
        j_in_event = Journal('j_in_events', 'data/alert_analyzer_test/inject_events01.json')
        j_in_event.inject_queue(get_service(SERVICE_EVENT_Q))
        
        # Check that the analyzer got them -- only len because can't compare locations
        self.assertTrue(j_out_all.wait_for_entries(27))

        # Pump in some alerts
        j_in_alert = Journal('j_in_events', 'data/alert_analyzer_test/inject_alerts01.json')
        j_in_alert.inject_queue(get_service(SERVICE_ALERT_ANALYZER_Q))
        
        # Check that the analyzer got them -- only len because can't compare locations
        self.assertTrue(j_out_all.wait_for_entries(34))
        
        alertmgr = get_service(SERVICE_ALERT_MGR)
        self.assertEqual(len(alertmgr.in_mem_alerts_duplicate), 34)

class AlertAnalyzerSubclassTest3(TealTestCase):
    '''Test the alert analyzer can be subclassed '''

    def setUp(self):
        '''Setup Teal'''
        self.keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'Yes') 
        self.remove_env('TEAL_ALERT_DUPLICATE_CHECK')   # Get rid of environment variable so configuration will be used
        self.teal = Teal('data/alert_analyzer_test/test02.conf', "stderr", msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
    
    def tearDown(self):
        '''Teardown teal'''
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', self.keep_ADC)

    def testAlertAnalyzerSubclassing01_3(self):
        ''' Test that the alert analyzer subclass works properly and that environment section in configuration works correctly  '''
        # Get the alert listener
        for listener in get_service(SERVICE_ALERT_DELIVERY).listeners:
            if listener.get_name() == 'AllAlerts':
                j_out_all = listener.journal
                
        # Pump in some events
        j_in_event = Journal('j_in_events', 'data/alert_analyzer_test/inject_events01.json')
        j_in_event.inject_queue(get_service(SERVICE_EVENT_Q))
        
        # Check that the analyzer got them -- only len because can't compare locations
        self.assertTrue(j_out_all.wait_for_entries(27))

        # Pump in some alerts
        j_in_alert = Journal('j_in_events', 'data/alert_analyzer_test/inject_alerts01.json')
        j_in_alert.inject_queue(get_service(SERVICE_ALERT_ANALYZER_Q))
        
        # Check that the analyzer got them -- only len because can't compare locations
        self.assertTrue(j_out_all.wait_for_entries(34))

        alertmgr = get_service(SERVICE_ALERT_MGR)
        self.assertEqual(len(alertmgr.in_mem_alerts_duplicate), 0)

if __name__ == "__main__":
    unittest.main()