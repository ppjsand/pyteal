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
 
import unittest
import time
from multiprocessing import Process

from ibm.teal import registry
from ibm.teal.database import db_interface
from ibm.teal import Teal
from ibm.teal.checkpoint_mgr import EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME,\
    EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA
import os
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.registry import SHUTDOWN_MODE_DEFERRED, SHUTDOWN_MODE_IMMEDIATE
from ibm.teal.teal import TEAL_SHUTDOWN_MODE, TEAL_RUN_MODE_HISTORIC
from ibm.teal.teal_error import TealError

def run_teal(msglevel, sleep_amount):
    teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=msglevel)
    time.sleep(sleep_amount)
    teal.shutdown()
    return

class TEALShutdownModeTest1(TealTestCase):
    ''' Test setting of shutdown mode works '''
    
    def setUp(self):
        self.t = Teal('data/tlcommands_test/test.conf', 'stderr', msgLevel=self.msglevel, data_only=True)  
          
    def tearDown(self):
        self.t.shutdown()
    
    def testDefaultShutdownMode(self):
        ''' Test that the shutdown mode correctly defaults '''  
        self.assertEqual(SHUTDOWN_MODE_DEFERRED, registry.get_service(registry.SERVICE_SHUTDOWN_MODE))


class TEALShutdownModeTest2(TealTestCase):
    ''' Test setting of shutdown mode works '''
    
    def setUp(self):
        self.keep_mode = self.force_env(TEAL_SHUTDOWN_MODE, SHUTDOWN_MODE_DEFERRED)
        self.t = Teal('data/tlcommands_test/test.conf', 'stderr', msgLevel=self.msglevel, data_only=True)  
          
    def tearDown(self):
        self.t.shutdown()
        self.restore_env(TEAL_SHUTDOWN_MODE, self.keep_mode)
    
    def testSettingDeferredShutdownMode(self):
        ''' Test that the shutdown mode being set to deferred works '''  
        self.assertEqual(SHUTDOWN_MODE_DEFERRED, registry.get_service(registry.SERVICE_SHUTDOWN_MODE))


class TEALShutdownModeTest3a(TealTestCase):
    ''' Test setting of shutdown mode works '''
    
    def setUp(self):
        self.keep_mode = self.force_env(TEAL_SHUTDOWN_MODE, SHUTDOWN_MODE_IMMEDIATE)
        self.t = Teal('data/tlcommands_test/test.conf', 'stderr', msgLevel=self.msglevel, data_only=True)  
          
    def tearDown(self):
        self.t.shutdown()
        self.restore_env(TEAL_SHUTDOWN_MODE, self.keep_mode)
    
    def testSettingImmediateShutdownMode(self):
        ''' Test that the shutdown mode to immediate works ENV '''  
        self.assertEqual(SHUTDOWN_MODE_IMMEDIATE, registry.get_service(registry.SERVICE_SHUTDOWN_MODE))


class TEALShutdownModeTest3b(TealTestCase):
    ''' Test setting of shutdown mode works '''
    
    def setUp(self):
        self.t = Teal('data/checkpoint_test/shutdown_immediate.conf', 'stderr', msgLevel=self.msglevel, data_only=True)  
          
    def tearDown(self):
        self.t.shutdown()
    
    def testSettingImmediateShutdownMode(self):
        ''' Test that the shutdown mode to immediate works config '''  
        self.assertEqual(SHUTDOWN_MODE_IMMEDIATE, registry.get_service(registry.SERVICE_SHUTDOWN_MODE))


