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
from ibm.teal.alert import ALERT_STATE_INCOMPLETE, ALERT_STATE_OPEN,\
    ALERT_STATE_CLOSED, create_teal_alert
from ibm.teal.util.journal import Journal
from ibm.teal.util.listenable_queue import ListenableQueue, QueueListener
import multiprocessing
from ibm.teal.database import db_interface
from ibm.teal.test.teal_unittest import TealTestCase, unittest

from ibm.teal import Teal
from ibm.teal.registry import SERVICE_ALERT_MGR, get_service,\
    SERVICE_DB_INTERFACE
from ibm.teal.alert_mgr import AlertMgrError
import sys

class AlertTestBasic(TealTestCase):
    
    def setUp(self):
        self.teal = Teal('data/common/configurationtest.conf','stderr',msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
          
    def tearDown(self):
        '''Nothing to do ... yet
        '''
        self.teal.shutdown()
 
    def testAlertRawDataDict(self):
        ''' test the raw data dictionary support '''
        t_alert = get_service(SERVICE_ALERT_MGR).allocate('TestAlert', {})
        # Test with no raw data
        t_dictO = t_alert.get_raw_data_as_dict()
        self.assertEquals(t_alert.raw_data, None)
        self.assertEquals(len(t_dictO), 1)
        self.assertTrue('non_dict_raw_data' in t_dictO)
        self.assertEquals(t_dictO['non_dict_raw_data'], None)
        t_dictO = None
        # Set raw data to a value 
        t_alert.raw_data = 'stuff'
        t_dict0 = t_alert.get_raw_data_as_dict()
        self.assertEquals(t_alert.raw_data, 'stuff')
        self.assertEquals(len(t_dict0), 1)
        self.assertTrue('non_dict_raw_data' in t_dict0)
        self.assertEquals(t_dict0['non_dict_raw_data'], 'stuff')
        t_dict0['k1'] = 'v1'
        t_alert.set_raw_data_from_dict(t_dict0)
        self.assertEquals(t_alert.raw_data, '{"k1":"v1"}stuff')
        t_dict2 = t_alert.get_raw_data_as_dict()
        self.assertEquals(len(t_dict2), 2)
        self.assertTrue('non_dict_raw_data' in t_dict2)
        self.assertEquals(t_dict2['non_dict_raw_data'], 'stuff')
        self.assertTrue('k1' in t_dict2)
        self.assertEquals(t_dict2['k1'], 'v1')
        t_dict2 = None
        t_dict0['k2'] = 'v2'
        t_alert.set_raw_data_from_dict(t_dict0)
        self.assertEquals(t_alert.raw_data, '{"k2":"v2","k1":"v1"}stuff')
        t_dict2 = t_alert.get_raw_data_as_dict()
        self.assertEquals(len(t_dict2), 3)
        self.assertTrue('non_dict_raw_data' in t_dict2)
        self.assertEquals(t_dict2['non_dict_raw_data'], 'stuff')
        self.assertTrue('k1' in t_dict2)
        self.assertEquals(t_dict2['k1'], 'v1')
        self.assertTrue('k2' in t_dict2)
        self.assertEquals(t_dict2['k2'], 'v2')
        t_dict0 = {'key1':'value1','key3':'value3'}
        t_alert.raw_data = None
        t_dictO = t_alert.get_raw_data_as_dict()
        self.assertEquals(t_alert.raw_data, None)
        self.assertEquals(len(t_dictO), 1)
        self.assertTrue('non_dict_raw_data' in t_dictO)
        self.assertEquals(t_dictO['non_dict_raw_data'], None)
        t_dictO = None
        t_alert.set_raw_data_from_dict(t_dict0)
        self.assertEquals(t_alert.raw_data, '{"key3":"value3","key1":"value1"}')
        t_dict2 = t_alert.get_raw_data_as_dict()
        self.assertEquals(len(t_dict2), 2)
        self.assertTrue('non_dict_raw_data' not in t_dict2)
        self.assertTrue('key1' in t_dict2)
        self.assertEquals(t_dict2['key1'], 'value1')
        self.assertTrue('key3' in t_dict2)
        self.assertEquals(t_dict2['key3'], 'value3') 
        t_dict0 = {'non_dict_raw_data':'when in the course'} 
        t_alert.set_raw_data_from_dict(t_dict0) 
        self.assertEquals(t_alert.raw_data, 'when in the course')
        # Bug test
        t_alert.raw_data = '{"fru_list":"{HFI_DDG,Isolation Procedure,,,},{HFI_CAB,Symbolic Procedure,Uf.i.s-P1-T11-T3,,},{CABCONT,Symbolic Procedure,Uf.i.s-P1-T11-T3,,},{47K1234,FRU,Ug.h.t-P1-R2, 47K1234,YL55555,ABC123,TRMD},{47K1234,FRU,Uf.i.s-P1-R3,47K1234,YL12345,ABC123,TRMD},"}'
        n_dict = t_alert.get_raw_data_as_dict()
        
        return
    

class CheckAlertStateListener(QueueListener):
    ''' check the state of the alert called with '''
    
    def __init__(self, max_count):
        self.count = 0
        self.max_count = max_count
        self.my_event = multiprocessing.Event()
        self.alerts = []
        return
    
    def get_name(self):
        ''' '''
        return 'CheckAlertStateListener'
    
    def notify(self, item):
        ''' check state is new '''
        self.alerts.append(item)
        if item.state == ALERT_STATE_OPEN:
            self.count += 1
            if self.count == self.max_count:
                self.my_event.set()
            return True
        self.my_event.set()
        return True
        
    
class AlertTestStates(TealTestCase):
    
    def testStateIncompleteIM(self):
        ''' Test alert gets created in memory in incomplete state'''
        self.teal = Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        am = get_service(SERVICE_ALERT_MGR)
        t_alert = am.allocate('TestAlert', {})
        self.assertEquals(t_alert.state, ALERT_STATE_INCOMPLETE)
        # No metadata
        self.assertRaises(KeyError, am.commit, t_alert)
        self.teal.shutdown()
        
    def testStateIncompleteDB(self):
        ''' Test alert gets created in memory in incomplete state'''
        self.teal = Teal('data/alert_test/test.conf', 'stderr', msgLevel='debug', commit_alerts=True, commit_checkpoints=False)
        am = get_service(SERVICE_ALERT_MGR)
        t_alert = am.allocate('TestAlert', {})
        self.assertEquals(t_alert.state, ALERT_STATE_INCOMPLETE)
        # No metadata
        self.assertRaises(KeyError, am.commit, t_alert)
        self.teal.shutdown()

    def testStateOtherStatesIM(self):
        '''test alert state NEW in memory'''
        self.teal = Teal('data/alert_test/test.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)

        j_in_dq = Journal('j_in_DQ', 'data/alert_test/inject_DQ_alerts.json')
        tq = ListenableQueue('test LQ')
        ql = CheckAlertStateListener(7)
        tq.register_listener(ql)
        j_in_dq.inject_queue(tq, progress_cb=None, fail_on_invalid=False, no_delay=True)
        ql.my_event.wait()
        self.assertEquals(ql.count, 7)
        ta1 = ql.alerts[0]
        am = get_service(SERVICE_ALERT_MGR)
        # TODO: Should not be hardcoded rec ids after this 
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.close, 5)
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.close, 6)
        self.assertRaisesTealError(AlertMgrError, 'Current alert state does not allow this operation', am.reopen, ta1.rec_id)
        am.close(ta1.rec_id)
        self.assertEquals(ta1.state, ALERT_STATE_CLOSED)
        self.assertRaisesTealError(AlertMgrError, 'Current alert state does not allow this operation', am.close, ta1.rec_id)
        self.assertRaisesTealError(AlertMgrError, 'Alert with specified record id not found', am.close, 23456)
        self.assertEquals(ql.alerts[1].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[2].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[3].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[4].state, ALERT_STATE_CLOSED)
        self.assertEquals(ql.alerts[5].state, ALERT_STATE_CLOSED)
        self.assertEquals(ql.alerts[6].state, ALERT_STATE_OPEN)
        # reopen it 
        self.assertRaisesTealError(AlertMgrError, 'Alert with specified record id not found', am.reopen, 23456)
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.reopen, 5)
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.reopen, 6)
        am.reopen(ta1.rec_id)
        self.assertEquals(ta1.state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[1].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[2].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[3].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[4].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[5].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[6].state, ALERT_STATE_OPEN)
        am.close(3)
        self.assertEquals(ta1.state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[1].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[2].state, ALERT_STATE_CLOSED)
        self.assertEquals(ql.alerts[3].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[4].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[5].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[6].state, ALERT_STATE_OPEN)
        am.reopen(3)
        self.assertEquals(ta1.state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[1].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[2].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[3].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[4].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[5].state, ALERT_STATE_OPEN)
        self.assertEquals(ql.alerts[6].state, ALERT_STATE_OPEN)
        self.teal.shutdown()
        return
    
    def testStateOtherStatesDB(self):
        '''test alert state NEW in memory'''
        self.prepare_db()
        self.teal = Teal('data/alert_test/test.conf', 'stderr', msgLevel='debug', commit_alerts=True, commit_checkpoints=False)

        j_in_dq = Journal('j_in_DQ', 'data/alert_test/inject_DQ_alerts.json')
        tq = ListenableQueue('test LQ')
        ql = CheckAlertStateListener(7)
        tq.register_listener(ql)
        j_in_dq.inject_queue(tq, progress_cb=None, fail_on_invalid=False, no_delay=True)
        ql.my_event.wait()
        self.assertEquals(ql.count, 7)
        ta1 = ql.alerts[0]
        am = get_service(SERVICE_ALERT_MGR)
        self.assertEquals(ta1.state, ALERT_STATE_OPEN)
        # TODO: Really should query to get the recid to use for hardcoded ones in rest of this test case
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.close, 5)
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.close, 6)
        self.assertRaisesTealError(AlertMgrError, 'Current alert state does not allow this operation', am.reopen, ta1.rec_id)
        am.close(ta1.rec_id)
        # Get duplicates of this one        
        self.assertRaisesTealError(AlertMgrError, 'Current alert state does not allow this operation', am.close, ta1.rec_id)
        self.assertRaisesTealError(AlertMgrError, 'Alert with specified record id not found', am.close, 23456)
        # Note that in memory won't be updated ... only in DB
        # so lets get it from the DB
        dbi = get_service(SERVICE_DB_INTERFACE)
        event_cnxn, cursor =_get_connection(dbi)
        self.assert_alert_closed(dbi, cursor, ta1.rec_id)
        self.assert_alert_open(dbi, cursor, 2)
        self.assert_alert_open(dbi, cursor, 3)
        self.assert_alert_open(dbi, cursor, 4)
        self.assert_alert_closed(dbi, cursor, 5)
        self.assert_alert_closed(dbi, cursor, 6)
        self.assert_alert_open(dbi, cursor, 7)
        self.assertRaisesTealError(AlertMgrError, 'Alert with specified record id not found', am.reopen, 23456)
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.reopen, 5)
        self.assertRaisesTealError(AlertMgrError, 'Operation not allowed on duplicate alert', am.reopen, 6)
        # reopen it 
        am.reopen(ta1.rec_id)
        event_cnxn, cursor =_get_connection(dbi, event_cnxn)
        self.assert_alert_open(dbi, cursor, ta1.rec_id)
        self.assert_alert_open(dbi, cursor, 2)
        self.assert_alert_open(dbi, cursor, 3)
        self.assert_alert_open(dbi, cursor, 4)
        self.assert_alert_open(dbi, cursor, 5)
        self.assert_alert_open(dbi, cursor, 6)
        self.assert_alert_open(dbi, cursor, 7)
        am.close(3)
        event_cnxn, cursor =_get_connection(dbi, event_cnxn)
        self.assert_alert_open(dbi, cursor, ta1.rec_id)
        self.assert_alert_open(dbi, cursor, 2)
        self.assert_alert_closed(dbi, cursor, 3)
        self.assert_alert_open(dbi, cursor, 4)
        self.assert_alert_open(dbi, cursor, 5)
        self.assert_alert_open(dbi, cursor, 6)
        self.assert_alert_open(dbi, cursor, 7)
        am.reopen(3)
        event_cnxn, cursor =_get_connection(dbi, event_cnxn)
        self.assert_alert_open(dbi, cursor, ta1.rec_id)
        self.assert_alert_open(dbi, cursor, 2)
        self.assert_alert_open(dbi, cursor, 3)
        self.assert_alert_open(dbi, cursor, 4)
        self.assert_alert_open(dbi, cursor, 5)
        self.assert_alert_open(dbi, cursor, 6)
        self.assert_alert_open(dbi, cursor, 7)
        event_cnxn.close()
        self.teal.shutdown()
        return
    
    def assert_alert_closed(self, dbi, cursor, rec_id):
        ''' Check that the alert for the specified rec_id is closed '''
        dbi.select(cursor, ['state'], db_interface.TABLE_ALERT_LOG, where='$rec_id = ?', where_fields=['rec_id'], parms=(rec_id,))
        row = cursor.fetchone()
        self.assertTrue(row != None)
        self.assertTrue(row[0] != None)
        self.assertEquals(row[0],ALERT_STATE_CLOSED)
        return 
    
    def assert_alert_open(self, dbi, cursor, rec_id):
        ''' Check that the alert for the specified rec_id is closed '''
        dbi.select(cursor, ['state'], db_interface.TABLE_ALERT_LOG, where='$rec_id = ?', where_fields=['rec_id'], parms=(rec_id,))
        row = cursor.fetchone()
        self.assertTrue(row != None)
        self.assertTrue(row[0] != None)
        self.assertEquals(row[0],ALERT_STATE_OPEN)
        return 
    
    # Other states 
    #     ALERT_STATE_FILTERED and ALERT_STATE_REPORTED are tested by alert_delivery_test.py
    #
    #     ALERT_STATE_PASSED is not used
    # 
    
    
