#!/usr/bin/env python
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

'''
This module is responsible for parsing the AllServiceable events from the HMCs
and logging them into the TEAL database
'''

import os
import re
import optparse
import subprocess

from ibm.teal import teal, registry, event, extdata, alert_mgr, alert
from ibm.teal.registry import get_logger
from ibm.teal.database import db_interface
from ibm.teal.monitor import teal_semaphore

# Configuration file contents
CONFIG_SFP_TEAL = 'connector.sfp'
CONFIG_REFCODE_FILTER = 'refcode_filter'
CONFIG_MTMS_FILTER = 'mtms_filter'

# Directory on HMC where batch files are kept until retrieved
REMOTE_BATCH_FILE_DIR = '/home/hscroot/tmp/'

# TEAL Common Base Event columns
SFP_TEAL_EVENT_COLS = [event.EVENT_ATTR_EVENT_ID,
                       event.EVENT_ATTR_TIME_OCCURRED,
                       event.EVENT_ATTR_SRC_COMP,
                       event.EVENT_ATTR_SRC_LOC_TYPE,
                       event.EVENT_ATTR_SRC_LOC,
                       event.EVENT_ATTR_RPT_COMP,
                       event.EVENT_ATTR_RPT_LOC_TYPE,
                       event.EVENT_ATTR_RPT_LOC,
                       event.EVENT_ATTR_RAW_DATA_FMT
                       ]

# TEAL Extended Event columns
SFP_TEAL_EXTENDED_PK = 'rec_id'
SFP_EVENT_ATTR_PROB_NUM = 'prob_num'
SFP_FRULIST_SIZE = 1536
SFP_RAWDATA_SIZE = 2048
SFP_TEAL_EXTENDED_COLS = [SFP_EVENT_ATTR_PROB_NUM,
                          'description',
                          'call_home',
                          'fru_list',
                          'sfp_raw_data',
                         ]

# TEAL Extended Data Information 
SFP_TEAL_EXTDATA_V1_T1 = 0x5346500080010001L 

# Queries
SFP_CHG_EVENT_QUERY = ''
SFP_ALERT2EVENT_QUERY = ''
SFP_ALERT2EVENT_NOT_QUERY = '' 
SFP_ALERT2ALERT_QUERY = ''    
    

################################################################################                 
#  Used Serviceable Event Data Fields
################################################################################                 

EVENT_CONDITION = 'LSSVCEVENTS_ALL'
EVENT_TYPE = 'EventType'
EVENT_TYPE_OPEN = 'open'
EVENT_TYPE_CLOSED = 'close'
EVENT_TYPE_CHANGED = 'change'
EVENT_REFCODE = 'RefCode'
EVENT_TIMESTAMP = 'OriginalTimeStamp'
EVENT_FAILING_TYPE = 'FDMachineType'
EVENT_FAILING_MODEL = 'FDMachineModel'
EVENT_FAILING_SERIAL = 'FDMachineSerial'
EVENT_FRU_CLASS = 'FRUClass'
EVENT_FRU_SERIAL = 'FRUSerialNumber'
EVENT_FRU_CCIN = 'FRUCCIN'
EVENT_FRU_PARTNUM = 'FRUPartNumber'
EVENT_TEXT = 'EventText'
EVENT_DESCRIPTION = 'Description'
EVENT_DETAILED_DESC = 'DetailedDescription'
EVENT_CALL_HOME = 'EverCallHome'
EVENT_PROB_NUM = 'ProblemNumber'
EVENT_HSC_ID = 'HSCId'
EVENT_HSC_NAME = 'HSCName'
EVENT_HOSTNAME = 'HostName'

# This list of keys are used to prune the raw data saved for the event
EVENT_RM_KEYS = [EVENT_REFCODE,
                 EVENT_TIMESTAMP,
                 EVENT_PROB_NUM,
                 EVENT_FAILING_TYPE,
                 EVENT_FAILING_MODEL,
                 EVENT_FAILING_SERIAL,
                 EVENT_FRU_CLASS,
                 EVENT_FRU_PARTNUM,
                 EVENT_FRU_SERIAL,
                 EVENT_FRU_CCIN,
                 'ExtendedErrorData',
                 EVENT_CALL_HOME,
                 EVENT_TEXT,
                 EVENT_DETAILED_DESC,
                 EVENT_DESCRIPTION,
                 EVENT_HSC_ID,
                 EVENT_HSC_NAME
                ]

