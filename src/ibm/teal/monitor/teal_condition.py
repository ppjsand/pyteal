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

import threading
import sys

class Condition(object):
    '''
    This class is used to notify the teal framework when events are only
    added within the same process that the teal framework is running
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.condition = threading.Condition()
        self.value = 0
        
    def post(self):
        ''' 
        Send a notification to the monitor to indicate that an
        event has been added to the event log
        '''
        self.condition.acquire()
        if self.value != sys.maxint:
            self.value = self.value + 1
        self.condition.notify()
        self.condition.release()
    
    def wait(self):
        '''
        Wait for events to be added to the event log
        '''
        self.condition.acquire()
        while (self.value == 0):
            self.condition.wait()
        self.value = 0    
        self.condition.release()
        return 0