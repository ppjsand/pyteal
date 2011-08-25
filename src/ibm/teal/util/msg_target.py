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

from abc import ABCMeta, abstractmethod

from ibm.teal.registry import get_logger

# NOTE: msg_target_logger defined after MsgTargetLogger class definition


class MsgTarget(object):
    '''
    Provide a place to write messages
    
    Idea is to allow them to either go to the logger, a screen, or 
    elsewhere
    '''
    
    __metaclass__ = ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @abstractmethod
    def debug(self, msg):
        ''' Write an debug message to the message target
        '''
        pass
     
    @abstractmethod
    def info(self, msg):
        ''' Write an info message to the message target
        '''
        pass
    
    @abstractmethod
    def warning(self, msg):
        ''' Write a warning message to the message target
        '''
        pass
    
    @abstractmethod
    def error(self, msg):
        ''' Write an error message to the message target
        '''
        pass
    
    @abstractmethod
    def exception(self, msg):
        ''' Write an exception and message to the message target 
        '''
        pass
    
    @abstractmethod
    def clear(self):
        ''' Clear the msg target (if appropriate) '''
        pass
    
class MsgTargetIgnoreMsg(MsgTarget):
    ''' Throw the messages away ''' 
    
    def __init__(self):
        return
    
    def debug(self, msg):
        return
    
    def info(self, msg):
        return
    
    def warning(self, msg):
        return
    
    def error(self, msg):
        return
    
    def exception(self, msg):
        return
    
    def clear(self):
        return
 
class MsgTargetLogger(MsgTarget):
    ''' Implementation of the Msg target that send the messages to the logger '''
    
    def __init__(self, logger=None, prefix=None):
        ''' Constructor '''
        if logger is None:
            self.logger = get_logger()
        else:
            self.logger = logger
            
        if prefix is not None:
            self.prefix = prefix
            self.debug = self.debug_PREFIX
            self.info = self.info_PREFIX
            self.warning = self.warning_PREFIX
            self.error = self.error_PREFIX
            self.exception = self.exception_PREFIX
            self.clear = self.clear_PREFIX
        return 
    
    def debug(self, msg):
        ''' Write an debug message to the specified logger
        '''
        self.logger.debug(msg)
        return
    
    def debug_PREFIX(self, msg):
        ''' Write an debug message to the specified logger
        '''
        self.logger.debug('{0}{1}'.format(self.prefix, msg))
        return
    
    def info(self, msg):
        ''' Write an info message to the specified logger
        '''
        self.logger.info(msg)
        return
    
    def info_PREFIX(self, msg):
        ''' Write an info message to the specified logger
        '''
        self.logger.info('{0}{1}'.format(self.prefix, msg))
        return
      
    def warning(self, msg):
        ''' Write a warning message to the specified logger
        '''
        self.logger.warning(msg)
        return
    
    def warning_PREFIX(self, msg):
        ''' Write a warning message to the specified logger
        '''
        self.logger.warning('{0}{1}'.format(self.prefix, msg))
        return
    
    def error(self, msg):
        ''' Write an error message to the specified logger
        '''
        self.logger.error(msg)
        return
    
    def error_PREFIX(self, msg):
        ''' Write an error message to the specified logger
        '''
        self.logger.error('{0}{1}'.format(self.prefix, msg))
        return
    
    def exception(self, msg):
        ''' Write an exception to the specified logger
        '''
        self.logger.exception(msg)
        return
    
    def exception_PREFIX(self, msg):
        ''' Write an exception to the specified logger
        '''
        self.logger.exception('{0}{1}'.format(self.prefix, msg))
        return
    
    def clear(self):
        ''' clear if appropriate 
        
        Not appropriate, but put out a debug separator '''
        get_logger().debug('--- Msg Target cleared ---')
        return
    
    def clear_PREFIX(self):
        ''' clear if appropriate 
        
        Not appropriate, but put out a debug separator '''
        get_logger().debug('{0} --- Msg Target cleared ---'.format(self.prefix))
        return

msg_target_ignore = MsgTargetIgnoreMsg()
        