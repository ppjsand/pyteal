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
 
from ibm.teal.test.teal_unittest import TealTestCase, unittest
from datetime import datetime

from ibm import teal
from ibm.teal.registry import get_logger, register_service, SERVICE_EVENT_METADATA, unregister_service, \
         get_service, SERVICE_ALERT_METADATA
from ibm.teal.metadata import Metadata, META_TYPE_EVENT, META_EVENT_ID, META_EVENT_COMP, META_EVENT_MSG, \
         META_TYPE_ALERT,       \
         META_ALERT_ID, META_ALERT_MSG_TEMPLATE, META_ALERT_RECOMMENDATION, META_ALERT_URGENCY, \
         META_ALERT_SEVERITY, META_ALERT_CALL_HOME, META_ALERT_CUST_NOTIFICATION, META_ALERT_FRU_CLASS, \
         META_ALERT_FRU_LIST, META_EVENT_DESCRIPTION, META_ALERT_DESCRIPTION,\
    META_ALERT_PRIORITY
         
from ibm.teal.event import Event, EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID,\
    EVENT_ATTR_SRC_COMP, EVENT_ATTR_TIME_OCCURRED
from ibm.teal.teal_error import XMLParsingError, ConfigurationError

class EventMetadataTest(TealTestCase):

    def setUp(self):
        '''Setup TEAL if needed
        '''
        self.teal = teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel=self.msglevel, data_only=True, commit_alerts=False, commit_checkpoints=False)

    def tearDown(self):
        '''Not currently used
        '''
        self.teal.shutdown()

    def testBasicNoFiles(self):
        '''Test if no files are specified
        '''
        esm1 = Metadata(META_TYPE_EVENT,[])
        self.assertEqual(len(esm1), 0)
        return

    def testBasicOneEntry(self):
        '''Test that can parse a simple correct event XML file
        '''
        esm1 = Metadata(META_TYPE_EVENT, ['metadata_test/event_metadata_01.xml'])
        event_id = 'idvalue0'
        comp_id = "TST"
        self.assertEqual(len(esm1), 1)
        self.assertTrue((comp_id, event_id) in esm1)
        meta_dict = esm1[(comp_id, event_id)]
        self.assertEqual(meta_dict[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict[META_EVENT_COMP], comp_id)
        self.assertEqual(meta_dict[META_EVENT_MSG], 'This is test message 0')
        self.assertEqual(meta_dict[META_EVENT_DESCRIPTION], 'This is a description')
        return
    
    def testBasicOneErrorMissingComp(self):
        '''Test that not specifying the component causes exception
        '''
        self.assertRaises(XMLParsingError, Metadata, META_TYPE_EVENT, ['metadata_test/event_metadata_02_error.xml'])
        return
    
    def testBasicOneErrorReq1(self):
        '''Test that not specifying the message causes exception
        '''
        self.assertRaises(XMLParsingError, Metadata, META_TYPE_EVENT, ['metadata_test/event_metadata_03_error.xml'])
        return
    
    def testBasicOneErrorWrongElem(self):
        '''Test that specifying the wrong element causes exception
        '''
        self.assertRaises(XMLParsingError, Metadata, META_TYPE_EVENT, ['metadata_test/event_metadata_04_error.xml'])
        return
    
    def testBasicTwoEntry(self):
        '''Test that can parse a simple correct XML file with two entries
        '''
        esm1 = Metadata(META_TYPE_EVENT, ['metadata_test/event_metadata_05.xml'])
        event_id = 'idvalue0'
        event_comp = 'TST'
        self.assertEqual(len(esm1), 2)
        self.assertTrue((event_comp, event_id) in esm1)
        meta_dict = esm1[(event_comp, event_id)]
        self.assertEqual(meta_dict[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict[META_EVENT_COMP], event_comp)
        self.assertEqual(meta_dict[META_EVENT_MSG], 'This is test message 0')
        event_id = 'idvalue1'
        meta_dict2 = esm1[(event_comp, event_id)]
        self.assertEqual(meta_dict2[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict[META_EVENT_COMP], event_comp)        
        self.assertEqual(meta_dict2[META_EVENT_MSG], 'This is test message 1')
        self.assertEqual(meta_dict2[META_EVENT_DESCRIPTION], None)
        return
    
    def testGetViaEvent(self):
        '''Test getting via an event'''
        esm1 = Metadata(META_TYPE_EVENT, ['metadata_test/event_metadata_05.xml'])
        unregister_service(SERVICE_EVENT_METADATA)
        register_service(SERVICE_EVENT_METADATA, esm1)
        event_id = 'idvalue1'
        event_comp = 'TST'
        e1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                           EVENT_ATTR_EVENT_ID:event_id, 
                           EVENT_ATTR_SRC_COMP: 'TST', 
                           EVENT_ATTR_TIME_OCCURRED: datetime.now()})  
        meta_dict2 = e1.get_metadata()
        self.assertEqual(meta_dict2[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict2[META_EVENT_COMP], event_comp)
        self.assertEqual(meta_dict2[META_EVENT_MSG], 'This is test message 1')
        return
    
    def testBadType(self):
        '''Test bad metadata type'''
        self.assertRaises(ConfigurationError, Metadata, 'Frobbles', ['metadata_test/event_metadata_04_error.xml'])
        return

    def testEventDataForAlert(self):
        '''Test giving an Alert metadata Event data'''
        self.assertRaises(XMLParsingError, Metadata, META_TYPE_ALERT, ['metadata_test/event_metadata_04_error.xml'])
        return
 
    def testSameFileTwice(self):
        '''Test that can parse a simple correct XML file twice 
        '''
        # Yes, next line should have same file twice
        esm1 = Metadata(META_TYPE_EVENT, ['metadata_test/event_metadata_01.xml', 'metadata_test/event_metadata_01.xml' ])
        event_id = 'idvalue0'
        event_comp = 'TST'
        self.assertEqual(len(esm1), 1)
        self.assertTrue((event_comp, event_id) in esm1)
        meta_dict = esm1[(event_comp, event_id)]
        self.assertEqual(meta_dict[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict[META_EVENT_COMP], event_comp)
        self.assertEqual(meta_dict[META_EVENT_MSG], 'This is test message 0')
        return

    def testBasicOneAlert(self):
        '''Test that can parse a simple correct Alert XML file
        '''
        asm1 = Metadata(META_TYPE_ALERT, ['metadata_test/alert_metadata_01.xml'])
        alert_id = 'Alert01'
        self.assertEqual(len(asm1), 1)
        self.assertTrue(alert_id in asm1)
        meta_dict = asm1[alert_id]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 01')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'W')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], 'fru_class')
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], 'fru_list1, fru_list2')
        self.assertEqual(meta_dict[META_ALERT_DESCRIPTION], 'This is a description')
        self.assertEqual(meta_dict[META_ALERT_PRIORITY], None)
        return
    
    def testBasicTwoAlert(self):
        '''Test that can parse a simple correct Alert XML file with two elements
        '''
        asm1 = Metadata(META_TYPE_ALERT, ['metadata_test/alert_metadata_02.xml'])
        alert_id = 'Alert01'
        self.assertEqual(len(asm1), 2)
        self.assertTrue(alert_id in asm1)
        meta_dict = asm1[alert_id]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 01')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'W')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], 'fru_class')
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], 'fru_list1, fru_list2')
        self.assertEqual(meta_dict[META_ALERT_DESCRIPTION], None)
        self.assertEqual(meta_dict[META_ALERT_PRIORITY], None)
        alert_id2 = 'Alert02'
        self.assertTrue(alert_id2 in asm1)
        meta_dict = asm1[alert_id2]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id2)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 02')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something else')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'S')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        self.assertEqual(meta_dict[META_ALERT_PRIORITY], None)
        return
    
    def testBasicCNMAlert(self):
        '''Test that can parse a CNM example alert metadata file
        '''
