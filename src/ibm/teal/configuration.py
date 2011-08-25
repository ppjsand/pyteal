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

from ibm.teal.registry import get_logger
from ibm.teal.teal_error import TealError

CONFIG_EVENT_ANALYZERS = 'event_analyzer'
CONFIG_ALERT_ANALYZERS = 'alert_analyzer'
CONFIG_ALERT_FILTERS = 'alert_filter'
CONFIG_ALERT_LISTENERS = 'alert_listener'
CONFIG_EVENT_MONITORS = 'event_monitor'
CONFIG_DB_INTERFACE = 'db_interface'
CONFIG_LOCATION = 'location'
CONFIG_PACKAGE = 'package'

class ConfigurationXMLError(TealError):
    '''Exception for XML errors in configuration file '''
    pass


class Configuration(ConfigParser.ConfigParser):
    '''
    Dictionary of event metadata
    TODO: What kind of validation, if any should be done?
    '''

    def __init__(self, conf_files):
        '''
        Load the list of specified xml files
        '''
        get_logger().debug('Creating Configuration Service')
        ConfigParser.ConfigParser.__init__(self)
        self.add_files(conf_files)
        return
            
    def add_files(self, conf_files):
        '''Read in conf files one by one'''
        for the_file in conf_files:
            self.read(the_file)
        ''' process any includes '''
        includes = self.get_entries('include')
        for (section, name) in includes:
            files = self.get(section,'files').split(',')
            get_logger().debug('Processing include: {0} of files {1}'.format(name, files))
            for file in files:
                self.read(file)
            # TODO: Only supports one level of include, should we support more?
        return
    
    def get_entries(self, area):
        '''Get a list that contains tuples of entry keys and names for the specified area'''
        results = []
        for config_entry in self.sections():
            config_area, entry_name = config_entry.split('.',1)
            if config_area == area:
                results.append((config_entry, entry_name))
        return results
    
    def __repr__(self):
        '''Print out the configuration ''' 
        for section in self.sections():
            print section
            for option in self.options(section):
                print "  ", option, "=", self.get(section, option)
        return

        
    
    
        

