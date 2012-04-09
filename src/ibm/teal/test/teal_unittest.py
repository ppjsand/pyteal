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

import os
import sys
import unittest
import time
from ibm.teal.teal import Teal, TealLogger
from ibm.teal.registry import SERVICE_DB_INTERFACE, get_service, get_logger,\
    SERVICE_LOGGER, register_service, SERVICE_EVENT_Q
from ibm.teal.database import db_interface
from ibm.teal.database import db_interface_pyodbc
from ibm.teal.alert import ALERT_STATE_CLOSED
import platform
import subprocess
from datetime import datetime
import logging


TEAL_TEST_DB_TIME_PATTERN = 'TEAL_TEST_DB_TIME_PATTERN'
TEAL_TEST_MSGLEVEL = 'TEAL_TEST_MSGLEVEL'
DEFAULT_TEST_MSGLEVEL = 'warning' 

def truncate_all_teal_tables():  
    ''' Truncate all of the teal tables ''' 
    myteal = Teal('data/common/dbinterfaceonly.conf', 'stderr', msgLevel='warning')
    dbi = get_service(SERVICE_DB_INTERFACE)
    cnxn = dbi.get_connection()
    cursor = cnxn.cursor()
    # ORDER IS IMPORTANT!
    dbi.truncate(cursor, db_interface.TABLE_CHECKPOINT)
    cnxn.commit()
    dbi.truncate(cursor, db_interface.TABLE_ALERT2ALERT)
    cnxn.commit()
    dbi.truncate(cursor, db_interface.TABLE_ALERT2EVENT)
    cnxn.commit()
    dbi.delete(cursor, db_interface.TABLE_EVENT_LOG)
    cnxn.commit()
    # Must close all alerts before they can be removed
    #   don't have to worry about relationships because they are all gone
    dbi.update(cursor, ['state'], db_interface.TABLE_ALERT_LOG, parms=(ALERT_STATE_CLOSED,))
    cnxn.commit()
    dbi.delete(cursor, db_interface.TABLE_ALERT_LOG)
    cnxn.commit()
    cnxn.close()
    myteal.shutdown()
    return

def get_table_date_time_pattern():
    time_pattern = os.environ.get(TEAL_TEST_DB_TIME_PATTERN, None)

    if time_pattern is None:
        myteal = Teal('data/common/dbinterfaceonly.conf', 'stderr', msgLevel='warning')
        dbi = get_service(SERVICE_DB_INTERFACE)
        if isinstance(dbi, db_interface_pyodbc.DBInterfacePyODBC):
            if isinstance(dbi.sql_generator, db_interface_pyodbc.SQLGeneratorDB2):
                time_pattern = '%Y-%m-%d %H:%M:%S.%f'
            elif isinstance(dbi.sql_generator, db_interface_pyodbc.SQLGeneratorMySQL):
                time_pattern = '%Y-%m-%d %H:%M:%S'
            else:
                print 'Unknown generator type ... unable to determine pattern'
        else:
            print 'Unknown DB Interface type ... unable to determine pattern'
        myteal.shutdown()
    return time_pattern

