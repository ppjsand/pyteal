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

from ibm.teal.util.journal import Journal
import unittest

from ibm import teal
from ibm.teal import registry
from ibm.teal.registry import get_logger, SERVICE_ALERT_DELIVERY_Q,\
    SERVICE_ALERT_DELIVERY
from ibm.teal.filter.alert_filter import AlertFilter
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.analyzer import analyzer

class SampleAlertFilterRemoveDup(AlertFilter):
    ''' Alert filter that removes duplicate for a specified amount of time'''
    
    def __init__(self, name, config_dict=None):
        '''The constructor'''
        self.name = name
        if 'time_period' not in config_dict:
            self.time_period = 5
        else:
            self.time_period = int(config_dict['time_period'])
        #self.name += '(' + str(self.time_period) + ')'
        self.alerts = {}
        AlertFilter.__init__(self, self.name, config_dict)
        return

    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on
        '''
        # get alert from list if there 
        filter_it = False
        alert_id = alert.alert_id
        if alert_id in self.alerts:
            delta = alert.get_time_occurred() - self.alerts[alert_id].get_time_occurred()
            get_logger().debug('delta is %s for alert %s', str(delta.seconds), str(alert))
            if delta.seconds < self.time_period:
                filter_it = True 
            else:
                # replace one we have and let this one through 
                self.alerts[alert_id] = alert
                filter_it = False
        else:
            # add it 
            self.alerts[alert_id] = alert
            filter_it = False 
        return filter_it

    def resolve_and_validate(self, info_dict):
        ''' Nothing to do '''
        return
    
class DummyTestAnalyzer(analyzer.EventAnalyzer):
    ''' Used to configre an analyzer to test against for analyzer name filter '''
    def __init__(self, name, inEventQueue, outQueue, config_dict=None, number=0):
        analyzer.EventAnalyzer.__init__(self, name, inEventQueue, outQueue, config_dict, number)
                                        
    def analyze_alert(self):
        return False
    
    def analyze_event(self, event):
        pass
    
    def handle_control_msg(self, control_msg):
        pass
    
    def will_analyze_alert(self, alert):
        return False
    
    def will_analyze_event(self, event):
        return False    
    
class NoiseAlertFilterTest(TealTestCase):
    def testEmptyNoiseFilter(self):
        ''' Runs a noise filter with no values '''
        self.prepare_db()
        t = teal.Teal('data/alert_filter_test/test_03.conf',msgLevel='warn',logFile='stderr')

        dq = registry.get_service(SERVICE_ALERT_DELIVERY)
        self.assertEqual(dq.filters[0].get_name(),'NoiseAlertFilter')
                
        j = Journal('AlertAnalyzer', 'data/alert_filter_test/inject_DQ_alerts.json')
        j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
    
        alj = find_listener()
        alj.journal.wait_for_entries(7)
        
        out_j = Journal('AlertListener', 'data/alert_filter_test/empty_alerts.json')
        self.assertTrue(alj.journal.deep_match(out_j, ignore_times=True))

        t.shutdown()
        
    def testFullNoiseFilter(self):
        ''' Runs a noise filter with all values '''
        self.prepare_db()
        t = teal.Teal('data/alert_filter_test/test_04.conf',msgLevel='warn',logFile='stderr')
        
        j = Journal('AlertAnalyzer', 'data/alert_filter_test/inject_DQ_alerts.json')
        j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
    
        alj = find_listener()
        alj.journal.wait_for_entries(6)
        
        out_j = Journal('AlertListener', 'data/alert_filter_test/full_alerts.json')
        self.assertTrue(alj.journal.deep_match(out_j, ignore_times=True))
        
        t.shutdown()
                        
    def testPartialNoiseFilter(self):
        ''' Runs a noise filter with some values '''
        self.prepare_db()
        t = teal.Teal('data/alert_filter_test/test_05.conf',msgLevel='warn',logFile='stderr')
        
        j = Journal('AlertAnalyzer', 'data/alert_filter_test/inject_DQ_alerts.json')
        j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
    
        alj = find_listener()
        alj.journal.wait_for_entries(4)
        
        out_j = Journal('AlertListener', 'data/alert_filter_test/partial_alerts.json')
        self.assertTrue(alj.journal.deep_match(out_j, ignore_times=True))
        
        t.shutdown()
        
class AnalyzerNameFilterTest(TealTestCase):
    def testEmptyConfig(self):
        ''' Configure AnalyzerNameFilter without any parms '''
        self.assertRaisesTealError(ConfigurationError, 
                                   'AlertFilterFromAnalyzer requires when be specified', 
                                   teal.Teal, 
                                   'data/alert_filter_test/test_06.conf',
                                   msgLevel='warn',
                                   logFile='stderr')
        
    def testBadWhen(self):
        ''' Test invalid when clause in stanza '''
        self.assertRaisesTealError(ConfigurationError, 
                                   'AlertFilterFromAnalyzer when must be from_analyzer or not_from_analyzer. Value is pigs_fly was specified for NameFilter', 
                                   teal.Teal, 
                                   'data/alert_filter_test/test_07.conf',
                                   msgLevel='warn',
                                   logFile='stderr')
        
    def testMissingName(self):
        ''' Test missing name clause in stanza '''
        self.assertRaisesTealError(ConfigurationError, 
                                   'AlertFilterFromAnalyzer requires analyzer_names be specified', 
                                   teal.Teal, 
                                   'data/alert_filter_test/test_08.conf',
                                   msgLevel='warn',
                                   logFile='stderr')
        
    def testEmptyName(self):
        ''' Test name specified but empty '''
        self.assertRaisesTealError(ConfigurationError, 
                                   'AlertFilterFromAnalyzer analyzer_names was empty', 
                                   teal.Teal, 
                                   'data/alert_filter_test/test_09.conf',
                                   msgLevel='warn',
                                   logFile='stderr')
    
    def testUnconfiguredAnalyzer(self):
        ''' Test name filter for analyzer that is not configured '''
        self.assertRaisesTealError(ConfigurationError, 
                                   'AlertFilterFromAnalyzer analyzer_names entry MissingAnalyzer not configured or not active', 
                                   teal.Teal, 
                                   'data/alert_filter_test/test_10.conf',
                                   msgLevel='warn',
                                   logFile='stderr')
    
    def testAnalyzers(self):
        ''' Validate functionality of both analyzer types '''
        self.prepare_db()
        t = teal.Teal('data/alert_filter_test/test_11.conf',msgLevel='info',logFile='stderr')
        j = Journal('AlertAnalyzer', 'data/alert_filter_test/inject_DQ_alerts.json')
        j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
    
        aif = find_listener('AlertFilterIfNameListener')
        aif.journal.wait_for_entries(5)
        
        anif = find_listener('AlertFilterIfNotNameListener')
        anif.journal.wait_for_entries(4)
        
        out_jif = Journal('AlertListener', 'data/alert_filter_test/ifname_alerts.json')
        self.assertTrue(aif.journal.deep_match(out_jif, ignore_times=True))

        out_jnif = Journal('AlertListener', 'data/alert_filter_test/ifnotname_alerts.json')
        self.assertTrue(aif.journal.deep_match(out_jnif, ignore_times=True))
        
        t.shutdown()

    
class DuplicateInMemAlertFilterTest(TealTestCase):
    def setUp(self):
        self.prepare_db()
        self.t = teal.Teal('data/alert_filter_test/test_01.conf', 'stderr', msgLevel='warn', commit_alerts=False, commit_checkpoints=False)

    def tearDown(self):
        self.t.shutdown()
    
    def testName(self):
        ''' Test that the name was set and can be retrieved
        '''
        dq = registry.get_service(SERVICE_ALERT_DELIVERY)
        self.assertEqual(dq.filters[0].get_name(),'DuplicateAlertFilter')
    
    def testFilter(self):
        ''' Test that a duplicate is filtered when not backed by a database 
        ''' 
        j = Journal('AlertAnalyzer', 'data/alert_test/inject_DQ_alerts.json')
        j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
    
        alj = find_listener()
        alj.journal.wait_for_entries(4)
        
        out_j = Journal('AlertListener', 'data/alert_filter_test/unfiltered_alerts.json')
        self.assertTrue(alj.journal.deep_match(out_j, ignore_times=True))
    
class DuplicateDbAlertFilterTest(TealTestCase):
    def setUp(self):
        self.prepare_db()
        self.t = teal.Teal('data/alert_filter_test/test_02.conf', 'stderr', msgLevel='warn', commit_alerts=True, commit_checkpoints=False)

    def tearDown(self):
        self.t.shutdown()
    
    def testFilter(self):
        ''' Test that a duplicate is filtered when backed by a database
        '''
        j = Journal('AlertAnalyzer', 'data/alert_test/inject_DQ_alerts.json')
        j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
    
        alj = find_listener()
        alj.journal.wait_for_entries(4)
        
        out_j = Journal('AlertListener', 'data/alert_filter_test/unfiltered_alerts.json')
        self.assertTrue(alj.journal.deep_match(out_j, ignore_times=True))

def find_listener(listener_name="AlertFilterTestListener"):
    ''' Find the Test analyzer that holds onto the journal for processing
    '''
    al = None
    dq = registry.get_service(registry.SERVICE_ALERT_DELIVERY)
    for al in dq.listeners:
        if al.get_name() == listener_name:
            break
    return al

    
if __name__ == "__main__":
    unittest.main()