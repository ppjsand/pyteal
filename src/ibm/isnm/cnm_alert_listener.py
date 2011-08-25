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
import socket
import struct
import Queue
import threading 
from ibm.teal import registry
from ibm.teal.alert import raw_data2dict
from ibm.teal.listener.alert_listener import AlertListener
from ibm.teal.metadata import META_ALERT_CUST_NOTIFICATION, META_ALERT_CALL_HOME
from ibm.teal.registry import get_logger, SERVICE_DB_INTERFACE
from ibm.isnm.sfp_message import SfpCreateMessage

PORT = 3827              		# The same port as used by the server
SFP_RETRY_COUNT = 'sfp_retry_count'
CNM_TEST_LISTENER_LOG_ONLY = 'CNM_TEST_LISTENER_LOG_ONLY'


#==========================================================================
# The CNM Alert Listener
#==========================================================================
class CnmAlertListener(AlertListener):
    '''
    This listener is responsible for converting TEAL Alerts into Service Focal Point (SFP)
    Error Log packets and sending them to the Service Focal Point
    
    When initialized it sets up a permanent socket to the HMC (primary or secondary)
    
    '''

    #======================================================================
    # ISNM Alert Listener that reports alerts to Service Focal Point (SFP)
    #    - Check to see if the CNM_TEST_LISTENER_LOG_ONLY is set.
    #    - Get the retry count for sending alerts to SFP
    #    - Get the Primary and Backup HMC addresses
    #    - Get the Client name
    #    - Open the connection to the HMC
    #======================================================================
    def __init__(self, name, config_dict=None):
        '''	Constructor '''
        AlertListener.__init__(self, name, config_dict)

        # Check if environment variable is set to allow testing when an HMC isn't present
        self.log_only = (os.environ.get(CNM_TEST_LISTENER_LOG_ONLY, 'N') != 'N')

        # Try to get the retry count from configuration
        if config_dict is None or SFP_RETRY_COUNT not in config_dict:
            self.sfp_retry_count = 5
        else:
            self.sfp_retry_count = config_dict[SFP_RETRY_COUNT]
            
        # Get addresses for HMCs
        db = registry.get_service(SERVICE_DB_INTERFACE)
        connection = db.get_connection()
        cursor = connection.cursor()
        self.hmc_primary_addr = self._get_hmc_address(db, cursor, 'ea_primary_hmc')
        self.hmc_backup_addr = self._get_hmc_address(db, cursor, 'ea_backup_hmc')
        connection.close()
        self.hmc_connected = False
        
        # Setup client name 
        self.client_name = socket.gethostname() + ":cnm_alert_listener"
        
        # Get initial connection
        self.hmc_using_addr = self.hmc_primary_addr    # Which HMC were using to know where to start retries

        self.queue = Queue.Queue()
        
        self.condition = threading.Condition()

        self.running = True # Set here so we don't run into timing issues in shutdown
        self.process_thread = threading.Thread(group=None,target=self.start,name='alert_processor')
        self.process_thread.setDaemon(True)
        self.process_thread.start()
	
        return 

    #======================================================================
    # Connect to the HMC so alerts can be sent to SFP
    #    - Open the connection to the Primary or Backup HMC, if the
    #      packet fails to be sent to Service Focal Point (SFP)
    #======================================================================
    def _connect_to_hmc(self):
        ''' Connect to the HMC '''
            
        if self.hmc_using_addr == self.hmc_primary_addr:
            # Try primary 
            if self._try_to_connect(self.hmc_primary_addr) == True:
                get_logger().info('Connected to primary HMC')
                self.hmc_connected = True
                return 
            # Try backup 
            if self._try_to_connect(self.hmc_backup_addr) == True:
                self.hmc_using_addr = self.hmc_backup_addr
                self.hmc_connected = True
                get_logger().info('Connected to secondary HMC')
                return
        else:
            # Try backup 
            if self._try_to_connect(self.hmc_backup_addr) == True:
                self.hmc_connected = True
                get_logger().info('Connected to secondary HMC')
                return
            # Try primary 
            if self._try_to_connect(self.hmc_primary_addr) == True:
                self.hmc_connected = True
                self.hmc_using_addr = self.hmc_primary_addr
                get_logger().info('Connected to primary HMC')
                return 
            
        # Neither worked
        get_logger().info('Unable to connect to HMC')
        self.hmc_using_addr = self.hmc_primary_addr   # Start with primary next time
        return
    
    #======================================================================
    # Try to connect to the HMC so alerts can be sent to SFP
    #======================================================================
    def _try_to_connect(self, address):
        ''' Try to connect to the address for the number of retries '''
        if address is None:
            return False
        retries_left = self.sfp_retry_count
        while retries_left > 0:
            try:
                self.sock.connect((address, PORT))
                return True
            except socket.error:
                get_logger().exception('Socket connect to {0} failed -- retries left {1}'.format(address, retries_left))
                retries_left -= 1 
        return False
    
    #======================================================================
    # Get the IP address of the HMC (Primary or Backup)
    #======================================================================
    def _get_hmc_address(self, db, cursor, key):
        ''' Get address for entry for key from xCAT DB ''' 
        hmc_address = None
        db.select(cursor, ['value'], 'site', where='$key = ?', where_fields=['key'], parms=(key,))
        val = cursor.fetchone()
        if val and val[0]:
            hmc_address = val[0]
            get_logger().debug('Address found for {0} is {1}'.format(key, hmc_address))
        else:
            get_logger().debug('Address not found for {0}'.format(key))
        return hmc_address
    
    #======================================================================
    # Process the Alert, so it is ready to be sent to SFP
    #======================================================================
    def process_alert(self, alert):
        ''' Convert the alert to a service focal point log and send to the service focal point
    	'''
        get_logger().debug('In cnm_alert_listener')
        self.queue.put(alert, True)
        
        return
    
    #======================================================================
    # Process the Alert, so it is ready to be sent to SFP
    #======================================================================
    def send_alert_tosfp(self, alert):
        ''' Convert the alert to a service focal point log and send to the service focal point
    	'''

        get_logger().debug('In send_alert_tofsp')

        #==================================================================
        #  Parameters for build() call, which will build the SFP message.
        #       self, alert, client_name, fru_list, notif_type,
        #       enc_mtms, pwr_mtms, neighbor_list, eed_location,
        #       extended_data
        #==================================================================
        self.raw_data_dict = raw_data2dict(alert.raw_data)
        if 'fru_list' in self.raw_data_dict: 
            fru_list = self.raw_data_dict['fru_list']
            frus = str(fru_list).replace('{','').rstrip('}').split('},')
            get_logger().debug('There is a fru list in the raw data dict.')
        else:
            frus = []
            get_logger().debug('There is no fru list in the raw data dict.')

        if 'encl_mtms' in self.raw_data_dict: 
            enclos_mtms = str(self.raw_data_dict['encl_mtms'])
            get_logger().debug('Enclosure MTMS = {0}'.format(enclos_mtms))
        else:
            enclos_mtms = []
            get_logger().debug('There is no Enclosure MTMS in the raw data dict.')
            
        if 'pwr_enc' in self.raw_data_dict: 
            pwr_mtms = str(self.raw_data_dict['pwr_enc'])
            get_logger().debug('Power Enclosure MTMS = {0}'.format(enclos_mtms))
        else:
            pwr_mtms = []
            get_logger().debug('There is no Power MTMS in the raw data dict.')
 
        notif_type = 0
        cust_notif = alert.get_metadata()[META_ALERT_CUST_NOTIFICATION]
        if (cust_notif == 'Y'):
            notif_type = 1

        call_home = alert.get_metadata()[META_ALERT_CALL_HOME]

        #==================================================================
        # If call_home is not set, then set to a default
        #==================================================================
        if (call_home == 'Y'):
            notif_type |= 16       
        
        if 'nbr_loc' in self.raw_data_dict and 'nbr_typ' in self.raw_data_dict: 
            neighbor_list = ['{0}:{1}'.format(self.raw_data_dict['nbr_typ'], self.raw_data_dict['nbr_loc'])]
        else:
            neighbor_list = []

        if 'eed_loc' in self.raw_data_dict: 
            eed_location = str(self.raw_data_dict['eed_loc'])
        else:
            eed_location = ""

        extended_data = ""
        
        #get_logger().debug('FRUs           = {0}'.format('\n'.join([str(fru) for fru in frus])))
        get_logger().debug('    Power MTMS = {0}'.format(pwr_mtms))
        get_logger().debug(' Neighbor list = {0}'.format(neighbor_list))
        get_logger().debug('  EED location = {0}'.format(eed_location))

        msg = SfpCreateMessage()
        pkt = msg.build(alert, self.client_name, frus, notif_type, enclos_mtms, 
                        pwr_mtms, neighbor_list, eed_location, extended_data)
        
        #==================================================================
        # The following is for DEBUGING
        #==================================================================
        #pkt_file = open('/tmp/create_msg.txt', 'a')
        #print >>pkt_file,pkt
        #pkt_file.close()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._connect_to_hmc()

        #==================================================================
        # Try to send the Packet to SFP, the number of times specified in
        # in self.sfp_retry_count
        #==================================================================
        if (self.hmc_connected == True):
            retries_left = self.sfp_retry_count
            while retries_left > 0: 
                try: 
                    rc = self.sock.send(pkt)
                    if  rc == 0 :
                         get_logger().exception('send failed.')
                    else:
                         get_logger().debug('The message has been sent to SFP of size {0}'.format(rc))
                    break 
                except:
                    retries_left -= 1
                    get_logger().exception('send failed.  Retries left {0}'.format(retries_left))
                    self._connect_to_hmc()

            #==================================================================
            # Check the data returned from the send
            #==================================================================
            data = self.sock.recv(10)
            msg_ver, status, seq_num = struct.unpack('>BBQ', data)
            get_logger().debug('Message Version = {0}'.format(msg_ver))
            get_logger().debug('         Status = {0}'.format(status))
            get_logger().debug('Sequence number = {0}'.format(seq_num))

            #==================================================================
            # Check the status returned:
	    #    0  - Success the message has been sent to SFP
	    #    1  - Message was not sent because of bad formatting
	    #    2  - Message was not sent because of a duplicate sequence num
            #==================================================================
            if (status == 0):
                get_logger().debug('The message has been sent to Service Focal Point')
            elif (status == 1):
                get_logger().warning('The message has not been sent to Service Focal Point, because of bad formatting')
            elif (status == 2):
                # TODO: If 2 need to resend with the next sequence # 
                get_logger().warning('The message has not been sent to Service Focal Point, because of duplicate sequence number')
            else:
                get_logger().warning('The message has not been sent to Service Focal Point, because of a connection loss')
            self.hmc_connected = False
        else:
            get_logger().warning('The message has not been sent to Service Focal Point, because of no connection to the HMC.')
            get_logger().warning('Here is the Alert Data:')
            get_logger().warning('          Alert = {0}'.format(alert))
            get_logger().warning('    Client Name = {0}'.format(self.client_name))
            get_logger().warning('           FRUs = {0}'.format(frus))
            get_logger().warning('    Notify Type = {0}'.format(notif_type))
            get_logger().warning(' Enclosure MTMS = {0}'.format(enclos_mtms))
            get_logger().warning('     Power MTMS = {0}'.format(pwr_mtms))
            get_logger().warning('  Neighbor List = {0}'.format(neighbor_list))
            get_logger().warning('   EED Location = {0}'.format(eed_location))
            get_logger().warning('  Extended Data = {0}'.format(extended_data))

        self.sock.shutdown(socket.SHUT_RDWR)
        return

    #======================================================================
    # Process the Alert, so it is ready to be sent to SFP
    #======================================================================
    def start(self):
        '''The Alert is extracted from Alert queue and processed.
           The processing subsequent alerts are delayed for 6 seconds 
           before processing them .
        '''

        get_logger().info('Starting Alert processing Thread')
        while self.running:
           item = self.queue.get(True)
           get_logger().debug('Got Alert from Queue')
           self.send_alert_tosfp(item)

           self.condition.acquire()

           # Wait 6 secs before processing next alert.
           self.condition.wait(6.0)

           self.condition.release()

        return

    def shutdown(self):
        '''Stop running the event monitor.
        '''
        get_logger().debug('Starting shutdown')
        self.running = False

        get_logger().debug('Joining thread')
        self.process_thread.join()

        get_logger().debug('Shutdown complete')
        return

