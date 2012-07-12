#!/usr/bin/env python
# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import sys
import re
import socket
from datetime import datetime

from ibm.teal import Teal, registry, extdata, event
from ibm.teal.database import db_interface
from ibm.teal.monitor import teal_semaphore

# Filter constants
CONFIG_AMM_TEAL = 'connector.amm'
CONFIG_EVENTID_FILTER = 'eventid_filter'

# Software Failure Event IDs
AMM_INVALID_EVENT = 'AMFFFFFFF'

# AMM External Data Format
AMM_EXTDATA_FMT = 0x414d4d0080010001

# AMM Extended Data Column Names
AMM_APP_ID = 'app_id'
AMM_SP_TXT_ID = 'sp_txt_id'
AMM_SYS_UUID = 'sys_uuid'
AMM_SYS_SERN = 'sys_sern'
AMM_APP_TYPE = 'app_type'
AMM_PRIORITY = 'priority'
AMM_MSG_TEXT = 'msg_text'
AMM_HOST_CONTACT = 'host_contact'
AMM_HOST_LOCATION = 'host_location'
AMM_BLADE_NAME = 'blade_name'
AMM_BLADE_SERN = 'blade_sern'
AMM_BLADE_UUID = 'blade_uuid'
AMM_EVT_NAME = 'evt_name'
AMM_SOURCE_ID = 'source_id'
AMM_CALL_HOME_FLAG = 'call_home_flag'
AMM_SYS_IP_ADDRESS = 'sys_ip_address'
AMM_SYS_MACHINE_MODEL = 'sys_machine_model'
AMM_BLADE_MACHINE_MODEL = 'blade_machine_model'


