# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
from ibm.teal.registry import get_logger, get_service, SERVICE_CHECKPOINT_MGR,\
    SERVICE_DB_INTERFACE, SERVICE_EVENT_Q
from ibm.teal.util.listenable_queue import QueueListener
from ibm.teal.control_msg import CONTROL_MSG_TYPE_END_OF_DATA
from ibm.teal.teal_error import ConfigurationError, TealError
from ibm.teal.database import db_interface
import threading
from ibm.teal.event import EVENT_ATTR_REC_ID

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
CHECKPOINT_STATUS_TIMED_OUT = 'T'
CHECKPOINT_STATUS_UNKNOWN = 'U'  # Should not be persisted
CHECKPOINT_STATUS_DELETED = 'D'

# Constants for event checkpoint fields
EVENT_CPF_CHKPT_ID = 'chkpt_id'
EVENT_CPF_NAME = 'name'
EVENT_CPF_STATUS = 'status'
EVENT_CPF_EVENT_RECID = 'event_recid'
EVENT_CPF_DATA = 'data'

# Constant SQL statements
_SQL_EVENT_INSERT = None
_SQL_EVENT_SELECT_BY_NAME = None
_SQL_EVENT_UPDATE_CHECKPOINT = None
_SQL_EVENT_UPDATE_CHECKPOINT_NO_DATA = None
_SQL_EVENT_UPDATE_STATUS = None
_SQL_EVENT_INSERT = None


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
        
        # Validate restart mode
        if restart_mode is not None and restart_mode not in RESTART_MODES:
            raise ConfigurationError('Unrecognized restart mode specified: {0}'.format(restart_mode))
        self.restart_mode = restart_mode
        
        if use_db == True: 
            get_logger().debug('Checkpoint manager is using the DB')
            
            # Setup SQL strings
            db = get_service(SERVICE_DB_INTERFACE)
            
            #   Insert event row
            global _SQL_EVENT_INSERT
            _SQL_EVENT_INSERT = db.gen_insert(
                    [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                    db_interface.TABLE_CHECKPOINT)
            
            #   Get event row
            global _SQL_EVENT_SELECT_BY_NAME
            _SQL_EVENT_SELECT_BY_NAME = db.gen_select(
                    [EVENT_CPF_CHKPT_ID, EVENT_CPF_NAME, EVENT_CPF_STATUS, EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                    db_interface.TABLE_CHECKPOINT, 
                    where='${0} = ?'.format(EVENT_CPF_NAME),
                    where_fields=[EVENT_CPF_NAME])
           
            #   Update event checkpoint
            global _SQL_EVENT_UPDATE_CHECKPOINT
            _SQL_EVENT_UPDATE_CHECKPOINT = db.gen_update(
                    [EVENT_CPF_EVENT_RECID, EVENT_CPF_DATA],
                    db_interface.TABLE_CHECKPOINT, 
                    where='${0} = ?'.format(EVENT_CPF_CHKPT_ID),
                    where_fields=[EVENT_CPF_CHKPT_ID])
            
            #   Update event checkpoint
            global _SQL_EVENT_UPDATE_CHECKPOINT_NO_DATA
            _SQL_EVENT_UPDATE_CHECKPOINT_NO_DATA = db.gen_update(
                    [EVENT_CPF_EVENT_RECID],
                    db_interface.TABLE_CHECKPOINT, 
                    where='${0} = ?'.format(EVENT_CPF_CHKPT_ID),
                    where_fields=[EVENT_CPF_CHKPT_ID])
            
            #   Update event status
            global _SQL_EVENT_UPDATE_STATUS
            _SQL_EVENT_UPDATE_STATUS = db.gen_update(
                    [EVENT_CPF_STATUS],
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
            
        return
        
    def get_next_event_checkpoint_rec_id(self): 
        ''' Get the next event checkpoint rec id '''
        tmp_rec_id = None
        if self.use_db == True: 
            self.chkpt_recid_lock.acquire()
            self.event_checkpoint_rec_id += 1
            tmp_rec_id = self.event_checkpoint_rec_id
            self.chkpt_recid_lock.release()
            self.event_checkpoint_rec_id = tmp_rec_id
        return tmp_rec_id
      
    def register_event_checkpoint(self, checkpoint):
        ''' Register the event checkpoint with the manager '''
        self.event_checkpoints[checkpoint.name] = checkpoint
        return 
    
    def unregister_event_checkpoint(self, checkpoint):
        ''' Unregister the event checkpoint with the manager '''
        del self.event_checkpoints[checkpoint.name]
        return 
        
    def get_starting_event_rec_id(self, override_restart_mode=None):
        '''
        Use the mode and checkpoints to determine what rec_id should
        be used to start event retrieval
        
           Mode         Behavior
            begin        start at first event in event log (0)
            recovery     start at first failure.  If not failures then like lastproc
            lastproc     start at the last event in the event log that was processed by anyone.
            now          start after max rec_id in event log
             
        default is recovery
           if specified during init (from TEAL input) then that is used
           else if specified in the monitoring stanza that is used 
           
        Checkpoints are prepared for restart    
        
        Returns (start_event_rec_id, mode_used)
        '''
        t_restart_mode = self.restart_mode
        if t_restart_mode is None:
            if override_restart_mode is not None:
                if override_restart_mode not in RESTART_MODES:
                    raise ConfigurationError('Unrecognized restart mode specified: {0}'.format(override_restart_mode))
                t_restart_mode = override_restart_mode
            else:
                t_restart_mode = RESTART_MODE_RECOVERY
                
        start_eri = None
        # Process based on restart mode 
        if t_restart_mode == RESTART_MODE_RECOVERY:
            # Find the earliest we have to start to retry failures
            min_start = None
            # Find the last one anyone processed
            max_start = None
            
            for t_ckpt in self.event_checkpoints.values():
                # Collect minimum of non-shutdown checkpoints
                if t_ckpt.status != CHECKPOINT_STATUS_SHUTDOWN:
                    t_min_start = t_ckpt.get_starting_event_rec_id()
                    if t_min_start is not None:
                        if min_start is None:
                            min_start = t_min_start
                        else:
                            min_start = min(min_start, t_min_start)
                # Collect maximum of all checkpoints
                t_max_start = t_ckpt.start_rec_id
                if t_max_start is not None:
                    if max_start is None:
                        max_start = t_max_start
                    else:
                        max_start = max(max_start, t_max_start)
            # if there is a min, something failed, so use it
            if min_start is not None:
                start_eri = min_start
            else:
                start_eri = max_start
                
        elif t_restart_mode == RESTART_MODE_BEGIN:
            start_eri = 0
        elif t_restart_mode == RESTART_MODE_LASTPROC:
            # Find the last event processed
            for t_ckpt in self.event_checkpoints.values():
                t_start = t_ckpt.start_rec_id
                if t_start is not None:
                    if start_eri is None:
                        start_eri = t_start
                    else:
                        start_eri = max(start_eri, t_start)
        # ELSE: default (None) is what should be returned for 'now' (the only option left) 
        
        if start_eri is None and self.use_db == True:
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
                    
        get_logger().info('Checkpoint manager used \'{0}\' to determine starting event rec id = {1}'.format(t_restart_mode, str(start_eri)))

        # Prepare checkpoints for restart 
        for t_ckpt in self.event_checkpoints.values():
            t_ckpt.prepare_for_restart(t_restart_mode, start_eri)
        
        return (start_eri, t_restart_mode)
    
    def shutdown(self):
        ''' Do any shutdown processing '''
        if len(self.event_checkpoints) != 0:
            if self.use_db == True:
                dump = False
                for t_ckpt in self.event_checkpoints.values():
                    if t_ckpt.status != CHECKPOINT_STATUS_SHUTDOWN:
                        dump = True
                if dump == False:
                    return 
                
            get_logger().info('<<START: SHUTDOWN DUMP OF CHECKPOINTS\n {0}'.format(str(self)))
            get_logger().info('>>END: SHUTDOWN DUMP OF CHECKPOINTS')
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
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        if checkpoint_mgr.use_db == True:
            # Get entry for name in DB
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(_SQL_EVENT_SELECT_BY_NAME, (name))
            row = cursor.fetchone()

            if row is not None:
                get_logger().debug('Found entry for {0}'.format(name))
                self.ckpt_rec_id, self.name, self.status, self.start_rec_id, self.data = row 
            else:
                self.ckpt_rec_id = checkpoint_mgr.get_next_event_checkpoint_rec_id()
                cursor.execute(_SQL_EVENT_INSERT, (self.ckpt_rec_id, self.name, self.status, self.start_rec_id, self.data))
                cnxn.commit()
            cnxn.close()       
 
            self.set_status = self.set_status_DB
            self.set_checkpoint = self.set_checkpoint_DB
            self.set_checkpoint_no_data = self.set_checkpoint_no_data_DB
            
        checkpoint_mgr.register_event_checkpoint(self)
        return 
    
    def get_status(self):
        ''' get status ''' 
        if self.status is None:
            return CHECKPOINT_STATUS_UNKNOWN
        return self.status
        
    def get_checkpoint(self):
        ''' get the checkpoint data '''
        return (self.start_rec_id, self.data)
    
    def get_starting_event_rec_id(self):
        ''' Return the rec_id to start with '''
        # If shutdown or not starting rec_id don't have special requirements 
        if self.status == CHECKPOINT_STATUS_SHUTDOWN or self.start_rec_id is None:
            return None
        return self.start_rec_id
    
    def prepare_for_restart(self, restart_mode, restart_rec_id):        
        ''' Prepare for restarting with the restart mode and specified rec_id
        based on the context of the mode and the starting rec_id to determine what to do.
        '''
        self.set_status(CHECKPOINT_STATUS_RUNNING)
        if restart_mode == RESTART_MODE_NOW or restart_mode == RESTART_MODE_BEGIN:
            self.set_checkpoint(None)
        return 
        
    def set_status(self, status):
        ''' set status '''
        get_logger().info('Updating status for {0} from {1} to {2}'.format(self.name, self.status, status))
        self.status = status
        return 
    
    def set_status_DB(self, status):
        ''' set status '''
        get_logger().info('Updating status for {0} from {1} to {2}'.format(self.name, self.status, status))
        self.status = status
        try:
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            if cursor.execute(_SQL_EVENT_UPDATE_STATUS, (status, self.ckpt_rec_id)).rowcount == 0:
                self.retry_db_update(dbi, cnxn, cursor)
            cnxn.commit()
            cnxn.close()
        except:
            # Log and hope we get it the next time
            get_logger().exception('Failure updating checkpoint {0}'.format(str(self)))
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
        self.start_rec_id = start_rec_id
        self.data = data
        try:
            if data is not None and len(data) > MAX_CHECKPOINT_DATA_SIZE:
                get_logger().warning('Checkpoint failure: length of data {0} too large\n data: {1}'.format(len(data), str(data))) 
                self.data = None
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            if cursor.execute(_SQL_EVENT_UPDATE_CHECKPOINT, (start_rec_id, self.data, self.ckpt_rec_id)).rowcount == 0:
                self.retry_db_update(dbi, cnxn, cursor)
            cnxn.commit()
            cnxn.close()
        except:
            # Log and hope we get it the next time
            get_logger().exception('Failure updating checkpoint {0}'.format(str(self)))
        return 
    
    def set_checkpoint_no_data(self, start_rec_id):
        ''' set the checkpoint data '''
        get_logger().debug('Updating checkpoint for {0} from {1} to {2}'.format(self.name, self.start_rec_id, start_rec_id))
        self.start_rec_id = start_rec_id
        return
    
    def set_checkpoint_no_data_DB(self, start_rec_id):
        ''' set the checkpoint data '''
        get_logger().debug('Updating checkpoint for {0} from {1} to {2}'.format(self.name, self.start_rec_id, start_rec_id))
        self.start_rec_id = start_rec_id
        try:
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            if cursor.execute(_SQL_EVENT_UPDATE_CHECKPOINT_NO_DATA, (start_rec_id, self.ckpt_rec_id)).rowcount == 0:
                self.retry_db_update(dbi, cnxn, cursor)
            cnxn.commit()
            cnxn.close()
        except:
            # Log and hope we get it the next time
            get_logger().exception('Failure updating checkpoint {0}'.format(str(self)))
        return 
    
    def set_checkpoint_DELETED(self, start_rec_id, data=None):
        ''' Cannot set checkpoint if deleted '''
        get_logger().warning('Tried to set checkpoint on deleted checkpoint {0}'.format(self.name))
        return 
    
    def delete(self):
        ''' Mark the checkpoint as deleted '''
        checkpoint_mgr = get_service(SERVICE_CHECKPOINT_MGR)
        checkpoint_mgr.unregister_event_checkpoint(self)
        
        self.status = CHECKPOINT_STATUS_DELETED
        self.start_rec_id = None
        self.data = None
        self.starting_cb = None
        self.set_status = self.set_status_DELETED
        self.set_checkpoint = self.set_checkpoint_DELETED
        
        if checkpoint_mgr.use_db == True:
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
    
    def retry_db_update(self, dbi, cnxn, cursor):
        ''' DB write failed -- retry it '''
        # Try to validate the data
        try:
            if self.start_rec_id is not None:
                # See if the value for self.start_rec_id is valid
                dbi.select(cursor,
                           [EVENT_ATTR_REC_ID],
                           db_interface.TABLE_EVENT_LOG, 
                           where='${0} = ?'.format(EVENT_ATTR_REC_ID),
                           where_fields=[EVENT_ATTR_REC_ID], 
                           parms=(self.start_rec_id))
                if cursor.rowcount == 0 or cursor.fetchone() is None:
                    # Checkpoint rec id is no longer valid
                    self.start_rec_id = None
                    self.data = None 
            # See if entry for this checkpoint
            if cursor.execute(_SQL_EVENT_SELECT_BY_NAME, (self.name)).rowcount == 0 or cursor.fetchone() is None:
                # No entry, so insert it
                cursor.execute(_SQL_EVENT_INSERT, (self.ckpt_rec_id, self.name, self.status, self.start_rec_id, self.data))
            else:
                # Entry, so try to update it
                cursor.execute(_SQL_EVENT_UPDATE_CHECKPOINT, (self.start_rec_id, self.data, self.ckpt_rec_id) )
                cursor.execute(_SQL_EVENT_UPDATE_STATUS, (self.status, self.ckpt_rec_id) )
        except:
            # Log and hope we get it the next time
            get_logger().exception('Failure updating checkpoint {0}'.format(str(self)))
        return 
    
    def __str__(self):
        ''' dump the checkpoint into a string '''
        outstr = 'Checkpoint {0}({1}) -- {2} '.format(self.name, self.ckpt_rec_id, self.get_status())
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
        return

    def process_event(self,event,context):
        get_logger().debug('CheckpointListener: process_event')
        # Get the needed event information.
        try:
            self.event_checkpoint.set_checkpoint_no_data(event.rec_id)
        except:
            get_logger().exception('Unable to update checkpoint rec_id for {0}'.format(self.name))
        return False

    def process_alert(self,alert,context):
        ''' Handle double dispatch from an alert.
        This listener does not handle alerts. '''
        get_logger().error('CheckpointListener was given an alert.')
        return False

    def process_control_msg(self, control_msg, context):
        get_logger().debug('CheckpointListener: process_control_msg')
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            try:
                self.event_checkpoint.set_status(CHECKPOINT_STATUS_SHUTDOWN)
                # Default is to leave checkpointed rec id alone 
            except:
                get_logger().exception('Unable to update checkpoint status to shutdown for {0}'.format(self.name))

            self.shutdown()
            self.listenQ.unregister_listener(self)
        return True
    
    
class CheckpointRecoveryComplete(TealError):
    ''' Used to throw exception indicating that the checkpoint has completed recovery and
        that normal processing can be resumed.
    '''
    
    def __init__(self, msg):
        ''' Message will be logged ''' 
        if msg is None:
            msg = 'Checkpoint Recovery Complete'
        TealError.__init__(self, msg, False) # Not a Error 
        return 
