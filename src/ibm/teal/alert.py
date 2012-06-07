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
from ibm.teal.constants import ALERT_LIMIT_ATTR_ALERT_ID
from ibm.teal.incident import Incident
from ibm.teal.location import Location
from ibm.teal.registry import get_logger, SERVICE_ALERT_METADATA,\
    SERVICE_LOCATION, SERVICE_ALERT_MGR
from ibm.teal.metadata import META_ALERT_MSG_TEMPLATE, META_ALERT_RECOMMENDATION, META_ALERT_SEVERITY, META_ALERT_URGENCY
from ibm.teal import registry
from ibm.teal.event import get_event_using_rec_id
from string import Template
from ibm.teal.teal_error import TealError
import json

ALERT_ATTR_REC_ID = 'rec_id'
ALERT_ATTR_ALERT_ID = 'alert_id'
ALERT_ATTR_CREATION_TIME = 'creation_time'
ALERT_ATTR_SEVERITY = 'severity'
ALERT_ATTR_URGENCY = 'urgency'
ALERT_ATTR_EVENT_LOC_OBJECT = 'event_loc_object'
ALERT_ATTR_EVENT_LOC = 'event_loc'
ALERT_ATTR_EVENT_LOC_TYPE = 'event_loc_type'
ALERT_ATTR_FRU_LOC = 'fru_loc'
ALERT_ATTR_RECOMMENDATION = 'recommendation'
ALERT_ATTR_REASON = 'reason'
ALERT_ATTR_SRC_NAME = 'src_name'
ALERT_ATTR_STATE = 'state'
ALERT_ATTR_RAW_DATA = 'raw_data'
# Not columns -- in memory attributes
ALERT_ATTR_ASSOC = 'associations'
ALERT_ATTR_MSG_TEMPLATE = 'msg_template'
ALERT_ATTR_CONDITION_EVENTS = 'condition_events'
ALERT_ATTR_SUBST_DICT = 'subst_dict'
ALERT_ATTR_PRIORITY = 'priority'

# All Columns
ALERT_COLS_SELECT = [ALERT_ATTR_REC_ID, ALERT_ATTR_ALERT_ID, ALERT_ATTR_CREATION_TIME, ALERT_ATTR_SEVERITY, \
              ALERT_ATTR_URGENCY, ALERT_ATTR_EVENT_LOC, ALERT_ATTR_EVENT_LOC_TYPE, \
              ALERT_ATTR_FRU_LOC, ALERT_ATTR_RECOMMENDATION, ALERT_ATTR_REASON, ALERT_ATTR_SRC_NAME, \
              ALERT_ATTR_STATE, ALERT_ATTR_RAW_DATA]

ALERT2EVENT_ATTR_ALERT_RECID = 'alert_recid'
ALERT2EVENT_ATTR_ASSOC_TYPE = 'assoc_type'
ALERT2EVENT_ATTR_T_EVENT_RECID = 't_event_recid'
ALERT2EVENT_ASSOC_TYPE_CONDITION = 'C'
ALERT2EVENT_ASSOC_TYPE_SUPPRESSION = 'S'

ALERT2ALERT_ATTR_ALERT_RECID = 'alert_recid'
ALERT2ALERT_ATTR_ASSOC_TYPE = 'assoc_type'
ALERT2ALERT_ATTR_T_ALERT_RECID = 't_alert_recid'
ALERT2ALERT_ASSOC_TYPE_CONDITION = 'C'
ALERT2ALERT_ASSOC_TYPE_SUPPRESSION = 'S'
ALERT2ALERT_ASSOC_TYPE_DUPLICATE = 'D'

ALERT2ALERT_COLS = [ALERT2ALERT_ATTR_ALERT_RECID, ALERT2ALERT_ATTR_ASSOC_TYPE, ALERT2ALERT_ATTR_T_ALERT_RECID]
ALERT2ALERT_TYPES = [ALERT2ALERT_ASSOC_TYPE_SUPPRESSION, ALERT2ALERT_ASSOC_TYPE_CONDITION, ALERT2ALERT_ASSOC_TYPE_DUPLICATE]
ALERT2EVENT_COLS = [ALERT2EVENT_ATTR_ALERT_RECID, ALERT2EVENT_ATTR_ASSOC_TYPE, ALERT2EVENT_ATTR_T_EVENT_RECID]
ALERT2EVENT_TYPES = [ALERT2ALERT_ASSOC_TYPE_SUPPRESSION, ALERT2EVENT_ASSOC_TYPE_CONDITION]

