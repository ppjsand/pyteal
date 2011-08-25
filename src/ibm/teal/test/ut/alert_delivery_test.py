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
from ibm.teal import Teal
from ibm.teal.filter.alert_filter import AlertFilter
from ibm.teal.registry import get_service, SERVICE_ALERT_DELIVERY_Q, \
    SERVICE_ALERT_DELIVERY, SERVICE_ALERT_MGR
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.util.journal import Journal
import unittest
from ibm.teal.listener.alert_listener import AlertListener
from ibm.teal.alert import create_teal_alert

class AlertListenerFailure(AlertListener):
    ''' Alert listener that creates alerts '''
    
    def process_alert(self, alert):
        '''The alert for the listener to process is passed'''
        self.create_listener_alert('TST00001', 'testing', 'alert id = {0}'.format(alert.alert_id))
        return
    
class AlertFilterSampleSeverity(AlertFilter):
    ''' Only allow alerts with the specified severity through'''
    
    def __init__(self, name, config_dict=None):
        '''The constructor'''
        use_name = name
        if config_dict is not None and 'severity' not in config_dict:
            self.severity ='I'
        else:
            self.severity = config_dict['severity']
        #use_name += '(' + self.severity + ')'
        AlertFilter.__init__(self, use_name, config_dict)
        return

    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on
        '''
        # get alert from list if there 
        if alert.severity == self.severity:
            #p rint 'S do not filter ' + str(alert.severity)
            return False
        else:
            #p rint 'S filter ' + str(alert.severity)
            return True
   
    def resolve_and_validate(self, info_dict):  
        ''' nothing to resolve '''
        return   

class AlertFilterSampleAlertId(AlertFilter):
    ''' Only allow alerts with the specified alert id through'''
    
    def __init__(self, name, config_dict=None):
        '''The constructor'''
        use_name = name
        if config_dict is not None and 'alert_id' not in config_dict:
            raise ValueError
        else:
            self.alert_id = config_dict['alert_id']
        #use_name += '(' + self.alert_id + ')'
        AlertFilter.__init__(self, use_name, config_dict)
        return
    
    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on
        '''
        # get alert from list if there 
        if alert.alert_id == self.alert_id:
            #p rint 'A do not filter ' + str(alert.get_alert_id())
            return False
        else:
            #p rint 'A filter ' + str(alert.get_alert_id())
            return True
   
    def resolve_and_validate(self, info_dict):  
        ''' nothing to resolve '''
        return   


