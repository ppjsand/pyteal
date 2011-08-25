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

from ibm.teal.registry import get_service, SERVICE_ALERT_METADATA

from ibm.teal.test.teal_unittest import TealTestCase, unittest

from ibm.teal import teal
from ibm.teal.analyzer.gear.ruleset import GearRuleset
from ibm.teal.teal_error import XMLParsingError
from ibm.teal.analyzer.gear.rule_value import _contains_gear_variable,\
    _parse_gear_variable


#class GearRulesetTest(TealTestCase):
#    '''Test loading GEAR rulesets'''
#
#    def setUp(self):
#        self.teal = teal.Teal('data/gear_ruleset_test/gear_ruleset_test.conf', 'stderr', msgLevel='debug', commit_alerts=False)
#        return
#
#    def tearDown(self):
#        self.teal.shutdown()
#        return
#
#    def testGearAnalyzeMissing(self):
#        ''' Test fails when analyze not specified '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_analyze_001_err.xml' )
#        return
#    
#    def testGearAnalyzeEmpty(self):
#        ''' Test fails when analyze has no subelements '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_analyze_002_err.xml' )
#        return
#
#    def testGearControlEmpty(self):
#        ''' Test get expected results when GEAR Control is empty'''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_control_001.xml',None, True)
##        self.assertEqual(grs1['gear_control'].use_alert_regx, False)
#        self.assertEqual(grs1['gear_control'].use_event_regx, False)
#        self.assertEqual(grs1['gear_control']['default_event_comp'], None)
#        self.assertEqual(grs1.get_default_event_component(), None)
#        self.assertEqual(grs1.description,'This is a description')
#        return
#        
#    def testGearControlDefaultComp(self):
#        ''' Test specification of a default component '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_control_002.xml',None, True)
##        self.assertEqual(grs1['gear_control'].use_alert_regx, False)
#        self.assertEqual(grs1['gear_control'].use_event_regx, False)
#        self.assertEqual(grs1['gear_control']['default_event_comp'], 'TC')
#        return
#    
#    def testGearControlValidIgnored(self):
#        ''' Test that the will_analyze can specify the default and work'''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_control_003.xml',None, True)
##        self.assertEqual(grs1['gear_control'].use_alert_regx, False)
#        self.assertEqual(grs1['gear_control'].use_event_regx, False)
#        self.assertEqual(grs1['gear_control']['default_event_comp'], 'TC')
#        self.assertEqual(grs1.get_default_event_component(), 'TC')
#        return
#       
#    def testGearControlSpecifyEvents(self):
#        ''' Test events being specified '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_control_004.xml',None, True)
##        self.assertEqual(grs1['gear_control'].use_alert_regx, False)
#        self.assertEqual(grs1['gear_control'].use_event_regx, True)
#        self.assertEqual(grs1['gear_control'].event_comp_regx_string,'[A|B]')
#        self.assertEqual(grs1['gear_control'].event_id_regx_string,'.*')
#        self.assertEqual(grs1['gear_control']['default_event_comp'], 'B')
#        return
#    
#    def testGearControlSpecifyBadAttributes(self):
#        ''' Specify incompatible attributes on will_analyze'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_control_005.xml')
#        return
#      
#    def testGearControlSpecifyAlerts(self):
#        ''' Test alerts being specified '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_control_006.xml',None, True)
##        self.assertEqual(grs1['gear_control'].use_alert_regx, True)
#        self.assertEqual(grs1['gear_control'].use_event_regx, True)
##        self.assertEqual(grs1['gear_control'].alert_id_regx_string, '  Z  ,   B,Q')
#        self.assertEqual(grs1['gear_control']['default_event_comp'], 'TC')
#        return
#    
#    def testGearControlNoCompSpecfied(self):
#        '''Test that if no comp is specified and rules do not specify it fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_control_007_err.xml')
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_control_008_err.xml')
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_control_009_err.xml')
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_control_010_err.xml')
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_control_011_err.xml')
#        return
#    
#    def testGearEvents001(self):
#        '''Test that the events info is correctly handled'''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_events_001.xml',None, True)
#        self.assertEqual(len(grs1['events'].event_info), 3)
#        print grs1['events'].event_info
#        self.assertTrue(('TC2','Example1') in grs1['events'].event_info)
#        self.assertTrue(('TC','Example2') in grs1['events'].event_info)
#        self.assertTrue(('PS','Example5') in grs1['events'].event_info)
#        self.assertEqual(len(grs1['events'].event_info[('TC2','Example1')]), 5)
#        self.assertEqual(grs1['events'].event_info[('TC2','Example1')]['id'], 'Example1')
#        self.assertEqual(grs1['events'].event_info[('TC2','Example1')]['name'], None)
#        self.assertEqual(grs1['events'].event_info[('TC2','Example1')]['min_time_in_pool'], 5)
#        self.assertEqual(grs1['events'].event_info[('TC2','Example1')]['pool_extension_time'], 3)
#        self.assertEqual(grs1['events'].event_info[('TC2','Example1')]['comp'], 'TC2')
#        self.assertEqual(len(grs1['events'].event_info[('TC','Example2')]), 5)
#        self.assertEqual(grs1['events'].event_info[('TC','Example2')]['id'], 'Example2')
#        self.assertEqual(grs1['events'].event_info[('TC','Example2')]['name'], None)
#        self.assertEqual(grs1['events'].event_info[('TC','Example2')]['min_time_in_pool'], 0)
#        self.assertEqual(grs1['events'].event_info[('TC','Example2')]['pool_extension_time'], 0)
#        self.assertEqual(grs1['events'].event_info[('TC','Example2')]['comp'], 'TC')
#        self.assertEqual(len(grs1['events'].event_info[('PS','Example5')]), 5)
#        self.assertEqual(grs1['events'].event_info[('PS','Example5')]['id'], 'Example5')
#        self.assertEqual(grs1['events'].event_info[('PS','Example5')]['name'], 'REFNAME')
#        self.assertEqual(grs1['events'].event_info[('PS','Example5')]['min_time_in_pool'], 0)
#        self.assertEqual(grs1['events'].event_info[('PS','Example5')]['pool_extension_time'], 0)
#        self.assertEqual(grs1['events'].event_info[('PS','Example5')]['comp'], 'PS')
#        return
#    
#    def testGearEvents002(self):
#        ''' Test that the bad rules files cause failures '''
#        self.assertRaisesTealError(XMLParsingError, 'Event id Example2 name must be at least 1 character', GearRuleset, 'data/gear_ruleset_test/gear_events_002_err.xml',None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Event id  must be at least 1 character', GearRuleset, 'data/gear_ruleset_test/gear_events_003_err.xml',None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Event id 123456789 is longer than 8 characters', GearRuleset, 'data/gear_ruleset_test/gear_events_004_err.xml',None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Event id Example1 pool extension time must be positive', GearRuleset, 'data/gear_ruleset_test/gear_events_005_err.xml',None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Event id Example1 minimum time in pool must be positive', GearRuleset, 'data/gear_ruleset_test/gear_events_006_err.xml',None, True)
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 13: events element specified with no 'event' elements", GearRuleset, 'data/gear_ruleset_test/gear_events_007_err.xml',None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Event Example1 in events section must have a component specified', GearRuleset, 'data/gear_ruleset_test/gear_events_008_err.xml',None, True)
#        return
#    
#    def testRulesetMissingRootElement(self):
#        ''' Test that detects missing root element '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_ruleset_001_err.xml')
#        return
#    
#    def testRulesetNoEventSpecification(self):
#        ''' Test that detects missing root element '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_ruleset_002_err.xml', None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 15: event_equals element requires comp when event id is used', GearRuleset, 'data/gear_ruleset_test/gear_ruleset_003_err.xml', None, True)
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 19: suppress_events element requires component to be specified', GearRuleset, 'data/gear_ruleset_test/gear_ruleset_004_err.xml', None, True)
#        return
#
## TODO: Reactivate when support alert analyzers in GEAR
##    def testGearAlerts001(self):
##        '''Test that the alert info is correctly handled'''
##        grs1 = GearRuleset('data/gear_ruleset_test/gear_alerts_001.xml')
##        self.assertEqual(len(grs1['alerts'].alert_info), 2)
##        self.assertTrue('Alert1' in grs1['alerts'].alert_info)
##        self.assertTrue('Alert2' in grs1['alerts'].alert_info)
##        self.assertEqual(len(grs1['alerts'].alert_info['Alert1']), 4)
##        self.assertEqual(grs1['alerts'].alert_info['Alert1']['id'], 'Alert1')
##        self.assertEqual(grs1['alerts'].alert_info['Alert1']['name'], 'George')
##        self.assertEqual(grs1['alerts'].alert_info['Alert1']['min_time_in_pool'], 7)
##        self.assertEqual(grs1['alerts'].alert_info['Alert1']['pool_extension_time'], 12)
##        self.assertEqual(len(grs1['alerts'].alert_info['Alert2']), 4)
##        self.assertEqual(grs1['alerts'].alert_info['Alert2']['id'], 'Alert2')
##        self.assertEqual(grs1['alerts'].alert_info['Alert2']['name'], None)
##        self.assertEqual(grs1['alerts'].alert_info['Alert2']['min_time_in_pool'], None)
##        self.assertEqual(grs1['alerts'].alert_info['Alert2']['pool_extension_time'], 0)
##        # Check the event stuff too
##        self.assertEqual(len(grs1['events'].event_info), 3)
##        self.assertTrue(('TC','Example1') in grs1['events'].event_info)
##        self.assertTrue(('TC','Example2') in grs1['events'].event_info)
##        self.assertTrue(('PS','Example5') in grs1['events'].event_info)
##        tmp_event_info = grs1['events'].event_info[('TC','Example1')]
##        self.assertEqual(len(tmp_event_info), 5)
##        self.assertEqual(tmp_event_info['id'], 'Example1')
##        self.assertEqual(tmp_event_info['name'], None)
##        self.assertEqual(tmp_event_info['min_time_in_pool'], 5)
##        self.assertEqual(tmp_event_info['pool_extension_time'], 3)
##        self.assertEqual(tmp_event_info['comp'], 'TC')
##        tmp_event_info = grs1['events'].event_info[('TC','Example2')]
##        self.assertEqual(len(tmp_event_info), 5)
##        self.assertEqual(tmp_event_info['id'], 'Example2')
##        self.assertEqual(tmp_event_info['name'], None)
##        self.assertEqual(tmp_event_info['min_time_in_pool'], None)
##        self.assertEqual(tmp_event_info['pool_extension_time'], 0)
##        self.assertEqual(tmp_event_info['comp'], 'TC')
##        tmp_event_info = grs1['events'].event_info[('PS','Example5')]
##        self.assertEqual(len(tmp_event_info), 5)
##        self.assertEqual(tmp_event_info['id'], 'Example5')
##        self.assertEqual(tmp_event_info['name'], 'REFNAME')
##        self.assertEqual(tmp_event_info['min_time_in_pool'], None)
##        self.assertEqual(tmp_event_info['pool_extension_time'], 0)
##        self.assertEqual(tmp_event_info['comp'], 'PS')
##        return
#
#    def testConstantsFromOther(self):
#        ''' Test getting constants from other events and alerts sections'''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_constants_001.xml',None, True)
#        self.assertEqual(len(grs1['constants']['event_id']),1)
##        self.assertEqual(len(grs1['constants']['alert_id']),1)
#        self.assertEqual(len(grs1['constants']['set_of_event_ids']),0)
##        self.assertEqual(len(grs1['constants']['set_of_alert_ids']),0)
#        self.assertEqual(grs1['constants'].get_constant('REFNAME', 'event_id'), 'Example5')
##        self.assertEqual(grs1['constants'].get_constant('George', 'alert_id'), 'Alert1')
#        return    
#        
#    def testConstants001(self):
#        ''' Test getting constants from other events and alerts sections'''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_constants_002.xml',None, True)
#        self.assertEqual(len(grs1['constants']['event_id']),2)
##        self.assertEqual(len(grs1['constants']['alert_id']),2)
#        self.assertEqual(len(grs1['constants']['set_of_event_ids']),1)
##        self.assertEqual(len(grs1['constants']['set_of_alert_ids']),1)
#        self.assertEqual(grs1['constants'].get_constant('MyEventConstant', 'event_id'), 'Example2')
##        self.assertEqual(grs1['constants'].get_constant('MyAlertConstant', 'alert_id'), 'Alert2')
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet', 'set_of_event_ids'), set(['Example1', 'Example2', 'Example5']))
##        self.assertEqual(grs1['constants'].get_constant('MyAlertSet', 'set_of_alert_ids'), set(['Alert1', 'Alert2']))    
#        # Make sure the ones from alerts and events are still there
#        self.assertEqual(grs1['constants'].get_constant('REFNAME', 'event_id'), 'Example5')
##        self.assertEqual(grs1['constants'].get_constant('George', 'alert_id'), 'Alert1')
#        return   
#    
#    def testConstants002(self):
#        ''' Test constant set with duplicates '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_constants_003.xml',None, True)
#        self.assertEqual(len(grs1['constants']['event_id']),2)
##        self.assertEqual(len(grs1['constants']['alert_id']),2)
#        self.assertEqual(len(grs1['constants']['set_of_event_ids']),1)
##        self.assertEqual(len(grs1['constants']['set_of_alert_ids']),1)
#        self.assertEqual(grs1['constants'].get_constant('MyEventConstant', 'event_id'), 'Example2')
##        self.assertEqual(grs1['constants'].get_constant('MyAlertConstant', 'alert_id'), 'Alert2')
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet', 'set_of_event_ids'), set(['Example1', 'Example2', 'Example5']))
##        self.assertEqual(grs1['constants'].get_constant('MyAlertSet', 'set_of_alert_ids'), set(['Alert1', 'Alert2']))    
#        # Make sure the ones from alerts and events are still there
#        self.assertEqual(grs1['constants'].get_constant('REFNAME', 'event_id'), 'Example5')
##        self.assertEqual(grs1['constants'].get_constant('George', 'alert_id'), 'Alert1')
#        return 
#           
#    def testConstants003(self):
#        ''' Test constant sets using constant and constant sets '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_constants_004.xml',None, True)
#        self.assertEqual(len(grs1['constants']['event_id']),2)
##        self.assertEqual(len(grs1['constants']['alert_id']),2)
#        self.assertEqual(len(grs1['constants']['set_of_event_ids']),3)
##        self.assertEqual(len(grs1['constants']['set_of_alert_ids']),1)
#        self.assertEqual(grs1['constants'].get_constant('MyEventConstant', 'event_id'), 'Example2')
##        self.assertEqual(grs1['constants'].get_constant('MyAlertConstant', 'alert_id'), 'Alert2')
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet', 'set_of_event_ids'), set(['Example1', 'Example2', 'Example5']))
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet1', 'set_of_event_ids'), set(['Example1', 'Example5']))
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet2', 'set_of_event_ids'), set(['Example2', 'Example5']))
##        self.assertEqual(grs1['constants'].get_constant('MyAlertSet', 'set_of_alert_ids'), set(['Alert1', 'Alert2']))    
#        # Make sure the ones from alerts and events are still there
#        self.assertEqual(grs1['constants'].get_constant('REFNAME', 'event_id'), 'Example5')
##        self.assertEqual(grs1['constants'].get_constant('George', 'alert_id'), 'Alert1')
#        return  
#          
#    def testConstants004(self):
#        ''' Test constant sets using constant and constant sets '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_constants_005.xml',None, True)
#        self.assertEqual(len(grs1['constants']['event_id']),2)
##        self.assertEqual(len(grs1['constants']['alert_id']),2)
#        self.assertEqual(len(grs1['constants']['set_of_event_ids']),4)
##        self.assertEqual(len(grs1['constants']['set_of_alert_ids']),1)
#        self.assertEqual(grs1['constants'].get_constant('MyEventConstant', 'event_id'), 'Example2')
##        self.assertEqual(grs1['constants'].get_constant('MyAlertConstant', 'alert_id'), 'Alert2')
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet', 'set_of_event_ids'), set(['Example1', 'Example2', 'Example5']))
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet1', 'set_of_event_ids'), set(['Example1', 'Example5']))
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet2', 'set_of_event_ids'), set(['Example2', 'Example5']))
#        self.assertEqual(grs1['constants'].get_constant('MyEventSet3', 'set_of_event_ids'), set(['Example5']))
##        self.assertEqual(grs1['constants'].get_constant('MyAlertSet', 'set_of_alert_ids'), set(['Alert1', 'Alert2']))    
#        # Make sure the ones from alerts and events are still there
#        self.assertEqual(grs1['constants'].get_constant('REFNAME', 'event_id'), 'Example5')
##        self.assertEqual(grs1['constants'].get_constant('George', 'alert_id'), 'Alert1')
#        return   
#         
#    def testConstants005a(self):
#        ''' Test constant sets using constant and constant sets with loopback one level'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_006_err.xml')
#        return
#    
#    def testConstants005b(self):
#        ''' Test constant sets using constant and constant sets with loopback two levels'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_007_err.xml')
#        return
#    
#    def testConstants005c(self):
#        ''' Test constant duplicate definition '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_008_err.xml')
#        return
#    
#    def testConstants005d(self):
#        ''' Test constant not constant elements in constants '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_009_err.xml')
#        return
#    
#    def testConstants005e(self):
#        ''' Test constant name is blank on event element'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_010_err.xml')
#        return
#    
#    def testConstants005f(self):
#        ''' Test constant name is blank on constant element'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_011_err.xml')
#        return
#    
#    def testConstants005g(self):
#        ''' Test constant type is blank '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_012_err.xml')
#        return
#    
#    def testConstants005h(self):
#        ''' Test constant type is invalid value: fubar'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_013_err.xml')
#        return
#    
#    def testConstants005i(self):
#        ''' Test constant value is blank '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 21: constant 'MyEventConstant2' value must be at least one character", GearRuleset, 'data/gear_ruleset_test/gear_constants_014_err.xml',None, True)
#        return
#    
#    def testConstants005j(self):
#        ''' Test constant value not specified'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_015_err.xml',None, True)
#        return
#    
#    def testConstants005k(self):
#        ''' Test constant type not specified '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_016_err.xml',None, True)
#        return
#    
#    def testConstants005l(self):
#        ''' Test constant name not specified '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_constants_017_err.xml',None, True)
#        return
#    
#    def testRuleValueContainsGV(self):
#        ''' Test rule variable contains bad gear variable - HELPER'''
#        self.assertTrue(_contains_gear_variable("GEAR[cur_event]"))
#        self.assertTrue(_contains_gear_variable("GEAR[cur_event.src_loc]"))
#        self.assertTrue(_contains_gear_variable("GEAR[cur_event.ext.neighbor]"))
#        self.assertTrue(_contains_gear_variable("GEAR[condition_events]"))
#        self.assertFalse(_contains_gear_variable("BB0075a"))
#        self.assertFalse(_contains_gear_variable(""))
#        self.assertRaises(XMLParsingError, _parse_gear_variable, "xGEAR[cur_event]")
#        self.assertRaises(XMLParsingError, _parse_gear_variable, "GEAR [cur_event]")
#        self.assertRaises(XMLParsingError, _parse_gear_variable, "GEAR[cur_event]x")
#        self.assertRaises(XMLParsingError, _parse_gear_variable, "GEAR[]")
#        return
#    
#    def testRuleValueBadGV(self):
#        ''' Test bad GEAR variable specifications '''
## TODO: Add test cases for these --> have to create an xml file now
##        self.assertRaises(XMLParsingError, rule_value_factory, "GEAR[sneeple]", 0)
##        self.assertRaises(XMLParsingError, rule_value_factory, "GEAR[cur_event.sneeple]", 0)
##        self.assertRaises(XMLParsingError, rule_value_factory, "GEAR[cur_event.extr.neighbor]", 0) 
##        self.assertRaises(XMLParsingError, rule_value_factory, "GEAR[cur_event.ext.neighbor", 0) 
#        return
#
#    def testPoolControl001(self):
#        ''' test that pool control works when forced '''
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_pool_control_001.xml',None, True)
#        self.assertEqual(grs1['pool_control']['initial_duration'], 4)
#        self.assertEqual(grs1['pool_control']['max_duration'], 9)
#        return
#    
#    def testPoolControl002(self):
#        ''' test that pool control works when value in configuration and ignored when forced'''
#        config_dict = {'initial_pool_duration':'5', 'max_pool_duration':'10'}
#        # 5 will be ignored due to force, 10 will override because in range.
#        grs1 = GearRuleset('data/gear_ruleset_test/gear_pool_control_001.xml', config_dict, True)
#        self.assertEqual(grs1['pool_control']['initial_duration'], 4)
#        self.assertEqual(grs1['pool_control']['max_duration'], 10)
#        return
#    
#    def testPoolControl003(self):
#        ''' test that pool control fails when out of range'''
#        config_dict = {'initial_pool_duration':'5', 'max_pool_duration':'1'}
#        # 5 will be ignored due to force, 1 will fail because too small
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 33: pool control max duration error: value specified is less than minimum', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_001.xml', config_dict, True)
#        # Now set value too big
#        config_dict['max_pool_duration'] = '200'
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 33: pool control max duration error: value specified is greater than maximum', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_001.xml', config_dict, True)
#        return
#    
#    def testPoolControl004(self):
#        ''' test that pool control causes failure when not specified in config or in rule '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 0: pool control initial duration not in rule, so must be in configuration file', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_002_err.xml',None, True)
#        return
#    
#    def testPoolControl005(self):
#        ''' test that pool control with no subelements fails '''
#        config_dict = {'initial_pool_duration':'5', 'max_pool_duration':'1'}
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 33: pool control element must have at least one sub-element specified', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_003_err.xml', config_dict, True)
#        return
#    
#    def testPoolControl006(self):
#        ''' Test that specifying minimum with force fails '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 33: pool control initial duration error: force attribute and minimum cannot both be specified', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_004_err.xml',None, True)
#        return
#    
#    def testPoolControl007(self):
#        ''' Test that specifying maximum with force fails '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 32: pool control initial duration error: force attribute and maximum cannot both be specified', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_005_err.xml',None, True)
#        return
#    
#    def testPoolControl008(self):
#        ''' Test that specifying force with no default '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 32: pool control initial duration error: force attribute without default', GearRuleset, 'data/gear_ruleset_test/gear_pool_control_006_err.xml',None, True)
#        return
#    
#    def testRuleErr01(self):
#        ''' Test that rule element must have condition subelement'''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 16: rules element requires both the 'condition' and 'action' sub-elements", GearRuleset, 'data/gear_ruleset_test/gear_rule_001_err.xml',None, True)
#        return
#
#    def testRuleErr02(self):
#        ''' Test that rule element must have action subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_002_err.xml', None)
#        return
#
#    def testRuleErr03(self):
#        ''' Test Test that rule element must have subelements (just desc)'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_003_err.xml', None)
#        return
#
#    def testRuleErr04(self):
#        ''' Test that rule element must have subelements (none)'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_004_err.xml', None)
#        return
#
#    def testRuleErr05(self):
#        ''' Test that rule element must have only one condition subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_005_err.xml', None)
#        return
#
#    def testRuleErr06(self):
#        ''' Test that condition element must have a subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_006_err.xml', None)
#        return
#
#    def testRuleErr07(self):
#        ''' Test that condition element must have a subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_007_err.xml', None)
#        return
#    
#    def testRuleErr08(self):
#        ''' Test that condition element must have a subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_008_err.xml', None)
#        return
#
#    def testRuleErr09(self):
#        ''' Test that condition element must have a subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_009_err.xml', None)
#        return
#
#    def testRuleErr10(self):
#        ''' Test that condition element must have a subelement'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_010_err.xml', None)
#        return
#
#    def testRuleErr11(self):
#        ''' Test that condition element scope with bad type fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_011_err.xml', None)
#        return
#
#    def testRuleErr12(self):
#        ''' Test that condition element scope with bad component fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_012_err.xml', None)
#        return
#
#    def testRuleErr13(self):
#        ''' Test that event_equals with bad scope type fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_013_err.xml', None)
#        return
#
#    def testRuleErr14(self):
#        ''' Test that event_equals with bad scope comp fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_014_err.xml', None)
#        return
#
#    def testRuleErr15(self):
#        ''' Test that event_equals with bad scope comp fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_015_err.xml', None)
#        return
#
#    def testRuleErr16(self):
#        ''' Test that any_events missing num fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_016_err.xml', None)
#        return
#
#    def testRuleErr17(self):
#        ''' Test that any_events missing ids fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_017_err.xml', None)
#        return
#
#    def testRuleErr18(self):
#        ''' Test that any_events missing comp fails'''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_018_err.xml', None)
#        return
#
#    def testRuleErr19(self):
#        ''' Test that event_occurred without comp fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_019_err.xml', None)
#        return
#
#    def testRuleErr20(self):
#        ''' Test that event_occurred without num fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_020_err.xml', None)
#        return
#
#    def testRuleErr21(self):
#        ''' Test that event_occurred without id fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_021_err.xml', None)
#        return
#
#    def testRuleErr22(self):
#        ''' Test that event_occurred with negative num fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_022_err.xml', None)
#        return
#
#    def testRuleErr23(self):
#        ''' Test that event_occurred with negative duration fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_023_err.xml', None)
#        return
#
#    def testRuleErr24(self):
#        ''' Test that event_occurred with zero duration fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_024_err.xml', None)
#        return
#
#    def testRuleErr25(self):
#        ''' Test that event_occurred with blank num fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_025_err.xml', None)
#        return
#
#    def testRuleErr26(self):
#        ''' Test that event_occurred with blank duration fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_026_err.xml', None)
#        return
#    
#    def testRuleErr27(self):
#        ''' Test that event_occurred with char num fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_027_err.xml', None)
#        return
#    
#    def testRuleErr28(self):
#        ''' Test that event_occurred with char num fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_028_err.xml', None)
#        return
#   
#    def testRuleErr29(self):
#        ''' Test that event_occurred with char num fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_029_err.xml', None)
#        return
#
#    def testRuleErr30(self):
#        ''' Test that action with no sub-elements fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_030_err.xml', None)
#        return
#
#    def testRuleErr31(self):
#        ''' Test that action with no sub-elements fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_031_err.xml', None)
#        return
#
#    def testRuleErr32(self):
#        ''' Test that action with no sub-elements fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_032_err.xml', None)
#        return
#    
#    def testRuleErr33(self):
#        ''' Test that action with no sub-elements fails '''
#        self.assertRaises(XMLParsingError, GearRuleset, 'data/gear_ruleset_test/gear_rule_033_err.xml', None)
#        return
#    
#    def testRuleErr34(self):
#        ''' Test that scope and events attribute together fails '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 23: suppress_events element does not allow scope attribute to be specified with events attribute',GearRuleset, 'data/gear_ruleset_test/gear_rule_034_err.xml',None, True)
#        return
#
#    def testRuleErr35(self):
#        ''' Test that fails: all_events element: ids attribute is required'''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 20: all_events element ids attribute: Required attribute not set', GearRuleset, 'data/gear_ruleset_test/gear_rule_035_err.xml',None, True)
#        return
#    
#    def testRuleErr36(self):
#        ''' Test that fails: all_events element: comp attribute must be specified '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 20: all_events element comp attribute: required value not set', GearRuleset, 'data/gear_ruleset_test/gear_rule_036_err.xml',None, True)
#        return
#   
#    def testRuleErr37(self):
#        ''' Test that fails: any_events element: num attribute is required '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 20: any_events element num attribute: Required attribute not set', GearRuleset, 'data/gear_ruleset_test/gear_rule_037_err.xml',None, True)
#        return
#   
#    def testRuleErr38(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: any_events element((20, '0.3.1.2.1')): instance_loc_comp attribute required when instances attribute is used", GearRuleset, 'data/gear_ruleset_test/gear_rule_038_err.xml',None, True)
#        return
#   
#    def testRuleErr39(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 23: suppress_events element must specify ids, location, or events attribute', GearRuleset, 'data/gear_ruleset_test/gear_rule_039_err.xml',None, True)
#        return
#    
#    def testRuleErr40(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 24: create_alert element requires the 'id' attribute", GearRuleset, 'data/gear_ruleset_test/gear_rule_040_err.xml',None, True)
#        return
#    
#    def testRuleErr41(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable specification unrecognized (depth) variable name 'GEAR[name.bad]'", GearRuleset, 'data/gear_ruleset_test/gear_rule_041_err.xml',None, True)
#        return
#    
#    def testRuleErr42(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable name not supported 'xyzzy'", GearRuleset, 'data/gear_ruleset_test/gear_rule_042_err.xml', None, True)
#        return
#   
#    def testRuleErr43(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable specification unrecognized variable name 'xyzzy' (2nd)", GearRuleset, 'data/gear_ruleset_test/gear_rule_043_err.xml', None, True)
#        return
#  
#    def testRuleErr44(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 22: evaluate element was unable to load specified the class: ibm.teal.test.ut.data.gear_ruleset_test.t046.test_class.Class046BAD', GearRuleset, 'data/gear_ruleset_test/gear_rule_044_err.xml', None, True)
#        return
#  
#    def testRuleErr45(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, 'Parsing failure in GEAR ruleset unnamed on line 22: evaluate element was unable to load specified the class: ibm.teal.test.ut.data.gear_ruleset_test.t046.bad.test_class.Class046', GearRuleset, 'data/gear_ruleset_test/gear_rule_045_err.xml', None, True)
#        return
# 
#    def testRuleErr46(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable specification unrecognized (depth) variable name'GEAR[cur_event.ext.dict.more]'", GearRuleset, 'data/gear_ruleset_test/gear_rule_046_err.xml', None, True)
#        return
# 
#    def testRuleErr47(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable specification 'GEAR[condition_events]' not allowed in condition portion of a rule", GearRuleset, 'data/gear_ruleset_test/gear_rule_047_err.xml', None, True)
#        return
# 
#    def testRuleErr48(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable specification 'GEAR[condition_event_ids]' not allowed in condition portion of a rule", GearRuleset, 'data/gear_ruleset_test/gear_rule_048_err.xml', None, True)
#        return
# 
#    def testRuleErr49(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parm error: GEAR variable reference to config dict invalid.  'not_there' not in dictionary", GearRuleset, 'data/gear_ruleset_test/gear_rule_049_err.xml', None, True)
#        return
#    
#    def testRuleErr50(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parameter error: parm element must have a 'name' attribute", GearRuleset, 'data/gear_ruleset_test/gear_rule_050_err.xml', None, True)
#        return
#    
#    def testRuleErr51(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 22: evaluate element parameter error: parm element must have a 'value' attribute", GearRuleset, 'data/gear_ruleset_test/gear_rule_051_err.xml', None, True)
#        return
#    
#    def testRuleErr52(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 36: evaluate element must have a 'class' attribute", GearRuleset, 'data/gear_ruleset_test/gear_rule_052_err.xml', None, True)
#        return
#    
#    def testRuleErr53(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 36: evaluate element must have a 'name' attribute", GearRuleset, 'data/gear_ruleset_test/gear_rule_053_err.xml', None, True)
#        return    
#    
#    def testRulesetErr05(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 0: events to analyze must be specified either using the 'events' element or the 'will_analyze' element", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_005_err.xml', None, True)
#        return
#    
#    def testRulesetErr06(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 11: Component TST event id Example2 (Example2) is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_006_err.xml', None, True)
#        return
#    
#    def testRulesetErr07(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 11: Component TST event id Example2 (Example2) is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_007_err.xml', None, True)
#        return
#    
#    def testRulesetErr08(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 10: condition element encountered an unexpected sub-element bad_element", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_008_err.xml', None, True)
#        return
#     
#    def testRulesetErr09(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 12: event_occurred element num attribute: Required attribute not set", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_009_err.xml', None, True)
#        return
#     
#    def testRulesetErr10(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 14: Component TST event id BadOne in list Example2,BadOne is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_010_err.xml', None, True)
#        return
#     
#    def testRulesetErr11(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 14: Component TST event id BadOne in list BadOne is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_011_err.xml', None, True)
#        return
#     
#    def testRulesetErr12(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 18: Component TST event id BadOne2 in list Example2,BadOne2 is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_012_err.xml', None, True)
#        return
#     
#    def testRulesetErr13(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 15: Component TST event id BAD3 in list Example1, BAD3, Example2 is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_013_err.xml', None, True)
#        return
#     
#    def testRulesetErr14(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 15: Component TST event id BAD3 in list Example1, BAD3, Example2 is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_014_err.xml', None, True)
#        return
#    
#    def testRulesetErr15(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 15: Component TST event id BAD3 in list Example1, Example2, BAD3, Example2 is not one that will be evaluated.", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_015_err.xml', None, True)
#        return
#    
#    def testRulesetErr16(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element alert id validation failed trying to retrieve the alert metadata", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_016_err.xml', None, True)
#        return
#    
#    def testRulesetErr17(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_017_err.xml', None, True)
#        return
#    
#    def testRulesetErr18(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_018_err.xml', None, True)
#        return
#    
#    def testRulesetErr19(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_019_err.xml', None, True)
#        return
#    
#    def testRulesetErr20(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_020_err.xml', None, True)
#        return
#    
#    def testRulesetErr21(self):
#        ''' Test that fails '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_021_err.xml', None, True)
#        return
#    
#    def testRulesetErr22(self):
#        ''' Test that fails 22 '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 0: gear_ruleset element schema_version was 1.1 but only 1.0 is currently supported", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_022_err.xml', None, True)
#        return
#    
#    
#class GearRulesetTestWithMetadata(TealTestCase):
#    '''Test loading GEAR rulesets
#       Need a valid alertmetadata for tese tests, so hijacking t001's configuration
#    '''
#
#    def setUp(self):
#        self.teal = teal.Teal('data/gear_ruleset_test/t001/config.conf', 'stderr', msgLevel='debug', commit_alerts=False)
#        return
#
#    def tearDown(self):
#        self.teal.shutdown()
#        return
#    
#    def testRulesetErr16a(self):
#        ''' Test that fails with metadata 16a '''
#        self.assertRaisesTealError(XMLParsingError, "Parsing failure in GEAR ruleset unnamed on line 20: create_alert element alert id Bad Alert id does not have metadata", GearRuleset, 'data/gear_ruleset_test/gear_ruleset_016_err.xml', None, True)
#        return

    
if __name__ == "__main__":
    unittest.main()