class AMMEvent(object):
    ''' This object is a container of all the AMM event data parsed from the received SNMP event
    '''
    def __init__(self):
        self.reset()

    def _set_value(self, value):
        ''' Helper for setting string attributes
        
        Returns None if string is empty
        '''
        if value:
            return value
        else:
            return None
        
    def reset(self):
        ''' Clear all values to reuse object again
        '''
        self._trap = None
        self._date_time = datetime.now()
        self._app_id = None
        self._sp_txt_id = None
        self._sys_uuid = None
        self._sys_sern = None
        self._app_type = None
        self._priority = None
        self._msg_text = None
        self._host_contact = None
        self._host_location = None
        self._blade_name = None
        self._blade_sern = None
        self._blade_uuid = None
        self._evt_name = None
        self._source_id = None
        self._call_home_flag = None
        self._sys_ip_address = None
        self._sys_machine_model = None
        self._blade_machine_model = None  
        
    def is_valid(self):
        ''' Verify all required fields are present
        '''
        try:
            result = (self.trap is not None)           
            result &= (self.source_id is not None)            
            result &= (self.sys_ip_address is not None)            
        except:
            result = False
            
        return result
    
    @property
    def date_time(self):
        return self._date_time
        
    @date_time.setter
    def date_time(self, value):
        ''' Set the date/time value
        If this method is not called or called with invalid data, then the timestamp defaults to "now"
        '''
        #Date(m/d/y)=01/26/12, Time(h:m:s)=17:42:59
        m = re.match(r'Date\(m/d/y\)=(\d+/\d+/\d+), *Time\(h:m:s\)=(\d+:\d+:\d+)', value)
        if m:
            try:
                self._date_time = datetime.strptime('{0} {1}'.format(m.group(1), m.group(2)), '%m/%d/%y %H:%M:%S')
            except ValueError:
                pass

    @property
    def trap(self):
        return self._trap
    
    @trap.setter
    def trap(self, value):
        m = re.match('BLADESPPALT-MIB::(.+)', value)
        if m:
            self._trap = m.group(1)
            
    @property
    def app_id(self):
        return self._app_id
    
    @app_id.setter
    def app_id(self, value):
        self._app_id = self._set_value(value)
        
    @property
    def sp_txt_id(self):
        return self._sp_txt_id
    
    @sp_txt_id.setter
    def sp_txt_id(self, value):
        self._sp_txt_id = self._set_value(value)
 
    @property
    def sys_uuid(self):
        return self._sys_uuid
    
    @sys_uuid.setter
    def sys_uuid(self, value):
        self._sys_uuid = self._set_value(value)

    @property
    def sys_sern(self):
        return self._sys_sern
    
    @sys_sern.setter
    def sys_sern(self, value):
        self._sys_sern = self._set_value(value)

    @property
    def app_type(self):
        return self._app_type

    @app_type.setter
    def app_type(self, value):
        self._app_type = int(value)

    @property
    def priority(self):
        return self._priority
        
    @priority.setter
    def priority(self, value):
        self._priority = int(value)
        
    @property
    def msg_text(self):
        return self._msg_text
        
    @msg_text.setter
    def msg_text(self, value):
        self._msg_text = self._set_value(value)
        
    @property
    def host_contact(self):
        return self._host_contact
        
    @host_contact.setter
    def host_contact(self, value):
        self._host_contact = self._set_value(value)
        
    @property
    def host_location(self):
        return self._host_location
        
    @host_location.setter
    def host_location(self, value):
        self._host_location = self._set_value(value)

    @property
    def blade_name(self):
        return self._blade_name
        
    @blade_name.setter
    def blade_name(self, value):
        self._blade_name = self._set_value(value)

    @property
    def blade_sern(self):
        return self._blade_sern
        
    @blade_sern.setter
    def blade_sern(self, value):
        self._blade_sern = self._set_value(value)
        
    @property
    def blade_uuid(self):
        return self._blade_uuid
        
    @blade_uuid.setter
    def blade_uuid(self, value):
        self._blade_uuid = self._set_value(value)
        
    @property
    def evt_name(self):
        return self._evt_name
        
    @evt_name.setter
    def evt_name(self, value):
        self._evt_name = int(value)
        
    @property
    def source_id(self):
        return self._source_id
        
    @source_id.setter
    def source_id(self, value):
        self._source_id = self._set_value(value)
        
    @property
    def call_home_flag(self):
        return self._call_home_flag
        
    @call_home_flag.setter
    def call_home_flag(self, value):
        self._call_home_flag = int(value)

    @property
    def sys_ip_address(self):
        return self._sys_ip_address
        
    @sys_ip_address.setter
    def sys_ip_address(self, value):
        self._sys_ip_address = self._set_value(value)

    @property
    def sys_machine_model(self):
        return self._sys_machine_model
        
    @sys_machine_model.setter
    def sys_machine_model(self, value):
        self._sys_machine_model = self._set_value(value)

    @property
    def blade_machine_model(self):
        return self._blade_machine_model
        
    @blade_machine_model.setter
    def blade_machine_model(self, value):
        self._blade_machine_model = self._set_value(value)
        
    def generate_event_log(self, event_lines):
        ''' Generate the event data required to log an AMM event
        
        This will return two tuples, the first one is the data for the common event structure and
        the second is for the extended data
        '''
        t = Teal(None, data_only=True, msgLevel='warn', logFile='$TEAL_LOG_DIR/tlammtraphandler.log')        
        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
                
        event_valid = self.is_valid() 
        
        # Generate the event id
        src_comp = 'AMM'
        if event_valid:
            event_id = hex(self.evt_name).upper()[2:].rjust(8,'0')
            
            # Check if this event should be reported or not
            if event_filtered(event_id):
                return
            
            time_occurred = self.date_time
            
            src_loc_type = 'D'
            try:
                src_node_address = socket.gethostbyaddr(self.sys_ip_address)[0]
            except socket.herror:
                src_node_address =  self.sys_ip_address
                  
            if (self.source_id.startswith('BLADE_')):
                tmp_loc = find_blade_name(db, self.sys_ip_address, self.source_id)
                
                # If a node was found, use that instead of the AMM address
                if (tmp_loc != self.source_id):
                    src_loc =  tmp_loc
                else:
                    # Unknown blade - report it as a subcomponent of the AMM
                    src_loc = '{0}##{1}'.format(src_node_address, self.source_id)
            else:
                src_loc = '{0}##{1}'.format(src_node_address, self.source_id)
                
            
            rpt_comp = 'AMM'
            rpt_loc_type = 'A'
            rpt_loc = src_node_address
        else:        
            event_id = AMM_INVALID_EVENT
            time_occurred = datetime.now()
            src_loc_type = 'A'
            src_loc = socket.gethostname()

            rpt_comp = None
            rpt_loc_type = None
            rpt_loc = None
        
        # Generate the extended data
        if event_valid:
            raw_data_fmt = AMM_EXTDATA_FMT
            raw_data = None
            exd = (self.app_id,
                   self.sp_txt_id,
                   self.sys_uuid,
                   self.sys_sern,
                   self.app_type,
                   self.priority,
                   self.msg_text,
                   self.host_contact,
                   self.host_location,
                   self.blade_name,
                   self.blade_sern,
                   self.blade_uuid,
                   self.evt_name,
                   self.source_id,
                   self.call_home_flag,
                   self.sys_ip_address,
                   self.sys_machine_model,
                   self.blade_machine_model)
        else:
            raw_data_fmt = 0
            raw_data = event_lines[0:2048]
            exd = None

        # Generate the common base event
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cbe = (event_id, time_occurred, src_comp, src_loc_type, src_loc, rpt_comp, rpt_loc_type, rpt_loc, raw_data_fmt, raw_data)
        db.insert(cursor,                  
                  [event.EVENT_ATTR_EVENT_ID, 
                   event.EVENT_ATTR_TIME_OCCURRED,
                   event.EVENT_ATTR_SRC_COMP,
                   event.EVENT_ATTR_SRC_LOC_TYPE,
                   event.EVENT_ATTR_SRC_LOC,
                   event.EVENT_ATTR_RPT_COMP,
                   event.EVENT_ATTR_RPT_LOC_TYPE,
                   event.EVENT_ATTR_RPT_LOC,
                   event.EVENT_ATTR_RAW_DATA_FMT,
                   event.EVENT_ATTR_RAW_DATA],
                   db_interface.TABLE_EVENT_LOG,
                   parms=cbe)

        if exd:
            db.insert_dependent(cursor,
                                event.EVENT_ATTR_REC_ID,
                                [AMM_APP_ID,
                                 AMM_SP_TXT_ID,
                                 AMM_SYS_UUID,
                                 AMM_SYS_SERN,
                                 AMM_APP_TYPE,
                                 AMM_PRIORITY,
                                 AMM_MSG_TEXT,
                                 AMM_HOST_CONTACT,
                                 AMM_HOST_LOCATION,
                                 AMM_BLADE_NAME,
                                 AMM_BLADE_SERN,
                                 AMM_BLADE_UUID,
                                 AMM_EVT_NAME,
                                 AMM_SOURCE_ID,
                                 AMM_CALL_HOME_FLAG,
                                 AMM_SYS_IP_ADDRESS,
                                 AMM_SYS_MACHINE_MODEL,
                                 AMM_BLADE_MACHINE_MODEL],
                                 extdata.extdata_fmt2table_name(AMM_EXTDATA_FMT),
                                 parms=exd)
                       
        conn.commit()
        cursor.close()
        conn.close()
        t.shutdown()
        
        # Tell TEAL that a new event has been added
        teal_semaphore.Semaphore().post()        

