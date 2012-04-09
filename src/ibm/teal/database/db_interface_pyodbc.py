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
from string import Template
import os
import re
import time
import pyodbc

from ibm.teal.registry import get_logger, get_service, TEAL_CONF_DIR
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.database import db_interface

TEAL_TEST_PYODBC_CONFIG = 'TEAL_TEST_PYODBC_CONFIG'
TEAL_TEST_XCAT_CFGLOG_PREFIX = 'TEAL_TEST_XCAT_CFGLOG_PREFIX'

class DBInterfacePyODBC(db_interface.DBInterface):

    '''The DBInterfacePyODBC class implements the DBInterface base class
    so that PyODBC can be used to access the DB
    '''
    
    def __init__(self, config_dict):
        
        ''' The constructor. 
        '''
        CONFIG_KEY = 'config'
        if CONFIG_KEY not in config_dict:
            raise ConfigurationError('DBInterfacePyODBC requires config be specified in the configuration file')
        # See if configuration overridden with environment variable
        config_dict[CONFIG_KEY] = os.environ.get(TEAL_TEST_PYODBC_CONFIG, config_dict[CONFIG_KEY])
        if config_dict[CONFIG_KEY][0] == '{':
            self.sql_generator = ConfigurationEnvVar().get_generator(config_dict[CONFIG_KEY])
        else:
            # create configuration class
            try:
                module_name, class_name = config_dict[CONFIG_KEY].rsplit('.', 1)
                module = __import__(module_name, globals(), locals(), [class_name])
            except ImportError,ie:
                get_logger().error(ie)
                raise # throw the ImportError up the chain
            plugin_class = getattr(module, class_name)
            self.sql_generator = plugin_class().get_generator(config_dict)
        return

    def get_connection(self):
        ''' Return connection to the database.
        '''
        for i in range(5):
            try:
                cnxn = pyodbc.connect(**self.sql_generator.gen_connect())
            except pyodbc.Error, e:
                if (i == 4):
                    get_logger().error('Database connection error: {0}'.format(e))
                    raise
                else:
                    get_logger().warn('Database connection retry: {0}'.format(e))
                    time.sleep(1)
        return cnxn

    def gen_insert(self, fields, table):
        ''' return the generated insert string
        '''
        return self.sql_generator.gen_insert(fields, table) 
       
    def gen_insert_dependent(self, pk_field, fields, table):
        ''' return the generated insert string
        '''
        return self.sql_generator.gen_insert_dependent(pk_field, fields, table) 
       
    def gen_select(self, fields, table, where=None, where_fields=None, order=None):
        ''' return the generated select string
        '''
        return self.sql_generator.gen_select(fields, table, where, where_fields, order) 
       
    def gen_select_max(self, field, table, where=None, where_fields=None):
        ''' return the generated select max string
        '''
        return self.sql_generator.gen_select_max(field, table, where=None, where_fields=None) 
    
    def gen_truncate(self, table):
        ''' return the truncate string
        '''
        return self.sql_generator.gen_truncate(table)
    
    def gen_update(self, fields, table, where=None, where_fields=None):
        ''' return the generated update string
        '''
        return self.sql_generator.gen_update(fields, table, where, where_fields) 
    
    def gen_delete(self, table, where=None, where_fields=None):
        ''' return the generated delete string
        '''
        return self.sql_generator.gen_delete(table, where, where_fields)    

    
    def insert(self, cursor, fields, table, parms=None):
        ''' execute the insert
        '''
        if parms is None:
            return cursor.execute(self.sql_generator.gen_insert(fields, table))
        else:
            return cursor.execute(self.sql_generator.gen_insert(fields, table), parms)

    def insert_dependent(self, cursor, pk_field, fields, table, parms=None):
        ''' execute the insert
        '''
        if parms is None:
            return cursor.execute(self.sql_generator.gen_insert_dependent(pk_field, fields, table))
        else:
            return cursor.execute(self.sql_generator.gen_insert_dependent(pk_field, fields, table), parms)

    def select(self, cursor, fields, table, where=None, where_fields=None, order=None, parms=None):
        ''' execute the select
        '''
        if parms is None:
            return cursor.execute(self.sql_generator.gen_select(fields, table, where, where_fields, order))
        else:
            return cursor.execute(self.sql_generator.gen_select(fields, table, where, where_fields, order), parms)
    
    def select_max(self, cursor, field, table, where=None, where_fields=None, parms=None):
        ''' execute the select max
        '''
        if parms is None:
            return cursor.execute(self.sql_generator.gen_select_max(field, table, where, where_fields))
        else:
            return cursor.execute(self.sql_generator.gen_select_max(field, table, where, where_fields), parms)
    
    def truncate(self, cursor, table):
        ''' truncate the table
        '''
        return cursor.execute(self.sql_generator.gen_truncate(table))
    
    def update(self, cursor, fields, table, where=None, where_fields=None, parms=None):
        ''' execute the update
        '''
        if parms is None:
            return cursor.execute(self.sql_generator.gen_update(fields, table, where, where_fields))
        else:
            return cursor.execute(self.sql_generator.gen_update(fields, table, where, where_fields), parms)
    
    def delete(self, cursor, table, where=None, where_fields=None, parms=None):
        ''' execute the delete
        '''
        if parms is None:
            return cursor.execute(self.sql_generator.gen_delete(table, where, where_fields))
        else:
            return cursor.execute(self.sql_generator.gen_delete(table, where, where_fields),parms)

