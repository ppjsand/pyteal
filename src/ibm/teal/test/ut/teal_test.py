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

import os
import sys
from ibm.teal import Teal, registry
from ibm.teal.registry import SERVICE_EVENT_Q, SERVICE_ALERT_DELIVERY_Q, \
    SERVICE_ALERT_ANALYZER_Q, SERVICE_ALERT_DELIVERY, get_service, TEAL_DATA_DIR,\
    TEAL_ROOT_DIR, TEAL_LOG_DIR
from ibm.teal.teal_error import TealError
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.util.journal import Journal
import unittest
from ibm.teal.teal import TEAL_RUN_MODE_HISTORIC
from multiprocessing import Process


def check_environment(exp_root_dir, exp_data_dir, exp_log_dir):
    ''' Ensure a subprocess inherits the environment properly
    '''
    act_data_dir = os.environ.get(TEAL_DATA_DIR, None)
    act_root_dir = os.environ.get(TEAL_ROOT_DIR, None)
    act_log_dir = os.environ.get(TEAL_LOG_DIR, None)
    
    success = True
    success &= (act_root_dir == exp_root_dir)  
    success &= (act_data_dir == exp_data_dir)
    success &= (act_log_dir == exp_log_dir)
    
    if success:
        sys.exit(0)
    else:
        print >>sys.stderr, '*** TEAL_ROOT_DIR: actual = {0}, expected = {1}'.format(act_root_dir, exp_root_dir) 
        print >>sys.stderr, '*** TEAL_DATA_DIR: actual = {0}, expected = {1}'.format(act_data_dir, exp_data_dir) 
        print >>sys.stderr, '*** TEAL_LOG_DIR: actual = {0}, expected = {1}'.format(act_log_dir, exp_log_dir) 
        sys.exit(30)