ALERT_STATE_AS_STRING = ['Incomplete', 'Open', 'Closed']
ALERT_STATE_INCOMPLETE = 0
ALERT_STATE_OPEN = 1
ALERT_STATE_CLOSED = 2

# These must be in priority order for duplicate checking 
ALERT_SEVERITY_VALUES = ['F','E','W','I']
ALERT_URGENCY_VALUES = ['I','S','N','D','O']

class Alert(Incident):
    '''This is the in memory version of an alert being processed by TEAL.   
       The actual data is in kept in the Alert Log table in the DB.
    '''
    
    def __init__(self, rec_id, alert_id, in_dict):
        '''Constructor
            Alerts should NOT be created directly but should be created and manipulated
            via the AlertMgr class.  Directly working with the Alert class can cause
            changes to the alert to not be persisted.
        
            This creates an in memory version of an alert.  It does not have to be
            complete or valid at this point.  Resolve and validate should be called
            to ensure completeness
                alert_id -- Required -- alert id for the alert 
                in_dict -- Optional -- other attributes of the alert
        '''
        ## Check input
        # Alert id must be specified
        if alert_id is None:
            get_logger().error('Alert constructor -- alert id is required')
            raise ValueError
        
        ## Initialize attributes
        self.alert_id = alert_id
        self.rec_id = rec_id
        self.creation_time = None
        self.event_loc = None
        self.reason = None
        self.msg_template = None
        self.recommendation = None
        self.urgency = None
        self.severity = None
        self.src_name = None
        self.state = ALERT_STATE_INCOMPLETE
        # Optional
        self.dup_alert_recid = None
        self.fru_loc = None
        self.raw_data = None
        # associations
        self.supresses = set()
        self.condition_events = set()
        self.duplicates = set()
        self.subst_dict = None
        self.priority = None

        Incident.__init__(self)

        ## Read from the dictionary
        if in_dict is not None:
            self._read_from_dictionary(in_dict)
        
        return

    def resolve_and_validate(self):
        ''' Resolve (get default values from alert metadata if needed) and validate that 
            all required fields are specified
        '''
        ## Resolve 
        # Get the metadata service 
        alert_metadata = registry.get_service(SERVICE_ALERT_METADATA)
        # Check the required values that can have a default
        if self.reason is None and self.msg_template is None:
            self.msg_template = alert_metadata[self.alert_id][META_ALERT_MSG_TEMPLATE]
        if self.recommendation is None:
            self.recommendation = alert_metadata[self.alert_id][META_ALERT_RECOMMENDATION]
        if self.urgency is None:
            self.urgency = alert_metadata[self.alert_id][META_ALERT_URGENCY]
        if self.severity is None:
            self.severity = alert_metadata[self.alert_id][META_ALERT_SEVERITY]
        # fill in the reason using the message template if not set
        if self.reason is None:
            self.reason = self.msg_template
        # Do substitutions
        tmp_template = Template(self.reason)
        self.reason = tmp_template.safe_substitute(self.event_loc.get_substitution_dict()) 
        if self.subst_dict is not None:
            tmp_template = Template(self.reason)
            self.reason = tmp_template.safe_substitute(self.subst_dict)

        ## Validate 
        # rec_id is managed by the AlertMgr so do not check here
        # alert_id was required to create so do not check here
        ## Validate that required entries are there (or get from alert metadata)
        if self.event_loc is None:
            get_logger().error('Alert validation -- event location is not set')
            raise ValueError
        if self.reason is None:
            get_logger().error('Alert validation -- reason is not set')
            raise ValueError
        if self.recommendation is None:
            get_logger().error('Alert validation -- recommendation is not set')
            raise ValueError
        if self.urgency is None:
            get_logger().error('Alert validation -- urgency is not set')
            raise ValueError
        if self.urgency not in ALERT_URGENCY_VALUES:
            get_logger().error('Alert validation -- urgency has an invalid value: {0}'.format(self.urgency))
            raise ValueError
        if self.severity is None:
            get_logger().error('Alert validation -- severity is not set')
            raise ValueError
        if self.severity not in ALERT_SEVERITY_VALUES:
            get_logger().error('Alert validation -- severity has an invalid value: {0}'.format(self.severity))
            raise ValueError
        if len(self.alert_id) > ALERT_LIMIT_ATTR_ALERT_ID:
            get_logger().error('Alert validation -- alert id is too large: {0} is {1} characters'.format(self.alert_id, len(self.alert_id)))
            print self.alert_id
            print ALERT_LIMIT_ATTR_ALERT_ID
            print len(self.alert_id)
            raise TealError(self.alert_id)
            #raise ValueError
        return
    
    def is_valid(self):
        ''' Determine if the alert is valid
        '''
        # TODO: Need code here 
        return True
            
    def get_rec_id(self):
        ''' ABC '''
        return self.rec_id
    
    def get_incident_id(self):
        '''Return as incident id for ABC'''
        return self.alert_id
    
    def get_time_occurred(self):
        '''Get the time the alert occurred
        Note same as time_logged'''
        return self.creation_time
    
    def get_time_logged(self):
        '''Get the time the alert was logged 
        Note same as time_occurred''' 
        return self.creation_time
    
    def get_type(self):
        '''Return incident type -- for debug'''
        return 'A'
    
    def am_add_suppressions(self, add_set):
        ''' Add items to suppressed set 
            This should ONLY be used via the Alert Manager'''
        self.supresses.update(add_set)
        return
    
    def am_update(self, in_dict):
        ''' Update the alert with the dictionary entries
            This should ONLY be used via the Alert Manager '''
        self._read_from_dictionary(in_dict)
        return
            
    def get_metadata(self):
        '''Get the metadata dictionary from alert metadata service'''
        metadata = registry.get_service(SERVICE_ALERT_METADATA)
        if metadata is None:
            return None
        elif self.alert_id not in metadata:
            return None
        return metadata[self.alert_id]
    
    def get_analysis_info(self, info_source):
        '''Get the analysis info via double dispatch to the info_source'''
        return info_source.get_analysis_info_alert(self)

    def __repr__(self):
        '''Detailed printout of alert info'''
        strout = self.alert_id + '(' + str(self.get_rec_id()) + ') '
        strout += str(self.get_time_occurred())
        return strout        

    def as_line(self):
        ''' return string to use as one line display '''
        outstr = '{0:5d}: {1} {2} {3}'.format(self.rec_id, self.alert_id, self.creation_time.strftime('%H:%M:%S.%f'), self.event_loc.get_location())