class TEALShutdownModeTest4(TealTestCase):
    ''' Test setting of shutdown mode ignored '''
    
    def setUp(self):
        self.keep_mode = self.force_env(TEAL_SHUTDOWN_MODE, SHUTDOWN_MODE_IMMEDIATE)
        self.t = Teal('data/tlcommands_test/test.conf', 'stderr', msgLevel=self.msglevel, data_only=True, run_mode=TEAL_RUN_MODE_HISTORIC, commit_alerts=False)  
          
    def tearDown(self):
        self.t.shutdown()
        self.restore_env(TEAL_SHUTDOWN_MODE, self.keep_mode)
    
    def testSettingImmediateShutdownMode(self):
        ''' Test that the shutdown mode to immediate ignored if HISTORIC '''  
        self.assertEqual(SHUTDOWN_MODE_DEFERRED, registry.get_service(registry.SERVICE_SHUTDOWN_MODE))


class TEALShutdownModeTest5(TealTestCase):
    ''' Test setting of shutdown mode ignored '''
    
    def setUp(self):
        self.keep_mode = self.force_env(TEAL_SHUTDOWN_MODE, 'BAD_shutdown_mode_VALUE')
          
    def tearDown(self):
        self.restore_env(TEAL_SHUTDOWN_MODE, self.keep_mode)
    
    def testSettingImmediateShutdownMode(self):
        ''' Test that the shutdown mode being set to a bad value fails '''  
        self.assertRaisesTealError(TealError, "A value of 'BAD_shutdown_mode_VALUE' is not supported for environment variable 'TEAL_SHUTDOWN_MODE'", Teal, 'data/tlcommands_test/test.conf', 'stderr', self.msglevel,'now','realtime',False, False, None, False, '', False)


