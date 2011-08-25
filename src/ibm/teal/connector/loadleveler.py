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

import time
import signal
import threading
import optparse
import string
import sys

from ibm.teal import teal
from ibm.teal import registry
from ibm.teal import event
from ibm.teal import extdata
from ibm.teal.util import command
from ibm.teal.database import db_interface
from ibm.teal.monitor import teal_semaphore

# Loadleveler DB information
LL_EVENT_TABLE = 'TLL_RASLog' 

LL_EVENT_ATTR_TIME_OCCURRED = 'time_occurred'
LL_EVENT_ATTR_TIME_LOGGED = 'time_logged'
LL_EVENT_ATTR_MSG_TYPE = 'msg_type'

LL_EVENT_COLS = [LL_EVENT_ATTR_TIME_OCCURRED, 
                 LL_EVENT_ATTR_TIME_LOGGED, 
                 'event_id',
                 'node',
                 LL_EVENT_ATTR_MSG_TYPE,
                 'message',
                 'detail',
                 'subject',
                 'reporter',
                 'job_step_id'
                 ]

ll_col = lambda x: LL_EVENT_COLS.index(x)
LL_EVENT_COL_TIME_OCCURRED = ll_col(LL_EVENT_ATTR_TIME_OCCURRED)
LL_EVENT_COL_TIME_LOGGED = ll_col(LL_EVENT_ATTR_TIME_LOGGED)
LL_EVENT_COL_EVENT_ID = ll_col('event_id')
LL_EVENT_COL_NODE = ll_col('node')
LL_EVENT_COL_MSG_TYPE = ll_col(LL_EVENT_ATTR_MSG_TYPE)
LL_EVENT_COL_MESSAGE = ll_col('message')
LL_EVENT_COL_DETAIL = ll_col('detail')
LL_EVENT_COL_SUBJECT = ll_col('subject')
LL_EVENT_COL_REPORTER = ll_col('reporter')
LL_EVENT_COL_JOB_STEP_ID = ll_col('job_step_id')

# Loadleveler does not use xCAT to create the tables so the query does not need
# any specific preperation using the DB interfaces
LL_EVENT_QUERY_STR = '''SELECT {0} FROM {1} WHERE {2} > ? AND {3} IN ({4}) ORDER BY {5} ASC'''

# Loadleveler event message types
LL_MSG_TYPES = {'RAS_ERROR':"'E'", 'RAS_WARN':"'E','W'", 'RAS_INFO':"'E','W','I'", 'RAS_TRACE':"'E','W','I','T'"}
 
# Scaling factor to retrieve seconds from LL data
SECONDS_FACTOR = 1000000L

# XCAT Table definitions
XCAT_SITE = 'site'
XCAT_SITE_KEY = 'key'
XCAT_SITE_VALUE = 'value'
XCAT_LL_CHKPT = 'teal_ll_ckpt'

# TEAL DB Information for LoadLeveler
LL_TEAL_COLS = [event.EVENT_ATTR_EVENT_ID,
                event.EVENT_ATTR_TIME_OCCURRED,
                event.EVENT_ATTR_SRC_COMP,
                event.EVENT_ATTR_SRC_LOC_TYPE,
                event.EVENT_ATTR_SRC_LOC,
                event.EVENT_ATTR_RPT_COMP,
                event.EVENT_ATTR_RPT_LOC_TYPE,
                event.EVENT_ATTR_RPT_LOC,
                event.EVENT_ATTR_RAW_DATA_FMT
                ]

LL_TEAL_EXTENDED_PK = 'rec_id'
LL_TEAL_EXTENDED_COLS = [LL_EVENT_ATTR_TIME_OCCURRED,
                         LL_EVENT_ATTR_TIME_LOGGED,
                         'msg_type',
                         'message',
                         'detail',
                        ]

# TEAL Extended Data Information 
LL_TEAL_EXTDATA_V1_T1 = 0x4C4C000080010001L 

# Configuration Parameters
LL_TEAL_DEFAULT_POLL_INTERVAL = 5
LL_TEAL_DEFAULT_MSG_TYPE = LL_MSG_TYPES['RAS_WARN']

CONFIG_LL_TEAL = 'connector.loadleveler'
CONFIG_POLL_INTERVAL = 'poll_interval'
CONFIG_MSG_TYPE = 'msg_type'
    
