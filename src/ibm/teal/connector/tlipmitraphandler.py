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
import os
import socket
import struct
from datetime import datetime, timedelta

from ibm.teal import registry
from ibm.teal import event
from ibm.teal import extdata
from ibm.teal.teal import Teal
from ibm.teal.database import db_interface
from ibm.teal.registry import get_logger
from ibm.teal.monitor import teal_semaphore

# Sample BMC event
#host=imm2
#ip=UDP: [10.0.0.2]:46213
#DISMAN-EVENT-MIB::sysUpTimeInstance=27:20:18:09.17
#SNMPv2-MIB::snmpTrapOID.0=SNMPv2-SMI::enterprises.3183.1.1.0.814848
#decodedipmialert=INFORMATION: Memory, Correctable ECC Memory module 255 (Sensor 0x53)
#SNMPv2-SMI::enterprises.3183.1.1.1=E7 EB 93 8E 07 4D 11 E1 A5 6C 5C F3 FC 30 46 24  00 53 1A FD 41 F6 FF FF 20 20 02 81 53 00 00 00  FF FF 00 00 00 00 00 19 00 00 4F 4D 01 61 C1
#SNMP-COMMUNITY-MIB::snmpTrapAddress.0=10.0.0.2
#SNMP-COMMUNITY-MIB::snmpTrapCommunity.0=public
#SNMPv2-MIB::snmpTrapEnterprise.0=SNMPv2-SMI::enterprises.3183.1.1

# Filter constants
CONFIG_IPMI_TEAL = 'connector.ipmi'
CONFIG_EVENTID_FILTER = 'eventid_filter'

# Extended data format
IPMI_EXTDATA_FMT = 0x49504d4980010001

# IPMI Software Errors
IPMI_INVALID_EVENT = 'IIFFFFFF'
IPMI_INVALID_EVENT_ID = 'IIFFFFFE'
IPMI_INVALID_LOCATION = 'IIFFFFFD'

# Offsets in event data tuple
IPMI_GUID = 0
IPMI_SEQ = 1
IPMI_TIMESTAMP = 2
IPMI_UTC_OFF = 3
IPMI_TRAP_SOURCE = 4
IPMI_EVENT_SOURCE = 5
IPMI_SEVERITY = 6
IPMI_SENSOR_DEVICE = 7
IPMI_SENSOR_NUM = 8
IPMI_ENTITY = 9
IPMI_ENTITY_INSTANCE = 10
IPMI_EVENT_DATA = 11
IPMI_LANGUAGE_CODE = 19
IPMI_MFG_ID = 20
IPMI_SYSTEM_ID = 21

# IPMI Extended Data Column Names
IPMI_EVENT_GUID = 'guid'
IPMI_EVENT_SEQ = 'sequence'
IPMI_EVENT_TIMESTAMP = 'time_occurred'
IPMI_EVENT_UTC_OFF = 'utc_offset'
IPMI_EVENT_TRAP_SOURCE = 'trap_src'
IPMI_EVENT_EVENT_SOURCE = 'event_src'
IPMI_EVENT_SEVERITY = 'severity'
IPMI_EVENT_SENSOR_DEVICE = 'sensor_dev'
IPMI_EVENT_SENSOR_NUM = 'sensor_num'
IPMI_EVENT_ENTITY = 'entity'
IPMI_EVENT_ENTITY_INSTANCE = 'entity_inst'
IPMI_EVENT_EVENT_DATA1 = 'event_data1'
IPMI_EVENT_EVENT_DATA2 = 'event_data2'
IPMI_EVENT_EVENT_DATA3 = 'event_data3'
IPMI_EVENT_EVENT_DATA4 = 'event_data4'
IPMI_EVENT_EVENT_DATA5 = 'event_data5'
IPMI_EVENT_EVENT_DATA6 = 'event_data6'
IPMI_EVENT_EVENT_DATA7 = 'event_data7'
IPMI_EVENT_EVENT_DATA8 = 'event_data8'
IPMI_EVENT_LANGUAGE_CODE = 'lang_code'
IMPI_EVENT_MFG_ID = 'mfg_id'
IPMI_EVENT_SYSTEM_ID = 'sys_id'
IPMI_EVENT_MSG = 'message'

