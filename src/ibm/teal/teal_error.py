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

import exceptions

from ibm.teal.registry import get_logger


class TealError(exceptions.Exception):
    '''Error occurred in Teal ... all teal generated errors should inherit from this'''
    
    def __init__(self, msg, error=True):
        '''Allow more information to be added to the Exception'''
        self.msg = msg
        if error == True:
            get_logger().error('TealError occurred: %s', str(self))
        else:
            get_logger().debug('TealError occurred: %s', str(self))
        return

    def __str__(self):
        '''Print out additional information'''
        return repr(self.msg)
    
class XMLParsingError(TealError):
    '''Could not parse XML for some reason 
    msg should describe'''
    pass

class ConfigurationError(TealError):
    '''Problem consuming the configuration file '''
    pass
    