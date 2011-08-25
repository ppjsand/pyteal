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

from ibm import teal
from ibm.teal import registry
from ibm.teal.registry import get_logger, SERVICE_CONFIGURATION
from ibm.teal.configuration import Configuration
from ibm.teal.configuration import CONFIG_EVENT_ANALYZERS, CONFIG_ALERT_ANALYZERS, CONFIG_ALERT_FILTERS, CONFIG_ALERT_LISTENERS

class ConfigurationTest(unittest.TestCase):


    def setUp(self):
        '''Setup logging and get deregister existing service
        '''
        if get_logger() is None: 
            teal.Teal('data/common/configurationtest.conf', 'stderr', msgLevel='debug', commit_alerts=False, commit_checkpoints=False)
        get_logger().debug('Creating SimpleAnalyzerAllAlert')

        self.existing = registry.get_service(SERVICE_CONFIGURATION)
        registry.unregister_service(SERVICE_CONFIGURATION)
        return

    def tearDown(self):
        '''If service was stored, restore it
        '''
        if self.existing is not None:
            registry.unregister_service(SERVICE_CONFIGURATION)
            registry.register_service(SERVICE_CONFIGURATION, self.existing)
        return

    def testBasicNoFiles(self):
        '''Test if one file is specified
        '''
        cf1 = Configuration([])
        self.assertEqual(len(cf1.sections()), 0)
        # TODO: Test deletion somehow
#        del cf1
#        cf_reg = registry.get_service(SERVICE_CONFIGURATION)
#        self.assertEqual(cf_reg, None)
        return
     
    def testBasicOneFile(self):
        '''Test if no files are specified
        '''
        cf1 = Configuration(['data/configuration_test/configurationtest_01.conf'])
        self.assertEqual(len(cf1.sections()), 4)
        # Event Analyzers
        ea = cf1.get_entries(CONFIG_EVENT_ANALYZERS)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], (CONFIG_EVENT_ANALYZERS + '.mya1', 'mya1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'analyzer1.Analyzer1')
        # Alert Analyzers
        aa = cf1.get_entries(CONFIG_ALERT_ANALYZERS)
        self.assertEqual(len(aa), 1)
        self.assertEqual(aa[0], (CONFIG_ALERT_ANALYZERS + '.myaA', 'myaA'))
        opts = cf1.items(aa[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrulesA')
        self.assertEqual(opts_dict['class'], 'analyzerA.AnalyzerA')
        # Alert Listeners
        al = cf1.get_entries(CONFIG_ALERT_LISTENERS)
        self.assertEqual(len(al), 1)
        self.assertEqual(al[0], (CONFIG_ALERT_LISTENERS + '.myl1', 'myl1'))
        # Alert Filters
        af = cf1.get_entries(CONFIG_ALERT_FILTERS)
        self.assertEqual(len(af), 1)
        self.assertEqual(af[0], (CONFIG_ALERT_FILTERS + '.myf1', 'myf1'))
        return

    def testBasicLoadAnalyzer(self):
        '''Test loading an analyzer'''
        cf1 = Configuration(['data/configuration_test/configurationtest_02.conf'])
        self.assertEqual(len(cf1.sections()), 1)
        # Event Analyzers
        ea = cf1.get_entries(CONFIG_EVENT_ANALYZERS)
        self.assertEqual(len(ea), 1)
        self.assertEqual(ea[0], (CONFIG_EVENT_ANALYZERS + '.allalert', 'allalert'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'ibm.teal.test.ut.event_analyzer_test.SimpleEventAnalyzerAllAlert')
        # Note that test of using the data is done by teal_test
        return

    def testCallAddFilesTwice(self):
        '''test that can add more than one file'''
        cf1 = Configuration(['data/configuration_test/configurationtest_01.conf',   \
                             'data/configuration_test/configurationtest_02.conf'])
        self.assertEqual(len(cf1.sections()), 5)
        # Event Analyzers
        ea = cf1.get_entries(CONFIG_EVENT_ANALYZERS)
        self.assertEqual(len(ea), 2)
        self.assertEqual(ea[0], (CONFIG_EVENT_ANALYZERS + '.mya1', 'mya1'))
        opts = cf1.items(ea[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'analyzer1.Analyzer1')
        self.assertEqual(ea[1], (CONFIG_EVENT_ANALYZERS + '.allalert', 'allalert'))
        opts = cf1.items(ea[1][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrules1')
        self.assertEqual(opts_dict['class'], 'ibm.teal.test.ut.event_analyzer_test.SimpleEventAnalyzerAllAlert')
        # Alert Analyzers
        aa = cf1.get_entries(CONFIG_ALERT_ANALYZERS)
        self.assertEqual(len(aa), 1)
        self.assertEqual(aa[0], (CONFIG_ALERT_ANALYZERS + '.myaA', 'myaA'))
        opts = cf1.items(aa[0][0])
        self.assertEqual(len(opts), 3)
        opts_dict = dict(opts)
        self.assertEqual(opts_dict['enabled'],'all')
        self.assertEqual(opts_dict['rule_file'],'myrulesA')
        self.assertEqual(opts_dict['class'], 'analyzerA.AnalyzerA')
        # Alert Listeners
        al = cf1.get_entries(CONFIG_ALERT_LISTENERS)
        self.assertEqual(len(al), 1)
        self.assertEqual(al[0], (CONFIG_ALERT_LISTENERS + '.myl1', 'myl1'))
        # Alert Filters
        af = cf1.get_entries(CONFIG_ALERT_FILTERS)
        self.assertEqual(len(af), 1)
        self.assertEqual(af[0], (CONFIG_ALERT_FILTERS + '.myf1', 'myf1'))
        return
        
        
if __name__ == "__main__":
    unittest.main()