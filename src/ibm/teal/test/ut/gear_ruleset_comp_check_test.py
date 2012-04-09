# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import unittest 
from ibm.teal import teal
from ibm.teal.test.teal_unittest import TealTestCase

    
class GearRulesetCompCheck(TealTestCase):
    ''' Test that component rulesets load '''
    
    def test_isnm(self):
        ''' test that isnm rule loads '''
        config = 'data/gear_ruleset_test/isnm/config.conf'
        try:
            myteal = teal.Teal(config, 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
            myteal.shutdown()
        except IOError:
            # Assume it is because it isn't installed 
            print 'Warning ISNM rule not tested because not installed'
        return
 
    def test_ll(self):
        ''' test that ll rule loads '''
        config = 'data/gear_ruleset_test/ll/config.conf'
        try:
            myteal = teal.Teal(config, 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
            myteal.shutdown()
        except IOError:
            # Assume it is because it isn't installed 
            print 'Warning LL rule not tested because not installed'
        return
       
    def test_pnsd(self):
        ''' test that pnsd rule loads '''
        config = 'data/gear_ruleset_test/pnsd/config.conf'
        try:
            myteal = teal.Teal(config, 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
            myteal.shutdown()
        except IOError:
            # Assume it is because it isn't installed 
            print 'Warning PNSD rule not tested because not installed'
        return
    
if __name__ == "__main__":
    unittest.main()