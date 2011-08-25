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

import unittest
import smtpd
import email
import asyncore
import threading
import Queue

from ibm.teal import teal, registry, alert
from ibm.teal.metadata import META_ALERT_MSG_TEMPLATE
from ibm.teal.util.journal import Journal
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.registry import SERVICE_ALERT_DELIVERY_Q, SERVICE_ALERT_METADATA

SMTP_SERVER = ('127.0.0.1', 25000)

class TealSmtpTestserver(smtpd.SMTPServer):
    ''' SMTP Server class used to test messages sent from the SMTP Listeer '''
    def __init__(self, localaddr, remoteaddr):
        self.q = Queue.Queue()
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        
    def process_message(self, peer, mailfrom, rcpttos, data):
        self.q.put([mailfrom, rcpttos, data])
    
    def compare_messages(self, exp_msg_list):
        ''' Compare expected message [from, to, subject, payload] to actual'''
        match = True
        for exp_msg_info in exp_msg_list:
            act_msg_info = self.q.get(timeout=5)            
            msg =  email.message_from_string(act_msg_info[2])

            if ((act_msg_info[0] != exp_msg_info[0]) or
                (msg['From'] != exp_msg_info[0])):
                registry.get_logger().debug('From field mismatch: {0} != {1}'.format(act_msg_info[0], exp_msg_info[0]))
                match = False
                
            if ((', '.join(act_msg_info[1]) != exp_msg_info[1]) or
                (msg['To'] != exp_msg_info[1])):
                registry.get_logger().debug('To field mismatch: {0} != {1}'.format(act_msg_info[1], exp_msg_info[1]))
                match = False
            
            if msg['Subject'] != exp_msg_info[2]:
                registry.get_logger().debug('Subject field mismatch: {0} != {1}'.format(msg['Subject'], exp_msg_info[2]))
                match = False
                
            payload = msg.get_payload().replace('\r','').replace('\n','')
            if payload != exp_msg_info[3]:
                registry.get_logger().debug('Payload field mismatch: {0} != {1}'.format(payload, exp_msg_info[3]))
                match = False
                
        return match
    
def smtp_server_thread():
    ''' SMTP Server '''
    asyncore.loop()
    
def start_smtp_server():
    ''' This method is responsible for starting an SMTP server '''
    server = TealSmtpTestserver(SMTP_SERVER,None)
    t = threading.Thread(target=smtp_server_thread)
    t.setDaemon(True)
    t.start()
    return server

def gen_message_list(in_j):
    ''' Generate the expected message list for SMTP Listener'''
    metadata = registry.get_service(SERVICE_ALERT_METADATA)
    
    msg_list = []
    keys = in_j.keys()
    keys.sort()
    for key in keys:
        alert_dict = in_j[key].data_dict
        alert_id = alert_dict[alert.ALERT_ATTR_ALERT_ID]
        msg_list.append(['phil@us.ibm.com', 
                         'jim@us.ibm.com, mark@us.ibm.com, john@us.ibm.com',
                         '{0} - {1}:{2}'.format(alert_id,
                                                alert_dict[alert.ALERT_ATTR_EVENT_LOC_TYPE],
                                                alert_dict[alert.ALERT_ATTR_EVENT_LOC]),
                        '{0}{1}'.format(metadata[alert_id][META_ALERT_MSG_TEMPLATE],
                                        alert_dict[alert.ALERT_ATTR_RECOMMENDATION])])
    return msg_list

class SmtpAlertListenerTest(TealTestCase):
    def testSmtpAlertListener(self):
        ''' Test the SMTP Alert Listener '''
        server = start_smtp_server()
        
        t = teal.Teal('data/alert_listener_test/test_01.conf', msgLevel='warn', logFile='stderr', commit_alerts=False, commit_checkpoints=False)
        
        in_j = Journal('SMTP Journal', 'data/alert_test/inject_DQ_alerts.json')
        in_j.inject_queue(registry.get_service(SERVICE_ALERT_DELIVERY_Q))
        
        self.assertTrue(server.compare_messages(gen_message_list(in_j)))
        
        t.shutdown()

if __name__ == "__main__":
    unittest.main()