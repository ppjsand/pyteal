#!/usr/bin/env python
import sys
import time
import os
import socket
import re
import commands
from ibm.teal import teal
from ibm.teal import registry
from ibm.teal import event
from ibm.teal.database import db_interface
from ibm.teal.monitor import teal_semaphore

now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

MLX_TEAL_COLS = (event.EVENT_ATTR_EVENT_ID,
                 event.EVENT_ATTR_TIME_OCCURRED,
                 event.EVENT_ATTR_SRC_COMP,
                 event.EVENT_ATTR_SRC_LOC_TYPE,
                 event.EVENT_ATTR_SRC_LOC,
                 event.EVENT_ATTR_RPT_COMP,
                 event.EVENT_ATTR_RPT_LOC_TYPE,
                 event.EVENT_ATTR_RPT_LOC,
                 event.EVENT_ATTR_RAW_DATA,
                 event.EVENT_ATTR_RAW_DATA_FMT
                )

MLX_EVENTS_IDS = {"asicChipDown":"MX000001",
                  "asicOverTempReset":"MX000002",
                  "asicOverTemp":"MX000003",
                  "lowPower":"MX000004",
                  "bxAsicChipDown":"MX010001",
                  "bxAsicOverTempReset":"MX010002",
                  "bxAsicOverTemp":"MX010003",
                  "ibSMup":"MX020001",
                  "ibSMdown":"MX020002",
                  "ibSMrestart":"MX020003",
                  "internalBusError":"MX030001",
                  "procCrash":"MX030002",
                  "cpuUtilHigh":"MX030003",
                  "procUnexpectedExit":"MX030004",
                  "unexpectedShutdown":"MX030005",
                  "diskSpaceLow":"MX030006",
                  "systemHealthStatus":"MX030007",
                  "lowPowerRecover":"MX030008",
                  "insufficientFans":"MX030009",
                  "insufficientFansRecover":"MX030010",
                  "mlxIBCAHealthStatusChange":"MX040001",
                  "mlxIBCAInsertion":"MX040002",
                  "mlxIBCARemoval":"MX040003",
                  "mlxIBSwitchInsertion":"MX040004",
                  "mlxIBSwitchRemoval":"MX040005",
                  "mlxIBRouterInsertion":"MX040006",
                  "mlxIBRouterRemoval":"MX040007",
                  "mlxIBPortStateChange":"MX040008",
                  "mlxIBPortPhysicalStateChange":"MX040009",
                  "mlxIBPortInsertion":"MX040010",
                  "mlxIBPortRemoval":"MX040011"
                  }

mlx_eventid = lambda x: MLX_EVENTS_IDS.get(x)

# XCAT Table definitions
XCAT_NODE = 'nodelist'
XCAT_NODE_KEY = 'groups'
XCAT_NODE_VALUE = "'%ufm%'"

XCAT_PWD = 'passwd'
XCAT_PWD_KEY = 'key'

def translate_trap(ip,trap_oid):
    src_loc_type = 'D'
    src_comp = 'IB'
    rpt_comp = 'TEAL'
    rpt_loc_type = 'A'
    raw_data = ''
    raw_data_fmt = 0
    src_loc = ''
    teal_event = None
    rpt_loc = os.path.basename(sys.argv[0]) + '##' + str(os.getpid())
    switch_name = socket.gethostbyaddr(ip)[0]
    if not switch_name:
        command = '/usr/bin/snmpget -v 2c -c public ' + ip + ' MELLANOX-MIB::nodeName.0'
        registry.get_logger().debug('command to retrieve switch name: {0}'.format(command))
        (status, output) = commands.getstatusoutput(command)
        if status == 0 :
            if re.match('.*STRING',output):
                src_loc = output.rsplit('"',2)[1]
            else:
                src_loc = ip
        else:
            registry.get_logger().error('Retrieve switch name failed, use ip address instead.')
            src_loc = ip
    else:
        src_loc = switch_name
    command = '/usr/bin/snmptranslate -Td MELLANOX-MIB::' + trap_oid
    registry.get_logger().debug('command to retrieve trap name: {0}'.format(command))
    (status, output) = commands.getstatusoutput(command)
    if status == 0 :
            raw_data = output.split('"')[1].replace('\n        ','')
    else:
        registry.get_logger().error('Retrieve trap description failed, use trap name instead.')
        raw_data = trap_oid
    time_occurred = now_time
    event_id = mlx_eventid(trap_oid.split('.')[0])
    if not event_id:
        msg = "Unrecognized event!" 
        registry.get_logger().warn(msg)
        event_id = "MX03FFFF"
    teal_event = (event_id, time_occurred, src_comp, src_loc_type, src_loc, rpt_comp, rpt_loc_type, rpt_loc, raw_data, raw_data_fmt)
    msg = "Common data:: event_id: %s, time_occurred: %s, src_comp: %s, src_loc_type: %s, src_loc: %s, rpt_comp: %s, rpt_loc_type: %s, rpt_loc: %s, raw_data: %s, raw_data_fmt: %d" % teal_event
    registry.get_logger().debug(msg)
    return teal_event

def log_traps(event):
    event_logged = False
    db = registry.get_service(registry.SERVICE_DB_INTERFACE)
    cnxn = db.get_connection()
    teal_cursor = cnxn.cursor()
    try:
        db.insert(teal_cursor, MLX_TEAL_COLS, db_interface.TABLE_EVENT_LOG, event)
        cnxn.commit()
        msg = "Logged an event: event_id: %s, time_occurred: %s, src_comp: %s, src_loc_type: %s, src_loc: %s, rpt_comp: %s, rpt_loc_type: %s, rpt_loc: %s, raw_data: %s, raw_data_fmt: %d" % teal_event
        registry.get_logger().info(msg)
        # Notify TEAL that events have been inserted
        notifier = teal_semaphore.Semaphore()
        if notifier:
            notifier.post()
        else:
            registry.get_logger().warn('TEAL notifier not configured.')
    except:
        # Don't attempt to commit anything since we had an error processing the events
        registry.get_logger().exception("Error processing new events")
        cnxn.rollback()
    cnxn.close()


##########MAIN##########
if __name__ == '__main__':
    log_file = '$TEAL_LOG_DIR/tlmlxtraphandler.log'
    try:
        # Set up the TEAL environment to get at the data required for logging
        t = teal.Teal(None,
                      data_only=True,
                      msgLevel='warn',
                      logFile=log_file,
                      daemon_mode=False)

        switch_ip = ''
        sys_up_time = ''
        trap_oid = ''
        trap_vars = {}
        for line in sys.stdin.readlines():
            # Filter out this redundant line firstly
            if re.match('.*snmpTrapEnterprise',line):
                continue
            if re.match('.*ip=',line):
                switch_ip = line.split('[')[1].split(']')[0]
                continue
            if re.match('.*snmpTrapOID',line):
                trap_oid = line.split('::')[2].split('.')[0].strip('\n')
                continue
            if re.match('.*mlx',line):
                vars = line.split('=')
                value = vars[1].strip('\n')
                key = vars[0].split('::')[1].split('.')[0]
                trap_vars[key] = value
                continue
        msg = "trap received: switch_ip = {0}, trap_oid = {1},vars = {2}".format(switch_ip,trap_oid,trap_vars)
        registry.get_logger().debug(msg)
        teal_event = translate_trap(switch_ip,trap_oid)
        log_traps(teal_event)
    except:
        registry.get_logger().exception("Teal Mellanox switch trap handler failed")
        sys.exit(1)
