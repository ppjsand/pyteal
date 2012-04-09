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

from datetime import timedelta, datetime
from ibm import teal
from ibm.teal.analyzer.pool import IncidentPool
from ibm.teal.analyzer.pool.incident_pool import IncidentPoolClosedError, IncidentPoolStateTransitionError, \
    IncidentPoolNotClosedError,\
    ArrivalCheckCtl, IncidentPoolFailedError, POOL_STATE_FAILED,\
    IncidentPoolEventCheckpoint
from ibm.teal.analyzer.pool.incident_pool import POOL_CLOSE_REASON_SHUTDOWN
from ibm.teal.analyzer.pool.incident_pool import POOL_MODE_OCCURRED, POOL_MODE_LOGGED,\
    POOL_CLOSE_REASON_INCIDENT_TIME, IncidentPoolConfigError
from ibm.teal.analyzer.pool.incident_pool import POOL_STATE_NEW, POOL_STATE_RUNNING, POOL_STATE_CLOSED
from ibm.teal.registry import get_logger
from ibm.teal.test.teal_unittest import TealTestCase
import multiprocessing
import unittest
import sys
from ibm.teal.event import EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID,\
    EVENT_ATTR_SRC_COMP, EVENT_ATTR_TIME_OCCURRED, EVENT_ATTR_TIME_LOGGED
       
    
