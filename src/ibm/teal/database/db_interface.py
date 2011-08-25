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

# These globals will be dynamically changed
TABLE_EVENT_LOG = ''
TABLE_CHECKPOINT = ''
TABLE_ALERT_LOG = ''
TABLE_ALERT2ALERT = ''
TABLE_ALERT2EVENT = ''
TABLE_TEMPLATE = ''

class DBInterface:

    '''The DBinterface class is an abstract base class for a family of classes
    that enable generic access to different databases.   It abstracts out the 
    retrieval of the configuration information and the generate of the correct
    SQL string for the DB being targeted.
    
    It provides the connect() method which returns a connection object that
    is then used for working with the DB
    
    It provides the gen_*() methods which return the SQL strings to use for the 
    DB being used
    
    It provides insert(), update(), and select() methods that take a cursor and
    internally generate an use the string on the specified command.
    
    '''
    
    __metaclass__ = ABCMeta

    def __init__(self, config_dict):
        
        ''' The constructor. 
        '''
        return

    @abstractmethod
    def get_connection(self):
        ''' Return connection to the database.
        '''
        pass
    
    @abstractmethod
    def gen_insert(self, fields, table):
        ''' return the generated insert string
        '''
        pass 
       
    @abstractmethod
    def gen_insert_dependent(self, pk_field, fields, table):
        ''' return the generated insert string
        '''
        pass 
       
    @abstractmethod
    def gen_select(self, fields, table, where=None, where_fields=None, order=None):
        ''' return the generated select string
        '''
        pass    
       
    @abstractmethod
    def gen_select_max(self, fields, table):
        ''' return the generated select max string
        '''
        pass    
    
    @abstractmethod
    def gen_update(self, fields, table, where=None, where_fields=None):
        ''' return the generated update string
        '''
        pass
    
    @abstractmethod
    def gen_delete(self, table, where=None, where_fields=None):
        ''' return the generated delete string
        '''
        pass    
       
    @abstractmethod
    def insert(self, cursor, fields, table, parms=None):
        ''' execute the insert
        '''
        pass
    
    @abstractmethod
    def insert_dependent(self, cursor, pk_field, fields, table, parms=None):
        ''' execute the insert
        '''
        pass
    
    @abstractmethod
    def select(self, cursor, fields, table, where=None, where_fields=None, order=None, parms=None):
        ''' execute the select
        '''
        pass
    
    @abstractmethod
    def select_max(self, cursor, field, table, parms=None):
        ''' execute the select max
        '''
        pass
    
    @abstractmethod
    def truncate(self, cursor, table):
        ''' truncate the specified table
        '''
        pass
    
    @abstractmethod
    def update(self, cursor, fields, table, where=None, where_fields=None, parms=None):
        ''' execute the update
        '''
        pass

    @abstractmethod
    def delete(self, cursor, table, where=None, where_fields=None, parms=None):
        ''' execute the select
        '''
        pass
    
    