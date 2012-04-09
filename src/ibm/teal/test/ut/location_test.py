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
import sys
from exceptions import ValueError

from ibm.teal import Teal
from ibm.teal.location import Location

from ibm.teal import registry
from ibm.teal.registry import SERVICE_LOCATION
from ibm.teal.test.teal_unittest import TealTestCase

class LocationTest(TealTestCase):

    def setUp(self):
        self.teal = Teal('data/location_test/locationtest_01.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
                
    def tearDown(self):
        self.teal.shutdown()
        
    def testSimpleGood(self):
        ''' Test good path simple locations '''
        simple1 = Location('TS','a')
        self.assertEqual(simple1.get_location(),'a')
            
        simple2 = Location('TS','a.b')
        self.assertEqual(simple2.get_location(),'a.b')
        
        simple3 = Location('TS','a.b.c')
        self.assertEqual(simple3.get_location(),'a.b.c')
    
    def testComplexGood(self):
        ''' Test good path complex locations '''
        # Minimum tree specified
        complex1 = Location('TC',"R")
        self.assertEqual(complex1.get_location(),'R')
        
        complex2 = Location('TC',"R-H")
        self.assertEqual(complex2.get_location(),'R-H')
        
        # No value allowed
        complex3 = Location('TC',"R-H-JC")
        self.assertEqual(complex3.get_location(),'R-H-JC')

        # min-only specified
        complex4 = Location('TC',"R-H-MM12345")
        self.assertEqual(complex4.get_location(),'R-H-MM12345')
        
        complex4a = Location('TC',"R-H-MM"+str(sys.maxint))
        self.assertEqual(complex4a.get_location(),'R-H-MM'+str(sys.maxint))
        
        # Range specified
        complex5 = Location('TC',"R-H-PS9")
        self.assertEqual(complex5.get_location(),'R-H-PS9')
        
        # max-only specified
        complex6 = Location('TC',"R-H-K0")
        self.assertEqual(complex6.get_location(),'R-H-K0')
        
        # Full tree specified
        complex7 = Location('TC',"R-H-K20-S")
        self.assertEqual(complex7.get_location(),'R-H-K20-S')
        
    def testComplexBad(self):
        ''' Test invalid complex locations '''
        keep_env = self.force_env('TEAL_LOCATION_VALIDATION', 'IMMEDIATE')
        self.assertRaises(KeyError, Location, 'TZ',"R-H")            # Invalid Type of Location
        self.assertRaises(TypeError, Location, 'TC',["R","H"])       # Create with something that is not a string
        self.assertRaises(ValueError, Location, 'TC',"R01")          # No value allowed
        self.assertRaises(ValueError, Location, 'TC',"R-H02")        # No value allowed child
        self.assertRaises(ValueError, Location, 'TC',"R-H-JC10")     # No value allowed leaf
        self.assertRaises(ValueError, Location, 'TC',"R-H-PS")       # No value specified but required             ) 
        self.assertRaises(ValueError, Location, 'TC',"R-H-PS0")      # Below specified min value (min/max specified) 
        self.assertRaises(ValueError, Location, 'TC',"R-H-PS11")     # Above specified max value (min/max specified)
        self.assertRaises(ValueError, Location, 'TC',"R-H-MM4")      # Below specified min value (min-only specified)
        self.assertRaises(ValueError, Location, 'TC',"R-H-K21")      # Above specified max value (max-only specified)
        self.assertRaises(ValueError, Location, 'TC',"R-H-K20-S12")  # No value allowed on leaf after multi-node component      
        self.assertRaises(ValueError, Location, 'TC',"R-H-K20-S-Z")  # Too many components      
        self.assertRaises(ValueError, Location, 'TC',"R-H-X-S")      # Unknown component      
        self.assertRaises(ValueError, Location, 'TC',"R-xH-X-S")     # Bad front end
        self.assertRaises(ValueError, Location, 'TC',"R-Hx1-X-S")    # Bad back end 
        self.restore_env('TEAL_LOCATION_VALIDATION', keep_env)     
        return  
    
    def testComplexBadDefered(self): 
        ''' Test invalid complex locations with validation deferred '''
        cbad1 = Location('TZ', 'R-H')   
        self.assertEqual('TZ: R-H', str(cbad1)) 
        self.assertRaises(KeyError, cbad1.get_substitution_dict)
        self.assertRaises(KeyError, cbad1.get_comp_value, 'dummy')
        self.assertRaises(KeyError, cbad1.new_location_by_scope, 'dummy')
        self.assertEqual('TZ', cbad1.get_id())
        self.assertEqual('R-H', cbad1.get_location())
        cbad2 = Location('TZ', 'R-H')
        cbad3 = Location('TZ', 'R-I')
        self.assertTrue(cbad1 == cbad2)
        self.assertFalse(cbad1 == cbad3)
        self.assertTrue(cbad1.match(cbad2, None))
        self.assertRaises(KeyError, cbad1.match, cbad2, 'dummy')
        return

    def testSimpleMatch(self):
        simple1 = Location('TS','a.b.c')
        simple2 = Location('TS','a.b.z')
        simple3 = Location('TS','x.y.z')
        
        self.assertTrue(simple1.match(simple1))
        
        self.assertFalse(simple1.match(simple2))
        self.assertTrue(simple1.match(simple2,'child'))
        self.assertTrue(simple1.match(simple2,'parent'))

        self.assertFalse(simple1.match(simple3))
        self.assertFalse(simple1.match(simple3,'child'))
        self.assertFalse(simple1.match(simple3,'parent'))

    def testComplexMatch(self):
        ''' Test matching scopes with complex locations '''
        complex1 = Location('TC',"R-H-PS9")
        complex2 = Location('TC',"R-H-K8-S")
        complex3 = Location('TC',"R-H-K9-S")
        
        self.assertTrue(complex1.match(complex1))
        
        self.assertTrue(complex1.match(complex1))
        self.assertFalse(complex1.match(complex2))
        self.assertTrue(complex1.match(complex2,'home'))
        self.assertTrue(complex1.match(complex2,'top'))

        self.assertFalse(complex2.match(complex3))
        
        # Can do different length w/o problems
        complex2 = Location('TC','R-H')
        complex3 = Location('TC','R-H-K9-S')
        self.assertFalse(complex2.match(complex3,'kilroy'))
        self.assertFalse(complex3.match(complex2,'kilroy'))

        
    def testComplexMatchBad(self):
        ''' Test matching scopes with complex locations and errors '''
        simple1 = Location('TS','a.b.c')
        simple2 = Location('TS','a.b.z')
        complex1 = Location('TC',"R-H-PS9")
        
        # Can't mix location types
        self.assertFalse(simple1.match(complex1)) 
                        
        # Can't use an invalid location component
        self.assertRaises(KeyError, simple1.match, simple2,'mom')        
    
    def testSimpleComponentValues(self):
        ''' Test getting the value of a component for simple locations '''
        simple1 = Location('TS','a.b.c')
        self.assertEquals(simple1.get_comp_value('grandchild'),'c')
        self.assertEquals(simple1.get_comp_value('child'),'b')
        self.assertEquals(simple1.get_comp_value('parent'),'a')

    def testComplexComponentValues(self):
        ''' Test getting the value of a component for complex locations '''
        complex1 = Location('TC',"R-H-K8-S")
        self.assertEquals(complex1.get_comp_value('kilroy'),'8')
    
    def testComplexComponentValuesBad(self):
        ''' Test getting the value of a component for complex locations '''
        complex1 = Location('TC',"R-H-K8-S")
        self.assertRaises(ValueError, complex1.get_comp_value, 'home')
        self.assertRaises(ValueError, complex1.get_comp_value, 'jecarey')
    
    def testNewLocationByScope(self):
        ''' Test creating a new location with a given scope '''
        complex1 = Location('TC',"R-H-K8-S")
        complex2 = complex1.new_location_by_scope('kilroy')
        self.assertEquals(complex2,Location('TC','R-H-K8'))

        complex3 = complex1.new_location_by_scope('home')
        complex4 = complex2.new_location_by_scope('home')
        self.assertEquals(complex3,complex4)
    
        self.assertRaises(KeyError, complex1.new_location_by_scope, 'bad')
    
        # Scoping lower than the id will just return the id
        complex5 = complex3.new_location_by_scope('kilroy')
        self.assertEquals(complex3,complex5)
    
    def testMisc(self):
        ''' Test miscellaneous Location capabilities '''
        l1 = Location("TS",'foo')
        l2 = Location("TC",'R-H-K8-S')
        
        self.assertNotEqual(hash(l1),hash(l2))
        self.assertEquals(hash(l1),hash(l1))

        self.assertEqual(l1.get_id(),'TS')
        self.assertEqual(l2.get_id(),'TC')
        
    def testLocationService(self): 
        ''' Test Location Service public functions '''       
        loc_svc = registry.get_service(SERVICE_LOCATION)
        self.assertTrue(loc_svc.is_scope_valid('TC','kilroy'))
        self.assertFalse(loc_svc.is_scope_valid('TC','archerc'))
        
    def testSubstitutionDict(self):
        ''' Test getting the substitution dictionary '''
        l1 = Location("TS",'foo')
        sd1 = l1.get_substitution_dict()
        self.assertEquals(len(sd1.keys()), 1)
        self.assertTrue('parent' in sd1)
        self.assertEquals(sd1['parent'], 'foo')
        l2 = Location("TC",'R-H-K8-S')
        sd2 = l2.get_substitution_dict()
        self.assertEquals(len(sd2.keys()), 4)
        self.assertTrue('kilroy' in sd2)
        self.assertEquals(sd2['kilroy'], 'K8')
        self.assertTrue('src' in sd2)
        self.assertEquals(sd2['src'], 'S')
        self.assertTrue('top' in sd2)
        self.assertEquals(sd2['top'], 'R')
        self.assertTrue('home' in sd2)
        self.assertEquals(sd2['home'], 'H')
        return


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()