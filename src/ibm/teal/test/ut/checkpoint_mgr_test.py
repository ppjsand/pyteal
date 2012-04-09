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

from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.registry import get_service, SERVICE_CHECKPOINT_MGR
from ibm.teal.teal import Teal
import unittest
from ibm.teal.checkpoint_mgr import CHECKPOINT_STATUS_DELETED,\
    CHECKPOINT_STATUS_RUNNING, CHECKPOINT_STATUS_FAILED, EventCheckpoint,\
    CHECKPOINT_STATUS_SHUTDOWN
from ibm.teal.teal_error import ConfigurationError
 
''' Method to use for testing the callback '''
def test_starting_cb_count(start_rec_id, data):
    if data is None:
        return start_rec_id
    else:
        return len(data)


class TealCheckpointMgrTestExecution(TealTestCase):
    
    def setUp(self):        
        self.teal = Teal('data/checkpoint_test/noop_monitor.conf','stderr',msgLevel=self.msglevel, commit_checkpoints=False)
        return 

    def tearDown(self):
        self.teal.shutdown()
        return 
        
    def test_checkpoint001_no_db_init(self):
        ''' 001: Check that the checkpoint service is correctly setup and available '''
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        self.assertNotEqual(checkpoint_mgr, None)
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 0)
        #print str(checkpoint_mgr)
        return 
        
    def test_checkpoint002_no_db_add_one(self):
        ''' 002: Check that a single event checkpoint works '''
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        self.assertNotEqual(checkpoint_mgr, None)
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 0)
        # Create a new checkpoint 
        k_ckpt = EventCheckpoint('test')
        # Validate it got created correctly 
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 1)
        self.assertEqual(k_ckpt.name, 'test')
        self.assertEqual(k_ckpt.get_status(), CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k_ckpt.status, CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k_ckpt.start_rec_id, None)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (None,'recovery'))
        # Set the status and check it got set
        k_ckpt.set_status(CHECKPOINT_STATUS_FAILED)
        self.assertEqual(k_ckpt.get_status(), CHECKPOINT_STATUS_FAILED)
        # Set the checkpoint and check it got set
        k_ckpt.set_checkpoint(345)
        self.assertEqual(k_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k_ckpt.start_rec_id, 345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (345, 'recovery'))
        k_ckpt.set_checkpoint(123, 'data')
        self.assertEqual(k_ckpt.get_checkpoint(), (123, 'data'))
        self.assertEqual(k_ckpt.start_rec_id, 123)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (123, 'recovery'))
        # Delete the checkpoint and check 
        k_ckpt.delete()
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 0)
        self.assertEqual(k_ckpt.status, CHECKPOINT_STATUS_DELETED)
        self.assertEqual(k_ckpt.start_rec_id, None)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (None, 'recovery'))
        return 
        
    def test_checkpoint003_no_db_add_two(self):
        ''' 003: Check that two event checkpoints work '''
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        k1_ckpt = EventCheckpoint('test1')
        k2_ckpt = EventCheckpoint('test2')
        # Validate it got created correctly 
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 2)
        self.assertEqual(k1_ckpt.name, 'test1')
        self.assertEqual(k1_ckpt.get_status(), CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k1_ckpt.status, CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k1_ckpt.start_rec_id, None)
        self.assertEqual(k2_ckpt.name, 'test2')
        self.assertEqual(k2_ckpt.get_status(), CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k2_ckpt.status, CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.start_rec_id, None)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (None, 'recovery'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (None, 'lastproc'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (None, 'recovery'))
        # Set the checkpoint and check it got set
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k1_ckpt.start_rec_id, 345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (345, 'lastproc'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(123, 'data')
        self.assertEqual(k2_ckpt.get_checkpoint(), (123, 'data'))
        self.assertEqual(k2_ckpt.start_rec_id, 123)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (123, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (123, 'data'))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(123, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(123, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(123, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (345, 'lastproc'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(123, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (123, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (123, 'data'))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(123, 'data')
        # Delete the checkpoint and check 
        k2_ckpt.delete()
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 1)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k2_ckpt.status, CHECKPOINT_STATUS_DELETED)
        self.assertEqual(k2_ckpt.start_rec_id, None)
        k1_ckpt.delete()
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 0)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (None, 'recovery'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (None, 'lastproc'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (None, 'recovery'))
        return 
    
    def test_checkpoint004_no_db_cb_test(self):
        ''' 004: Check that the event checkpoint callback gets called '''
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        k1_ckpt = EventCheckpoint('test1')
        k2_ckpt = EventCheckpoint('test2')
        # Validate it got created correctly 
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 2)
        self.assertEqual(k1_ckpt.name, 'test1')
        self.assertEqual(k1_ckpt.get_status(), CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k1_ckpt.status, CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k1_ckpt.start_rec_id, None)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (None, 'lastproc'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (None, 'recovery'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id('recovery'), (None, 'recovery'))
        self.assertEqual(k2_ckpt.name, 'test2')
        self.assertEqual(k2_ckpt.get_status(), CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k2_ckpt.status, CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.start_rec_id, None)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (None, 'recovery'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (None, 'lastproc'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (None, 'recovery'))
        # Set the checkpoint and check it got set
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k1_ckpt.start_rec_id, 345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (345, 'lastproc'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(1, 'data')
        self.assertEqual(k2_ckpt.get_checkpoint(), (1, 'data'))
        self.assertEqual(k2_ckpt.start_rec_id, 1)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (1, 'recovery'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(1, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(1, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (345, 'lastproc'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(1, 'data')
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (1, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (1, 'data'))
        k1_ckpt.set_checkpoint(345)
        k2_ckpt.set_checkpoint(1, 'data')
        # Delete the checkpoint and check 
        k2_ckpt.delete()
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 1)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        self.assertEqual(k2_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (345, 'lastproc'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (345, 'recovery'))
        self.assertEqual(k1_ckpt.get_checkpoint(), (345, None))
        k1_ckpt.set_checkpoint(345)
        self.assertEqual(k2_ckpt.status, CHECKPOINT_STATUS_DELETED)
        self.assertEqual(k2_ckpt.start_rec_id, None)
        k1_ckpt.delete()
        self.assertEqual(len(checkpoint_mgr.event_checkpoints), 0)
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(), (None, 'recovery'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (None, 'lastproc'))
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (None, 'recovery'))
        return 
    
    
    def test_checkpoint005_no_db_cb_test(self):
        ''' 005: Check that the checkpoint state doesn't matter for recovery '''
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        k_list = []
        for i in xrange(0,5):
            k_list.append(EventCheckpoint('test' + str(i)))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        k_force = [ (CHECKPOINT_STATUS_SHUTDOWN, 300, None), 
                    (CHECKPOINT_STATUS_FAILED, 200, None),
                    (CHECKPOINT_STATUS_SHUTDOWN, 3, None),
                    (CHECKPOINT_STATUS_RUNNING, 10, None),
                    (CHECKPOINT_STATUS_SHUTDOWN, 40, None)]
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        for k in k_list:
            print str(k)
        # Check each override option 
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (300, 'lastproc'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (3, 'recovery'))
        for k in k_list:
            if k.name == 'test1':
                self.assertEqual(k.get_status(), CHECKPOINT_STATUS_FAILED)  # Failed aren't touched when recovery mode
            else:
                self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        # Different status            
        k_force = [ (CHECKPOINT_STATUS_SHUTDOWN, 300, None), 
                    (CHECKPOINT_STATUS_SHUTDOWN, 200, None),
                    (CHECKPOINT_STATUS_SHUTDOWN, 345, None),
                    (CHECKPOINT_STATUS_SHUTDOWN, 10, None),
                    (CHECKPOINT_STATUS_SHUTDOWN, 40, None)]
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        for k in k_list:
            print str(k)
        # Check each override option 
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='now'), (None, 'now'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='begin'), (0, 'begin'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='lastproc'), (345, 'lastproc'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        self.assertEqual(checkpoint_mgr.get_starting_event_rec_id(override_restart_mode='recovery'), (10, 'recovery'))
        for k in k_list: 
            self.assertEqual(k.get_status(), CHECKPOINT_STATUS_RUNNING)
        for i in xrange(0,5):
            k_list[i].set_status(k_force[i][0])
            k_list[i].set_checkpoint(k_force[i][1], k_force[i][2])
        return 
    
    
class TealCheckpointMgrTestFailure(TealTestCase):
    
    def test_checkpoint_fail001_bad_restart_mode(self):
        ''' Fail 001: Check bad restart mode caught when overriding on get start event '''
        teal = Teal('data/checkpoint_test/noop_monitor.conf','stderr',msgLevel=self.msglevel, commit_checkpoints=False)
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        self.assertRaisesTealError(ConfigurationError, 'Unrecognized restart mode specified: bad', checkpoint_mgr.get_starting_event_rec_id, override_restart_mode='bad')
        teal.shutdown()
        return

    def test_checkpoint_fail002_bad_restart_mode(self):
        ''' Fail 002: Check bad restart mode caught when creating TEAL '''
        # Exception will also get logged as a startup failure
        self.assertRaisesTealError(ConfigurationError, 'Unrecognized restart mode specified: alsobad', Teal, 'data/checkpoint_test/noop_monitor.conf','stderr', self.msglevel,'alsobad','realtime',False, False, None, False, '', False)
        return 
    
    def test_checkpoint_fail003_deleted_checkpoint(self):
        ''' Fail 003: Check bad restart mode caught when overriding on get start event '''
        teal = Teal('data/checkpoint_test/noop_monitor.conf','stderr',msgLevel=self.msglevel, commit_checkpoints=False)
        #checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        k1_ckpt = EventCheckpoint('deltest1')
        k1_ckpt.set_checkpoint(123, 'data')
        k1_ckpt.delete()
        # Make sure can't get at stuff
        self.assertEqual(k1_ckpt.get_status(), CHECKPOINT_STATUS_DELETED)
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_status(CHECKPOINT_STATUS_RUNNING)
        self.assertEqual(k1_ckpt.get_status(), CHECKPOINT_STATUS_DELETED)
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        k1_ckpt.set_checkpoint(555, 'moredata')
        self.assertEqual(k1_ckpt.get_status(), CHECKPOINT_STATUS_DELETED)
        self.assertEqual(k1_ckpt.get_checkpoint(), (None, None))
        teal.shutdown()
        return

        
if __name__ == "__main__":
    unittest.main()
