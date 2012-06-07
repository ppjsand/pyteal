# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010, 2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import json
from multiprocessing import Process, Queue
from ibm.teal import Teal, registry
from ibm.teal.event import Event
from ibm.teal.database import db_interface
from ibm.teal.registry import SERVICE_DB_INTERFACE, get_service,\
    SERVICE_CHECKPOINT_MGR, SERVICE_ALERT_DELIVERY, SERVICE_ALERT_DELIVERY_Q,\
    SERVICE_EVENT_Q, get_logger, SERVICE_EVENT_MONITOR, SERVICE_ALERT_ANALYZER_Q
from ibm.teal.test.teal_unittest import TealTestCase,\
    get_table_date_time_pattern, apply_time_pattern
from ibm.teal.util.journal import Journal
import time
import unittest
from ibm.teal.checkpoint_mgr import EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME,\
    EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA,\
    get_current_min_checkpoint_rec_id
from ibm.teal.control_msg import inject_flush_control_msg, ControlMsg,\
    CONTROL_MSG_TYPE_FLUSH, inject_update_checkpoint_msg
from datetime import datetime
from ibm.teal.monitor.realtime_monitor import RealtimeMonitor
from ibm.teal.analyzer.analyzer import EventAnalyzer
import sys

MONITOR_CONTROL_PROCESS_ONE_EVENT = 1
MONITOR_CONTROL_PROCESS_ALL_EVENTS = 3
MONITOR_CONTROL_WAIT_ON_NOTIFY = 2 

class SteppableRealTimeMonitor(RealtimeMonitor):
    ''' This defines a realtime monitor subclass that can be controlled via a command queue ''' 
    
    def __init__(self, config_dict):
        self.control_q = Queue()
        RealtimeMonitor.__init__(self, config_dict)
        
    def start(self):
        '''Start the notifier-based event monitor running.
        '''
        event_queue =  registry.get_service(SERVICE_EVENT_Q)
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        next_failure_log = None
        
        while self.running:
            ctl = self.control_q.get()
            if ctl == MONITOR_CONTROL_WAIT_ON_NOTIFY:
                self.notifier.wait()
            elif ctl == MONITOR_CONTROL_PROCESS_ONE_EVENT or ctl == MONITOR_CONTROL_PROCESS_ALL_EVENTS:
                # Process just one of the events (but do the full query) ... or all depending on ctl message
                get_logger().debug('Processing events in monitor event injection thread. startRecid = {0}'.format(self.start_recid))
                try:
                    cnxn = dbi.get_connection()
                    cursor = cnxn.cursor()
                    for row in cursor.execute(self.sql_runtime_query, self.start_recid):
                        get_logger().debug('Processing row, rec_id = {0} time_occurred = {1}, time_logged = {2}'.format(row[0], row[2],row[3]))
                        e = Event.fromDB(row);
                        event_queue.put(e)
                        self.start_recid = row[0] 
#                        if self.running == False: 
#                            get_logger().info('Monitor event injection thread interrupted.  last recid = {0}'.format(self.start_recid))
#                            break 
                        if self.start_recid % self.update_checkpoint_frequency == 0:
                            get_logger().debug('Updating checkpoints at rec_id = {0}'.format(self.start_recid))
                            inject_update_checkpoint_msg(self.start_recid)
                        if ctl == MONITOR_CONTROL_PROCESS_ONE_EVENT:
                            break # ONLY DO ONE
                    cnxn.close()
                except:
                    cur_time = datetime.now()
                    if next_failure_log is None or  cur_time > next_failure_log:
                        get_logger().exception('Failure in monitor event injection thread')
                        next_failure_log = cur_time + datetime.timedelta(minutes=10)
#            rc = self.notifier.wait()
        get_logger().debug('Exiting monitor event injection thread.  Last recid = {0}'.format(self.start_recid))    


class TestEventAnalyzerEventCapture(EventAnalyzer):
    ''' Event analyzer that simply captures the events it processed. It does not produce alerts ''' 
    
    def __init__(self, name, inEventQueue, outQueue, config_dict=None, number=0, checkpoint=None):
        ''' setup new attributes and call parent '''
        self.list_of_events = []
        self.list_of_ctl_msgs = []
        self.last_rec_id = None 
        self.ckpt_frequency = 2
        if config_dict is not None and 'ckpt_frequency' in config_dict:
            self.ckpt_frequency = config_dict['ckpt_frequency']
        EventAnalyzer.__init__(self, name, inEventQueue, outQueue, config_dict, number, checkpoint)

    def will_analyze_event(self, event):
        ''' Always analyze event '''
        return True
    
    def analyze_event(self, event):
        ''' keep track of events '''
        self.list_of_events.append(event)
        self.last_rec_id = event.rec_id
        
    def base_analyze_event_CHECKPOINT(self, event):
        ''' Add checkpointing after analyze event'''
        self.analyze_event(event)
        if self.last_rec_id % self.ckpt_frequency == 0:  # only checkpoint at specified frequency
            self.checkpoint.set_checkpoint(event.rec_id)
            
    def handle_control_msg(self, control_msg):
        ''' No additions '''
        self.list_of_ctl_msgs.append(control_msg)
    
    
class TestEventAnalyzerDelay(EventAnalyzer):
    ''' Test event analyzer that will delay when it gets a specified event for the specified amount of time '''
    
    def __init__(self, name, inEventQueue, outQueue, config_dict=None, number=0, checkpoint=None):
        ''' setup new attributes and call parent '''
        #print config_dict
        self.list_of_events = []
        self.last_rec_id = None
        analyze_event_ids_str = config_dict.get('analyze_event_ids', '')
        self.analyze_event_ids = analyze_event_ids_str.split(',')
        #print self.analyze_event_ids
        delay_event_ids_str = config_dict.get('delay_event_ids', '')
        self.delay_event_ids = delay_event_ids_str.split(',')
        #print self.delay_event_ids
        self.delay_amount = config_dict.get('delay_amount', 30)
        #print self.delay_amount 
        EventAnalyzer.__init__(self, name, inEventQueue, outQueue, config_dict, number, checkpoint)

    def will_analyze_event(self, event):
        ''' Always analyze event '''
        #print 'analyze checking ' + event.event_id + '  against  ' + str(self.analyze_event_ids)
        #print self.name + '  ' + event.brief_str() + ' ? ' + str(event.event_id in self.analyze_event_ids)
        return event.event_id in self.analyze_event_ids
    
    def analyze_event(self, event):
        ''' keep track of events '''
        self.list_of_events.append(event)
        self.last_rec_id = event.rec_id
        #print 'delay checking ' + event.event_id + '  against  ' + str(self.delay_event_ids)
        #print event.event_id in self.delay_event_ids
        if event.event_id in self.delay_event_ids:
            print 'delaying ' + event.brief_str() + ' for ' + str(self.delay_amount)
            time.sleep(float(self.delay_amount))
            print 'delay completed'
                    
    def handle_control_msg(self, control_msg):
        ''' No additions '''
        pass


