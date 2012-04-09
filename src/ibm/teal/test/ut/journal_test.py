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
from ibm.teal.alert import ALERT_ATTR_REC_ID, ALERT_ATTR_ALERT_ID, \
    ALERT_ATTR_RECOMMENDATION
from ibm.teal.event import EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID
from ibm.teal.registry import get_service, SERVICE_ALERT_DELIVERY_Q, \
    SERVICE_ALERT_DELIVERY
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.util.journal import Journal
from ibm.teal.util.listenable_queue import ListenableQueue
from time import sleep
import unittest


class JournalTest(TealTestCase):


    def setUp(self):        
        self.teal = Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)

    def tearDown(self):
        self.teal.shutdown()

    def testJournalLoadSave(self):
        ''' Test loading and saving a json file ''' 
        Journal('test journal', file='data/journal_test/data_sample_001_NEW.json')
        # TODO: Clean up the file after it gets created
        #j.save('data/journal_test/data_sample_001_NEW_AUTO_OUT.json')
        return
    
    def testJournalQueue(self):
        ''' Test injecting the Journal through a queue'''
        lq = ListenableQueue('test journal queue')
        j = Journal('test journal -- input', file='data/journal_test/data_sample_001_NEW.json')
        j_rec = Journal('j_rec -- output')
        lq.register_listener(j_rec)
        j.inject_queue(lq)
        while len(j) != len(j_rec):
            # p rint ('waiting for queue to process %s of %s' % (str(len(j_rec)), str(len(j))))
            sleep(1.0)
        #p rint j
        #p rint j_rec
        self.assertTrue(j.deep_match(j))
        self.assertTrue(j.deep_match(j_rec, ignore_delay=True))
        return
     

class JournalTestWithOptionalData(TealTestCase):


    def setUp(self):
        self.teal = Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)

    def tearDown(self):
        self.teal.shutdown()

#    def testJournalLoadSave(self):
#        ''' Test loading and saving a json file with optional fields. ''' 
#        j = Journal('test journal', file='data/journal_test/data_sample_002_NEW.json')
#        j.save('data/journal_test/data_sample_002_NEW_AUTO_OUT.json')
#        return
    
    def testJournalQueue(self):
        ''' Test injecting a Journal containing optional fields through a queue'''
        lq = ListenableQueue('test journal queue')
        j = Journal('test journal', file='data/journal_test/data_sample_002_NEW.json')
        j_rec = Journal('j_rec')
        lq.register_listener(j_rec)
        j.inject_queue(lq)
        while len(j) != len(j_rec):
            # p rint ('waiting for queue to process %s of %s' % (str(len(j_rec)), str(len(j))))
            sleep(1.0)
        #p rint j
        #p rint j_rec
        self.assertTrue(j.deep_match(j))
        self.assertTrue(j.deep_match(j_rec, ignore_delay=True))
        return
    
    