#        if self.raw_data is not None:
#            outstr += ' ' + self.raw_data
        return outstr    
    
    def process(self, processor, context):
        '''Send myself to the correct processor method'''
        return processor.process_alert(self, context)
    
    def _read_from_dictionary(self, in_dict):
        '''Set the attributes of Alert from information from a dictionary'''
        try:
            self.supresses.clear()
            self.condition_events.clear()
            for key in in_dict:
                value = in_dict[key]
                if key == ALERT_ATTR_ALERT_ID:
                    # Alert id is set on the allocate call only
                    # If in dictionary ignore it
                    pass
                elif key == ALERT_ATTR_CREATION_TIME:
                    self.creation_time = value
                elif key == ALERT_ATTR_SEVERITY:
                    self.severity = value
                elif key == ALERT_ATTR_URGENCY:
                    self.urgency = value
                elif key == ALERT_ATTR_EVENT_LOC:
                    try:
                        if value is not None:
                            self.event_loc = Location(in_dict[ALERT_ATTR_EVENT_LOC_TYPE],value)
                    except BaseException, e:
                        get_logger().warning('Error processing location: value is %s', (value,))
                        raise
                elif key == ALERT_ATTR_EVENT_LOC_TYPE:
                    pass # Used to build Location above
                elif key == ALERT_ATTR_EVENT_LOC_OBJECT:
                    self.event_loc = value
                elif key == ALERT_ATTR_FRU_LOC:
                    self.fru_loc = value
                elif key == ALERT_ATTR_RECOMMENDATION:
                    self.recommendation = value
                elif key == ALERT_ATTR_REASON:
                    self.reason = value
                elif key == ALERT_ATTR_SRC_NAME:
                    self.src_name = value
                elif key == ALERT_ATTR_STATE:
                    self.state = value
                elif key == ALERT_ATTR_MSG_TEMPLATE:
                    self.msg_template = value
                elif key == ALERT_ATTR_RAW_DATA:
                    self.raw_data = value
                elif key == ALERT_ATTR_ASSOC:
                    # list of strings with pattern assoc_type:target_type:rec_id
                    for item in value:
                        assoc_type, target_type, rec_id = item.split(':')
                        if target_type == 'E':
                            incident = get_event_using_rec_id(rec_id)
                        elif target_type == 'A':
                            get_logger().fatal('Assoc not suppoted YET: {0} --IGNORED'.format(item))
                        else:
                            get_logger().fatal('Assoc not supported: {0} -- IGNORED '.format(item))
                        if assoc_type == 'S':
                            self.supresses.add(incident)
                        elif assoc_type == 'C':
                            self.condition_events.add(incident)
                        else:
                            get_logger().fatal('Assoc not supported: {0} -- IGNORED'.format(item))
                elif key == ALERT_ATTR_CONDITION_EVENTS:
                    self.condition_events.update(value)
                elif key == ALERT_ATTR_SUBST_DICT:
                    self.subst_dict = value
                elif key == ALERT_ATTR_PRIORITY:
                    self.priority = value
                elif key == ALERT_ATTR_REC_ID:
                    # This can only be set directly by the AlertMgr.
                    # If it is in the dictionary ignore it
                    pass
                else:
                    get_logger().warning('Read from dictionary encountered unexpected element %s', key)
        except BaseException, e:
                print e
                get_logger().error('Read from dictionary Exception: {0}'.format(str(e)))
                raise
        return
    
    def write_to_dictionary(self):
        '''Write the attributes of Alert into a dictionary'''
        out_dict = {}
        # TODO: message template ... and all output alert journals will now be wrong ... 
        out_dict[ALERT_ATTR_REC_ID] = self.rec_id
        out_dict[ALERT_ATTR_ALERT_ID] = self.alert_id
        out_dict[ALERT_ATTR_CREATION_TIME] =  self.creation_time
        out_dict[ALERT_ATTR_SEVERITY] = self.severity
        out_dict[ALERT_ATTR_URGENCY] =  self.urgency
        # TODO: Should remove check when we validate required fields since it is req
        if self.event_loc is not None:
            out_dict[ALERT_ATTR_EVENT_LOC] =  self.event_loc.get_location()
            out_dict[ALERT_ATTR_EVENT_LOC_TYPE] =  self.event_loc.get_id() 
        if self.fru_loc is not None:
            out_dict[ALERT_ATTR_FRU_LOC] = self.fru_loc
        out_dict[ALERT_ATTR_RECOMMENDATION] = self.recommendation
        out_dict[ALERT_ATTR_REASON] = self.reason
        out_dict[ALERT_ATTR_SRC_NAME] = self.src_name
        out_dict[ALERT_ATTR_STATE] = self.state
        if self.raw_data is not None:
            out_dict[ALERT_ATTR_RAW_DATA] =  self.raw_data
        assoc_list= []
        for item in self.supresses:
            assoc_list.append('S:{0}:{1}'.format(item.get_type(),str(item.get_rec_id())))
        for item in self.condition_events:
            assoc_list.append('C:{0}:{1}'.format(item.get_type(),str(item.get_rec_id())))
        if assoc_list:
            out_dict[ALERT_ATTR_ASSOC] = assoc_list
        return out_dict
    
    def write_to_tuple(self, in_cols=ALERT_COLS_SELECT):
        '''Write the attributes of Alert into a tuple'''
        result = []
        for col in in_cols:
            if col == ALERT_ATTR_EVENT_LOC:
                result.append(self.event_loc.get_location())
            elif col == ALERT_ATTR_EVENT_LOC_TYPE:
                result.append(self.event_loc.get_id())
            elif col == ALERT_ATTR_EVENT_LOC_OBJECT:
                pass
            else:
                result.append(getattr(self,col)) 
        return tuple(result)
    
    def read_from_tuple(self, in_tup, in_cols=ALERT_COLS_SELECT ):
        ''' Read from the tuple into the specified columns
        if cols is None then all values are included and they
        are in the order of the ALERT_COLS constant
        '''
        # validate input   TODO: remove?
        if len(in_tup) != len(in_cols):
            get_logger().fatal('Alert read_from_tuple called with mismatched parms: {0} != {1}'.format(len(in_tup), len(in_cols)))
            raise ValueError()
        self.read_from_dictionary(dict(zip(in_tup,in_cols)))
        return  
    
    def get_raw_data_as_dict(self):  
        '''Get the raw data as a dictionary 
        Raw data must be in the format { "key":"value", ... }
        this must be begin the raw data string.  Any data after this will be returned in an entry
        with the key 'non_dict_raw_data'.   Note that the non-dictionary data cannot contain a }.
        '''
        return raw_data2dict(self.raw_data)
    
    def set_raw_data_from_dict(self, in_dict):   
        '''Set the raw data from a dictionary
        See get method for a description of the field
        '''
        self.raw_data = dict2raw_data(in_dict)
        return
    
    def brief_str(self): 
        ''' Shortest string that identifies this '''
        return '{0}({1})'.format(self.alert_id, self.rec_id)   

    
