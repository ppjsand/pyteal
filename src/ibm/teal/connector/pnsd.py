#!/usr/bin/env python
# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import os
import time
import optparse

from ibm.teal import teal, registry, event
from ibm.teal.database import db_interface
from ibm.teal.monitor import teal_semaphore
from ibm.teal.registry import get_logger

PNSD_RETRANSMIT_THRESHOLD = 'PNSD0001'
PNSD_STAT_SENSOR = 'TealPnsdStat'

# TEAL Common Base Event columns
PNSD_TEAL_EVENT_COLS = [event.EVENT_ATTR_EVENT_ID,
                        event.EVENT_ATTR_TIME_OCCURRED,
                        event.EVENT_ATTR_SRC_COMP,
                        event.EVENT_ATTR_SRC_LOC_TYPE,
                        event.EVENT_ATTR_SRC_LOC,
                        event.EVENT_ATTR_RPT_COMP,
                        event.EVENT_ATTR_RPT_LOC_TYPE,
                        event.EVENT_ATTR_RPT_LOC,
                        event.EVENT_ATTR_RAW_DATA_FMT,
                        event.EVENT_ATTR_RAW_DATA
                        ]

def log_event(event_id, time_occurred, src, rpt, raw_data_fmt, raw_data):
    ''' Log the event to TEAL. This event will only use the raw data within the
    event to log additional data
    '''
    dbi = registry.get_service(registry.SERVICE_DB_INTERFACE)
    cnxn = dbi.get_connection()
    cursor = cnxn.cursor()
    
    # Create the event and log it in the error log
    dbi.insert(cursor,
               PNSD_TEAL_EVENT_COLS,
               db_interface.TABLE_EVENT_LOG,
               [event_id,
                time_occurred,
                src[0],
                src[1],
                src[2],
                rpt[0],
                rpt[1],
                rpt[2],
                raw_data_fmt,
                raw_data
                ])
    
    cnxn.commit()
    cnxn.close()
    
    teal_semaphore.Semaphore().post()
    

def parse_event(errm_env):
    ''' Handles a PNSD event that was directly monitored by the node
    '''
    # Make sure it was our sensor that fired
    rsrc_name = errm_env.get('ERRM_RSRC_NAME')
    if  rsrc_name != PNSD_STAT_SENSOR:
        get_logger().warn('Unknown resource name: {0}'.format(rsrc_name))
        return
    
    event_id = PNSD_RETRANSMIT_THRESHOLD
    
    # Time from RMC is in sec,usec format
    sec_usec = errm_env.get('ERRM_TIME', None)
    if sec_usec is not None:
        sec = long(sec_usec.split(',')[0])
    else:
        sec = None
        
    time_occurred = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec))
    
    # Create the location codes 
    src = ('PNSD', 'A', '{0}##{1}'.format(errm_env.get('ERRM_NODE_NAME'), rsrc_name))
    rpt = (None, None, None)
    
    # Save the restransmit percentage as the error data
    raw_data_fmt = 0 # No special formatting required
    raw_data = errm_env.get('ERRM_VALUE')

    log_event(event_id, time_occurred, src, rpt, raw_data_fmt, raw_data)

def parse_last_event(errm_env):
    ''' Pull the items of interest form the event and log it to TEAL
    '''
    last_event = errm_env.get('ERRM_VALUE')
    
    (occurred, 
     err_num,
     err_msg,
     event_flags,
     event_time_sec,
     event_time_usec,
     rsrc_handle,
     node_name,
     num_attr,
     num_attr_evt_expr,
     start_index,
     attributes) = last_event.split(',',11)
     
    if int(err_num) != 0:
        get_logger().error("Error event occurred: {0}".format(last_event))
        return
    
    for attr_num in range(int(num_attr)):
        attr = attributes.split(',',3)
        
        name = attr[0].strip('"')
        value = attr[2].strip('"')
        
        if name == 'Float64':
            raw_data = value
        elif name == 'Name':
            rsrc_name = value
            
        if len(attr) == 4:
            attributes = attr[3]
    
    event_id = PNSD_RETRANSMIT_THRESHOLD    
    time_occurred = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(long(event_time_sec))) 
    
    src = ('PNSD', 'A', '{0}##{1}'.format(node_name.strip('"'), rsrc_name))
    rpt = ('PNSD', 'A', '{0}##{1}'.format(errm_env.get('ERRM_NODE_NAME'),
                                          errm_env.get('ERRM_RSRC_NAME')))
        
    # Using the raw data in the event itself, i.e. no extended data
    raw_data_fmt = 0
    
    log_event(event_id, time_occurred, src, rpt, raw_data_fmt, raw_data)
            
     
if __name__ == '__main__':
    
    parser = optparse.OptionParser()
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
    parser.add_option("", 
                      "--hierarchical",
                      help="Response is part of a hierarchical monitoring event",
                      action="store_true",
                      dest="hierarchical",
                      default=False)
    
    (options, args) = parser.parse_args()
  
    if options.log_file is None:
        log_file = "$TEAL_LOG_DIR/teal_pnsd.log"
    else:
        log_file = options.log_file
  
    try:
        t = teal.Teal(None, data_only=True, msgLevel=options.msg_level, logFile=log_file)
    
        if options.hierarchical:
            parse_last_event(os.environ)
        else:
            parse_event(os.environ)
        
        t.shutdown()
    except BaseException, be:
        get_logger().exception(be)
