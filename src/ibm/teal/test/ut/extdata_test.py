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
import unittest
import struct

from ibm.teal.teal import Teal
from ibm.teal.extdata import ExtensionData, extdata_fmt2table_name
from ibm.teal.location import Location
from ibm.teal.database import db_interface  
from ibm.teal.test.teal_unittest import TealTestCase

class ExtensionDataTest(TealTestCase):

    def setUp(self):
        self.teal = Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)

    def tearDown(self):
        self.teal.shutdown()

    def testInvalidFormat(self):
        ''' Test invalid format handled '''
        raw_data = 'This is raw data'
        fmt = 0x4142434400000000
        self.assertRaises(IOError, ExtensionData, fmt, None, raw_data)
         
    def testInvalidTable(self):
        ''' Test invalid table handled '''
        raw_data = 'This is raw data'
        fmt = 0x5445535400001234
        self.assertRaises(ValueError, ExtensionData, fmt, None, raw_data)
    
    def testTableName(self):
        ''' Test table name generation '''
        # This is to circumvent the need to start up TEAL to set the variable
        db_interface.TABLE_TEMPLATE = 'x_{0}'
        # Tests
        fmt_raw_data = 0x5445535400001234
        fmt_db_data1 = 0x5445535480001234
        fmt_db_data2 = 0x5445535480F812AB
        self.assertFalse(extdata_fmt2table_name(fmt_raw_data))
        self.assertEqual(extdata_fmt2table_name(fmt_db_data1),'x_TEST_0_1234')
        self.assertEqual(extdata_fmt2table_name(fmt_db_data2),'x_TEST_F8_12AB')
        
    def testRawDataOnly(self):
        ''' Test raw data only '''
        raw_data = 'This is raw data'
        ed = ExtensionData(0, None, raw_data)
        
        self.assertEqual(raw_data, ed['raw_data'])
        self.assertEqual(len(ed.keys()), 1)
        self.assertEqual(0, ed.get_format())
    
    def testString(self):
        ''' Test string data ''' 
        raw_data = "0123456789ABCDEFGH"
        fmt = 0x5445535400000001
        ed = ExtensionData(fmt,None, raw_data)
        
        self.assertEqual(raw_data, ed['raw_data'])
        self.assertEqual(raw_data, ed['info'])
        self.assertEqual(len(ed.keys()), 2)
        self.assertEqual(fmt, ed.get_format())

    def testNumbers(self):   
        ''' Test numbers are handled correctly '''     
        s = struct.Struct("i")
        fmt = 0x5445535400000004
        raw_data = s.pack(0x12345678)        
        ed = ExtensionData(fmt, None, raw_data)
        #print hex(ed['number'])
        self.assertEqual(0x12345678,ed['number'])
                
        s = struct.Struct("q")
        fmt = 0x5445535400000005
        raw_data = s.pack(0x123456789ABCDEF0)        
        ed = ExtensionData(fmt,None, raw_data)
        #print hex(ed['number'])
        self.assertEqual(0x123456789ABCDEF0,ed['number'])
                
    def testLocation(self):
        ''' Test location is handled correctly '''
        s = struct.Struct("3p256p")
        fmt = 0x5445535400000003
        loc = Location('C','MB-SL3-ET1-PT2')
        
        raw_data = s.pack(loc.get_id(),loc.get_location())        
        ed = ExtensionData(fmt,None, raw_data)
        
        self.assertEqual(raw_data,ed['raw_data'])
        self.assertEqual(loc,ed['neighbor'])
        self.assertEqual(len(ed.keys()),2)
        self.assertEqual(fmt,ed.get_format())
        
    def testToFromDict(self):
        ''' Test to and from dict is handled correctly '''
        s = struct.Struct("3p256p")
        fmt = 0x5445535400000003
        loc = Location('C','MB-SL3-ET1-PT2')
        
        raw_data = s.pack(loc.get_id(),loc.get_location())        
        ed = ExtensionData(fmt,None, raw_data)
        
        self.assertEqual(raw_data,ed['raw_data'])
        self.assertEqual(loc,ed['neighbor'])
        self.assertEqual(len(ed.keys()),2)
        self.assertEqual(fmt,ed.get_format())
        tmp_dict = ed.write_to_dictionary()
        new_ed = ExtensionData(fmt, None, None, tmp_dict)
        self.assertEqual(raw_data, new_ed['raw_data'])
        self.assertEqual(loc, new_ed['neighbor'])
        self.assertEqual(len(new_ed.keys()), 2)
        self.assertEqual(fmt, new_ed.get_format())
        return
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocation']
    unittest.main()