############
## HELPERS
def raw_data2dict(raw_data):
    ''' Convert raw data string into a dictionary
    '''
    out_dict = {}
    if raw_data and raw_data[0] == '{':
        # TODO: Should we allow the remaining data to contain a }?
        dict_str, remainder = raw_data.rsplit('}', 1)
        out_dict = json.loads(dict_str+'}')
        if remainder:
            out_dict['non_dict_raw_data'] = remainder
    else:
        out_dict['non_dict_raw_data'] = raw_data
    return out_dict

def dict2raw_data(in_dict):
    ''' Covert raw data in dictionary form into a raw data string
    '''
    # TODO: Use json to emit as well?
    t_dict = dict(in_dict)
    remainder = in_dict.get('non_dict_raw_data', None)
    if remainder is not None:
        if len(in_dict) == 1:
            return remainder
        del t_dict['non_dict_raw_data']
   
    entry_list = []  
    for key in t_dict:
        item = t_dict[key]
        entry_list.append('"{0}":"{1}"'.format(str(key),str(item)))
        
    if remainder:
        return '{{{0}}}{1}'.format(",".join(entry_list), remainder)
    return '{{{0}}}'.format(",".join(entry_list))

# TEAL ALERT ID Constants
TEAL_ALERT_ID_TEAL_STARTED = 'TL000001'
TEAL_ALERT_ID_ANALYZER_FAILURE = 'TLFFFFFF'

def create_teal_alert(alert_id, reason, raw_data, src_name='TEAL', severity='I', 
                      urgency='N', loc_instance=None, recommendation='Contact next level of support',
                      disable_dup=False):
    ''' create a TEAL alert
          This will used the parameters to:
            (1) Create the alert initialization dictionary
            (2) Allocate the alert
            (3) Commit the alert
            (4) Put the alert in the delivery queue
    '''
    get_logger().debug('Creating {0} alert'.format(src_name))
    
    # Build the Alert directly from the event information
    alert_dict = {ALERT_ATTR_SEVERITY:severity,
                  ALERT_ATTR_URGENCY:urgency,
                  ALERT_ATTR_RECOMMENDATION:recommendation,
                  ALERT_ATTR_REASON:reason,
                  ALERT_ATTR_RAW_DATA:raw_data,
                  ALERT_ATTR_SRC_NAME: src_name
                  }
        
    alert_dict[ALERT_ATTR_EVENT_LOC_OBJECT] = registry.get_service(SERVICE_LOCATION).get_teal_location(loc_instance)
    registry.get_service(SERVICE_ALERT_MGR).create_and_deliver_alert(alert_id, alert_dict, disable_dup=disable_dup)

    return