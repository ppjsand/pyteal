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


class Journalable(object):
    '''The Journalable ABC is used to allow things to be put into a Journal'''
 
    __metaclass__ = ABCMeta
   
    @abstractmethod
    def write_to_dictionary(self):
        '''Be able to write my attributes to a dictionary and return it'''
        return 
    
# TODO: Make sure this is not used
#    @abstractmethod
#    def read_from_dictionary(self, in_dict):
#        '''Be able to set my attributes from a dictionary'''
#        return
        