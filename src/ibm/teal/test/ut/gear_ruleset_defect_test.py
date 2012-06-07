# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011, 2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import unittest 
from ibm.teal import teal
from ibm.teal.registry import get_service, SERVICE_ALERT_DELIVERY, SERVICE_EVENT_Q
from ibm.teal.util.journal import Journal
from ibm.teal.test.teal_unittest import TealTestCase
from datetime import datetime, timedelta
from ibm.teal.event import EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID,\
    EVENT_ATTR_TIME_OCCURRED, EVENT_ATTR_TIME_LOGGED, EVENT_ATTR_SRC_COMP,\
    EVENT_ATTR_SRC_LOC, EVENT_ATTR_SRC_LOC_TYPE, EVENT_ATTR_RAW_DATA_FMT,\
    EVENT_ATTR_RAW_DATA, Event
from ibm.teal.location import Location
from ibm.teal.control_msg import ControlMsg, CONTROL_MSG_TYPE_FLUSH,\
    CONTROL_MSG_ATTR_CREATION_TIME
import time

    
class GearDefectRegressionTestA(TealTestCase):
    '''Test running GEAR rulesets'''
    
    def test_defect_x000001a(self):
        ''' Ensure x000001a does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/x000001/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD02', None ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD14', None ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD04', None ))
        event_q.put_nowait(self._crt_flush(100))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/x000001/alert_output_a.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp)))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_x000001b(self):
        ''' Ensure that x000001b does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/x000001/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        #event_q.put_nowait(self._crt_isnm_event(1, 'BD700041', 'BB03-FR007-SN000-DR1-HB0-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD02', None ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD14', None ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD04', None ))
        event_q.put_nowait(self._crt_flush(100))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/x000001/alert_output_b.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp)))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_x000001c(self):
        ''' Ensure that x000001c does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/x000001/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        #event_q.put_nowait(self._crt_isnm_event(1, 'BD700041', 'BB03-FR007-SN000-DR1-HB0-LD01', None ))
        #event_q.put_nowait(self._crt_isnm_event(2, 'BD700041', 'BB03-FR007-SN000-DR1-HB0-LD02', None ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD14', None ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD04', None ))
        event_q.put_nowait(self._crt_flush(100))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/x000001/alert_output_c.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp)))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_x000001d(self):
        ''' Ensure that x000001d does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/x000001/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        #event_q.put_nowait(self._crt_isnm_event(1, 'BD700041', 'BB03-FR007-SN000-DR1-HB0-LD01', None ))
        #event_q.put_nowait(self._crt_isnm_event(2, 'BD700041', 'BB03-FR007-SN000-DR1-HB0-LD02', None ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700041', 'FR007-CG03-SN000-DR1-HB0-OM20-LD14', None ))
        #event_q.put_nowait(self._crt_isnm_event(4, 'BD700041', 'BB03-FR007-SN000-DR1-HB0-LD04', None ))
        event_q.put_nowait(self._crt_flush(100))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/x000001/alert_output_d.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp)))
        #self.assertTrue(j_out.wait_for_entries(1, seconds=10))
        #j_out.save('data/gear_ruleset_test/bugs/x000001/alert_output_d.json')
        #print j_out
        #print j_out
        #print j_exp
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    
    def test_defect_172183(self):
        ''' Ensure that defect 172183 does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d172183/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD500031', 'FR007-CG03-SN001-DR0-HB0-LL01', 'FR007-CG03-SN001-DR0-HB3-LL01'  ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD50002F', 'FR007-CG03-SN001-DR0-HB0-LL01', 'FR007-CG03-SN001-DR0-HB3-LL01'  ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD50002F', 'FR007-CG03-SN001-DR0-HB6-LL01', 'FR007-CG03-SN001-DR0-HB3-LL04'  ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700027', 'FR007-CG03-SN001-DR0-HB0-LL01', 'FR007-CG03-SN001-DR0-HB3-LL01'  ))
        event_q.put_nowait(self._crt_flush(10))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d172183/alert_output.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_173776(self):
        ''' Ensure that defect 173776 does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d173776/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG03-SN000-DR0-HB1-OM20-LD15', 'FR007-CG03-SN016-DR0-HB0-OM20-LD15'  ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700041', 'FR007-CG03-SN000-DR0-HB1-OM20-LD15', 'FR007-CG03-SN016-DR0-HB0-OM20-LD15'  ))
        event_q.put_nowait(self._crt_flush(10))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d173776/alert_output.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_173863(self):
        ''' Ensure that defect 173863 does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d173776/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700040', 'FR007-CG03-SN000-DR0-HB1-OM20-LD14', 'FR007-CG03-SN000-DR0-HB0-OM20-LD15'  ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD70003F', 'FR007-CG03-SN000-DR0-HB1-OM20-LD14', 'FR007-CG03-SN000-DR0-HB0-OM20-LD15'  ))
        #event_q.put_nowait(self._crt_isnm_event(3, 'BD50002F', 'BB03-FR007-SN001-DR0-HB6-LL01', 'BB03-FR007-SN001-DR0-HB3-LL04'  ))
        #event_q.put_nowait(self._crt_isnm_event(4, 'BD700027', 'BB03-FR007-SN001-DR0-HB0-LL01', 'BB03-FR007-SN001-DR0-HB3-LL01'  ))
        event_q.put_nowait(self._crt_flush(10))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d173863/alert_output.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
   
    def test_defect_173874(self):
        ''' Ensure that defect 173874 does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d173776/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700054', 'FR007-CG03-SN000-DR0-HB0-OM20-LR01', 'FR007-CG03-SN000-DR1-HB1-OM20-LR00'  ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700054', 'FR007-CG03-SN000-DR0-HB0-OM20-LR00', 'FR007-CG03-SN000-DR2-HB1-OM20-LR00'  ))
        event_q.put_nowait(self._crt_flush(100))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d173874/alert_output.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #print j_out
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_178935(self):
        ''' Ensure that defect 178935 does not get regressed '''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178935/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM07-LD07', 'FR007-CG11-SN008-DR0-HB0-OM06-LD06')) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM09-LD09', 'FR007-CG09-SN006-DR0-HB0-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD700037', 'FR007-CG12-SN009-DR0-HB1-OM07-LD07', 'FR007-CG11-SN008-DR0-HB1-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD700037', 'FR007-CG12-SN009-DR0-HB1-OM09-LD09', 'FR007-CG09-SN006-DR0-HB1-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(15, 'BD700037', 'FR007-CG12-SN009-DR0-HB2-OM07-LD07', 'FR007-CG11-SN008-DR0-HB2-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(16, 'BD700037', 'FR007-CG12-SN009-DR0-HB2-OM09-LD09', 'FR007-CG09-SN006-DR0-HB2-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(17, 'BD700037', 'FR007-CG12-SN009-DR0-HB3-OM07-LD07', 'FR007-CG11-SN008-DR0-HB3-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(18, 'BD700037', 'FR007-CG12-SN009-DR0-HB3-OM09-LD09', 'FR007-CG09-SN006-DR0-HB3-OM06-LD06'))
        event_q.put_nowait(self._crt_flush(100))

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178935/alert_output.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_178935b(self):
        ''' Ensure that defect 178935 does not get regressed -- Make sure priming doesn't cause alert'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178935/config2.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM07-LD07', 'FR007-CG11-SN008-DR0-HB0-OM06-LD06')) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM09-LD09', 'FR007-CG09-SN006-DR0-HB0-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD700037', 'FR007-CG12-SN009-DR0-HB1-OM07-LD07', 'FR007-CG11-SN008-DR0-HB1-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD700037', 'FR007-CG12-SN009-DR0-HB1-OM09-LD09', 'FR007-CG09-SN006-DR0-HB1-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(15, 'BD700037', 'FR007-CG12-SN009-DR0-HB2-OM07-LD07', 'FR007-CG11-SN008-DR0-HB2-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(16, 'BD700037', 'FR007-CG12-SN009-DR0-HB2-OM09-LD09', 'FR007-CG09-SN006-DR0-HB2-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(17, 'BD700037', 'FR007-CG12-SN009-DR0-HB3-OM07-LD07', 'FR007-CG11-SN008-DR0-HB3-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(18, 'BD700037', 'FR007-CG12-SN009-DR0-HB3-OM09-LD09', 'FR007-CG09-SN006-DR0-HB3-OM06-LD06'))
        #event_q.put_nowait(self._crt_flush(10))
        #event_q.put_nowait(self._crt_flush(20))
        time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178935/alert_output.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test_defect_178935c(self):
        ''' Ensure that defect 178935 does not get regressed -- Make sure priming with event creates alerts'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178935/config2.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM07-LD07', 'FR007-CG11-SN008-DR0-HB0-OM06-LD06')) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM09-LD09', 'FR007-CG09-SN006-DR0-HB0-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD700037', 'FR007-CG12-SN009-DR0-HB1-OM07-LD07', 'FR007-CG11-SN008-DR0-HB1-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD700037', 'FR007-CG12-SN009-DR0-HB1-OM09-LD09', 'FR007-CG09-SN006-DR0-HB1-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(15, 'BD700037', 'FR007-CG12-SN009-DR0-HB2-OM07-LD07', 'FR007-CG11-SN008-DR0-HB2-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(16, 'BD700037', 'FR007-CG12-SN009-DR0-HB2-OM09-LD09', 'FR007-CG09-SN006-DR0-HB2-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(17, 'BD700037', 'FR007-CG12-SN009-DR0-HB3-OM07-LD07', 'FR007-CG11-SN008-DR0-HB3-OM06-LD06'))
        event_q.put_nowait(self._crt_isnm_event(18, 'BD700037', 'FR007-CG12-SN009-DR0-HB3-OM09-LD09', 'FR007-CG09-SN006-DR0-HB3-OM06-LD06'))
        event_q.put_nowait(self._crt_flush(10))
        event_q.put_nowait(self._crt_isnm_event(39, 'BD700037', 'FR007-CG12-SN009-DR0-HB0-OM07-LD07', 'FR007-CG11-SN008-DR0-HB0-OM06-LD06')) 
        #event_q.put_nowait(self._crt_flush(20))
        time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178935/alert_output2.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_179277a(self):
        ''' Ensure that defect 179277 does not get regressed -- Case 1 where should create an single alert'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d179277/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        LOC1 = 'FR007-CG11-SN008-DR0-HB0-OM07-LD07'
        LOC2 = 'FR007-CG11-SN008-DR0-HB0-OM06-LD06'
        LOC3 = 'FR007-CG11-SN008-DR0-HB0-OM09-LD09'
        LOC4 = 'FR007-CG11-SN008-DR0-HB0-OM02-LD06'
        LOC5 = 'FR007-CG11-SN008-DR0-HB0-OM12-LD03'
        event_q.put_nowait(self._crt_isnm_event(11, 'BD70003B', LOC1, LOC2)) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD70003B', LOC2, LOC3))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD70003B', LOC4, LOC5))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD70003B', LOC4, LOC5))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d179277/alert_output1.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
        
    def test__defect_179277b(self):
        ''' Ensure that defect 179277 does not get regressed -- Case 2 where should create a single alert'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d179277/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        LOC1 = 'FR007-CG11-SN008-DR0-HB0-OM07-LD07'
        LOC2 = 'FR007-CG11-SN008-DR0-HB0-OM06-LD06'
        LOC3 = 'FR007-CG11-SN008-DR0-HB0-OM09-LD09'
        LOC4 = 'FR007-CG11-SN008-DR0-HB0-OM02-LD06'
        #LOC5 = 'FR007-CG11-SN008-DR0-HB0-OM12-LD03'
        event_q.put_nowait(self._crt_isnm_event(11, 'BD70003B', LOC1, LOC2)) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD70003B', LOC2, LOC3))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD70003B', LOC3, LOC4))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD70003B', LOC1, LOC4))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d179277/alert_output2.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
        
    def test__defect_179277c(self):
        ''' Ensure that defect 179277 does not get regressed -- Case 1 where should not create BDFF0050'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d179277/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        LOC1 = 'FR007-CG11-SN008-DR0-HB0-OM07-LD07'
        LOC2 = 'FR007-CG11-SN008-DR0-HB0-OM06-LD06'
        LOC3 = 'FR007-CG11-SN008-DR0-HB0-OM09-LD09'
        LOC4 = 'FR007-CG11-SN008-DR0-HB0-OM02-LD06'
        #LOC5 = 'FR007-CG11-SN008-DR0-HB0-OM12-LD03'
        event_q.put_nowait(self._crt_isnm_event(11, 'BD70003B', LOC1, LOC2)) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD70003B', LOC3, LOC4))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD70003B', LOC3, LOC4))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD70003B', LOC3, LOC4))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d179277/alert_output3.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
        
    def test__defect_179277d(self):
        ''' Ensure that defect 179277 does not get regressed -- Case 2 where should not create BDFF0050'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d179277/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        LOC1 = 'FR007-CG11-SN008-DR0-HB0-OM07-LD07'
        LOC2 = 'FR007-CG11-SN008-DR0-HB0-OM06-LD06'
        LOC3 = 'FR007-CG11-SN008-DR0-HB0-OM09-LD09'
        LOC4 = 'FR007-CG11-SN008-DR0-HB0-OM02-LD06'
        #LOC5 = 'FR007-CG11-SN008-DR0-HB0-OM12-LD03'
        event_q.put_nowait(self._crt_isnm_event(11, 'BD70003B', LOC1, LOC2)) 
        event_q.put_nowait(self._crt_isnm_event(12, 'BD70003B', LOC1, LOC2))
        event_q.put_nowait(self._crt_isnm_event(13, 'BD70003B', LOC1, LOC2))
        event_q.put_nowait(self._crt_isnm_event(14, 'BD70003B', LOC3, LOC4))
        event_q.put_nowait(self._crt_isnm_event(15, 'BD70003B', LOC1, LOC2))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d179277/alert_output4.json')      
        self.assertTrue(j_out.wait_for_entries(2))#len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d179277/alert_output4.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106a(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700025', 'FR008-CG03-SN004-DR0-HB0-LD01', 'FR008-CG07-SN005-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output1.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output1.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106b(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output2.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output2.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106c(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700026', 'FR008-CG03-SN004-DR0-HB0-LR03', 'FR008-CG04-SN004-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output3.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output3.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106d(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output4.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output4.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
   
    def test__defect_178106e(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700027    ', 'FR007-CG03-SN001-DR0-HB0-LL03', 'FR007-CG04-SN001-DR0-HB3-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD7000   27', 'FR007-CG04-SN001-DR0-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700027', 'FR007-CG03-SN001-DR0-HB0-LL03', 'FR007-CG04-SN001-DR0-HB3-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700027', 'FR007-CG03-SN001-DR0-HB0-LL04', 'FR007-CG04-SN001-DR0-HB3-LL04' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output5.json')      
        self.assertTrue(j_out.wait_for_entries(2)) #len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output5.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
   
    def test__defect_178106f(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700027', 'FR007-CG03-SN001-DR0-HB0-LL03', 'FR007-CG04-SN001-DR0-HB3-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700027', 'FR007-CG04-SN001-DR0-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700027', 'FR007-CG04-SN001-DR0-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700027', 'FR007-CG03-SN001-DR0-HB0-LL03', 'FR007-CG04-SN001-DR0-HB3-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700027', 'FR007-CG04-SN001-DR0-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700027', 'FR007-CG04-SN001-DR0-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(7, 'BD700027', 'FR007-CG03-SN001-DR0-HB0-LL03', 'FR007-CG04-SN001-DR0-HB3-LL03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output6.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output6.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
   
    def test__defect_178106g(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', 'FR007-CG03-SN001-DR0-HB0-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(7, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(8, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(9, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(10, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output7.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output7.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
        
           
    def test__defect_178106g2(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', None))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(7, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(8, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(9, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(10, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output7.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output7.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106h(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', None))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700025', 'FR007-CG03-SN001-DR0-HB0-LD01', 'FR007-CG07-SN002-DR0-HB3-LD01' ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700025', 'FR007-CG07-SN002-DR0-HB3-LD01', None ))
        event_q.put_nowait(self._crt_isnm_event(7, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(8, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(9, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(10, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700026', 'FR007-CG03-SN001-DR0-HB0-LR03', 'FR007-CG04-SN001-DR1-HB3-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output8.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(5)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output8.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106i(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output9.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(15)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output9.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
       
    def test__defect_178106j(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(4, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(5, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(6, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(7, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(8, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(9, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(10, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(11, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(12, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(21, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(23, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(24, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(25, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(26, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(27, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(28, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(29, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(30, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(31, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(32, 'BD700026', 'FR007-CG04-SN001-DR1-HB3-LR03', 'FR007-CG03-SN001-DR0-HB0-LR03' ))
        event_q.put_nowait(self._crt_isnm_event(41, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(42, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(43, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(44, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(45, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(46, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(47, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(48, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(49, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(50, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(51, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_isnm_event(52, 'BD700027', 'FR007-CG04-SN001-DR1-HB3-LL03', 'FR007-CG03-SN001-DR0-HB0-LL03' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output10.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(15)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output10.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_178106k(self):
        ''' Ensure that defect  does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d178106/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD03' ))
        event_q.put_nowait(self._crt_isnm_event(2, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD04', 'FR007-CG03-SN001-DR0-HB0-LD04' ))
        event_q.put_nowait(self._crt_isnm_event(3, 'BD700025', 'FR007-CG04-SN001-DR1-HB3-LD03', 'FR007-CG03-SN001-DR0-HB0-LD04' ))
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d178106/alert_output11.json')      
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(15)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d178106/alert_output11.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
    
    def test__defect_181301a(self):
        ''' Ensure that defect  181301 does not get regressed -- Case 1'''
        myteal = teal.Teal('data/gear_ruleset_test/bugs/d181301/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        event_q = get_service(SERVICE_EVENT_Q)
        event_q.put_nowait(self._crt_isnm_event(1049088, 'BD700025', 'FR003-CG10-SN049-DR3-HB0-OM15-LD15', 'FR001-CG06-SN000-DR3-HB3-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049091, 'BD700025', 'FR003-CG10-SN049-DR3-HB1-OM15-LD15', 'FR001-CG14-SN016-DR3-HB3-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049092, 'BD700025', 'FR003-CG10-SN049-DR3-HB3-OM15-LD15', 'FR003-CG06-SN048-DR3-HB3-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049095, 'BD700025', 'FR003-CG10-SN049-DR3-HB2-OM15-LD15', 'FR002-CG10-SN032-DR3-HB3-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049096, 'BD700025', 'FR003-CG10-SN049-DR3-HB4-OM15-LD15', 'FR001-CG06-SN000-DR3-HB7-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049097, 'BD700025', 'FR003-CG10-SN049-DR3-HB5-OM15-LD15', 'FR001-CG14-SN016-DR3-HB7-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049101, 'BD700025', 'FR003-CG10-SN049-DR3-HB6-OM15-LD15', 'FR002-CG10-SN032-DR3-HB7-OM14-LD14'))
        event_q.put_nowait(self._crt_isnm_event(1049102, 'BD700025', 'FR003-CG10-SN049-DR3-HB7-OM15-LD15', 'FR003-CG06-SN048-DR3-HB7-OM14-LD14'))        
        event_q.put_nowait(self._crt_flush(20))
        #time.sleep(10)

        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() == 'ListenerJournal':
                j_out = listener.journal
               
        j_exp = Journal('j_exp', 'data/gear_ruleset_test/bugs/d181301/alert_output1a.json')    
        self.assertTrue(j_out.wait_for_entries(len(j_exp), seconds=20))
        #time.sleep(15)
        #print j_out
        #j_out.save('data/gear_ruleset_test/bugs/d181301/alert_output1a.json')
        self.assertTrue(j_out.deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        return
       
    def _crt_isnm_event(self, rec_id, event_id, src_loc, neighbor_loc, time=0):
        right_now = datetime.now()+ timedelta(seconds=time)
        crt_dict = {}
        crt_dict[EVENT_ATTR_REC_ID] = rec_id
        crt_dict[EVENT_ATTR_EVENT_ID] = event_id
        crt_dict[EVENT_ATTR_TIME_OCCURRED] = right_now
        crt_dict[EVENT_ATTR_TIME_LOGGED] = right_now + timedelta(seconds=1)
        crt_dict[EVENT_ATTR_SRC_COMP] = 'CNM'
        crt_dict[EVENT_ATTR_SRC_LOC] = src_loc
        crt_dict[EVENT_ATTR_SRC_LOC_TYPE] = 'H'
        crt_dict[EVENT_ATTR_RAW_DATA_FMT] = long('0x5445535400000001',16)
        crt_dict[EVENT_ATTR_RAW_DATA] = 'When in the course'
        event = Event.fromDict(crt_dict)
        if neighbor_loc is None:
            event.raw_data['neighbor_loc'] = None
        else:
            event.raw_data['neighbor_loc'] = Location('H', neighbor_loc)
        event.raw_data['local_port'] = '2'
        event.raw_data['local_torrent'] = '3'
        event.raw_data['local_planar'] = '4'
        event.raw_data['local_om'] = '5'
        event.raw_data['nbr_port'] = '6'
        event.raw_data['nbr_torrent'] = '7'
        event.raw_data['nbr_planar'] = '8'
        event.raw_data['nbr_om'] = '9'
        event.raw_data['encl_mtms'] = '10'
        event.raw_data['pwr_ctrl_mtms'] = '11'
        event.raw_data['eed_loc_info'] = '12'
        return event
    
    def _crt_flush(self, time=0):
        ''' create a flush command msg '''
        return ControlMsg(CONTROL_MSG_TYPE_FLUSH, {CONTROL_MSG_ATTR_CREATION_TIME: datetime.now()+ timedelta(seconds=time)})
            

if __name__ == "__main__":
    unittest.main()