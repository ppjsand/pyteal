#!/usr/bin/env python

import time
import signal
import threading
import optparse
import string
import sys
import os
import json
import re
import socket
import select
import Queue
import copy
import commands

from ibm.teal import teal
from ibm.teal import registry
from ibm.teal import event
from ibm.teal import extdata
from ibm.teal.database import db_interface
from ibm.teal.util import command
from time import strftime, gmtime
from ibm.teal.monitor import teal_semaphore


# TEAL DB Information for Infiniband
IB_TRAP_ATTR_TRAP_OID = 'snmpTrapOID.0'
IB_TRAP_ATTR_SEVERITY = 'volIbSmaNotificationObjects.1'
IB_TRAP_ATTR_CATEGORY = 'volIbSmaNotificationObjects.2'
IB_TRAP_ATTR_TIME_OCCURRED = 'volIbSmaNotificationObjects.3'
IB_TRAP_ATTR_SOURCE = 'volIbSmaNotificationObjects.4'
IB_TRAP_ATTR_EVENT_ID = 'volIbSmaNotificationObjects.5'
IB_TRAP_ATTR_DESCRIPTION = 'volIbSmaNotificationObjects.6'
IB_TRAP_ATTRS = {IB_TRAP_ATTR_TRAP_OID:"",
                 IB_TRAP_ATTR_SEVERITY:"",
                 IB_TRAP_ATTR_CATEGORY:"",
                 IB_TRAP_ATTR_TIME_OCCURRED:"",
                 IB_TRAP_ATTR_SOURCE:"",
                 IB_TRAP_ATTR_EVENT_ID:"",
                 IB_TRAP_ATTR_DESCRIPTION:""
                }

IB_TEAL_COLS = (event.EVENT_ATTR_EVENT_ID,
                event.EVENT_ATTR_TIME_OCCURRED,
                event.EVENT_ATTR_SRC_COMP,
                event.EVENT_ATTR_SRC_LOC_TYPE,
                event.EVENT_ATTR_SRC_LOC,
                event.EVENT_ATTR_RPT_COMP,
                event.EVENT_ATTR_RPT_LOC_TYPE,
                event.EVENT_ATTR_RPT_LOC,
                event.EVENT_ATTR_RAW_DATA_FMT
                )

UFM_EVENT_PREFIX = 'UFM00'
IB_TEAL_SRC_COMP = 'IB'
IB_TEAL_RPT_COMP = 'TEAL'
IB_TEAL_RPT_LOC_TYPE = 'A'
IB_TEAL_MAX_KEY = (IB_TEAL_COLS[2], IB_TEAL_COLS[5], IB_TEAL_COLS[6],IB_TEAL_COLS[7])            
IB_TEAL_MAX_KEY_VALUE = (IB_TEAL_SRC_COMP, IB_TEAL_RPT_COMP, IB_TEAL_RPT_LOC_TYPE)    


IB_TRAP_SRC_LOCS = {"Grid":"G",
                    "Computer":"C",
                    "Device":"D",
                    "Module":"M",
                    "VM":"V",
                    "Environment":"E",
                    "Gateway":"GW",
                    "LogicalServer":"LS",
                    "VMM":"VM",
                    "Site":"S",
                    "Switch":"SW",
                    "Line":"L",
                    "Spine":"SP",
                    "PSU":"PS",
                    "SMB":"SM",
                    "Fan":"F"
                   }
ib_prefix = lambda x: IB_TRAP_SRC_LOCS.get(x)

IB_MODULE_TYPES = {"sFU2204":"Fan",
                   "sFU2004":"Fan",
                   "sFU":"Fan",
                   "sFU-8500H":"Fan",
                   "sFU1u":"Fan",
                   "sFU40H":"Fan",
                   "sFU4":"Fan",
                   "sFU40V":"Fan",
                   "sFU42H":"Fan",
                   "sFU42V":"Fan",
                   "sFU4_MOD":"Fan",
                   "sFU8":"Fan",
                   "sFU8_MOD":"Fan",
                   "sPSU1u":"PSU",
                   "sPSUS":"PSU",
                   "sMB":"SMB",
                   "sMBANE2012":"SMB",
                   "sMBCM":"SMB",
                   "Line":"Line",
                   "IS5001":"Line",
                   "SX6001":"Line",
                   "sLB-1024":"Line",
                   "sLB2024":"Line",
                   "sLB24":"Line",
                   "sLB24D":"Line",
                   "sLB4018":"Line",
                   "sLB8_12":"Line",
                   "sRB20210G":"Line",
                   "sRBD":"Line",
                   "sRBD20":"Line",
                   "sRBDD":"Line",
                   "Spine":"Spine",
                   "IS5002":"Spine",
                   "SX6002":"Spine",
                   "sFB":"Spine",
                   "sFB-8500":"Spine",
                   "sFB12":"Spine",
                   "sFB12D":"Spine",
                   "sFB2004":"Spine",
                   "sFB2012":"Spine",
                   "sFB4":"Spine",
                   "sFB4200":"Spine",
                   "sFB4700":"Spine",
                   "sFB4700x2":"Spine",
                   "sFB4D":"Spine"
                  }

