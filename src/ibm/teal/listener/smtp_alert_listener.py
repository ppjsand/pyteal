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

import smtplib
from string import Template
from email.mime.text import MIMEText

from ibm.teal.listener.alert_listener import AlertListener 
from ibm.teal.alert import ALERT_ATTR_CREATION_TIME, ALERT_ATTR_REC_ID, ALERT_ATTR_ALERT_ID, ALERT_ATTR_EVENT_LOC_TYPE, ALERT_ATTR_EVENT_LOC
from ibm.teal.alert import ALERT_ATTR_REASON, ALERT_ATTR_RECOMMENDATION
from ibm.teal.registry import get_logger
from ibm.teal.teal_error import ConfigurationError

class SmtpAlertListener(AlertListener):
    '''
    This listener will send an email message with a pre-canned alert message to the configured
    senders using SMTP
    '''

    def __init__(self, name, config_dict):
        '''
        Constructor
        '''
        if config_dict is None:
            raise ConfigurationError, 'SMTP Listener must have a configuration stanza'
        
        # Set debug level
        if 'debug_level' in config_dict:
            if config_dict['debug_level'] == 'true':
                self.debug_level = True
            else:
                self.debug_level = False
        else:
            self.debug_level = False
                
        # From: single user name
        if 'from' in config_dict:
            self.sender = config_dict['from']
        else:
            get_logger().error('SMTP sender not configured')
            raise ConfigurationError, 'SMTP sender not configured'
            
        # To: is a list of people to notify    
        if 'to' in config_dict:
            self.receivers = config_dict['to']
        else:
            get_logger().error('SMTP receivers not configured')
            raise ConfigurationError, 'SMTP receivers not configured'
        
        # Server is host:port
        if 'server' in config_dict:
            self.server = config_dict['server']
        else:
            get_logger().error('SMTP server not configured')
            raise ConfigurationError, 'SMTP server not configured'
        
        # If server login required
        if 'login' in config_dict:
            (self.uid,self.password) = config_dict['login'].split(':')
        else:
            self.uid = None
            self.password = None

        # User defined templates for subject and message body                        
        if 'subj_template' in config_dict:
            self.subj_template = Template(config_dict['subj_template'])
        else:
            self.subj_template = Template('${0} - ${1}:${2}'.format(ALERT_ATTR_ALERT_ID,
                                                                    ALERT_ATTR_EVENT_LOC_TYPE,
                                                                    ALERT_ATTR_EVENT_LOC))

        if 'body_template' in config_dict:
            self.body_template = Template(config_dict['body_template'].decode('string-escape'))
        else:
            self.body_template = Template('${0}\r\n\r\n${1}\r\n\r\n'.format(ALERT_ATTR_REASON,
                                                                        ALERT_ATTR_RECOMMENDATION))
        
        AlertListener.__init__(self,name,config_dict)
        
    def process_alert(self, alert):
        ''' Send an alert via email to the requested recipients
        '''
        alert_dict = alert.write_to_dictionary()
        
        msg = MIMEText(self.body_template.safe_substitute(alert_dict))
        msg['Subject'] = self.subj_template.safe_substitute(alert_dict)
        msg['Date'] = str(alert_dict[ALERT_ATTR_CREATION_TIME])
        msg['From'] = self.sender
        msg['To'] = self.receivers
        
        try:
            # Create the proper SMTP instance
            server = smtplib.SMTP()
            smtp_server = self.server

            # Connect to the server
            server.set_debuglevel(self.debug_level)
            server.connect(smtp_server)

            # Login, if required
            if self.uid:
                server.login(self.uid,self.password)
                
            # Send the alert to the intended recipients
            server.sendmail(self.sender,self.receivers.split(','),msg.as_string())
            
            # Disconnect from the server
            server.quit()
        except Exception,e:            
            get_logger().warn("Failed to send alert({0}) via SMTP: {1}".format(alert_dict[ALERT_ATTR_REC_ID],e))
        