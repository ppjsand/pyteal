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

from multiprocessing import Process
from ibm.teal import Teal, registry
from ibm.teal.database import db_interface
from ibm.teal.registry import SERVICE_DB_INTERFACE, get_logger, get_service,\
    SERVICE_CHECKPOINT_MGR, SERVICE_ALERT_DELIVERY, SERVICE_ALERT_DELIVERY_Q
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.util.journal import Journal
import time
import unittest
from ibm.teal.checkpoint_mgr import EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME,\
    EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA,\
    get_current_min_checkpoint_rec_id
from ibm.teal.control_msg import inject_flush_control_msg
from datetime import datetime

class TealTestCheckpointEmptyDb(TealTestCase):
    '''Test the checkpoint support (not restart)''' 
    
    def setUp(self):
        '''Setup '''
        # Modify environment variable, so the tealtestdb is 
        # used rather than the regular db.
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        self.prepare_db()
        return
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        return    
    
    def testCheckpointEmptyDb(self):
        '''Test checkpoint value after inserting into an empty db.'''
        
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel='info')
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
        
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], None)
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
        _check_checkpoint(self, ckp_rows, expected)
        
        j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')

        try:
            j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        except:
            raise

        self.assertTrue(alj.wait_for_entries(4))
        #time.sleep(5)
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', max_id, '["2010-03-30 21:40:27.100000", "{0}", []]'.format(str(max_id))]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        # Shutdown to get pool closure
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # check the checkpoint
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 'Demo1Analyzer': ['S', None, None]}
        _check_checkpoint(self, ckp_rows, expected)
        cnxn.close()
        return
 
 
class TealTestCheckpointNonEmptyDb(TealTestCase):
    '''Test the checkpoint support (not restart)''' 
    
    def setUp(self):
        '''Setup Teal'''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        return
    
    def tearDown(self):
        '''Teardown teal'''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        return    
    
    def testCheckpointNonEmptyDb(self):
        '''Test checkpoint value after inserting into an non-empty db.'''
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel='info')
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
        
        # Make sure something is put into the database.
        j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')

        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        self.assertTrue(alj.wait_for_entries(4))
        #time.sleep(5)
        
        # Make sure the eventlog and checkpoint tables are not empty.
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', max_id, '["2010-03-30 21:40:27.100000", "{0}", []]'.format(str(max_id))]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        cnxn.close()

        # Insert the next series of events.
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        self.assertTrue(alj.wait_for_entries(8))
        #time.sleep(5)
        
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', max_id, '["2010-03-30 21:40:27.100000", "{0}", []]'.format(str(max_id))]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # check the checkpoint
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 'Demo1Analyzer': ['S', None, None]}
        _check_checkpoint(self, ckp_rows, expected)
        cnxn.close()
        return
     
     
class TealTestCheckpointGEARinFlight(TealTestCase):
    '''Test the checkpoint support when GEAR is in flight''' 
    
    def setUp(self):
        '''Setup Teal'''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        return
    
    def tearDown(self):
        '''Teardown teal'''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        return    
    
    def testCheckpointNonEmptyDb(self):
        '''Test checkpoint value after with GEAR in-flight'''
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel='info')
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
        
        # Make sure something is put into the database.
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_001.json')

        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        # Make sure the eventlog and checkpoint tables are not empty.
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)

        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(alj.wait_for_entries(4))
        #time.sleep(5)
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(max_id))]}
        _check_checkpoint(self, ckp_rows, expected)   
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        cnxn.close()
        keep_max_id = max_id 
         

        # Insert the next series of events.
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', keep_max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(keep_max_id))]}
        _check_checkpoint(self, ckp_rows, expected)   
        self.assertEqual(get_current_min_checkpoint_rec_id(), keep_max_id)
        
        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(alj.wait_for_entries(8))
        #time.sleep(5)
        
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(max_id))]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # check the checkpoint
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 'Demo1Analyzer': ['S', None, None]}
        _check_checkpoint(self, ckp_rows, expected)
        cnxn.close()
        return
    
    