MAX_RETRY_TIME = 2

# TEAL Extended Data Information
IB_TEAL_EXTDATA_V1_T1 = 0x4942000080010001L
IB_TEAL_EXTENDED_PK = 'rec_id'
IB_TEAL_EXTENDED_COLS = ['severity',                 
                         'category',
                         'description'
                        ]

IB_TRAP_SEVERITY = ('cleared',
                    'indeterminate',           
                    'critical',
                    'major',
                    'minor',             
                    'warning'
                   )

IB_TRAP_CATEGORY = ('Unknown',
                    'Hardware',           
                    'Traffic',
                    'TrafficConfiguration',
                    'TrafficNotification',
                    'FabricTopology',
                    'FabricConfiguration',
                    'FabricNotification',
                    'CommunicationError',
                    'ModuleStatus',
                    'EnvironmentNotification',
                    'UFMServer',
                    'Maintenance',
                    'LogicalModel',
                    'Gateway'
                   )

# Configuration Parameters
CONFIG_IB_TEAL = 'connector.infiniband'
CONFIG_POLL_INTERVAL = 'poll_interval'
CONFIG_REMOTE_SHELL = 'remote_shell'
CONFIG_UFM_TRAP = 'ufm_event_filter'

# Default value of Parameters 
IB_TEAL_DEFAULT_POLL_INTERVAL = 30
IB_TEAL_DEFAULT_REMOTE_SHELL = '/opt/xcat/bin/xdsh'

# XCAT Table definitions
XCAT_SITE = 'site'
XCAT_SITE_KEY = 'key'
XCAT_SITE_VALUE = 'value'

XCAT_NODE = 'nodelist'
XCAT_NODE_KEY = 'groups'
XCAT_NODE_VALUE = "'%ufm%'"

UFM_CKPT_PREFIX = 'tlufm_ckpt_'

# IB connector instance
ib = None

SOCKET_FILE = '/tmp/tlibsocket'

CHECK_UFM_CMD = 'service ufmd status >/dev/null 2>&1; echo $?'

# Event log related
TRAP_CMD = 'python /opt/ufm/scripts/eventlog_filter.py'
CURRENT_LOG_DIR = '/opt/ufm/files/log'
CURRENT_LOG_NAME = 'event.log'
CURRENT_LOG = CURRENT_LOG_DIR + '/' + CURRENT_LOG_NAME

# Status of UFM server
STATUS_UP = 'Running'
STATUS_DOWN = 'Stopped'
STATUS_UNKNOWN = 'Unknown'

IB_TEAL_UFM_TRAP_HANDLER = 'tlufmtraphandler.py'

def _debug(message):
    try:
        thread_name = thread_dict[threading.currentThread()]
    except:
        thread_name = 'Unknown'
    msg = "<Thread:{0}>".format(thread_name) + message
    if not logger:
        mylogger = registry.get_logger()
    else:
        mylogger = logger
    mylogger.debug(msg)

def _warn(message):
    try:
        thread_name = thread_dict[threading.currentThread()]
    except:
        thread_name = 'Unknown'
    msg = "<Thread:{0}>".format(thread_name) + message
    if not logger:
        mylogger = registry.get_logger()
    else:
        mylogger = logger
    mylogger.warn(msg)

def _error(message):
    try:
        thread_name = thread_dict[threading.currentThread()]
    except:
        thread_name = 'Unknown'
    msg = "<Thread:{0}>".format(thread_name) + message
    if not logger:
        mylogger = registry.get_logger()
    else:
        mylogger = logger
    mylogger.error(msg)

def _exception(message):
    try:
        thread_name = thread_dict[threading.currentThread()]
    except:
        thread_name = 'Unknown'
    msg = "<Thread:{0}>".format(thread_name) + message
    if not logger:
        mylogger = registry.get_logger()
    else:
        mylogger = logger
    mylogger.exception(msg)

def _info(message):
    try:
        thread_name = thread_dict[threading.currentThread()]
    except:
        thread_name = 'Unknown'
    msg = "<Thread:{0}>".format(thread_name) + message
    registry.get_logger().info(msg)

'''An approach to achieve recv_all()'''
End='end_of_ufm_msg'
def recv_end(the_socket):
    total_data=[];
    data=''
    while True:
        data=the_socket.recv(8192)
        # No data means remote socket is closed
        if not data:
            total_data.append(data)
            break
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data)>1:
           #check if end_of_data was split
            last_pair=total_data[-2]+total_data[-1]
            if End in last_pair:
                total_data[-2]=last_pair[:last_pair.find(End)]
                total_data.pop()
                break
    return ''.join(total_data)

"""execute commands on UFM via remote shell""" 
def remote_execute(server,rsh,cmd):
    cmd =  rsh + ' ' + server + ' -l root ' + "'" + cmd + "'"
    _debug('command is {0}'.format(cmd))
    lines = []
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0 :
        lines = output.split('\n')
    else:
        _error('Invoke command on UFM server {0} failed.'.format(server))
    return lines

