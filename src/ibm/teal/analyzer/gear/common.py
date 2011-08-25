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

from ibm.teal.location import Location
from ibm.teal.teal_error import XMLParsingError, ConfigurationError
from ibm.teal.registry import get_service, SERVICE_LOCATION, get_logger

#GRSE = GEAR RuleSet Element
GRSE_GEAR_CTL = 'gear_control'
GRSE_EVENTS = 'events'
GRSE_CONSTANTS = 'constants'
GRSE_POOL_CTL = 'pool_control'
GRSE_ANALYZE = 'analyze'
GRSE_TEMPLATES = 'templates'
GRSE_ON_ERROR = 'on_error'

# GRUL = GEAR RULe 
GRUL_PART_AS_STRING = ['condition', 'action', 'external']
GRUL_PART_CONDITION = 0
GRUL_PART_ACTION = 1
GRUL_PART_EXTERNAL = 2

# GCFG = GEAR ConFiGuration
GCFG_RULES = 'rules'
GCFG_TRACE = 'trace'
        
def gearstr2loc(loc_str):
    ''' Take a string input and validate it and create a location '''
    if loc_str is None:
        return None
    try:
        loc_id, loc_data = loc_str.split(':', 1)
        loc_id.strip()
        loc_data.strip()
        return Location(loc_id, loc_data)
    except:
        raise XMLParsingError('Invalid location specification: {0}'.format(loc_str))
    return None

def loc2gearstr(loc):
    if loc is None:
        return 'None'
    return loc.get_id() + ':' + str(loc) 

def gearstr2scope(scope_str):
    if scope_str is None:
        return None
    try:
        scope_type, scope_data = scope_str.split(':', 1)
        scope_type.strip()
        scope_data.strip()
        if not get_service(SERVICE_LOCATION).is_scope_valid(scope_type, scope_data):
            raise XMLParsingError('Invalid scope: {0}'.format(scope_str))
    except:
        raise XMLParsingError('Invalid scope: {0}'.format(scope_str))
    return scope_type, scope_data

def scope2gearstr(scope_type, scope_data):
    return scope_type + ':' + scope_data

def trace_fmt(trace_id, msg):
    ''' Format a GEAR trace message '''
    return 'GTP[{0}]: {1}'.format(trace_id, msg)

class GearTrace(object):
    ''' This class provides the interface to allow tracing of GEAR
    '''
    
    def __init__(self, name, number=0, trace=None):
        ''' Need to know who I am and what my trace number is
        '''
        self.number = number
        self.name = name
        if trace is None:
            # No trace control specified, so use the TEAL logger
            self.tracer = get_logger()
        else:
            # TODO: Need to enhance trace support to allow target specification
            # stderr, strout, log file name 
            self.tracer = get_logger()
        return 
    
    def get_tracer(self):
        ''' Get the tracer which is a logger used for tracing '''
        return self.tracer
    
    # Helpers for the top three
    def trace_debug(self, trace_id, msg):
        ''' Debug level trace information '''
        self.get_tracer().debug('GTP[{0}]: {1}'.format(trace_id, msg))
        return
    
    def trace_info(self, trace_id, msg):
        ''' Informational level trace information '''
        self.get_tracer().info('GTP[{0}]: {1}'.format(trace_id, msg))
        return
    
    def trace_error(self, trace_id, msg):
        ''' Error level trace information '''
        self.get_tracer().error('GTP[{0}]: {1}'.format(trace_id, msg))
        return
    
    # Helpers for exceptions
    def parse_error(self, line_num, msg):
        ''' Parsing error '''
        raise XMLParsingError('Parsing failure in GEAR ruleset {0} on line {1}: {2}'.format(self.name, line_num, msg))
    
    def config_error(self, msg):
        ''' Configuration error '''
        raise ConfigurationError('Configuration failure for GEAR ruleset {0}: {1}'.format(self.name, msg))
