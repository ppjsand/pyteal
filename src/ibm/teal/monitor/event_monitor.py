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
'''
Created on Mar 31, 2010

@author Matthew Markland
'''


from abc import ABCMeta, abstractmethod

class EventMonitor:
    '''The EventMonitor class is based on the EventMonitor class from BG ELA.
    Making things abstract here based on the Analyzable.py class.
    
    An EventMonitor represents an entity that listens for notifications of changes
    to an underlying data store from which TEAL reads in event information.

    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def shutdown(self):
        ''' Stop the even monitor.
        '''
        return
