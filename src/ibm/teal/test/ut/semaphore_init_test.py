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

from ibm.teal import Teal

class TealTestSemaphoreInit(unittest.TestCase):
    '''Test the situation where TEAL starts and then shuts down immediately without
    processing events. Testing to ensure the monitor semaphore which is touched during
    shutdown is initialized correctly.'''

    
    def setUp(self):
        '''Setup Teal'''
        self.teal = Teal('data/checkpoint_test/configurationtest_05_semaphore.conf', 'stderr', msgLevel='info')
        return
    
    def tearDown(self):
        '''Teardown teal'''

        if self.teal is not None:
            self.teal.shutdown()
        return    
    

    def testTealSemaphoreInit(self):
        '''Test checkpoint value after inserting into an empty db.'''
        # If there is a problem, the shutdown process would throw
        # an exception.
        return

if __name__ == "__main__":
    unittest.main()
