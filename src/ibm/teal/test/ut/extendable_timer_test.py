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
import multiprocessing
from datetime import timedelta

from ibm import teal
from ibm.teal.util.extendable_timer import ExtendableTimer
from ibm.teal.registry import get_logger


class TestBasicTimer(unittest.TestCase):

    def setUp(self):
        '''Setup for logging, an event and an timer to use for testing
        '''
        if get_logger() is None: 
            teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        self.timeout_occurred = False
        self.my_event = multiprocessing.Event()
        self.timer = ExtendableTimer(5, self.setTimeoutOccurred)
        return

    def tearDown(self):
        '''Clear the event and cancel the timer
        '''
        self.my_event.clear()
        self.timer.cancel()
        return
        
    def setTimeoutOccurred(self):
        '''Callback when timer completes
        
        Set a flag and the event
        '''
        # print 'In setTimeoutOccurred'
        self.timeout_occurred = True
        self.my_event.set()
        return
    
    def testTimeoutCancel(self):
        '''Make sure the timeout cancels
        
        Start timer, wait a couple of seconds, cancel, 
        then wait beyond when timeout would have occurred
        '''
        self.timer.start()
        self.my_event.wait(2)
        self.timer.cancel()
        self.my_event.wait(5)
        self.assertFalse(self.timeout_occurred)
        return
 
    def testTimeoutFail(self):
        '''Make sure the timeout doesn't occur right away
        
        Start timer, wait a couple of seconds and then check
        '''
        self.timer.start()
        self.my_event.wait(2)
        self.assertFalse(self.timeout_occurred)
        return
    
    def testTimeoutPass(self):
        '''Make sure the timeout does occur
        
        Start timer and wait on the event past when it should occur
        '''
        self.timer.start()
        self.my_event.wait(10)
        self.assertTrue(self.timeout_occurred)
        # The next test isn't 100% true ... timers don't have to be exact
        self.assertEqual(self.timer.get_delta().seconds,5)
        return
    
    def testTimeoutExtendFail(self):
        '''Make sure that the time does extend
        
        Start timer, extend, wait more than the initial value but less than the
        extension and make sure we timeout before that.
        '''
        self.timer.start()
        self.timer.add_time(5)  # Now 10
        self.my_event.wait(8)
        self.assertFalse(self.timeout_occurred)
        return
        
    def testTimeoutExtendPass(self):
        '''Make sure that the time does extend and times out
        
        Start timer, extend, wait more than the the new timeout and make sure 
        the timeout occurs
        '''
        self.timer.start()
        self.timer.add_time(5)  # Now 10
        self.my_event.wait(20)
        self.assertTrue(self.timeout_occurred)
        # The next test isn't 100% true ... timers don't have to be exact
        self.assertEqual(self.timer.get_delta().seconds, 10)
        return
          
    def testTimeoutStartLess(self):
        '''Make sure the time start value overrides
        
        Start timer with shorter value, wait less than original value, 
        make sure timeout occurs
        '''
        self.timer.start(2)
        self.my_event.wait(3)
        self.assertTrue(self.timeout_occurred)
        # The next test isn't 100% true ... timers don't have to be exact
        self.assertEqual(self.timer.get_delta().seconds,2)
        return

    def testTimeoutExtendPass1(self):
        '''Make sure extensions accumulate
        
        Start timer, wait 2, extend timer, extend timer, ensure timeout
        '''
        self.timer.start()
        self.my_event.wait(2)
        self.timer.add_time(5)  # Now 10
        self.timer.add_time(2)  # Now 12
        self.my_event.wait(20)
        self.assertTrue(self.timeout_occurred)
        # The next test isn't 100% true ... timers don't have to be exact
        self.assertEqual(self.timer.get_delta().seconds,timedelta(seconds=12).seconds)
        return
    
    def testTimeoutExtendPass2(self):
        '''Make sure subsequent extensions accumulate
        
        Start timer, wait 2, extend timer, wait into extension, extend timer, ensure timeout
        '''
        self.timer.start()
        self.my_event.wait(2)
        self.timer.add_time(5)  # Now 10
        self.my_event.wait(6)
        self.timer.add_time(5)  # Now 15
        self.my_event.wait(20)
        self.assertTrue(self.timeout_occurred)
        # The next test isn't 100% true ... timers don't have to be exact
        self.assertEqual(15, self.timer.get_delta().seconds)
        return

if __name__ == "__main__":
    unittest.main()