class TealTestCheckpointGEARFailure(TealTestCase):
    '''Test the checkpoint support when GEAR is in flight''' 
    
    def setUp(self):
        '''Setup Teal'''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        return
    
    def tearDown(self):
        '''Teardown teal'''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        return    
    
    def testCheckpointNonEmptyDb(self):
        '''Test checkpoint value after with GEAR in-flight'''
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel='info')
        
        # Get the jounal from the listener 
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        # self.assertTrue(j_out_all.wait_for_entries(6))
        # self.assertTrue(j_out_all.deep_match(jadb, ignore_delay=True, ignore_times=True))
        
        # Make sure something is put into the database.
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_001.json')

        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        # Make sure the eventlog and checkpoint tables are not empty.
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)

        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(j_out_all.wait_for_entries(4))
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(max_id))]}
        _check_checkpoint(self, ckp_rows, expected)  
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        cnxn.close()
        keep_max_id = max_id 
         

        # Insert the next series of events.   This one will cause the Analyzer to fail
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_002.json')
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        # Check the status of the checkpoint table.
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['R', keep_max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(keep_max_id))]}
        _check_checkpoint(self, ckp_rows, expected)   
        self.assertEqual(get_current_min_checkpoint_rec_id(), keep_max_id)

        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        # Because of failure, don't know how many to wait for
        # Cannot: self.assertTrue(j_out_all.wait_for_entries(8))
        time.sleep(5)

        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # get rec id info 
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        max_id = rows[0][0]
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 'Demo1Analyzer': ['F', keep_max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(keep_max_id))]}
        _check_checkpoint(self, ckp_rows, expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), keep_max_id)
        
        self.teal.shutdown()
        # Get checkpoint info
        dbi.select(cursor, 
                   [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                   db_interface.TABLE_CHECKPOINT)
        ckp_rows = cursor.fetchall()
        # check the checkpoint
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 'Demo1Analyzer': ['F', keep_max_id, '["2010-03-31 11:07:43.100000", "{0}", []]'.format(str(keep_max_id))]}
        _check_checkpoint(self, ckp_rows, expected)
        
        cnxn.close()
        return
    

class TealTestCheckpointGEARFailureRestart(TealTestCase):
    '''Test the checkpoint support when GEAR is in flight and restart''' 
    
    def setUp(self):
        '''Setup '''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        return
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        return  
    
    def run_teal_first(self):
        teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel='info')
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_001.json')
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        self.assertTrue(j_out_all.wait_for_entries(4))
        
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(40)
        teal.shutdown()
        return      
    
    def testCheckpointGEARrestart(self):
        '''Test restart of GEAR after failure '''
        tealp = Process(target=self.run_teal_first)
        tealp.start()
        time.sleep(20)
        tealp.terminate()
        tealp.join()
        
        # Now restart and make sure we 
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel='info', restart='recovery')
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(j_out_all.wait_for_entries(4))
        
        self.teal.shutdown()
        return
    
def _check_checkpoint(tc, rows, expected_dict):
    ''' Check the checkpoint against the expected dictionary
    where it contains name -> [status, mcp_rec_id, data]
    '''
    try:
        tc.assertEqual(len(rows), len(expected_dict))
        for ckpt_rec_id, name, status, cpd_rec_id, data in rows:
            try:
                tc.assertTrue(name in expected_dict.keys())
                e_status, e_cpd_rec_id, e_data = expected_dict[name]
                tc.assertEqual(e_status, status)
                tc.assertEqual(e_cpd_rec_id, cpd_rec_id)
                tc.assertEqual(e_data, data)
            except:
                print 'checking: {0}'.format(name)
                raise
    except:
        print 'rows:    {0}'.format(str(rows))
        print 'expect:  {0}'.format(str(expected_dict))
        print str(get_service(SERVICE_CHECKPOINT_MGR))
        raise
    return


if __name__ == "__main__":
    unittest.main()