################################################################################                 
# Normal ERRM Environment Variables
################################################################################

#            'ERRM_COND_HANDLE'
#            'ERRM_COND_NAME',
#            'ERRM_COND_SEVERITY',
#            'ERRM_COND_SEVERITYID',
#            'ERRM_ER_HANDLE',
#            'ERRM_ER_NAME',
#            'ERRM_RSRC_HANDLE',
#            'ERRM_RSRC_CLASS_NAME',
#            'ERRM_RSRC_CLASS_PNAME',
#            'ERRM_TIME',
#            'ERRM_TYPE',
#            'ERRM_TYPEID',
#            'ERRM_EXPR',
#            'ERRM_ATTR_NAME',
#            'ERRM_ATTR_PNAME',
#            'ERRM_DATA_TYPE',
#            'ERRM_VALUE',
#            'ERRM_SD_DATA_TYPES',
#            'ERRM_NODE_NAME',
#            'ERRM_NODE_NAMELIST',
#            'ERRM_RSRC_TYPE',
#            'ERRM_ERROR_NUM',
#            'ERRM_ERROR_MSG',
#            'ERRM_COND_BATCH',
#            'ERRM_COND_BATCH_NUM',
#            'ERRM_COND_MAX_BATCH',
#            'ERRM_EVENT_DETAIL_FILE',
#            'ERRM_BATCH_REASON',
#            'ERRM_ATTR_NUM'

# These values are based on the ERRM_ATTR_NUM
#             'ERRM_ATTR_PNAME_{0}',
#             'ERRM_DATA_TYPE_{0}',
#             'ERRM_VALUE_{0}',
#             'ERRM_SD_DATA_TYPES_{0}'


################################################################################                 
# ERRM Batch Event Environment Variables
################################################################################
                 
#             'ERRM_COND_HANDLE',
#             'ERRM_COND_NAME',
#             'ERRM_ER_HANDLE',
#             'ERRM_ER_NAME',
#             'ERRM_TIME',
#             'ERRM_COND_BATCH',
#             'ERRM_COND_BATCH_NUM',
#             'ERRM_COND_MAX_BATCH',
#             'ERRM_EVENT_DETAIL_FILE',
#             'ERRM_BATCH_REASON'

################################################################################                 
# Event Batch File ERRM Environment Variables
################################################################################                 

# This is the header information at the top of the event file
#
#             'FIRST_EVENT_TIME',
#             'LAST_EVENT_TIME',
#             'NUM_EVENTS'

# This is the possible data for every event in the event file
#             'ERRM_COND_HANDLE',
#             'ERRM_COND_NAME',
#             'ERRM_COND_SEVERITY',
#             'ERRM_COND_SEVERITYID'                   
#             'ERRM_RSRC_HANDLE',
#             'ERRM_RSRC_CLASS_NAME',
#             'ERRM_RSRC_CLASS_NAME',
#             'ERRM_RSRC_CLASS_PNAME',
#             'ERRM_TIME',
#             'ERRM_TYPE',
#             'ERRM_TYPEID',
#             'ERRM_EXPR',
#             'ERRM_ATTR_NAME',
#             'ERRM_ATTR_PNAME',
#             'ERRM_DATA_TYPE',
#             'ERRM_VALUE',
#             'ERRM_SD_DATA_TYPES',
#             'ERRM_NODE_NAME',
#             'ERRM_NODE_NAMELIST',
#             'ERRM_RSRC_TYPE',
#             'ERRM_ERROR_NUM',
#             'ERRM_ERROR_MSG',
#             'ERRM_COND_BATCH',
#             'ERRM_COND_MAX_BATCH',
#             'ERRM_ATTR_NUM'

# These values are based on the ERRM_ATTR_NUM
#             'ERRM_ATTR_PNAME_{0}',
#             'ERRM_DATA_TYPE_{0}',
#             'ERRM_VALUE_{0}',
#             'ERRM_SD_DATA_TYPES_{0}'


################################################################################                 
# Required Serviceable Event Keywords
################################################################################                 

