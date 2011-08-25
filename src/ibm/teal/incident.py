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
from ibm.teal.registry import get_logger
from ibm.teal.processable import Processable


class Incident(Processable):
    '''Base class for incidents in an incident pool
    
    It allows the pool to work with Events and Alerts generically and 
    still enable an analyzer to get to the enclosed event
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        '''Constructor
        '''
        get_logger().debug('Creating Incident')
        return
        
    def __hash__(self):
        '''Hash value for use in sets and as dictionary key'''
        return hash(self.get_type()) + hash(self.get_rec_id())
        
    def __eq__(self, other):
        '''Implementation for equals for use in sets and as dictionary key'''
        return self.get_type() == other.get_type() and self.get_rec_id() == other.get_rec_id()
       
    @abstractmethod    
    def get_rec_id(self):
        '''Get the rec_id which is a unique id for this type of incident'''
        return
    
    @abstractmethod
    def get_incident_id(self):
        '''Get the incident id'''
        return
        
    @abstractmethod
    def get_time_occurred(self):
        '''Get when the incident occurred'''
        return
     
    @abstractmethod
    def get_time_logged(self):
        '''Get when the incident occurred'''
        return
      
    @abstractmethod
    def get_type(self):
        '''Get the type of incident as a single letter'''
        return
    
    @abstractmethod
    def get_metadata(self):
        '''Get the metadata dictionary from the source for this incident'''
        return
    
    @abstractmethod
    def get_analysis_info(self, info_source):
        '''Get the analysis info via double dispatch to the info_source'''
        return 
              
    def as_line(self):
        '''return string to use as a single line description in a display'''
        return self.__str__()  
           
    def brief_str(self): 
        ''' Shortest string that identifies this assuming that consumer know what type it is
        '''
        return '{0}({1})'.format(self.get_incident_id(), self.get_rec_id())   
    
    def __str__(self):
        outstr = 'Incident ' + str(self.get_type()) + ':' + str(self.get_incident_id()) + '(' + str(self.get_rec_id())+ ') at '
        outstr += str(self.get_time_logged())
        return outstr
            