"""check UFM server status"""
def check_ufm_status(server,rsh):
    try:
        rec = remote_execute(server, rsh, CHECK_UFM_CMD)
    except:
        _error("Error to check UFM server's status")
        return STATUS_UNKNOWN

    if rec == []:
        _error("Fail to check UFM server's status")
        return STATUS_UNKNOWN

    rc = rec[0]
    if re.match('.*xdsh',rsh):
        rc = rc.replace(server + ': ','',1)

    if rc == '0':
        return STATUS_UP
    elif rc == '3':
        return STATUS_DOWN
    else:
        _warn("Unknown UFM status")
        return STATUS_UNKNOWN

class ufm_server():
    def __init__(self,server,poll_interval,rsh,last_ufm_status,last_time_logged,first_trap):
        # server name
        self.svr = server
        # remote shell to poll ufm
        self.rsh = rsh 
        # the traps polled out when launch
        self.first_traps = first_trap
        # the traps polled out when running
        self.traps = None
        # polling interval
        self.poll_interval = poll_interval
        # Last UFM server status
        self.last_ufm_status = last_ufm_status
        # Last logged trap's occur time
        self.last_time_logged = last_time_logged
        # retry counter
        self.retry_cnt = 0
        # TEAL notifier
        self.notifier = None
        # Running or not
        self.running = True
        # polled out trap queue
        self.queue = Queue.Queue(-1)
        # cached trap queue
        self.cqueue = Queue.Queue(-1)

        # Set thread processing traps from UFM captured by xCAT
        self.processor = MyThread(self._process_traps,(), 'processor_of_' + self.svr)

        # Set thread timing poll
        self.timer = MyThread(self._timer,(), 'timer_of_' + self.svr)

        # Set thread doing poll from UFM
        self.poller = MyThread(self._poller,(), 'poller_of_' + self.svr)

        # Set event to control timer
        self.tevt = threading.Event()

        # Set event to control poller
        self.pevt = threading.Event()

        # Set event to control queue
        self.qevt = threading.Event()

        # Set up notifier to TEAL
        self.notifier = teal_semaphore.Semaphore()
      
        # Set up DB connection
        self.db = registry.get_service(registry.SERVICE_DB_INTERFACE)
      
        # Set up check point prefix
        self.ckpt = UFM_CKPT_PREFIX + self.svr

    """thread to poll ufm""" 
    def _poller(self):
        while self.poller.running:
            if self.pevt.isSet():
                self.pevt.clear()
            self.pevt.wait()
            """judge stop or scheduled poll"""
            if not self.tevt.isSet():
                self.poll_doer()
                self.pevt.clear()
        msg = 'Poller stopped'
        _debug(msg)

    """thead to control polling interval""" 
    def _timer(self):
        logger = registry.get_logger()
        while self.timer.running:
            if not self.tevt.isSet() :
                _debug('Scheduled polling')            
                self.pevt.set()                                  
            self.tevt.wait(self.poll_interval)
        msg = 'Timer stopped'
        #logger.debug(msg)
        _debug(msg)

    """method to log trap data stored in a dict""" 
    def _process_new_xcattraps(self, dict):
        # if there is no scheduled polling, refresh immediately
        if self.queue.empty():
            if not dict[IB_TRAP_ATTR_TIME_OCCURRED] > self.last_time_logged:
                msg = "Trap already logged, ignore!"
                _debug(msg)
                return
            self.pevt.set()
            msg = "New trap comes and refresh polling!"
            _info(msg)
        # if there is a scheduled polling
        else:
            self.cqueue.put_nowait(jstr)
            msg = "There is a undergoing polling, cache this new trap for later processing!"
            _info(msg)

    """method to log traps""" 
    def _log_traps(self, event, ext_data):
        _debug('Logging event {0}, ext data {1}'.format(event,ext_data))
        try:
            self.cnxn = self.db.get_connection()
            self.teal_cursor = self.cnxn.cursor()
            self.db.insert(self.teal_cursor, IB_TEAL_COLS, db_interface.TABLE_EVENT_LOG, event)
            self.db.insert_dependent(self.teal_cursor, IB_TEAL_EXTENDED_PK, IB_TEAL_EXTENDED_COLS, IB_TEAL_EXTDATA_TABLE, ext_data)
            # Status related events also need a update of site table
            if event[0] == 'MX060001' or event[0] == 'MX060002' or event[0] == 'MX060003':
                self.db.update(self.teal_cursor,
                              [XCAT_SITE_VALUE,'disable'],
                               XCAT_SITE,
                               where="${0} = '{1}'".format(XCAT_SITE_KEY, self.ckpt),
                               where_fields=[XCAT_SITE_KEY],
                               parms=[str(event[1]),str(self.last_ufm_status)])
            else:
                self.db.update(self.teal_cursor,
                              [XCAT_SITE_VALUE],
                               XCAT_SITE,
                               where="${0} = '{1}'".format(XCAT_SITE_KEY, self.ckpt),
                               where_fields=[XCAT_SITE_KEY],
                               parms=[str(event[1])])

            self.cnxn.commit()
            # Update the logging time for the next check
            self.last_time_logged = str(event[1])
            # Notify TEAL that events have been inserted
            if self.notifier:
                self.notifier.post()
            else:
                _warn('TEAL notifier not configured.')
        except:
            # Don't attempt to commit anything since we had an error processing the events
            _exception("Error processing new events")
            self.cnxn.rollback()

        self.cnxn.close()
        
    """thead to prcoess traps""" 
    def _process_traps(self):
        while self.processor.running:
            if self.queue.empty() and self.cqueue.empty():
                self.qevt.clear()
                self.qevt.wait()
            if self.queue.empty() and not self.cqueue.empty():
                # traps from xCAT
                tmp = self.cqueue.get(False)
                if not tmp.__class__.__name__ == 'dict':
                    msg = "Unrecognized item in cached queue!"
                    _error(msg)
                    continue
                if not tmp[IB_TRAP_ATTR_TIME_OCCURRED] < self.last_time_logged:
                    msg = "New trap received, refresh!"
                    _debug(msg)
                    self.pevt.set()                 
                else:                                                                
                    msg = "Trap already logged! skip...."
                    _debug(msg)
                continue                               
            if self.queue.empty():
                # terminate now...
                break
            tmp = self.queue.get(False)           
            # traps from UFM
            self._translate_UFM_traps(tmp)
            msg = 'Processed a trap at: '
            msg += strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            _debug(msg)
        msg = 'Processor stopped'
        _debug(msg)

    """
     handle ufm status related event
         type_id=1 means ufm is abnormal
         type_id=2 means ufm is down
         type_id=3 means ufm is up
    """
    def handle_ufm_status_event(self, occur_time, type_id):
        src_loc_type = ''
        rpt_loc_type = 'A'
        rpt_comp     = 'TEAL'
        src_comp     = 'UFM'
        time_occured = occur_time
        src_loc_type = 'A'
        rpt_loc      = socket.gethostname() + '##' + str(os.getpid())
        src_loc      = self.svr
        if type_id == '1':
            event_id     = 'MX060001'
            severity     = 'Warning'
            description  = 'UFM server is abnormal.'
        elif type_id == '2':
            event_id     = 'MX060002'
            severity     = 'Fatal'
            description  = 'UFM server is down. Please try to bring it up.'
        elif type_id == '3':
            event_id     = 'MX060003'
            severity     = 'Informational'
            description  = 'UFM server is up.'
        else:
            msg = 'Unknown event.'
            _error(msg)
            return
        teal_event = (event_id, time_occured, src_comp, src_loc_type, src_loc, rpt_comp, rpt_loc_type, rpt_loc, IB_TEAL_EXTDATA_V1_T1)
        extended_data = (severity, '', description)
        self._log_traps(teal_event, extended_data)

    """Check if a UFM traps should be filter out""" 
    def check_filter(self, trap):
        if ib.filter_dict == {}:
            return trap    
        else:
            for k in ib.filter_dict.keys():
                if ib.filter_dict[k]:
                    try:
                        str = re.match(ib.filter_dict[k], trap[k])
                        if str:
                            _debug("Trap {0} hits the filter {1}, ignore it....".format(trap[k],ib.filter_dict[k]))
                            return {}
                    except:
                        _warn("Bad regular expresion {0} found in configuration, treat it as a non-effective filter...".format(ib.filter_dict[k]))
        return trap

    """Parse UFM traps into a dict and check if it should be filtered out""" 
    def _handle_UFM_traps(self, trap):
        result               = trap.split(' [')
        dict                 = {}
        if not len(result) == 5:
            _error('unrecognized traps {0} received!'.format(trap))
            return dict
        if not result[0] > self.last_time_logged:
            msg = "Older than lastest logged time {0}, already logged, skip....".format(self.last_time_logged)
            _debug(msg)
            return dict
        '''
        result[0] = 2012-04-18 17:16:27.376
        result[1] = 313]
        result[2] = 64] INFO
        result[3] = Fabric_Notification] Site 
        result[4] = default(15) / NA / NA / NA]: GID Address In Service: prefix fe80000000000001,guid 0002c9030034c7f1
        '''
        dict['time_occured'] = str(result[0])
        '''
        313] [64] INFO [Fabric_Notification] Site [default(15) / NA / NA / NA]: GID Address In Service: prefix fe80000000000001,guid 0002c9030034c7f1
        '''
        dict['id']           = str(result[1].split(']')[0])
        result1              = result[2].split('] ')
        dict['event_id']     = str(result1[0])
        dict['severity']     = str(result1[1])
        result2              = result[3].split('] ')
        dict['category']     = str(result2[0].replace('_',' '))
        dict['type']         = str(result2[1])
        result3              = result[4].split(']: ')
        dict['src']          = str(result3[0])
        dict['description']  = str(result3[1])
        # start to check if it hits the filter expression
        dict = self.check_filter(dict)
        return dict

    """Log on UFM server and get device type via ibnodes command""" 
    def get_dev_type(self, dev):
        shell_command = '/usr/sbin/ibnodes | grep "{0}" | cut -d: -f1 | tr -d "\t"'.format(dev)
        cmd = self.rsh + ' ' + self.svr + ' -l root ' + "'" + shell_command + "'"
        _debug('cmd is {0}'.format(cmd))
        type = ""
        (status, output) = commands.getstatusoutput(cmd)
        if status == 0 :
            # Only use the first line and remove redundant string introduced by xdsh
            type = output.split('\n')[0].replace(self.svr + ': ','',1)
        else:
            _error('Retrieve ibnodes info from UFM server {0} failed.'.format(self.svr))
        if type == 'Ca':
            return 'Computer'
        if type == 'Switch':
            return type
        else:
            return 'Device'

    """Pull events out of queue, translate them and then log them""" 
    def _translate_UFM_traps(self, trap):
        first_layer  = ""
        second_layer = ""
        third_layer  = ""
        fourth_layer  = ""
        time_occured = trap['time_occured']
        event_id     = 'MX050' + '0' * (3 - len(trap['event_id'])) + trap['event_id']
        severity     = trap['severity']
        category     = trap['category']
        type         = trap['type']
        src          = trap['src'].split(' / ')
        desc         = trap['description']
        # use 'A' for logical/software-related events and 'U' for physical/hardware-related events
        src_loc_type = ""
        # log physical object model events: Computer, Device, Gateway, Port, Switch, Module
        if len(src) == 4:
            if not src[1] == 'NA':
                src_loc_type = 'U'
                first_layer  = 'S:' + src[0].split('(')[0] + '|'
                dev = src[1].split(': ')
                if dev[0] == 'Device':
                # start to see if it is a switch or computer
                    dev_type = self.get_dev_type(dev[1])
                else:
                    dev_type = dev[0]
                if dev_type == 'Switch':
                    # sample: "MF0;c870ibsw1-1133fc:IS5100/L03/U1"  "MF0;ACC1-sw1-5e0d8e:SX90Y3245/U1"  "MF0;c160-mlnx1:IS5030/U1"
                    dev_name = dev[1].split(':')[0].replace('MF0;','',1)
                elif dev_type == 'Computer':
                    # sample: "c160f3n08 HCA-1"  "c160fm01 HCA-1"  "localhost iba0"  "c870hsm1 HCA-1"
                    dev_name = dev[1].split(' ')[0]
                else:   
                    # do nothing here
                    dev_name = dev[1]
                second_layer = str(ib_prefix(dev_type)) + ':' + str(dev_name)
            else:
                #Should be site events 
                src_loc_type = 'A'
                #Use UFM server name as src_loc
                first_layer = self.svr
            if not src[2] == 'NA':
                mod = src[2].split(': ')
                if len(mod) > 1:
                    # build up module location if any
                    third_layer = '|' + str(ib_prefix(mod[0])) + ':' + str(mod[1])
                elif len(mod) == 1:
                    # look up module name/type by ourselves
                    mod_name = mod[0].split(' ')[0]
                    try:
                        third_layer = '|' + str(ib_prefix(IB_MODULE_TYPES[mod_name])) + ':' + str(mod[0])
                    except:
                        # Unknown module
                        third_layer = '|M:' + str(mod[0])
            if not src[3] == 'NA':
                fourth_layer = '|P:' + src[3]
        # log logical object model events: Grid, Network, Environment and Site event if there is an initialization of site
        elif len(src) == 1:
            src_loc_type = 'A'
            #Use UFM server name as src_loc
            first_layer  = self.svr
        # log LogicalServer event
        elif len(src) == 2:
            src_loc_type = 'A'
            #Use UFM server name as src_loc
            first_layer = self.svr
        else:
            msg = 'Unrecognized source format {0}!'.format(src)
            _warn(msg)
        rpt_loc = self.svr
        src_loc = first_layer + second_layer + third_layer + fourth_layer
        teal_event = (event_id, time_occured, 'IB', src_loc_type, str(src_loc), 'TEAL', 'A', rpt_loc, IB_TEAL_EXTDATA_V1_T1)
        extended_data = (severity, category, desc)
        self._log_traps(teal_event, extended_data)

    """Function to retrieve UFM events and put them into queue""" 
    def poll_doer(self):
        # check ufm status at first
        status = check_ufm_status(self.svr,self.rsh)
        if not self.last_ufm_status == status:
            self.last_ufm_status = status
            occur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '.000'
            if status == STATUS_DOWN:
                self.handle_ufm_status_event(occur_time, '2')
            elif status == STATUS_UP:
                self.handle_ufm_status_event(occur_time, '3')
            else:
                self.handle_ufm_status_event(occur_time, '1')
        # No need to poll since the first polling has been done in _configure()
        if self.first_traps and not self.traps:                                   
            self.traps = self.first_traps                           
            self.first_traps = None
        else:                                  
            try:                                   
                cmd = TRAP_CMD + ' -t "' + self.last_time_logged + '" -d ' + CURRENT_LOG_DIR + ' -f ' + CURRENT_LOG_NAME
                self.traps = remote_execute(self.svr, self.rsh, cmd)
            except:  
                occur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '.000'
                self.handle_ufm_status_event(occur_time, '1')
                if self.retry_cnt < MAX_RETRY_TIME:                         
                    self.retry_cnt += 1                          
                    msg = 'Error access UFM event log, retrying...'
                    _warn(msg)                             
                    return                                             
                elif self.retry_cnt == MAX_RETRY_TIME:          
                    msg = 'Maximum retry time exceeded, return...'               
                    _error(msg)                             
                    self.retry_cnt = 0                          
                    return                                           
        if not self.retry_cnt == 0:                          
            msg = 'UFM recovered...'
            _info(msg)                             
            self.retry_cnt = 0                          
            occur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '.000'
            self.handle_ufm_status_event(occur_time, '3')
        msg = '-' * 20 + 'Started polling traps' + '-' * 20
        _info(msg)
        if len(self.traps) == 0:
            _info('No new traps found during this polling...')
        for line in self.traps:
            if re.match('.*xdsh',self.rsh):
                line = line.replace(self.svr + ': ','',1)
            # Empty lines
            if re.match('^#',line) or re.match("[' ']*$",line):
                continue
            _debug(line)
            trap = self._handle_UFM_traps(line)
            if not len(trap) > 0:
                msg = "No traps need to be logged"
                _debug(msg)
                continue                        
            msg = "put a new polled out trap into process queue...."
            _debug(msg)
            if self.queue.empty():
                self.queue.put_nowait(trap)
                self.qevt.set()
            else:
                self.queue.put_nowait(trap)
        msg = '-' * 20 + 'Ended polling traps' + '-' * 20
        _info(msg)

    """launch an instance to process a UFM server"""
    def start(self):
        self.processor.start()
        self.poller.start()
        self.timer.start()

    """stop an instance to process a UFM server"""
    def stop(self):
        self.tevt.set()
        self.timer.stop()
        self.poller.stop()
        self.pevt.set()
        self.processor.stop()
        # Unblock waiting on queue
        self.qevt.set()