class Configuration:

    ''' The Configuration class is an abstract base class for a family of classes
    that know how to get the configuration information for PyODBC 
    
    The get_generator method takes a dictionary of configuration keywords 
    that is used in retrieving the configuration and constructs the 
    appropriate SQL generator and returns it
    
    It should also set the correct table name values in the db_interface module
    '''
    
    __metaclass__ = ABCMeta

    def __init__(self):
        
        ''' The constructor. 
        '''
        return

    @abstractmethod
    def get_generator(self, config_dict):
        ''' Return the appropriate SQL generator 
        based on the configuration information retrieved
        '''
        pass


class ConfigurationXCAT(Configuration):

    ''' The ConfigurationXCAT class implements the ABC Configuration 
    to load the DB information from the xCAT configuration file.
    '''
 
    def get_generator(self, config_dict):
        ''' Return the appropriate SQL generator 
        based on the configuration information retrieved
        '''
        DB_CONF_PATH = '{0}/xcat'.format(get_service(TEAL_CONF_DIR))
        prefix = os.environ.get(TEAL_TEST_XCAT_CFGLOG_PREFIX, '')
        DB_CONF_FILE = '{0}cfgloc'.format(prefix)
        
        # Set xCAT table names
        db_interface.TABLE_EVENT_LOG = 'x_tealeventlog'
        db_interface.TABLE_CHECKPOINT = 'x_tealcheckpoint'
        db_interface.TABLE_ALERT_LOG = 'x_tealalertlog'
        db_interface.TABLE_ALERT2ALERT = 'x_tealalert2alert'
        db_interface.TABLE_ALERT2EVENT = 'x_tealalert2event'
        db_interface.TABLE_TEMPLATE = 'x_{0}'

        # Well-known path to the information.
        ds_file = '{0}/{1}'.format(DB_CONF_PATH,DB_CONF_FILE)
        get_logger().debug('DB Configuration: {0}'.format(ds_file))
        
        try:
            conf_file = open(ds_file,'r')
        except IOError, e:
            get_logger().error('Unable to open DB configuration file. {0}'.format(e))
            raise

        db_info = conf_file.readline()
        if(db_info == ""):
            get_logger().error('Unable to retrieve DB configuration information from file {0}'.format(ds_file))
            raise RuntimeError()
        self.raw_driver = db_info
        if(db_info[0] == 'm'):
            # mysql:dbname=xcatdb;host=xcatmn2|xcatadmin|xcat20 
            info = re.match('(\w+):dbname=(\w+);host=([\w\.]+)\|(\w+)\|(\w+)',db_info)
            (db_data,db_name,db_server,db_user,db_pw) = info.groups()
            connect_dict = {'driver':db_data, 'dsn':db_name, 'uid':db_user, 'pwd':db_pw, 'server':db_server}
            get_logger().debug('MySQL connection: {0}'.format(connect_dict))
            return SQLGeneratorMySQL(connect_dict)
        elif(db_info[0] == 'D'):
            # DB/2 format: "DB2:<databasename>|<instancename>|<instancepassword>"
            info = re.match('(\w+):(\w+)\|(\w+)\|(\w+)',db_info)
            (db_data,db_name,db_instance,db_pw) = info.groups()
            # CORRECT------>'DRIVER={DB2};DSN=bgdb0;UID=bgpsysdb;PWD=db24bgp'
            connect_dict = {'driver':db_data, 'dsn':db_name, 'uid':db_instance, 'pwd':db_pw}
            get_logger().debug('DB2 connection: {0}'.format(connect_dict))
            return SQLGeneratorDB2(connect_dict)
        else:
            raise ConfigurationError('Unrecognized db_type in configuration file: {0}'.format(db_info))
            
        return