class TestIncidentPoolBasic(TealTestCase):

    def setUp(self):
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)

    def tearDown(self):
        self.teal.shutdown()

    def testCreation(self):
        '''Test creation of pool
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 0)
        self.assertEqual(p1.last_incident, None)
        self.assertEqual(p1.arrival_check_ctl, None)
        self.assertEqual(p1.arrival_window_values, [-1])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        
        # Realtime
        p1 = IncidentPool.new_pool(POOL_MODE_LOGGED, 20, None, use_timer=True)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEqual(p1.mode, POOL_MODE_LOGGED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 0)
        self.assertEqual(p1.last_incident, None)
        self.assertEqual(p1.arrival_check_ctl, None)
        self.assertEqual(p1.arrival_window_values, [-1])
        self.assertEqual(p1.use_timer, True)
        self.assertEqual(len(p1.moved_forward), 0)

        # Bad values
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool,POOL_MODE_OCCURRED, -3, None)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, 2, 20, None)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, -1, 20, None)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, 40000, 20, None)
        ac1bad = ArrivalCheckCtl(None, None, None, None)
        ac2bad = ArrivalCheckCtl(None, 1, 1, 1)
        ac3bad = ArrivalCheckCtl(2, 2, 2, None)
        ac4bad = ArrivalCheckCtl(3, 3, None, 3)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, POOL_MODE_OCCURRED, 20, None, None, None, False, ac1bad)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, POOL_MODE_OCCURRED, 20, None, None, None, False, ac2bad)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, POOL_MODE_OCCURRED, 20, None, None, None, False, ac3bad)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, POOL_MODE_OCCURRED, 20, None, None, None, False, ac4bad)
        return
        
    def testAddOneOccurred(self):
        '''Test adding the first incident to a historic pool
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: None})   # validates that it is unused
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, None)
        self.assertEqual(p1.arrival_window_values, [-1])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        return

    def testAddOneLogged(self):
        '''Test adding the first incident to a historic pool
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_LOGGED, 20, None)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: None,   # validates that it is unused
                                   EVENT_ATTR_TIME_LOGGED: right_now})   
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_LOGGED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, None)
        self.assertEqual(p1.arrival_window_values, [-1])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        return
    
    def testAddOneLoggedArrival(self):
        '''Test adding the first incident to a historic pool
        '''
        # Historic
        ac1 = ArrivalCheckCtl(4, 4, 2, 10)
        p1 = IncidentPool.new_pool(POOL_MODE_LOGGED, 20, None, arrival_check_ctl=ac1)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: None,  # validates that it is unused
                                   EVENT_ATTR_TIME_LOGGED: right_now})   
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_LOGGED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, -1, 0])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        return

    def testAddTwiceOccurred(self):
        '''Test that handles adding 2nd and detects adding same incident twice 
        '''
        # Historic
        ac1 = ArrivalCheckCtl(4, 4, 2, 10)
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, arrival_check_ctl=ac1)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: None})   # validates that it is unused
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, -1, 0])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)

        # Add the 2nd one
        right_now2 = right_now + timedelta(seconds=10)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                           EVENT_ATTR_EVENT_ID:'IPT1', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now2,
                           EVENT_ATTR_TIME_LOGGED: None})   # validates that it is unused

        te2.time_logged = None # To cause failures if incorrectly used 
        p1.add_incident(te2, 3, 5)
        self.assertEqual(len(p1.incidents), 2)
        self.assertTrue(p1.contains_incident('E', 'IPT1')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te2)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, 0, 10])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        return
    
    def testAddFourDiffOccurred(self):
        '''Test that handles adding 2nd and detects adding same incident twice 
        '''
        ac1 = ArrivalCheckCtl(4, 4, 2, 11)
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, arrival_check_ctl=ac1)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        # Add 1st
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1.event_id in p1.incidents.keys())
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, -1, 0])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(None), None)
        self.assertEqual(p1.get_arrival_extension(None), 0)
        # Add the 2nd one
        right_now2 = right_now + timedelta(seconds=10)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        self.assertEqual(len(p1.incidents), 2)
        self.assertTrue(p1.contains_incident('E', 'IPT1')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te2)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, 0, 10])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(None), None)
        self.assertEqual(p1.get_arrival_extension(None), 0)
        # Add the 3rd one
        right_now3 = right_now2 + timedelta(seconds=3)
        te3 = teal.Event.fromDict({EVENT_ATTR_REC_ID:3, 
                           EVENT_ATTR_EVENT_ID:'IPT2', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now3,
                           EVENT_ATTR_TIME_LOGGED: right_now3})  
        p1.add_incident(te3, 0, 0)
        self.assertEqual(len(p1.incidents), 3)
        self.assertTrue(p1.contains_incident('E', 'IPT2')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension + 0
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te3)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, 0, 10, 13])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(None), None)
        self.assertEqual(p1.get_arrival_extension(None), 0)
        # Add the 4th one
        right_now4 = right_now3 + timedelta(seconds=7)
        te4 = teal.Event.fromDict({EVENT_ATTR_REC_ID:4, 
                           EVENT_ATTR_EVENT_ID:'IPT3', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now4,
                           EVENT_ATTR_TIME_LOGGED: right_now4})  
        p1.add_incident(te4, 0, 0)
        self.assertEqual(len(p1.incidents), 4)
        self.assertTrue(p1.contains_incident('E', 'IPT3')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertTrue(te4 in p1.incidents[te4.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension + 0 + 0
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te4)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [0, 10, 13, 20])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 160)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        # Keep adding 4 until get infinite arrival rate
        p1.add_incident(te4, 0, 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 266)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        p1.add_incident(te4, 0, 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 333)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        p1.add_incident(te4, 0, 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 800)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        # Now have array of 20's but duration is 25, so won't get better than 800
        # So force to 20 and watch what happens 
        self.assertEqual(p1.get_arrival_rate(20), sys.maxint)
        self.assertEqual(p1.get_arrival_extension(20), 11)
        self.assertEqual(p1.arrival_window_values, [20, 20, 20, 20])
        return
    
    def testMinArrivalWindowSize(self):
        '''Test that handles adding 2nd and detects adding same incident twice 
        '''
        ac1 = ArrivalCheckCtl(3, 4, 2, 11)
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, arrival_check_ctl=ac1)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        # Add 1st
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1.event_id in p1.incidents.keys())
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, -1, 0])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(None), None)
        self.assertEqual(p1.get_arrival_extension(None), 0)
        # Add the 2nd one
        right_now2 = right_now + timedelta(seconds=10)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        self.assertEqual(len(p1.incidents), 2)
        self.assertTrue(p1.contains_incident('E', 'IPT1')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te2)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, -1, 0, 10])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(None), None)
        self.assertEqual(p1.get_arrival_extension(None), 0)
        # Add the 3rd one
        right_now3 = right_now2 + timedelta(seconds=3)
        te3 = teal.Event.fromDict({EVENT_ATTR_REC_ID:3, 
                           EVENT_ATTR_EVENT_ID:'IPT2', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now3,
                           EVENT_ATTR_TIME_LOGGED: right_now3})  
        p1.add_incident(te3, 0, 0)
        self.assertEqual(len(p1.incidents), 3)
        self.assertTrue(p1.contains_incident('E', 'IPT2')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension + 0
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te3)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [-1, 0, 10, 13])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        # THIS IS THE ACTUAL TEST ... that this has a value instead of NONE
        self.assertEqual(p1.get_arrival_rate(p1.duration), 120)
        # THE REST IS TO ENSURE THAT it doesn't impact the other results
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        # Add the 4th one
        right_now4 = right_now3 + timedelta(seconds=7)
        te4 = teal.Event.fromDict({EVENT_ATTR_REC_ID:4, 
                           EVENT_ATTR_EVENT_ID:'IPT3', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now4,
                           EVENT_ATTR_TIME_LOGGED: right_now4})  
        p1.add_incident(te4, 0, 0)
        self.assertEqual(len(p1.incidents), 4)
        self.assertTrue(p1.contains_incident('E', 'IPT3')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertTrue(te4 in p1.incidents[te4.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension + 0 + 0
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        self.assertEqual(p1.last_incident, te4)
        self.assertEqual(p1.arrival_check_ctl, ac1)
        self.assertEqual(p1.arrival_window_values, [0, 10, 13, 20])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 160)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        # Keep adding 4 until get infinite arrival rate
        p1.add_incident(te4, 0, 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 266)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        p1.add_incident(te4, 0, 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 333)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        p1.add_incident(te4, 0, 0)
        self.assertEqual(p1.get_arrival_rate(p1.duration), 800)
        self.assertEqual(p1.get_arrival_extension(p1.duration), 0)
        check_str = '\nIncidentPool TESTING:  state = Running;   last = 4\n  duration: 20 >25< 300' + \
            '        timer = False\n  times: S: {0} PC: {1}' + \
            '(   25)\n  active incidents:\n         4: IPT3     {2}(   20)\n      ' + \
            '   4: IPT3     {2}(   20)\n         4: IPT3     {2}' + \
            '(   20)\n         4: IPT3     {2}(   20)\n         3: IPT2     ' + \
            '{3}(   13)\n         2: IPT1     {4}(   10)\n  ' + \
            '       1: IPT0     {5}(    0)\n  suppressed incidents:\n     <none>\n  ' + \
            'suppression relationships:\n     <none>\n  priming incidents:\n     <none>\n  min time in ' + \
            'pool monitoring list:\n         1: IPT0     left =     3 added =     0 ext =     2\n         ' + \
            '2: IPT1     left =     5 added =    10 ext =     3\n  arrival rate:  2 per sec   11 sec\n   ' + \
            '  [20,20,20,20] rate = 800/1000 per sec'
        self.assertEqual(str(p1), check_str.format(str(p1.start_time), str(p1.planned_close_time),
            str(te4.time_occurred), str(te3.time_occurred), str(te2.time_occurred), 
            str(te1.time_occurred)))
        # Now have array of 20's but duration is 25, so won't get better than 800
        # So force to 20 and watch what happens 
        self.assertEqual(p1.get_arrival_rate(20), sys.maxint)
        self.assertEqual(p1.get_arrival_extension(20), 11)
        self.assertEqual(p1.arrival_window_values, [20, 20, 20, 20])
        return
    
    def testAddFourSameOccurred(self):
        '''Test that handles adding multiples with the same incident id
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        # Add 1st
        p1.add_incident(te1, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 22) #20 + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 22)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertEqual(p1.last_incident, te1)
        self.assertEqual(p1.arrival_check_ctl, None)
        self.assertEqual(p1.arrival_window_values, [-1])
        self.assertEqual(p1.use_timer, False)
        self.assertEqual(len(p1.moved_forward), 0)
        self.assertEqual(p1.get_arrival_rate(None), None)
        self.assertEqual(p1.get_arrival_extension(None), 0)
        # Add the 2nd one
        right_now2 = datetime.now()
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertEqual(len(p1.incidents['IPT0']), 2)
        self.assertTrue(p1.contains_incident('E', 'IPT0')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 24) #20 + 2 extension + 2 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 24)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)
        # Add the 3rd one
        right_now3 = datetime.now()
        te3 = teal.Event.fromDict({EVENT_ATTR_REC_ID:3, 
                           EVENT_ATTR_EVENT_ID:'IPT0', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now3,
                           EVENT_ATTR_TIME_LOGGED: right_now3})  
        p1.add_incident(te3, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertEqual(len(p1.incidents['IPT0']), 3)
        self.assertTrue(p1.contains_incident('E', 'IPT0')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 26) #20 + 2 extension + 2 + 2 
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 26)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 3)
        # Add the 4th one
        right_now4 = datetime.now()
        te4 = teal.Event.fromDict({EVENT_ATTR_REC_ID:4, 
                           EVENT_ATTR_EVENT_ID:'IPT0', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now4,
                           EVENT_ATTR_TIME_LOGGED: right_now4})  
        p1.add_incident(te4, 2, 3)
        self.assertEqual(len(p1.incidents), 1)
        self.assertEqual(len(p1.incidents['IPT0']), 4)
        self.assertTrue(p1.contains_incident('E', 'IPT0')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertTrue(te4 in p1.incidents[te4.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 28) #20 + 2 extension + 2 + 2 + 2
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 28)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 4)
        return
