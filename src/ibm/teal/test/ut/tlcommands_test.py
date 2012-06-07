# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2012     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import os
import unittest
from ibm.teal.teal import Teal, registry
from ibm.teal.util.journal import Journal
from ibm.teal.test.teal_unittest import TealTestCase,\
    get_table_date_time_pattern, apply_time_pattern
from ibm.teal.checkpoint_mgr import  EventCheckpoint

RMALERT = ''
CHALERT = ''
LSALERT = ''
RMEVENT = ''
LSEVENT = ''
LSCKPT = ''
TEAL = ''
VFYRULE = ''

class TealCommandLineTest(TealTestCase):

    def setUp(self):
        t = Teal('data/tlcommands_test/test.conf', data_only=True)
        global RMALERT, CHALERT, LSALERT, RMEVENT, LSEVENT, LSCKPT, TEAL, VFYRULE
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        RMALERT = os.path.join(teal_path,'bin/tlrmalert')
        CHALERT = os.path.join(teal_path,'bin/tlchalert')
        LSALERT = os.path.join(teal_path,'bin/tllsalert')
        RMEVENT = os.path.join(teal_path,'bin/tlrmevent')
        LSEVENT = os.path.join(teal_path,'bin/tllsevent')
        LSCKPT = os.path.join(teal_path, 'bin/tllsckpt')
        TEAL    = os.path.join(teal_path,'ibm/teal/teal.py')
        VFYRULE = os.path.join(teal_path, 'bin/tlvfyrule')
        t.shutdown()
        
        self.time_pattern = get_table_date_time_pattern()

        self.prepare_db()
        self._add_journal('data/tlcommands_test/events_001.json')
        self._add_journal('data/tlcommands_test/alerts_001.json')
        
        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR', '/opt/teal'), 'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)

    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)
    
    def _add_journal(self, json_file):
        ''' Load the alert DB from the journal JSON file '''
        t = Teal('data/tlcommands_test/test.conf')
        # Alerts
        ja = Journal('temp_journal', file=json_file)
        ja.insert_in_db(truncate=False, no_delay=True)
        t.shutdown()

    def test_tlchalert_invalid_opts(self):
        ''' Make sure the tlchalert command fails invalid options '''
        # Invalid command arguments
        self.assertCmdFails([CHALERT], exp_err_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]tlchalert: error: Must specify at least one attribute to change')
        self.assertCmdFails([CHALERT,'--id'], exp_err_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]tlchalert: error: --id option requires an argument')
        self.assertCmdFails([CHALERT,'--id', '1'], exp_err_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]tlchalert: error: Must specify at least one attribute to change')
        self.assertCmdFails([CHALERT,'--id', '1', '--state'], exp_err_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]tlchalert: error: --state option requires an argument')
        self.assertCmdFails([CHALERT,'--id', '1', '--state', 'reopen'], exp_err_msg="Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]tlchalert: error: option --state: invalid choice: 'reopen' (choose from 'close')")
        self.assertCmdFails([CHALERT,'--id', '1', '--close'], exp_err_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]tlchalert: error: no such option: --close')

    def test_tlchalert_invalid_states(self):
        ''' Make sure the tlchalert command fails invalid state changes '''
        # Close a duplicate alert
        self.assertCmdFails([CHALERT,'--id','2','--state','close'], exp_err_msg="Cannot close alert. Reason: rc = 3: 'Operation not allowed on duplicate alert'", exp_rc=1)

        # Close a closed alert
        self.assertCmdWorks([CHALERT,'--id','3','--state','close'])
        self.assertCmdFails([CHALERT,'--id','3','--state','close'], exp_err_msg="Cannot close alert. Reason: rc = 2: 'Current alert state does not allow this operation'", exp_rc=1)

    def test_tlchalert_valid_states(self):
        ''' Make sure the tlchalert command works on alerts in valid states '''
        # Close an alert with no associations to other alerts
        self.assertCmdWorks([CHALERT,'--id','6','--state','close'])

        # Close an alert with a duplicate alert
        self.assertCmdWorks([CHALERT,'--id','1','--state','close'])
        self.assertCmdFails([CHALERT,'--id','2','--state','close'], exp_err_msg="Cannot close alert. Reason: rc = 2: 'Current alert state does not allow this operation'", exp_rc=1)
        
        # Close a suppressed alert
        self.assertCmdWorks([CHALERT,'--id','4','--state','close'])

    def test_tlrmalert_invalid_opts(self):
        ''' Make sure the tlrmalert fails invalid options '''
        self.assertCmdFails([RMALERT,'--ids'],exp_err_msg='Usage: tlrmalert [options]tlrmalert: error: --ids option requires an argument')
        self.assertCmdFails([RMALERT,'--id 1'],exp_err_msg='Usage: tlrmalert [options]tlrmalert: error: no such option: --id 1')

    def test_tllsevent_time(self):
        ''' Test timestamp values for tllsevent '''
        self.assertCmdFails([LSEVENT,'--query','time_occurred=2011-01-33'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid timestamp for time_occurred: 2011-01-33')
        self.assertCmdFails([LSEVENT,'--query','time_logged=2011-13-17'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid timestamp for time_logged: 2011-13-17')
        tmp_good_msg = 'rec_id,event_id,time_occurred,time_logged,src_comp,src_loc,src_loc_type,rpt_comp,rpt_loc,rpt_loc_type,event_cnt,elapsed_time1,Event 01,{0},{1},CNM,MB-SL3-ET1-PT2,C,,,,,2,Event 02,{2},{3},CNM,MB-SL1-ET1-PT1,C,,,,,3,Event 03,{4},{5},CNM,MB-SL1-ET1-PT2,C,,,,,4,Event 04,{6},{7},CNM,MB-SL1-ET1-PT2,C,,,,,5,Event 05,{8},{9},CNM,MB-SL1-ET1-PT2,C,,,,,6,Event 06,{10},{11},CNM,MB-SL1-ET1-PT2,C,,,,,'
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:00.100000', '2011-01-17 21:40:00.100000', '2011-01-17 21:40:04.100000', '2011-01-17 21:40:04.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:12.100000' ,'2011-01-17 21:40:12.100000', '2011-01-17 21:40:16.100000', '2011-01-17 21:40:16.100000', '2011-01-17 21:40:20.100000' ,'2011-01-17 21:40:20.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','time_occurred>2011-01-16','-f','csv'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = 'rec_id,event_id,time_occurred,time_logged,src_comp,src_loc,src_loc_type,rpt_comp,rpt_loc,rpt_loc_type,event_cnt,elapsed_time5,Event 05,{0},{1},CNM,MB-SL1-ET1-PT2,C,,,,,6,Event 06,{2},{3},CNM,MB-SL1-ET1-PT2,C,,,,,'
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:16.100000', '2011-01-17 21:40:16.100000', '2011-01-17 21:40:20.100000', '2011-01-17 21:40:20.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','time_occurred>2011-01-17-21:40:12','-f','csv'], exp_good_msg=tmp_good_msg)
        
    def test_tllalert_time(self):
        ''' Test timestamp values for tllsalert '''
        self.assertCmdFails([LSALERT,'--query','creation_time=2011-01-33'], exp_err_msg='Usage: tllsalert [options]tllsalert: error: Invalid timestamp for creation_time: 2011-01-33')
        tmp_good_msg = 'rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data4,Alert US,{0},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,5,Alert 03,{1},E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test6,Alert US,{2},W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:25.437000', '2011-01-17 16:14:26.453000', '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'--query','creation_time>2011-01-17-16:14:21','-f','csv'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = 'rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data1,Alert US,{0},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,3,Alert US,{1},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,4,Alert US,{2},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,5,Alert 03,{3},E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test6,Alert US,{4},W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', '2011-01-17 16:14:21.437000', '2011-01-17 16:14:25.437000', '2011-01-17 16:14:26.453000', '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'--query','creation_time>2011-01-16','-f','csv'], exp_good_msg=tmp_good_msg)
        
    def test_teal_time(self):
        ''' Test timestamp values for teal '''
        os.environ['TEAL_DATA_DIR'] = self.teal_data_dir
        self.assertCmdFails([TEAL,'--historic','--query','time_occurred=2011-01-33','-c','data/tlcommands_test/test_historic.conf'], exp_err_msg='Usage: teal.py [options]teal.py: error: Invalid timestamp for time_occurred: 2011-01-33')
        self.assertCmdFails([TEAL,'--historic','--query','time_logged=2011-13-17','-c','data/tlcommands_test/test_historic.conf'], exp_err_msg='Usage: teal.py [options]teal.py: error: Invalid timestamp for time_logged: 2011-13-17')
        self.assertCmdWorks([TEAL,'--historic','--query','time_occurred>2011-01-17-16:14:21','-c','data/tlcommands_test/test_historic.conf','--msglevel=debug'], 
                         exp_good_msg='Demo:Alert 02(1) 2011-02-20 15:13:06.052000 None Demo1Analyzer',
                         exp_good_msg_ranges=[(0,17),(43,-1)])  # Only check before and after timestamp 
        
    def test_tlrmevent_checkpoint(self):
        ''' Test that tlrmevent interacts correctly with the checkpoints '''
        # Get rid of all of the alerts 
        self.assertCmdWorks([CHALERT,'--id','1','--state','close'])
        self.assertCmdWorks([CHALERT,'--id','3','--state','close'])
        self.assertCmdWorks([CHALERT,'--id','4','--state','close'])
        self.assertCmdWorks([CHALERT,'--id','5','--state','close'])
        self.assertCmdWorks([CHALERT,'--id','6','--state','close'])
        self.assertCmdWorks([RMALERT], exp_good_msg='5 unique alerts removed', alt_exp_good_msgs=['6 unique alerts removed'])
        # Start TEAL so we can add some checkpoints!
        t = Teal(None)
        # DB was cleared ... so no checkpoints in table
        e_ckpt = EventCheckpoint('test')
        # Set the checkpoint to the first event ... so NOTHING can be removed
        e_ckpt.set_checkpoint(1)
        # Try removing anyway 
        self.assertCmdWorks([RMEVENT], exp_good_msg='0 events removed')
        # Fails ... but we get a rc of 0
        self.assertCmdFails([RMEVENT, '--id','2'], exp_rc=0,
                            exp_good_msg='0 events removed', 
                            exp_err_msg="Event '2' cannot be removed."
                            + '\tReason: Event is within the checkpointed events.  (event rec_id 2 >= checkpoint rec_id 1)')
        # Set the checkpoint to the fourth event
        e_ckpt.set_checkpoint(4)
        # Should be able to remove the 2nd one now
        self.assertCmdFails([RMEVENT, '--id','2'], exp_rc=0,
                            exp_good_msg='1 event removed')
        # Should be able to remove 1 and 3 
        self.assertCmdFails([RMEVENT], exp_rc=0,
                            exp_good_msg='2 events removed')
        # Checkpoint needs to be removed so don't break
        #e_ckpt.set_checkpoint(None)
        t.shutdown()
                
    def test_commands(self):
        ''' Try all the commands '''
        # NOTE:
        # CMVC does not allow checking in of very long lines
        # use + to separate long strings
        # Close the first event (and its duplicate)
        self.assertCmdWorks([CHALERT,'--id','1','--state','close'], exp_good_msg='')
        tmp_good_msg = '1: Alert US {0} C:MB-SL1-ET1-PT2    2: Alert US {1} C:MB-SL1-ET1-PT2'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', '2011-01-17 16:14:17.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-c','-d'], exp_good_msg=tmp_good_msg)
        # Check option interaction 
        self.assertCmdFails([LSALERT,'-c','-d','-x'], exp_err_msg="Usage: tllsalert [options]tllsalert: error: Cannot specify --xref with 'brief' formatting")
        tmp_good_msg = '===================================================rec_id : 1alert_id : Alert UScreation_time : {0}severity : Wurgency : Nevent_loc : MB-SL1-ET1-PT2event_loc_type : Cfru_loc : Nonerecommendation : Recommend doing somethingreason : no value' \
        + 'src_name : AnalyzerTest057astate : 2raw_data : NoneCondition Alerts: []Condition Events: []Duplicate Alerts: [2]Suppression Alerts: []Suppression Events: [1,2]Duplicate Of Alerts: []===================================================rec_id : 2alert_id : Alert UScreation_time : {1}severity : Wurgency : N' \
        + 'event_loc : MB-SL1-ET1-PT2event_loc_type : Cfru_loc : Nonerecommendation : Recommend doing somethingreason : no valuesrc_name : AnalyzerTest057astate : 2raw_data : NoneCondition Alerts: []Condition Events: []Duplicate Alerts: []Suppression Alerts: []Suppression Events: [2]Duplicate Of Alerts: [1]' 
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', '2011-01-17 16:14:17.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-c','-d','-x','-f','text','-w'], exp_good_msg=tmp_good_msg)
        tmp_good_msg ='rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data,associations,xref1,Alert US,{0},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,2,' \
        + ',"{{\'D:A\': \'[2]\', \'C:E\': \'[]\', \'C:A\': \'[]\', \'S:A\': \'[]\', \'S:E\': \'[1,2]\'}}",{{\'DO:A\': \'[]\'}}2,Alert US,{1},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,2,,"{{\'D:A\': \'[]\', \'C:E\': \'[]\', \'C:A\': \'[]\', \'S:A\': \'[]\', \'S:E\': \'[2]\'}}",{{\'DO:A\': \'[1]\'}}'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', '2011-01-17 16:14:17.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-c','-d','-x','-f','csv', '-w'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '{{"associations": {{"D:A": "[2]", "C:E": "[]", "C:A": "[]", "S:A": "[]", "S:E": "[1,2]"}}, "xref": {{"DO:A": "[]"}}, "severity": "W", "state": 2, "rec_id": 1, "creation_time": "{0}", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2",' \
        + ' "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}}{{"associations": {{"D:A": "[]", "C:E": "[]", "C:A": "[]", "S:A": "[]", "S:E": "[2]"}}, "xref": {{"DO:A": "[1]"}}, "severity": "W", "state": 2, "rec_id": 2, "creation_time": "{1}",' \
        + ' "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}}'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', '2011-01-17 16:14:17.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-c','-d','-x','-f','json', '-w'], exp_good_msg=tmp_good_msg)
        # Attempt to remove the events by id -- all are associated with alerts
        self.assertCmdWorks([RMEVENT,'--id','1,2,3,4,5,6'], exp_good_msg="0 events removed", exp_err_msg="Event '1' cannot be removed.\tReason: Event is associated with Alert '1'Event '2' cannot be removed.\tReason: Event is associated with Alert '1'\tReason: Event is associated with Alert '2'Event '3' cannot be removed.\tReason: Event is associated with Alert '3'Event '4' cannot be removed.\tReason: Event is associated with Alert '4'Event '5' cannot be removed.\tReason: Event is associated with Alert '5'Event '6' cannot be removed.\tReason: Event is associated with Alert '6'")
        self.assertCmdWorks([RMEVENT,'--older-than','2011-01-18'], exp_good_msg='0 events removed')
        self.assertCmdWorks([RMALERT,'--ids','4,5,36'], exp_good_msg="0 unique alerts removed", exp_err_msg="Alert '4' cannot be removed.\tReason: Alert is not closedAlert '5' cannot be removed.\tReason: Alert is not closed")
        self.assertCmdWorks([RMALERT,'--id','1'], exp_good_msg='1 unique alert removed')
        tmp_good_msg = 'rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data\r\n3,Alert US,{0},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n' \
        + '4,Alert US,{1},W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n5,Alert 03,{2},E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test\r\n6,Alert US,{3},W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:21.437000', '2011-01-17 16:14:25.437000', '2011-01-17 16:14:26.453000', '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-f','csv'], exp_good_msg=tmp_good_msg)
        self.assertCmdWorks([RMEVENT], exp_good_msg='2 events removed')
        self.assertCmdWorks([LSEVENT,'-q','rec_id=1,2'])
        # Check option interaction check
        self.assertCmdFails([LSEVENT,'-q','rec_id=1,2','-x'], exp_err_msg="Usage: tllsevent [options]tllsevent: error: Cannot use --xref option with 'brief' format")
        self.assertCmdWorks([LSEVENT,'-q','rec_id=1,2','-f','text', '-x'])
        self.assertCmdWorks([CHALERT,'--id','5','--state','close'])
        self.assertCmdWorks([CHALERT,'--id','6','--state','close'])
        tmp_good_msg = '===================================================\r\nrec_id : 5\r\nalert_id : Alert 03\r\ncreation_time : {0}\r\nseverity : E\r\nurgency : I\r\nevent_loc : MB-SL1-ET1-PT2\r\nevent_loc_type : C\r\nfru_loc : fru_loc2\r\nrecommendation : try again\r\nreason : reason from config1\r\nsrc_name : AnalyzerTest057a\r\nstate : 2\r\nraw_data : This is another test\r\n===================================================\r\n' \
        + 'rec_id : 6\r\nalert_id : Alert US\r\ncreation_time : {1}\r\nseverity : W\r\nurgency : N\r\nevent_loc : MB-SL1-ET1-PT1\r\nevent_loc_type : C\r\nfru_loc : None\r\nrecommendation : Recommend doing something\r\nreason : no value\r\nsrc_name : AnalyzerTest057a\r\nstate : 2\r\nraw_data : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:26.453000', '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-q','rec_id=5,6','-f','text','-c'], exp_good_msg=tmp_good_msg)
        self.assertCmdWorks([RMALERT,'--older-than','2011-01-18'], exp_good_msg='2 unique alerts removed')
        tmp_good_msg = '{{"severity": "W", "state": 1, "rec_id": 3, "creation_time": "{0}", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}}\r\n{{"severity": "W", "state": 1, "rec_id": 4, "creation_time": "{1}", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}}'
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:21.437000', '2011-01-17 16:14:25.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-f','json'], exp_good_msg=tmp_good_msg)
        self.assertCmdWorks([RMEVENT,'--older-than','2011-01-18'], exp_good_msg='2 events removed')
        tmp_good_msg = '{{"src_comp": "CNM", "rpt_loc_type": null, "event_id": "Event 03", "src_loc_type": "C", "time_occurred": "{0}", "rec_id": 3, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, "rpt_comp": null, "time_logged": "{1}", "src_loc": "MB-SL1-ET1-PT2"}}\r\n{{"src_comp": "CNM", "rpt_loc_type": null, "event_id": "Event 04", "src_loc_type": "C", "time_occurred": "{2}", "rec_id": 4, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, "rpt_comp": null, "time_logged": "{3}", "src_loc": "MB-SL1-ET1-PT2"}}\r\n'
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:08.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:12.100000', '2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'-f','json'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 3\r\nevent_id : Event 03 \r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : CNM\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'   \
        + '===================================================\r\nrec_id : 4\r\nevent_id : Event 04 \r\ntime_occurred : {2}\r\ntime_logged : {3}\r\nsrc_comp : CNM\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n' 
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:08.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:12.100000', '2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'-f','text'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================rec_id : 3event_id : Event 03 time_occurred : {0}time_logged : {1}src_comp : CNMsrc_loc : MB-SL1-ET1-PT2src_loc_type : Crpt_comp : Nonerpt_loc : Nonerpt_loc_type : Noneevent_cnt : Noneelapsed_time : NoneCondition For Alerts: []Suppressed By Alerts: [3]===================================================rec_id : 4event_id : Event 04 time_occurred : {2}time_logged : {3}'  \
        + 'src_comp : CNMsrc_loc : MB-SL1-ET1-PT2src_loc_type : Crpt_comp : Nonerpt_loc : Nonerpt_loc_type : Noneevent_cnt : Noneelapsed_time : NoneCondition For Alerts: [4]Suppressed By Alerts: []'
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:08.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'-f','text','-x'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '{{"src_comp": "CNM", "rpt_loc_type": null, "xref": {{"CF:A": "[]", "SB:A": "[3]"}}, "event_id": "Event 03", "src_loc_type": "C", "time_occurred": "{0}", "rec_id": 3, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, "rpt_comp": null, "time_logged": "{1}", "src_loc": "MB-SL1-ET1-PT2"}}{{"src_comp": "CNM", "rpt_loc_type": null, "xref": {{"CF:A": "[4]", "SB:A": "[]"}}, "event_id": "Event 04", "src_loc_type": "C", "time_occurred": "{2}", "rec_id": 4, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, ' \
        + '"rpt_comp": null, "time_logged": "{3}", "src_loc": "MB-SL1-ET1-PT2"}}' 
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:08.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'-f','json','--xref'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = 'rec_id,event_id,time_occurred,time_logged,src_comp,src_loc,src_loc_type,rpt_comp,rpt_loc,rpt_loc_type,event_cnt,elapsed_time3,Event 03,{0},{1},CNM,MB-SL1-ET1-PT2,C,,,,,,"{{\'CF:A\': \'[]\', \'SB:A\': \'[3]\'}}"4,Event 04,{2},{3},CNM,MB-SL1-ET1-PT2,C,,,,,,"{{\'CF:A\': \'[4]\', \'SB:A\': \'[]\'}}"'
        tmp_dts = apply_time_pattern(['2011-01-17 21:40:08.100000', '2011-01-17 21:40:08.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'-f','csv','-x'], exp_good_msg=tmp_good_msg)
    
    def test_help(self):
        ''' Verify help text displays correctly '''
        self.assertCmdWorks([TEAL,'-h'], exp_good_msg='Usage: teal.py [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-c CONFIG_FILE, --configfile=CONFIG_FILE                        fully qualified TEAL config file/directory - optional  '
        + '-l LOG_FILE, --logfile=LOG_FILE                        fully qualified log file  '
        + '-m MSG_LEVEL, --msglevel=MSG_LEVEL                        <debug | info | warning | error | critical> - optional                        [default: info]  '
        + '--realtime            Run TEAL in realtime mode  '
        + '-d, --daemon          run as a daemon  '
        + '-r RESTART, --restart=RESTART                        <now | begin | recovery | lastproc> [default:                        recovery]  '
        + '--historic            Run TEAL in historic mode  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of events.  '
        + '--commit              Commit alerts in historic mode [default=False]  '
        + '--occurred            Use time occurred instead of time logged                        [default=False]')
        self.assertCmdWorks([TEAL,'--help'], exp_good_msg='Usage: teal.py [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-c CONFIG_FILE, --configfile=CONFIG_FILE                        fully qualified TEAL config file/directory - optional  '
        + '-l LOG_FILE, --logfile=LOG_FILE                        fully qualified log file  '
        + '-m MSG_LEVEL, --msglevel=MSG_LEVEL                        <debug | info | warning | error | critical> - optional                        [default: info]  '
        + '--realtime            Run TEAL in realtime mode  '
        + '-d, --daemon          run as a daemon  '
        + '-r RESTART, --restart=RESTART                        <now | begin | recovery | lastproc> [default:                        recovery]  '
        + '--historic            Run TEAL in historic mode  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of events.  '
        + '--commit              Commit alerts in historic mode [default=False]  '
        + '--occurred            Use time occurred instead of time logged                        [default=False]')
        
        self.assertCmdWorks([CHALERT,'-h'], exp_good_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-s STATE, --state=STATE                        The new alert state. (close is the only valid value at                        this time.  '
        + '-i REC_ID, --id=REC_ID                        The record id of the alert. (use tllsalert)  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of alerts                        listed. See list of valid values below  '
        + '-l LOCATIONS, --locations=LOCATIONS                        Change all alerts at the specified locations  '  
        + '-c, --contained       Change alerts at all contained sublocations of the                        specified locations  '
        + '-d DELIM, --delimiter=DELIM                        Delimiter between specified locations. Cannot be space                        (default: comma)'
        + 'Valid query values and their operations and formats:    '
        + 'alert_id      - =           - A single id or a comma-separated list of ids (equals-only)'
        + 'creation_time - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:S'
        + 'Sseverity      - =           - The severity level, listed in order of severity:                                  F=fatal, E=error, W=warning, I=info (equals-only)'
        + 'urgency       - =           - The urgency of the alert, listed in order of urgency:                             I=immediate, S=schedule, N=normal, D=defer, O=optional                (equals-only)'
        + 'event_loc     - =           - A location in the format <location type>:<location>.                               The location is optional; otherwise all events                               with the same location type will be included'
        + 'event_scope   - =           - A scoping value for the specified reporting location type'
        + 'src_name      - =           - A single value or a comma-separated list of values')
        self.assertCmdWorks([CHALERT,'--help'], exp_good_msg='Usage: tlchalert -s close -i <rec_id> | -q <query string> | -l <locations> [-c|-d <delim>]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-s STATE, --state=STATE                        The new alert state. (close is the only valid value at                        this time.  '
        + '-i REC_ID, --id=REC_ID                        The record id of the alert. (use tllsalert)  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of alerts                        listed. See list of valid values below  '
        + '-l LOCATIONS, --locations=LOCATIONS                        Change all alerts at the specified locations  '  
        + '-c, --contained       Change alerts at all contained sublocations of the                        specified locations  '
        + '-d DELIM, --delimiter=DELIM                        Delimiter between specified locations. Cannot be space                        (default: comma)'
        + 'Valid query values and their operations and formats:    '
        + 'alert_id      - =           - A single id or a comma-separated list of ids (equals-only)'
        + 'creation_time - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:S'
        + 'Sseverity      - =           - The severity level, listed in order of severity:                                  F=fatal, E=error, W=warning, I=info (equals-only)'
        + 'urgency       - =           - The urgency of the alert, listed in order of urgency:                             I=immediate, S=schedule, N=normal, D=defer, O=optional                (equals-only)'
        + 'event_loc     - =           - A location in the format <location type>:<location>.                               The location is optional; otherwise all events                               with the same location type will be included'
        + 'event_scope   - =           - A scoping value for the specified reporting location type'
        + 'src_name      - =           - A single value or a comma-separated list of values')
        
        self.assertCmdWorks([LSALERT,'-h'], exp_good_msg='Usage: tllsalert [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of alerts                        listed. See list of valid values below  '
        + '-f OUTPUT_FORMAT, --format=OUTPUT_FORMAT                        Output format of alert: json,csv,text [default =                        brief]  '
        + '-w, --with-assoc      Print the associated events and alerts for the                        matching alert  '
        + '-a, --all             Print all open and closed alerts  '
        + '-c, --closed          Print only closed alerts  '
        + '-d, --with-dups       Print the duplicate alerts also  '
        + '-x, --xref            Include cross reference data in output' 
        + 'Valid query values and their operations and formats:    '
        + 'rec_id        - =           - A single id or a comma-separated list of ids (equals-only)'
        + 'alert_id      - =           - A single id or a comma-separated list of ids (equals-only)'
        + 'creation_time - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS'
        + 'severity      - =           - The severity level, listed in order of severity:                              \tF=fatal, E=error, W=warning, I=info (equals-only)'
        + 'urgency       - =           - The urgency of the alert, listed in order of urgency:\t                     \tI=immediate, S=schedule, N=normal, D=defer, O=optional\t\t\t\t(equals-only)'
        + 'event_loc     - =           - A location in the format <location type>:<location>.                               The location is optional; otherwise all events                               with the same location type will be included'
        + 'event_scope   - =           - A scoping value for the specified reporting location type'
        + 'src_name      - =           - A single value or a comma-separated list of values')

        self.assertCmdWorks([LSALERT,'--help'], exp_good_msg='Usage: tllsalert [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of alerts                        listed. See list of valid values below  '
        + '-f OUTPUT_FORMAT, --format=OUTPUT_FORMAT                        Output format of alert: json,csv,text [default =                        brief]  '
        + '-w, --with-assoc      Print the associated events and alerts for the                        matching alert  '
        + '-a, --all             Print all open and closed alerts  '
        + '-c, --closed          Print only closed alerts  '
        + '-d, --with-dups       Print the duplicate alerts also  '
        + '-x, --xref            Include cross reference data in output' 
        + 'Valid query values and their operations and formats:    '
        + 'rec_id        - =           - A single id or a comma-separated list of ids (equals-only)'
        + 'alert_id      - =           - A single id or a comma-separated list of ids (equals-only)'
        + 'creation_time - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS'
        + 'severity      - =           - The severity level, listed in order of severity:                              \tF=fatal, E=error, W=warning, I=info (equals-only)'
        + 'urgency       - =           - The urgency of the alert, listed in order of urgency:\t                     \tI=immediate, S=schedule, N=normal, D=defer, O=optional\t\t\t\t(equals-only)'
        + 'event_loc     - =           - A location in the format <location type>:<location>.                               The location is optional; otherwise all events                               with the same location type will be included'
        + 'event_scope   - =           - A scoping value for the specified reporting location type'
        + 'src_name      - =           - A single value or a comma-separated list of values')

        self.assertCmdWorks([LSCKPT,'-h'], exp_good_msg='Usage: tllsckpt [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-n NAME, --name=NAME  Name of checkpoint to list  '
        + '-f OUTPUT_FORMAT, --format=OUTPUT_FORMAT                        Output format of checkpoints: json,csv,text [default =                        brief]')
        self.assertCmdWorks([LSCKPT,'--help'], exp_good_msg='Usage: tllsckpt [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-n NAME, --name=NAME  Name of checkpoint to list  '
        + '-f OUTPUT_FORMAT, --format=OUTPUT_FORMAT                        Output format of checkpoints: json,csv,text [default =                        brief]')
        
        self.assertCmdWorks([LSEVENT,'-h'], exp_good_msg='Usage: tllsevent [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of events                        listed. See list of valid values below '
        +' -f OUTPUT_FORMAT, --format=OUTPUT_FORMAT                        Output format of event: json,csv,text [default =                        brief]  '
        + '-e, --extended        Include extended event data in output  '
        + '-x, --xref            Include cross reference data in output' 
        + 'Valid query values and their operations and formats:    '
        + 'rec_id        - =,<.>,>=,<= - A single id or a comma-separated list of ids (equals-only)'
        + 'event_id      - =           - A single id or comma-separated list of event ids'
        + 'time_occurred - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS'
        + 'time_logged   - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS'
        + 'src_comp      - =           - A single component or a comma-separated list of components'
        + 'src_loc       - =           - A location in the format <location type>:<location>. location can                               be omitted to return all locations of the specified type'
        + 'src_scope     - =           - A scoping value for the specified reporting location type'
        + 'rpt_comp      - =           - A single component or a comma-separated list of components'
        + 'rpt_loc       - =           - A location in the format <location type>:<location>. location                               can be omitted to return all locations of the specified type'
        + 'rpt_scope     - =           - A scoping value for the specified reporting location type')
        self.assertCmdWorks([LSEVENT,'--help'], exp_good_msg='Usage: tllsevent [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-q QUERY, --query=QUERY                        Query parameters used to limit the range of events                        listed. See list of valid values below '
        +' -f OUTPUT_FORMAT, --format=OUTPUT_FORMAT                        Output format of event: json,csv,text [default =                        brief]  '
        + '-e, --extended        Include extended event data in output  '
        + '-x, --xref            Include cross reference data in output' 
        + 'Valid query values and their operations and formats:    '
        + 'rec_id        - =,<.>,>=,<= - A single id or a comma-separated list of ids (equals-only)'
        + 'event_id      - =           - A single id or comma-separated list of event ids'
        + 'time_occurred - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS'
        + 'time_logged   - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS'
        + 'src_comp      - =           - A single component or a comma-separated list of components'
        + 'src_loc       - =           - A location in the format <location type>:<location>. location can                               be omitted to return all locations of the specified type'
        + 'src_scope     - =           - A scoping value for the specified reporting location type'
        + 'rpt_comp      - =           - A single component or a comma-separated list of components'
        + 'rpt_loc       - =           - A location in the format <location type>:<location>. location                               can be omitted to return all locations of the specified type'
        + 'rpt_scope     - =           - A scoping value for the specified reporting location type')
        
        self.assertCmdWorks([VFYRULE,'-h'], exp_good_msg='Usage: tlvfyrule [options] rule-fileOptions:  '
        + '-h, --help            show this help message and exit  '
        + '-m METADATA, --metadata=METADATA                        verify the rule using this alert metadata                        specification  '
        + '-a, --alert           verifying a rule that also processes alerts  '
        + '-c CONF_ATTR, --conf_attr=CONF_ATTR                        verify the rule assuming these configuration                        attributes  '
        + '-x CREF, --cref=CREF  if valid provide a cross reference of id usage')
        self.assertCmdWorks([VFYRULE,'--help'], exp_good_msg='Usage: tlvfyrule [options] rule-fileOptions:  '
        + '-h, --help            show this help message and exit  '
        + '-m METADATA, --metadata=METADATA                        verify the rule using this alert metadata                        specification  '
        + '-a, --alert           verifying a rule that also processes alerts  '
        + '-c CONF_ATTR, --conf_attr=CONF_ATTR                        verify the rule assuming these configuration                        attributes  '
        + '-x CREF, --cref=CREF  if valid provide a cross reference of id usage')

    def test_tlcommand_query_fail(self):
        ''' Try invalid query options for tllsevent and teal commands '''
        # tllsevent and teal options
        # rec_id        - =,<.>,>=,<= - A single id or a comma-separated list of ids (equals-only)
        # event_id      - =           - A single id or comma-separated list of event ids
        # time_occurred - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS
        # time_logged   - =,<.>,>=,<= - A time value in the format YYYY-MM-DD-HH:MM:SS
        # src_comp      - =           - A single component or a comma-separated list of components
        # src_loc       - =           - A location in the format <location type>:<location>. location can be omitted to return all locations of the specified type
        # src_scope     - =           - A scoping value for the specified reporting location type
        # rpt_comp      - =           - A single component or a comma-separated list of components
        # rpt_loc       - =           - A location in the format <location type>:<location>. location can be omitted to return all locations of the specified type
        # rpt_scope     - =           - A scoping value for the specified reporting location type
        self.assertCmdFails([LSEVENT,'-q','recid=1'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid field specified: recid')
        self.assertCmdFails([LSEVENT,'-q','rec_id'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid query string specified')
        self.assertCmdFails([LSEVENT,'-q','rec_id=1,'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid value(s) for rec_id: 1,')
        self.assertCmdFails([LSEVENT,'-q','rec_id=b'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid value(s) for rec_id: b')
        self.assertCmdFails([LSEVENT,'-q','rec_id!=1'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid query string specified')
        
        self.assertCmdFails([LSEVENT,'-q','event_id>1'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid operation specified for field "event_id": >')
        self.assertCmdFails([LSEVENT,'-q','event_id=BD000000,'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Invalid value(s) for event_id: BD000000,')
        self.assertCmdFails([LSEVENT,'-q','src_scope=frame'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: src_scope can not be specified without a valid src_loc')
        self.assertCmdFails([LSEVENT,'-q','rpt_scope=frame'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: rpt_scope can not be specified without a valid rpt_loc')

        self.assertCmdFails([LSEVENT,'-q','event_id=\'BD000000\''], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Query string must not contain quotes')
        self.assertCmdFails([LSEVENT,'-q','event_id="BD000000"'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Query string must not contain quotes')

        self.assertCmdFails([LSEVENT,'-q','rpt_loc=C:MB'], exp_err_msg='Usage: tllsevent [options]tllsevent: error: Location specification "rpt_loc" is invalid')
        self.assertCmdFails([TEAL,'-q','rpt_loc=C:MB'], exp_err_msg='Usage: teal.py [options]teal.py: error: Location specification "rpt_loc" is invalid')

        self.assertCmdFails([TEAL,'-q','time_occurred=2011:11:11'], exp_err_msg='Usage: teal.py [options]teal.py: error: Invalid timestamp for time_occurred: 2011:11:11')
        self.assertCmdFails([TEAL,'-q','time_logged=2011-13'], exp_err_msg='Usage: teal.py [options]teal.py: error: Invalid timestamp for time_logged: 2011-13')


class TealCommandLineTest_tlrmalert(TealTestCase):

    def setUp(self):
        t = Teal('data/tlcommands_test/test.conf', data_only=True)
        global RMALERT, CHALERT, LSALERT, RMEVENT, LSEVENT, LSCKPT, TEAL, VFYRULE
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        RMALERT = os.path.join(teal_path,'bin/tlrmalert')
        CHALERT = os.path.join(teal_path,'bin/tlchalert')
        LSALERT = os.path.join(teal_path,'bin/tllsalert')
        RMEVENT = os.path.join(teal_path,'bin/tlrmevent')
        LSEVENT = os.path.join(teal_path,'bin/tllsevent')
        LSCKPT = os.path.join(teal_path, 'bin/tllsckpt')
        TEAL    = os.path.join(teal_path,'ibm/teal/teal.py')
        VFYRULE = os.path.join(teal_path, 'bin/tlvfyrule')
        t.shutdown()
        
        self.time_pattern = get_table_date_time_pattern()

        self.prepare_db()
        self._add_journal('data/tlcommands_test/events_001.json')
        self._add_journal('data/tlcommands_test/alerts_002.json')  # Note different from class above
        
        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR', '/opt/teal'), 'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)

    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)
    
    def _add_journal(self, json_file):
        ''' Load the alert DB from the journal JSON file '''
        t = Teal('data/tlcommands_test/test.conf')
        # Alerts
        ja = Journal('temp_journal', file=json_file)
        ja.insert_in_db(truncate=False, no_delay=True)
        t.shutdown()

    def test_tlrmalert_dup(self):
        ''' Test special case of tlrmalert handling duplicates '''
        self.assertCmdWorks([CHALERT,'--id','1','--state','close'], exp_good_msg='')
        self.assertCmdFails([CHALERT,'--id','2','--state','close'], exp_err_msg="Cannot close alert. Reason: rc = 2: 'Current alert state does not allow this operation'", exp_rc=1)
        self.assertCmdWorks([CHALERT,'--id','3','--state','close'], exp_good_msg='')
        self.assertCmdFails([CHALERT,'--id','4','--state','close'], exp_err_msg="Cannot close alert. Reason: rc = 2: 'Current alert state does not allow this operation'", exp_rc=1)
        self.assertCmdWorks([CHALERT,'--id','5','--state','close'], exp_good_msg='')
        self.assertCmdFails([CHALERT,'--id','6','--state','close'], exp_err_msg="Cannot close alert. Reason: rc = 2: 'Current alert state does not allow this operation'", exp_rc=1)
        self.assertCmdWorks([RMALERT,'--id','1,2,4'], exp_good_msg='1 unique alert removed', exp_err_msg="Alert '4' cannot be removed.\tReason: Alert is associated with Alert '3'")
        tmp_good_msg = '3: Alert US {0} C:MB-SL1-ET1-PT2    4: Alert US {1} C:MB-SL1-ET1-PT2    5: Alert 03 {2} C:MB-SL1-ET1-PT2    6: Alert US {3} C:MB-SL1-ET1-PT1'       
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:21.437000', '2011-01-17 16:14:25.437000', '2011-01-17 16:14:26.453000', '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-c','-d'], exp_good_msg=tmp_good_msg)


class TealCommandLineTest_tlchalert(TealTestCase):
    def setUp(self):
        t = Teal('data/tlcommands_test/test.conf', data_only=True)
        global RMALERT, CHALERT, LSALERT, RMEVENT, LSEVENT, LSCKPT, TEAL, VFYRULE
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        CHALERT = os.path.join(teal_path,'bin/tlchalert')
        LSALERT = os.path.join(teal_path,'bin/tllsalert')
        t.shutdown()
        
        self.time_pattern = get_table_date_time_pattern()

        self.prepare_db()
        self._add_journal('data/tlcommands_test/events_001.json')
        self._add_journal('data/tlcommands_test/alerts_003.json')
        
        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR', '/opt/teal'), 'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)

    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)
    
    def _add_journal(self, json_file):
        ''' Load the alert DB from the journal JSON file '''
        t = Teal('data/tlcommands_test/test.conf')
        # Alerts
        ja = Journal('temp_journal', file=json_file)
        ja.insert_in_db(truncate=False, no_delay=True)
        t.shutdown()

    def test_tlchalert_qry(self):
        ''' Test tlchalert query string support '''
        # Close with different severity than others
        self.assertCmdWorks([CHALERT,'--state','close','--query','severity=E'], exp_good_msg='')

        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    3: Alert_US {2} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {3} C:MB-SL1-ET2-PT3')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                                                         
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg=tmp_good_msg)
        
        tmp_good_msg =(    '5: Alert_03 {0} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {1} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                                                                 
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

        # Close with split between primary & duplicate alerts where duplicate is in query range
        self.assertCmdWorks([CHALERT,'--state','close','--query','creation_time>2011-01-17-16:14:15'], exp_good_msg='')
        
        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                                                         
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg=tmp_good_msg)
        
        tmp_good_msg =(    '3: Alert_US {0} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {1} C:MB-SL1-ET2-PT3' +
                       '    5: Alert_03 {2} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {3} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000', 
                                      '2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

        # Close with split between primary & duplicate where duplicate is not in query range
        self.assertCmdWorks([CHALERT,'--state','close','--query','creation_time<2011-01-17-16:14:15'], exp_good_msg='')
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg='')
        
        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    3: Alert_US {2} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {3} C:MB-SL1-ET2-PT3' +
                       '    5: Alert_03 {4} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {5} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000',
                                      '2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)        
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

    def test_tlchalert_qryloc(self):
        ''' Test tlchalert based on location query '''
        self.assertCmdWorks([CHALERT,'--state','close','-l','MB-SL2-ET1-PT2'], exp_good_msg='')
        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    3: Alert_US {2} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {3} C:MB-SL1-ET2-PT3')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)        
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg=tmp_good_msg)

        tmp_good_msg =(    '5: Alert_03 {0} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {1} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)        
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

        self.assertCmdWorks([CHALERT,'--state','close','-l','MB-SL1-ET1-PT2,MB-SL1-ET2-PT3'], exp_good_msg='')
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg='')
        
        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    3: Alert_US {2} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {3} C:MB-SL1-ET2-PT3' +
                       '    5: Alert_03 {4} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {5} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000',
                                      '2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

    def test_tlchalert_qryloc_delim(self):
        ''' Test tlchalert based on location query '''
        self.assertCmdWorks([CHALERT,'--state','close','-l','MB-SL1-ET1-PT2@MB-SL2-ET1-PT2','-d','@'], exp_good_msg='')

        tmp_good_msg =(    '3: Alert_US {0} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {1} C:MB-SL1-ET2-PT3')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg=tmp_good_msg)
        
        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    5: Alert_03 {2} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {3} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                        
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

    def test_tlchalert_qryloc_contained(self):
        ''' Test tlchalert based on location query with containment '''
        self.assertCmdWorks([CHALERT,'--state','close','-l','MB-SL1','-c'], exp_good_msg='')
        
        tmp_good_msg =(    '5: Alert_03 {0} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {1} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg=tmp_good_msg)

        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    3: Alert_US {2} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {3} C:MB-SL1-ET2-PT3')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

    def test_tlchalert_qryloc_contained_delim(self):
        ''' Test tlchalert based on location query with delimiter and containment '''
        self.assertCmdWorks([CHALERT,'--state','close','-l','MB-SL1-ET1@MB-SL2','-c','-d','@'], exp_good_msg='')
        
        tmp_good_msg =(    '3: Alert_US {0} C:MB-SL1-ET2-PT3' +
                       '    4: Alert_US {1} C:MB-SL1-ET2-PT3')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:21.437000', 
                                      '2011-01-17 16:14:25.437000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                
        self.assertCmdWorks([LSALERT,'-d'], exp_good_msg=tmp_good_msg)
        
        tmp_good_msg =(    '1: Alert_US {0} C:MB-SL1-ET1-PT2' +
                       '    2: Alert_US {1} C:MB-SL1-ET1-PT2' +
                       '    5: Alert_03 {2} C:MB-SL2-ET1-PT2' +
                       '    6: Alert_US {3} C:MB-SL2-ET1-PT2')
        tmp_dts = apply_time_pattern(['2011-01-17 16:14:13.437000', 
                                      '2011-01-17 16:14:17.437000', 
                                      '2011-01-17 16:14:26.453000', 
                                      '2011-01-17 16:14:33.468000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)                
        self.assertCmdWorks([LSALERT,'-d','-c'], exp_good_msg=tmp_good_msg)

class TealCommandLineTest_tllsevent_metadata_msg(TealTestCase):

    def setUp(self):
        t = Teal('data/tlcommands_test/test.conf', data_only=True)
        global LSEVENT, TEAL
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        LSEVENT = os.path.join(teal_path,'bin/tllsevent')
        TEAL    = os.path.join(teal_path,'ibm/teal/teal.py')
        t.shutdown()
        
        self.time_pattern = get_table_date_time_pattern()

        self.prepare_db()
        self._add_journal('data/tlcommands_test/events_metadata_001.json')
        
        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR', '/opt/teal'), 'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)
        tmp_cfg_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR', '/'), 'etc')
 
        # If the path doesn't exists, then it is assumed that this is an installed
        # version of TEAL and will use the default CONF path
        if os.path.exists(tmp_cfg_dir):
            # This is a non-standard install (build environment) and will use
            # the etc directory from the ROOT dir
            pass
        else:
            tmp_cfg_dir = '/etc'

        self.teal_cfg_dir = self.force_env('TEAL_CONF_DIR', tmp_cfg_dir)
        
        # Create a logger for logging if the test was not run because the package was missing
        self.create_temp_logger('info')

    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)
        self.restore_env('TEAL_CONF_DIR', self.teal_cfg_dir)
    
    def _add_journal(self, json_file):
        ''' Load the alert DB from the journal JSON file '''
        t = Teal('data/tlcommands_test/test.conf')
        # Alerts
        ja = Journal('temp_journal', file=json_file)
        ja.insert_in_db(truncate=False, no_delay=True)
        t.shutdown()

    def test_tllsevent_ll_metadata_msg(self):
        ''' Test event LL metadata messages for tllsevent '''
        # Verify that the LL package is loaded and return if it is not
        if os.path.exists(os.path.join(os.environ['TEAL_ROOT_DIR'],'ibm','teal','connector','loadleveler.py')) is False:
            registry.get_logger().info('Loadlever package not installed. Skipping test')
            return

        tmp_good_msg = '===================================================\r\nrec_id : 7\r\nevent_id : LL001000 - Schedd daemon down\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : TST\r\nrpt_loc : MB-SL1-ET1-PT3\r\nrpt_loc_type : D\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:00.100000', '2011-01-21 21:40:00.100000', '2011-01-21 21:40:12.100000','2011-01-21 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL001000','-f','text'],exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 8\r\nevent_id : LL001001 - Startd daemon down\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : TST\r\nrpt_loc : MB-SL1-ET1-PT3\r\nrpt_loc_type : D\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:00.100000', '2011-01-21 21:40:00.100000', '2011-01-21 21:40:12.100000','2011-01-21 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts) 
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL001001','-f','text'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 9\r\nevent_id : LL001003 - Central Manager down\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT1\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : 42\r\nelapsed_time : 101\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:04.100000', '2011-01-21 21:40:04.100000', '2011-01-21 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL001003','-f','text'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 10\r\nevent_id : LL001004 - Resource Manager down\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:08.100000', '2011-01-21 21:40:08.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL001004','-f','text'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 11\r\nevent_id : LL001005 - Region Manager down\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:12.100000', '2011-01-21 21:40:12.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL001005','-f','text'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 12\r\nevent_id : LL002001 - Job step rejected\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:16.100000', '2011-01-21 21:40:16.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL002001','-f','text'], exp_good_msg=tmp_good_msg)
        tmp_good_msg = '===================================================\r\nrec_id : 13\r\nevent_id : LL002002 - Job step vacated\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : LL\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:20.100000', '2011-01-21 21:40:20.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=LL002002','-f','text'], exp_good_msg=tmp_good_msg)

    def test_tllsevent_pnsd_metadata_msg(self):
        ''' Test event PNSD metadata messages for tllsevent '''
        # Verify that the PNSD package is loaded and return if it is not
        if os.path.exists(os.path.join(os.environ['TEAL_ROOT_DIR'],'ibm','teal','connector','pnsd.py')) is False:
            registry.get_logger().info('PNSD package not installed. Skipping test')
            return

        tmp_good_msg = '===================================================\r\nrec_id : 14\r\nevent_id : PNSD0001 - Packet retransmit threshold exceeded\r\ntime_occurred : {0}\r\ntime_logged : {1}\r\nsrc_comp : PNSD\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
        tmp_dts = apply_time_pattern(['2011-01-21 21:40:24.100000', '2011-01-21 21:40:24.100000', '2011-01-17 21:40:12.100000','2011-01-17 21:40:12.100000'], self.time_pattern)
        tmp_good_msg = tmp_good_msg.format(*tmp_dts)
        self.assertCmdWorks([LSEVENT,'--query','event_id=PNSD0001','-f','text'], exp_good_msg=tmp_good_msg)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)

