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
import time
import multiprocessing

from ibm import teal
from ibm.teal.registry import get_logger
from ibm.teal.util.listenable_queue import QueueListener, ListenableQueue

class SampleQueueListenerT(QueueListener):
    def __init__(self, name):
        self.name = name
        self.notifications = []
        QueueListener.__init__(self)
        return
    
    def get_name(self):
        return self.name
    
    def notify(self, item):
        # p rint 'notified about ' + item
        self.notifications.append(item)
        return True
    
    
class SampleQueueListenerF(QueueListener):
    def __init__(self, name):
        self.name = name
        self.notifications = []
        QueueListener.__init__(self)
        return
    
    def get_name(self):
        return self.name
    
    def notify(self, item):
        # p rint 'notified about ' + item
        self.notifications.append(item)
        return False


class ListenableQueueTest(unittest.TestCase):

    def setUp(self):
        if get_logger() is None: 
            teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        self.callback_occurred = False
        self.callback_item = None
        self.my_event = multiprocessing.Event()
        return

    def tearDown(self):
        self.my_event.clear()
        return

    def process_callback(self, item):
        self.callback_occurred = True
        self.callback_item = item
        self.my_event.set()
        return
    

    def testBasicOne(self):
        '''Test that one listener works'''
        lq = ListenableQueue('Queue 01')
        listener1 = SampleQueueListenerT('Listener 01T')
        lq.register_listener(listener1)
        self.assertEqual(len(listener1.notifications), 0)
        item = 'Item 01'
        lq.put_nowait(item)
        time.sleep(1)
        self.assertEqual(len(listener1.notifications), 1)
        self.assertTrue(item in listener1.notifications)
        return
    
    def testBasicTwo(self):
        '''Test that two listeners work'''
        lq = ListenableQueue('Queue 02')
        listener1 = SampleQueueListenerT('Listener 01T')
        listener2 = SampleQueueListenerT('Listener 02T')
        lq.register_listener(listener1)
        lq.register_listener(listener2)
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
        return
        
    def testCallback(self):
        '''Test that callback work when all false '''
        lq = ListenableQueue('Queue 03', self.process_callback)
        listener1 = SampleQueueListenerF('Listener 01F')
        listener2 = SampleQueueListenerF('Listener 02F')
        lq.register_listener(listener1)
        lq.register_listener(listener2)
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
        return
    
    def testNoCallback(self):
        '''Test callback isn't called when 2nd True'''
        lq = ListenableQueue('Queue 03', self.process_callback)
        listener1 = SampleQueueListenerF('Listener 01F')
        listener2 = SampleQueueListenerT('Listener 02T')
        lq.register_listener(listener1)
        lq.register_listener(listener2)
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
        return
    

if __name__ == "__main__":
    unittest.main()