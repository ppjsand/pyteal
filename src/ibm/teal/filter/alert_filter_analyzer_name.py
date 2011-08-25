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

from ibm.teal.filter.alert_filter import AlertFilter
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.registry import get_logger

AFAN_CONFIG_ANALYZER_NAMES = 'analyzer_names'
AFAN_CONFIG_WHEN = 'when'
AFAN_WHEN_TYPE_NOT_FROM = 'not_from_analyzer'
AFAN_WHEN_TYPE_FROM = 'from_analyzer'

class AlertFilterAnalyzerName(AlertFilter):
    '''
    Filter alerts based on what analyzer produced them
    '''

    def __init__(self, name, config_dict=None):
        '''The constructor'''
        if config_dict is not None:
            if AFAN_CONFIG_WHEN in config_dict:
                self.when = config_dict[AFAN_CONFIG_WHEN]
                if self.when != AFAN_WHEN_TYPE_NOT_FROM and self.when != AFAN_WHEN_TYPE_FROM:
                    out_str = 'AlertFilterFromAnalyzer when must be from_analyzer or not_from_analyzer'
                    out_str += '. Value is {0} was specified for {1}'.format(str(self.when), name)
                    raise ConfigurationError(out_str)      
            else:
                out_str = 'AlertFilterFromAnalyzer requires when be specified'
                raise ConfigurationError(out_str)
            
            if AFAN_CONFIG_ANALYZER_NAMES in config_dict:
                self.analyzers = [a.strip() for a in config_dict[AFAN_CONFIG_ANALYZER_NAMES].split(',') if len(a.strip()) != 0]
                get_logger().debug('Filter {0} analyzers = {1}'.format(name, str(self.analyzers)))
                if len(self.analyzers) == 0:
                    raise ConfigurationError('AlertFilterFromAnalyzer analyzer_names was empty')
            else:
                raise ConfigurationError('AlertFilterFromAnalyzer requires analyzer_names be specified')         
        else:
            raise ConfigurationError('AlertFilterFromAnalyzer requires when and analyzer_names be specified')
        AlertFilter.__init__(self, name, config_dict)
        return
    
    def keep_from_listeners(self, alert):
        '''Filter the alert.  True means filtered and False means send on
        '''
        alert_analyzer = alert.src_name
        found = False
        for analyzer in self.analyzers:
            if alert_analyzer == analyzer:
                found = True
                break
        if found:
            if self.when == AFAN_WHEN_TYPE_FROM:
                # Filter it because it was from one of the listed names
                return True    
            else:
                # Don't filter it because it was not from one of the listed names
                return False
        else:
            if self.when == AFAN_WHEN_TYPE_NOT_FROM:
                # Don't filter it because it was from one of the listed names
                return True   
            else:
                # Filter it because it was not from one of the listed names
                return False
    
    def resolve_and_validate(self, info_dict):  
        ''' Makes sure that the analyzers specified are active in the config '''
        for analyzer in self.analyzers:
            if analyzer not in info_dict['analyzer_names']:
                raise ConfigurationError('AlertFilterFromAnalyzer analyzer_names entry {0} not configured or not active'.format(analyzer))
        return
    