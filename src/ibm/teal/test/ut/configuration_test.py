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

from ibm.teal.configuration import Configuration
from ibm.teal.configuration import CONFIG_EVENT_ANALYZERS, CONFIG_ALERT_ANALYZERS, CONFIG_ALERT_FILTERS, CONFIG_ALERT_LISTENERS
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.teal_error import ConfigurationError

class ConfigurationTest(TealTestCase):


    def setUp(self):
        ''' Nothing to do'''
        self.create_temp_logger('critical')

    def tearDown(self):
        ''' Nothing to do ''' 

    def testBasicNoFiles(self):
        '''Test if one file is specified
        '''
        cf1 = Configuration([])
        self.assertEqual(len(cf1.sections()), 0)
     
    def testBasicOneFile(self):
        '''Test if no files are specified
        '''
        cf1 = Configuration(['data/configuration_test/configurationtest_01.conf'])
        self.assertEqual(len(cf1.sections()), 4)
        # Event Analyzers
        ea = cf1.get_active_sections(CONFIG_EVENT_ANALYZERS)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], (CONFIG_EVENT_ANALYZERS + '.mya1', 'mya1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'analyzer1.Analyzer1')
        # Alert Analyzers
        aa = cf1.get_active_sections(CONFIG_ALERT_ANALYZERS)
        self.assertEqual(len(aa), 1)
        self.assertEqual(aa[0], (CONFIG_ALERT_ANALYZERS + '.myaA', 'myaA'))
        opts = cf1.items(aa[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrulesA')
        self.assertEqual(opts_dict['class'], 'analyzerA.AnalyzerA')
        # Alert Listeners
        al = cf1.get_active_sections(CONFIG_ALERT_LISTENERS, 'all')
        self.assertEqual(len(al), 1)
        self.assertEqual(al[0], (CONFIG_ALERT_LISTENERS + '.myl1', 'myl1'))
        # Alert Filters
        af = cf1.get_active_sections(CONFIG_ALERT_FILTERS, 'all')
        self.assertEqual(len(af), 1)
        self.assertEqual(af[0], (CONFIG_ALERT_FILTERS + '.myf1', 'myf1'))
        return

    def testBasicLoadAnalyzer(self):
        '''Test loading an analyzer'''
        cf1 = Configuration(['data/configuration_test/configurationtest_02.conf'])
        self.assertEqual(len(cf1.sections()), 1)
        # Event Analyzers
        ea = cf1.get_active_sections(CONFIG_EVENT_ANALYZERS)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], (CONFIG_EVENT_ANALYZERS + '.allalert', 'allalert'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'ibm.teal.test.ut.event_analyzer_test.SimpleEventAnalyzerAllAlert')
        # Note that test of using the data is done by teal_test

    def testCallAddFilesTwice(self):
        '''test that can add more than one file'''
        cf1 = Configuration(['data/configuration_test/configurationtest_01.conf',   \
                             'data/configuration_test/configurationtest_02.conf'])
        self.assertEqual(len(cf1.sections()), 5)
        # Event Analyzers
        ea = cf1.get_active_sections(CONFIG_EVENT_ANALYZERS)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[1], (CONFIG_EVENT_ANALYZERS + '.mya1', 'mya1'))
        opts = cf1.items(ea[1][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'analyzer1.Analyzer1')
        self.assertEqual(ea[0], (CONFIG_EVENT_ANALYZERS + '.allalert', 'allalert'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'ibm.teal.test.ut.event_analyzer_test.SimpleEventAnalyzerAllAlert')
        # Alert Analyzers
        aa = cf1.get_active_sections(CONFIG_ALERT_ANALYZERS)
        self.assertEqual(len(aa), 1)
        self.assertEqual(aa[0], (CONFIG_ALERT_ANALYZERS + '.myaA', 'myaA'))
        opts = cf1.items(aa[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrulesA')
        self.assertEqual(opts_dict['class'], 'analyzerA.AnalyzerA')
        # Alert Listeners
        al = cf1.get_active_sections(CONFIG_ALERT_LISTENERS)
        self.assertEqual(len(al), 1)
        self.assertEqual(al[0], (CONFIG_ALERT_LISTENERS + '.myl1', 'myl1'))
        # Alert Filters
        af = cf1.get_active_sections(CONFIG_ALERT_FILTERS)
        self.assertEqual(len(af), 1)
        self.assertEqual(af[0], (CONFIG_ALERT_FILTERS + '.myf1', 'myf1'))
    
    def testGetActiveSectionsNoRunMode(self):
        ''' Test the get active sections support ignoring run mode '''
        cf1 = Configuration(['data/configuration_test/configurationtest_03.conf'])
        self.assertEqual(len(cf1.sections()), 7)
        ##### Variation 1: test one with a name
        ea = cf1.get_active_sections('needs_name1', name_required=True)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('needs_name1.name1', 'name1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name1a'],'value1a')
        # Since has name not requiring it should give same results 
        ea = cf1.get_active_sections('needs_name1', name_required=False)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('needs_name1.name1', 'name1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name1a'],'value1a')
        # Since singleton, requiring it be one should give same results
        ea = cf1.get_active_sections('needs_name1', name_required=True, singleton=True)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('needs_name1.name1', 'name1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name1a'],'value1a')
        ##### Variation 2: test one without a name
        self.assertRaisesTealError(ConfigurationError, 'Configuration sections for \'needs_name2\' must have a name, but none was specified', cf1.get_active_sections, 'needs_name2', None, True)
        # Since has name not requiring it should work 
        ea = cf1.get_active_sections('needs_name2', name_required=False)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('needs_name2', None))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name2a'],'value2a')
        # Since singleton, requiring it be one should give same results
        ea = cf1.get_active_sections('needs_name2', name_required=False, singleton=True)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('needs_name2', None))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name2a'],'value2a')
        ##### Variation 3: test duplicate stanzas
        self.assertRaisesTealError(ConfigurationError, 'Configuration sections for \'single02\' must have a name, but none was specified', cf1.get_active_sections, 'single02', None, True)
        # Since has name not requiring it should work 
        ea = cf1.get_active_sections('single02', name_required=False)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('single02', None))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name21'],'value21')
        self.assertEqual(opts_dict['name22'],'value22')
        # Last one wins when duplicates
        self.assertEqual(opts_dict['dupestanza'],'second')
        # Since singleton, requiring it be one should give same results
        ea = cf1.get_active_sections('single02', name_required=False, singleton=True)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], ('single02', None))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name21'],'value21')
        self.assertEqual(opts_dict['name22'],'value22')
        # Last one wins when duplicates
        self.assertEqual(opts_dict['dupestanza'],'second')
        #### Variation 4: test singleton, both with names
        ea = cf1.get_active_sections('single03', name_required=True)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], ('single03.name31', 'name31'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name31'],'value31')
        self.assertEqual(ea[1], ('single03.name32', 'name32'))
        opts = cf1.items(ea[1][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name32'],'value32')
        # Since has name not requiring it should give same results 
        ea = cf1.get_active_sections('single03', name_required=False)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], ('single03.name31', 'name31'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name31'],'value31')
        self.assertEqual(ea[1], ('single03.name32', 'name32'))
        opts = cf1.items(ea[1][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name32'],'value32')
        # Since singleton, requiring it be one should give same results
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'single03'", cf1.get_active_sections, 'single03', None, True, True)
        ##### Variation 5: test singleton, one with name 
        self.assertRaisesTealError(ConfigurationError, 'Configuration sections for \'single04\' must have a name, but none was specified', cf1.get_active_sections, 'single04', None, True)
        # Since has name not requiring it should work 
        ea = cf1.get_active_sections('single04', name_required=False)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[1], ('single04.name41', 'name41'))
        opts = cf1.items(ea[1][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name41'],'value41')
        self.assertEqual(ea[0], ('single04', None))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 1)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['name42'],'value42')
        # Since singleton, requiring it be one should give same results
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'single04'", cf1.get_active_sections, 'single04', None, False, True)
    
    def testGetActiveSectionsWithRunMode(self):
        ''' Test the get active sections with run mode '''
        cf1 = Configuration(['data/configuration_test/configurationtest_04.conf'])
        self.assertEqual(len(cf1.sections()), 9)
        ##### Variation 1: enabled = <blank>
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'historic', True, True)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'realtime', True, True)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'historic', True, False)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'realtime', True, False)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'historic', False, False)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'realtime', False, False)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'historic', False, True)
        self.assertRaisesTealError(ConfigurationError, "Configuration section 'test1.blank_enabled' has an unrecognized value for enabled keyword: ''", cf1.get_active_sections, 'test1', 'realtime', False, True)
        ##### Variation 2: enabled = false
        ea = cf1.get_active_sections('test2', 'realtime', True, True)
        self.assertEqual(len(ea), 0)
        ea = cf1.get_active_sections('test2', 'realtime', True, False)
        self.assertEqual(len(ea), 0)
        ea = cf1.get_active_sections('test2', 'realtime', False, True)
        self.assertEqual(len(ea), 0)
        ea = cf1.get_active_sections('test2', 'realtime', False, False)
        self.assertEqual(len(ea), 0)
        ##### Variation 3: enabled = all 
        ea = cf1.get_active_sections('test3', 'realtime', False, False)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], ('test3.all_enabled1', 'all_enabled1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 2)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['tn3a'],'tv3a')
        ea = cf1.get_active_sections('test3', 'realtime', True, False)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], ('test3.all_enabled1', 'all_enabled1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 2)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['tn3a'],'tv3a')
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'test3'", cf1.get_active_sections, 'test3', 'historic', True, True)
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'test3'", cf1.get_active_sections, 'test3', 'historic', False, True)
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'test3'", cf1.get_active_sections, 'test3', 'realtime', True, True)
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'test3'", cf1.get_active_sections, 'test3', 'realtime', False, True)
        ##### Variation 4: one of each
        ea = cf1.get_active_sections('test4', 'realtime', False, False)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], ('test4.misc1', 'misc1'))
        opts = cf1.items(ea[0][0])
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['tn4a'], 'tv4a')
        self.assertEqual(ea[1], ('test4.misc3', 'misc3'))
        opts = cf1.items(ea[1][0])
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['tn4c'], 'tv4c')
        ea = cf1.get_active_sections('test4', 'historic', True, False)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], ('test4.misc1', 'misc1'))
        opts = cf1.items(ea[0][0])
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['tn4a'], 'tv4a')
        self.assertEqual(ea[1], ('test4.misc2', 'misc2'))
        opts = cf1.items(ea[1][0])
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['tn4b'], 'tv4b')
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'test4'", cf1.get_active_sections, 'test4', 'realtime', False, True)
        self.assertRaisesTealError(ConfigurationError, "There can only be one section called 'test4'", cf1.get_active_sections, 'test4', 'historic', False, True)
        
if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
