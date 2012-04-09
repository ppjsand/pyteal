# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
from ibm.teal import registry
from ibm.teal.constants import EVENT_LIMIT_ATTR_EVENT_ID
from ibm.teal.database import db_interface
from ibm.teal.extdata import ExtensionData, EXT_DATA_RAW_DATA
from ibm.teal.incident import Incident
from ibm.teal.location import Location
from ibm.teal.registry import get_logger, get_service, SERVICE_EVENT_METADATA,\
    SERVICE_DB_INTERFACE
import ast

EVENT_ATTR_REC_ID = 'rec_id'
EVENT_ATTR_EVENT_ID = 'event_id'
EVENT_ATTR_TIME_OCCURRED = 'time_occurred'
EVENT_ATTR_TIME_LOGGED = 'time_logged'
EVENT_ATTR_SRC_COMP = 'src_comp'
EVENT_ATTR_SRC_LOC = 'src_loc'
EVENT_ATTR_SRC_LOC_TYPE = 'src_loc_type'
EVENT_ATTR_RPT_COMP = 'rpt_comp'
EVENT_ATTR_RPT_LOC = 'rpt_loc'
EVENT_ATTR_RPT_LOC_TYPE = 'rpt_loc_type'
EVENT_ATTR_EVENT_CNT = 'event_cnt'
EVENT_ATTR_ELAPSED_TIME = 'elapsed_time'
EVENT_ATTR_RAW_DATA_FMT = 'raw_data_fmt'
EVENT_ATTR_RAW_DATA = 'raw_data'

EVENT_COLS = [EVENT_ATTR_REC_ID, EVENT_ATTR_EVENT_ID, EVENT_ATTR_TIME_OCCURRED,
              EVENT_ATTR_TIME_LOGGED, EVENT_ATTR_SRC_COMP, EVENT_ATTR_SRC_LOC,
              EVENT_ATTR_SRC_LOC_TYPE, EVENT_ATTR_RPT_COMP, EVENT_ATTR_RPT_LOC,
              EVENT_ATTR_RPT_LOC_TYPE, EVENT_ATTR_EVENT_CNT, EVENT_ATTR_ELAPSED_TIME,
              EVENT_ATTR_RAW_DATA_FMT, EVENT_ATTR_RAW_DATA ]

# Static methods
def get_event_using_rec_id(rec_id):
    ''' This method creates an in memory version of an event from the DB using the
    pass rec_id '''
    get_logger().debug('Loading (selecting) event from table for event with rec_id = {0}'.format(rec_id))
    dbi = get_service(SERVICE_DB_INTERFACE)
    event_cnxn = dbi.get_connection()
    cursor = event_cnxn.cursor()
    dbi.select(cursor, EVENT_COLS, db_interface.TABLE_EVENT_LOG, where='$rec_id = ?', where_fields=['rec_id'], parms=(rec_id))
    row = cursor.fetchone()
    #print 'row',row
    if row is None:
        get_logger().fatal('Table did not cotains an entry for event with rec_id = {0}'.format(rec_id))
        raise ValueError
    result_event = Event.fromDB(row)
    event_cnxn.close()
    return result_event         


