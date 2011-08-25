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

from datetime import datetime
from ibm.teal.registry import get_logger, get_service, SERVICE_EVENT_Q
from ibm.teal.processable import Processable

CONTROL_MSG_TYPE_AS_STRING = ['End of Events', 'Flush']
CONTROL_MSG_TYPE_END_OF_DATA = 0
CONTROL_MSG_TYPE_FLUSH = 1

CONTROL_MSG_ATTR_MSG_TYPE = 'msg_type'
CONTROL_MSG_ATTR_CREATION_TIME = 'creation_time'

class ControlMsg(Processable):
    '''This is the in memory version of an alert being processed by teal.   
    
    The actual data is in kept in the Alert Log table in the DB.
    
    '''

    def __init__(self, msg_type=None, in_dict=None):
        '''Constructor
             msg_type -- the type of control message
             in_dict -- dictionary to initialize with
        '''
        self.msg_type = msg_type
        self.creation_time = datetime.now()
        if in_dict is not None:
            self.read_from_dictionary(in_dict)
        if self.msg_type is None:
            get_logger().error('Message type was not set')
            raise ValueError
        return
    
    def process(self, processor, context):
        '''Processable: double dispatch back to specific process method'''
        return processor.process_control_msg(self, context)
        
    def __str__(self):
        outstr = 'Control Msg: ' + CONTROL_MSG_TYPE_AS_STRING[int(self.msg_type)]
        return outstr
    
    def brief_str(self):
        ''' Brief as possible string '''
        return CONTROL_MSG_TYPE_AS_STRING[int(self.msg_type)]


    def is_valid(self):
        '''Determine if valid control message'''
        if self.msg_type == None:
            return False
        return True

    def read_from_dictionary(self, in_dict):
        '''Set the attributes of Event from information from a dictionary'''
        try:
            for key in in_dict:
                value = in_dict[key]
                if key == CONTROL_MSG_ATTR_MSG_TYPE:
                    self.msg_type = value
                elif key == CONTROL_MSG_ATTR_CREATION_TIME:
                    self.creation_time = value
                else:
                    get_logger().warning('Read from dictionary encountered unexpected element {0}'.format(key))
        except BaseException, e:
            get_logger().error('Read from dictionary Exception: {0}'.format(str(e)))
            return
        return
    
    def write_to_dictionary(self):
        '''Write the attributes of Event into a dictionary'''
        out_dict = {}
        out_dict[CONTROL_MSG_ATTR_MSG_TYPE] = self.msg_type
        out_dict[CONTROL_MSG_ATTR_CREATION_TIME] = self.creation_time
        return out_dict

    def as_line(self):
        ''' return string to use as one line display '''
        outstr = 'Control Msg:' + CONTROL_MSG_TYPE_AS_STRING[self.msg_type]
        return outstr     
    
    
# Helper methods
def inject_flush_control_msg(create_time=None):
    ''' Inject a flush message '''
    if create_time is None:
        create_time = datetime.now()
    get_service(SERVICE_EVENT_Q).put_nowait(ControlMsg(CONTROL_MSG_TYPE_FLUSH, {CONTROL_MSG_ATTR_CREATION_TIME: create_time}))
    return