class ConfigurationConfFile(Configuration):

    ''' The ConfigurationConfFile class implements the ABC Configuration 
    to load the DB information from the configuration file.
    '''
 
    def get_generator(self, config_dict):
        ''' Return the appropriate SQL generator 
        based on the configuration information retrieved
        '''
        db_interface.TABLE_EVENT_LOG = 'x_tealeventlog'
        db_interface.TABLE_CHECKPOINT = 'x_tealcheckpoint'
        db_interface.TABLE_ALERT_LOG = 'x_tealalertlog'
        db_interface.TABLE_ALERT2ALERT = 'x_tealalert2alert'
        db_interface.TABLE_ALERT2EVENT = 'x_tealalert2event'
        db_interface.TABLE_TEMPLATE = 'x_{0}'

        # Set table names
        if 'TABLE_EVENT_LOG' in config_dict:
            db_interface.TABLE_EVENT_LOG = config_dict['TABLE_EVENT_LOG']  
        if 'TABLE_CHECKPOINT' in config_dict:
            db_interface.TABLE_CHECKPOINT = config_dict['TABLE_CHECKPOINT']
        if 'TABLE_ALERT_LOG' in config_dict:
            db_interface.TABLE_ALERT_LOG = config_dict['TABLE_ALERT_LOG']
        if 'TABLE_ALERT2ALERT' in config_dict:
            db_interface.TABLE_ALERT2ALERT = config_dict['TABLE_ALERT2ALERT']
        if 'TABLE_ALERT2EVENT' in config_dict:
            db_interface.TABLE_ALERT2EVENT = config_dict['TABLE_ALERT2EVENT']
        if 'TABLE_TEMPLATE' in config_dict:
            db_interface.TABLE_TEMPLATE = config_dict['TABLE_TEMPLATE']

        # Get the values from the configuration dictionary
        connect_dict = {}
        if 'db_type' not in config_dict:
            raise ConfigurationError('ConfigurationConfFile requires db_type keyword')
        db_type = config_dict['db_type']
        if 'driver' in config_dict:
            connect_dict['driver'] = config_dict['driver']
        if 'dbname' in config_dict:
            connect_dict ['dsn'] = config_dict['dbname']
        if 'user_id' in config_dict:
            connect_dict['uid'] = config_dict['user_id']
        if 'pwd' in config_dict:
            connect_dict['pwd'] = config_dict['pwd']
            
        # Build the connection string
        if(db_type == 'MySQL'):
            get_logger().debug('MySQL connection: {0}'.format(connect_dict))
            return SQLGeneratorMySQL(connect_dict)
        elif(db_type == 'DB2'):
            get_logger().debug('DB2 connection: {0}'.format(connect_dict))
            return SQLGeneratorDB2(connect_dict)
        else:
            raise ConfigurationError('Unrecognized db_type in configuration file: {0}'.format(db_type))
         
        return
    
    
