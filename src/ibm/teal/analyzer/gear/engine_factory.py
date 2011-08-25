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
from ibm.teal.analyzer.gear.common import GCFG_RULES
from ibm.teal.analyzer.gear.ruleset import GearRuleset
from ibm.teal.registry import get_service, TEAL_DATA_DIR
from ibm.teal.teal_error import ConfigurationError
import os

def engine_factory(name, config_dict, event_input=False, alert_input=False, number=0, send_alert=None):
    ''' Create the appropriate GEAR engine
    
        Currently only the executable ruleset is supported 
    '''
    rules_file = config_dict.get(GCFG_RULES, None)
    if rules_file is None:
        raise ConfigurationError('Configuration failure for GEAR based event analyzer {0}: rules not specified'.format(name))
    data_dir = get_service(TEAL_DATA_DIR)
    rules_file_path = os.path.join(data_dir,rules_file)
    return GearRuleset(rules_file_path, config_dict, event_input=event_input, alert_input=alert_input, number=number, name=name, send_alert=send_alert)