#        'EventType',
#        'FDMachineType',
#        'FDMachineModel',
#        'FDMachineSerial'
#        'EverCallHome',
#        'CalledHome',
#        'Description',
#        'HSCId',
#        'HSCName',                

################################################################################                 
# Optional Serviceable Event Keywords
################################################################################
                 
#         'ProblemNumber',
#         'Detail-Description',
#         'LastReportedTimeStamp',
#         'RefCode',
#         'FRUCCIN',
#         'FRUEnclosureMachineTypeModel',
#         'FRUEnclosureMachineSerialNumber',
#         'FRULogicControllingCECMachineTypeModel',
#         'FRULogicControllingCECMachineSerialNumber',
#         'FRUPowerControllingCECMachineTypeModel',
#         'FRUPowerControllingCECMachineSerialNumber',
#         'FRUPartNumber',
#         'FRUPartNumberReplace',
#         'FRURecentlyReplaced',
#         'FRUReplaceTimeStamp',
#         'FRUAddLocation',
#         'FRUAddPartNumber',
#         'FRUAddReplaceTimestamp',
#         'FRUClass',
#         'FRUReplacementPriority',
#         'FRUConcurentMaintenance',
#         'FRUDescription',
#         'FRUSerialNumber',
#         'ErrorClass',
#         'ErrorCode',
#         'OriginalTimeStamp',
#         'CECMachineType',
#         'CECMachineModel',
#         'CECMachineSerialNumber',
#         'CreatedTimeStamp',
#         'DuplicateCount',
#         'ExtendedErrorData',
#         'DumpID',
#         'ComponentID',
#         'CreatorID',
#         'FixPackageInfo',
#         'ErrorLabel',          # OS-reported error info
#         'ErrorSequence',       # OS-reported error info
#         'OSType',              # OS-reported error info
#         'PartitionID',         # OS-reported error info
#         'PartitionName',       # OS-reported error info
#         'HostName',            # OS-reported error info
#         'SystemRefCode',
#         'FDAAdditionalMachine',
#         'ClusterMachineTypeModel',
#         'ClusterMchineSerialNumber',
#         'CEDataName',
#         'CEDataText',
#         'CEDataTimestamp',
#         'PlatformLogID',
#         'SubsystemID',
#         'EventSeverity'

#def print_errm_env(errm_env):
#    ''' Dump all of the ERRM environment variables to a file for viewing
#    '''
#    log = open('/tmp/teal_errm.log', "a")
#    print >> log, datetime.now()
#
#    # Spit out all the possible simple environment variables
#    for evar in ERRM_ENV:
#        print >>log, evar, '=', errm_env.get(evar, None)
#
#        # If there is an array of additional values, build the string 
#        # and fetch the possible value
#        attr_num = errm_env.get('ERRM_ATTR_NUM', None)
#        if (attr_num is not None and int(attr_num) > 1):
#            for i in xrange(2, int(attr_num)+1):
#                idx = str(i)
#                for evar_x in ERRM_ENVIRON_X:
#                    var = evar_x.format(idx)
#                    print >>log, var, '=', errm_env.get(var,None)
#                    
#    log.close()

def gen_time_occurred(event_time):
    ''' Reformat the time occurred in the time format expected by TEAL
    '''
    m = re.match('(\d+)/(\d+)/(\d+) +(.*)', event_time)
    mo = m.group(1)
    dy = m.group(2)
    yr = m.group(3)
    time = m.group(4)    
    time_occurred = '{0}-{1}-{2} {3}'.format(yr, mo, dy, time)
    
    return time_occurred

def gen_rpt_loc(errm_env, event_data):
    ''' Create the Reporting Location from the event data
    '''
    rpt_comp = '{0}/{1}'.format(event_data[EVENT_HSC_ID], event_data[EVENT_HSC_NAME])
    rpt_loc_type = 'A' 
    rpt_loc = '{0}##{1}'.format(errm_env['ERRM_NODE_NAME'], errm_env['ERRM_COND_NAME'])
    
    return(rpt_comp, rpt_loc_type, rpt_loc)

