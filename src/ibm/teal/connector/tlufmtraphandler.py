#!/usr/bin/env python
import sys
import os
import socket
from ibm.teal import teal
from ibm.teal import registry
End = 'end_of_ufm_msg'
socket_file = '/tmp/tlibsocket'
process_name = os.path.basename(sys.argv[0])

if __name__ == '__main__':
    log_file = '$TEAL_LOG_DIR/tlufmtraphandler.log'
    # Set up the TEAL environment to get at the data required for logging
    t = teal.Teal(None,
                  data_only=True,
                  msgLevel='info',
                  logFile=log_file,
                  daemon_mode=False)

    # UFM traps sent to tlufm.py to process
    registry.get_logger().debug('A trap from UFM received!')
    l = {'process':"",
         'data':[]
        }
    l['process']    = process_name
    l['data'].extend(sys.stdin.readlines())
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(socket_file)
        import json
        message = json.dumps(l)
        s.sendall(message + End)
    except:
        registry.get_logger().warn("tlufm.py may be not running, please check...")
        import traceback
        registry.get_logger().exception(traceback.format_exc())
    s.close()
   