#        asm1 = 
        Metadata(META_TYPE_ALERT, ['cnm/cnm.NMalertMetaData.xml'])
#        keys = asm1.keys()
#        keys.sort()
#        for key in keys:
#            print asm1[key]
        return

    def testBasicThreeAlert(self):
        '''Test that can parse a simple correct Alert XML file with three elements
        '''
        asm1 = Metadata(META_TYPE_ALERT, ['metadata_test/alert_metadata_03.xml'])
        alert_id = 'Alert01'
        self.assertEqual(len(asm1), 3)
        self.assertTrue(alert_id in asm1)
        meta_dict = asm1[alert_id]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 01')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'W')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], 'fru_class')
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], 'fru_list1, fru_list2')
        self.assertEqual(meta_dict[META_ALERT_PRIORITY], None)
        alert_id2 = 'Alert02'
        self.assertTrue(alert_id2 in asm1)
        meta_dict = asm1[alert_id2]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id2)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 02')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something else')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'S')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        self.assertEqual(meta_dict[META_ALERT_PRIORITY], 2)
        alert_id3 = 'Alert03'
        self.assertTrue(alert_id3 in asm1)
        meta_dict = asm1[alert_id3]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id3)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 03')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Do not do anything')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'Y')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        self.assertEqual(meta_dict[META_ALERT_PRIORITY], None)
        return
    
    
