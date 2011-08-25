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
from datetime import datetime,timedelta 

from ibm import teal
#from ibm.teal.Event import EventMetadataMissingError
from ibm.teal import Teal
from ibm.teal.event import EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID, EVENT_ATTR_TIME_OCCURRED, \
        EVENT_ATTR_TIME_LOGGED, EVENT_ATTR_SRC_COMP, EVENT_ATTR_SRC_LOC, \
        EVENT_ATTR_SRC_LOC_TYPE, EVENT_ATTR_RPT_COMP, EVENT_ATTR_RPT_LOC, \
        EVENT_ATTR_RPT_LOC_TYPE, EVENT_ATTR_EVENT_CNT, EVENT_ATTR_ELAPSED_TIME, \
        EVENT_ATTR_RAW_DATA_FMT, EVENT_ATTR_RAW_DATA, Event
from ibm.teal.location import Location
from ibm.teal.extdata import EXT_DATA_RAW_DATA
from ibm.teal.test.teal_unittest import TealTestCase

class EventTest(TealTestCase):
    
    def setUp(self):
        self.teal = Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
          
    def tearDown(self):
        '''Nothing to do ... yet
        '''
        self.teal.shutdown()
 
    def testCreateRecIdOnly(self):
        '''Test basic event creation
        '''
        te1 = teal.Event(1)
        self.assertEquals(te1.get_rec_id(), 1)
        # Can't use any other get methods, since they will try to
        #  load the Event from the DB is they are not set
        self.assertEquals(te1.event_id, None)
        self.assertEquals(te1.time_occurred, None)
        self.assertEquals(te1.time_logged, None)
        self.assertEquals(te1.src_comp, None)
        self.assertEquals(te1.src_loc, None)
        self.assertEquals(te1.rpt_comp, None)
        self.assertEquals(te1.rpt_loc, None)
        self.assertEquals(te1.event_cnt, None)
        self.assertEquals(te1.elapsed_time, None)
        self.assertEquals(te1.raw_data, None)
        # No associations
        # Not valid because missing required fields
        self.assertFalse(te1.is_valid())
        return
    
    def testCreateDict(self):
        '''Create from a dictionary'''
        right_now = datetime.now()
        crt_dict = {}
        crt_dict[EVENT_ATTR_REC_ID] = 2
        crt_dict[EVENT_ATTR_EVENT_ID] = 'Event2'
        crt_dict[EVENT_ATTR_TIME_OCCURRED] = right_now
        crt_dict[EVENT_ATTR_TIME_LOGGED] = right_now + timedelta(seconds=1)
        crt_dict[EVENT_ATTR_SRC_COMP] = 'SC'
        crt_dict[EVENT_ATTR_SRC_LOC] = 'SCL'
        crt_dict[EVENT_ATTR_SRC_LOC_TYPE] = 'S'
        crt_dict[EVENT_ATTR_RPT_COMP] = 'RC'
        crt_dict[EVENT_ATTR_RPT_LOC] = 'RL'
        crt_dict[EVENT_ATTR_RPT_LOC_TYPE] = 'S'
        crt_dict[EVENT_ATTR_EVENT_CNT] = 12
        crt_dict[EVENT_ATTR_ELAPSED_TIME] = 4
        crt_dict[EVENT_ATTR_RAW_DATA_FMT] = long('0x5445535400000001',16)
        crt_dict[EVENT_ATTR_RAW_DATA] = 'When in the course'
        te1 = teal.Event(in_dict=crt_dict)
        self.assertEquals(te1.get_rec_id(), 2)
        # Can't use any other get methods, since they will try to
        #  load the Event from the DB is they are not set
        self.assertEquals(te1.event_id, crt_dict[EVENT_ATTR_EVENT_ID])
        self.assertEquals(te1.time_occurred, crt_dict[EVENT_ATTR_TIME_OCCURRED])
        self.assertEquals(te1.time_logged, crt_dict[EVENT_ATTR_TIME_LOGGED])
        self.assertEquals(te1.src_comp, crt_dict[EVENT_ATTR_SRC_COMP])
        self.assertEquals(te1.src_loc.get_location(), crt_dict[EVENT_ATTR_SRC_LOC])
        self.assertEquals(te1.src_loc.get_id(), crt_dict[EVENT_ATTR_SRC_LOC_TYPE])
        self.assertEquals(te1.rpt_comp, crt_dict[EVENT_ATTR_RPT_COMP])
        self.assertEquals(te1.rpt_loc.get_location(), crt_dict[EVENT_ATTR_RPT_LOC])
        self.assertEquals(te1.rpt_loc.get_id(), crt_dict[EVENT_ATTR_RPT_LOC_TYPE])
        self.assertEquals(te1.event_cnt, crt_dict[EVENT_ATTR_EVENT_CNT])
        self.assertEquals(te1.elapsed_time, crt_dict[EVENT_ATTR_ELAPSED_TIME])
        self.assertEquals(te1.raw_data[EXT_DATA_RAW_DATA], crt_dict[EVENT_ATTR_RAW_DATA])
        # No associations
        # Not valid because has all required fields
        self.assertTrue(te1.is_valid())
        # specify a different rec id than in dict
        self.assertRaises(ValueError, Event, 5, crt_dict)
        del crt_dict[EVENT_ATTR_REC_ID]
        # Reuse local
        te1 = Event(5, crt_dict)
        self.assertEquals(te1.get_rec_id(), 5)
        # Can't use any other get methods, since they will try to
        #  load the Event from the DB is they are not set
        self.assertEquals(te1.event_id, crt_dict[EVENT_ATTR_EVENT_ID])
        self.assertEquals(te1.time_occurred, crt_dict[EVENT_ATTR_TIME_OCCURRED])
        self.assertEquals(te1.time_logged, crt_dict[EVENT_ATTR_TIME_LOGGED])
        self.assertEquals(te1.src_comp, crt_dict[EVENT_ATTR_SRC_COMP])
        self.assertEquals(te1.src_loc.get_location(), crt_dict[EVENT_ATTR_SRC_LOC])
        self.assertEquals(te1.src_loc.get_id(), crt_dict[EVENT_ATTR_SRC_LOC_TYPE])
        self.assertEquals(te1.rpt_comp, crt_dict[EVENT_ATTR_RPT_COMP])
        self.assertEquals(te1.rpt_loc.get_location(), crt_dict[EVENT_ATTR_RPT_LOC])
        self.assertEquals(te1.rpt_loc.get_id(), crt_dict[EVENT_ATTR_RPT_LOC_TYPE])
        self.assertEquals(te1.event_cnt, crt_dict[EVENT_ATTR_EVENT_CNT])
        self.assertEquals(te1.elapsed_time, crt_dict[EVENT_ATTR_ELAPSED_TIME])
        self.assertEquals(te1.raw_data[EXT_DATA_RAW_DATA], crt_dict[EVENT_ATTR_RAW_DATA])
        # No associations
        # Not valid because has all required fields
        self.assertTrue(te1.is_valid())
        # Don't specific a rec id
        self.assertRaises(ValueError, Event, in_dict=crt_dict)
        return
    
    def testEventMatch(self):
        '''Test the match method'''
        # Create an event to work with
        right_now = datetime.now()
        crt_dict = {}
        crt_dict[EVENT_ATTR_REC_ID] = 2
        crt_dict[EVENT_ATTR_EVENT_ID] = 'Event2'
        crt_dict[EVENT_ATTR_TIME_OCCURRED] = right_now
        crt_dict[EVENT_ATTR_TIME_LOGGED] = right_now + timedelta(seconds=1)
        crt_dict[EVENT_ATTR_SRC_COMP] = 'SC'
        crt_dict[EVENT_ATTR_SRC_LOC] = 'node##app##pid'
        crt_dict[EVENT_ATTR_SRC_LOC_TYPE] = 'S'
        crt_dict[EVENT_ATTR_RPT_COMP] = 'RC'
        crt_dict[EVENT_ATTR_RPT_LOC] = 'node2##app2##pid'
        crt_dict[EVENT_ATTR_RPT_LOC_TYPE] = 'S'
        crt_dict[EVENT_ATTR_EVENT_CNT] = 12
        crt_dict[EVENT_ATTR_ELAPSED_TIME] = 4
        crt_dict[EVENT_ATTR_RAW_DATA_FMT] = long('0x5445535400000001',16)
        crt_dict[EVENT_ATTR_RAW_DATA] = 'When in the course'
        te1 = teal.Event(in_dict=crt_dict)
        # match(event_id, src_comp, src_loc, rpt_loc, scope)
        # Always matches
        self.assertTrue(te1.match(None, None, None, None, None))
        # Check event id
        self.assertTrue(te1.match('Event2', None, None, None, None))
        self.assertFalse(te1.match('Event3', None, None, None, None))
        # Check src comp
        self.assertTrue(te1.match(None, 'SC', None, None, None))
        self.assertFalse(te1.match(None, 'RC', None, None, None))
        self.assertTrue(te1.match('Event2', 'SC', None, None, None))
        self.assertFalse(te1.match('Event2', 'RC', None, None, None))
        self.assertFalse(te1.match('Event3', 'SC', None, None, None))
        # Check scr loc
        chk_loc1 = Location('S', 'node##app##pid')
        self.assertTrue(te1.match(None, None, chk_loc1, None, None))  
        self.assertTrue(te1.match(None, None, chk_loc1, None, 'application'))  
        self.assertTrue(te1.match(None, None, chk_loc1, None, 'node'))  
        self.assertTrue(te1.match(None, None, chk_loc1, None, 'pid'))  
        self.assertTrue(te1.match('Event2', 'SC', chk_loc1, None, 'node'))
        chk_loc2 = Location('S', 'node##app##pid2')      
        self.assertFalse(te1.match(None, None, chk_loc2, None, None))  
        self.assertTrue(te1.match(None, None, chk_loc2, None, 'application'))  
        self.assertTrue(te1.match(None, None, chk_loc2, None, 'node'))  
        self.assertFalse(te1.match(None, None, chk_loc2, None, 'pid')) 
        self.assertTrue(te1.match('Event2', 'SC', chk_loc2, None, 'node'))
        self.assertFalse(te1.match('Event2', 'SC', chk_loc2, None, 'pid'))
        chk_loc3 = Location('C', 'MB')
        self.assertFalse(te1.match(None, None, chk_loc3, None, None)) 
        self.assertFalse(te1.match(None, None, chk_loc3, None, 'application'))
        # Check rpt_loc
        chk_loc1r = Location('S', 'node2##app2##pid')
        self.assertTrue(te1.match(None, None, None, chk_loc1r, None))
        self.assertTrue(te1.match(None, None, None, chk_loc1r, 'application'))  
        self.assertTrue(te1.match(None, None, None, chk_loc1r, 'node'))  
        self.assertTrue(te1.match(None, None, None, chk_loc1r, 'pid'))  
        self.assertTrue(te1.match(None, None, chk_loc1, chk_loc1r, None))
        self.assertTrue(te1.match(None, None, chk_loc1, chk_loc1r, 'application'))  
        self.assertTrue(te1.match(None, None, chk_loc1, chk_loc1r, 'node'))  
        self.assertTrue(te1.match(None, None, chk_loc1, chk_loc1r, 'pid'))  
        self.assertFalse(te1.match(None, None, chk_loc2, chk_loc1r, 'pid')) 
        chk_loc2r = Location('S', 'node2##app2##pidzzz')
        self.assertFalse(te1.match(None, None, chk_loc1, chk_loc2r, 'pid')) 
        self.assertTrue(te1.match('Event2', 'SC', chk_loc1, chk_loc1r, 'node')) 
        # Test with no rpt loc
        del crt_dict[EVENT_ATTR_RPT_COMP]
        del crt_dict[EVENT_ATTR_RPT_LOC]
        te2 = teal.Event(in_dict=crt_dict)
        self.assertFalse(te2.match('Event2', 'SC', chk_loc1, chk_loc1r, 'node')) 
        self.assertTrue(te2.match('Event2', 'SC', chk_loc1, None, 'node')) 
        return
    
    def testCreateBadlocations(self):
        '''Create from a dictionary with bad locations'''
        keep_env = self.force_env('TEAL_LOCATION_VALIDATION', 'IMMEDIATE')
        right_now = datetime.now()
        crt_dict = {}
        crt_dict[EVENT_ATTR_REC_ID] = 72
        crt_dict[EVENT_ATTR_EVENT_ID] = 'Event 7'
        crt_dict[EVENT_ATTR_TIME_OCCURRED] = right_now
        crt_dict[EVENT_ATTR_TIME_LOGGED] = right_now + timedelta(seconds=1)
        crt_dict[EVENT_ATTR_SRC_COMP] = 'SC'
        crt_dict[EVENT_ATTR_SRC_LOC] = 'Sbad'
        crt_dict[EVENT_ATTR_SRC_LOC_TYPE] = 'DABs'
        crt_dict[EVENT_ATTR_RPT_COMP] = 'RC'
        crt_dict[EVENT_ATTR_RPT_LOC] = 'Rbad'
        crt_dict[EVENT_ATTR_RPT_LOC_TYPE] = 'DABr'
        crt_dict[EVENT_ATTR_EVENT_CNT] = 12
        crt_dict[EVENT_ATTR_ELAPSED_TIME] = 4
        crt_dict[EVENT_ATTR_RAW_DATA_FMT] = long('0x5445535400000001',16)
        crt_dict[EVENT_ATTR_RAW_DATA] = 'When in the course'
        te1 = teal.Event(in_dict=crt_dict)
        self.assertEquals(te1.get_rec_id(), 72)
        # Can't use any other get methods, since they will try to
        #  load the Event from the DB is they are not set
        self.assertEquals(te1.event_id, crt_dict[EVENT_ATTR_EVENT_ID])
        self.assertEquals(te1.time_occurred, crt_dict[EVENT_ATTR_TIME_OCCURRED])
        self.assertEquals(te1.time_logged, crt_dict[EVENT_ATTR_TIME_LOGGED])
        self.assertEquals(te1.src_comp, crt_dict[EVENT_ATTR_SRC_COMP])
        self.assertEquals(te1.src_loc, None)
        self.assertEquals(te1.rpt_comp, crt_dict[EVENT_ATTR_RPT_COMP])
        self.assertEquals(te1.rpt_loc, None)
        self.assertEquals(te1.event_cnt, crt_dict[EVENT_ATTR_EVENT_CNT])
        self.assertEquals(te1.elapsed_time, crt_dict[EVENT_ATTR_ELAPSED_TIME])
        self.assertEquals(te1.raw_data[EXT_DATA_RAW_DATA], crt_dict[EVENT_ATTR_RAW_DATA])
        self.restore_env('TEAL_LOCATION_VALIDATION', keep_env)     
        return
           
if __name__ == "__main__":
    unittest.main()