class InfiniBand(threading.Thread):
    def __init__(self):
        '''Constructor
        '''
        self.ufm_dict = {}
        thread_dict[threading.currentThread()] = '_ufm_'
        self._configure()
        threading.Thread.__init__(self)
        # Set thread listenning to local domain socket
        self.listener = MyThread(self._listener,(),self._listener.__name__)


    def start(self):
        self.listener.start()
        for key in self.ufm_dict:
            _debug('start instance of server {0}'.format(key))
            self.ufm_dict[key].start()

    def stop(self):
        if os.path.exists(SOCKET_FILE):
            os.remove(SOCKET_FILE)

        for key in self.ufm_dict:
            _debug('stop instance of server {0}'.format(key))
            self.ufm_dict[key].stop()
        self.listener.stop()
        # Write a byte to interupt select()
        os.write(self.pipe[1],'x')

    def parse_traps(self,string,dict):
        for k in dict:
            if string.find(k) != -1:
               dict[k] = (string.split('=')[-1]).strip('\n')
               break

    def get_ufm_server(self):
        dict = {}
        # Find UFM servers in xCAT table
        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        # Connection to get UFM nodes from nodelist table
        cnxn = db.get_connection()
        cursor = cnxn.cursor()
        # Connection to get UFM server's latest logged time from site table
        cnxn_site = db.get_connection()
        cursor_site = cnxn_site.cursor()
        try:
            db.select(cursor,
                     ['*'],
                      XCAT_NODE,
                      where='{0} LIKE {1}'.format(XCAT_NODE_KEY,XCAT_NODE_VALUE),
                      where_fields=[XCAT_NODE_KEY])
            # If there is no UFM server defined, return
            row = cursor.fetchone()
            while row and row[0]:
                svr = row[0]
                # Set key value of current UFM server's checkpoint
                ckpt = UFM_CKPT_PREFIX + svr
                # First assume that the high watermark was stored in the site table
                db.select(cursor_site,
                          ['*'],
                          XCAT_SITE,
                          where='${0} = ?'.format(XCAT_SITE_KEY),
                          where_fields=[XCAT_SITE_KEY],
                          parms=[ckpt])

                # If it isn't there then try to figure out the max from what has already
                # been logged, otherwise just start at the beginning
                line = cursor_site.fetchone()
                last_time_logged = ""
                last_ufm_status = ""
                if line is None or line[1] is None:
                    _debug('No items or last_logged_time in site table')
                    parm_list = [IB_TEAL_MAX_KEY_VALUE[0],IB_TEAL_MAX_KEY_VALUE[1],IB_TEAL_MAX_KEY_VALUE[2],svr]
                    max_time = db.select_max(cursor_site, 
                                             IB_TEAL_COLS[1], 
                                             db_interface.TABLE_EVENT_LOG,
                                             where='{0} = ? AND {1} = ? AND {2} = ? AND {3} = ?'.format(IB_TEAL_MAX_KEY[0],IB_TEAL_MAX_KEY[1],IB_TEAL_MAX_KEY[2],IB_TEAL_MAX_KEY[3]),
                                             where_fields=[IB_TEAL_MAX_KEY],
                                             parms=parm_list).fetchone()  
                    if (max_time and max_time[0]):
                        last_time_logged = str(max_time[0])
                        _debug('Retrieved last_logged_time {0} from previous event log'.format(last_time_logged))
                else:
                    last_time_logged = str(line[1])
                    _debug('Use last_time_logged {0} existing in site table for server{1}'.format(last_time_logged,svr))
                    
                if line is None or line[3] is None:
                    _debug('No items or last_ufm_status in site table')
                    parm_list = ['MX060003','MX060004',svr]
                    last_status = db.select_max(cursor_site,
                                                IB_TEAL_COLS[0],
                                                db_interface.TABLE_EVENT_LOG,
                                                where='{0} = ? OR {1} = ? AND {2} = ?'.format(IB_TEAL_COLS[0],IB_TEAL_COLS[0],IB_TEAL_COLS[4]),
                                                where_fields=[IB_TEAL_COLS[0],IB_TEAL_COLS[0],IB_TEAL_COLS[4]],
                                                parms=parm_list).fetchone()  
                    if (last_status and last_status[0]):
                        if last_status == 'MX060003':
                            last_ufm_status = STATUS_DOWN
                        else:
                            last_ufm_status = STATUS_UP
                        _debug('get last UFM server status %s from previous log' % last_ufm_status)
                    else:
                        last_ufm_status = check_ufm_status(svr,self.rsh)
                        _debug('get last UFM server status %s from remote shell' % last_ufm_status)
                else:
                    last_ufm_status = str(line[3])
                    _debug('Use last_ufm_status {0} existing in site table for server {1}'.format(last_ufm_status,svr))

                # Initialize the checkpoint field in the site table so it is always there
                if line is None:
                    db.insert(cursor_site,
                             [XCAT_SITE_KEY, XCAT_SITE_VALUE, 'comments','disable'],
                              XCAT_SITE,
                             [ckpt, str(last_time_logged), 'teal_ib checkpoint - DO NOT DELETE OR MODIFY', str(last_ufm_status)])
                elif line[1] is None or line[3] is None:
                    db.update(cursor_site,
                             [XCAT_SITE_VALUE,'disable'],
                              XCAT_SITE,
                              where="${0} = '{1}'".format(XCAT_SITE_KEY, ckpt),
                              where_fields=[XCAT_SITE_KEY],
                              parms=[str(last_time_logged),str(last_ufm_status)])

                cnxn.commit()

                # Quick test if the UFM event log can be polled out, the first polling will also be invoked
                if last_time_logged == "":
                    cmd = TRAP_CMD + ' -a -d ' + CURRENT_LOG_DIR + ' -f ' + CURRENT_LOG_NAME
                else:
                    if last_time_logged.find('.') == -1:
                        last_time_logged += '.000'
                    cmd = TRAP_CMD + ' -t "' + last_time_logged + '" -d ' + CURRENT_LOG_DIR + ' -f ' + CURRENT_LOG_NAME
                result = remote_execute(svr,self.rsh,cmd)
                if result == []:
                    _error('UFM event log can not be polled')
                else:
                    dict[svr] = ufm_server(svr,self.poll_interval,self.rsh,last_ufm_status,last_time_logged,result)
                row = cursor.fetchone()
        except:
            raise
            _error('Error access xCAT DB {0}'.format(sys.exc_info()))
        cnxn.close()
        cnxn_site.close()
        return dict

    def _configure_filter(self, filter):
        filters = filter.split('#')
        filter_dict = {'event_id':"",
                       'severity':"",
                       'category':"",
                       'time_occured':"",
                       'description':"",
                       'id':"",
                       'type':"",
                      }

        for k in filters:
            key = k.split(':')[0].strip()
            value = k.split(':')[1]
            if key in filter_dict.keys():
                 if not filter_dict[key]:
                     filter_dict[key] = value
                     continue
                 else:
                     _error('Field {0} already configured in configuration file'.format(key))
            else:
                _error('Unsupported field {0} in configuration file'.format(key))
            sys.exit(1)
        return filter_dict
    
    def _configure(self):
        ''' Prepare to run. This method will read the configuration file to
        get its operating parameters and figure out where it needs to start
        based on the last event it logged to TEAL
        '''
        # Set the polling time based on the IB Connector conf file
        cfg = registry.get_service(registry.SERVICE_CONFIGURATION)
        try:
            value = cfg.get(CONFIG_IB_TEAL, CONFIG_POLL_INTERVAL)
            self.poll_interval = int(value)
        except:
            self.poll_interval = IB_TEAL_DEFAULT_POLL_INTERVAL
    
        _debug('Configuring poll interval to {0} seconds'.format(self.poll_interval)) 

        # Set remote shell
        try:
            self.rsh = cfg.get(CONFIG_IB_TEAL, CONFIG_REMOTE_SHELL)
        except:
            self.rsh = IB_TEAL_DEFAULT_REMOTE_SHELL
    
        _debug('Configuring remote shell to {0} seconds'.format(self.rsh)) 

        # Set up the trap related configuration
        filter = cfg.get(CONFIG_IB_TEAL, CONFIG_UFM_TRAP)
        if not filter == 'None': 
            if re.match('(.+:.+)+(#.+:.+)*',filter):
                self.filter_dict = self._configure_filter(filter)
            else:
                _error('Invalid format {0} in UFM trap filter configuation'.format(filter)) 
                sys.exit(1)
        else:
            self.filter_dict = {}
        _debug('UFM trap filter configuation is {0}'.format(self.filter_dict)) 

        # Get UFM servers from xCAT table
        _debug('Retrieve UFM server list from xCAT tables..')
        self.ufm_dict = self.get_ufm_server()
        if len(self.ufm_dict) == 0:
            _error('No UFM server available!')
            sys.exit(1)

    """
        find UFM server this trap belongs to and insert it into queue
    """
    def process_xcat_trap(self,ip,dict):
        if not ip:
            msg = 'No trap source ip address found!'
            _debug(msg)
        server = None
        ufm_name = ""
        try:
            # Remove redundant domain name
            ufm_name = socket.gethostbyaddr(ip)[0].split('.')[0]
        except:
            _debug("Can't get host name for ip {0}".format(ip))
        for key in self.ufm_dict.keys():
            # found the ufm server
            if key == ip or key == ufm_name:
                server = self.ufm_dict[key]
                break
        if server:
            server._process_new_xcattraps(dict)
        else:
            _debug("No corresponding server found from {0}".format(ip))
            
    """
        Listen for the traps forwarded by xCAT from UFM server and parse them as well as append them to corresponding processing queue
    """
    def _listener(self):
        self.pipe = os.pipe()
        self.socket = s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        input = [s,self.pipe[0]]
        try:
           os.remove(SOCKET_FILE)
        except OSError:
           pass
        s.bind(SOCKET_FILE)
        s.listen(5)
        while self.listener.running:
            try:
                inputready,outputready,exceptready = select.select(input,[],[])
            except select.error, e:
                break
            except socket.error, e:
                break
            for svr in inputready:
                if svr == s:
                    client, address = s.accept()
                    input.append(client)
                elif svr == self.pipe[0]:
                    # To interrupt select() here
                    os.read(self.pipe[0],1)
                    break
                else:
                    data = recv_end(svr)
                    if data:
                        msg = "Message %s received!" % data
                        _debug(msg)
                        jstr = json.loads(data)
                        # handle traps here
                        if jstr['process'] == IB_TEAL_UFM_TRAP_HANDLER:
                            dict = copy.deepcopy(IB_TRAP_ATTRS)
                            ufm_ip = ''
                            while jstr['data']:
                                trap_item = jstr['data'].pop()
                                if re.match('^ip=UDP:',trap_item):
                                    # extract ufm server ip here
                                    ufm_ip = trap_item.split('[')[1].split(']')[0]
                                else:
                                    self.parse_traps(trap_item,dict)
                            self.process_xcat_trap(ufm_ip,dict)
                        else:
                            msg = "Unsupported message!"
                            _warn(msg)
                    else:
                        svr.close()
                        input.remove(svr)
        s.close()
        msg = 'Listener stopped'
        _debug(msg)

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        thread_dict[threading.currentThread()] = self.name
        while self.running:
            self.func(*self.args)

