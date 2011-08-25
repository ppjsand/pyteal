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
from datetime import datetime

from ibm import teal
from ibm.teal.registry import get_logger
from ibm.teal.incident import Incident


class SampleIncident1(Incident):
    '''Subclass of Incident to ease testing of 
        Incident Pools
        
        Instead of forwarding to a contained Event or Alert
        allow the data to be passed by constructor
    '''  
          
    def __init__(self, rec_id, incident_id, time_occurred=None):
        '''Constructor
        
        uuid -- unique id
        name -- name this is referred to by
        type --
        '''
        get_logger().debug('Creating Incident')
        self.rec_id = rec_id
        self.incident_id = incident_id
        if time_occurred is None:
            self.time_occurred = datetime.now()
        else:
            self.time_occurred = time_occurred
        Incident.__init__(self)
        return
        
    def get_type(self):
        return 'T'
    
    def get_rec_id(self):
        return self.rec_id
    
    def get_incident_id(self):
        return self.incident_id
    
    def get_time_occurred(self):
        return self.time_occurred
    
    def get_time_logged(self):
        return self.time_occurred
    
    def get_analysis_info(self, info_source):
        return
    
    def read_from_dictionary(self):
        return
    
    def write_to_dictionary(self):
        return
    
    def process(self):
        return
    
    def get_metadata(self):
        return

    
class TestIncidentsBasic(unittest.TestCase):
    
    def setUp(self):
        if get_logger() is None: 
            teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        return
    
    def testCreate1(self):
        '''Test that basic creation works
        '''
        now = datetime.now()
        i1 = SampleIncident1('1','Ia')   
        self.assertEqual(i1.get_rec_id(), '1') 
        self.assertEqual(i1.get_incident_id(), 'Ia')
        self.assertEqual(i1.get_type(), 'T')
        self.assertEqual((i1.get_time_occurred()-now).seconds, 0)
#        print 'test that print works'
#        print str(i1)
#        print repr(i1)
        return
    
    def testCreate2(self):
        '''Test that basic creation works with time
        '''
        now = datetime.now()
        i1 = SampleIncident1('1','Ia', now)   
        self.assertEqual(i1.get_rec_id(), '1') 
        self.assertEqual(i1.get_incident_id(), 'Ia')
        self.assertEqual(i1.get_type(), 'T')
        self.assertEqual((i1.get_time_occurred()-now).seconds, 0)
        return
                  

if __name__ == "__main__":
    unittest.main()