def apply_time_pattern(in_timestamp_str_list, time_pattern):
    result = []
    for in_timestamp_str in in_timestamp_str_list:
        tmp_timestamp = datetime.strptime(in_timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        result.append(datetime.strftime(tmp_timestamp, time_pattern))
    return result


class TealTestCase(unittest.TestCase):
    '''Add TEAL testing helpers to the unittest support'''
    
    def __init__(self, methodName='runTest'):
        ''' set the msglevel ''' 
        self.msglevel = os.environ.get(TEAL_TEST_MSGLEVEL, DEFAULT_TEST_MSGLEVEL)
        unittest.TestCase.__init__(self, methodName)
        
    def assertRaisesTealError(self, exception, msg, method, *args, **kwargs):
        ''' Call the method and check for the exception and check its string'''
        try:
            method(*args, **kwargs)
        except exception as e:
            self.assertEqual(msg, e.msg)
            return
        except BaseException, e:
            print 'Expected %s got %s' % (exception, e.__class__,)
            self.assertRaises(exception, method, *args)
        self.fail('Exception %s did not occur' % (exception,))
        return
    
    def prepare_db(self):
        truncate_all_teal_tables()
        return
    
    def force_env(self, var_name, new_value):
        ''' force the environment variable to the specified value
            return the info for restore_env method 
        '''
        try:
            restore_value = os.environ[var_name]
        except:
            restore_value = None
        os.environ[var_name] = new_value
        return restore_value
    
    def remove_env(self, var_name):
        ''' force the environment variable to the specified value
            return the info for restore_env method 
        '''
        try:
            restore_value = os.environ[var_name]
            del os.environ[var_name]
        except:
            restore_value = None
        return restore_value
    
    def restore_env(self, var_name, restore_value):
        ''' restore the environment variable to the restore value from the force_env method
        '''
        if restore_value:
            os.environ[var_name] = restore_value
        else:
            try:
                del os.environ[var_name]
            except:
                pass
        return
    
    def _run_cmd(self, var_list):
        ''' Run the command with the variable list passed '''
        if platform.system() == 'Windows':
            var_list.insert(0,'python')
        process = subprocess.Popen(var_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        return (process.returncode, output[0].strip(), output[1].strip())

    def assertCmdFails(self, var_list, exp_err_msg='', exp_good_msg='', exp_rc=2, print_out=False):
        ''' Make sure command fails and that returns the right message '''
        rc, good_out, err_out = self._run_cmd(var_list)  
        if rc != exp_rc or print_out == True:
            print 'rc = ', rc
            print 'good_out = ', good_out
            print 'err_out = ', err_out
        self.assertEqual(rc, exp_rc)
        self.assertEqual(exp_err_msg.replace("\n","").replace("\r",""), err_out.replace("\n","").replace("\r",""))
        self.assertEqual(good_out.replace("\n","").replace("\r",""), exp_good_msg.replace("\n","").replace("\r",""))
        return
    
    def assertCmdWorks(self, var_list, exp_good_msg='', exp_err_msg='', exp_good_msg_ranges=None, print_out=False, alt_exp_good_msgs=None):
        ''' Make sure command works and that returns the right message '''
        rc, good_out, err_out = self._run_cmd(var_list)  
        if rc != 0 or print_out == True:
            print 'rc = ', rc
            print 'good_out = ', good_out
            print 'err_out = ', err_out
        self.assertEqual(rc, 0)
        if alt_exp_good_msgs is None:
            alt_exp_good_msgs = [exp_good_msg]
        else:
            alt_exp_good_msgs.append(exp_good_msg)
        good_fail = True
        for tmp_good_msg in alt_exp_good_msgs:
            if exp_good_msg_ranges is None:
                if tmp_good_msg.replace("\n","").replace("\r","") == good_out.replace("\n","").replace("\r",""):
                    good_fail = False
                    break
            else:
                tmp_exp = ''
                tmp_out = ''
                for rstart, rend in exp_good_msg_ranges:
                    tmp_exp += tmp_good_msg[rstart:rend].replace("\n","").replace("\r","")
                    tmp_out += good_out[rstart:rend].replace("\n","").replace("\r","")
                if tmp_exp == tmp_out:
                    good_fail = False
                    break
        if good_fail == True:
            if len(alt_exp_good_msgs) > 1:
                self.fail('{0} did not match any of the allowable outputs {1}'.format(good_out, str(alt_exp_good_msgs)))  
            else:
                self.fail('{0} did not match {1}'.format(good_out, alt_exp_good_msgs[0]))  
        self.assertEqual(err_out.replace("\n","").replace("\r",""), exp_err_msg.replace("\n","").replace("\r",""))
        return
    
    def create_temp_logger(self, msg_level):
        ''' Create a temporary logger if one isn't available '''
        if get_logger() is None:
            # Create and register the logger
            logging.setLoggerClass(TealLogger)
            logger = logging.getLogger('tealLogger')
        
            if msg_level is None: 
                # basically throw away logs 
                hdlr = logging.handlers.MemoryHandler(100, logging.NOTSET, target=None)
            else:
                # send logs to stdout
                hdlr = logging.StreamHandler(sys.stdout)
                        
            log_format =  "%(asctime)-15s [%(process)d:%(thread)d] UT:%(module)s - %(levelname)s: %(message)s"
            formatter = logging.Formatter(log_format)
            hdlr.setFormatter(formatter)
            logger.addHandler(hdlr)
            
            # Define the string levels and set them in the logger
            levels = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL}
            
            # Set the lowest level of message to log
            level = levels.get(msg_level, logging.NOTSET)
            logger.setLevel(level)
        
            register_service(SERVICE_LOGGER, logger)
                
        return
    
    def assertGEARAnalyzerGotEvents(self, name, num_events, time_out=120):
        ''' Assert that the GEAR analyzer named name in the config has received the num_events before 
            the time_out value 
            
            Note that analysis by GEAR will move things to another collection
        '''
        # TODO: Check all of the incident pool collections
        # Find the analyzer
        eq = get_service(SERVICE_EVENT_Q)
        for method in eq.listener_methods:
            if method.__self__.get_name() == name:
                ea = method.__self__
        if ea is None:
            self.fail('GEAR event analyzer {0} was not active'.format(name))
        # Now wait for the three entries to get into the pool 
        count = 0
        while len(ea.engine.event_pool.incidents) < num_events:
            if count > time_out:
                self.fail('Waited for events too long for events to get to pool')
            time.sleep(1)
            count += 1

            