def event_filtered(event_id):
    ''' Returns a true if the passed in event should be filtered based on information in the configuration file
    
    This function assumes that the TEAL object has already been constructed
    '''
    cfg = registry.get_service(registry.SERVICE_CONFIGURATION)
    try:
        pattern = cfg.get(CONFIG_IPMI_TEAL, CONFIG_EVENTID_FILTER)
        registry.get_logger().debug('event id filter enabled: {0}'.format(pattern))
        
        if re.match(pattern, event_id) is not None:
            registry.get_logger().debug('event id {0} filtered'.format(event_id))
            return True                
    except:
        registry.get_logger().debug('No valid event id filter defined')            
    
    return False

def find_location(imm):
    ''' Translate the IMM IP address to a node address if possible using the ipmi xCAT tables
    '''
    try:
        imm_ip = socket.gethostbyname(imm)
        db.select(cursor,['node'],'ipmi',where='$bmc in (?,?)', where_fields=['bmc'],parms=(imm,imm_ip))
    
        # Assuming bmc (ip or name) maps to exactly one node
        row = cursor.fetchone()
        if row and row[0]:
            node = row[0]
        else:
            node = imm
    except:
        node = imm
        
    return node

def parse_event_data(data_str):
    ''' Parse the IPMI event data into its constituent parts.
    
        To remain generic, the OEM data is not retrieved or stored
    '''
    # Remove all spaces so there are just digits
    event_data_str = data_str.replace(' ', '')
    
    # Event data cannot be trusted if not correct length or not divisible by 2
    event_data_len = len(event_data_str)
    if (((event_data_len % 2) != 0) or (event_data_len < 47*2)):
        return None

    # Translate every two characters into a byte
    event_data_list = [int(event_data_str[i:i+2],16) for i in range(0,len(event_data_str),2)]
    
    # Pull out only the fixed data
    event_fixed_list = event_data_list[0:46]
    
    # Parse that data into its actual values
    event_fixed_struct = struct.pack('B'*46,*event_fixed_list)     
    event_fixed_tmp = struct.unpack('>2QHLh16BLH',event_fixed_struct)
    
    # Put the fixed data
    event_data = [hex(event_fixed_tmp[0])[2:-1].upper() + hex(event_fixed_tmp[1])[2:-1].upper()]   # GUID
    event_data.extend(event_fixed_tmp[2:])
    
    # Return the parsed tuple of event data
    return event_data
    
    