# SNMP line to event field
AMM_SNMP_FIELDS = \
[
    # Common between AMM and RSA 
    (re.compile(r'(ibmS|s)pTrapDateTime'), 'date_time'),
    (re.compile(r'(ibmS|s)pTrapAppId'), 'app_id'),
    (re.compile(r'(ibmS|s)pTrapSpTxtId'), 'sp_txt_id'),
    (re.compile(r'(ibmS|s)pTrapSysUuid'), 'sys_uuid'),
    (re.compile(r'(ibmS|s)pTrapSysSern'), 'sys_sern'),
    (re.compile(r'(ibmS|s)pTrapAppType'), 'app_type'),
    (re.compile(r'(ibmS|s)pTrapPriority'), 'priority'),
    (re.compile(r'(ibmS|s)pTrapMsgText'), 'msg_text'),
    (re.compile(r'(ibmS|s)pTrapHostContact'), 'host_contact'),
    (re.compile(r'(ibmS|s)pTrapHostLocation'), 'host_location'),
    
    # AMM-only fields
    (re.compile(r'spTrapBladeName'), 'blade_name'),
    (re.compile(r'spTrapBladeSern'), 'blade_sern'),
    (re.compile(r'spTrapBladeUuid'), 'blade_uuid'),
    (re.compile(r'spTrapEvtName'), 'evt_name'),
    (re.compile(r'spTrapSourceId'), 'source_id'),
    (re.compile(r'spTrapCallHomeFlag'), 'call_home_flag'),
    (re.compile(r'spTrapSysIPAddress'), 'sys_ip_address'),
    (re.compile(r'spTrapSysMachineModel'), 'sys_machine_model'),
    (re.compile(r'spTrapBladeMachineModel'), 'blade_machine_model'),
    
    # RAS-only fields 
    #(re.compile(r'ibmSpTrapSpNumId'), 'sp_num_id') ****Not Used ****
    
    # Generic Trap Info
    (re.compile(r'snmpTrapOID.0'), 'trap'),
]
        
