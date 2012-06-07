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

class Processable(object):
    '''The Processable ABC is used to allow things in a ListenableQueue to be processed via a
    double dispatch
    '''
    __metaclass__ = ABCMeta
   
    @abstractmethod
    def process(self, processor, context):
        '''Send myself to the correct method
        
        Should return the result of the specific process call
        '''
        return