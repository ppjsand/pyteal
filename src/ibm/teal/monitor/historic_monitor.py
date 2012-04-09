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

import sys
from threading import Thread
from datetime import datetime, timedelta

from ibm.teal.monitor.event_monitor import EventMonitor
from ibm.teal import registry
from ibm.teal.database.db_interface import TABLE_EVENT_LOG
from ibm.teal.event import Event, EVENT_COLS, EVENT_ATTR_REC_ID,\
    EVENT_ATTR_TIME_OCCURRED
from ibm.teal.registry import get_logger, SERVICE_DB_INTERFACE, SERVICE_EVENT_Q, SERVICE_HISTORIC_QUERY, SERVICE_SHUTDOWN,\
    SERVICE_TIME_MODE
from ibm.teal.teal_error import ConfigurationError

class HistoricMonitor(EventMonitor):
    '''
    The historic monitor is used by an administrator or developer to analyze a specific set of events from the command line. 
    It can be used to validate rules, rerun with a specific set of events for recreation, or to analyze a set of events for 
    re-evaluation
    '''

    def __init__(self, config_dict):
        '''
        Constructor
        '''
        # Validate configuration parameters
        if config_dict['enabled'] != 'historic':
            raise ConfigurationError('Historic monitor can only enabled for historic use.  Unsupported value specified: {0}'.format(config_dict['enabled']))
        
        self.query = self._build_query()
        self.running = True # Set here so we don't run into timing issues in shutdown
        self.monitor_thread = Thread(group=None, target=self.start, name='event_monitor')
        self.monitor_thread.setDaemon(True)
        self.monitor_thread.start()
        pass
    
    def _build_query(self):
        ''' Create the query string from the passed in query during TEAL creation
        '''
        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        query = registry.get_service(SERVICE_HISTORIC_QUERY)
        
        if (query):
            where_str = query[0]
            where_fields = query[1]
        else:
            where_str = None
            where_fields = None
        
        # Check if should use occurred times, which means we need to order by them
        if registry.get_service(SERVICE_TIME_MODE) == 'time_occurred':
            order_str = EVENT_ATTR_TIME_OCCURRED
        else:
            order_str = EVENT_ATTR_REC_ID
        
        return db.gen_select(EVENT_COLS, TABLE_EVENT_LOG, where=where_str, where_fields=where_fields, order=order_str)

    def start(self):
        '''Start the historic monitor. Make one large query and iterate through each event that is returned
        passing it through the processing pipeline. A test will be made to quit if requested by the client.
        At the end of processing all events, a shutdown request will be submitted
        '''
        
        event_q = registry.get_service(SERVICE_EVENT_Q)
        dbi = registry.get_service(SERVICE_DB_INTERFACE)
        cursor = dbi.get_connection().cursor()
        
        disp_delta = timedelta(seconds=3) 
        disp_time = datetime.now() + disp_delta

        get_logger().debug('Historic query: {0}'.format(self.query))

        for row in cursor.execute(self.query):
            # Create the event from the database and post it to the event queue
            e = Event.fromDB(row)
            event_q.put(e)
                
            # Quit executing the loop if we are supposed to shut down
            if self.running == False:
                get_logger().info('Monitor event injection thread interrupted.  last recid = {0}'.format(row[0]))
                break
                
            # Display progress to the user
            cur_time = datetime.now()
            if cur_time >= disp_time:
                disp_time = cur_time + disp_delta
                print >>sys.stderr,'.',
                
        # If the program is still running, initiate a shutdown now that all requests have been submitted
        # to the processing pipeline
        if self.running:
            print >>sys.stderr
            registry.get_service(SERVICE_SHUTDOWN).notify()
                    
    
    def shutdown(self):
        '''Stop running the event monitor. 
        '''
        get_logger().debug('Starting shutdown')
        self.running = False
        
        get_logger().debug('Joining thread')
        self.monitor_thread.join()

        get_logger().debug('Shutdown complete')
        return

        