class AlertFilterSampleNotAlertId(AlertFilter):
    ''' Only allow alerts that do not have the specified alert id through'''
    
    def __init__(self, name, config_dict=None):
        '''The constructor'''
        use_name = name
        if config_dict is not None and 'alert_id' not in config_dict:
            raise ValueError
        else:
            self.alert_id = config_dict['alert_id']
        #use_name += '(' + self.alert_id + ')'
        AlertFilter.__init__(self, use_name, config_dict)
        return

    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on
        '''
        # get alert from list if there 
        if alert.alert_id == self.alert_id:
            #p rint 'N filter ' + str(alert.alert_id)
            return True
        else:
            #p rint 'N do not filter ' + str(alert.alert_id)
            return False
   
    def resolve_and_validate(self, info_dict):  
        ''' nothing to resolve '''
        return   

class AlertDeliveryTest(TealTestCase):
    '''Test the alert delivery (filters and listeners)'''

    def setUp(self):
        '''Setup Teal'''
        self.keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'No')
        self.teal = Teal('data/alert_delivery_test/test_local_filters.conf', "stderr", msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        return
    
    def tearDown(self):
        '''Teardown teal'''
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', self.keep_ADC)
        return

    def testGeneralFilters(self):
        '''test alert delivery with global and local filtering'''
        j_in_dq = Journal('j_in_DQ', 'data/alert_delivery_test/data_sample_inject_DQ.json')
        #p rint str(j_in_dq)
        dq_q = get_service(SERVICE_ALERT_DELIVERY_Q)
        # Get the AlertListenerJournal journals
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            #p rint name
            if name == 'AllAlerts':
                j_out_all = listener.journal
            if name == 'OnlyAlertId':
                j_out_alert_id = listener.journal
            if name == 'OnlyAlertIdUrgent':
                j_out_ai_urgent = listener.journal
        # inject
        j_in_dq.inject_queue(dq_q)
        # wait for stuff to come out
        self.assertTrue(j_out_all.wait_for_entries(5))
        self.assertTrue(j_out_alert_id.wait_for_entries(3))
        self.assertTrue(j_out_ai_urgent.wait_for_entries(2))
        #
        print j_out_all
        j_out_all_exp = Journal('j_out_all_exp', 'data/alert_delivery_test/data_sample_out_all_alerts.json')
        print j_out_all_exp
        self.assertTrue(j_out_all.deep_match(j_out_all_exp, ignore_delay=True, ignore_times=True))
        print j_out_alert_id
        j_out_alert_id_exp = Journal('j_out_alert_id_exp', 'data/alert_delivery_test/data_sample_out_alert_id.json')
        self.assertTrue(j_out_alert_id.deep_match(j_out_alert_id_exp, ignore_delay=True, ignore_times=True))
        print j_out_ai_urgent
        j_out_ai_urgent_exp = Journal('j_out_ai_urgent_exp', 'data/alert_delivery_test/data_sample_out_ai_urgent.json')
        self.assertTrue(j_out_ai_urgent.deep_match(j_out_ai_urgent_exp, ignore_delay=True, ignore_times=True))
        return
    
    
class AlertAnalyzerFilterTest(TealTestCase):
    '''Test the alert delivery (filters and listeners)'''

    def setUp(self):
        '''Setup Teal'''
        # Not testing duplicates, so OK to turn off
        self.keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'No')
        self.teal = Teal('data/alert_delivery_test/analyzer_filter/test.conf', "stderr", msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        return
    
    def tearDown(self):
        '''Teardown teal'''
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', self.keep_ADC)
        return

    def testGeneralFilters(self):
        '''test alert delivery with global and local filtering'''
        j_in_dq = Journal('j_in_DQ', 'data/alert_delivery_test/analyzer_filter/inject_DQ_alerts.json')
        print j_in_dq
        dq_q = get_service(SERVICE_ALERT_DELIVERY_Q)
        # Get the AlertListenerJournal journals
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'AllAlerts':
                j_out_all = listener.journal
            if name == 'OnlyAnalyzer1':
                j_out_analyzer1 = listener.journal
            if name == 'AnyButAnalyzer1':
                j_out_not_analyzer1 = listener.journal
            if name == 'OnlyAnalyzer2and3':
                j_out_analyzer2and3 = listener.journal
            if name == 'AnyButAnalyzer2and3':
                j_out_not_analyzer2and3 = listener.journal
            if name == 'AnyButAnalyzer1and2and3':
                j_out_not_analyzer1and2and3 = listener.journal
        # inject
        j_in_dq.inject_queue(dq_q)
        # Get expected values
        j_out_all_exp = Journal('all_exp', 'data/alert_delivery_test/analyzer_filter/alerts_out_all.json')
        j_out_analyzer1_exp = Journal('analyzer1', 'data/alert_delivery_test/analyzer_filter/alerts_out_analyzer1.json')
        j_out_not_analyzer1_exp = Journal('not_analyzer1', 'data/alert_delivery_test/analyzer_filter/alerts_out_not_analyzer1.json')
        j_out_analyzer2and3_exp = Journal('analyzer2and3', 'data/alert_delivery_test/analyzer_filter/alerts_out_analyzer2and3.json')
        j_out_not_analyzer2and3_exp = Journal('not_analyzer2and3', 'data/alert_delivery_test/analyzer_filter/alerts_out_not_analyzer2and3.json')
        j_out_not_analyzer1and2and3_exp = Journal('not_analyzer1and2and3','data/alert_delivery_test/analyzer_filter/alerts_out_not_analyzer1and2and3.json')
        # wait for stuff to come out
        self.assertTrue(j_out_all.wait_for_entries(len(j_out_all_exp)))
        self.assertTrue(j_out_analyzer1.wait_for_entries(len(j_out_analyzer1_exp)))
        self.assertTrue(j_out_not_analyzer1.wait_for_entries(len(j_out_not_analyzer1_exp)))
        self.assertTrue(j_out_analyzer2and3.wait_for_entries(len(j_out_analyzer2and3_exp)))
        self.assertTrue(j_out_not_analyzer2and3.wait_for_entries(len(j_out_not_analyzer2and3_exp)))
        self.assertTrue(j_out_not_analyzer1and2and3.wait_for_entries(len(j_out_not_analyzer1and2and3_exp)))
        # Check that it was what was expected
        self.assertTrue(j_out_all.deep_match(j_out_all_exp, ignore_delay=True, ignore_times=True))
        self.assertTrue(j_out_analyzer1.deep_match(j_out_analyzer1_exp, ignore_delay=True, ignore_times=True))
        self.assertTrue(j_out_not_analyzer1.deep_match(j_out_not_analyzer1_exp, ignore_delay=True, ignore_times=True))
        self.assertTrue(j_out_analyzer2and3.deep_match(j_out_analyzer2and3_exp, ignore_delay=True, ignore_times=True))
        self.assertTrue(j_out_not_analyzer2and3.deep_match(j_out_not_analyzer2and3_exp, ignore_delay=True, ignore_times=True))
        self.assertTrue(j_out_not_analyzer1and2and3.deep_match(j_out_not_analyzer1and2and3_exp, ignore_delay=True, ignore_times=True))
        return    
    
    
class AlertListenerFailureTest(TealTestCase):
    '''Test the alert delivery (filters and listeners)'''

    def setUp(self):
        '''Setup Teal'''
        # Not testing duplicates, so OK to turn off
        self.keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'No')
        self.teal = Teal('data/alert_delivery_test/listener_failure/test.conf', "stderr", msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        return
    
    def tearDown(self):
        '''Teardown teal'''
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', self.keep_ADC)
        return

    def testGeneralFilters(self):
        '''test alert delivery with global and local filtering'''
        j_in_dq = Journal('j_in_DQ', 'data/alert_delivery_test/listener_failure/inject_DQ_alerts.json')
        print j_in_dq
        dq_q = get_service(SERVICE_ALERT_DELIVERY_Q)
        # Get the AlertListenerJournal journals
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'AllAlerts':
                j_out_all = listener.journal
            if name == 'OnlyAnalyzer1':
                j_out_analyzer1 = listener.journal
        # inject
        j_in_dq.inject_queue(dq_q)
        # Create a TEAL alert 
        create_teal_alert('XXXXXXXX', 'no reason at all', 'medium well', loc_instance="YYY")
        
        # Get expected values
        j_out_all_exp = Journal('all_exp', 'data/alert_delivery_test/analyzer_filter/alerts_out_all.json')
        j_out_analyzer1_exp = Journal('analyzer1', 'data/alert_delivery_test/analyzer_filter/alerts_out_analyzer1.json')
        # wait for stuff to come out
        self.assertTrue(j_out_all.wait_for_entries(len(j_out_all_exp)+3))
        self.assertTrue(j_out_analyzer1.wait_for_entries(len(j_out_analyzer1_exp)))
        # Check that it was what was expected
        
        # Can't really check this because the location is unique for each machine and run
        #  Make sure only 3 extra
        self.assertEqual(len(j_out_all)-len(j_out_all_exp), 3)
        #self.assertTrue(j_out_all.deep_match(j_out_all_exp, ignore_delay=True, ignore_times=True))
        self.assertTrue(j_out_analyzer1.deep_match(j_out_analyzer1_exp, ignore_delay=True, ignore_times=True))
        print j_out_all
        #print j_out_analyzer1
        return
    

if __name__ == "__main__":
    unittest.main()