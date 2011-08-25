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
import subprocess
import os
import platform

from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal import Teal, registry
VFYRULE = ''

class TestTlvfyrule(TealTestCase):

    def setUp(self):
        global VFYRULE
        t = Teal('data/tlcommands_test/test.conf',data_only=True)
        teal_path = registry.get_service(registry.TEAL_ROOT_DIR)
        VFYRULE = os.path.join(teal_path,'bin/tlvfyrule')
        t.shutdown()
        
        tmp_data_dir = os.path.join(os.environ.get('TEAL_ROOT_DIR','/opt/teal'),'data')
        self.teal_data_dir = self.force_env('TEAL_DATA_DIR', tmp_data_dir)
        return
    
    def tearDown(self):
        self.restore_env('TEAL_DATA_DIR', self.teal_data_dir)
        return
    
    def test_tlvfyrule(self):
        ''' Run with test rule files both good and bad '''
        self.assertCmdFails([VFYRULE], 'rule file to process must be specified', exp_rc=1)
        # TODO: ruleset needs to be updated --> self.assertCmdFails([VFYRULE, 'data/gear_ruleset_test/gear_ruleset_017_err.xml'], "'Parsing failure in GEAR ruleset data/gear_ruleset_test/gear_ruleset_017_err.xml on line 20: create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false'")  
        # TODO: Needs loc support --> self.assertCmdWorks([VFYRULE, 'data/gear_ruleset_test/t001/rule_to_test.xml', '--metadata=data/gear_ruleset_test/t001/alert_metadata.xml', '--conf_attr=initial_pool_duration:1'])
        self.assertCmdWorks([VFYRULE, 'data/gear_ruleset_test/t004/rule_to_test.xml', '--metadata=data/gear_ruleset_test/t004/alert_metadata.xml', '--conf_attr=max_pool_duration:100,initial_pool_duration:1'])
        # TODO: Needs loc support --> self.assertCmdWorks([VFYRULE, 'data/gear_ruleset_test/t005/rule_to_test.xml', '--metadata=data/gear_ruleset_test/t005/alert_metadata.xml', '--conf_attr=max_pool_duration:100,initial_pool_duration:1'])
        return

if __name__ == "__main__":
    unittest.main()