class Event(Incident):
    '''This is the in memory version of an event being processed by teal.   
    
    The actual data is in kept in the Event Log table
    in the DB.
    
    Currently changes made to instances of this class are NOT
    reflected back into the DB
    '''
    
    @classmethod
    def fromDB(cls, in_tuple):
        ''' Create Event using DB row (tuple) ''' 
        new_obj = cls()
        try:
            new_obj.rec_id = in_tuple[0]
            new_obj.event_id = in_tuple[1].strip()
            new_obj.time_occurred = in_tuple[2]
            new_obj.time_logged = in_tuple[3]
            new_obj.src_comp = in_tuple[4].strip()
            try:
                new_obj.src_loc = Location(in_tuple[6].strip(), in_tuple[5].strip())
            except:
                get_logger().exception('source location could not be created from Event DB tuple {0}'
                                     .format(str(in_tuple)))
                new_obj.src_loc = None
            # Optional attributes
            if in_tuple[7] is None:
                new_obj.rpt_comp = None
            else:
                new_obj.rpt_comp = in_tuple[7].strip()
            if in_tuple[9] is None or in_tuple[8] is None:
                new_obj.rpt_loc = None
            else:
                try:
                    new_obj.rpt_loc = Location(in_tuple[9].strip(), in_tuple[8].strip())
                except:
                    get_logger().exception('source location could not be created from Event DB tuple {0}'
                                             .format(str(in_tuple)))
                    new_obj.rpt_loc = None 
            new_obj.event_cnt = in_tuple[10]
            new_obj.elapsed_time = in_tuple[11]
            new_obj.ext_key = None
            new_obj.raw_data_fmt = in_tuple[12]
            try:
                new_obj.raw_data = new_obj.raw_data = ExtensionData(new_obj.raw_data_fmt, new_obj.rec_id, in_tuple[13])
            except:
                get_logger().exception('Raw Data could not be created from Event DB tuple {0}'
                                              .format(str(in_tuple)))
                new_obj.raw_data = None 
        except:
            get_logger().exception('creation with DB tuple failed for event {0}'.format(str(in_tuple)))
        get_logger().debug('Created an event for rec_id {0}'.format(str(new_obj.rec_id)))
        return new_obj
    
    @classmethod
    def fromDict(cls, in_dict):
        new_obj = cls()
        # Required attributes
        new_obj.rec_id = None
        new_obj.event_id = None
        new_obj.time_occurred = None
        new_obj.time_logged = None
        new_obj.src_comp = None
        new_obj.src_loc = None
        # Optional attributes
        new_obj.rpt_comp = None
        new_obj.rpt_loc = None
        new_obj.event_cnt = None
        new_obj.elapsed_time = None
        new_obj.ext_key = None
        new_obj.raw_data_fmt = None
        new_obj.raw_data = None
        
        try:
            for key in in_dict:
                value = in_dict[key]
                if key == EVENT_ATTR_TIME_OCCURRED:
                    new_obj.time_occurred = value
                elif key == EVENT_ATTR_TIME_LOGGED:
                    new_obj.time_logged = value 
                elif key == EVENT_ATTR_EVENT_ID:
                    new_obj.event_id = value
                elif key == EVENT_ATTR_SRC_COMP:
                    new_obj.src_comp = value
                elif key == EVENT_ATTR_SRC_LOC:
                    try:
                        new_obj.src_loc = Location(in_dict[EVENT_ATTR_SRC_LOC_TYPE],value)
                    except:
                        get_logger().exception('source location could not be created from event dict {0}. value {1}'
                                             .format(new_obj._dump_event_info(in_dict),value))
                elif key == EVENT_ATTR_SRC_LOC_TYPE:
                    pass # Value is used to create the source location
                elif key == EVENT_ATTR_RPT_COMP:
                    new_obj.rpt_comp = value
                elif key == EVENT_ATTR_RPT_LOC:
                    if value is not None:
                        try:
                            new_obj.rpt_loc = Location(in_dict[EVENT_ATTR_RPT_LOC_TYPE],value)
                        except:
                            get_logger().exception('reporting location could not be created from event dict {0}.  value {1}'
                                                  .format(new_obj._dump_event_info(in_dict),value))
                    else:
                        new_obj.rpt_loc = None
                elif key == EVENT_ATTR_RPT_LOC_TYPE:
                    pass # Value is used to create the reporting location 
                elif key == EVENT_ATTR_EVENT_CNT:
                    new_obj.event_cnt = value
                elif key == EVENT_ATTR_ELAPSED_TIME:
                    new_obj.elapsed_time = value
                elif key == EVENT_ATTR_RAW_DATA_FMT:
                    raw_data = in_dict.get(EVENT_ATTR_RAW_DATA, None)
                    ext_key = in_dict.get(EVENT_ATTR_REC_ID, new_obj.rec_id)
                    if (raw_data is not None or ext_key is not None):
                        try:
                            if isinstance(raw_data, dict):
                                new_obj.raw_data = ExtensionData(value, ext_key, None, raw_data)
                            else:
                                if raw_data is not None and raw_data[:1] == '{':
                                    tmp_dict = ast.literal_eval(raw_data)
                                    new_obj.raw_data = ExtensionData(value, ext_key, None, tmp_dict)
                                else:
                                    new_obj.raw_data = ExtensionData(value, ext_key, raw_data)
                        except:
                            get_logger().exception('Raw Data could not be created from event dict {0}'
                                                  .format(new_obj._dump_event_info(in_dict)))
                    else:
                        raise ValueError, 'Raw data format specified without raw data or extension key for event {0}'.format(new_obj._dump_event_info(in_dict))
                elif key == EVENT_ATTR_RAW_DATA:
                    pass # Value used to create extension data
                elif key == EVENT_ATTR_REC_ID:
                    new_obj.rec_id = value
                else:
                    get_logger().warning('Read from dictionary from event dict (0) encountered unexpected element {1}'
                                          .format(new_obj._dump_event_info(in_dict),value))
        except:
            get_logger().exception('Read event from dictionary failed for event {0}'.format(new_obj._dump_event_info(in_dict)))
        
        get_logger().debug('Created an event for rec_id {0}'.format(str(new_obj.rec_id)))
        return new_obj

    def __init__(self):
        '''Constructor
             rec_id -- a unique id (the primary key)
             in_dict -- a dictionary of all attributes for the Event
             
        '''
        get_logger().debug('Creating an event')
        Incident.__init__(self)
        return
    
    def _dump_event_info(self, in_dict):
        ''' Get the event id and rec id info from the dict ... if available and build a 
            printable string '''
        out_str = '-unknown-'
        try:
            if self.event_id is not None:
                out_str = self.event_id
            else:
                if EVENT_ATTR_EVENT_ID in in_dict:
                    if in_dict[EVENT_ATTR_EVENT_ID] is not None:
                        out_str = in_dict[EVENT_ATTR_EVENT_ID]
                    
            if self.rec_id is not None:
                out_str += '({0})'.format(self.rec_id)
            else: 
                if EVENT_ATTR_EVENT_ID in in_dict:
                    if in_dict[EVENT_ATTR_REC_ID] is not None:
                        out_str += '({0})'.format(in_dict[EVENT_ATTR_REC_ID])
        except:
            pass
        
        return out_str
    
    def write_to_dictionary(self, as_objects=True):
        '''Write the attributes of Event into a dictionary'''
        out_dict = {}
        out_dict[EVENT_ATTR_REC_ID] = self.get_rec_id()
        out_dict[EVENT_ATTR_EVENT_ID] = self.get_event_id()
        out_dict[EVENT_ATTR_TIME_OCCURRED] =  self.get_time_occurred()
        out_dict[EVENT_ATTR_TIME_LOGGED] = self.get_time_logged()
        out_dict[EVENT_ATTR_SRC_COMP] =  self.get_src_comp()
        out_dict[EVENT_ATTR_SRC_LOC] =  self.get_src_loc().get_location()
        out_dict[EVENT_ATTR_SRC_LOC_TYPE] =  self.get_src_loc().get_id() 
        if self.rpt_comp is not None:
            out_dict[EVENT_ATTR_RPT_COMP] = self.get_rpt_comp()
            out_dict[EVENT_ATTR_RPT_LOC] = self.get_rpt_loc().get_location()
            out_dict[EVENT_ATTR_RPT_LOC_TYPE] = self.get_rpt_loc().get_id()
        if self.event_cnt is not None:
            out_dict[EVENT_ATTR_EVENT_CNT] =  self.get_event_cnt()
        if self.raw_data is not None:
            tmp_raw_data = self.raw_data
            #print 'HERE HERE HERE ', tmp_raw_data
            #print type(tmp_raw_data)
            if isinstance(tmp_raw_data, ExtensionData):
                #print 'ExtensionData'
                if as_objects == True:
                    out_dict[EVENT_ATTR_RAW_DATA] = tmp_raw_data.write_to_dictionary()
                else:
                    out_dict[EVENT_ATTR_RAW_DATA] = str(tmp_raw_data.write_to_dictionary())
            else:
                #print 'Not ExtensionData'
                out_dict[EVENT_ATTR_RAW_DATA] = tmp_raw_data

            fmt = self.get_raw_data_fmt()
            if (fmt is not None):
                out_dict[EVENT_ATTR_RAW_DATA_FMT] = self.get_raw_data_fmt()
                
        if self.elapsed_time is not None:
            out_dict[EVENT_ATTR_ELAPSED_TIME] = self.get_elapsed_time()
        return out_dict
        
    def write_to_tuple(self, in_cols=EVENT_COLS):
        '''Write the attributes of Alert into a tuple'''
        result = []
        for col in in_cols:
            if col == EVENT_ATTR_SRC_LOC:
                result.append(self.src_loc.get_location())
            elif col == EVENT_ATTR_SRC_LOC_TYPE:
                result.append(self.src_loc.get_id())
            elif col == EVENT_ATTR_RPT_LOC:
                result.append(self.rpt_loc.get_location())
            elif col == EVENT_ATTR_RPT_LOC_TYPE:
                result.append(self.rpt_loc.get_id())
            elif col == EVENT_ATTR_RAW_DATA:
                result.append(self.raw_data[EXT_DATA_RAW_DATA])
            else:
                result.append(getattr(self,col)) 
        return tuple(result)
    
    def is_valid(self):
        '''Check if the event has values for all of the required attributes'''
        # Check for required 
        if self.event_id is None:
            get_logger().debug('Missing event id')
            return False
        if self.time_occurred is None:
            get_logger().debug('Missing time occurred')
            return False
        if self.src_comp is None:
            get_logger().debug('Missing source component')
            return False
        if self.src_loc is None:
            get_logger().debug('Missing source location')
            return False
        if self.time_logged is None:
            get_logger().debug('Missing time logged')
            return False
        if (((self.rpt_comp is not None) and (self.rpt_loc is None)) or
            ((self.rpt_comp is None) and (self.rpt_loc is not None))):
            get_logger().debug('Missing full reporting component information')
            return False
        if len(self.event_id) > EVENT_LIMIT_ATTR_EVENT_ID:
            get_logger().debug('Event id is too long: {0} is {1} characters'.format(self.event_id,len(self.event_id)))
            return False
        return True
        
    def get_rec_id(self):
        '''Get the rec id
        
             Provided so that implementation can be changed'''
        return self.rec_id
    
    def get_event_id(self):
        '''Get the event id
        
             Provided so that implementation can be changed'''
        return self.event_id
    
    def get_incident_id(self):
        '''Return as incident id for incident ABC'''
        return self.event_id
    
    def get_time_occurred(self):
        '''Get the time the event occurred
        
             Provided so that implementation can be changed'''
        return self.time_occurred
    
    def get_time_logged(self):
        ''' Get the time the event was logged (added to event log) '''
        return self.time_logged
    
    def get_src_comp(self):
        ''' Get the source component '''
        return self.src_comp
    
    def get_src_loc(self):
        ''' Get the source location '''
        return self.src_loc
    
    def get_src_loc_id(self):
        ''' Get the source location type '''
        return self.src_loc.get_id()
    
    def get_rpt_comp(self):
        ''' get the reporting component'''
        return self.rpt_comp
    
    def get_rpt_loc(self):
        '''Get the reporting location'''
        return self.rpt_loc
    
    def get_rpt_loc_id(self):
        '''Get the reporting location type'''
        return self.rpt_loc.get_id()
    
    def get_event_cnt(self):
        '''Get the event count -- when event represents multiple events'''
        return self.event_cnt
    
    def get_elapsed_time(self):
        '''Get the elapsed time for the multiple events'''
        return self.elapsed_time
    
    def get_ext_key(self):
        return self.raw_data.get_ext_key()
    
    def get_raw_data(self):
        '''Get the raw data '''
        return self.raw_data[EXT_DATA_RAW_DATA]

    def get_raw_data_fmt(self):
        '''Get the raw data format'''
        return self.raw_data.get_format()

    def process(self, processor, context):
        '''Send myself to the correct processor method'''
        return processor.process_event(self, context)
                 
    def get_type(self):
        '''Return incident type -- for debug'''
        return 'E'
    
    def get_metadata(self):
        '''Helper to get the metadata for this event's event id'''
        metadata = registry.get_service(SERVICE_EVENT_METADATA)
        # TODO: Just try/except and return None
        key = (self.get_src_comp(), self.get_event_id())
        if metadata is None:
            return None
        elif key not in metadata:
            return None
        return metadata[key]
    
    def get_analysis_info(self, info_source):
        '''Get the analysis info via double dispatch to the info_source'''
        return info_source.get_analysis_info_event(self)

    def as_line(self):
        ''' return string to use as one line display '''
        outstr = str(self.rec_id) + ':' + self.event_id + ' ' + self.time_occurred.strftime('%H:%M:%S')
        if self.raw_data is not None:
            outstr += ' RW:' + self.raw_data
        return outstr  
    
    def brief_str(self): 
        ''' Shortest string that identifies this '''
        return '{0} {1}({2})'.format(self.src_comp, self.event_id, self.rec_id)   

    def match(self, event_id, src_comp, src_loc, rpt_loc, scope):
        '''check if the event matches the passed in values
        
        A None passed in means wildcard ... i.e. assume it matches
        '''
        try:
            if event_id is not None and event_id != self.get_event_id():
                #get_logger().debug('Match failed due to event id mismatch {0} != {1}'.format(event_id, self.get_event_id()))
                return False
            if src_comp is not None and src_comp != self.get_src_comp():
                #get_logger().debug('Match failed due to comp mismatch {0} != {1}'.format(src_comp, self.get_src_comp()))
                return False
            if src_loc is not None:
                if not src_loc.match(self.get_src_loc(), scope):
                    #get_logger().debug('Match failed due to src_loc mismatch {0} != {1}'.format(str(src_loc), str(self.get_src_loc())))
                    return False
            if rpt_loc is not None:
                if self.get_rpt_loc() is None:
                    #get_logger().debug('Match failed due to event not having rpt_loc value')
                    return False
                if not rpt_loc.match(self.get_rpt_loc(), scope):
                    #get_logger().debug('Match failed due to rpt_loc mismatch {0} != {1}'.format(str(rpt_loc), str(self.get_rpt_loc())))
                    return False
        except BaseException:
            get_logger().exception('Event {0}: Match failed'.format(self.brief_str()))
            return False
        #get_logger().debug('Matched')
        return True

        
