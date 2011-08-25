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

from abc import ABCMeta, abstractmethod


class AlertFilter(object):
    '''The AlertFilter class is the base class for modules that
    determine if alerts should be filtered or not.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, name, config_dict=None):
        '''The constructor'''
        self.name = name
        return
    
    def get_name(self):
        '''Get the name of the listener.'''
        return self.name

    @abstractmethod
    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on
        '''
        pass
    
    @abstractmethod
    def resolve_and_validate(self, info_dict):
        ''' Perform any detailed resolution and validation '''
        pass
    
    