def define_queries():
    ''' Generate the select strings for the needed queries
    '''
    # Find the already logged event that matches the current event that just
    # came from the SFP
    global SFP_CHG_EVENT_QUERY, SFP_ALERT2EVENT_QUERY, SFP_ALERT2EVENT_NOT_QUERY, SFP_ALERT2ALERT_QUERY
    
    where_clause = '${0} = ?'.format(SFP_EVENT_ATTR_PROB_NUM)
    chg_sub_query = dbi.gen_select([SFP_TEAL_EXTENDED_PK], 
                                   SFP_TEAL_EXTDATA_TABLE,
                                   where=where_clause, 
                                   where_fields=[SFP_EVENT_ATTR_PROB_NUM])
    
    where_clause = '${0} = ? AND ${1} = ? AND ${2} = ? AND ${3} in ({4})'.format(event.EVENT_ATTR_TIME_OCCURRED,
                                                                                 event.EVENT_ATTR_RPT_LOC_TYPE,
                                                                                 event.EVENT_ATTR_RPT_LOC,
                                                                                 event.EVENT_ATTR_REC_ID,
                                                                                 chg_sub_query)
    
    SFP_CHG_EVENT_QUERY = dbi.gen_select([event.EVENT_ATTR_REC_ID],
                                         db_interface.TABLE_EVENT_LOG,
                                         where=where_clause,
                                         where_fields=[event.EVENT_ATTR_TIME_OCCURRED,
                                                       event.EVENT_ATTR_RPT_LOC_TYPE,
                                                       event.EVENT_ATTR_RPT_LOC,
                                                       event.EVENT_ATTR_REC_ID])


    # Find the alerts that have an event as a condition
    where_open_alerts = '${0} = {1}'.format(alert.ALERT_ATTR_STATE,
                                            alert.ALERT_STATE_OPEN)
    alt_sub_query = dbi.gen_select([alert.ALERT_ATTR_REC_ID],
                                   db_interface.TABLE_ALERT_LOG,
                                   where=where_open_alerts,
                                   where_fields=[alert.ALERT_ATTR_STATE])
    
    
    # All alerts that have the provided event as a condition
    where_clause = "${0} = ? AND ${1} = '{2}' AND ${3} in ({4})".format(alert.ALERT2EVENT_ATTR_T_EVENT_RECID,
                                                                        alert.ALERT2EVENT_ATTR_ASSOC_TYPE,
                                                                        alert.ALERT2EVENT_ASSOC_TYPE_CONDITION,
                                                                        alert.ALERT2EVENT_ATTR_ALERT_RECID,
                                                                        alt_sub_query)
                                                                 
    SFP_ALERT2EVENT_QUERY = dbi.gen_select([alert.ALERT2EVENT_ATTR_ALERT_RECID],
                                           db_interface.TABLE_ALERT2EVENT,
                                           where=where_clause,
                                           where_fields=[alert.ALERT2EVENT_ATTR_T_EVENT_RECID,
                                                         alert.ALERT2EVENT_ATTR_ASSOC_TYPE,
                                                         alert.ALERT2EVENT_ATTR_ALERT_RECID])
    
    # All condition events minus the provided event for a provided alert
    where_clause = "${0} = ? AND ${1} = '{2}' AND ${3} != ?".format(alert.ALERT2EVENT_ATTR_ALERT_RECID,
                                                                    alert.ALERT2EVENT_ATTR_ASSOC_TYPE,
                                                                    alert.ALERT2EVENT_ASSOC_TYPE_CONDITION,
                                                                    alert.ALERT2EVENT_ATTR_T_EVENT_RECID)
    
    SFP_ALERT2EVENT_NOT_QUERY = dbi.gen_select([alert.ALERT2EVENT_ATTR_ALERT_RECID],
                                               db_interface.TABLE_ALERT2EVENT,
                                               where=where_clause,
                                               where_fields=[alert.ALERT2EVENT_ATTR_T_EVENT_RECID,
                                                             alert.ALERT2EVENT_ATTR_ASSOC_TYPE,
                                                             alert.ALERT2EVENT_ATTR_ALERT_RECID])

    # All condition alerts for a provided alert
    where_clause = "${0} = ? AND ${1} = '{2}'".format(alert.ALERT2ALERT_ATTR_ALERT_RECID,
                                                      alert.ALERT2ALERT_ATTR_ASSOC_TYPE,
                                                      alert.ALERT2ALERT_ASSOC_TYPE_CONDITION)
    
    SFP_ALERT2ALERT_QUERY = dbi.gen_select([alert.ALERT2EVENT_ATTR_ALERT_RECID],
                                           db_interface.TABLE_ALERT2ALERT,
                                           where=where_clause,
                                           where_fields=[alert.ALERT2ALERT_ATTR_ALERT_RECID,
                                                         alert.ALERT2ALERT_ATTR_ASSOC_TYPE])
    
    
