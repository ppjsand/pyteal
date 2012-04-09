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
 
from threading import Timer
from datetime import datetime

from ibm.teal.registry import get_logger
from ibm.teal.util.teal_thread import ThreadKilled


class ExtendableTimer(object):
    '''This is a timer that can have its time extended by calling add_time
    '''

    def __init__(self, timeout_default,callback):
        '''Specify the default timeout to use and what to call back when the timeout occurs
        '''
        self.timeout_default = timeout_default
        self.callback = callback
        self.timeout_current = 0
        self.timeout_sofar = 0
        self.timeout_total = 0
        self.my_timer = None
        self.timeout_start = datetime.now()
        self.timeout_end = self.timeout_start
        get_logger().debug('Creating timer with default {0}'.format(str(self.timeout_default)))
        return
    
    def __del__(self):
        '''Make sure the timer gets canceled when this goes out of scope
        '''
        get_logger().debug('Deleting timer')
        self.cancel()
        
    def __str__(self):
        return 'Timer delta = ' + str( self.get_delta())
      
    def get_delta(self):
        return self.timeout_end - self.timeout_start
        
    def start(self, timeout=None):
        '''Start the timer
        
        Supports overriding the default timeout
        '''
        self.timeout_start = datetime.now()
        if timeout is None:
            timeout = self.timeout_default
        get_logger().debug('Starting timer at {0} with timeout {1}'.format(str(self.timeout_start),str(timeout)))
        self.timeout_current = timeout
        self.timeout_sofar = timeout
        self.timeout_total = timeout
        self.timeout_end = self.timeout_start
        self.my_timer = Timer(timeout, self.internal_timeout)
        self.my_timer.start()
        return
        
    def add_time(self,time_to_add):
        '''Extend the timer by the specified amount of time
        
        If negative, it will be subtracted from the total time, but will
        not interrupt the current timer.
        '''
        self.timeout_total += time_to_add
        get_logger().debug('Extending timer by {0} to {1}'.format(str(time_to_add),self.timeout_total))
        return
        
    def cancel(self):
        '''Cancel the timer
        '''
        get_logger().debug('Canceling timer')
        if self.my_timer is not None:
            self.my_timer.cancel()
        self.callback = None 
        return
             
    def internal_timeout(self):
        '''Internal method to process the Timer timeout used in the implementation
        '''
        if self.timeout_sofar < self.timeout_total:
            self.timeout_current = self.timeout_total - self.timeout_sofar
            self.timeout_sofar += self.timeout_current
            get_logger().debug('Extended timer for {0}'.format(str(self.timeout_current)))
            self.my_timer = Timer(self.timeout_current, self.internal_timeout)
            self.my_timer.start()
        else:
            self.timeout_end = datetime.now()
            try:
                get_logger().debug('Completed timer {0}'.format(self.timeout_end))
            except ThreadKilled:
                raise
            except:
                pass
            if self.callback is not None: 
                self.callback()
        return
        