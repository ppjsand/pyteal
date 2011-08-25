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
import subprocess
import os
import platform
from ibm.teal.teal import Teal, registry
from ibm.teal.util.journal import Journal
from ibm.teal.test.teal_unittest import TealTestCase

LSALERT = ''

class TestTllsalert(TealTestCase):

    def setUp(self):
        t = Teal('data/tllsalert_test/test.conf',data_only=True)
        
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        
        global LSALERT
        LSALERT = os.path.join(teal_path,'bin/tllsalert')
        
        t.shutdown()
        
        self.prepare_db()
        self._add_journal('data/tllsalert_test/events_001.json')
        self._add_journal('data/tllsalert_test/alerts_001.json')

        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR','/opt/teal'),'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)

    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)

    
    def _add_journal(self, json_file):
        ''' Load the alert DB from the journal JSON file '''
        self.teal = Teal('data/tllsalert_test/test.conf','stderr',msgLevel='info')
        # Alerts
        ja = Journal('temp_journal', file=json_file)
        ja.insert_in_db(truncate=False, no_delay=True)
        self.teal.shutdown()
        return
   
    def test_tllsalert(self):
        ''' Test associations returned '''
        # NOTE:
        # CMVC does not allow checking in of very long lines
        # use + to separate long strings
        self.assertCmdWorks([LSALERT], exp_good_msg='1: Alert US 2010-07-22 16:14:13.437000 C:MB-SL1-ET1-PT2    3: Alert US 2010-07-22 16:14:21.437000 C:MB-SL1-ET1-PT2    4: Alert US 2010-07-22 16:14:25.437000 C:MB-SL1-ET1-PT2    5: Alert 03 2010-07-22 16:14:26.453000 C:MB-SL1-ET1-PT2    6: Alert US 2010-07-22 16:14:33.468000 C:MB-SL1-ET1-PT1')
        self.assertCmdWorks([LSALERT,'--with-assoc','--format=json'], exp_good_msg=
                               '{"associations": {"D:A": "[2]", "C:E": "[]", "C:A": "[]", "S:A": "[]", "S:E": "[1,2]"}, "severity": "W", "state": 1, "rec_id": 1, "creation_time": "2010-07-22 16:14:13.437000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}'+
                               '{"associations": {"D:A": "[]", "C:E": "[]", "C:A": "[]", "S:A": "[4]", "S:E": "[3]"}, "severity": "W", "state": 1, "rec_id": 3, "creation_time": "2010-07-22 16:14:21.437000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}'+
                               '{"associations": {"D:A": "[]", "C:E": "[4]", "C:A": "[]", "S:A": "[]", "S:E": "[]"}, "severity": "W", "state": 1, "rec_id": 4, "creation_time": "2010-07-22 16:14:25.437000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}'+
                               '{"associations": {"D:A": "[]", "C:E": "[5]", "C:A": "[]", "S:A": "[]", "S:E": "[]"}, "severity": "E", "state": 1, "rec_id": 5, "creation_time": "2010-07-22 16:14:26.453000", "reason": "reason from config1", "alert_id": "Alert 03", "event_loc": "MB-SL1-ET1-PT2", "recommendation": "try again", "src_name": "AnalyzerTest057a", "raw_data": "This is another test", "event_loc_type": "C", "urgency": "I", "fru_loc": "fru_loc2"}'+
                               '{"associations": {"D:A": "[]", "C:E": "[]", "C:A": "[]", "S:A": "[]", "S:E": "[6]"}, "severity": "W", "state": 1, "rec_id": 6, "creation_time": "2010-07-22 16:14:33.468000", "reason": "no value", "alert_id": "Alert US", "event_loc": "MB-SL1-ET1-PT1", "recommendation": "Recommend doing something", "src_name": "AnalyzerTest057a", "raw_data": null, "event_loc_type": "C", "urgency": "N", "fru_loc": null}')
        self.assertCmdWorks([LSALERT,'-f','csv'], exp_good_msg='rec_id,alert_id,creation_time,severity,urgency,event_loc,event_loc_type,fru_loc,recommendation,reason,src_name,state,raw_data\r\n1,Alert US,2010-07-22 16:14:13.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n3,Alert US,2010-07-22 16:14:21.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n4,Alert US,2010-07-22 16:14:25.437000,W,N,MB-SL1-ET1-PT2,C,,Recommend doing something,no value,AnalyzerTest057a,1,\r\n5,Alert 03,2010-07-22 16:14:26.453000,E,I,MB-SL1-ET1-PT2,C,fru_loc2,try again,reason from config1,AnalyzerTest057a,1,This is another test\r\n6,Alert US,2010-07-22 16:14:33.468000,W,N,MB-SL1-ET1-PT1,C,,Recommend doing something,no value,AnalyzerTest057a,1,')
        self.assertCmdWorks([LSALERT,'-f','text'], exp_good_msg='===================================================\r\nrec_id : 1\r\nalert_id : Alert US\r\ncreation_time : 2010-07-22 16:14:13.437000\r\nseverity : W\r\nurgency : N\r\nevent_loc : MB-SL1-ET1-PT2\r\nevent_loc_type : C\r\nfru_loc : None\r\nrecommendation : Recommend doing something\r\nreason : no value\r\nsrc_name : AnalyzerTest057a\r\nstate : 1\r\nraw_data : None\r\n===================================================\r\n' 
    + 'rec_id : 3\r\nalert_id : Alert US\r\ncreation_time : 2010-07-22 16:14:21.437000\r\nseverity : W\r\nurgency : N\r\nevent_loc : MB-SL1-ET1-PT2\r\nevent_loc_type : C\r\nfru_loc : None\r\nrecommendation : Recommend doing something\r\nreason : no value\r\nsrc_name : AnalyzerTest057a\r\nstate : 1\r\nraw_data : None\r\n===================================================\r\n' 
    + 'rec_id : 4\r\nalert_id : Alert US\r\ncreation_time : 2010-07-22 16:14:25.437000\r\nseverity : W\r\nurgency : N\r\nevent_loc : MB-SL1-ET1-PT2\r\nevent_loc_type : C\r\nfru_loc : None\r\nrecommendation : Recommend doing something\r\nreason : no value\r\nsrc_name : AnalyzerTest057a\r\nstate : 1\r\nraw_data : None\r\n===================================================\r\n' 
    + 'rec_id : 5\r\nalert_id : Alert 03\r\ncreation_time : 2010-07-22 16:14:26.453000\r\nseverity : E\r\nurgency : I\r\nevent_loc : MB-SL1-ET1-PT2\r\nevent_loc_type : C\r\nfru_loc : fru_loc2\r\nrecommendation : try again\r\nreason : reason from config1\r\nsrc_name : AnalyzerTest057a\r\nstate : 1\r\nraw_data : This is another test\r\n===================================================\r\nrec_id : 6\r\nalert_id : Alert US\r\ncreation_time : 2010-07-22 16:14:33.468000\r\nseverity : W\r\nurgency : N\r\nevent_loc : MB-SL1-ET1-PT1\r\nevent_loc_type : C\r\nfru_loc : None\r\nrecommendation : Recommend doing something\r\nreason : no value\r\nsrc_name : AnalyzerTest057a\r\nstate : 1\r\nraw_data : None')
        self.assertCmdWorks([LSALERT,'-q','rec_id=1,3,6'], exp_good_msg='1: Alert US 2010-07-22 16:14:13.437000 C:MB-SL1-ET1-PT2    3: Alert US 2010-07-22 16:14:21.437000 C:MB-SL1-ET1-PT2    6: Alert US 2010-07-22 16:14:33.468000 C:MB-SL1-ET1-PT1')
        return

if __name__ == "__main__":
    unittest.main()
