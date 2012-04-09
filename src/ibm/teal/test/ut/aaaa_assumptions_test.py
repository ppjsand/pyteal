# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import unittest

from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal import Teal, registry
from ibm.teal.registry import SERVICE_DB_INTERFACE 
from ibm.teal.database import db_interface

class AssumptionsTests(TealTestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def _check_rows(self, table_name, num_rows):
        self.dbi.select(self.cursor, '*', table_name)
        rows = self.cursor.fetchall()
        if len(rows) != num_rows:
            out_msg = 'table {0} had an unexpected number of rows. {1} rows != {2}.'.format(table_name, len(rows), num_rows)
            print out_msg
            print '   ' + str(rows)
            self.fail(out_msg)
    
    def testDBtruncate(self):
        ''' Test that the DB tables correctly truncate '''
        # Truncate the tables 
        self.prepare_db()
        teal = Teal('data/aaaa_assumptions_test/minimal.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)
        self.dbi = registry.get_service(SERVICE_DB_INTERFACE)
        self.cnxn = self.dbi.get_connection()
        self.cursor = self.cnxn.cursor()
        # Check the tables
        self._check_rows(db_interface.TABLE_EVENT_LOG, 0)
        self._check_rows(db_interface.TABLE_ALERT_LOG, 0)
        self._check_rows(db_interface.TABLE_ALERT2ALERT, 0)
        self._check_rows(db_interface.TABLE_CHECKPOINT, 0)
        self.cnxn.close()
        teal.shutdown()
        
        teal = Teal('data/aaaa_assumptions_test/minimal.conf', 'stderr', msgLevel=self.msglevel)
        self.dbi = registry.get_service(SERVICE_DB_INTERFACE)
        self.cnxn = self.dbi.get_connection()
        self.cursor = self.cnxn.cursor()
        # Check the tables
        self._check_rows(db_interface.TABLE_EVENT_LOG, 0)
        self._check_rows(db_interface.TABLE_ALERT_LOG, 0)
        self._check_rows(db_interface.TABLE_ALERT2ALERT, 0)
        self._check_rows(db_interface.TABLE_CHECKPOINT, 1)
        self.cnxn.close()
        teal.shutdown()
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()