class TealTest(TealTestCase):

    def testTooManyMonitors(self):
        ''' Verify that Teal fails if more than one monitor is specified'''
        self.assertRaisesTealError(TealError, "There can only be one section called 'event_monitor'", Teal, 'data/teal_test/tealtest_01.conf', 'stderr', self.msglevel,'now','realtime',False, False, None, False, '', False)

    def testTooFewMonitors(self):
        ''' Verify that Teal fails if no monitor is specified'''
        self.assertRaisesTealError(TealError, 
                                   'No monitor configured - must have one monitor configured and enabled',
                                   Teal, 
                                   'data/teal_test/tealtest_03.conf', 'stderr', self.msglevel,'now','realtime',False, False, None, False, '', False)

    def testTooManyDatabases(self):
        ''' Verify that Teal fails if more than one database is specified'''
        #TODO: Need to create a dummy database connection or full db connection usport
        #self.assertRaises(TealError, Teal, 'data/teal_test/tealtest_02.conf', 'stderr')
        pass
    
    def testBadEnabled(self):
        '''Verify failure when plugin section has bad value for enabled keyword'''
        self.assertRaisesTealError(TealError, "Configuration section 'event_monitor.EventMonitorNoop' has an unrecognized value for enabled keyword: 'bad_value'", Teal, 'data/teal_test/bad_02.conf','stderr', self.msglevel,'now','realtime',False, False, None, False, '', False)
    
    def testBadEnvHasConfig(self):
        ''' Verify failure when environment section specifies a config dir '''
        self.assertRaisesTealError(TealError, "Option 'TEAL_CONF_DIR' is not allowed in the 'environment' stanza", Teal, 'data/teal_test/bad_03.conf','stderr', self.msglevel,'now','realtime',False, False, None, False, '', False)
        
    def testBadRunModeValue(self):
        ''' Verify failure if bad runmode is passed '''
        self.assertRaisesTealError(TealError, "Unrecognized run mode specified: bad_mode", Teal, 'data/teal_test/bad_02.conf', 'stderr', self.msglevel, 'now', 'bad_mode')
       
    def testEnabledRealtime(self):
        ''' Verify that realtime indicator on enabled plug-in control works '''
        teal = Teal('data/teal_test/good_01.conf', 'stderr', msgLevel=self.msglevel, run_mode='realtime', commit_alerts=False, commit_checkpoints=False)
        event_q_lsrs = registry.get_service(SERVICE_EVENT_Q).listener_methods
        self.assertEquals(len(event_q_lsrs), 2)
        names = []
        for lsr_m in event_q_lsrs:
            names.append(lsr_m.__self__.get_name())
        self.assertTrue('AnalyzerTest055a' in names)
        self.assertTrue('AnalyzerTest055b' in names)
        teal.shutdown()
    
    def testEnabledHistoric(self):
        ''' Verify that historic indicator on enabled plug-in control works '''
        teal = Teal('data/teal_test/good_01.conf', 'stderr', msgLevel=self.msglevel, run_mode='historic', commit_alerts=False, commit_checkpoints=False)
        event_q_lsrs = registry.get_service(SERVICE_EVENT_Q).listener_methods
        self.assertEquals(len(event_q_lsrs), 1)
        names = []
        for lsr_m in event_q_lsrs:
            names.append(lsr_m.__self__.get_name())
        self.assertTrue('AnalyzerTest055a' in names)
        teal.shutdown()
    
    def testHistoricOnlyHistoric(self):
        ''' Verify that the historic monitor can only be run in historic mode '''
        self.assertRaisesTealError(TealError, "Historic monitor can only enabled for historic use.  Unsupported value specified: realtime", Teal, 'data/teal_test/bad_hist_mon_01.conf', 'stderr', self.msglevel, 'now', 'realtime')
        self.assertRaisesTealError(TealError, "Historic monitor can only enabled for historic use.  Unsupported value specified: all", Teal, 'data/teal_test/bad_hist_mon_02.conf', 'stderr', self.msglevel, 'now', 'historic')
        # Should run ... clear the DB and run it with no events, so nothing will happen
        self.prepare_db()
        teal = Teal('data/teal_test/bad_hist_mon_03.conf', 'stderr', self.msglevel, 'now', 'historic')
        teal.shutdown()
    
    def testRealtimeOnlyRealtime(self):
        ''' Verify that the realtime monitor can only be run in realtime mode '''
        self.assertRaisesTealError(TealError, "Realtime monitor can only enabled for realtime use.  Unsupported value specified: historic", Teal, 'data/teal_test/bad_real_mon_01.conf', 'stderr', self.msglevel, 'now', 'historic')
        self.assertRaisesTealError(TealError, "Realtime monitor can only enabled for realtime use.  Unsupported value specified: all", Teal, 'data/teal_test/bad_real_mon_02.conf', 'stderr', self.msglevel, 'now', 'realtime')
        # Notifier is checked after the enabled check ... so this makes sure enabled check passed
        keep_ev = self.remove_env('TEAL_TEST_NOTIFIER_CONFIG')
        self.assertRaisesTealError(TealError, "RealtimeMonitor requires notifier be specified in the configuration file or as an environment variable", Teal, 'data/teal_test/bad_real_mon_03.conf', 'stderr', self.msglevel, 'now', 'realtime')
        self.restore_env('TEAL_TEST_NOTIFIER_CONFIG', keep_ev)
        
    def testEnvInConfig(self):
        ''' Test that having env in the config works '''
        keep_root_dir = self.remove_env(TEAL_ROOT_DIR)
        keep_log_dir = self.remove_env(TEAL_LOG_DIR)
        keep_data_dir = self.remove_env(TEAL_DATA_DIR)
        self.teal = Teal('data/teal_test/env_test.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        
        root_dir = registry.get_service(registry.TEAL_ROOT_DIR)
        data_dir = registry.get_service(registry.TEAL_DATA_DIR)
        log_dir = registry.get_service(registry.TEAL_LOG_DIR)
        
        tealp = Process(target=check_environment, args=(root_dir, data_dir, log_dir))
        
        tealp.start()
        tealp.join()
        
        self.teal.shutdown()
        self.restore_env(TEAL_ROOT_DIR, keep_root_dir)
        self.restore_env(TEAL_LOG_DIR, keep_log_dir)
        self.restore_env(TEAL_DATA_DIR, keep_data_dir)
        
        # After everything is restored, make sure that the subprocess completed successfully
        self.assertEquals(tealp.exitcode, 0)
        
class TealTestDemoEventQ(TealTestCase):
    '''Test the demo configuration ''' 
        
    def testDemo1EventQ(self):
        '''Test that the first demo flow works -- Inject Event Q'''
        self.teal = Teal('data/teal_test/configurationtest_05_auto.conf', 'stderr', msgLevel=self.msglevel, 
                         commit_alerts=False, commit_checkpoints=False, run_mode=TEAL_RUN_MODE_HISTORIC)
        j_in = Journal('j_in', file='data/demo/data_sample_demo_NEW_001.json')
        j_out_aaq = Journal('j_out_aaq')
        j_out_dq = Journal('j_out_dq')
        j_out_lis = Journal('j_out_lis')
        q_in = registry.get_service(SERVICE_EVENT_Q)
        q_out_aaq = registry.get_service(SERVICE_ALERT_ANALYZER_Q)
        q_out_dq = registry.get_service(SERVICE_ALERT_DELIVERY_Q)
        q_out_dq.register_listener(j_out_dq)
        q_out_aaq.register_listener(j_out_aaq)
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'outputJournal':
                j_out_lis = listener.journal
        j_in.inject_queue(q_in)
        self.assertTrue(j_out_lis.wait_for_entries(3))
        j_exp_aaq = Journal('j_exp_aaq', 'data/teal_test/data_sample_demo_NEW_001_AAQ_Result.json')
        self.assertTrue(j_out_aaq.deep_match(j_exp_aaq, ignore_delay=True, ignore_times=True))
        j_exp_dq = Journal('j_exp_dq', 'data/teal_test/data_sample_demo_NEW_001_DQ_Result.json')
        self.assertTrue(j_out_dq.deep_match(j_exp_dq, ignore_delay=True, ignore_times=True))
        j_exp_lis = Journal('j_exp_lis', 'data/teal_test/data_sample_demo_NEW_001_LIS_Result.json')
        self.assertTrue(j_out_lis.deep_match(j_exp_lis, ignore_delay=True, ignore_times=True))
        
        q_out_aaq.unregister_listener(j_out_aaq)        
        q_out_dq.unregister_listener(j_out_dq)
        self.teal.shutdown()
    
    
class TealTestDemoDB(TealTestCase):
    '''Test the demo configuration '''
    
    def testDemo1DB(self):
        '''Test demo flow by injecting into DB'''
        self.prepare_db()
        keep_var = self.force_env('TEAL_TEST_POOL_TIMERS_OFF', 'YES')
        self.teal = Teal('data/teal_test/configurationtest_05_semaphore_auto.conf', 'stderr', 
                         msgLevel=self.msglevel)

        j_in = Journal('j_in', file='data/demo/data_sample_demo_NEW_001.json')
        j_out_eq = Journal('j_out_eq')
        j_out_aaq = Journal('j_out_aaq')
        j_out_dq = Journal('j_out_dq')
        j_out_lis = Journal('j_out_lis')
        q_out_eq = registry.get_service(SERVICE_EVENT_Q)
        q_out_aaq = registry.get_service(SERVICE_ALERT_ANALYZER_Q)
        q_out_dq = registry.get_service(SERVICE_ALERT_DELIVERY_Q)
        q_out_eq.register_listener(j_out_eq)
        q_out_dq.register_listener(j_out_dq)
        q_out_aaq.register_listener(j_out_aaq)
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'outputJournal':
                j_out_lis = listener.journal
        try:
            j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=False, post=True)
        except:
            print 'INSERTION FAILED'
            q_out_eq.unregister_listener(j_out_eq)
            q_out_dq.unregister_listener(j_out_dq)
            q_out_aaq.unregister_listener(j_out_aaq)
            raise
       
        # Yes, only 2: Flush can't be injected to connector, so pool does not get closed, so last event
        # Does not get turned into an alert!
        self.assertTrue(j_out_lis.wait_for_entries(2))

        # Note these connector ('C') versions have one less alert
        #     The analyzer is being run in historic mode (see configuration) if that was 
        #     changed to runtime then the pool would time out and the last alert would be journaled
        j_exp_aaq = Journal('j_exp_aaq', 'data/teal_test/data_sample_demo_NEW_001_AAQ_Result_C.json')
        self.assertTrue(j_out_aaq.deep_match(j_exp_aaq, ignore_delay=True, ignore_times=True))
        j_exp_dq = Journal('j_exp_dq', 'data/teal_test/data_sample_demo_NEW_001_DQ_Result_C.json')
        self.assertTrue(j_out_dq.deep_match(j_exp_dq, ignore_delay=True, ignore_times=True))
        j_exp_lis = Journal('j_exp_lis', 'data/teal_test/data_sample_demo_NEW_001_LIS_Result_C.json')
        self.assertTrue(j_out_lis.deep_match(j_exp_lis, ignore_delay=True, ignore_times=True))

        q_out_eq.unregister_listener(j_out_eq)
        q_out_dq.unregister_listener(j_out_dq)
        q_out_aaq.unregister_listener(j_out_aaq)
        
        self.teal.shutdown()
        self.restore_env('TEAL_TEST_POOL_TIMERS_OFF', keep_var)

  
if __name__ == "__main__":
    unittest.main()
