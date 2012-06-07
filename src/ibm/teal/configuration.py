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

import ConfigParser

from ibm.teal.registry import get_logger, RUN_MODE_REALTIME, RUN_MODE_HISTORIC
from ibm.teal.teal_error import TealError, ConfigurationError

CONFIG_EVENT_ANALYZERS = 'event_analyzer'
CONFIG_ALERT_ANALYZERS = 'alert_analyzer'
CONFIG_ALERT_FILTERS = 'alert_filter'
CONFIG_ALERT_LISTENERS = 'alert_listener'
CONFIG_EVENT_MONITORS = 'event_monitor'
CONFIG_DB_INTERFACE = 'db_interface'
CONFIG_LOCATION = 'location'
CONFIG_PACKAGE = 'package'
CONFIG_ENVIRONMENT = 'environment'

class Configuration(ConfigParser.ConfigParser):
    ''' Load and manage configuration information 
    '''

    def __init__(self, conf_files):
        '''
        Load the list of specified configuration files
        '''
        get_logger().debug('Creating Configuration Service')
        ConfigParser.ConfigParser.__init__(self)
        self.optionxform = str
        self.add_files(conf_files)
            
    def add_files(self, conf_files):
        '''Read in conf files one by one'''
        for the_file in conf_files:
            get_logger().debug('Loading configuration from {0}'.format(the_file))
            self.read(the_file)
        # process any includes -- only supports one level of includes
        includes = self.get_active_sections('include', 'all', name_required=False, singleton=False)
        for (section, name) in includes:
            files = self.get(section,'files').split(',')
            get_logger().debug('Processing include: {0} of files {1}'.format(name, files))
            for inc_file in files:
                self.read(inc_file)
    
    def get_active_sections(self, area, runmode=None, name_required=True, singleton=False):
        '''Get a list that contains tuples of active section key and names for the specified area
        '''
        results = []
        for section in self.sections():
            # split into config_area and entry_name
            result = section.split('.',1)
            if result[0] == area:
                if runmode is not None and self.has_option(section, 'enabled'):
                    enabled_val = self.get(section, 'enabled')
                    if enabled_val != 'all':
                        if  enabled_val == 'false' or                                                    \
                            (enabled_val == 'realtime' and runmode != RUN_MODE_REALTIME) or                  \
                            (enabled_val == 'historic' and runmode != RUN_MODE_HISTORIC):
                            get_logger().debug('Skipping section \'{0}\' with enabled set to \'{1}\''.format(section, enabled_val))
                            continue
                        elif enabled_val not in ['realtime', 'historic']:
                            raise ConfigurationError('Configuration section \'{0}\' has an unrecognized value for enabled keyword: \'{1}\''.format(section, enabled_val))
                            
                if len(result) == 1:
                    if name_required == True:
                        raise ConfigurationError('Configuration sections for \'{0}\' must have a name, but none was specified'.format(area))
                    result.append(None)
                    
                if singleton == True and len(results) == 1:
                    raise ConfigurationError('There can only be one section called \'{0}\''.format(area))
                
                results.append((section,result[1]))
        results.sort()
        return results
    
    def __str__(self):
        '''Print out the configuration 
        ''' 
        outstr = ''
        for section in self.sections():
            outstr += '[{0}]\n'.format(section)
            for option in self.options(section):
                outstr += '{0} = {1}\n'.format(option, self.get(section, option))
        return outstr
