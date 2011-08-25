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

import os
import csv
import json
import sys

from ibm.teal.listener.alert_listener import AlertListener
from ibm.teal.registry import get_service,get_logger,TEAL_LOG_DIR
from ibm.teal.alert import ALERT_COLS_SELECT, ALERT_ATTR_REASON, ALERT_ATTR_RECOMMENDATION, ALERT_ATTR_RAW_DATA
from ibm.teal.util import command

class FileAlertListener(AlertListener):
    ''' Write an alert to a file
    '''

    def __init__(self, name, config_dict):
        '''
        Constructor
        '''
        AlertListener.__init__(self,name,config_dict)
        
        if config_dict is not None and 'format' in config_dict:
            self.formatter = config_dict['format']
            if self.formatter in ['json','csv','text','brief']:
                pass
            else:
                get_logger().warn('Invalid formatter specified: {0}. Defaulting to csv'.format(self.formatter))
                self.formatter = "csv"
        else:
            self.formatter = "csv"
            
        if config_dict is not None and 'file' in config_dict:
            self.file_name = config_dict['file']
        else:
            log_dir = get_service(TEAL_LOG_DIR)
            self.file_name = os.path.join(log_dir,'tealalert.log')

        if config_dict is not None and 'mode' in config_dict:
            cfg_mode = config_dict['mode']
            if cfg_mode == 'append':
                mode = "a"
            elif cfg_mode == 'write':
                mode = 'w'
            else:        
                get_logger().warn('Invalid mode specified: {0}. Defaulting to "append"'.format(mode))
                mode = 'a'                
        else:
            mode = 'a'
            
        try:
            if self.file_name == 'stderr':
                self.file = sys.stderr
            elif self.file_name == 'stdout':
                self.file = sys.stdout
            else:
                self.file = open(self.file_name, mode)
                
            if self.formatter == 'csv':
                self.writer = csv.DictWriter(self.file, ALERT_COLS_SELECT,extrasaction='ignore')
                get_logger().info("CSV Headings: {0}".format(ALERT_COLS_SELECT))
        except IOError,e:
            get_logger().error('Could not open {0}: {1}'.format(self.file_name,e))
            self.file = None    

         
    def process_alert(self, alert):
        ''' Process the alert by writing it to a file in the configured format
        '''
        if not self.file:
            return
        
        alert_dict = alert.write_to_dictionary()
        
        if self.formatter == 'json':        
            json.dump(alert_dict, self.file, cls=command.JSONEventEncoder)
            print >>self.file
        
        elif self.formatter == 'csv':
            alert_dict[ALERT_ATTR_REASON] = alert_dict[ALERT_ATTR_REASON].replace('\n','').replace('\r','')
            alert_dict[ALERT_ATTR_RECOMMENDATION] = alert_dict[ALERT_ATTR_RECOMMENDATION].replace('\n','').replace('\r','')
            if ALERT_ATTR_RAW_DATA in alert_dict and alert_dict[ALERT_ATTR_RAW_DATA]:
                alert_dict[ALERT_ATTR_RAW_DATA] = alert_dict[ALERT_ATTR_RAW_DATA].replace('\n','').replace('\r','')

            self.writer.writerow(alert_dict)
            
        elif self.formatter == 'brief':
            print >>self.file, alert.as_line()
         
        else: # text
            print >>self.file, '==================================================='
            for col in ALERT_COLS_SELECT:
                print >>self.file, col, ':', alert_dict.get(col,None)
        
        self.file.flush()