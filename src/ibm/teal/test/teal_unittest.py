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

import os
import unittest
from ibm.teal.teal import Teal
from ibm.teal.registry import SERVICE_DB_INTERFACE, get_service
from ibm.teal.database import db_interface
from ibm.teal.alert import ALERT_STATE_CLOSED
import platform
import subprocess
  
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

class TealTestCase(unittest.TestCase):
    '''Add TEAL testing helpers to the unittest support'''

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
    
    def restore_env(self, var_name, restore_value):
        ''' restore the environment variable to the restore value from the force_env method
        '''
        if restore_value:
            os.environ[var_name] = restore_value
        else:
            del os.environ[var_name]
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
    
    def assertCmdWorks(self, var_list, exp_good_msg='', exp_err_msg='', exp_good_msg_ranges=None, print_out=False):
        ''' Make sure command works and that returns the right message '''
        rc, good_out, err_out = self._run_cmd(var_list)  
        if rc != 0 or print_out == True:
            print 'rc = ', rc
            print 'good_out = ', good_out
            print 'err_out = ', err_out
        self.assertEqual(rc, 0)
        if exp_good_msg_ranges is None:
            self.assertEqual(exp_good_msg.replace("\n","").replace("\r",""), good_out.replace("\n","").replace("\r",""))
        else:
            for rstart, rend in exp_good_msg_ranges:
                self.assertEqual(exp_good_msg[rstart:rend].replace("\n","").replace("\r",""), good_out[rstart:rend].replace("\n","").replace("\r",""))
        self.assertEqual(err_out.replace("\n","").replace("\r",""), exp_err_msg.replace("\n","").replace("\r",""))
        return