def find_logged_alerts(event_rec_id):
    ''' Find an alert where this is the only event associated 
    '''
    alert_recids = []    
    
    # Find the open alerts that this event is a condition for
    # For each alert, determine if the event is the only condition
    qry_cursor = cnxn.cursor()
    subqry_cursor = cnxn.cursor()
    for row in qry_cursor.execute(SFP_ALERT2EVENT_QUERY,event_rec_id):
        alert_recid = row[0]
        # Need to check both alerts and events
        subqry_cursor.execute(SFP_ALERT2ALERT_QUERY,alert_recid)
        a2a_row = subqry_cursor.fetchone()
        
        subqry_cursor.execute(SFP_ALERT2EVENT_NOT_QUERY, alert_recid, event_rec_id)
        a2e_row = subqry_cursor.fetchone()
        
        # If there are no other condition alerts or events with this particular alert, then we want to close it
        if (a2a_row is None or a2a_row[0] is None) and (a2e_row is None or a2e_row[0] is None):
            alert_recids.append(alert_recid)
            
    return alert_recids

def close_event(errm_env, event_data):
    ''' Find an alert that associated with the closed event and close it. This
    will only close an alert that has this event as the one and only event
    '''
    # Find the matching event in the event log
    event_rec_id = find_logged_event(errm_env, event_data)
    
    # If no event was found, there is nothing more to do
    if event_rec_id is None:
        return
    
    # Find an alert that this event is the only event associated with
    alert_recids = find_logged_alerts(event_rec_id)
    
    # If there is no alert associated with this event, then it may have
    # already been closed out or never logged in the first place based 
    # on when this connector started listening for events
    if len(alert_recids) == 0:
        return
    
    # Close this alert and any alerts that were duplicates of this alert
    a_mgr = registry.get_service(registry.SERVICE_ALERT_MGR)
    
    for alert_recid in alert_recids:
        try:
            a_mgr.close(alert_recid)
        except alert_mgr.AlertMgrError, ame:
            get_logger().warn('Failed to close alert({0}) associated to event ({1}): {2}'.format(alert_recid, event_rec_id, ame))

def find_logged_event(errm_env, event_data):
    ''' Query the event log for a particular problem number and reporting 
    HMC location. Return the event rec_id if found
    '''    
    time_occurred = gen_time_occurred(event_data[EVENT_TIMESTAMP])
    rpt_comp, rpt_loc_type, rpt_loc = gen_rpt_loc(errm_env, event_data)

    qry_cursor = cnxn.cursor()
    qry_cursor.execute(SFP_CHG_EVENT_QUERY, 
                       time_occurred, 
                       rpt_loc_type, 
                       rpt_loc, 
                       event_data[EVENT_PROB_NUM])
     
    row = qry_cursor.fetchone()
    if row is not None and row[0] is not None:
        return row[0]
    else:
        return None
    
def split_partnum_info(part_num_loc):
    ''' Split the part number and physical location code into two separate lists
    '''
    part_nums = []
    locs = []
    for data in part_num_loc:
        pn_info = data.split(' ')
        part_nums.append(pn_info[0])
        if len(pn_info) == 2:
            locs.append(pn_info[1])
        else:
            locs.append('')    
            
    return (part_nums, locs)
            