class ConfigurationEnvVar(ConfigurationConfFile):

    ''' The ConfigurationEnvVar class implements the ABC Configuration 
    to load the DB information from the string set on the environment variable.
    '''
 
    def get_generator(self, config_string):
        ''' Return the appropriate SQL generator 
        based on the configuration information retrieved
        '''
        # Get the values from the configuration string
        config_string = config_string.strip('{}').replace(' ', '')
        config_dict = dict(item.split(":") for item in config_string.split(","))
        get_logger().debug('Env var used for config: {0}'.format(config_string))
        return ConfigurationConfFile.get_generator(self, config_dict)


class SQLGenerator:

    ''' The SQLGenerator class is an abstract base class for a family of classes 
    that know how to generate the correct SQL string for the DB they are associated
    with.
    
    The init method takes a the connection string that should be used for the 
    particular instance of the DB it is connecting to.
    '''
    
    __metaclass__ = ABCMeta

    def __init__(self, connect_dict):
        
        ''' The constructor. 
        '''
        self.connect_dict = connect_dict
        return
    
    @abstractmethod
    def gen_field_name(self, field_name):
        ''' return the generated string for the field name 
        '''
        pass
    
    def gen_field_name_subs(self, field_names):
        sub_dict = {}
        for field_name in field_names:
            sub_dict[field_name] = self.gen_field_name(field_name)
        return sub_dict
    
    def gen_where(self, where, where_fields):
        ''' return the where string from the template '''
        return Template(where).substitute(self.gen_field_name_subs(where_fields))

    def gen_connect(self):
        ''' Return the appropriate SQL generator 
        based on the configuration information retrieved
        '''
        return self.connect_dict
    
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
    def gen_truncate(self, table):
        ''' return the generated truncate string 
        '''
        pass
       
    @abstractmethod
    def gen_select_max(self, field, table, where=None, where_fields=None):
        ''' return the generated select max string
        '''
        pass    
    
    @abstractmethod
    def gen_update(self, fields, table, where, where_fields):
        ''' return the generated update string
        '''
        pass
    
    @abstractmethod    
    def gen_delete(self, table, where=None, where_fields=None):
        ''' return the generated delete string
        '''
        pass


class SQLGeneratorDB2(SQLGenerator):

    ''' The SQLGeneratorDB2 class implements the SQLGenarator class so that 
    it generates strings that can be used with PyODBC for working with DB2
    '''
    
    def gen_field_name(self, field_name):
        ''' generate the quoted field name for DB2 '''
        return '"{0}"'.format(field_name)

    def gen_insert(self, fields, table):
        ''' return the generated insert string
        '''
        t = table.upper()
        f = ','.join(map(self.gen_field_name, fields))
        return '''INSERT INTO {0}({1}) VALUES({2})'''.format(t,f,('?, '*len(fields)).rstrip(', '))
       
    def gen_insert_dependent(self, pk_field, fields, table):
        ''' return the generated insert string
        '''
        t = table.upper()
        f = ','.join(map(self.gen_field_name, fields))
        return '''INSERT INTO {0}("{1}",{2}) VALUES(IDENTITY_VAL_LOCAL(),{3})'''.format(t,pk_field,f,('?, '*len(fields)).rstrip(', '))
       
    def gen_select(self, fields, table, where=None, where_fields=None, order=None):
        ''' return the generated select string
        '''
        where_str = ""
        order_str = ""
        
        # Allow the user to select all columns
        if (len(fields) == 1) and (fields[0] == '*'):
            f = fields[0]
        else:
            f = ','.join(map(self.gen_field_name, fields))

        select_str =  '''SELECT {0} FROM {1}'''.format(f, table.upper())
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        if order:
            order_str =  '''ORDER BY "{0}" ASC'''.format(order)
        return ' '.join([select_str, where_str, order_str])
       
    def gen_select_max(self, field, table, where=None, where_fields=None):
        ''' return the generated select max string
        '''
        t = table.upper()
        f = self.gen_field_name(field)
        where_str = ""
        select_str =  '''SELECT max({0}) FROM {1}'''.format(f, t)
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        return ' '.join([select_str, where_str])
    
    def gen_truncate(self, table):
        ''' return the generated truncate string
        '''
        t = table.upper()
        return '''TRUNCATE TABLE {0} IMMEDIATE'''.format(t)
    
    def gen_update(self, fields, table, where=None, where_fields=None):
        ''' return the generated update string
        '''
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        else:
            where_str = ''
        t = table.upper()
        f = ' = ?, '.join(map(self.gen_field_name, fields))+' = ?'
        update_str = '''UPDATE {0} SET {1}'''.format(t, f)
        return ' '.join([update_str, where_str])
    
    def gen_delete(self, table, where=None, where_fields=None):
        ''' return the generated delete string
        '''
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        else:
            where_str = ''
        
        t = table.upper()
        delete_str =  '''DELETE FROM {0}'''.format(t)
        return ' '.join([delete_str,where_str])

