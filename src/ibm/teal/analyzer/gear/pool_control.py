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

from ibm.teal.registry import get_logger
from ibm.teal.teal_error import XMLParsingError
from ibm.teal.analyzer.pool.incident_pool import ArrivalCheckCtl
import os

GPCL_INIT_DURATION = 'initial_duration'
GPCL_MAX_DURATION = 'max_duration'
GPCL_ARRIVAL_RATE_EXTENSION = 'arrival_rate_extension'

MAX_DURATION_DEFAULT = 300 # 5 minutes 
ENV_ARRIVAL_RATE_EXTENSION = 'TEAL_TEST_{0}_POOL_ARRIVAL_RATE_EXTENSION'
CFG_ARRIVAL_RATE_EXTENSION = 'pool_arrival_rate_extension'

class GearPoolControl(dict):
    '''
    Dictionary of GEAR constants by type
    '''

    def __init__(self, config_dict, ruleset):
        '''
        Constructor
        Get initial values from the config_dict
        '''
        dict.__init__(self)
        self.ruleset = ruleset
        self.trace_id = (0, 'poolcontrol')

        if config_dict is None or 'initial_pool_duration' not in config_dict:
            self[GPCL_INIT_DURATION] = None
        else:
            self[GPCL_INIT_DURATION] = int(config_dict['initial_pool_duration'])
            
        if config_dict is None or 'max_pool_duration' not in config_dict:
            self[GPCL_MAX_DURATION] = None
        else:
            self[GPCL_MAX_DURATION] = int(config_dict['max_pool_duration'])
            
        # Check for environment variable 
        env_to_check = ENV_ARRIVAL_RATE_EXTENSION.format(self.ruleset.name.upper())
        env_value = os.environ.get(env_to_check, None)
        if env_value is not None:
            tarel = [int(v) for v in env_value.split(',')]
            self[GPCL_ARRIVAL_RATE_EXTENSION] = ArrivalCheckCtl(window_min=tarel[0], window_max=tarel[1], arrival_rate=tarel[2], extension=tarel[3])
            get_logger().warning('Arrival Rate extension overridden using environment variable {0} with value {1}'.format(env_to_check, str(self[GPCL_ARRIVAL_RATE_EXTENSION])))
        else:
            if config_dict is None or CFG_ARRIVAL_RATE_EXTENSION not in config_dict:
                self[GPCL_ARRIVAL_RATE_EXTENSION] = None
            else:
                tarel = [int(v) for v in config_dict[CFG_ARRIVAL_RATE_EXTENSION].split(',')]
                self[GPCL_ARRIVAL_RATE_EXTENSION] = ArrivalCheckCtl(window_min=tarel[0], window_max=tarel[1], arrival_rate=tarel[2], extension=tarel[3])
                get_logger().debug('Arrival Rate extension overridden in config with value {0}'.format(str(self[GPCL_ARRIVAL_RATE_EXTENSION])))
        return
    
    def read_xml(self, xml_element, trace_dict):
        '''Read the pool control XML'''
        self.trace_id = trace_dict[xml_element]
        entry_found = False
        for xml_entry in xml_element:
            entry_name = xml_entry.tag.split('}')[-1]
            get_logger().debug('Processing  {0}'.format(entry_name))
            if entry_name == GPCL_INIT_DURATION:
                entry_found = True
                try:
                    self[GPCL_INIT_DURATION] = self._process_duration_xml(xml_entry, self[GPCL_INIT_DURATION])
                except XMLParsingError as e:
                    self.ruleset.parse_error(self.trace_id[0], 'pool control initial duration error: {0}'.format(e.msg))
            elif entry_name == GPCL_MAX_DURATION:
                entry_found = True
                try:
                    self[GPCL_MAX_DURATION] = self._process_duration_xml(xml_entry, self[GPCL_MAX_DURATION])
                except XMLParsingError as e:
                    self.ruleset.parse_error(self.trace_id[0], 'pool control max duration error: {0}'.format(e.msg))
            elif entry_name == GPCL_ARRIVAL_RATE_EXTENSION:
                entry_found = True
                if self[GPCL_ARRIVAL_RATE_EXTENSION] is None:
                    self._process_arrival_rate_extension(xml_entry)
            else:
                self.ruleset.parse_error(self.trace_id[0], 'pool control encountered an unexpected element \'{0}\''.format(entry_name))
        if not entry_found:
            self.ruleset.parse_error(self.trace_id[0], 'pool control element must have at least one sub-element specified')
        return
    
    def resolve_and_validate(self):
        ''' Resolve and validate the values '''
        if self[GPCL_INIT_DURATION] is None:
            self.ruleset.parse_error(self.trace_id[0], 'pool control initial duration not in rule, so must be in configuration file')
        # If maximum is not set to default 
        if self[GPCL_MAX_DURATION] is None:
            self[GPCL_MAX_DURATION] = MAX_DURATION_DEFAULT  
        # Check that init is not bigger than the max
        if self[GPCL_INIT_DURATION] > self[GPCL_MAX_DURATION]:
            raise XMLParsingError('pool control specified initial duration is larger than max duration')
        return
            
    def _process_duration_xml(self, xml_element, config_value):
        ''' Read the default component element '''
        # Throw XMLParsingError ... caught and rethrown with ruleset
        if 'force' in xml_element.attrib and xml_element.attrib['force'] == 'true':
            if 'default' not in xml_element.attrib:
                raise XMLParsingError('force attribute without default')
            if 'minimum' in xml_element.attrib:
                raise XMLParsingError('force attribute and minimum cannot both be specified')
            if 'maximum' in xml_element.attrib:
                raise XMLParsingError('force attribute and maximum cannot both be specified')                
            if config_value is not None:
                get_logger().warning('Configuration entry for pool duration ignored')
            return int(xml_element.attrib['default'])
        current_guess = config_value
        if 'default' in xml_element.attrib:
            if current_guess is None:
                current_guess = int(xml_element.attrib['default'])
        if 'minimum' in xml_element.attrib:
            if current_guess < int(xml_element.attrib['minimum']):
                raise XMLParsingError('value specified is less than minimum')
        if 'maximum' in xml_element.attrib:
            if current_guess > int(xml_element.attrib['maximum']):
                raise XMLParsingError('value specified is greater than maximum')
        return current_guess         
    
    def _process_arrival_rate_extension(self, xml_element):
        ''' Read the arrival rate extension element '''
        if 'window_min' not in xml_element.attrib \
                or 'window_max' not in xml_element.attrib \
                or 'arrival_rate' not in xml_element.attrib \
                or 'extension' not in xml_element.attrib:
            raise XMLParsingError('The arrival_rate_extension element requires that the window_max, arrival_rate, and extension attributes be specified')
        window_max = int(xml_element.attrib['window_max'])
        arrival_rate = int(xml_element.attrib['arrival_rate'])
        extension = int(xml_element.attrib['extension'])
        if 'window_min' in xml_element.attrib:
            window_min = int(xml_element.attrib['window_min'])
        else:
            window_min = window_max
        self[GPCL_ARRIVAL_RATE_EXTENSION] = ArrivalCheckCtl(window_min=window_min, window_max=window_max, arrival_rate=arrival_rate, extension=extension)
        return