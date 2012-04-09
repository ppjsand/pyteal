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

from threading import Thread
import ctypes
import exceptions
from ibm.teal.registry import get_logger

# TODO: This class is a work around that should be removed when moving to Python 3.x
class ThreadKilled(exceptions.Exception):
    ''' Exception to kill the thread 
    
        This exception is created asynchronously on a thread to cause it to be killed.
        
        It cannot have any construction arguments
        
    ''' 
    pass

# TODO: This class is a work around that should be removed when moving to Python 3.x
class TealThread(Thread):
    ''' Add a Thread class that supports killing the thread
    
        This is a workaround for the problem that an abandoned (not joined) thread can be reactivated 
        after the main process has ended but before the process is clean up.  The abandoned thread can
        then access things it shouldn't and thus cause a segmentation fault.
        
        This is fixed in Python 3.x
    '''
    
    def kill_thread_using_exception(self):
        if self.isAlive():
            get_logger().debug('Sending ThreadKill exception to {0}'.format(self.ident))
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), ctypes.py_object(ThreadKilled))
    