class LoadLeveler(threading.Thread):
    def __init__(self):
        ''' Constructor
        '''
        self.poll_interval = LL_TEAL_DEFAULT_POLL_INTERVAL
        self.msg_type = ""
        self.last_time_logged = 0
        self. notifier = None
        self.running = True
        self.LL_EVENT_QUERY = ''
        self.exception = None
        
        self._configure()
        threading.Thread.__init__(self)
    
    def stop(self):
        ''' Indicator to connector to stop running. Stopping will occur once
        the process has completed its current iteration
        '''
        self.running = False
        
    def run(self):
        ''' Run the polling loop looking for new events from Loadleveler
        '''
        try:
            while(self.running):
                # Receive any new events since last polling period
                self._handle_events()
                                
                # Wait for the next polling iteration
                time.sleep(self.poll_interval)

        except BaseException as self.exception:            
            registry.get_logger().exception("Connector failed")
            
    def _handle_events(self):
        ''' Look for and handle any new events from the last time it was checked
        '''
        event_logged = False
        last_time_logged = self.last_time_logged

        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        cnxn = db.get_connection()
        ll_cursor = cnxn.cursor()
        teal_cursor = cnxn.cursor()
        
        try:
            # Query the LL event log for new events
            for ll_event in ll_cursor.execute(self.LL_EVENT_QUERY, last_time_logged):
                event_logged = True
                
                # Log the event into TEAL
                self._log_event(db, teal_cursor, ll_event)
                
                # Update the 'cursor' into the LL database
                last_time_logged = ll_event[LL_EVENT_COL_TIME_LOGGED]
                        
        except:            
            # Don't attempt to commit anything since we had an error processing the events
            registry.get_logger().exception("Error processing new events")
            cnxn.rollback()
            event_logged = False
                    
        # Notify TEAL that events have been inserted
        if (event_logged):
            db.update(teal_cursor, 
                      [XCAT_SITE_VALUE], 
                      XCAT_SITE, 
                      where="${0} = '{1}'".format(XCAT_SITE_KEY, XCAT_LL_CHKPT), 
                      where_fields=[XCAT_SITE_KEY], 
                      parms=[str(last_time_logged)])
            
            cnxn.commit()
            
            # Update the logging time for the next check
            self.last_time_logged = last_time_logged
            
            if self.notifier:
                self.notifier.post()
            else:
                registry.get_logger().warn('TEAL notifier not configured.')
        
        cnxn.close()
        
    def _configure(self):
        ''' Prepare to run. This method will read the configuration file to
        get its operating parameters and figure out where it needs to start
        based on the last event it logged to TEAL
        '''
        # Set the polling time based on the LL Connector conf file
        cfg = registry.get_service(registry.SERVICE_CONFIGURATION)
        try:
            value = cfg.get(CONFIG_LL_TEAL, CONFIG_POLL_INTERVAL)
            self.poll_interval = int(value)
        except:
            registry.get_logger().debug('Configuring poll interval to {0} seconds'.format(LL_TEAL_DEFAULT_POLL_INTERVAL))            
            self.poll_interval = LL_TEAL_DEFAULT_POLL_INTERVAL
    
        # Set up the minimum message type
        try:
            value = cfg.get(CONFIG_LL_TEAL, CONFIG_MSG_TYPE)
            self.msg_type = LL_MSG_TYPES[value]
        except:
            registry.get_logger().debug('Configuring minimum message type to RAS_WARN')            
            self.msg_type = LL_TEAL_DEFAULT_MSG_TYPE

        self.LL_EVENT_QUERY = LL_EVENT_QUERY_STR.format(','.join(LL_EVENT_COLS),
                                                        LL_EVENT_TABLE,
                                                        LL_EVENT_ATTR_TIME_LOGGED,
                                                        LL_EVENT_ATTR_MSG_TYPE,
                                                        self.msg_type,
                                                        LL_EVENT_ATTR_TIME_LOGGED)
        
        # Find the highwater mark (time_logged) for the last LL event logged into TEAL
        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        cnxn = db.get_connection()
        cursor = cnxn.cursor()

        # First assume that the high watermark was stored in the site table
        db.select(cursor, 
                 [XCAT_SITE_VALUE], 
                  XCAT_SITE, 
                  where='${0} = ?'.format(XCAT_SITE_KEY), 
                  where_fields=[XCAT_SITE_KEY], 
                  parms=[XCAT_LL_CHKPT])

        # If it isn't there then try to figure out the max from what has already
        # been logged, otherwise just start at the beginning
        row = cursor.fetchone()
        if row is None or row[0] is None:
            max_time = db.select_max(cursor, LL_EVENT_ATTR_TIME_LOGGED, LL_TEAL_EXTDATA_TABLE).fetchone()
            if (max_time and max_time[0]):
                self.last_time_logged = max_time[0]
            
            # Initialize the checkpoint field in the site table so it is always there    
            db.insert(cursor, 
                      [XCAT_SITE_KEY, XCAT_SITE_VALUE, 'comments'], 
                      XCAT_SITE, 
                      [XCAT_LL_CHKPT, str(self.last_time_logged), 'teal_ll checkpoint - DO NOT DELETE OR MODIFY'])
            
            cnxn.commit()
        else:
            self.last_time_logged = long(row[0])

        # Quick test to see if the Loadleveler DB exists
        try:
            cursor.execute(self.LL_EVENT_QUERY, self.last_time_logged)
        except:
            registry.get_logger().exception("Error accessing Loadleveler tables")
            sys.exit("Error accessing Loadleveler tables")
            
        cnxn.close() 
        registry.get_logger().debug("Starting queries after time_logged = {0}".format(self.last_time_logged))
        
        # Set up notifier to TEAL
        self.notifier = teal_semaphore.Semaphore() 

    def _translate_event(self, ll_event):
        ''' Translate the LL event to a TEAL event
        '''    
        # This value will be split by second (10 digits) and microsecond (6 digits)
        sec = ll_event[LL_EVENT_COL_TIME_OCCURRED]/SECONDS_FACTOR
        time_occurred = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec))
        
        node = ll_event[LL_EVENT_COL_NODE].strip()
        
        src_comp = 'LL'
        job_step_id = ll_event[LL_EVENT_COL_JOB_STEP_ID]
        if  job_step_id:
            src_loc_type = 'J'
            src_loc = '{0}##{1}'.format(job_step_id, node)
        else:
            src_loc_type = 'A'
            subject = ll_event[LL_EVENT_COL_SUBJECT]
            if (subject):
                src_loc = '{0}##{1}'.format(node, subject)
            else:
                src_loc = node
        
        rpt_comp = 'LL'
        rpt_loc_type = 'A'
        reporter = ll_event[LL_EVENT_COL_REPORTER]
        if reporter:
            rpt_loc = string.replace(reporter.strip(),':','##')
        else:
            rpt_loc = node
            
        return (ll_event[LL_EVENT_COL_EVENT_ID], time_occurred, src_comp, src_loc_type, src_loc, rpt_comp, rpt_loc_type, rpt_loc, LL_TEAL_EXTDATA_V1_T1)
    
    def _log_event(self, db, cursor, ll_event):
        ''' Log event into TEAL event log. The LL event is actually a combination
        of common event data and LL specific data
        '''
        # Translate each event into a TEAL format
        teal_event = self._translate_event(ll_event)
        #print teal_event
        db.insert(cursor, LL_TEAL_COLS, db_interface.TABLE_EVENT_LOG, teal_event)
        
        # Rules assume detail is provided so set to empty string if not
        detail = ll_event[LL_EVENT_COL_DETAIL]
        if detail is None:
            detail = ''
        
        # Now add the LL extended data
        ll_extended_data = [ll_event[LL_EVENT_COL_TIME_OCCURRED],
                            ll_event[LL_EVENT_COL_TIME_LOGGED],
                            ll_event[LL_EVENT_COL_MSG_TYPE],
                            ll_event[LL_EVENT_COL_MESSAGE],
                            detail]
        
        db.insert_dependent(cursor,
                            LL_TEAL_EXTENDED_PK,
                            LL_TEAL_EXTENDED_COLS,
                            LL_TEAL_EXTDATA_TABLE,
                            ll_extended_data)
            
        registry.get_logger().debug("Logged event [{0},{1},{2}]".format(ll_event[LL_EVENT_COL_TIME_OCCURRED],
                                                                        ll_event[LL_EVENT_COL_EVENT_ID],
                                                                        ll_event[LL_EVENT_COL_NODE].strip()))

