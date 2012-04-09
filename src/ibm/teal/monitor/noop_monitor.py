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

from ibm.teal.monitor.event_monitor import EventMonitor
from ibm.teal.registry import get_logger

class EventMonitorNoop(EventMonitor):
    '''
    This monitor is used for TEAL framework testing
    '''
    
    def __init__(self,config_dict):
        '''
        Constructor
        '''
        pass
    
    def shutdown(self):
        get_logger().debug('Shutting down')
    
        
