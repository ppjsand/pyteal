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

import unittest
import time
import multiprocessing

from ibm import teal
from ibm.teal.registry import get_logger, SHUTDOWN_MODE_IMMEDIATE
from ibm.teal.util.listenable_queue import QueueListener, ListenableQueue
from ibm.teal.control_msg import CONTROL_MSG_TYPE_END_OF_DATA, ControlMsg
from ibm.teal.teal import TEAL_SHUTDOWN_MODE
from ibm.teal.test.teal_unittest import TealTestCase

class SampleQueueListenerT(QueueListener):
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue
        self.queue.register_listener(self)
        self.notifications = []
        self.shutdown_immediate_flag = False 
        QueueListener.__init__(self)
        return
    
    def get_name(self):
        return self.name
    
    def notify(self, item):
        # p rint 'notified about ' + item
        self.notifications.append(item)
        if isinstance(item, ControlMsg) and (item.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            self.queue.unregister_listener(self)
        return True
    
    def shutdown_immediate(self):
        self.shutdown_immediate_flag = True
    
    
class SampleQueueListenerF(QueueListener):
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue
        self.queue.register_listener(self)
        self.notifications = []
        self.shutdown_immediate_flag = False 
        QueueListener.__init__(self)
        return
    
    def get_name(self):
        return self.name
    
    def notify(self, item):
        # p rint 'notified about ' + item
        self.notifications.append(item)
        if isinstance(item, ControlMsg) and (item.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            self.queue.unregister_listener(self)
        return False
    
    def shutdown_immediate(self):
        self.shutdown_immediate_flag = True
    
    
class SampleQueueListenerWD(QueueListener):
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue
        self.queue.register_listener(self)
        self.notifications = []
        self.shutdown_immediate_flag = False 
        QueueListener.__init__(self)
        return
    
    def get_name(self):
        return self.name
    
    def notify(self, item):
        # p rint 'notified about ' + item
        self.notifications.append(item)
        # Don't unregister ... so this will hang if we wait for unregister 
        #if isinstance(item, ControlMsg) and (item.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
        #    self.queue.unregister_listener(self)
        return False
    
    def shutdown_immediate(self):
        self.shutdown_immediate_flag = True


class ListenableQueueTest(TealTestCase):

    def setUp(self):
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        self.callback_occurred = False
        self.callback_item = None
        self.my_event = multiprocessing.Event()

    def tearDown(self):
        self.my_event.clear()
        self.teal.shutdown()

    def process_callback(self, item):
        self.callback_occurred = True
        self.callback_item = item
        self.my_event.set()
        return
    
    def testBasicOne(self):
        '''Test that one listener works'''
        lq = ListenableQueue('Queue 01')
        listener1 = SampleQueueListenerT('Listener 01T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        item = 'Item 01'
        lq.put_nowait(item)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        lq.shutdown()
        self.assertFalse(listener1.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 2)
        return
    
    def testBasicTwo(self):
        '''Test that two listeners work'''
        lq = ListenableQueue('Queue 02')
        listener1 = SampleQueueListenerT('Listener 01T', lq)
        listener2 = SampleQueueListenerT('Listener 02T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        self.assertEqual(len(listener2.notifications), 0)
        item = 'Item 02'
        lq.put_nowait(item)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 1)
        self.assertTrue(item in listener2.notifications)
        # unregister listener
        lq.unregister_listener(listener1)
        item2 = 'Item 03'
        lq.put_nowait(item2)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications),1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 2)
        self.assertTrue(item in listener2.notifications)
        self.assertTrue(item2 in listener2.notifications)
        lq.shutdown()
        self.assertFalse(listener1.shutdown_immediate_flag)
        self.assertFalse(listener2.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 1) # It was unregsitered before shutdown!
        self.assertEqual(len(listener2.notifications), 3)
        return
        
    def testCallback(self):
        '''Test that callback work when all false '''
        lq = ListenableQueue('Queue 03', self.process_callback)
        listener1 = SampleQueueListenerF('Listener 01F', lq)
        listener2 = SampleQueueListenerF('Listener 02F', lq)
        self.assertEqual(len(listener1.notifications), 0)
        self.assertEqual(len(listener2.notifications), 0)
        item = 'Item 02'
        lq.put_nowait(item)
        self.my_event.wait(2)
        self.assertEqual(self.callback_occurred, True)
        self.assertEqual(self.callback_item, item)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 1)
        self.assertTrue(item in listener2.notifications)
        lq.shutdown()
        self.assertFalse(listener1.shutdown_immediate_flag)
        self.assertFalse(listener2.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 2)
        self.assertEqual(len(listener2.notifications), 2)
        return
    
    def testNoCallback(self):
        '''Test callback isn't called when 2nd True'''
        lq = ListenableQueue('Queue 03', self.process_callback)
        listener1 = SampleQueueListenerF('Listener 01F', lq)
        listener2 = SampleQueueListenerT('Listener 02T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        self.assertEqual(len(listener2.notifications), 0)
        item = 'Item 02'
        lq.put_nowait(item)
        self.my_event.wait(2)
        self.assertEqual(self.callback_occurred, False)
        self.assertEqual(self.callback_item, None)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 1)
        self.assertTrue(item in listener2.notifications)
        lq.shutdown()
        self.assertFalse(listener1.shutdown_immediate_flag)
        self.assertFalse(listener2.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 2)
        self.assertEqual(len(listener2.notifications), 2)
        return
    
    