class BaseTestCheckpoint(TealTestCase):

    def _get_max_event(self):
        ''' Helper to get the max event rec id '''
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        dbi.select_max(cursor, 'rec_id',db_interface.TABLE_EVENT_LOG)
        rows = cursor.fetchall()
        cnxn.close()
        # get_logger().info('Length of max(rec_id) return: {0}'.format(len(rows)))
        self.assertEqual(len(rows), 1)
        return rows[0][0]
    
    def _force_checkpoint(self, force_dict):
        ''' Force the checkpoint table to the values in the force_dict 
        
            Note that any events rec_ids referenced must already exist in the event log 
        ''' 
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        # Truncate the checkpoint table 
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        dbi.truncate(cursor, db_interface.TABLE_CHECKPOINT)
        cnxn.commit()
        
        CKPT_INSERT = dbi.gen_insert(
                [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                db_interface.TABLE_CHECKPOINT)
        new_rec_id = 0
        for name, entry in force_dict.items():
            new_rec_id += 1 
            cursor.execute(CKPT_INSERT, (new_rec_id, name, entry[0], entry[1], entry[2]))
        cnxn.commit()
        cnxn.close()
    
    def _check_checkpoint(self, rows, expected_dict, noisy=True, only_names=None, GEAR_delta=0):
        ''' Check the checkpoint against the expected dictionary
        where it contains name -> [status, mcp_rec_id, data]
        '''
        try:
            self.assertEqual(len(rows), len(expected_dict))
            for ckpt_rec_id, name, status, cpd_rec_id, data in rows:
                try:
                    if only_names is None or name in only_names: 
                        self.assertTrue(name in expected_dict.keys())
                        e_status, e_cpd_rec_id, e_data = expected_dict[name]
                        self.assertEqual(e_status, status)
                        self.assertEqual(e_cpd_rec_id, cpd_rec_id)
                        if GEAR_delta != 0 and e_data != data and e_data[0] == '[':
                            data_l = json.loads(data)
                            e_data_l = json.loads(e_data)
                            self.assertEqual(len(data_l), len(e_data_l))
                            for i in xrange(1,len(data_l)-1):
                                self.assertEqual(data_l[i], e_data_l[i])
                            a_time = datetime.strptime(json.loads(data)[0], '%Y-%m-%d %H:%M:%S.%f')
                            e_time = datetime.strptime(json.loads(e_data)[0], '%Y-%m-%d %H:%M:%S.%f')
                            time_delta = abs(a_time - e_time).seconds
                            if time_delta > GEAR_delta:
                                self.assertEqual(e_data, data)
                            if time_delta > 0:
                                get_logger().warning('Passing because GEAR delta of {0} was less then limit of {1}'.format(str(time_delta),str(GEAR_delta)))
                        else:
                            self.assertEqual(e_data, data)
                except:
                    if noisy:
                        print 'checking: {0}({1})'.format(name, str(ckpt_rec_id))
                    raise
        except:
            if noisy:
                print 'interspersed entries:'
                key_list_exp = expected_dict.keys()
                for row in rows:
                    print '    row:    {0}'.format(row)
                    t_name = row[1]
                    if t_name in key_list_exp:
                        print '    exp:         \'{0}\':{1}'.format(t_name, expected_dict[t_name])
                        key_list_exp.remove(t_name)
                    else:
                        print '    exp:    <no match>'
                for key, value in key_list_exp: 
                    print '    row:    <no match>'
                    print '    exp:         \'{0}\':{1}'.format(key, value)
                print str(get_service(SERVICE_CHECKPOINT_MGR))
            raise
    
    def _wait_for_checkpoint(self, expected_dict, in_tries=None, dbi=None, only_names=None, GEAR_delta=0):
        if in_tries is None:
            tries = 9
        else:
            tries = in_tries
            
        if dbi is None:
            dbi = registry.get_service(SERVICE_DB_INTERFACE)

        match = False
        while tries > 0:
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            # Get checkpoint info
            dbi.select(cursor, 
                       [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                       db_interface.TABLE_CHECKPOINT)
            ckp_rows = cursor.fetchall()
            cnxn.close()
            # check the checkpoint
            try:
                self._check_checkpoint(ckp_rows, expected_dict, noisy=False, only_names=only_names, GEAR_delta=GEAR_delta)
                match = True
                break
            except:
                pass
            time.sleep(0)
            time.sleep(1)
            tries -= 1 
        if match == False:
            self._check_checkpoint(ckp_rows, expected_dict, noisy=True, only_names=only_names, GEAR_delta=GEAR_delta)


class TealTestCheckpoint(BaseTestCheckpoint):
    '''Test the checkpoint support (not restart)''' 
    
    def setUp(self):
        '''Setup '''
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        self.prepare_db()
        self.time_pattern = get_table_date_time_pattern()
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        if self.teal is not None:
            try:
                self.teal.shutdown()
            except:
                pass
    
    def testCheckpointEmptyDb(self):
        '''Test checkpoint value after inserting into an empty db.'''
        
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=self.msglevel)
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
              
        self.assertEqual(self._get_max_event(), None)
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        
        j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)

        self.assertTrue(alj.wait_for_entries(4))
        
        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-30 21:40:27.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        
        # Shutdown to get pool closure
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['S', max_id, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
 
    def testCheckpointNonEmptyDb(self):
        '''Test checkpoint value after inserting into an non-empty db.'''
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=self.msglevel)
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
        
        # Make sure something is put into the database.
        j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')

        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        self.assertTrue(alj.wait_for_entries(4))
        
        # Make sure the eventlog and checkpoint tables are not empty.
        # Check the status of the checkpoint table.
        max_id = self._get_max_event()
        # check the checkpoint
        tmp_dts = apply_time_pattern(['2010-03-30 21:40:27.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)

        # Insert the next series of events.
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        self.assertTrue(alj.wait_for_entries(8))
        #time.sleep(5)
        
        # Check the status of the checkpoint table.
        max_id = self._get_max_event()
        # check the checkpoint
        tmp_dts = apply_time_pattern(['2010-03-30 21:40:27.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['S', max_id, None]}
        self._wait_for_checkpoint(expected )
        self.teal.shutdown()

    def testCheckpointInFlight(self):
        '''Test checkpoint value after with GEAR in-flight'''
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel=self.msglevel)
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
        
        # Make sure something is put into the database.
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_001.json')
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        # Make sure the eventlog and checkpoint tables are not empty.
        max_id = self._get_max_event()
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)

        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(alj.wait_for_entries(4, seconds=60))

        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self._wait_for_checkpoint(expected)   
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        keep_max_id = max_id 

        # Insert the next series of events.
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', keep_max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(keep_max_id))]}
        self._wait_for_checkpoint(expected)   
        self.assertEqual(get_current_min_checkpoint_rec_id(), keep_max_id)
        
        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(alj.wait_for_entries(8, seconds=60))
        
        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self._wait_for_checkpoint(expected)   
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['S', max_id, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
    
    def testCheckpointInflight2(self):
        '''Test checkpoint value after with GEAR in-flight'''
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel=self.msglevel)
        
        # Get the jounal from the listener 
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        
        # Make sure something is put into the database.
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_001.json')

        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        # Make sure the eventlog and checkpoint tables are not empty.
        max_id = self._get_max_event()
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)

        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(j_out_all.wait_for_entries(4, seconds=60))
        
        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
        keep_max_id = max_id 

        # Insert the next series of events.   This one will cause the Analyzer to fail
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_002.json')
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        time.sleep(5)
        
        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', keep_max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(keep_max_id))]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), keep_max_id)

        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        # Because of failure, don't know how many to wait for so can't use wait_for_entries(8)
        time.sleep(5)

        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['F', keep_max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(keep_max_id))]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), keep_max_id)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        tmp_dts = apply_time_pattern(['2010-03-31 11:07:43.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['F', keep_max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(keep_max_id))]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
    def testCheckpointInactiveCkpts(self):
        '''Test checkpoint value after with GEAR in-flight'''
        
        # Start with three analyzers (1, 2, 3) 
        self.teal = Teal('data/checkpoint_test/inactive_test_3.conf', 'stderr', msgLevel=self.msglevel)
                
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 
                    'Analyzer1': ['R', None, None], 
                    'Analyzer2': ['R', None, None], 
                    'Analyzer3': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/inactive_test_3.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', None, 'recovery None'], 
                    'Analyzer1': ['S', None, None], 
                    'Analyzer2': ['S', None, None], 
                    'Analyzer3': ['S', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Restart with two analyzers (3, 5)
        self.teal = Teal('data/checkpoint_test/inactive_test_4.conf', 'stderr', msgLevel=self.msglevel)
                
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 
                    'Analyzer3': ['R', None, None], 
                    'Analyzer5': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/inactive_test_4.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', None, 'recovery None'], 
                    'Analyzer3': ['S', None, None], 
                    'Analyzer5': ['S', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Restart with one analyzer (2)
        self.teal = Teal('data/checkpoint_test/inactive_test_1.conf', 'stderr', msgLevel=self.msglevel)
                
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 
                    'Analyzer2': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/inactive_test_1.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', None, 'recovery None'], 'Analyzer2': ['S', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Restart with two analyzer (1,2)
        self.teal = Teal('data/checkpoint_test/inactive_test_2.conf', 'stderr', msgLevel=self.msglevel)
                
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 
                    'Analyzer1': ['R', None, None], 
                    'Analyzer2': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/inactive_test_2.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', None, 'recovery None'], 
                    'Analyzer1': ['S', None, None], 
                    'Analyzer2': ['S', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Restart with two analyzer (1,2)
        self.teal = Teal('data/checkpoint_test/inactive_test_2.conf', 'stderr', msgLevel=self.msglevel)
                
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 
                    'Analyzer1': ['R', None, None], 
                    'Analyzer2': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/inactive_test_2.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', None, 'recovery None'], 
                    'Analyzer1': ['S', None, None], 
                    'Analyzer2': ['S', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Restart with two analyzers (3, 5)
        self.teal = Teal('data/checkpoint_test/inactive_test_4.conf', 'stderr', msgLevel=self.msglevel)
                
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 
                    'Analyzer3': ['R', None, None], 
                    'Analyzer5': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

        self.teal = Teal('data/checkpoint_test/inactive_test_4.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', None, 'recovery None'], 
                    'Analyzer3': ['S', None, None], 
                    'Analyzer5': ['S', None, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

class TealTestCheckpointGEARFailureRestart(BaseTestCheckpoint):
    '''Test the checkpoint support when GEAR is in flight and restart''' 
    
    def setUp(self):
        '''Setup '''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        self.time_pattern = get_table_date_time_pattern()
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
    
    def run_teal_first(self):
        Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel=self.msglevel)
        j_in = Journal('j_in', file='data/checkpoint_test/G1_input_events_no_flush_001.json')
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        self.assertGEARAnalyzerGotEvents('Demo1Analyzer', 4)
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        self.assertTrue(j_out_all.wait_for_entries(4, seconds=60))
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
        self.assertGEARAnalyzerGotEvents('Demo1Analyzer', 4)
    
    def testCheckpointGEARrestart(self):
        '''Test restart of GEAR after failure '''
        #tealp = threading.Thread(target=self.run_teal_first)
        tealp = Process(target=self.run_teal_first)
        tealp.start()
        tealp.join()
        
        # Now restart and make sure we 
        self.teal = Teal('data/checkpoint_test/G1_base.conf', 'stderr', msgLevel=self.msglevel, restart='recovery')
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            name = listener.get_name()
            if name == 'Journal':
                j_out_all = listener.journal
        # Find the analyzer
        self.assertGEARAnalyzerGotEvents('Demo1Analyzer', 4)
        # Now flush the analyzer
        inject_flush_control_msg(datetime.strptime('2010-03-31 11:07:43.100000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertTrue(j_out_all.wait_for_entries(4, seconds=60))
        self.teal.shutdown()

    def testCheckpointInterrupt01(self):
        ''' Put data in Force the checkpoints.  Start the monitor.  Step a bit then shutdown and check the checkpoint!'''
        self.prepare_db()
        
        # Prepopulate DB: Event log and checkpoints
        self.teal = Teal('data/checkpoint_test/int_db.conf', 'stderr', msgLevel=self.msglevel, data_only=True)
        # Insert the events -- must have rec_ids referenced by checkpoint in event log 
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/int_db_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=False)
        force_dict = {'monitor_event_queue': ['S', 2, 'forced value'], 
                                'Analyzer1': ['S', 4, 'misc'], 
                                'Analyzer2': ['S', 20, 'stuff']}
        self._force_checkpoint(force_dict)
        self.teal.shutdown()
        
        # process a few to get past the first checkpoint and then shutdown
        self.teal = Teal('data/checkpoint_test/int_db.conf', 'stderr', msgLevel=self.msglevel)
        expected = {'monitor_event_queue': ['R', 2, 'recovery 2'], 
                    'Analyzer1': ['R', 4, None],   # Gets update right away now
                    'Analyzer2': ['R', 20, None]}
        self._wait_for_checkpoint(expected)

        # Move forward two ... to match first checkpoint
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 4, 'recovery 2'], 
                    'Analyzer1': ['R', 4, None], 
                    'Analyzer2': ['R', 20, None]}
        self._wait_for_checkpoint(expected)
        
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/int_db.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 4, 'recovery 2'], 
                    'Analyzer1': ['S',4, None], 
                    'Analyzer2': ['R', 20, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Move up past last checkpoint 
        self.teal = Teal('data/checkpoint_test/int_db.conf', 'stderr', msgLevel=self.msglevel)
        expected = {'monitor_event_queue': ['R', 4, 'recovery 4'], 
                    'Analyzer1': ['R', 4, None], 
                    'Analyzer2': ['R', 20, None]}
        self._wait_for_checkpoint(expected)

        monitor = get_service(SERVICE_EVENT_MONITOR)
        for _ in range(17):
            monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 21, 'recovery 4'], 
                    'Analyzer1': ['R', 4, None], 
                    'Analyzer2': ['R', 20, None]}
        self._wait_for_checkpoint(expected, in_tries=30)
        
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/int_db.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 21, 'recovery 4'], 
                    'Analyzer1': ['S', 21, None], 
                    'Analyzer2': ['S', 21, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()

    def testCheckpointNewAnalyzer(self):
        ''' Make sure that new analyzer and shutdown aligned analyzers are handled correctly'''
        self.prepare_db()
        
        # Prepopulate DB: Event log and checkpoints
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True)
        # Insert the events -- must have rec_ids referenced by checkpoint in event log 
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/int_db_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=False)
        force_dict = {'monitor_event_queue': ['S', 10, 'forced value'], 
                                'Analyzer1': ['F', 4, 'misc'],
                                'Analyzer3': ['S', 10, None]}
        self._force_checkpoint(force_dict)
        self.teal.shutdown()
        
        # process a few to get past the first checkpoint and then shutdown
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel)
        expected = {'monitor_event_queue': ['R', 10, 'recovery 4'], 
                    'Analyzer1': ['F', 4, 'misc'], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)

        # Move forward two ... to match first checkpoint
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 5, 'recovery 4'], 
                    'Analyzer1': ['R', 4, 'misc'],      # Only checkpoints on events
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 6, 'recovery 4'], 
                    'Analyzer1': ['R', 6, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 7, 'recovery 4'], 
                    'Analyzer1': ['R', 6, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 7, 'recovery 4'], 
                    'Analyzer1': ['S', 7, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Move up past last checkpoint 
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel)
        expected = {'monitor_event_queue': ['R', 7, 'recovery 7'], 
                    'Analyzer1': ['R', 7, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)

        monitor = get_service(SERVICE_EVENT_MONITOR)
        for _ in range(17):
            monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 24, 'recovery 7'], 
                    'Analyzer1': ['R', 24, None], 
                    'Analyzer2': ['R', 24, None], 
                    'Analyzer3': ['R', 24, None]}
        self._wait_for_checkpoint(expected, in_tries=30)
        
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 24, 'recovery 7'], 
                    'Analyzer1': ['S', 24, None], 
                    'Analyzer2': ['S', 24, None], 
                    'Analyzer3': ['S', 24, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()    


class TealTestCheckpointGEAROngoing(BaseTestCheckpoint):
    '''Test the checkpoint support when GEAR is processing''' 
    
    def setUp(self):
        '''Setup '''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        self.conf_shutdown_mode_val = self.force_env('TEAL_SHUTDOWN_MODE', 'immediate')
        self.time_pattern = get_table_date_time_pattern()
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        self.restore_env('TEAL_SHUTDOWN_MODE', self.conf_shutdown_mode_val)
    
        
    def testCheckpointGEARrunning(self):
        '''Test checkpoint values as GEAR is running along.'''
        p = Process(target=self._runCheckpointGEARrunning)
        p.start()
        p.join()
 
    def _runCheckpointGEARrunning(self):
        self.teal = Teal('data/checkpoint_test/GEAR_move.conf', 'stderr', msgLevel=self.msglevel)
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
              
        self.assertEqual(self._get_max_event(), None)
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', None, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
        self._wait_for_checkpoint(expected)
        
        j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')
        # Force rec ids so we know when to flush
        j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=False, post=True)

        expected = {'monitor_event_queue': ['R', 8, 'recovery None'], 
                    'Demo1Analyzer': ['Not checked']}
        self._wait_for_checkpoint(expected, only_names=['monitor_event_queue'])
        
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put(ControlMsg(CONTROL_MSG_TYPE_FLUSH, {'creation_time':datetime.strptime("2010-03-30 21:40:25.100000", '%Y-%m-%d %H:%M:%S.%f')}))
        
        self.assertTrue(alj.wait_for_entries(2))
            
        max_id = self._get_max_event()
        tmp_dts = apply_time_pattern(['2010-03-30 21:40:25.100000'], self.time_pattern)
        keep_expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id-5, '["{0}", "{1}", ["{2}S484","{3}S487","{4}S488","{5}U489","{6}U499"]]'.format(tmp_dts[0], str(max_id), str(max_id-4), str(max_id-3), str(max_id-2), str(max_id-1), str(max_id))]}
        self._wait_for_checkpoint(keep_expected)
        self.assertEqual(get_current_min_checkpoint_rec_id(), max_id-5)
        
        # Shutdown to get pool closure
        get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
        self.teal.shutdown()
    
        # Restart without data to see that things shutdown cleanly    
        self.teal = Teal('data/checkpoint_test/GEAR_move.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 
                   'Demo1Analyzer': ['I', max_id-5, '["{0}", "{1}", ["{2}S484","{3}S487","{4}S488","{5}U489","{6}U499"]]'.format(tmp_dts[0], str(max_id), str(max_id-4), str(max_id-3), str(max_id-2), str(max_id-1), str(max_id))]}
        self._wait_for_checkpoint(expected)

        # Now force the checkpoint to the more interesting value it would have had if things hadn't shutdown 
        self._force_checkpoint(keep_expected)
        self.teal.shutdown()
        
        # restart to make sure things restart correctly after an immediate shutdown 
        self.teal = Teal('data/checkpoint_test/GEAR_move.conf', 'stderr', msgLevel=self.msglevel)
        # Add an alert listener
        alj = Journal('alert listener journal')
        get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
              
        self.assertEqual(self._get_max_event(), 8)
        # check the checkpoint
        expected = {'monitor_event_queue': ['R', 8, 'recovery 3'], 'Demo1Analyzer': ['Not checked']}
        self._wait_for_checkpoint(expected, only_names=['monitor_event_queue'])

        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put(ControlMsg(CONTROL_MSG_TYPE_FLUSH, {'creation_time':datetime.strptime("2010-03-30 20:40:55.100000", '%Y-%m-%d %H:%M:%S.%f')}))
        tmp_dts = apply_time_pattern(['2010-03-30 20:40:55.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id-5, '["{0}", "{1}", ["{2}S483","{3}S486","{4}S487","{5}U488","{6}U498"]]'.format(tmp_dts[0], str(max_id), str(max_id-4), str(max_id-3), str(max_id-2), str(max_id-1), str(max_id))]}
        
        # Flush the pool again much, much later (so nothing moves forward 
        event_q.put(ControlMsg(CONTROL_MSG_TYPE_FLUSH, {'creation_time':datetime.strptime("2010-03-30 22:40:55.100000", '%Y-%m-%d %H:%M:%S.%f')}))
        tmp_dts = apply_time_pattern(['2010-03-30 22:40:55.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                    'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
        self.teal.shutdown()
        
    def testCheckpointImmediate01(self):
        '''Test checkpoint Immediate 01.'''
        p = Process(target=self._runCheckpointImmediate01)
        p.start()
        p.join()
        self.assertEquals(p.exitcode, 0)
 
    def _runCheckpointImmediate01(self):
        '''Test checkpoint values as GEAR is running by delaying a long time on one event.'''
        
        exit_rc = 0
        try:
            self.teal = Teal('data/checkpoint_test/immediate_test01.conf', 'stderr', msgLevel=self.msglevel)
            self.assertEqual(self._get_max_event(), None)
            # check the checkpoint
            expected = {'monitor_event_queue': ['R', None, 'recovery None'], 'Demo1Analyzer': ['R', None, None], 'Demo2Analyzer': ['R', None, None]}
            self._wait_for_checkpoint(expected)
            
            j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')
            # Force rec ids so we know ids 
            j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=False, post=True)
            
            expected = {'monitor_event_queue': ['R', 8, 'recovery None'], 
                        'Demo1Analyzer': ['R', 3, None],
                        'Demo2Analyzer': ['R', 6, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()
    
            # Restart without data to see that things shutdown cleanly    
            self.teal = Teal('data/checkpoint_test/immediate_test01.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
            expected = {'monitor_event_queue': ['S', 8, 'recovery None'], 
                        'Demo1Analyzer': ['I', 3, None], 
                        'Demo2Analyzer': ['S', 8, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()
        except:
            exit_rc = 30
        sys.exit(exit_rc)
        
    def testCheckpointEmptyDbImmediateAligned(self):
        '''Test checkpoint Empty DB Immediate aligned.'''
        p = Process(target=self._runCheckpointEmptyDbImmediateAligned)
        p.start()
        p.join()
        self.assertEquals(p.exitcode, 0)
       
    def _runCheckpointEmptyDbImmediateAligned(self):
        '''Test checkpoint value after inserting into an empty db.immediate aligned'''
        exit_rc = 0 
        try:
            self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=self.msglevel)
            # Add an alert listener
            alj = Journal('alert listener journal')
            get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(alj)
                  
            self.assertEqual(self._get_max_event(), None)
            # check the checkpoint
            expected = {'monitor_event_queue': ['R', None, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
            self._wait_for_checkpoint(expected)
            
            j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')
            j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=False, no_delay=False, post=True)
    
            self.assertTrue(alj.wait_for_entries(4))
            
            max_id = self._get_max_event()
            tmp_dts = apply_time_pattern(['2010-03-30 21:40:27.100000'], self.time_pattern)
            expected = {'monitor_event_queue': ['R', max_id, 'recovery None'], 
                        'Demo1Analyzer': ['R', max_id, '["{0}", "{1}", []]'.format(tmp_dts[0], str(max_id))]}
            self._wait_for_checkpoint(expected)
            self.assertEqual(get_current_min_checkpoint_rec_id(), max_id)
            
            # Shutdown to get pool closure
            get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(alj)
            self.teal.shutdown()
            
            self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
            expected = {'monitor_event_queue': ['S', max_id, 'recovery None'], 
                        'Demo1Analyzer': ['S', max_id, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()
        except:
            exit_rc = 30
        sys.exit(exit_rc)
        
    def testCheckpointImmediate01Synch(self):
        '''Test checkpoint Immediate 01 Synch.'''
        p = Process(target=self._runCheckpointImmediate01Synch)
        p.start()
        p.join()
        self.assertEquals(p.exitcode, 0)

    def _runCheckpointImmediate01Synch(self):
        '''Test checkpoint values as GEAR is running synchronously by delaying a long time on one event.'''
        exit_rc = 0 
        try:
            self.teal = Teal('data/checkpoint_test/immediate_test01_synch.conf', 'stderr', msgLevel=self.msglevel)
            self.assertEqual(self._get_max_event(), None)
            # check the checkpoint
            expected = {'monitor_event_queue': ['R', None, 'recovery None'], 'Demo1Analyzer': ['R', None, None]}
            self._wait_for_checkpoint(expected)
            
            j_in = Journal('j_in', file='data/checkpoint_test/data_sample_demo_NEW_001.json')
            # Force rec ids so we know ids 
            j_in.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=True)
            
            # Stuck at 3 because Demo1Analyzer is waiting 100 seconds on it
            expected = {'monitor_event_queue': ['R', 3, 'recovery None'], 
                        'Demo1Analyzer': ['R', 3, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()
    
            # Restart without data to see that things shutdown cleanly    
            self.teal = Teal('data/checkpoint_test/immediate_test01_synch.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
            expected = {'monitor_event_queue': ['S', 3, 'recovery None'], 
                        'Demo1Analyzer': ['I', 3, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()
        except:
            exit_rc = 30
        sys.exit(exit_rc)

    def testCheckpointNewAnalyzerSI(self):
        '''Test checkpoint New Analyzer Shutdown immediate.'''
        p = Process(target=self._runCheckpointNewAnalyzerSI)
        p.start()
        p.join()
        self.assertEquals(p.exitcode, 0)
        
    def _runCheckpointNewAnalyzerSI(self):
        ''' Make sure that new analyzer and shutdown aligned analyzers are handled correctly'''
        exit_rc = 0 
        try:
            self.prepare_db()
            
            # Prepopulate DB: Event log and checkpoints
            self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True)
            # Insert the events -- must have rec_ids referenced by checkpoint in event log 
            in_j = Journal('events to inject to DB', 'data/checkpoint_test/int_db_01.json')
            in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=False)
            force_dict = {'monitor_event_queue': ['S', 10, 'forced value'], 
                                    'Analyzer1': ['F', 4, 'misc'],
                                    'Analyzer3': ['S', 10, None]}
            self._force_checkpoint(force_dict)
            self.teal.shutdown()
            
            # process a few to get past the first checkpoint and then shutdown
            self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel)
            expected = {'monitor_event_queue': ['R', 10, 'recovery 4'], 
                        'Analyzer1': ['F', 4, 'misc'], 
                        'Analyzer2': ['R', 10, None], 
                        'Analyzer3': ['R', 10, None]}
            self._wait_for_checkpoint(expected)
    
            # Move forward two ... to match first checkpoint
            monitor = get_service(SERVICE_EVENT_MONITOR)
            monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
            expected = {'monitor_event_queue': ['R', 5, 'recovery 4'], 
                        'Analyzer1': ['R', 4, 'misc'],      # Only checkpoints on events
                        'Analyzer2': ['R', 10, None], 
                        'Analyzer3': ['R', 10, None]}
            self._wait_for_checkpoint(expected)
            monitor = get_service(SERVICE_EVENT_MONITOR)
            monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
            expected = {'monitor_event_queue': ['R', 6, 'recovery 4'], 
                        'Analyzer1': ['R', 6, None], 
                        'Analyzer2': ['R', 10, None], 
                        'Analyzer3': ['R', 10, None]}
            self._wait_for_checkpoint(expected)
            monitor = get_service(SERVICE_EVENT_MONITOR)
            monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
            expected = {'monitor_event_queue': ['R', 7, 'recovery 4'], 
                        'Analyzer1': ['R', 6, None], 
                        'Analyzer2': ['R', 10, None], 
                        'Analyzer3': ['R', 10, None]}
            self._wait_for_checkpoint(expected)
            
            monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
            self.teal.shutdown()
            
            self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
            expected = {'monitor_event_queue': ['S', 7, 'recovery 4'], 
                        'Analyzer1': ['S', 7, None], 
                        'Analyzer2': ['R', 10, None], 
                        'Analyzer3': ['R', 10, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()
            
            # Move up past last checkpoint 
            self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel)
            expected = {'monitor_event_queue': ['R', 7, 'recovery 7'], 
                        'Analyzer1': ['R', 7, None], 
                        'Analyzer2': ['R', 10, None], 
                        'Analyzer3': ['R', 10, None]}
            self._wait_for_checkpoint(expected)
    
            monitor = get_service(SERVICE_EVENT_MONITOR)
            for _ in range(17):
                monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
            expected = {'monitor_event_queue': ['R', 24, 'recovery 7'], 
                        'Analyzer1': ['R', 24, None], 
                        'Analyzer2': ['R', 24, None], 
                        'Analyzer3': ['R', 24, None]}
            self._wait_for_checkpoint(expected, in_tries=30)
            
            monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
            self.teal.shutdown()
            
            self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
            expected = {'monitor_event_queue': ['S', 24, 'recovery 7'], 
                        'Analyzer1': ['S', 24, None], 
                        'Analyzer2': ['S', 24, None], 
                        'Analyzer3': ['S', 24, None]}
            self._wait_for_checkpoint(expected)
            self.teal.shutdown()    
        except:
            exit_rc = 30
        sys.exit(exit_rc)

    def testCheckpointUpdate001(self):
        ''' Make sure that the Checkpoint updates are correctly generated'''
        self.prepare_db()
        
        # Prepopulate DB: Event log and checkpoints
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True)
        # Insert the events -- must have rec_ids referenced by checkpoint in event log 
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/int_db_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=False)
        force_dict = {'monitor_event_queue': ['S', 10, 'forced value'], 
                                'Analyzer1': ['F', 4, 'misc'],
                                'Analyzer3': ['S', 10, None]}
        self._force_checkpoint(force_dict)
        self.teal.shutdown()
        
        # process a few to get past the first checkpoint and then shutdown
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel)
        expected = {'monitor_event_queue': ['R', 10, 'recovery 4'], 
                    'Analyzer1': ['F', 4, 'misc'], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)

        # Move forward two ... to match first checkpoint
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 5, 'recovery 4'], 
                    'Analyzer1': ['R', 4, 'misc'],      # Only checkpoints on events
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 6, 'recovery 4'], 
                    'Analyzer1': ['R', 6, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 7, 'recovery 4'], 
                    'Analyzer1': ['R', 6, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 7, 'recovery 4'], 
                    'Analyzer1': ['S', 7, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()
        
        # Move up past last checkpoint 
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel)
        expected = {'monitor_event_queue': ['R', 7, 'recovery 7'], 
                    'Analyzer1': ['R', 7, None], 
                    'Analyzer2': ['R', 10, None], 
                    'Analyzer3': ['R', 10, None]}
        self._wait_for_checkpoint(expected)

        monitor = get_service(SERVICE_EVENT_MONITOR)
        for _ in range(17):
            monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        expected = {'monitor_event_queue': ['R', 24, 'recovery 7'], 
                    'Analyzer1': ['R', 24, None], 
                    'Analyzer2': ['R', 24, None], 
                    'Analyzer3': ['R', 24, None]}
        self._wait_for_checkpoint(expected, in_tries=30)
        
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/new_analyzer.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 24, 'recovery 7'], 
                    'Analyzer1': ['S', 24, None], 
                    'Analyzer2': ['S', 24, None], 
                    'Analyzer3': ['S', 24, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown()    

class TealTestCheckpointUpdateBAD(BaseTestCheckpoint):
    '''Test the checkpoint update support''' 
    
    def setUp(self):
        '''Setup '''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        self.conf_update_val = self.force_env('TEAL_UPDATE_CHECKPOINT_FREQUENCY', 'bad value')
        self.unprocc_log = self.force_env('TEAL_EVENT_Q_NOT_ANALYZED_LOG_LEVEL', 'debug')
        self.time_pattern = get_table_date_time_pattern()
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        self.restore_env('TEAL_UPDATE_CHECKPOINT_FREQUENCY', self.conf_update_val)
        self.restore_env('TEAL_EVENT_Q_NOT_ANALYZED_LOG_LEVEL', self.unprocc_log)


    def testCheckpointUpdateBadEnv(self):
        ''' Test that the update freq defaults if bad env value ''' 
        self.teal = Teal('data/checkpoint_test/update/normal1.conf', 'stderr', msgLevel=self.msglevel)
        # Attach journals to the queues
        j_out_eq = Journal('j_out_eq')
        registry.get_service(SERVICE_EVENT_Q).register_listener(j_out_eq)
        j_out_aaq = Journal('j_out_aaq')
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).register_listener(j_out_aaq)
        j_out_dq = Journal('j_out_dq')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(j_out_dq)
        # inject some events
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/update/events_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=True)
        
        uc_count = 0
        ck_value = None
      
        # Wait for them to process -- only updates are processed
        expected = {'monitor_event_queue': ['R', 30, 'recovery None'], 
                    'Analyzer1': ['R', ck_value, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)

        self.assertEqual(len(j_out_eq), 30 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        registry.get_service(SERVICE_EVENT_Q).unregister_listener(j_out_eq)
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).unregister_listener(j_out_aaq)
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(j_out_dq)
        self.teal.shutdown()
        self.teal = Teal('data/checkpoint_test/update/normal1.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 30, 'recovery None'], 
                    'Analyzer1': ['S', 30, None], 
                    'Analyzer2': ['S', 30, None], 
                    'Analyzer3': ['S', 30, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown() 

TEST_UPDATE_FREQUENCY = 5
     
class TealTestCheckpointUpdate(BaseTestCheckpoint):
    '''Test the checkpoint update support''' 
    
    def setUp(self):
        '''Setup '''
        self.prepare_db()
        self.conf_dir_val = self.force_env('TEAL_CONF_DIR', 'data/checkpoint_test')
        self.conf_update_val = self.force_env('TEAL_UPDATE_CHECKPOINT_FREQUENCY', str(TEST_UPDATE_FREQUENCY))
        self.unprocc_log = self.force_env('TEAL_EVENT_Q_NOT_ANALYZED_LOG_LEVEL', 'debug')
        self.time_pattern = get_table_date_time_pattern()
    
    def tearDown(self):
        '''Teardown '''
        self.restore_env('TEAL_CONF_DIR', self.conf_dir_val)
        self.restore_env('TEAL_UPDATE_CHECKPOINT_FREQUENCY', self.conf_update_val)
        self.restore_env('TEAL_EVENT_Q_NOT_ANALYZED_LOG_LEVEL', self.unprocc_log)


    def testCheckpointUpdateShippedMonitor1(self):
        ''' Test updates are generated by the shipped monitor with analyzers that don't process anything ''' 
        self.teal = Teal('data/checkpoint_test/update/normal1.conf', 'stderr', msgLevel=self.msglevel)
        # Attach journals to the queues
        j_out_eq = Journal('j_out_eq')
        registry.get_service(SERVICE_EVENT_Q).register_listener(j_out_eq)
        j_out_aaq = Journal('j_out_aaq')
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).register_listener(j_out_aaq)
        j_out_dq = Journal('j_out_dq')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(j_out_dq)
        # inject some events
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/update/events_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=True)
        
        uc_count = 30//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
      
        # Wait for them to process -- only updates are processed
        expected = {'monitor_event_queue': ['R', 30, 'recovery None'], 
                    'Analyzer1': ['R', ck_value, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)

        self.assertEqual(len(j_out_eq), 30 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        registry.get_service(SERVICE_EVENT_Q).unregister_listener(j_out_eq)
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).unregister_listener(j_out_aaq)
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(j_out_dq)
        self.teal.shutdown()
        self.teal = Teal('data/checkpoint_test/update/normal1.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 30, 'recovery None'], 
                    'Analyzer1': ['S', 30, None], 
                    'Analyzer2': ['S', 30, None], 
                    'Analyzer3': ['S', 30, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown() 
           
    def testCheckpointUpdateShippedMonitor2(self):
        ''' Test updates are generated by the shipped monitor with analyzers that are processing events ''' 
        self.teal = Teal('data/checkpoint_test/update/normal2.conf', 'stderr', msgLevel=self.msglevel)
        # Attach journals to the queues
        j_out_eq = Journal('j_out_eq')
        registry.get_service(SERVICE_EVENT_Q).register_listener(j_out_eq)
        j_out_aaq = Journal('j_out_aaq')
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).register_listener(j_out_aaq)
        j_out_dq = Journal('j_out_dq')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(j_out_dq)
        # inject some events
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/update/events_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=True)
        
        uc_count = 30//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
      
        # Wait for them to process -- Last events only processed by 3 
        expected = {'monitor_event_queue': ['R', 30, 'recovery None'], 
                    'Analyzer1': ['R', ck_value, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', 30, None]}
        self._wait_for_checkpoint(expected)

        self.assertEqual(len(j_out_eq), 30 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        registry.get_service(SERVICE_EVENT_Q).unregister_listener(j_out_eq)
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).unregister_listener(j_out_aaq)
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(j_out_dq)
        self.teal.shutdown()
        self.teal = Teal('data/checkpoint_test/update/normal2.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 30, 'recovery None'], 
                    'Analyzer1': ['S', 30, None], 
                    'Analyzer2': ['S', 30, None], 
                    'Analyzer3': ['S', 30, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown() 

    def testCheckpointUpdateShippedMonitor3(self):
        ''' Test updates are generated by the shipped monitor with analyzers that are processing events using GEAR ''' 
        self.teal = Teal('data/checkpoint_test/update/normal3.conf', 'stderr', msgLevel=self.msglevel)
        # Attach journals to the queues
        j_out_eq = Journal('j_out_eq')
        registry.get_service(SERVICE_EVENT_Q).register_listener(j_out_eq)
        j_out_aaq = Journal('j_out_aaq')
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).register_listener(j_out_aaq)
        j_out_dq = Journal('j_out_dq')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(j_out_dq)
        # inject some events
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/update/events_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=True)
        
        uc_count = 30//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
      
        if TEST_UPDATE_FREQUENCY <= 1:
            A2_exp = 1
        else:
            A2_exp = None
        # Wait for them to process                     
        tmp_dts = apply_time_pattern(['2010-03-30 21:40:11.100000', '2010-03-30 21:40:12.100000'], self.time_pattern)
        expected = {'monitor_event_queue': ['R', 30, 'recovery None'], 
                    'AnalyzerA1': ['R', 1, '["{0}", "30", ["2U488","3S492","11U506","12U506","13S502","21U506","22U506","23S502"]]'.format(tmp_dts[1])], 
                    'AnalyzerA2': ['R', A2_exp, None], 
                    'AnalyzerB': ['R', 30, '["{0}", "30", []]'.format(tmp_dts[0])], 
                    'AnalyzerC': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected, in_tries=30)

        self.assertEqual(len(j_out_eq), 30 + uc_count)
        self.assertEqual(len(j_out_aaq), 9 + uc_count)
        self.assertEqual(len(j_out_dq), 9 + uc_count)
        
        registry.get_service(SERVICE_EVENT_Q).unregister_listener(j_out_eq)
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).unregister_listener(j_out_aaq)
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(j_out_dq)
        self.teal.shutdown()
        self.teal = Teal('data/checkpoint_test/update/normal3.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 30, 'recovery None'], 
                    'AnalyzerA1': ['S', 30, None], 
                    'AnalyzerA2': ['S', 30, None], 
                    'AnalyzerB': ['S', 30, None], 
                    'AnalyzerC': ['S', 30, None]}
        self._wait_for_checkpoint(expected)
        self.teal.shutdown() 
        
    def testCheckpointUpdateSteppingMonitor1(self):
        ''' Test updates are generated by the stepping monitor with analyzers that don't process anything ''' 
        self.teal = Teal('data/checkpoint_test/update/stepping1.conf', 'stderr', msgLevel=self.msglevel)
        # Attach journals to the queues
        j_out_eq = Journal('j_out_eq')
        registry.get_service(SERVICE_EVENT_Q).register_listener(j_out_eq)
        j_out_aaq = Journal('j_out_aaq')
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).register_listener(j_out_aaq)
        j_out_dq = Journal('j_out_dq')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(j_out_dq)
        # inject some events
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/update/events_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=False)
        
        monitor = get_service(SERVICE_EVENT_MONITOR)
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        
        if TEST_UPDATE_FREQUENCY != 1:
            expected = {'monitor_event_queue': ['R', 1, 'recovery None'], 
                        'Analyzer1': ['R', None, None], 
                        'Analyzer2': ['R', None, None], 
                        'Analyzer3': ['R', None, None]}
            self._wait_for_checkpoint(expected)
            self.assertEqual(len(j_out_eq), 1)
            self.assertEqual(len(j_out_aaq), 0)
            self.assertEqual(len(j_out_dq), 0)
        else:
            expected = {'monitor_event_queue': ['R', 1, 'recovery None'], 
                        'Analyzer1': ['R', 1, None], 
                        'Analyzer2': ['R', 1, None], 
                        'Analyzer3': ['R', 1, None]}
            self._wait_for_checkpoint(expected)
            self.assertEqual(len(j_out_eq), 2)
            self.assertEqual(len(j_out_aaq), 1)
            self.assertEqual(len(j_out_dq), 1)
        
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ALL_EVENTS)
        
        uc_count = 30//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
      
        # Wait for them to process -- only updates are processed
        expected = {'monitor_event_queue': ['R', 30, 'recovery None'], 
                    'Analyzer1': ['R', ck_value, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)

        self.assertEqual(len(j_out_eq), 30 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        registry.get_service(SERVICE_EVENT_Q).unregister_listener(j_out_eq)
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).unregister_listener(j_out_aaq)
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(j_out_dq)
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/update/stepping1.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 30, 'recovery None'], 
                    'Analyzer1': ['S', 30, None], 
                    'Analyzer2': ['S', 30, None], 
                    'Analyzer3': ['S', 30, None]}
        self._wait_for_checkpoint(expected)
        
        #monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)  Not using monitor
        self.teal.shutdown()    
        
    def testCheckpointUpdateSteppingMonitor2(self):
        ''' Test that the analyzers that are processing don't update ''' 
        self.teal = Teal('data/checkpoint_test/update/stepping2.conf', 'stderr', msgLevel=self.msglevel)
        # Attach journals to the queues
        j_out_eq = Journal('j_out_eq')
        registry.get_service(SERVICE_EVENT_Q).register_listener(j_out_eq)
        j_out_aaq = Journal('j_out_aaq')
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).register_listener(j_out_aaq)
        j_out_dq = Journal('j_out_dq')
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).register_listener(j_out_dq)
        # inject some events
        in_j = Journal('events to inject to DB', 'data/checkpoint_test/update/events_01.json')
        in_j.insert_in_db(progress_cb=None, truncate=False, use_rec_ids=True, no_delay=True, post=False)
        
        monitor = get_service(SERVICE_EVENT_MONITOR)
        
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        uc_count = 1//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
        if ck_value == 0:
            ck_value = None
        expected = {'monitor_event_queue': ['R', 1, 'recovery None'], 
                    'Analyzer1': ['R', ck_value, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(len(j_out_eq), 1 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        uc_count = 2//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
        if ck_value == 0:
            ck_value = None
        expected = {'monitor_event_queue': ['R', 2, 'recovery None'], 
                    'Analyzer1': ['R', 2, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(len(j_out_eq), 2 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        uc_count = 3//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
        if ck_value == 0:
            ck_value = None
        expected = {'monitor_event_queue': ['R', 3, 'recovery None'], 
                    'Analyzer1': ['R', max(2, ck_value), None], 
                    'Analyzer2': ['R', 3, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(len(j_out_eq), 3 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
         
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        uc_count = 4//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
        if ck_value == 0:
            ck_value = None
        expected = {'monitor_event_queue': ['R', 4, 'recovery None'], 
                    'Analyzer1': ['R', max(2, ck_value), None], 
                    'Analyzer2': ['R', max(3, ck_value), None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(len(j_out_eq), 4 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
                 
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        uc_count = 5//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
        if ck_value == 0:
            ck_value = None
        expected = {'monitor_event_queue': ['R', 5, 'recovery None'], 
                    'Analyzer1': ['R', max(2, ck_value), None], 
                    'Analyzer2': ['R', max(3, ck_value), None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(len(j_out_eq), 5 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
       
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ONE_EVENT)
        uc_count = 6//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
        if ck_value == 0:
            ck_value = None
        expected = {'monitor_event_queue': ['R', 6, 'recovery None'], 
                    'Analyzer1': ['R', max(2, ck_value), None], 
                    'Analyzer2': ['R', max(3, ck_value), None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)
        self.assertEqual(len(j_out_eq), 6 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)       
       
        monitor.control_q.put(MONITOR_CONTROL_PROCESS_ALL_EVENTS)
        uc_count = 30//TEST_UPDATE_FREQUENCY
        ck_value = uc_count * TEST_UPDATE_FREQUENCY
      
        # Wait for them to process -- only updates are processed
        expected = {'monitor_event_queue': ['R', 30, 'recovery None'], 
                    'Analyzer1': ['R', ck_value, None], 
                    'Analyzer2': ['R', ck_value, None], 
                    'Analyzer3': ['R', ck_value, None]}
        self._wait_for_checkpoint(expected)

        self.assertEqual(len(j_out_eq), 30 + uc_count)
        self.assertEqual(len(j_out_aaq), uc_count)
        self.assertEqual(len(j_out_dq), uc_count)
        
        registry.get_service(SERVICE_EVENT_Q).unregister_listener(j_out_eq)
        registry.get_service(SERVICE_ALERT_ANALYZER_Q).unregister_listener(j_out_aaq)
        registry.get_service(SERVICE_ALERT_DELIVERY_Q).unregister_listener(j_out_dq)
        monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)
        self.teal.shutdown()
        
        self.teal = Teal('data/checkpoint_test/update/stepping2.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        expected = {'monitor_event_queue': ['S', 30, 'recovery None'], 
                    'Analyzer1': ['S', 30, None], 
                    'Analyzer2': ['S', 30, None], 
                    'Analyzer3': ['S', 30, None]}
        self._wait_for_checkpoint(expected)
        
        #monitor.control_q.put(MONITOR_CONTROL_WAIT_ON_NOTIFY)  Not using monitor
        self.teal.shutdown()    
        

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)