class EventMetadataTestConf(TealTestCase):

    def setUp(self):
        '''Setup TEAL if needed
        '''
        return

    def tearDown(self):
        '''Not currently used'''
        return

    def testLoadingFromConNone(self):
        '''Test if no files are specified in the config file
        '''
        teal_inst = teal.Teal('data/metadata_test/load_config_01.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        esm1 = get_service(SERVICE_EVENT_METADATA)
        self.assertEqual(len(esm1), 0)
        asm1 = get_service(SERVICE_ALERT_METADATA)
        self.assertEqual(len(asm1), 0)
        teal_inst.shutdown()
        return
    
    def testLoadingFromConOne(self):
        '''Test if one files for each are specified in the config file in one section
        '''
        teal_inst = teal.Teal('data/metadata_test/load_config_02.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        # it loaded event_metadata_05 and alert_metadata_03
        # Check event metadata via event
        esm1 = get_service(SERVICE_EVENT_METADATA)
        self.assertEqual(len(esm1), 2)
        event_id = 'idvalue1'
        event_comp = 'TST'
        e1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                           EVENT_ATTR_EVENT_ID:event_id, 
                           EVENT_ATTR_SRC_COMP: 'TST', 
                           EVENT_ATTR_TIME_OCCURRED: datetime.now()})  
        meta_dict2 = e1.get_metadata()
        self.assertEqual(meta_dict2[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict2[META_EVENT_COMP], event_comp)
        self.assertEqual(meta_dict2[META_EVENT_MSG], 'This is test message 1')
        # check alert metadata directly
        asm1 = get_service(SERVICE_ALERT_METADATA)
        alert_id = 'Alert01'
        self.assertEqual(len(asm1), 3)
        self.assertTrue(alert_id in asm1)
        meta_dict = asm1[alert_id]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 01')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'W')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], 'fru_class')
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], 'fru_list1, fru_list2')
        alert_id2 = 'Alert02'
        self.assertTrue(alert_id2 in asm1)
        meta_dict = asm1[alert_id2]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id2)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 02')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something else')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'S')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        alert_id3 = 'Alert03'
        self.assertTrue(alert_id3 in asm1)
        meta_dict = asm1[alert_id3]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id3)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 03')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Do not do anything')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'Y')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        teal_inst.shutdown()
        return
    
    def testLoadingFromConTwo(self):
        '''Test if one files for each are specified in the config file in two sections
        '''
        teal_inst = teal.Teal('data/metadata_test/load_config_03.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        # it loaded event_metadata_05 and alert_metadata_03
        # Check event metadata via event
        esm1 = get_service(SERVICE_EVENT_METADATA)
        self.assertEqual(len(esm1), 2)
        event_id = 'idvalue1'
        event_comp = 'TST'
        e1 = teal.Event.fromDict({EVENT_ATTR_REC_ID:1, 
                           EVENT_ATTR_EVENT_ID:event_id, 
                           EVENT_ATTR_SRC_COMP: 'TST', 
                           EVENT_ATTR_TIME_OCCURRED: datetime.now()})  
        meta_dict2 = e1.get_metadata()
        self.assertEqual(meta_dict2[META_EVENT_ID], event_id)
        self.assertEqual(meta_dict2[META_EVENT_COMP], event_comp)
        self.assertEqual(meta_dict2[META_EVENT_MSG], 'This is test message 1')
        # check alert metadata directly
        asm1 = get_service(SERVICE_ALERT_METADATA)
        alert_id = 'Alert01'
        self.assertEqual(len(asm1), 3)
        self.assertTrue(alert_id in asm1)
        meta_dict = asm1[alert_id]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 01')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'W')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], 'fru_class')
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], 'fru_list1, fru_list2')
        alert_id2 = 'Alert02'
        self.assertTrue(alert_id2 in asm1)
        meta_dict = asm1[alert_id2]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id2)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 02')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Recommend doing something else')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'S')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'N')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        alert_id3 = 'Alert03'
        self.assertTrue(alert_id3 in asm1)
        meta_dict = asm1[alert_id3]
        self.assertEqual(meta_dict[META_ALERT_ID], alert_id3)
        self.assertEqual(meta_dict[META_ALERT_MSG_TEMPLATE], 'This is Alert 03')
        self.assertEqual(meta_dict[META_ALERT_RECOMMENDATION], 'Do not do anything')
        self.assertEqual(meta_dict[META_ALERT_URGENCY], 'N')
        self.assertEqual(meta_dict[META_ALERT_SEVERITY], 'E')
        self.assertEqual(meta_dict[META_ALERT_CALL_HOME], 'Y')
        self.assertEqual(meta_dict[META_ALERT_CUST_NOTIFICATION], 'N')
        self.assertEqual(meta_dict[META_ALERT_FRU_CLASS], None)
        self.assertEqual(meta_dict[META_ALERT_FRU_LIST], None)
        teal_inst.shutdown()
        return


if __name__ == "__main__":
    unittest.main()