MYSQL_KEYWORDS = ['key']

class SQLGeneratorMySQL(SQLGenerator):

    ''' The SQLGeneratorMySQL class implements the SQLGenerator ABC
    and returns strings that can be used with PyODBC to work with MySQL
    '''
    
    def gen_field_name(self, field_name):
        ''' generate the quoted field name for MySQL'''
        if field_name in MYSQL_KEYWORDS:
            return '`{0}`'.format(field_name)
        return field_name

    def gen_insert(self, fields, table):
        ''' return the generated insert string
        '''
        t = table
        f = ','.join(map(self.gen_field_name, fields))
        return '''INSERT INTO {0}({1}) VALUES({2})'''.format(t,f,('?, '*len(fields)).rstrip(', '))

    def gen_insert_dependent(self, pk_field, fields, table):
        ''' return the generated insert string
        '''
        t = table
        f = ','.join(map(self.gen_field_name, fields))
        return '''INSERT INTO {0}({1},{2}) VALUES(LAST_INSERT_ID(),{3})'''.format(t,pk_field,f,('?, '*len(fields)).rstrip(', '))
       
    def gen_select(self, fields, table, where=None, where_fields=None, order=None):
        ''' return the generated select string
        '''
        where_str = ""
        order_str = ""
        f = ','.join(map(self.gen_field_name, fields))
        select_str =  '''SELECT {0} FROM {1}'''.format(f,table)
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        if order:
            order_str =  '''ORDER BY {0} ASC'''.format(order)
        return ' '.join([select_str,where_str,order_str])

    def gen_select_max(self, field, table, where=None, where_fields=None):
        ''' return the generated select max string
        '''
        t = table
        f = self.gen_field_name(field)
        where_str = ""
        select_str =  '''SELECT max({0}) FROM {1}'''.format(f, t)
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        return ' '.join([select_str, where_str])
    
    def gen_truncate(self, table):
        ''' return the generated truncate string
        '''
        t = table
        return '''TRUNCATE TABLE {0}'''.format(t)
    
    def gen_update(self, fields, table, where=None, where_fields=None):
        ''' return the generated update string
        '''
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        else:
            where_str = ''
        t = table
        f = ' = ?, '.join(map(self.gen_field_name, fields))+' = ?'
        update_str = '''UPDATE {0} SET {1}'''.format(t, f)
        return ' '.join([update_str,where_str])

    def gen_delete(self, table, where=None, where_fields=None):
        ''' return the generated delete string
        '''
        if where:
            where_str = '''WHERE {0}'''.format(self.gen_where(where, where_fields))
        else:
            where_str = ''
        
        delete_str =  '''DELETE FROM {0}'''.format(table)
        return ' '.join([delete_str,where_str])
