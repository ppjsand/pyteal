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

from ibm.teal.util.xml_file_reader import read_xml_file


class Test(unittest.TestCase):

    def testReadNoXMLFile(self):
        ''' Read with no file specified '''
        root, trace_dict = read_xml_file('')
        self.assertEquals(root, None)
        self.assertEquals(len(trace_dict), 0)
        return

    def testReadXMLFile001(self):
        ''' Read an xml file and make sure get right results '''
        root, trace_dict = read_xml_file('data/demo/GEAR_rule_example_001.xml')
        self.assertNotEquals(root, None)
        self.assertNotEquals(len(trace_dict), 0)
        self.assertEquals(len(trace_dict), 30)
        self.assertEquals(trace_dict[root],(4,'1'))
        
        return

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()