def event_filtered(event_id):
    ''' Returns a true if the passed in event should be filtered based on information in the configuration file
    
    This function assumes that the TEAL object has already been constructed
    '''
    cfg = registry.get_service(registry.SERVICE_CONFIGURATION)
    try:
        pattern = cfg.get(CONFIG_AMM_TEAL, CONFIG_EVENTID_FILTER)
        registry.get_logger().debug('event id filter enabled: {0}'.format(pattern))
        
        if re.match(pattern, event_id) is not None:
            registry.get_logger().debug('event id {0} filtered'.format(event_id))
            return True                
    except:
        registry.get_logger().debug('No valid event id filter defined')            
    
    return False
            
def find_blade_name(dbi, mpa, blade_src):
    ''' Find the name of the affected node from the xCAT information
    
    mp table: node,mpa,id,comments,disable
    '''
    conn = dbi.get_connection()
    cur = conn.cursor()
    
    m = re.match('BLADE_(\d+)', blade_src)
    if m:
        blade_id =  m.group(1)
    
        dbi.select(cur, ['node'], 'mp', where='$id = ? AND $mpa = ?', where_fields = ['id','mpa'], parms=(blade_id, mpa))
        node = cur.fetchone()
        if node and node[0]:
            return node[0]
        else:
            return blade_src
    else:
        return blade_src
            
if __name__ == '__main__':
    amm_event = AMMEvent()
    event_lines = ''
    
    # Process the incoming SNMP event
    mib_re = re.compile('.*-MIB::(.*?)=(.*)')
    for line in sys.stdin.readlines():
        event_line = line.strip()
        if not event_line:
            continue
        else:
            event_lines += (event_line + '\n')
            
        # Parse the SNMP line for OID <-> value    
        m = mib_re.match(event_line)
        if m:
            for regx in AMM_SNMP_FIELDS:
                m_data = re.match(regx[0], m.group(1))
                if m_data:
                    setattr(amm_event, regx[1], m.group(2))
                    break

    amm_event.generate_event_log(event_lines)

    