def log_event(errm_env, event_data):
    ''' Logs the event to the event log and notifies teal
    '''
    #print_errm_env(errm_env)
    event_id = event_data[EVENT_REFCODE]
    
    # Format MM/DD/YYYY HH:MM:SS => YYYY-MM-DD HH:MM:SS
    time_occurred = gen_time_occurred(event_data[EVENT_TIMESTAMP])

    # Source location is the failing machine reported via the HMC or Hostname (if available)
    src_comp = "SFP"
    
    if ((EVENT_HOSTNAME in event_data) and (len(event_data[EVENT_HOSTNAME].strip()) > 0)):
        src_loc_type = 'A'
        src_loc = event_data[EVENT_HOSTNAME]
    else:
        src_loc_type = 'P' 
        src_loc = 'U{0}.{1}.{2}'.format(event_data[EVENT_FAILING_TYPE],
                                        event_data[EVENT_FAILING_MODEL],
                                        event_data[EVENT_FAILING_SERIAL])
    
    # Reporting location is the HMC and Sensor that fired reported via this connector
    rpt_comp,rpt_loc_type,rpt_loc =  gen_rpt_loc(errm_env, event_data)
    
    # Create a FRU list if one is available
    fru_list = []
    if 'FRUPartNumber' in event_data:
        pn_plc = event_data.get(EVENT_FRU_PARTNUM)
        (part_nums, locs) = split_partnum_info(pn_plc)
        classes = event_data.get(EVENT_FRU_CLASS, None)
        serial_nums = event_data.get(EVENT_FRU_SERIAL, None)
        ccins = event_data.get(EVENT_FRU_CCIN, None)
        
        for fru in range(len(part_nums)):
            fru_part_num = part_nums[fru]
            if classes is not None:
                fru_class = classes[fru]
            else:
                fru_class = ''
            fru_loc = locs[fru]
            if serial_nums is not None:
                fru_serial_num = serial_nums[fru]
            else:
                fru_serial_num = ''
            fru_ecid = ''
            if ccins is not None:
                fru_ccin = ccins[fru]
            else:
                fru_ccin = ''
                
            # The FRU list will be copied into an Alert as required
            fru_info = [fru_part_num,
                        fru_class,
                        fru_loc,
                        fru_serial_num,
                        fru_ecid,
                        fru_ccin]
            
            fru_list.append(fru_info)

    # Pull out the problem number if it exists for later correlation
    prob_num = event_data.get(EVENT_PROB_NUM, None)
    
    # Save off the description of the problem.
    if EVENT_TEXT in event_data:
        # EventText overrides all other error descriptons
        description = event_data[EVENT_TEXT]
    elif EVENT_DETAILED_DESC in event_data:
        # Detailed description is the full text if too big to fit in the description
        description = event_data[EVENT_DETAILED_DESC]
    else:
        description = event_data[EVENT_DESCRIPTION]
    
    # Call Home is used to determine if an alert should be created
    call_home = event_data.get(EVENT_CALL_HOME, None)
    if call_home is None:
        call_home = 'N'
    else:
        call_home = call_home[0]
        
    # Remove all the keys that we have used so far to reduce redundancy/size in the raw data
    for k in EVENT_RM_KEYS:
        if k in event_data:
            del event_data[k]
    raw_data = str(event_data)[0:SFP_RAWDATA_SIZE]
    
    # Shorten the FRU list if necessary to fit within the column size
    eol = -1
    str_fru_list = str(fru_list)    
    while (len(str_fru_list) > SFP_FRULIST_SIZE):
        str_fru_list = str(fru_list[0:eol])
        eol -= 1
    
    # Create the event and log it in the error log
    dbi.insert(cursor,
               SFP_TEAL_EVENT_COLS,
               db_interface.TABLE_EVENT_LOG,
               [event_id,
                time_occurred,
                src_comp,
                src_loc_type,
                src_loc,
                rpt_comp,
                rpt_loc_type,
                rpt_loc,
                SFP_TEAL_EXTDATA_V1_T1
                ])
    
    dbi.insert_dependent(cursor,
                         SFP_TEAL_EXTENDED_PK,
                         SFP_TEAL_EXTENDED_COLS,
                         SFP_TEAL_EXTDATA_TABLE,
                         [prob_num, description, call_home, str_fru_list, raw_data])
    