def app_terminate(sig, stack_frame):
    ''' Catch the termination signals and shut down cleanly
    '''
    if ib:
        ib.stop()
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
                      help="set the fully qualified log file",
                      action="store",
                      dest="log_file",
                      default=None)
    
    (options, args) = parser.parse_args()
    
    if options.run_as_daemon:
        # Do the necessary processing to spin off as a daemon
        command.daemonize('tlufm')
    else:
        # Make sure there is no other instances
        command.single_instance('tlufm')

    # Allow the user to CTRL-C application and shutdown cleanly        
    signal.signal(signal.SIGINT, app_terminate)    # CTRL-C
    signal.signal(signal.SIGTERM, app_terminate)    # Process Termination
    
    if options.log_file is None:
        log_file = '$TEAL_LOG_DIR/tlufm.log'
    else:
        log_file = options.log_file

    try:        
        # Set up the TEAL environment to get at the data required for logging
        t = teal.Teal(None,
                      data_only=True,
                      msgLevel=options.msg_level,
                      logFile=log_file,
                      daemon_mode=options.run_as_daemon)

        IB_TEAL_EXTDATA_TABLE = extdata.extdata_fmt2table_name(IB_TEAL_EXTDATA_V1_T1)
        # Map thread id to name
        thread_dict = {}
        logger = registry.get_logger()
        # Start Infiniband connector
        ib = InfiniBand()
        ib.start() 
        # Wait for Teal to shutdown before exiting
        shutdown = registry.get_service(registry.SERVICE_SHUTDOWN)
        shutdown.wait()

    except SystemExit, se:
        raise    
    except:
        registry.get_logger().exception("UFM connector failed")
        sys.exit(1)