class ListenableQueueTest2(TealTestCase):

    def setUp(self):
        self.keep_mode = self.force_env(TEAL_SHUTDOWN_MODE, SHUTDOWN_MODE_IMMEDIATE)
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        self.callback_occurred = False
        self.callback_item = None
        self.my_event = multiprocessing.Event()

    def tearDown(self):
        self.my_event.clear()
        self.teal.shutdown()
        self.restore_env(TEAL_SHUTDOWN_MODE, self.keep_mode)

    def process_callback(self, item):
        self.callback_occurred = True
        self.callback_item = item
        self.my_event.set()
        return

    def testBasicOne(self):
        '''Test that one listener works'''
        lq = ListenableQueue('Queue 01')
        listener1 = SampleQueueListenerT('Listener 01T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        item = 'Item 01'
        lq.put_nowait(item)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        lq.shutdown()
        self.assertTrue(listener1.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 1)  # EOD is not sent
        return
    
    def testBasicTwo(self):
        '''Test that two listeners work'''
        lq = ListenableQueue('Queue 02')
        listener1 = SampleQueueListenerT('Listener 01T', lq)
        listener2 = SampleQueueListenerT('Listener 02T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        self.assertEqual(len(listener2.notifications), 0)
        item = 'Item 02'
        lq.put_nowait(item)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 1)
        self.assertTrue(item in listener2.notifications)
        # unregister listener
        lq.unregister_listener(listener1)
        item2 = 'Item 03'
        lq.put_nowait(item2)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications),1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 2)
        self.assertTrue(item in listener2.notifications)
        self.assertTrue(item2 in listener2.notifications)
        lq.shutdown()
        self.assertFalse(listener1.shutdown_immediate_flag) # It was unregistered before shutdown!
        self.assertTrue(listener2.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 1) # It was unregistered before shutdown!
        self.assertEqual(len(listener2.notifications), 2) # EOD is not sent
        return
        
    def testCallback(self):
        '''Test that callback work when all false '''
        lq = ListenableQueue('Queue 03', self.process_callback)
        listener1 = SampleQueueListenerF('Listener 01F', lq)
        listener2 = SampleQueueListenerF('Listener 02F', lq)
        self.assertEqual(len(listener1.notifications), 0)
        self.assertEqual(len(listener2.notifications), 0)
        item = 'Item 02'
        lq.put_nowait(item)
        self.my_event.wait(2)
        self.assertEqual(self.callback_occurred, True)
        self.assertEqual(self.callback_item, item)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 1)
        self.assertTrue(item in listener2.notifications)
        lq.shutdown()
        self.assertTrue(listener1.shutdown_immediate_flag)
        self.assertTrue(listener2.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 1) # EOD not sent
        self.assertEqual(len(listener2.notifications), 1) # EOD not sent
        return
    
    def testNoCallback(self):
        '''Test callback isn't called when 2nd True'''
        lq = ListenableQueue('Queue 03', self.process_callback)
        listener1 = SampleQueueListenerF('Listener 01F', lq)
        listener2 = SampleQueueListenerT('Listener 02T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        self.assertEqual(len(listener2.notifications), 0)
        item = 'Item 02'
        lq.put_nowait(item)
        self.my_event.wait(2)
        self.assertEqual(self.callback_occurred, False)
        self.assertEqual(self.callback_item, None)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        self.assertEqual(len(listener2.notifications), 1)
        self.assertTrue(item in listener2.notifications)
        lq.shutdown()
        self.assertTrue(listener1.shutdown_immediate_flag)
        self.assertTrue(listener2.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 1) # EOD not sent
        self.assertEqual(len(listener2.notifications), 1) # EOD not sent
        return
    
    def testNoUnregister(self):
        '''Test that one listener works'''
        lq = ListenableQueue('Queue 01')
        listener1 = SampleQueueListenerWD('Listener 01T', lq)
        self.assertEqual(len(listener1.notifications), 0)
        item = 'Item 01'
        lq.put_nowait(item)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        lq.shutdown()
        self.assertTrue(listener1.shutdown_immediate_flag)
        self.assertEqual(len(listener1.notifications), 1)  # EOD is not sent
        return
    


if __name__ == "__main__":
    unittest.main()