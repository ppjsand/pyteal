# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011, 2012 
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
from ibm.teal.registry import get_logger, get_service, SERVICE_CHECKPOINT_MGR,\
    SERVICE_DB_INTERFACE, SERVICE_EVENT_Q
from ibm.teal.util.listenable_queue import QueueListener
from ibm.teal.control_msg import CONTROL_MSG_TYPE_END_OF_DATA
from ibm.teal.teal_error import ConfigurationError
from ibm.teal.database import db_interface
import threading
from ibm.teal.event import EVENT_ATTR_REC_ID
import exceptions
from ibm.teal.util.teal_thread import TealThread

# Restart modes 
RESTART_MODES = ['now', 'begin', 'recovery', 'lastproc']
RESTART_MODE_NOW = 'now'
RESTART_MODE_BEGIN = 'begin'
RESTART_MODE_RECOVERY = 'recovery'
RESTART_MODE_LASTPROC = 'lastproc'

MAX_CHECKPOINT_DATA_SIZE = 1024
# Constants for the last status checkpointed
CHECKPOINT_STATUS_RUNNING = 'R'
CHECKPOINT_STATUS_SHUTDOWN = 'S'
CHECKPOINT_STATUS_FAILED = 'F'
CHECKPOINT_STATUS_UNKNOWN = 'U'  # Should not be persisted
CHECKPOINT_STATUS_DELETED = 'D'
CHECKPOINT_STATUS_INTERRUPTED = 'I'

# Constants for event checkpoint fields
EVENT_CPF_CHKPT_ID = 'chkpt_id'
EVENT_CPF_NAME = 'name'
EVENT_CPF_STATUS = 'status'
EVENT_CPF_EVENT_RECID = 'event_recid'
EVENT_CPF_DATA = 'data'

# Constant SQL statements
_SQL_EVENT_CP_INSERT = None
_SQL_EVENT_CP_SELECT_BY_NAME = None
_SQL_EVENT_CP_UPDATE_CHECKPOINT = None


def get_current_min_checkpoint_rec_id():
    ''' Read *all* of the checkpoints in the checkpoint table and return the 
        mimimum rec_id
        
    '''
    get_logger().debug('Getting current minimum checkpoint rec id')
    min_rec_id = None
    db = get_service(SERVICE_DB_INTERFACE)
    cnxn = db.get_connection()
    cursor = cnxn.cursor()
    db.select(cursor, [EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID], db_interface.TABLE_CHECKPOINT)
    while 1:
        row = cursor.fetchone()
        if row is None:
            break
        name, status, rec_id = row 
        get_logger().debug('Checking {0} {1} {2}'.format(name, status, str(rec_id)))
        if rec_id is not None: 
            if min_rec_id is None: 
                min_rec_id = rec_id
            else:
                min_rec_id = min(min_rec_id, rec_id)
        
    get_logger().debug('returning minimum = {0}'.format(min_rec_id))
    cnxn.close()
    return min_rec_id
   
    
