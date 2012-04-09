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

from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal import Teal, registry
from ibm.teal.util.journal import Journal
from ibm.teal.analyzer.analyzer import EventAnalyzer
from ibm.teal.registry import SERVICE_CHECKPOINT_MGR

class JournalAnalyzer(EventAnalyzer):
    ''' Testcase analyzer that holds on to a journal so the testcase can
    determine what events have been processed by the framework
    '''
    def __init__(self, name, inQueue, outQueue, config_dict=None, number=0):        
        self.journal = Journal(name)
        EventAnalyzer.__init__(self, name, inQueue, outQueue, config_dict, number)
    
    def will_analyze_event(self, event):
        ''' always analyze it '''
        return True

    def analyze_event(self, event):
        self.journal.journal_event(event)

    def handle_control_msg(self, control_msg):
        pass

class RestartTest(TealTestCase):

    def setUp(self):
        self.prepare_db()
        
    def tearDown(self):
        self.stop_teal()

    def testRestartBeginEmptyDb(self):  
        ''' Verify we can start up in begin mode with an empty DB
        '''      
        self.restart_with_empty_db('begin')
        
    def testRestartRecoveryEmptyDb(self):
        ''' Verify we can start up in recovery with an empty DB
        '''      
        self.restart_with_empty_db('recovery')

    def testRestartLastProcEmptyDb(self):
        ''' Verify we can start up in lastproc mode with an empty DB
        '''      
        self.restart_with_empty_db('lastproc')

    def testRestartNowEmptyDb(self):
        ''' Verify we can start up in now mode with an empty DB
        '''      
        self.restart_with_empty_db('now')
    
    def testRestartLastProc(self):
        ''' Verify lastproc mode by reading events that have been added after shutdown
        '''
        self.add_entries_before_restart()
        # Add a few more events so we process things
        self.start_teal_no_monitor()
        j_inj = Journal('Pre-populate','data/restart_test/three_events_one.json')
        j_inj.insert_in_db(use_rec_ids=False, no_delay=True)
        self.stop_teal()
        
        # Now start up in lastproc mode and see that we don't get entries ... not checkpoints so acts like Now
        self.start_teal('lastproc')
        j_act = self.find_analyzer().journal
        self.assertFalse(j_act.wait_for_entries(1,seconds=3, msg_mode='quiet'))
        #self.assertTrue(j_act.wait_for_entries(3))
        #j_exp = Journal('After restart','data/restart_test/three_events_one_fromq.json')        
        #self.assertTrue(j_act.deep_match(j_exp,ignore_delay=True))
        j_act.clear()
        
        # Make sure we start getting new entries
        self.inject_new_entries()
        
    def testRestartNow(self):
        ''' Verify now mode by making sure no previous events are read
        '''
        self.add_entries_before_restart()
        
        # Now start up in now mode and make sure we don't get any events
        self.start_teal('now')
        j_act = self.find_analyzer().journal
        self.assertFalse(j_act.wait_for_entries(1,seconds=3, msg_mode='quiet'))
        j_empty = Journal('Empty')        
        self.assertTrue(j_act.deep_match(j_empty,ignore_delay=True))

        # Make sure we start getting new entries
        self.inject_new_entries()
        
    def testRestartBegin(self):
        ''' Verify begin mode by reading all events in the DB
        '''
        self.add_entries_before_restart()

        # Now start up in begin mode and make sure we get ALL the events
        self.start_teal('begin')
        j_act = self.find_analyzer().journal
        j_exp = Journal('After begin','data/restart_test/three_events_one_fromq.json')
        self.assertTrue(j_act.wait_for_entries(3))
        self.assertTrue(j_act.deep_match(j_exp,ignore_delay=True))
        j_act.clear()
        
        # Make sure we start getting new entries
        self.inject_new_entries()

    def testRestartRecovery(self):
        ''' Verify recovery mode by reading events that have been added after shutdown
        '''
        self.add_entries_before_restart()
                
        # Add a few more events so we process things
        self.start_teal_no_monitor()
        j_inj = Journal('Pre-populate','data/restart_test/three_events_one.json')
        j_inj.insert_in_db(use_rec_ids=False, no_delay=True)
        self.stop_teal()
        
        # Now start up in recovery mode and see that we get 3 events
        self.start_teal('recovery')

        j_act = self.find_analyzer().journal
        self.assertFalse(j_act.wait_for_entries(1,seconds=3, msg_mode='quiet'))
        #self.assertTrue(j_act.wait_for_entries(3))
        #j_exp = Journal('After restart','data/restart_test/three_events_one_fromq.json')        
        #self.assertTrue(j_act.deep_match(j_exp,ignore_delay=True))
        j_act.clear()
        
        # Make sure we start getting new entries
        self.inject_new_entries()
        
    def restart_with_empty_db(self,restart):
        ''' Restart TEAL in the specified mode. This assumes that since the 
        database is empty, there will be no events being processed       
        '''
        self.start_teal(restart)
        
        # Make sure that our analyzer doesn't get any events        
        j_act = self.find_analyzer().journal
        j_empty = Journal('Empty')        
        self.assertFalse(j_act.wait_for_entries(1, seconds=5, msg_mode='quiet'))
        self.assertTrue(j_act.deep_match(j_empty,ignore_delay=True))
        
        # Make sure we start getting new events
        self.inject_new_entries()

    def add_entries_before_restart(self, stop_teal=True):
        ''' Add events to TEAL and make sure they are processed
        '''
        self.start_teal('now')     
        # Insert a set of events and process them
        j_act = self.find_analyzer().journal
        j_inj = Journal('Pre-populate','data/restart_test/three_events_one.json')
        j_inj.insert_in_db(no_delay=True, truncate=True)   # Truncate is testing that we handle the ckpt table being destroyed
        registry.get_service(registry.SERVICE_NOTIFIER).post()
        self.assertTrue(j_act.wait_for_entries(3))
        j_exp = Journal('Expected', 'data/restart_test/three_events_one_fromq.json')
        self.assertTrue(j_act.deep_match(j_exp, ignore_delay=True))        
        # Stop this instance of TEAL if requested otherwise it is up
        # to the caller to stop it
        if stop_teal:
            self.stop_teal()

    def inject_new_entries(self,exp_json='data/restart_test/three_events_one_fromq.json',exp_num=3):
        ''' Verify that events still flow through TEAL after startup
        '''
        # Now make sure we start getting new events
        j_inj = Journal('After restart','data/restart_test/three_events_one.json')
        j_inj.insert_in_db(use_rec_ids=False, no_delay=True)
        registry.get_service(registry.SERVICE_NOTIFIER).post()
        j_exp = Journal('Inject New Entries', exp_json)
        j_act = self.find_analyzer().journal
        self.assertTrue(j_act.wait_for_entries(exp_num))
        self.assertTrue(j_act.deep_match(j_exp, ignore_delay=True))   

    def find_analyzer(self):
        ''' Find the Test analyzer that holds onto the journal for processing
        '''
        o = None
        event_q = registry.get_service(registry.SERVICE_EVENT_Q)
        for lm in event_q.listener_methods:
            o = lm.__self__
            if o.get_name() == "RestartAnalyzer":
                break;
        return o
                
    def start_teal(self,restart):
        ''' Start up teal with Journal Analyzer
        '''
        self.t = Teal('data/restart_test/teal_nodelta_noanalyze.conf', logFile='stderr', msgLevel=self.msglevel, restart=restart)

    def start_teal_no_monitor(self):
        ''' start Teal without a monitor so events can be added
        '''
        self.t = Teal('data/common/dbinterfaceonly.conf', logFile='stderr', msgLevel=self.msglevel, commit_checkpoints=False, data_only=True, commit_alerts=False)

    def stop_teal(self):
        ''' Shutdown the currently active TEAL instance
        '''
        try:
            self.t.shutdown()
        except:
            pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()