def parse_event(sfp_data):
    ''' Parse the RMC data into a dictionary that can be used to log the actual event
    '''
    event_data = {}
    
    if sfp_data:
        if sfp_data.startswith(EVENT_CONDITION):
            sfp_data = sfp_data[len(EVENT_CONDITION):]
        
        # Split out all the key/value pairs in the string    
        key_values = sfp_data.split('<=;=>')
       
        # Now walk through each key/value pair and put into a dictionary 
        # for easier access
        for key_value in key_values:
            data = key_value.split('<==>')
              
            # Make sure there is a key/value pair (could be empty pair)
            if len(data) == 2:
                event_key = data[0]
                event_value = data[1]
                
                # If the event data is a list, break it into a python list
                # Data is formated as <space>value<space>;
                if (data[1].find(';') >= 0):
                    event_value = []
                    elem = data[1].partition(' ;')
                    while(elem[1] == ' ;'):
                        event_value.append(elem[0][1:])
                        elem = elem[2].partition(' ;')
                    
                event_data[event_key] = event_value        
    else:
        raise ValueError,'No error value reported by RMC'

    return event_data

def event_filtered(errm_env, event_data):
    ''' Determine if the event should be filtered or not.
     
    Filtering is based on fixed values as well as values written in the configuration file
    '''
    
    # If the problem number is negative then this is an HMC internal update to a problem
    # and should be ignored    
    if EVENT_PROB_NUM in event_data and int(event_data[EVENT_PROB_NUM]) < 0:
        return True
    
    if EVENT_REFCODE in event_data:
        refcode = event_data[EVENT_REFCODE]
        # Do not process SFP events that have a refcode that is 
        # the same as those generated by Alerts in the framework
        alert_metadata = registry.get_service(registry.SERVICE_ALERT_METADATA)
        if refcode in alert_metadata:
            get_logger().info("{0} filtered. Reason: In alert metadata".format(refcode))
            return True
        
        # Filter based on refcode settings
        if ((refcode_filter is not None) and 
            (refcode_filter.match(refcode) is not None)):
            get_logger().info("{0} filtered. Reason: refcode filter match".format(refcode))
            return True
        
        # Filter based on Failing MTMS
        mtms = '{0}{1}{2}'.format(event_data[EVENT_FAILING_TYPE],
                                  event_data[EVENT_FAILING_MODEL],
                                  event_data[EVENT_FAILING_SERIAL])

        if ((mtms_filter is not None) and
            (mtms_filter.match(mtms) is not None)):
            get_logger().info("{0} filtered. Reason: MTMS filter match".format(mtms))
            return True
        
        # All filters passed
        return False
    else:
        # Can't process events that don't have a refcode
        return True 

def handle_event(errm_env):
    ''' Parse and log the event retrieved from the HMC
    '''
    event_data = parse_event(errm_env['ERRM_VALUE'])
    if not event_filtered(errm_env, event_data):
        event_type = event_data[EVENT_TYPE]
        
        if (event_type == EVENT_TYPE_OPEN):
            # New event -- Tell TEAL about it
            log_event(errm_env, event_data)
            
        elif (event_type == EVENT_TYPE_CLOSED):
            get_logger().info('{0}:{1} - {2}'.format(event_data[EVENT_PROB_NUM], 
                                                     event_data[EVENT_REFCODE],
                                                     event_type))
            close_event(errm_env, event_data)
            
        elif (event_type == EVENT_TYPE_CHANGED):
            # Make sure this is for an event with a valid problem number
            if (EVENT_PROB_NUM in event_data):
                # If this event has not been logged, then we missed the 
                # initial logging or never saw an open event (which can occur)
                if find_logged_event(errm_env, event_data) is None:
                    log_event(errm_env, event_data)
                    
        else:
            # Other event status changes are not operated on
            get_logger().warn('{0}:{1} - {2}'.format(event_data[EVENT_PROB_NUM], 
                                                     event_data[EVENT_REFCODE],
                                                     event_type))

def parse_batch_file(batch_filename):
    ''' Read the batch file and parse each of the events enclosed
    '''    
    new_event = re.compile('Event \d+:')
    event_env = {}
    skip_event = True
    
    batch_file = open(batch_filename)
    
    for batch_line in batch_file:
        line = batch_line.strip()
        
        # Skip any blank lines
        if len(line) == 0:
            continue
        
        # Check if this is the beginning of a new event
        m = new_event.match(line)
        if m:
            # If not first event, handle the previous
            if not skip_event:
                handle_event(event_env)
                
            # Set up to save the event environment for this new event
            event_env = {}
            skip_event = False
            continue
        elif skip_event:
            # Wait for first/next event to process
            continue
            
        # Pull out the event data and store in new "environment"
        (name, value) = line.split('=', 1)
        
        errm_name = name.strip()
        errm_value = value.strip()
        
        # If this is not an 'Event' type event skip it
        if errm_name == 'ERRM_TYPEID' and int(errm_value) != 0:
            skip_event = True
            continue
        
        event_env[errm_name] = errm_value            
    
    # Process the last event if it exists
    if event_env is not None:
        handle_event(event_env)
    
    batch_file.close()    