#
    
    def testSuppressOne(self):
        '''Test that handles simple suppression correctly
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        # Add 1st
        p1.add_incident(te1, 2, 3)
        # Add the 2nd one
        right_now2 = datetime.now()
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        self.assertEqual(len(p1.min_time_incidents), 2)

        # Have te2 supresses te1
        p1.suppresses(te2, set([te1]))
        # Stuff shouldn't have changed 
        self.assertEqual(len(p1.incidents), 1)
        self.assertTrue(p1.contains_incident('E', 'IPT0')) 
        self.assertTrue(p1.contains_incident('E', 'IPT1')) 
        self.assertFalse(te1.event_id in p1.incidents.keys())
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        self.assertEqual(len(p1.suppressed), 1)
        self.assertTrue(te1 in p1.suppressed[te1.event_id])
        self.assertFalse(te2.event_id in p1.suppressed.keys())
        self.assertEqual(len(p1.suppressions), 1)
        self.assertEqual(len(p1.min_time_incidents), 2)
        # Check that suppression occurred
        sup1 = p1.get_suppressed(te1)
        self.assertEqual(len(sup1), 0) # it was suppressed
        sup2 = p1.get_suppressed(te2)
        self.assertEqual(len(sup2), 1)
        self.assertTrue(te1 in sup2)
        self.assertTrue(p1.is_suppressed(te1))
        self.assertFalse(p1.is_suppressed(te2))
        
        # Suppress with empty set should do nothing
        p1.suppresses(te1, set())
        sup1 = p1.get_suppressed(te1)
        self.assertEqual(len(sup1), 0) # it was suppressed
        sup2 = p1.get_suppressed(te2)
        self.assertEqual(len(sup2), 1)
        self.assertTrue(te1 in sup2)
        self.assertTrue(p1.is_suppressed(te1))
        self.assertFalse(p1.is_suppressed(te2))
        self.assertEqual(len(p1.suppressed), 1)
        self.assertFalse(te1.event_id in p1.incidents.keys())
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te1 in p1.suppressed[te1.event_id])
        self.assertFalse(te2.event_id in p1.suppressed.keys())
        self.assertEqual(len(p1.suppressions), 1)
        self.assertEqual(len(p1.min_time_incidents), 2)
        
        # Force te2 to be suppressed
        p1.force_suppressed(te2)
        sup1 = p1.get_suppressed(te1)
        self.assertEqual(len(sup1), 0) # it was suppressed
        sup2 = p1.get_suppressed(te2)
        self.assertEqual(len(sup2), 1)
        self.assertTrue(te1 in sup2)
        self.assertTrue(p1.is_suppressed(te1))
        self.assertTrue(p1.is_suppressed(te2))
        self.assertEqual(len(p1.suppressed), 2)
        self.assertFalse(te1.event_id in p1.incidents.keys())
        self.assertFalse(te2.event_id in p1.incidents.keys())
        self.assertTrue(te1 in p1.suppressed[te1.event_id])
        self.assertTrue(te2 in p1.suppressed[te2.event_id])
        self.assertEqual(len(p1.suppressions), 1)
        self.assertEqual(len(p1.min_time_incidents), 2)
        return

    def testSuppressSelf(self):
        '''Test that handles suppressing itself 
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        # Add 1st
        p1.add_incident(te1, 2, 3)
        # Add the 2nd one
        right_now2 = datetime.now()
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        # Have te2 suppresses te1
        p1.suppresses(te1, set([te1]))
        # Stuff shouldn't have changed 
        self.assertTrue(p1.contains_incident('E', 'IPT0')) 
        self.assertTrue(p1.contains_incident('E', 'IPT1')) 
        self.assertEqual(len(p1.incidents), 1)
        self.assertFalse(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertEqual(len(p1.suppressed), 1)
        self.assertTrue(te1 in p1.suppressed[te1.event_id])
        self.assertFalse(te2 in p1.suppressed[te2.event_id])
        self.assertEquals(len(p1.suppressions), 1)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        # test that suppression occurred
        sup1 = p1.get_suppressed(te1)
        self.assertEqual(len(sup1), 1) 
        self.assertTrue(te1 in sup1)
        sup2 = p1.get_suppressed(te2)
        self.assertEqual(len(sup2), 0)
        return

    def testSuppressMany(self):
        '''Test that handles suppressing more than one at a time 
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        # Add 1st
        p1.add_incident(te1, 2, 3)
        # Add the 2nd one
        right_now2 = datetime.now()
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        # Add the 3rd one
        right_now3 = datetime.now()
        te3 = teal.Event.fromDict({EVENT_ATTR_REC_ID:3, 
                           EVENT_ATTR_EVENT_ID:'IPT2', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now3,
                           EVENT_ATTR_TIME_LOGGED: right_now3})  
        p1.add_incident(te3, 0, 0)
        # Add the 4th one
        right_now4 = datetime.now()
        te4 = teal.Event.fromDict({EVENT_ATTR_REC_ID:4, 
                           EVENT_ATTR_EVENT_ID:'IPT3', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now4,
                           EVENT_ATTR_TIME_LOGGED: right_now4})  
        p1.add_incident(te4, 0, 0)
        self.assertEqual(len(p1.incidents), 4)
        self.assertEqual(len(p1.suppressed), 0)
        self.assertEqual(len(p1.suppressions), 0)
        
        # Suppress
        p1.suppresses(te3, set([te2, te4]))
        # Should have changed
        self.assertEqual(len(p1.incidents), 2)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(p1.contains_incident('E', 'IPT1'))        
        self.assertTrue(p1.contains_incident('E', 'IPT2'))
        self.assertTrue(p1.contains_incident('E', 'IPT3')) 
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertFalse(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertFalse(te4 in p1.incidents[te4.event_id])
        self.assertEqual(len(p1.suppressed), 2)
        self.assertFalse(te1.event_id in p1.suppressed.keys())
        self.assertTrue(te2 in p1.suppressed[te2.event_id])
        self.assertFalse(te3.event_id in p1.suppressed.keys())
        self.assertTrue(te4 in p1.suppressed[te4.event_id])
        self.assertEqual(len(p1.suppressions), 1)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 25) #20 + 2 extension + 3 extension + 0 + 0
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 25)
        self.assertEqual(p1.close_callback, None)
        # Suppression checks
        sup1 = p1.get_suppressed(te1)
        self.assertEqual(len(sup1), 0) 
        sup2 = p1.get_suppressed(te2)
        self.assertEqual(len(sup2), 0) 
        sup3 = p1.get_suppressed(te3)
        self.assertEqual(len(sup3), 2) 
        self.assertTrue(te2 in sup3)
        self.assertTrue(te4 in sup3)
        sup4 = p1.get_suppressed(te4)
        self.assertEqual(len(sup4), 0) 
        return

    
class TestIncidentPoolStates(TealTestCase):

    def setUp(self):
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        self.callback_occurred = False
        self.callback_rec_id = -3
        self.my_event = multiprocessing.Event()

    def tearDown(self):
        self.my_event.clear()
        self.teal.shutdown()
    
    def setCallbackOccurred(self, reason, rec_id):
        '''Callback test method
        
           Set a flag and the event
        '''
        self.callback_occurred = True
        self.callback_reason = reason
        self.callback_rec_id = rec_id
        self.my_event.set()
        return

    def testStatesBasic(self):
        '''Test basic state transitions
        '''
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        # Start Manually
        right_now = datetime.now()
        p1.start(right_now)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close
        close_time = right_now + timedelta(seconds=11)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        return

    def testStatesNotAllowed(self):
        '''Test state transitions and operations not allowed in certain states
        '''
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        right_now = datetime.now()
        close_time = right_now + timedelta(seconds=5)
        # Start Manually
        right_now = datetime.now()
        p1.start(right_now)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Can't restart
        self.assertRaises(IncidentPoolStateTransitionError, p1.start, right_now)
        # Close
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # add_incident to closed pool should be detected
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'idvalue0', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertRaises(IncidentPoolClosedError, p1.add_incident, te1, 2, 3)
        # Can't restart
        self.assertRaises(IncidentPoolStateTransitionError, p1.start, right_now)
        return
    
    def testStatesCloseBeforeStart(self):
        '''Test check that can't close before start ''' 
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        # Start Manually
        right_now = datetime.now()
        p1.start(right_now)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close -- with bad times
        close_time = right_now - timedelta(seconds=11)
        self.assertRaises(IncidentPoolStateTransitionError, p1.close, close_time, 0)
        # Check nothing changed
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        return

    def testStatesCloseWithoutStart(self):
        '''Test check that correctly close without start''' 
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        # Close -- with bad times
        close_time = datetime.now()
        p1.close(close_time, 0)
        # Check nothing changed
        self.assertEqual(p1.start_time, None)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual(p1.planned_close_time, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        self.assertRaises(IncidentPoolClosedError, p1.add_incident, None, 0, 0)
        return

    def testStatesFailure(self):
        '''Test check that correctly close without start''' 
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        # Close -- with bad times
        p1.failed()
        # Check nothing changed
        self.assertEqual(p1.start_time, None)
        self.assertEqual(p1.close_time, None)
        self.assertEqual(p1.planned_close_time, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_FAILED)
        self.assertRaises(IncidentPoolFailedError, p1.add_incident, None, 0, 0)
        return

    def testCloseCallbackForceClose(self):
        '''Test callback on transition to close state
        '''
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, self.setCallbackOccurred)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.close_callback, self.setCallbackOccurred)
        # Start Manually
        right_now = datetime.now()
        p1.start(right_now)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close
        close_time = right_now + timedelta(seconds=11)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        self.my_event.wait(10)
        self.assertTrue(self.callback_occurred)
        self.assertEqual(self.callback_reason, 0)
        self.assertEqual(self.callback_rec_id, None)
        self.assertRaises(IncidentPoolClosedError, p1.add_incident, None, 0, 0)
        return
 
    def testCloseCallbackForceShutdownRunning(self):
        '''Test callback on shutdown when Running
        '''
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, self.setCallbackOccurred)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.close_callback, self.setCallbackOccurred)
        # Start Manually
        right_now = datetime.now()
        p1.start(right_now)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Make sure no event has occurred
        self.my_event.wait(1)
        self.assertFalse(self.callback_occurred)
        # Force shutdown
        p1.shutdown()
        # Close
        self.assertEqual(p1.close_time, p1.planned_close_time)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        self.my_event.wait(10)
        self.assertTrue(self.callback_occurred)
        self.assertEqual(self.callback_reason, POOL_CLOSE_REASON_SHUTDOWN)  
        self.assertEqual(self.callback_rec_id, None)     
        return
   
    def testCloseCallbackForceShutdownNew(self):
        '''Test callback on shutdown when New
        '''
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, self.setCallbackOccurred)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.close_callback, self.setCallbackOccurred)
        # Make sure no event has occurred
        self.my_event.wait(1)
        self.assertFalse(self.callback_occurred)
        # Force shutdown
        shutdown_time = datetime.now()
        p1.shutdown()
        # Close
        self.assertEqual((p1.close_time - shutdown_time).seconds, 20)
        self.assertEqual((p1.start_time - shutdown_time).seconds, 0)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, p1.close_time)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        self.my_event.wait(10)
        self.assertTrue(self.callback_occurred)
        self.assertEqual(self.callback_reason, POOL_CLOSE_REASON_SHUTDOWN) 
        self.assertEqual(self.callback_rec_id, None)
        return        
 
    def testCloseCallbackClosedByIncidentH(self):
        '''Test callback on closure when incident beyond close time
        '''
        # New Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 12, None, self.setCallbackOccurred)
        self.assertEqual(p1.duration, 12)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.close_callback, self.setCallbackOccurred)
        # Make sure no event has occurred
        self.my_event.wait(1)
        self.assertFalse(self.callback_occurred)
        # Add the events        
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        # Add 1st
        p1.add_incident(te1, 2, 3)
        # Add the 2nd one
        right_now2 = datetime.now()
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        # Add the 3rd one
        right_now3 = datetime.now()
        te3 = teal.Event.fromDict({EVENT_ATTR_REC_ID:3, 
                           EVENT_ATTR_EVENT_ID:'IPT2', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now3,
                           EVENT_ATTR_TIME_LOGGED: right_now3})  
        p1.add_incident(te3, 0, 0)
        # Make sure it worked
        self.assertEqual(len(p1.incidents), 3)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(p1.contains_incident('E', 'IPT1'))        
        self.assertTrue(p1.contains_incident('E', 'IPT2'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 17) #12 + 2 extension + 3 extension + 0 
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 17)
        self.assertEqual(p1.close_callback, self.setCallbackOccurred)
        #
        # Add the 4th one beyond the end --> closes
        right_now4 = right_now + timedelta(seconds=30)
        te4 = teal.Event.fromDict({EVENT_ATTR_REC_ID:4, 
                           EVENT_ATTR_EVENT_ID:'IPT3', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now4,
                           EVENT_ATTR_TIME_LOGGED: right_now4})  
        self.assertRaises(IncidentPoolClosedError, p1.add_incident, te4, 0, 0)
        self.my_event.wait(10)
        self.assertTrue(self.callback_occurred)
        self.assertEqual(self.callback_reason, POOL_CLOSE_REASON_INCIDENT_TIME)   
        self.assertEqual(self.callback_rec_id, te3.rec_id)    
        # only state should have changed
        self.assertEqual(len(p1.incidents), 3)
        self.assertTrue(p1.contains_incident('E', 'IPT0'))
        self.assertTrue(p1.contains_incident('E', 'IPT1'))        
        self.assertTrue(p1.contains_incident('E', 'IPT2'))
        self.assertTrue(te1 in p1.incidents[te1.event_id])
        self.assertTrue(te2 in p1.incidents[te2.event_id])
        self.assertTrue(te3 in p1.incidents[te3.event_id])
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 17) #12 + 2 extension + 3 extension + 0 
        self.assertEqual((p1.start_time - right_now).seconds, 0)
        self.assertEqual((p1.planned_close_time - p1.start_time).seconds, 17)
        self.assertEqual(p1.close_time, p1.planned_close_time)
        self.assertEqual(p1.close_callback, self.setCallbackOccurred)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        return