class JournalTestWithDB(TealTestCase):

    def testJournalWriteEventDB1(self):
        ''' Test writing to Event log DB basic
        '''
        self.teal = Teal('data/journal_test/events_001.conf','stderr',msgLevel=self.msglevel)
        j = Journal('DB test journal to write', file='data/journal_test/events_001.json')
        j.insert_in_db(truncate=True, no_delay=True)
        jdb = Journal('DB test journal to read')
        jdb.select_from_db('event')
        self.assertTrue(j.deep_match(jdb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        #p rint j
        #p rint jdb
        self.teal.shutdown()
        return
    
    def testJournalWriteEventDB2(self):
        ''' Test writing to Event log DB without recids
        '''
        self.teal = Teal('data/journal_test/events_001.conf','stderr',msgLevel=self.msglevel)
        j = Journal('DB test journal to write', file='data/journal_test/events_001.json')
        j.insert_in_db(truncate=True, use_rec_ids=False, no_delay=True)
        jdb = Journal('DB test journal to read')
        jdb.select_from_db('event')
        self.assertTrue(j.deep_match(jdb, ignore_delay=True, ignore_times=False, ignore_rec_id=True))
        #p rint j
        #p rint jdb
        self.teal.shutdown()
        return
    
    def testJournalWriteEventDB3(self):
        ''' Test reading from event DB with a subset of fields 
        '''
        self.teal = Teal('data/journal_test/events_001.conf','stderr',msgLevel=self.msglevel)
        j = Journal('DB test journal to write', file='data/journal_test/events_001.json')
        j.insert_in_db(truncate=True, use_rec_ids=False, no_delay=True)
        jdb = Journal('DB test journal to read')
        jdb.select_from_db('event', event_fields=[EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID])
        jexp = Journal('DB expected', 'data/journal_test/events_004.json')
        self.assertTrue(jexp.deep_match(jdb, ignore_delay=True, ignore_times=False, ignore_rec_id=True))
        #p rint j
        #p rint jdb
        self.teal.shutdown()
        return

    def testJournalWriteAlertDB1(self):
        ''' Test writing of Alert log DB basic '''
        self.teal = Teal('data/journal_test/events_001.conf','stderr',msgLevel=self.msglevel)
        # Events
        je = Journal('DB test input EVENTS', file='data/journal_test/events_002.json')
        je.insert_in_db(truncate=True, no_delay=True)
        # Alerts
        ja = Journal('DB test input ALERTS', file='data/journal_test/alerts_002.json')
        ja.insert_in_db(truncate=False, no_delay=True)
        # Check events
        jedb = Journal('Read DB test EVENTS')
        jedb.select_from_db('event')
        self.assertTrue(je.deep_match(jedb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        #p rint je
        #p rint jedb
        # Check alerts
        jadb = Journal('Read DB test ALERTS')
        jadb.select_from_db('alert')
        self.assertTrue(ja.deep_match(jadb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        #p rint ja
        #p rint jadb
        self.teal.shutdown()
        return
    
    def testJournalWriteAlertDB2(self):
        ''' Test getting alerts without associations '''
        self.teal = Teal('data/journal_test/events_001.conf','stderr',msgLevel=self.msglevel)
        # Events
        je = Journal('DB test input EVENTS', file='data/journal_test/events_002.json')
        je.insert_in_db(truncate=True, no_delay=True)
        # Alerts
        ja = Journal('DB test input ALERTS', file='data/journal_test/alerts_002.json')
        ja.insert_in_db(truncate=False, no_delay=True)
        # Check alerts
        jadb = Journal('Read DB test ALERTS')
        jadb.select_from_db('alert', include_alert_assoc=False)
        jaexp = Journal('DB test expected', 'data/journal_test/alerts_003.json')
        self.assertTrue(jaexp.deep_match(jadb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        #p rint ja
        #p rint jadb
        self.teal.shutdown()
        return
    
    def testJournalWriteAlertDB3(self):
        ''' Test getting only some fields of an alert '''
        self.teal = Teal('data/journal_test/events_001.conf','stderr',msgLevel=self.msglevel)
        # Events
        je = Journal('DB test input EVENTS', file='data/journal_test/events_002.json')
        je.insert_in_db(truncate=True, no_delay=True)
        # Alerts
        ja = Journal('DB test input ALERTS', file='data/journal_test/alerts_002.json')
        ja.insert_in_db(truncate=False, no_delay=True)
        # Check alerts
        jadb = Journal('Read DB test ALERTS')
        jadb.select_from_db('alert', include_alert_assoc=False, alert_fields=[ALERT_ATTR_REC_ID, ALERT_ATTR_ALERT_ID, ALERT_ATTR_RECOMMENDATION])
        jaexp = Journal('DB test expected', 'data/journal_test/alerts_005.json')
        self.assertTrue(jaexp.deep_match(jadb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        #p rint ja
        #p rint jadb
        self.teal.shutdown()
        return
    
    def testJournalWriteAlertDB4(self):
        ''' Test writing of Alert log queue after reading from DB '''
        # This test does not work with duplicate checking -- probably don't want it to 
        keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'No')
        self.teal = Teal('data/journal_test/events_002.conf','stderr',msgLevel=self.msglevel)
        # Events
        je = Journal('DB test input EVENTS', file='data/journal_test/events_002.json')
        je.insert_in_db(truncate=True, no_delay=True)
        # Alerts
        ja = Journal('DB test input ALERTS', file='data/journal_test/alerts_002.json')
        ja.insert_in_db(truncate=False, no_delay=True)
        # Check events
        jedb = Journal('Read DB test EVENTS')
        jedb.select_from_db('event')
        self.assertTrue(je.deep_match(jedb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        # Check alerts
        jadb = Journal('Read DB test ALERTS')
        jadb.select_from_db('alert')
        self.assertTrue(ja.deep_match(jadb, ignore_delay=True, ignore_times=False, ignore_rec_id=False))
        # Now insert into the Delivery Queue and make sure all come out 
        jadb.inject_queue(get_service(SERVICE_ALERT_DELIVERY_Q), progress_cb=None, fail_on_invalid=False, no_delay=True)
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        self.assertTrue(j_out_all.wait_for_entries(6))
        self.assertTrue(j_out_all.deep_match(jadb, ignore_delay=True, ignore_times=True))
        self.teal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', keep_ADC)
        return


if __name__ == "__main__":
    unittest.main()