def handle_batch_event(errm_env, remote):
    ''' Process the batch events
    '''
    if remote:
        try:
            remote_details = errm_env['ERRM_VALUE'].strip()
            m = re.match('\[.*,(.*),.*\]', remote_details)
            rmt_filename = m.group(1).strip() 
            
            # Need to copy over the event log so it can be handled
            rmt_host = errm_env['ERRM_NODE_NAME']
            rmt_file = 'hscroot@{0}:{1}'.format(rmt_host, rmt_filename)
            lcl_file = '/tmp/{0}_{1}'.format(rmt_host, os.path.basename(rmt_filename))  
                      
            subprocess.check_call(['/usr/bin/scp', rmt_file, lcl_file])
            
            # Parse the events that were saved on the remote system
            parse_batch_file(lcl_file)
            
            # All done processing events so remove the file
            os.remove(lcl_file)
            
        except subprocess.CalledProcessError, cpe:
            # TODO: Log error and leave
            get_logger().error("Failed to copy batch file: {0}".format(cpe))
        except OSError, ose:
            # TODO: Log the OS Error
            get_logger().error("Failed to process batch file: {0}".format(ose))
    else:
        parse_batch_file(errm_env['ERRM_EVENT_DETAIL_FILE'])

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-r', '--remote',
                      action='store_true',
                      default=False,
                      dest='remote',
                      help='Batching is done on the remote system')
    parser.add_option("-m", 
                      "--msglevel",
                      help="set the trace message level [default: %default]",
                      action="store",
                      dest="msg_level",
                      choices=['error','warn','info','debug'],
                      default='warn')
    parser.add_option("-l", 
                      "--logfile",
                      help="set the trace message level",
                      action="store",
                      dest="log_file",
                      default=None)

    (options, args) = parser.parse_args()

    if options.log_file is None:
        log_file = '$TEAL_LOG_DIR/teal_sfp.log'
    else:
        log_file = options.log_file

    # Set up the TEAL environment so we have access to the various services
    t = teal.Teal(None, data_only=True, msgLevel=options.msg_level, logFile=log_file)

    # Setup configuration info
    cfg = registry.get_service(registry.SERVICE_CONFIGURATION)
    try:
        value = cfg.get(CONFIG_SFP_TEAL, CONFIG_REFCODE_FILTER)
        get_logger().debug('refcode filter enabled: {0}'.format(value))            
        refcode_filter = re.compile(value)
    except:
        get_logger().debug('No refcode filter defined')            
        refcode_filter = None

    try:
        value = cfg.get(CONFIG_SFP_TEAL, CONFIG_MTMS_FILTER)
        get_logger().debug('MTMS filter enabled: {0}'.format(value))            
        mtms_filter = re.compile(value)
    except:
        get_logger().debug('No MTMS filter defined')            
        mtms_filter = None

    # Set up for database access within the process
    SFP_TEAL_EXTDATA_TABLE = extdata.extdata_fmt2table_name(SFP_TEAL_EXTDATA_V1_T1)
    dbi = registry.get_service(registry.SERVICE_DB_INTERFACE)
    cnxn = dbi.get_connection()
    cursor = cnxn.cursor()
    
    # Set up possible queries used to find events already logged
    define_queries()

    #####################################################
    # Process the event(s) that are being reported to TEAL            
    #####################################################
    try:
        batch = os.environ.get('ERRM_COND_BATCH', None)
        if (((batch is not None) and (int(batch) == 1)) or options.remote):
            handle_batch_event(os.environ, options.remote)
        else:
            handle_event(os.environ)
    except BaseException, be:
        get_logger().exception(be)
        
    # Commit the events that have been processed    
    cnxn.commit()
    cnxn.close()

    # Notify TEAL that events have been processed       
    teal_semaphore.Semaphore().post()
    
    # Shutdown and exit
    t.shutdown()
    