class TestIncidentPoolNext(TealTestCase):

    def setUp(self):
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
    
    def tearDown(self):
        self.teal.shutdown()

    def testNextFromEmpty(self):
        '''Test the next_pool constructor with an empty pool
        '''
        # Historic
        # Create first pool 
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # Start Manually
        right_now = datetime.now()
        p1.start(right_now)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close
        close_time = right_now + timedelta(seconds=11)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        self.assertEqual(len(p1.min_time_incidents), 0)
        # call on closed pool
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 0)
        self.assertEquals(len(p2.suppressed), 0)
        self.assertEquals(len(p2.suppressions), 0)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_NEW)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 20)
        self.assertEqual(p2.close_callback, None)
        return
        
    def testNextUSOneNoMin(self):
        '''Test that an un-suppressed incident with no min in pool time is correctly handled
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT3', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT3'))
        p1.add_incident(te1, 0, 0)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=18)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                           EVENT_ATTR_EVENT_ID:'IPT2', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now2,
                           EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT2'))
        p1.add_incident(te2, 0, 0)
        # Check things ok
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close manually
        close_time = right_now + timedelta(seconds=20)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual(p1.start_time, right_now)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.planned_close_time, right_now + timedelta(seconds=20))
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # call on closed pool 
        self.assertEqual(len(p1.min_time_incidents), 0)
        self.assertFalse( te1 in p1.min_time_incidents.keys())
        self.assertFalse( te2 in p1.min_time_incidents.keys())
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 0)
        self.assertEquals(len(p2.suppressed), 0)
        self.assertEquals(len(p2.suppressions), 0)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_NEW)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 20)
        self.assertEqual(p2.close_callback, None)
        return
    
    def testNextSOneNoMin1(self):
        '''Test that a suppressed incident with no min in pool time is correctly handled
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT3', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT3'))
        p1.add_incident(te1, 0, 0)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=18)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT2', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT2'))
        p1.add_incident(te2, 0, 0)
        # Check things ok
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(((right_now + timedelta(seconds=20)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Suppress one with itself
        p1.suppresses(te1, set([te1]))
        # Close manually
        close_time = right_now + timedelta(seconds=20)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(((right_now + timedelta(seconds=20)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # call on closed pool 
        self.assertEqual(len(p1.min_time_incidents), 0)
        self.assertFalse( te1 in p1.min_time_incidents.keys())
        self.assertFalse( te2 in p1.min_time_incidents.keys())
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 0)
        self.assertEquals(len(p2.suppressed), 0)
        self.assertEquals(len(p2.suppressions), 0)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_NEW)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 20)
        self.assertEqual(p2.close_callback, None)
        return

    def testNextSOneNoMin2(self):
        '''Test that two suppressed incidents with no min in pool time is correctly handled
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT3'))
        p1.add_incident(te1, 2, 3)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=18)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT2'))
        p1.add_incident(te2, 3, 5)
        # Check things ok
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Suppress one with itself
        p1.suppresses(te1, set([te1]))
        p1.suppresses(te1, set([te2]))
        # Close manually
        close_time = right_now + timedelta(seconds=25)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # call on closed pool 
        self.assertEqual(len(p1.min_time_incidents), 0)
        self.assertFalse( ('E', te1.rec_id) in p1.min_time_incidents)
        self.assertFalse( ('E', te2.rec_id) in p1.min_time_incidents)
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 0)
        self.assertEquals(len(p2.suppressed), 0)
        self.assertEquals(len(p2.suppressions), 0)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_NEW)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 20)
        self.assertEqual(p2.close_callback, None)
        return
         
    def testNextUSOneWMin1(self):
        '''Test that an un-suppressed incident with a min in pool time met is correctly handled
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=22)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                           EVENT_ATTR_EVENT_ID:'IPT1', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now2,
                           EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT1'))
        p1.add_incident(te2, 3, 5)
        # Check things ok
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close manually
        close_time = right_now + timedelta(seconds=25)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # call on closed pool 
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertFalse( te1 in p1.min_time_incidents.keys())
        self.assertTrue( te2 in p1.min_time_incidents.keys())
        # Create next 
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 1)
        self.assertFalse(te1 in p2.incidents[te1.event_id])
        self.assertTrue(te2 in p2.incidents[te2.event_id])
        self.assertEquals(len(p2.suppressed), 0)
        self.assertEquals(len(p2.suppressions), 0)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_RUNNING)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 23) # initial + 3 for moved forward!
        self.assertEqual(p2.close_callback, None)
        return 
         
    def testNextUSOneWMin1b(self):
        '''Test that a suppressed incident with a min in pool time met is correctly handled
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEquals(len(p1.suppressed), 0)
        self.assertEquals(len(p1.suppressions), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=22)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT1'))
        p1.add_incident(te2, 3, 5)
        # Check things ok
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Suppress
        p1.suppresses(te2, set([te2]))
        # Close manually
        close_time = right_now + timedelta(seconds=25)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # call on closed pool 
        self.assertEqual(len(p1.min_time_incidents), 1)
        self.assertFalse(te1 in p1.min_time_incidents.keys())
        self.assertTrue(te2 in p1.min_time_incidents.keys())
        # Create next 
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 0)
        self.assertFalse(te1 in p2.incidents)
        self.assertFalse(te2 in p2.incidents)
        self.assertEquals(len(p2.suppressed), 1)
        self.assertTrue(te2 in p2.suppressed[te2.event_id])
        self.assertEquals(len(p2.suppressions), 1)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_RUNNING)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 23) # initial + 3 for moved forward!
        self.assertEqual(p2.close_callback, None)
        return 
    
    def testNextUSIncidentsOneWMin2(self):
        '''Test that an un-suppressed incident with a min in pool time not met is correctly handled
        '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=10)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT1'))
        p1.add_incident(te2, 3, 5)
        # Check things ok
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        # Close manually
        close_time = right_now + timedelta(seconds=25)
        p1.close(close_time, 0)
        self.assertEqual(p1.close_time, close_time)
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 25)
        self.assertEqual(((right_now + timedelta(seconds=25)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_CLOSED)
        # call on closed pool 
        self.assertEqual(len(p1.min_time_incidents), 0)
        self.assertFalse( te1 in p1.min_time_incidents.keys())
        self.assertFalse( te2 in p1.min_time_incidents.keys())
        # Create next 
        p2 = IncidentPool.next_pool(p1)
        self.assertEqual(len(p2.incidents), 0)
        self.assertFalse(te1 in p2.incidents[te1.event_id])
        self.assertFalse(te2 in p2.incidents[te2.event_id])
        self.assertEquals(len(p2.suppressed), 0)
        self.assertFalse(te2 in p2.suppressed)
        self.assertEquals(len(p2.suppressions), 0)
        self.assertEqual(p2.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p2.state, POOL_STATE_NEW)
        self.assertEqual(p2.timer, None)
        self.assertEqual(p2.duration, 20)
        self.assertEqual(p2.close_callback, None)
        return
         
    def testMaxDurationSetting(self):
        ''' Test that the max duration is checked and set properly'''
        # Make sure can't be negative
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, POOL_MODE_OCCURRED, 300, -23)
        self.assertRaises(IncidentPoolConfigError, IncidentPool.new_pool, POOL_MODE_LOGGED, 300, 20)
        # Make sure it gets set
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, 304)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.max_duration, 304)
        self.assertEqual(p1.close_callback, None)
        # Make sure it defaults
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.max_duration, 300) # Default when None
        self.assertEqual(p1.close_callback, None)
        return
    
    def testZMaxDurationExecution(self):
        ''' Check that duration is not allowed to exceed the maximum '''
        # Historic
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, 41)
        self.assertEqual(len(p1.incidents), 0)
        self.assertEqual(p1.mode, POOL_MODE_OCCURRED)
        self.assertEqual(p1.state, POOL_STATE_NEW)
        self.assertEqual(p1.timer, None)
        self.assertEqual(p1.duration, 20)
        self.assertEqual(p1.max_duration, 41)
        self.assertEqual(p1.close_callback, None)
        # start by adding an event 
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        # Add another one 
        right_now2 = right_now + timedelta(seconds=5)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                           EVENT_ATTR_EVENT_ID:'IPT6', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now2,
                           EVENT_ATTR_TIME_LOGGED: right_now2})  
        self.assertFalse(p1.contains_incident('E', 'IPT6'))
        p1.add_incident(te2, 100, 0)
        # Check things ok
        self.assertEqual((right_now - p1.start_time).seconds, 0)
        self.assertEqual(p1.duration, 41)
        self.assertEqual(p1.max_duration, 41)
        self.assertEqual(((right_now + timedelta(seconds=41)) - p1.planned_close_time).seconds, 0)
        self.assertEqual(p1.state, POOL_STATE_RUNNING)
        return
    
    