ll = None

def app_terminate(sig, stack_frame):
    ''' Catch the termination signals and shut down cleanly
    '''
    if ll:
        ll.stop()
    teal.app_terminate(sig, stack_frame)        
        
if __name__ == '__main__':
    
    parser = optparse.OptionParser()
    parser.add_option("-d", 
                      "--daemon",
                      help="run program as a daemon",
                      action="store_true",
                      dest="run_as_daemon",
                      default=False)
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
    
    if options.run_as_daemon:
        # Do the necessary processing to spin off as a daemon
        command.daemonize('teal_ll')
    else:
        # Allow the user to CTRL-C application and shutdown cleanly        
        signal.signal(signal.SIGINT, app_terminate)    # CTRL-C
    
    if options.log_file is None:
        log_file = '$TEAL_LOG_DIR/teal_ll.log'
    else:
        log_file = options.log_file

    try:        
        # Set up the TEAL environment to get at the data required for logging
        t = teal.Teal(None,
                      data_only=True,
                      msgLevel=options.msg_level,
                      logFile=log_file,
                      daemon_mode=options.run_as_daemon)
        
        LL_TEAL_EXTDATA_TABLE = extdata.extdata_fmt2table_name(LL_TEAL_EXTDATA_V1_T1)
            
        # Create the connector and start it
        ll = LoadLeveler()
        ll.start()
        while ll.isAlive():
            # Need to wait with timeout so signals can be received by the process
            ll.join(10000000)

        # If thread died with an exception then pass that along
        if ll.exception:
            raise ll.exception
                    
        # Wait for Teal to shutdown before exiting
        shutdown = registry.get_service(registry.SERVICE_SHUTDOWN)
        shutdown.wait()

    except SystemExit, se:
        raise    
    except:
        registry.get_logger().exception("Loadleveler connector failed")
        sys.exit(1)
