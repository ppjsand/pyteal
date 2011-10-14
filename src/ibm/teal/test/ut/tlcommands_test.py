# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import os
import unittest
from ibm.teal.teal import Teal, registry
from ibm.teal.util.journal import Journal
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.registry import get_service, SERVICE_CHECKPOINT_MGR,\
    register_service
from ibm.teal.checkpoint_mgr import CheckpointMgr, RESTART_MODE_NOW,\
    EventCheckpoint, get_current_min_checkpoint_rec_id

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

        self.prepare_db()
        self._add_journal('data/tlcommands_test/events_001.json')
        self._add_journal('data/tlcommands_test/alerts_001.json')
        
        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR', '/opt/teal'), 'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)
        return

    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)
        return

    
    def _add_journal(self, json_file):
        ''' Load the alert DB from the journal JSON file '''
        t = Teal('data/tlcommands_test/test.conf')
        # Alerts
        ja = Journal('temp_journal', file=json_file)
        ja.insert_in_db(truncate=False, no_delay=True)
        t.shutdown()
        return

    def test_tlchalert_invalid_opts(self):
        ''' Make sure the tlchalert command fails invalid options '''
        # Invalid command arguments
        self.assertCmdFails([CHALERT], exp_err_msg='Usage: tlchalert [options]tlchalert: error: Invalid id specified')
        self.assertCmdFails([CHALERT,'--id'], exp_err_msg='Usage: tlchalert [options]tlchalert: error: --id option requires an argument')
        self.assertCmdFails([CHALERT,'--id', '1'], exp_err_msg='Usage: tlchalert [options]tlchalert: error: Must specify at least one attribute to change')
        self.assertCmdFails([CHALERT,'--id', '1', '--state'], exp_err_msg='Usage: tlchalert [options]tlchalert: error: --state option requires an argument')
        self.assertCmdFails([CHALERT,'--id', '1', '--state', 'reopen'], exp_err_msg="Usage: tlchalert [options]tlchalert: error: option --state: invalid choice: 'reopen' (choose from 'close')")
        self.assertCmdFails([CHALERT,'--id', '1', '--close'], exp_err_msg='Usage: tlchalert [options]tlchalert: error: no such option: --close')

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
        self.assertCmdWorks([LSEVENT,'--query','time_occurred>2011-01-16','-f','csv'], exp_good_msg='rec_id,event_id,time_occurred,time_logged,src_comp,src_loc,src_loc_type,rpt_comp,rpt_loc,rpt_loc_type,event_cnt,elapsed_time1,Event 01,2011-01-17 21:40:00.100000,2011-01-17 21:40:00.100000,CNM,MB-SL3-ET1-PT2,C,,,,,2,Event 02,2011-01-17 21:40:04.100000,2011-01-17 21:40:04.100000,CNM,MB-SL1-ET1-PT1,C,,,,,3,Event 03,2011-01-17 21:40:08.100000,2011-01-17 21:40:08.100000,CNM,MB-SL1-ET1-PT2,C,,,,,4,Event 04,2011-01-17 21:40:12.100000,2011-01-17 21:40:12.100000,CNM,MB-SL1-ET1-PT2,C,,,,,5,Event 05,2011-01-17 21:40:16.100000,2011-01-17 21:40:16.100000,CNM,MB-SL1-ET1-PT2,C,,,,,6,Event 06,2011-01-17 21:40:20.100000,2011-01-17 21:40:20.100000,CNM,MB-SL1-ET1-PT2,C,,,,,')
        self.assertCmdWorks([LSEVENT,'--query','time_occurred>2011-01-17-21:40:12','-f','csv'], exp_good_msg='rec_id,event_id,time_occurred,time_logged,src_comp,src_loc,src_loc_type,rpt_comp,rpt_loc,rpt_loc_type,event_cnt,elapsed_time5,Event 05,2011-01-17 21:40:16.100000,2011-01-17 21:40:16.100000,CNM,MB-SL1-ET1-PT2,C,,,,,6,Event 06,2011-01-17 21:40:20.100000,2011-01-17 21:40:20.100000,CNM,MB-SL1-ET1-PT2,C,,,,,')
        
    def test_tllalert_time(self):
        ''' Test timestamp values for tllsalert '''
        self.assertCmdFails([LSALERT,'--query','creation_time=2011-01-33'], exp_err_msg='Usage: tllsalert [options]tllsalert: error: Invalid timestamp for creation_time: 2011-01-33')
        self.assertCmdWorks([LSALERT,'--query','creation_time>2011-01-17-16:14:21','-f','csv'], exp_good_msg='rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data4,Alert US,2011-01-17 16:14:25.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,5,Alert 03,2011-01-17 16:14:26.453000,E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test6,Alert US,2011-01-17 16:14:33.468000,W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,')
        self.assertCmdWorks([LSALERT,'--query','creation_time>2011-01-16','-f','csv'], exp_good_msg='rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data1,Alert US,2011-01-17 16:14:13.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,3,Alert US,2011-01-17 16:14:21.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,4,Alert US,2011-01-17 16:14:25.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,5,Alert 03,2011-01-17 16:14:26.453000,E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test6,Alert US,2011-01-17 16:14:33.468000,W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,')
        
        
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
        self.assertCmdWorks([RMALERT], exp_good_msg='5 unique alerts removed')
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
        return 
        
    def test_commands(self):
        ''' Try all the commands '''
    # NOTE:
    # CMVC does not allow checking in of very long lines
    # use + to separate long strings
        # Close the first event (and its duplicate)
        self.assertCmdWorks([CHALERT,'--id','1','--state','close'], exp_good_msg='')
        self.assertCmdWorks([LSALERT,'-c','-d'], exp_good_msg='1: Alert US 2011-01-17 16:14:13.437000 C:MB-SL1-ET1-PT2    2: Alert US 2011-01-17 16:14:17.437000 C:MB-SL1-ET1-PT2')
        # Check option interaction 
        self.assertCmdFails([LSALERT,'-c','-d','-x'], exp_err_msg="Usage: tllsalert [options]tllsalert: error: Cannot specify --xref with 'brief' formatting")
        self.assertCmdWorks([LSALERT,'-c','-d','-x','-f','text','-w'], exp_good_msg='===================================================rec_id : 1alert_id : Alert UScreation_time : 2011-01-17 16:14:13.437000severity : Wurgency : Nevent_loc : MB-SL1-ET1-PT2event_loc_type : Cfru_loc : Nonerecommendation : Recommend doing somethingreason : no value'
    + 'src_name : AnalyzerTest057astate : 2raw_data : NoneCondition Alerts: []Condition Events: []Duplicate Alerts: [2]Suppression Alerts: []Suppression Events: [1,2]Duplicate Of Alerts: []===================================================rec_id : 2alert_id : Alert UScreation_time : 2011-01-17 16:14:17.437000severity : Wurgency : N'
    + 'event_loc : MB-SL1-ET1-PT2event_loc_type : Cfru_loc : Nonerecommendation : Recommend doing somethingreason : no valuesrc_name : AnalyzerTest057astate : 2raw_data : NoneCondition Alerts: []Condition Events: []Duplicate Alerts: []Suppression Alerts: []Suppression Events: [2]Duplicate Of Alerts: [1]')
        self.assertCmdWorks([LSALERT,'-c','-d','-x','-f','csv', '-w'], exp_good_msg='rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data,associations,xref1,Alert US,2011-01-17 16:14:13.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,2,'
    + ',"{\'D:A\': \'[2]\', \'C:E\': \'[]\', \'C:A\': \'[]\', \'S:A\': \'[]\', \'S:E\': \'[1,2]\'}",{\'DO:A\': \'[]\'}2,Alert US,2011-01-17 16:14:17.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,2,,"{\'D:A\': \'[]\', \'C:E\': \'[]\', \'C:A\': \'[]\', \'S:A\': \'[]\', \'S:E\': \'[2]\'}",{\'DO:A\': \'[1]\'}')
        self.assertCmdWorks([LSALERT,'-c','-d','-x','-f','json', '-w'], exp_good_msg='{"associations": {"D:A": "[2]", "C:E": "[]", "C:A": "[]", "S:A": "[]", "S:E": "[1,2]"}, "xref": {"DO:A": "[]"}, "severity": "W", "state": 2, "rec_id": 1, "creation_time": "2011-01-17 16:14:13.437000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2",'
    + ' "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}{"associations": {"D:A": "[]", "C:E": "[]", "C:A": "[]", "S:A": "[]", "S:E": "[2]"}, "xref": {"DO:A": "[1]"}, "severity": "W", "state": 2, "rec_id": 2, "creation_time": "2011-01-17 16:14:17.437000",'
    + ' "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}')
        
        # Attempt to remove the events by id -- all are associated with alerts
        self.assertCmdWorks([RMEVENT,'--id','1,2,3,4,5,6'], exp_good_msg="0 events removed", exp_err_msg="Event '1' cannot be removed.\tReason: Event is associated with Alert '1'Event '2' cannot be removed.\tReason: Event is associated with Alert '1'\tReason: Event is associated with Alert '2'Event '3' cannot be removed.\tReason: Event is associated with Alert '3'Event '4' cannot be removed.\tReason: Event is associated with Alert '4'Event '5' cannot be removed.\tReason: Event is associated with Alert '5'Event '6' cannot be removed.\tReason: Event is associated with Alert '6'")
        self.assertCmdWorks([RMEVENT,'--older-than','2011-01-18'], exp_good_msg='0 events removed')
        self.assertCmdWorks([RMALERT,'--ids','4,5,36'], exp_good_msg="0 unique alerts removed", exp_err_msg="Alert '4' cannot be removed.\tReason: Alert is not closed\tReason: Alert is associated with open Alert '3'Alert '5' cannot be removed.\tReason: Alert is not closed")
        self.assertCmdWorks([RMALERT,'--id','1'], exp_good_msg='1 unique alert removed')
        self.assertCmdWorks([LSALERT,'-f','csv'], exp_good_msg='rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data\r\n3,Alert US,2011-01-17 16:14:21.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n'
    +'4,Alert US,2011-01-17 16:14:25.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n5,Alert 03,2011-01-17 16:14:26.453000,E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test\r\n6,Alert US,2011-01-17 16:14:33.468000,W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,')
        self.assertCmdWorks([RMEVENT], exp_good_msg='2 events removed')
        self.assertCmdWorks([LSEVENT,'-q','rec_id=1,2'])
        # Check option interaction check
        self.assertCmdFails([LSEVENT,'-q','rec_id=1,2','-x'], exp_err_msg="Usage: tllsevent [options]tllsevent: error: Cannot use --xref option with 'brief' format")
        self.assertCmdWorks([LSEVENT,'-q','rec_id=1,2','-f','text', '-x'])
        self.assertCmdWorks([CHALERT,'--id','5','--state','close'])
        self.assertCmdWorks([CHALERT,'--id','6','--state','close'])
        self.assertCmdWorks([LSALERT,'-q','rec_id=5,6','-f','text','-c'], exp_good_msg='===================================================\r\nrec_id : 5\r\nalert_id : Alert 03\r\ncreation_time : 2011-01-17 16:14:26.453000\r\nseverity : E\r\nurgency : I\r\nevent_loc : MB-SL1-ET1-PT2\r\nevent_loc_type : C\r\nfru_loc : fru_loc2\r\nrecommendation : try again\r\nreason : reason from config1\r\nsrc_name : AnalyzerTest057a\r\nstate : 2\r\nraw_data : This is another test\r\n===================================================\r\n'
    + 'rec_id : 6\r\nalert_id : Alert US\r\ncreation_time : 2011-01-17 16:14:33.468000\r\nseverity : W\r\nurgency : N\r\nevent_loc : MB-SL1-ET1-PT1\r\nevent_loc_type : C\r\nfru_loc : None\r\nrecommendation : Recommend doing something\r\nreason : no value\r\nsrc_name : AnalyzerTest057a\r\nstate : 2\r\nraw_data : None\r\n')
        self.assertCmdWorks([RMALERT,'--older-than','2011-01-18'], exp_good_msg='2 unique alerts removed')
        self.assertCmdWorks([LSALERT,'-f','json'], exp_good_msg='{"severity": "W", "state": 1, "rec_id": 3, "creation_time": "2011-01-17 16:14:21.437000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}\r\n{"severity": "W", "state": 1, "rec_id": 4, "creation_time": "2011-01-17 16:14:25.437000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}')
        self.assertCmdWorks([RMEVENT,'--older-than','2011-01-18'], exp_good_msg='2 events removed')
        self.assertCmdWorks([LSEVENT,'-f','json'], exp_good_msg='{"src_comp": "CNM", "rpt_loc_type": null, "event_id": "Event 03", "src_loc_type": "C", "time_occurred": "2011-01-17 21:40:08.100000", "rec_id": 3, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, "rpt_comp": null, "time_logged": "2011-01-17 21:40:08.100000", "src_loc": "MB-SL1-ET1-PT2"}\r\n{"src_comp": "CNM", "rpt_loc_type": null, "event_id": "Event 04", "src_loc_type": "C", "time_occurred": "2011-01-17 21:40:12.100000", "rec_id": 4, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, "rpt_comp": null, "time_logged": "2011-01-17 21:40:12.100000", "src_loc": "MB-SL1-ET1-PT2"}\r\n')
        self.assertCmdWorks([LSEVENT,'-f','text'], exp_good_msg='===================================================\r\nrec_id : 3\r\nevent_id : Event 03 \r\ntime_occurred : 2011-01-17 21:40:08.100000\r\ntime_logged : 2011-01-17 21:40:08.100000\r\nsrc_comp : CNM\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n'
    + '===================================================\r\nrec_id : 4\r\nevent_id : Event 04 \r\ntime_occurred : 2011-01-17 21:40:12.100000\r\ntime_logged : 2011-01-17 21:40:12.100000\r\nsrc_comp : CNM\r\nsrc_loc : MB-SL1-ET1-PT2\r\nsrc_loc_type : C\r\nrpt_comp : None\r\nrpt_loc : None\r\nrpt_loc_type : None\r\nevent_cnt : None\r\nelapsed_time : None\r\n')
        self.assertCmdWorks([LSEVENT,'-f','text','-x'], exp_good_msg='===================================================rec_id : 3event_id : Event 03 time_occurred : 2011-01-17 21:40:08.100000time_logged : 2011-01-17 21:40:08.100000src_comp : CNMsrc_loc : MB-SL1-ET1-PT2src_loc_type : Crpt_comp : Nonerpt_loc : Nonerpt_loc_type : Noneevent_cnt : Noneelapsed_time : NoneCondition For Alerts: []Suppressed By Alerts: [3]===================================================rec_id : 4event_id : Event 04 time_occurred : 2011-01-17 21:40:12.100000time_logged : 2011-01-17 21:40:12.100000'
    + 'src_comp : CNMsrc_loc : MB-SL1-ET1-PT2src_loc_type : Crpt_comp : Nonerpt_loc : Nonerpt_loc_type : Noneevent_cnt : Noneelapsed_time : NoneCondition For Alerts: [4]Suppressed By Alerts: []')
        self.assertCmdWorks([LSEVENT,'-f','json','--xref'], exp_good_msg='{"src_comp": "CNM", "rpt_loc_type": null, "xref": {"CF:A": "[]", "SB:A": "[3]"}, "event_id": "Event 03", "src_loc_type": "C", "time_occurred": "2011-01-17 21:40:08.100000", "rec_id": 3, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, "rpt_comp": null, "time_logged": "2011-01-17 21:40:08.100000", "src_loc": "MB-SL1-ET1-PT2"}{"src_comp": "CNM", "rpt_loc_type": null, "xref": {"CF:A": "[4]", "SB:A": "[]"}, "event_id": "Event 04", "src_loc_type": "C", "time_occurred": "2011-01-17 21:40:12.100000", "rec_id": 4, "event_cnt": null, "rpt_loc": null, "elapsed_time": null, '
    + '"rpt_comp": null, "time_logged": "2011-01-17 21:40:12.100000", "src_loc": "MB-SL1-ET1-PT2"}')
        self.assertCmdWorks([LSEVENT,'-f','csv','-x'], exp_good_msg='rec_id,event_id,time_occurred,time_logged,src_comp,src_loc,src_loc_type,rpt_comp,rpt_loc,rpt_loc_type,event_cnt,elapsed_time3,Event 03,2011-01-17 21:40:08.100000,2011-01-17 21:40:08.100000,CNM,MB-SL1-ET1-PT2,C,,,,,,"{\'CF:A\': \'[]\', \'SB:A\': \'[3]\'}"4,Event 04,2011-01-17 21:40:12.100000,2011-01-17 21:40:12.100000,CNM,MB-SL1-ET1-PT2,C,,,,,,"{\'CF:A\': \'[4]\', \'SB:A\': \'[]\'}"')

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
        
        self.assertCmdWorks([CHALERT,'-h'], exp_good_msg='Usage: tlchalert [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-i REC_ID, --id=REC_ID                        The record id of the alert. (use tllsalert)  '
        + '-s STATE, --state=STATE                        The new alert state. (close is the only valid value at                        this time.')
        self.assertCmdWorks([CHALERT,'--help'], exp_good_msg='Usage: tlchalert [options]Options:  '
        + '-h, --help            show this help message and exit  '
        + '-i REC_ID, --id=REC_ID                        The record id of the alert. (use tllsalert)  '
        + '-s STATE, --state=STATE                        The new alert state. (close is the only valid value at                        this time.')
        
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



if __name__ == "__main__":
    unittest.main()