class IPCheckpointTest(IncidentPoolEventCheckpoint):
    ''' Need to provide implementations of stuff to make the checkpoint usable '''
    
    def __init__(self, name, msg_target=None, pool=None):
        IncidentPoolEventCheckpoint.__init__(self, name, msg_target)
        self.pool = pool
        return
    
    def get_pool(self):
        return self.pool
    
    
class TestIncidentPoolCheckpointing(TealTestCase):

    def setUp(self):
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
    
    def tearDown(self):
        self.teal.shutdown()
        
    def testAddFourDiffOccurred(self):
        '''Test that handles adding 2nd and detects adding same incident twice 
        '''
        
        ac1 = ArrivalCheckCtl(window_min=4, window_max=4, arrival_rate=2, extension=11)
        p1 = IncidentPool.new_pool(POOL_MODE_OCCURRED, 20, None, arrival_check_ctl=ac1)
        cp = IPCheckpointTest('TestingCP', None, p1)
        # Make sure init correctly
        self.assertEqual(cp.start_rec_id, None)
        self.assertEqual(cp.data, None)
        # set from the pool and make sure doesn't change
        cp.set_checkpoint_from_pool()
        self.assertEqual(cp.start_rec_id, None)
        self.assertEqual(cp.data, None)
        self.assertEqual(cp.start_rec_id, None)
        # Add event
        right_now = datetime.now()
        te1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                                   EVENT_ATTR_EVENT_ID:'IPT0', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now,
                                   EVENT_ATTR_TIME_LOGGED: right_now})  
        self.assertFalse(p1.contains_incident('E', 'IPT0'))
        p1.add_incident(te1, 2, 3)
        # Set and check
        cp.set_checkpoint_from_pool()
        self.assertEqual(cp.start_rec_id, 0)
        expected = '["{0}", "1", ["1U-19+2"]]'.format(str(right_now + timedelta(seconds=p1.duration)))
        self.assertEqual(cp.data, expected)
        self.assertEqual(cp.start_rec_id, 0)
        # Add a 2nd one 
        right_now2 = right_now + timedelta(seconds=10)
        te2 = teal.Event.fromDict({EVENT_ATTR_REC_ID:2, 
                                   EVENT_ATTR_EVENT_ID:'IPT1', 
                                   EVENT_ATTR_SRC_COMP: 'TC', 
                                   EVENT_ATTR_TIME_OCCURRED: right_now2,
                                   EVENT_ATTR_TIME_LOGGED: right_now2})  
        p1.add_incident(te2, 3, 5)
        # Set and check
        cp.set_checkpoint_from_pool()
        self.assertEqual(cp.start_rec_id, 0)
        expected = '["{0}", "2", ["1U-22+2","2U-10+3"]]'.format(str(right_now + timedelta(seconds=p1.duration)))
        self.assertEqual(cp.data, expected)
        self.assertEqual(cp.start_rec_id, 0) 
        # Add a 3rd
        right_now3 = right_now2 + timedelta(seconds=3)
        te3 = teal.Event.fromDict({EVENT_ATTR_REC_ID:3, 
                           EVENT_ATTR_EVENT_ID:'IPT2', 
                           EVENT_ATTR_SRC_COMP: 'TC', 
                           EVENT_ATTR_TIME_OCCURRED: right_now3,
                           EVENT_ATTR_TIME_LOGGED: right_now3})  
        p1.add_incident(te3, 0, 300)
        # Set and check
        cp.set_checkpoint_from_pool()
        self.assertEqual(cp.start_rec_id, 0)
        expected = '["{0}", "3", ["1U-22+2","2U-10+3","3U288"]]'.format(str(right_now + timedelta(seconds=p1.duration)))
        self.assertEqual(cp.data, expected)
        self.assertEqual(cp.start_rec_id, 0)
        # Close the pool and see that updates correctly
        p1.close(right_now3, 5)
        cp.set_checkpoint_from_pool()      
        self.assertEqual(cp.start_rec_id, 2) 
        expected = '["{0}", "3", ["3U288"]]'.format(str(right_now + timedelta(seconds=p1.duration)))
        self.assertEqual(cp.data, expected)
        return

if __name__ == "__main__":
    unittest.main()
    