class AlertTestDuplicateSupport(TealTestCase):
    
    def testDisableDup(self):
        ''' Test That disable dup works'''
        self.teal = Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        am = get_service(SERVICE_ALERT_MGR)
        self.assertEqual(len(am.in_mem_alerts), 0)
        self.assertEqual(len(am.in_mem_alerts_duplicate), 0)
        self.assertEqual(len(am.active_alerts_open), 0)
        create_teal_alert('XXXXXXXX', 'no reason at all', 'medium well', loc_instance="YYY")
        self.assertEqual(len(am.in_mem_alerts), 1)
        self.assertEqual(len(am.in_mem_alerts_duplicate), 0)
        self.assertEqual(len(am.active_alerts_open), 1)
        create_teal_alert('XXXXXXXX', 'no reason at all', 'medium well', loc_instance="YYY")
        self.assertEqual(len(am.in_mem_alerts), 2)
        self.assertEqual(len(am.in_mem_alerts_duplicate), 1)
        self.assertEqual(len(am.active_alerts_open), 1)
        create_teal_alert('XXXXXXXX', 'no reason at all', 'medium well', loc_instance="YYY", disable_dup=True)
        self.assertEqual(len(am.in_mem_alerts), 3)
        self.assertEqual(len(am.in_mem_alerts_duplicate), 1)
        self.assertEqual(len(am.active_alerts_open), 2)
        create_teal_alert('XXXXXXXX', 'no reason at all', 'medium well', loc_instance="YYY", disable_dup=True)
        self.assertEqual(len(am.in_mem_alerts), 4)
        self.assertEqual(len(am.in_mem_alerts_duplicate), 1)
        self.assertEqual(len(am.active_alerts_open), 3)
        create_teal_alert('XXXXXXXX', 'no reason at all', 'medium well', loc_instance="YYY")
        self.assertEqual(len(am.in_mem_alerts), 5)
        self.assertEqual(len(am.in_mem_alerts_duplicate), 2)
        self.assertEqual(len(am.active_alerts_open), 3)
        self.teal.shutdown()
        return
  
# Helpers

def _get_connection(dbi, old_cnxn=None): 
    if old_cnxn is not None:
            old_cnxn.close()
    event_cnxn = dbi.get_connection() 
    cursor = event_cnxn.cursor()
    return (event_cnxn, cursor)

if __name__ == "__main__":
    unittest.main()