if __name__ == '__main__':
    t = Teal(None, data_only=True, msgLevel='warn', logFile='$TEAL_LOG_DIR/tlipmitraphandler.log')
             
    # Location information
    event_location_regx = re.compile('host=(.+)')
    event_alt_location_regx = re.compile('ip=.*\[(.+)\]:.*')
    
    # Event message
    event_msg_regx = re.compile(' *decodedipmialert=(.*)')
    
    # Event data details
    event_data_regx = re.compile(' *SNMPv2-SMI::enterprises.3183.1.1.1=(.*)')
    
    # Event ID based on trap id
    event_id_regx = re.compile(' *SNMPv2-MIB::snmpTrapOID.0=SNMPv2-SMI::enterprises.3183.1.1.0.([0-9]+)')
    
    # Default event information
    event_lines = ''
    event_id = None
    event_msg = None
    event_data = None
    event_location = None
    event_alt_location = None
    
    # Parse out the event information
    for line in sys.stdin.readlines():
        event_line = line.strip()
        if not event_line:
            continue
        else:
            # Save the event for logging
            event_lines += (event_line + '\n')
            
        m = event_location_regx.match(event_line)
        if m:
            event_location = m.group(1).strip()
            continue
        
        m = event_alt_location_regx.match(event_line)
        if m:
            event_alt_location = m.group(1).strip()
            continue
        
        m = event_msg_regx.match(event_line)
        if m:
            event_msg = m.group(1).strip()
            continue
    
        m =  event_data_regx.match(event_line)
        if m:
            event_data = parse_event_data(m.group(1))
            continue
    
        m = event_id_regx.match(event_line)
        if m:
            event_id_int = int(m.group(1))
            
            # Event ID is outside of expected range
            if event_id_int > 0x00FFFFFF:
                event_id = IPMI_INVALID_EVENT_ID
                get_logger().warn('Invalid event id reported: {0}'.format(event_id_int))
            else:
                # Valid event id
                event_id = 'II{0:0>6}'.format(hex(event_id_int).upper()[2:])
            continue

    # Unexpected SNMP event received
    if event_id is None:
        event_id = IPMI_INVALID_EVENT
        event_data = None # Log the event lines with the error
        event_location = socket.gethostname()
    elif event_filtered(event_id):
        # No processing of filtered events
        sys.exit()
    else:
        # Continue processing the new event
        pass

    # Extract the timestamp of the event
    if event_data and (event_data[IPMI_TIMESTAMP] != 0):
        # Timestamp is local time as number of seconds since 1/1/1998
        event_time = datetime(year=1998,month=1,day=1) + timedelta(seconds=event_data[IPMI_TIMESTAMP])
    else:
        event_time = datetime.now()
    
    # Generate the source location    
    src_comp = 'IPMI'    
    src_loc_type = 'D'

    db = registry.get_service(registry.SERVICE_DB_INTERFACE)
    conn = db.get_connection()
    cursor = conn.cursor()

    if event_location and (event_location != '<UNKNOWN>'):
        src_loc = find_location(event_location)
    elif event_alt_location:
        try:
            src_loc = socket.gethostbyaddr(event_alt_location)[0]
        except:
            src_loc = event_alt_location
    else:
        src_loc = socket.gethostname()
        event_id = IPMI_INVALID_LOCATION
        get_logger().warn('No location found for event {0} reported on {1}'.format(event_id, event_time))
    
    # Generate the reporting location
    rpt_comp = 'TEAL'
    rpt_loc_type = 'A'
    rpt_loc = '{0}##{1}##{2}'.format(socket.gethostname(), os.path.basename(sys.argv[0]), os.getpid())

    # Log the base event information
    if event_data:
        event_data_fmt = IPMI_EXTDATA_FMT
        raw_data = None
        event_data.append(event_msg)
    else:
        event_data_fmt = 0
        raw_data = event_lines[0:2048]
    
    #print event_id,event_time,src_loc_type,':',src_loc,rpt_loc_type,":",rpt_loc,event_msg    
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
               (event_id,
                event_time,
                src_comp,
                src_loc_type,
                src_loc,
                rpt_comp,
                rpt_loc_type,
                rpt_loc,
                event_data_fmt,
                raw_data))
    
    # Log the additional event information
    if event_data:
        db.insert_dependent(cursor,
                            event.EVENT_ATTR_REC_ID,
                            [IPMI_EVENT_GUID,
                             IPMI_EVENT_SEQ,
                             IPMI_EVENT_TIMESTAMP,
                             IPMI_EVENT_UTC_OFF,
                             IPMI_EVENT_TRAP_SOURCE,
                             IPMI_EVENT_EVENT_SOURCE,
                             IPMI_EVENT_SEVERITY,
                             IPMI_EVENT_SENSOR_DEVICE,
                             IPMI_EVENT_SENSOR_NUM,
                             IPMI_EVENT_ENTITY,
                             IPMI_EVENT_ENTITY_INSTANCE,
                             IPMI_EVENT_EVENT_DATA1,
                             IPMI_EVENT_EVENT_DATA2,
                             IPMI_EVENT_EVENT_DATA3,
                             IPMI_EVENT_EVENT_DATA4,
                             IPMI_EVENT_EVENT_DATA5,
                             IPMI_EVENT_EVENT_DATA6,
                             IPMI_EVENT_EVENT_DATA7,
                             IPMI_EVENT_EVENT_DATA8,
                             IPMI_EVENT_LANGUAGE_CODE,
                             IMPI_EVENT_MFG_ID,
                             IPMI_EVENT_SYSTEM_ID,
                             IPMI_EVENT_MSG],
                             extdata.extdata_fmt2table_name(IPMI_EXTDATA_FMT),
                             parms=event_data)

    conn.commit()
    cursor.close()
    conn.close()
    
    teal_semaphore.Semaphore().post()
    