class TealCheckpointShutdownTest(TealTestCase):
    def setUp(self): 
        # Setup to use the tllsckpt command
        t = Teal('data/tlcommands_test/test.conf', 'stderr', msgLevel=self.msglevel, data_only=True)
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        self.tllsckpt = os.path.join(teal_path,'bin/tllsckpt')
        t.shutdown()
        
        self.prepare_db()
        
        # Need to have checkpointing to DB off so this doesn't interfer with the other instance of TEAL's checkpoints       
        self.teal = Teal('data/checkpoint_test/noop_monitor.conf','stderr',msgLevel=self.msglevel, commit_checkpoints=False)
        self.db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        self.query = self.db.gen_select(
                     [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                     db_interface.TABLE_CHECKPOINT)
        self.query_mon_data = self.db.gen_select([EVENT_CPF_DATA], db_interface.TABLE_CHECKPOINT, 
                                                 where="${0} = 'monitor_event_queue'".format(EVENT_CPF_NAME), where_fields=[EVENT_CPF_NAME])
        self.truncate = self.db.gen_truncate(db_interface.TABLE_CHECKPOINT)

    def tearDown(self):
        self.teal.shutdown()
        
    def testContolledShutdownClean(self):
        # Make sure the checkpoint table has no values
        cnxn = self.db.get_connection()
        cnxn.cursor().execute(self.truncate)
        cnxn.commit()
        
        # Start teal and let it shutdown gracefully
        tealp = Process(target=run_teal, args=(self.msglevel,1.0))
        tealp.start()
        tealp.join()
        
        # Now check the table to be sure we shut down cleanly
        cnxn = self.db.get_connection()
        cursor = cnxn.cursor()
        cursor.execute(self.query)
        
        row = cursor.fetchone()
        self.assertTrue(row)
        self.assertEqual(row[1],'Demo1Analyzer')
        self.assertEqual(row[2],'S')
        self.assertEqual(row[3], None)
        self.assertEqual(row[4], None)
        row = cursor.fetchone()
        self.assertTrue(row)
        self.assertEqual(row[1],'monitor_event_queue')
        self.assertEqual(row[2],'S')
        self.assertEqual(row[3], None)
        self.assertEqual(row[4], 'recovery None')
        row = cursor.fetchone()
        self.assertEqual(row, None)
        self.assertCmdWorks([self.tllsckpt], exp_good_msg='Demo1Analyzer        S  Nonemonitor_event_queue  S  NoneMAX_event_rec_id        None', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'brief'], exp_good_msg='Demo1Analyzer        S  Nonemonitor_event_queue  S  NoneMAX_event_rec_id        None', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'text'], 
                            exp_good_msg='==================================================='
                                       + 'name : Demo1Analyzer'
                                       + 'status : S'
                                       + 'event_recid : None'
                                       + 'data : None'
                                       + '==================================================='
                                       + 'name : monitor_event_queue'
                                       + 'status : S'
                                       + 'event_recid : None'
                                       + 'data : recovery None'
                                       + '==================================================='
                                       + 'name : MAX_event_rec_id'
                                       + 'status :  '
                                       + 'event_recid : None'
                                       + 'data :', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'json'], 
                            exp_good_msg='{"status": "S", "data": null, "name": "Demo1Analyzer", "event_recid": null}'
                                       + '{"status": "S", "data": "recovery None", "name": "monitor_event_queue", "event_recid": null}'
                                       + '{"status": " ", "data": "", "name": "MAX_event_rec_id", "event_recid": null}', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'csv'], exp_good_msg='Demo1Analyzer,S,,monitor_event_queue,S,,recovery NoneMAX_event_rec_id, ,,', exp_err_msg='', print_out=False)
        cnxn.close()
        return 
    
    def testControlledShutdownDirty(self):
        # Start TEAL and let it shutdown badly
        tealp = Process(target=run_teal, args=(self.msglevel,1000.0))
        tealp.start()
        try_times = 11
        time.sleep(10)
        while try_times > 0:
            time.sleep(1)
            cnxn = self.db.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(self.query_mon_data)
            row = cursor.fetchone()
            if row is not None:
                try_times = 0
            else:
                try_times -= 1
            #cnxn.close()  <<<< uncommenting changing the timing enough that it stops working!
        tealp.terminate()
        tealp.join()
        
        # Now check the table to be sure we shut down cleanly
        cnxn = self.db.get_connection()
        cursor = cnxn.cursor()
        cursor.execute(self.query)
        
        row = cursor.fetchone()
        self.assertEqual(row[1],'Demo1Analyzer')
        self.assertEqual(row[2],'R')
        self.assertEqual(row[3], None)
        self.assertEqual(row[4], None)
        row = cursor.fetchone()
        self.assertEqual(row[1],'monitor_event_queue')
        self.assertEqual(row[2],'R')
        self.assertEqual(row[3], None)
        self.assertEqual(row[4], 'recovery None')  
        row = cursor.fetchone()
        self.assertEqual(row, None)
        self.assertCmdWorks([self.tllsckpt], exp_good_msg='Demo1Analyzer        R  Nonemonitor_event_queue  R  NoneMAX_event_rec_id        None', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'brief'], exp_good_msg='Demo1Analyzer        R  Nonemonitor_event_queue  R  NoneMAX_event_rec_id        None', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'text'], 
                            exp_good_msg='==================================================='
                                       + 'name : Demo1Analyzer'
                                       + 'status : R'
                                       + 'event_recid : None'
                                       + 'data : None'
                                       + '==================================================='
                                       + 'name : monitor_event_queue'
                                       + 'status : R'
                                       + 'event_recid : None'
                                       + 'data : recovery None'
                                       + '==================================================='
                                       + 'name : MAX_event_rec_id'
                                       + 'status :  '
                                       + 'event_recid : None'
                                       + 'data :', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'json'], 
                            exp_good_msg='{"status": "R", "data": null, "name": "Demo1Analyzer", "event_recid": null}'
                                       + '{"status": "R", "data": "recovery None", "name": "monitor_event_queue", "event_recid": null}'
                                       + '{"status": " ", "data": "", "name": "MAX_event_rec_id", "event_recid": null}', exp_err_msg='', print_out=False)
        self.assertCmdWorks([self.tllsckpt, '-f', 'csv'], exp_good_msg='Demo1Analyzer,R,,monitor_event_queue,R,,recovery NoneMAX_event_rec_id, ,,', exp_err_msg='', print_out=False)
        cnxn.close()
        return 

    
if __name__ == "__main__":
    unittest.main()