class CheckpointMgr(object):
    '''
    Checkpoint manager
    
    Manages checkpoints for events and alerts
    '''

    def __init__(self, use_db, restart_mode):
        '''
        Initialize the checkpoint manager 
        '''
        get_logger().debug('Initializing checkpoint manager use_db = {0}, restart_mode = {1}'.format(str(use_db), str(restart_mode)))
        self.event_checkpoints = dict()
        self.use_db = use_db
        self.chkpt_recid_lock = threading.Lock()
        self.event_checkpoint_rec_id = 0
        self.shutdown_recid = None 
        
        # Validate restart mode
        if restart_mode is not None and restart_mode not in RESTART_MODES:
            raise ConfigurationError('Unrecognized restart mode specified: {0}'.format(restart_mode))
        self.restart_mode = restart_mode
        
        if use_db == True: 
            get_logger().debug('Checkpoint manager is using the DB')
            
            # Setup SQL strings
            db = get_service(SERVICE_DB_INTERFACE)
            
            #   Insert event row
            global _SQL_EVENT_CP_INSERT
            _SQL_EVENT_CP_INSERT = db.gen_insert(
                    [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                    db_interface.TABLE_CHECKPOINT)
            
            #   Get event row
            global _SQL_EVENT_CP_SELECT_BY_NAME
            _SQL_EVENT_CP_SELECT_BY_NAME = db.gen_select(
                    [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                    db_interface.TABLE_CHECKPOINT, 
                    where='${0} = ?'.format(EVENT_CPF_NAME),
                    where_fields=[EVENT_CPF_NAME])
           
            #   Update event checkpoint
            global _SQL_EVENT_CP_UPDATE_CHECKPOINT
            _SQL_EVENT_CP_UPDATE_CHECKPOINT = db.gen_update(
                    [EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                    db_interface.TABLE_CHECKPOINT, 
                    where='${0} = ?'.format(EVENT_CPF_CHKPT_ID),
                    where_fields=[EVENT_CPF_CHKPT_ID])
            
            # Determine the next event rec_id to use
            cnxn = db.get_connection()
            cursor = cnxn.cursor()
            db.select_max(cursor, EVENT_CPF_CHKPT_ID, db_interface.TABLE_CHECKPOINT)
            row = cursor.fetchone()
            if row and row[0]:
                self.event_checkpoint_rec_id = row[0]
            get_logger().debug('Checkpoint Manager starting after rec_id = {0}'.format(self.event_checkpoint_rec_id))
            cnxn.close()
            
            # Setup for asynchronous update of checkpoints in DB
            self.update_db_event = threading.Event()
            self.t1 = CheckpointDBUpdater(self)
            self.t1.setDaemon(True)
            self.t1.start()
        return
        
    def get_next_event_checkpoint_rec_id(self): 
        ''' Get the next event checkpoint rec id '''
        tmp_rec_id = None
        if self.use_db == True: 
            with self.chkpt_recid_lock:
                self.event_checkpoint_rec_id += 1
                tmp_rec_id = self.event_checkpoint_rec_id
        return tmp_rec_id
      
    def register_event_checkpoint(self, checkpoint):
        ''' Register the event checkpoint with the manager 
        
            Note does not check for duplicates
        '''
        self.event_checkpoints[checkpoint.name] = checkpoint
        return 
    
    def unregister_event_checkpoint(self, checkpoint):
        ''' Unregister the event checkpoint with the manager 
        
            Note does not tolerate unregistering a checkpoint that hasn't been registered
        '''
        del self.event_checkpoints[checkpoint.name]
        return 
        
    def get_starting_event_rec_id(self, override_restart_mode=None):
        '''
        Use the mode and checkpoints to determine what rec_id should be used to start event retrieval
        
           Mode         Behavior
            begin        start at first event in event log (0)
            recovery     start at lowest checkpoint rec id
            lastproc     start at the last event in the event log that was processed by anyone (highest checkpoint)
            now          start after max rec_id in event log
             
        default mode is recovery
           if specified during init (from TEAL input) then that is used
           else if specified in override_restart_mode (the monitoring stanza) that is used 
           
        Checkpoints are prepared for restart as part of this method 
        
        Returns (start_event_rec_id, mode_used)
        '''
        t_restart_mode = self.restart_mode # value from init (TEAL startup)
        if t_restart_mode is None:
            if override_restart_mode is not None:
                if override_restart_mode not in RESTART_MODES:
                    raise ConfigurationError('Unrecognized restart mode specified: {0}'.format(override_restart_mode))
                t_restart_mode = override_restart_mode
            else:
                t_restart_mode = RESTART_MODE_RECOVERY
                
        start_eri = None   # Where the monitor should start
        max_start = None   # The last one processed
        # Process based on restart mode 
        if t_restart_mode == RESTART_MODE_RECOVERY:
            # Find the earliest we have to restart
            for t_ckpt in self.event_checkpoints.values():
                value = t_ckpt.start_rec_id
                if value is not None: 
                    # Collect minimum of checkpoints
                    if start_eri is None:
                        start_eri = value
                    else:
                        start_eri = min(start_eri, value)
                    # Collect maximum 
                    if max_start is None:
                        max_start = value
                    else:
                        max_start = max(max_start, value)
                
        elif t_restart_mode == RESTART_MODE_BEGIN:
            start_eri = 0
            max_start = 0
            
        elif t_restart_mode == RESTART_MODE_LASTPROC:
            # Find the last event processed
            for t_ckpt in self.event_checkpoints.values():
                t_start = t_ckpt.start_rec_id
                if t_start is not None:
                    if start_eri is None:
                        start_eri = t_start
                    else:
                        start_eri = max(start_eri, t_start)
            max_start = start_eri
        # ELSE: default (None) is what should be returned for 'now' (the only option left) 
        if self.use_db == True: 
            # See if need to use last event rec_id and, if so, get it
            if start_eri is None:
                # Get the last rec_id as the one to start after 
                try: 
                    db = get_service(SERVICE_DB_INTERFACE)
                    cnxn = db.get_connection()
                    cursor = cnxn.cursor()
                    db.select_max(cursor, EVENT_ATTR_REC_ID, db_interface.TABLE_EVENT_LOG)
                    row = cursor.fetchone()
                    if row and row[0]:
                        start_eri = row[0]
                    cnxn.close()
                except:
                    get_logger().exception('Unable to determine maximum event rec_id - starting with None')
                    start_eri = None   
                   
            # Clear away the inactive checkpoint entries in the DB
            try:
                # Get the active checkpoint rec_ids from the DB
                tmp_ckpts = []
                db = get_service(SERVICE_DB_INTERFACE)
                cnxn = db.get_connection()
                cursor = cnxn.cursor()
                db.select(cursor, [EVENT_CPF_CHKPT_ID], db_interface.TABLE_CHECKPOINT)
                rows = cursor.fetchall()
                for row in rows: 
                    tmp_ckpts.append(row[0])
                
                # remove the active rec_ids from the 
                for t_ckpt in self.event_checkpoints.values():
                    keep_ckpt = t_ckpt.ckpt_rec_id
                    if keep_ckpt not in tmp_ckpts:
                        get_logger().warning('Checkpoint with primary key {0} not in list from DB {1}'.format(keep_ckpt, str(tmp_ckpts)))
                    else:
                        tmp_ckpts.remove(keep_ckpt)
                        
                # delete the inactive entries (all minus active)
                for del_ckpt in tmp_ckpts:
                    db.delete(cursor, db_interface.TABLE_CHECKPOINT, 
                              where='${0} = ?'.format(EVENT_CPF_CHKPT_ID), where_fields=[EVENT_CPF_CHKPT_ID], parms=(del_ckpt))
                cnxn.commit()
                cnxn.close()
            except:
                get_logger().exception('Unable to clear out inactive checkpoints')
             
                    
        get_logger().info('Checkpoint manager used \'{0}\' to determine starting event rec id = {1}'.format(t_restart_mode, str(start_eri)))

        # Prepare checkpoints for restart 
        for t_ckpt in self.event_checkpoints.values():
            t_ckpt.prepare_for_restart(t_restart_mode, start_eri, max_start)
        
        return (start_eri, t_restart_mode)
    
    def monitor_shutdown(self, recid):
        ''' Called by the monitor to indicate what '''
        get_logger().debug('monitor shutdown notification {0}'.format(str(recid)))
        if recid != 0: 
            self.shutdown_recid = recid
        return
    
    def shutdown(self):
        ''' Do any shutdown processing '''
        get_logger().debug('checkpoint manager shutting down')
        if len(self.event_checkpoints) != 0:
            if self.use_db == True:
                # Ensure that all checkpoints written to DB
                self.t1.running = False 
                self.update_db_event.set()
                self.t1.join()
                
                dump = False
                for t_ckpt in self.event_checkpoints.values():
                    if t_ckpt.status != CHECKPOINT_STATUS_SHUTDOWN:
                        dump = True
                if dump == False:
                    return 
            get_logger().info('<<START: CHECKPOINTS AT SHUTDOWN\n {0}'.format(str(self)))
            get_logger().info('>>END: CHECKPOINTS AT SHUTDOWN')
        return 
    
    def __str__(self):
        ''' Output as a string '''
        outstr = 'Checkpoint Manager'
        if self.use_db == True:
            outstr += '(in DB)'
        outstr += '\n   Event Checkpoints\n'
        if len(self.event_checkpoints) == 0:
            outstr += '      -None-'
        else:
            for e_ckpt in self.event_checkpoints.values():
                outstr += '     ' + str(e_ckpt)
        return outstr
    
    
class CheckpointDBUpdater(TealThread):
    '''This class is used to asynchronously update the checkpoints in the DB
    '''
    
    def __init__(self, mgr):
        '''Constructor
        '''
        self.mgr = mgr
        self.running = True
        TealThread.__init__(self)
        return
    
    def run(self):
        '''Wait for an update event 
        '''
        while self.running:
            self.mgr.update_db_event.wait()
            self.mgr.update_db_event.clear()
            # Iterate and update
            try: 
                dbi = get_service(SERVICE_DB_INTERFACE)
                cnxn = dbi.get_connection()
                cursor = cnxn.cursor()
                for checkpoint in self.mgr.event_checkpoints.values():
                    checkpoint.update_db(cursor)
                cnxn.commit()
                cnxn.close()
            except:
                get_logger().exception('Unable to update checkpoints in DB')
        get_logger().debug('run method ended')
        return
      
        
class EventCheckpoint(object): 
    ''' Event Checkpoint
       
       An instance should be created and registered with the Checkpoint Mgr
    ''' 
    
    def __init__(self, name):
        ''' Initialize the event checkpoint '''
        self.name = name

        self.ckpt_rec_id = None
        self.status = CHECKPOINT_STATUS_RUNNING
        self.start_rec_id = None
        self.data = None
        self.checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        if self.checkpoint_mgr.use_db == True:
            # Get entry for name in DB
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(_SQL_EVENT_CP_SELECT_BY_NAME, (name))
            row = cursor.fetchone()
            if row is not None:
                get_logger().debug('Found entry for {0}'.format(name))
                self.ckpt_rec_id, self.name, self.status, self.start_rec_id, self.data = row 
            else:
                get_logger().debug('Creating new entry for {0}'.format(name))
                self.ckpt_rec_id = self.checkpoint_mgr.get_next_event_checkpoint_rec_id()
                cursor.execute(_SQL_EVENT_CP_INSERT, (self.ckpt_rec_id, self.name, self.status, self.start_rec_id, self.data))
                cnxn.commit()
            cnxn.close()    
            
            # Use DB methods    
            self.set_status = self.set_status_DB
            self.set_checkpoint = self.set_checkpoint_DB
            self.set_checkpoint_no_data = self.set_checkpoint_no_data_DB
            
            self.changed = False
            self.lock = threading.RLock()
            
        self.checkpoint_mgr.register_event_checkpoint(self)
        return 
    
    def get_status(self):
        ''' get status ''' 
        if self.status is None:
            return CHECKPOINT_STATUS_UNKNOWN
        return self.status
        
    def get_checkpoint(self):
        ''' get the checkpoint data '''
        return (self.start_rec_id, self.data)
    
    def is_checkpoint_rec_id(self, value):
        ''' check if the value of the checkpoint is what was passed ''' 
        return value == self.start_rec_id
    
    def prepare_for_restart(self, restart_mode, restart_rec_id, max_start):        
        ''' Prepare for restarting with the restart mode and specified rec_id
        based on the context of the mode and the starting rec_id to determine what to do.
        '''
        if restart_mode == RESTART_MODE_RECOVERY:
            if self.status == CHECKPOINT_STATUS_SHUTDOWN:
                self.set_status(CHECKPOINT_STATUS_RUNNING)
            if self.get_checkpoint()[0] is None:
                self.set_checkpoint(max_start) 
        else: # RESTART_MODE_BEGIN, LAST_PROC or NOW
            self.set_status(CHECKPOINT_STATUS_RUNNING)
            self.set_checkpoint(None)
        return 
        
    def set_status(self, status):
        ''' set status '''
        get_logger().info('Updating status for {0} from {1} to {2}'.format(self.name, self.status, status))
        self.status = status
        return 
    
    def set_status_DB(self, status):
        ''' set status '''
        get_logger().info('Updating status for {0} from {1} to {2} (start = {3})'.format(self.name, self.status, status, str(self.start_rec_id)))
        with self.lock:
            self.status = status
            self.changed = True
            self.checkpoint_mgr.update_db_event.set()
        return

    def set_status_DELETED(self, status):
        ''' Cannot set status if deleted '''
        get_logger().warning('Tried to set status on deleted checkpoint {0}'.format(self.name))
        return 
    
    def set_checkpoint(self, start_rec_id, data=None):
        ''' set the checkpoint data '''
        get_logger().debug('Updating checkpoint for {0} from {1} to {2}'.format(self.name, self.start_rec_id, start_rec_id))
        self.start_rec_id = start_rec_id
        self.data = data
        if data is not None and len(data) > MAX_CHECKPOINT_DATA_SIZE:
            get_logger().warning('Checkpoint failure: length of data {0} too large\n data: {1}'.format(len(data), str(data))) 
            self.data = None
        return
    
    def set_checkpoint_DB(self, start_rec_id, data=None):
        ''' set the checkpoint data '''
        get_logger().debug('Updating checkpoint for {0} from {1} to {2}'.format(self.name, self.start_rec_id, start_rec_id))
        with self.lock: 
            self.start_rec_id = start_rec_id
            self.data = data
            if data is not None and len(data) > MAX_CHECKPOINT_DATA_SIZE:
                get_logger().warning('Checkpoint failure: length of data {0} too large\n data: {1}'.format(len(data), str(data))) 
                self.data = None
            self.changed = True
            self.checkpoint_mgr.update_db_event.set()
        return 
    
    def set_checkpoint_no_data(self, start_rec_id):
        ''' set the checkpoint data '''
        get_logger().debug('Updating checkpoint for {0} from {1} to {2}'.format(self.name, self.start_rec_id, start_rec_id))
        self.start_rec_id = start_rec_id
        return
    
    def set_checkpoint_no_data_DB(self, start_rec_id):
        ''' set the checkpoint data '''
        get_logger().debug('Updating checkpoint (no data) for {0} from {1} to {2}'.format(self.name, self.start_rec_id, start_rec_id))
        with self.lock:
            self.start_rec_id = start_rec_id
            self.changed = True
            self.checkpoint_mgr.update_db_event.set()
        return 
    
    def set_checkpoint_DELETED(self, start_rec_id, data=None):
        ''' Cannot set checkpoint if deleted '''
        get_logger().warning('Tried to set checkpoint on deleted checkpoint {0}'.format(self.name))
        return 
    
    def update_db(self, cursor):
        ''' Update the DB using the provided cursor with the latest information from this checkpoint '''
        with self.lock:
            if self.changed == True:
                cursor.execute(_SQL_EVENT_CP_UPDATE_CHECKPOINT, (self.status, self.start_rec_id, self.data, self.ckpt_rec_id))
                self.changed = False 
        return
    
    def shutdown(self, status_only=False):
        ''' Update the checkpoint for shutdown.   Need to make sure that the monitor has passed the checkpoint 
            before aligning with it
        '''
        with self.lock:
            shutdown_recid = self.checkpoint_mgr.shutdown_recid
            if (shutdown_recid is not None and shutdown_recid >= self.start_rec_id) or (shutdown_recid == self.start_rec_id):
                # If the shutdown recid is set and has reached my checkpoint then clear it out
                self.set_status(CHECKPOINT_STATUS_SHUTDOWN)
                if status_only == False:
                    self.set_checkpoint(shutdown_recid, None)
        return
    
    def shutdown_immediate(self, status_only=False):
        ''' Update the checkpoint for immediate shutdown.   Need to make sure that it has passed the checkpoint 
            before aligning with it
        '''
        shutdown_recid = self.checkpoint_mgr.shutdown_recid
        if (shutdown_recid is not None and shutdown_recid >= self.start_rec_id) or (shutdown_recid == self.start_rec_id):
            # If the shutdown recid is set and has reached my checkpoint then clear it out
            self.set_status(CHECKPOINT_STATUS_SHUTDOWN)
            if status_only == False:
                self.set_checkpoint(shutdown_recid, None)
        return
            
    def delete(self):
        ''' Mark the checkpoint as deleted 
        '''
        if self.checkpoint_mgr.use_db == True: 
            with self.lock:
                self.changed = False    # Stop any updates
                self.checkpoint_mgr.unregister_event_checkpoint(self)
        else:
            self.checkpoint_mgr.unregister_event_checkpoint(self)
        
        # Change in memory values 
        self.status = CHECKPOINT_STATUS_DELETED
        self.start_rec_id = None
        self.data = None
        self.starting_cb = None
        self.set_status = self.set_status_DELETED
        self.set_checkpoint = self.set_checkpoint_DELETED
        
        # Delete from DB 
        if self.checkpoint_mgr.use_db == True:
            try:
                dbi = get_service(SERVICE_DB_INTERFACE)
                cnxn = dbi.get_connection()
                cursor = cnxn.cursor()
                dbi.delete(cursor, db_interface.TABLE_CHECKPOINT, 
                           where='${0} = ?'.format(EVENT_CPF_NAME),
                           where_fields=[EVENT_CPF_NAME], 
                           parms=(self.name))
                cnxn.commit()
                cnxn.close()
            except:
                get_logger().exception('Unable to delete event checkpoint named {0}'.format(self.name))
                raise
        return 
    
    def confirm_checkpoint(self):
        ''' Confirm that checkpoint data in DB matches in memory values
            Default is no DB so nothing to do
        '''
        pass
    
    def __str__(self):
        ''' dump the checkpoint into a string '''
        if self.checkpoint_mgr.use_db == True and self.changed == True:
            t_c = '*'
        else: 
            t_c = ''
        outstr = 'Checkpoint {0}({1}){2} -- {3} '.format(self.name, self.ckpt_rec_id, t_c, self.get_status())
        if self.start_rec_id is None:
            outstr += 'at -unspecified- '
        else:
            outstr += 'at {0} '.format(self.start_rec_id)
        if self.data is None:
            outstr += ' with no data\n'
        else:
            outstr += ' with {0}\n'.format(self.data)
        return outstr


class CheckpointListener(QueueListener):

    def __init__(self, name):
        self.name = name
        # Register myself as a listener on the event Q
        self.listenQ = get_service(SERVICE_EVENT_Q)
        self.listenQ.register_listener(self)
        self.event_checkpoint = EventCheckpoint(name)
        return
    
    def set_data(self, data):
        ''' Set the data in the checkpoint '''
        self.event_checkpoint.set_checkpoint(self.event_checkpoint.start_rec_id, data)
        return 

    def get_name(self):
        return self.name

    def notify(self,item):
        item.process(self,None)
        # return False because this listener did nothing to cause output downstream.
        return False

    def shutdown(self):
        get_logger().debug('Shutdown CheckpointListener.')
        self.event_checkpoint.shutdown(status_only=True)  # Only status because used to record high water mark

    def shutdown_immediate(self):
        get_logger().debug('Shutdown (immediate) CheckpointListener.')
        # Shutdown where it is currently
        self.process_event = self.process_event_SHUTDOWN
        self.process_alert = self.process_alert_SHUTDOWN
        self.process_control_msg = self.process_control_msg_SHUTDOWN
        try:
            self.event_checkpoint.shutdown_immediate(status_only=True)
        except:
            pass
        self.listenQ.unregister_listener(self)

    def process_event(self, event, context):
        get_logger().debug('CheckpointListener: process_event')
        # Get the needed event information.
        try:
            self.event_checkpoint.set_checkpoint_no_data(event.rec_id)
        except:
            get_logger().exception('Unable to update checkpoint rec_id for {0}'.format(self.name))
        return False
    
    def process_event_SHUTDOWN(self, event, context):
        ''' shutdown, so stop processing ''' 
        return False 

    def process_alert(self, alert, context):
        ''' Handle double dispatch from an alert.
        This listener does not handle alerts. '''
        get_logger().error('CheckpointListener was given an alert.')
        return False
    
    def process_alert_SHUTDOWN(self, alert, context):
        ''' shutdown, so stop processing ''' 
        return False

    def process_control_msg(self, control_msg, context):
        get_logger().debug('CheckpointListener: process_control_msg')
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            try:
                self.shutdown() 
            except:
                get_logger().exception('Unable to update checkpoint status to shutdown for {0}'.format(self.name))

            self.listenQ.unregister_listener(self)
        return True
    
    def process_control_msg_SHUTDOWN(self, control_msg, context):
        ''' shutdown, so stop processing ''' 
        return True 
    
    
class CheckpointRecoveryComplete(exceptions.Exception):
    ''' Used to throw exception indicating that the checkpoint has completed recovery and
        that normal processing can be resumed.
    '''
    
    def __init__(self, recovery_rec_id, msg):
        ''' Message will be logged ''' 
        self.recovery_rec_id = recovery_rec_id
        self.msg = msg
        if self.recovery_rec_id is None:
            get_logger().debug('Checkpoint recovery not required: {0}'.format(str(self.msg)))
        else:
            get_logger().info('Checkpoint recovery complete at {0}: {1}'.format(self.recovery_rec_id, str(self.msg)))
        return 

    def __str__(self):
        '''Print out additional information'''
        return repr(self.msg)
