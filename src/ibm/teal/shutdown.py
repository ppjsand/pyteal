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

from threading import Event, Lock

class Shutdown(object):
    def __init__(self, callback):
        ''' Constructor '''
        self.shutdown_cb = callback
        self.shutdown_complete = False
        self.notif_event = Event()
        self.shutdown_lock = Lock() 
        
    def notify(self):    
        ''' Used to notify waiters to initiate a shutdown '''
        self.notif_event.set()

    def shutdown(self):
        ''' Execute the shutdown process '''
        # Only call the callback once. Multiple calls to
        # this method will just return once the condition
        # has occurred
        self.shutdown_lock.acquire()    
        if (self.shutdown_complete is False):
            self.shutdown_complete = True
            self.shutdown_cb()
        self.shutdown_lock.release()
        
        # Notify anybody waiting for a signal to start 
        # a shutdown so they can complete
        self.notify()    
                
    def wait(self):
        ''' Wait for notification of shutdown to proceed '''
        # Wait for someone to initiate the shutdown
        while not self.notif_event.is_set():
            self.notif_event.wait(1000000000)
        self.shutdown()
            
if __name__ == '__main__':
    pass