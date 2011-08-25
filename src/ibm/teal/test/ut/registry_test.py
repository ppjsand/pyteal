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

from ibm.teal import Teal
from ibm.teal import registry
from ibm.teal.registry import DuplicateKeyError, SERVICE_SHUTDOWN

SERVICE_REGISTRY_TEST ='registry_test'

class RegistryTest(unittest.TestCase):
    
        
    def setUp(self):
        Teal('data/common/configurationtest.conf', 'stderr' , msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
    
    def tearDown(self):
        registry.get_service(SERVICE_SHUTDOWN).shutdown()
        
    def testRegisterService(self):
        ''' Test register_service successful'''
        self.assertTrue(SERVICE_REGISTRY_TEST not in registry.registry)
        registry.register_service(SERVICE_REGISTRY_TEST, self)
        self.assertEquals(registry.registry[SERVICE_REGISTRY_TEST], self)
        del registry.registry[SERVICE_REGISTRY_TEST]
        
    def testUnregisterService(self):
        ''' Test unregister_service successful'''
        self.assertTrue(SERVICE_REGISTRY_TEST not in registry.registry)
        registry.register_service(SERVICE_REGISTRY_TEST, self)
        registry.unregister_service(SERVICE_REGISTRY_TEST)
        self.assertTrue(SERVICE_REGISTRY_TEST not in registry.registry)
            
    def testGetService(self):
        ''' Test get_service successful'''
        self.assertTrue(SERVICE_REGISTRY_TEST not in registry.registry)
        registry.register_service(SERVICE_REGISTRY_TEST, self)
        self.assertEquals(registry.get_service(SERVICE_REGISTRY_TEST), self)
        registry.unregister_service(SERVICE_REGISTRY_TEST)
        
    def testRegisterDuplicateService(self):
        ''' Test a service cannot be overridden'''
        registry.register_service(SERVICE_REGISTRY_TEST, self)
        self.assertRaises(ValueError, registry.register_service, SERVICE_REGISTRY_TEST, self)
        self.assertRaises(DuplicateKeyError, registry.register_service, SERVICE_REGISTRY_TEST, self)
        registry.unregister_service(SERVICE_REGISTRY_TEST)

if __name__ == '__main__':
    unittest.main()
