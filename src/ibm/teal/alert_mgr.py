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
import threading
from collections import defaultdict
from datetime import datetime
from ibm.teal.alert import Alert, ALERT_ATTR_REC_ID, ALERT_STATE_INCOMPLETE, \
    ALERT_STATE_AS_STRING, ALERT_STATE_OPEN, ALERT_STATE_CLOSED, ALERT_ATTR_ASSOC, \
    ALERT2ALERT_COLS, ALERT2EVENT_COLS, ALERT_ATTR_CREATION_TIME, ALERT_ATTR_ALERT_ID, \
    ALERT_ATTR_STATE, ALERT_SEVERITY_VALUES, ALERT_URGENCY_VALUES, \
    ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY
from ibm.teal.database import db_interface
from ibm.teal.registry import get_logger, get_service, SERVICE_DB_INTERFACE,\
    SERVICE_ALERT_DELIVERY_Q
from ibm.teal.teal_error import ConfigurationError, TealError
from string import upper
import weakref

ALERT_DUPLICATE_CHECK = 'TEAL_ALERT_DUPLICATE_CHECK'


class AlertMgr(object):
    '''This is the manager of the in memory instances of the Alerts    
    '''
    
    def __init__(self, use_backing_db=False):
        '''Constructor
             use_backing_db -- boolean -- should a backing db be used for alerts.
        '''
        self.alloc_rec_id = 0

        self.use_backing_db = use_backing_db
        if self.use_backing_db:
            get_logger().debug('Alert Manager is using a backing DB')
            dbi = get_service(SERVICE_DB_INTERFACE)
            if dbi is None:
                raise ConfigurationError('AlertMgr requires that a DB interface be active (configured) when committing alerts' )
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            dbi.select_max(cursor, 'rec_id', db_interface.TABLE_ALERT_LOG)
            row = cursor.fetchone()
            if row and row[0]:
                self.cur_rec_id = row[0]
            else:
                self.cur_rec_id = 0
            get_logger().debug('Alert Manager starting after rec_id = {0}'.format(self.cur_rec_id))
            cnxn.close()
            self.in_mem_alerts = None
            where_active_alerts = 'AND $rec_id NOT IN ({0})'.format(dbi.gen_select(['t_alert_recid'], db_interface.TABLE_ALERT2ALERT,where="$assoc_type = 'D'", where_fields=['assoc_type']))
            # if use above must add: 'state','rec_id' to where_fields
            self.sql_update_state = dbi.gen_update(['state'], db_interface.TABLE_ALERT_LOG, 
                       where='$state = ? AND $rec_id = ? {0}'.format(where_active_alerts), 
                       where_fields=['state','rec_id'])
            self.sql_get_state = dbi.gen_select(['state'], db_interface.TABLE_ALERT_LOG,
                           where='$rec_id = ?', where_fields=['rec_id'])
            sub_sel = dbi.gen_select(['t_alert_recid'], db_interface.TABLE_ALERT2ALERT, where="$alert_recid = ? AND $assoc_type = 'D'", where_fields=['alert_recid', 'assoc_type'])
            self.sql_update_dup_state = dbi.gen_update(['state'], db_interface.TABLE_ALERT_LOG,
                       where='$rec_id IN ({0})'.format(sub_sel), 
                       where_fields=['rec_id'])
            self.sql_select_poss_dup = dbi.gen_select([ALERT_ATTR_REC_ID, ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY], 
                       db_interface.TABLE_ALERT_LOG, 
                       where='$alert_id = ? AND $event_loc_type = ? AND $event_loc = ? {0} AND $state != 2'.format(where_active_alerts), 
                       where_fields=['rec_id', 'state', 'alert_id', 'event_loc_type', 'event_loc'])
            self.sql_select_is_dup = dbi.gen_select(['alert_recid'],
                                                    db_interface.TABLE_ALERT2ALERT,
                                                    where="$t_alert_recid = ? AND $assoc_type = 'D'",
                                                    where_fields=['t_alert_recid', 'assoc_type'])
        else:
            get_logger().debug('Alert Manager is NOT using a backing DB')
            # Start rec ids at 1 (0 is current max)
            self.cur_rec_id = 0
            self.in_mem_alerts = {}
            self.in_mem_alerts_duplicate = []
            self.active_alerts_open = []
            self.active_alerts_closed = []
        self.commit_recid_lock = threading.Lock()
        self.alloc_recid_lock = threading.Lock()
        if upper(os.environ.get(ALERT_DUPLICATE_CHECK, 'YES')) == 'YES':
            self._check_if_duplicate = self._check_if_duplicate_check
        else:
            get_logger().info('Alert duplicate checking has been turned off')
            self._check_if_duplicate = self._check_if_duplicate_pass
        return
    
    def allocate(self, alert_id, in_dict):
        ''' allocate the in memory alert only 
            to write to the DB commit must be called
        '''
        self.alloc_recid_lock.acquire()
        self.alloc_rec_id -= 1
        tmp_rec_id = self.alloc_rec_id
        self.alloc_recid_lock.release()
        get_logger().debug('Allocating alert with rec_id = {0}'.format(str(tmp_rec_id)))
        return Alert(tmp_rec_id, alert_id, in_dict)
        
    def commit(self, alert, disable_dup=False):
        ''' commit the alert to the backing DB
        '''
        # Make sure defaults are filled in and that all required fields are set
        get_logger().debug('Committing alert with rec_id = {0}'.format(alert.rec_id))
        alert.resolve_and_validate()
        
        if alert.state != ALERT_STATE_INCOMPLETE:
            get_logger().warning('Alert {0} already committed'.format(alert.rec_id))
            # Allows for injection of alerts with state
            
        alert.state = ALERT_STATE_OPEN
        self.commit_recid_lock.acquire()
        self.cur_rec_id += 1
        tmp_rec_id = self.cur_rec_id
        self.commit_recid_lock.release()
        get_logger().debug('Assigning alert with alloc rec_id = {0} commit rec_id {1}'.format(alert.rec_id, str(tmp_rec_id)))
        alert.rec_id = tmp_rec_id
        
        if disable_dup is False:
            duplicate_of = self._check_if_duplicate(alert)
        else:
            duplicate_of = None
        alert.creation_time = datetime.now()    
        if self.use_backing_db:
            # Put it in the DB and get the generated info
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            tmp_dict = alert.write_to_dictionary()
            if ALERT_ATTR_ASSOC in tmp_dict:
                del tmp_dict[ALERT_ATTR_ASSOC]
            get_logger().debug('Committing alert with rec_id = {0} INSERT'.format(alert.rec_id))
            try:
                try:
                    dbi.insert(cursor, tmp_dict.keys(), db_interface.TABLE_ALERT_LOG, tmp_dict.values())
                except:
                    get_logger().exception('Commit of alert {0}({1}) failed init_dict = {2}'.format(alert.alert_id, alert.rec_id, str(tmp_dict)))
                    raise
                get_logger().debug('Committing alert with rec_id = {0} COMPLETE'.format(alert.rec_id))
                # Do not cnxn.commit() because only want to do if associations get written
                # Insert associations
                assoc_cursor = cnxn.cursor()
                try:
                    # Suppressions
                    self._add_alert_assoc_to_table(alert.rec_id, alert.supresses, 'S', use_cursor=assoc_cursor, dbi=dbi)
                    # Condition events
                    self._add_alert_assoc_to_table(alert.rec_id, alert.condition_events, 'C', use_cursor=assoc_cursor, dbi=dbi)
                    # If duplicate then add association from the alert this is a duplicate of
                    if duplicate_of is not None:
                        dbi.insert(assoc_cursor, ALERT2ALERT_COLS, db_interface.TABLE_ALERT2ALERT, (duplicate_of, 'D', alert.rec_id))
                except:
                    get_logger().exception('Commit of alert {0}({1}) association update failed'.format(alert.alert_id, alert.rec_id))
                    get_logger().error('    suppressions = {0}'.format(str(alert.supresses)))
                    get_logger().error('    condition events = {0}'.format(str(alert.condition_events)))
                    raise
                cnxn.commit()
            except:
                cnxn.rollback()
            cnxn.close()
        else:
            self.in_mem_alerts[alert.rec_id] = InMemAlert( alert=alert )
            if duplicate_of is None:
                self.active_alerts_open.append(alert.rec_id)
            else:
                # Keep the list of alerts that are duplicates of
                # an active in memory alert up-to-date
                self.in_mem_alerts[duplicate_of].duplicates.add(alert.rec_id)
                
                # Keep the list of all alerts that are duplicates
                # up-to-date for simple duplicate checking
                self.in_mem_alerts_duplicate.append(alert.rec_id)
        return
    
    def _check_if_duplicate_pass(self, alert):
        ''' Used when duplicate checking is turned off '''
        return None
    
    def _check_if_duplicate_check(self, alert):
        ''' check if duplicate alert and return the recid of what it is a duplicate of if it is
            else return none
        '''
        get_logger().debug('Checking for duplicates for alert {0}({1})'.format(alert.alert_id, alert.rec_id))
        result = None
        if self.use_backing_db:
            # Get potential alerts it could be a duplicate of from DB
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(self.sql_select_poss_dup, (alert.alert_id, alert.event_loc.get_id(), alert.event_loc.get_location()))
            while 1:
                row = cursor.fetchone()
                if row is None:
                    break
                r_rec_id, r_severity, r_urgency = row
                if ALERT_SEVERITY_VALUES.index(r_severity) > ALERT_SEVERITY_VALUES.index(alert.severity):
                    continue
                if ALERT_URGENCY_VALUES.index(r_urgency) > ALERT_URGENCY_VALUES.index(alert.urgency):
                    continue
                result = r_rec_id
            get_logger().debug('   >>>> Duplicate <<<<')
            cnxn.commit()
            cnxn.close()
        else:
            # Iterate through all of the in memory alerts to check if duplicate
            for ex_alert_id in self.active_alerts_open:
                ex_in_mem_alert = self.in_mem_alerts[ex_alert_id]
                get_logger().debug('Checking against alert {0}({1})'.format(ex_in_mem_alert.alert_id, ex_alert_id))
                if ex_in_mem_alert.state == ALERT_STATE_CLOSED or \
                   ex_in_mem_alert.alert_id != alert.alert_id or \
                   ex_in_mem_alert.event_loc != alert.event_loc:   # Only if exactly the same location
                    continue
                if ALERT_SEVERITY_VALUES.index(ex_in_mem_alert.severity) > ALERT_SEVERITY_VALUES.index(alert.severity):
                    continue
                if ALERT_URGENCY_VALUES.index(ex_in_mem_alert.urgency) > ALERT_URGENCY_VALUES.index(alert.urgency):
                    continue
                result = ex_alert_id
                get_logger().debug('   >>>> Duplicate <<<<')
                break
        return result
   
    def close(self, rec_id):
        ''' Indicate that the alert should be closed 
            This will also close any duplicate alerts
        ''' 
        get_logger().debug('Closing alert {0}'.format(rec_id))
        if self.use_backing_db:
            failed = False
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(self.sql_update_state,(ALERT_STATE_CLOSED, ALERT_STATE_OPEN, rec_id)) 
            if cursor.rowcount == 0:
                failed = True
                # Failures could be due to: (1) rec_id bad, (2) alert already closed, or (3) duplicate
                # Get entry from alert log 
                cursor.execute(self.sql_get_state, (rec_id,))
                row = cursor.fetchone()
                # Process error after close up the DB connection
            else:
                # Updated the duplicates
                cursor.execute(self.sql_update_dup_state, (ALERT_STATE_CLOSED, rec_id)) 
            cnxn.commit()
            cnxn.close()
            if failed:
                if row is None:
                    # (1) rec_id is bad
                    raise AlertMgrError(AlertMgrError.AME_RC_RECID_MSG, AlertMgrError.AME_RC_RECID)
                tmp_state = row[0]
                if tmp_state == ALERT_STATE_CLOSED:
                    # (2) alert already closed
                    raise AlertMgrError(AlertMgrError.AME_RC_STATE_MSG, AlertMgrError.AME_RC_STATE)
                # (3) duplicate 
                raise AlertMgrError(AlertMgrError.AME_RC_DUPE_MSG, AlertMgrError.AME_RC_DUPE)
        else:
            if rec_id in self.in_mem_alerts:
                if self.in_mem_alerts[rec_id].state == ALERT_STATE_CLOSED:
                    raise AlertMgrError(AlertMgrError.AME_RC_STATE_MSG, AlertMgrError.AME_RC_STATE)
                if rec_id not in self.active_alerts_open:
                    raise AlertMgrError(AlertMgrError.AME_RC_DUPE_MSG, AlertMgrError.AME_RC_DUPE)
                self.in_mem_alerts[rec_id].set_state(ALERT_STATE_CLOSED)
                self.active_alerts_open.remove(rec_id)
                self.active_alerts_closed.append(rec_id)
                for dupe_id in self.in_mem_alerts[rec_id].duplicates:
                    self.in_mem_alerts[dupe_id].set_state(ALERT_STATE_CLOSED)
            else:
                raise AlertMgrError(AlertMgrError.AME_RC_RECID_MSG, AlertMgrError.AME_RC_RECID)

        return
    
    def reopen(self, rec_id):
        ''' Indicate that the alert should be reopened
            This will also reopen any duplicate alerts
        ''' 
        get_logger().debug('Reopening alert {0}'.format(rec_id))
        if self.use_backing_db:
            failed = False
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            cursor.execute(self.sql_update_state, (ALERT_STATE_OPEN, ALERT_STATE_CLOSED, rec_id)) 
            if cursor.rowcount == 0:
                # Failures could be due to: (1) rec_id bad, (2) alert already open, or (3) duplicate
                failed = True
                # Failed to updated for some reason
                cursor.execute(self.sql_get_state, (rec_id,))
                row = cursor.fetchone()
            else:
                # Update the duplicates
                cursor.execute(self.sql_update_dup_state, (ALERT_STATE_OPEN, rec_id)) 
            cnxn.commit()
            cnxn.close()
            if failed:
                if row is None:
                    # (1) rec_id bad
                    raise AlertMgrError(AlertMgrError.AME_RC_RECID_MSG, AlertMgrError.AME_RC_RECID)
                tmp_state = row[0]
                if tmp_state == ALERT_STATE_OPEN:
                    # (2) alert already open
                    raise AlertMgrError(AlertMgrError.AME_RC_STATE_MSG, AlertMgrError.AME_RC_STATE)
                # (3) duplicate
                raise AlertMgrError(AlertMgrError.AME_RC_DUPE_MSG, AlertMgrError.AME_RC_DUPE)
        else:
            if rec_id in self.in_mem_alerts:
                if self.in_mem_alerts[rec_id].state == ALERT_STATE_OPEN:
                    raise AlertMgrError(AlertMgrError.AME_RC_STATE_MSG, AlertMgrError.AME_RC_STATE)
                if rec_id not in self.active_alerts_closed:
                    raise AlertMgrError(AlertMgrError.AME_RC_DUPE_MSG, AlertMgrError.AME_RC_DUPE)
                self.in_mem_alerts[rec_id].set_state(ALERT_STATE_OPEN)
                self.active_alerts_closed.remove(rec_id)
                self.active_alerts_open.append(rec_id)
                for dupe_id in self.in_mem_alerts[rec_id].duplicates:
                    self.in_mem_alerts[dupe_id].set_state(ALERT_STATE_OPEN)
            else:
                raise AlertMgrError(AlertMgrError.AME_RC_RECID_MSG, AlertMgrError.AME_RC_RECID)

        return
        
    def update(self, alert, in_dict):
        ''' Update the alert with the values in the dictionnary ''' 
        get_logger().debug('Updating alert {0}'.format(alert.rec_id))
        # Update the in memory version
        alert.am_update(in_dict)

        # If alert has not been commited yet 
        if alert.state == ALERT_STATE_INCOMPLETE:
            return
        if self.use_backing_db:
            if ALERT_ATTR_REC_ID in in_dict or ALERT_ATTR_CREATION_TIME in in_dict or \
            ALERT_ATTR_ALERT_ID in in_dict or ALERT_ATTR_ASSOC in in_dict or \
            ALERT_ATTR_STATE in in_dict:
                get_logger().warning('Update input dictionary contains unsupported entries')
                # Programming error, so don't tolerate
                raise ValueError
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            dbi.update(cursor, in_dict.keys(), db_interface.TABLE_ALERT_LOG, where='$rec_id = ?', where_fields=['rec_id'], parms=in_dict.values().append(alert.rec_id))
            cnxn.commit()
            cnxn.close()
        else: 
            # Update the in memory alert
            self.in_mem_alerts[alert.rec_id].update()
        return
    
    def add_suppressions(self, alert, in_set):
        ''' Add suppressions to the alert '''
        get_logger().debug('Adding suppressions to alert {0}'.format(alert.rec_id))
        # Update the in-memory alert
        alert.am_add_suppressions(in_set)
        if alert.state == ALERT_STATE_INCOMPLETE:
            return 
        if self.use_backing_db:
            self._add_alert_assoc_to_table(alert.rec_id, in_set, 'S')
        else: 
            # Currently not tracking suppressions if in memory 
            pass
        return
    
    def _add_alert_assoc_to_table(self, alert_recid, in_set, type, use_cursor=None, dbi=None):
        ''' Add entries in the set to the alert association table using the specified type '''
        if use_cursor is None:
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            assoc_cursor = cnxn.cursor()
        else:
            assoc_cursor = use_cursor
        # Suppressions
        for item in in_set:
            if item.get_type() == 'E':
                t_event_recid = long(item.get_rec_id())
                dbi.insert(assoc_cursor, ALERT2EVENT_COLS, db_interface.TABLE_ALERT2EVENT, (alert_recid, type, t_event_recid))

            elif item.get_type() == 'A':
                t_event_recid = None
                t_alert_recid = long(item.get_rec_id())
                dbi.insert(assoc_cursor, ALERT2ALERT_COLS, db_interface.TABLE_ALERT2ALERT, (alert_recid, type, t_alert_recid))

            else:
                # This cannot happen
                get_logger().error('Encountered item type {0} which is not supported'.format(item.get_type()))
                continue

        if use_cursor is None:
            cnxn.commit()
            cnxn.close()
        return
    
    def shutdown(self):
        # Process shutdown
        get_logger().debug('Alert Manager shutdown')
        if self.use_backing_db == False:
            get_logger().info('<<START: SHUTDOWN DUMP OF ALERTS\n {0}'.format(self.dump_in_memory_alerts()))
            get_logger().info('>>END: SHUTDOWN DUMP OF ALERTS')
        return
    
    def is_duplicate(self, alert_recid):
        ''' Determine if the alert is a duplicate of an alert
        '''
        if self.use_backing_db:
            dbi = get_service(SERVICE_DB_INTERFACE)
            cnxn = dbi.get_connection()
            cursor = cnxn.cursor()
            
            cursor.execute(self.sql_select_is_dup, [alert_recid])
            row = cursor.fetchone()
            
            if row is None or row[0] is None:
                duplicate = False
            else:
                duplicate = True
            
            cnxn.close()
            return duplicate
        else:
            return (alert_recid in self.in_mem_alerts_duplicate)
            
    def create_and_deliver_alert(self, alert_id, alert_init_dict, disable_dup=False):
        ''' create (allocate and commit) an alert and put it on the delivery queue '''
        try:
            # Get the alert manager to create/allocate/commit the alert
            teal_alert = self.allocate(alert_id, in_dict=alert_init_dict)
            self.commit(teal_alert, disable_dup=disable_dup)
            get_service(SERVICE_ALERT_DELIVERY_Q).put(teal_alert)
        except:
            get_logger().exception('Unable to create alert with alert id = {0}'.format(alert_id))
            if alert_init_dict is not None:
                get_logger().info('Alert was being created using: {0}'.format(str(alert_init_dict)))
        return 

    def dump_in_memory_alerts(self):
        ''' Dump the alert information to a string ... if in memory '''
        if self.use_backing_db:
            return ''
        
        if len(self.in_mem_alerts) == 0:
            return '-empty-\n'
        
        outstr = ''
        alert_by_state = defaultdict(list)
        for key in self.in_mem_alerts:
            o_in_mem_alert = self.in_mem_alerts[key]
            if key in self.in_mem_alerts_duplicate:
                o_dup = 'D'
            else:
                o_dup = ' '
            alert_by_state[ALERT_STATE_AS_STRING[o_in_mem_alert.state]].append('{0} {1:5d}: {2} {3} {4}'.format( \
                   o_dup, key, o_in_mem_alert.alert_id, o_in_mem_alert.creation_time.strftime('%H:%M:%S.%f'), \
                   str(o_in_mem_alert.event_loc)))
            
        for o_state in alert_by_state.keys():
            outstr += ' {0}:'.format(o_state)
            for o_alert_info in alert_by_state[o_state]:
                outstr += '\n   {0}'.format(o_alert_info)
        return outstr
    
    
class AlertMgrError(TealError):
    ''' Exception for Alert Manager errors 
    '''
    
    # RC values
    AME_RC_RECID = 1
    AME_RC_RECID_MSG = 'Alert with specified record id not found' 
    AME_RC_STATE = 2
    AME_RC_STATE_MSG = 'Current alert state does not allow this operation'
    AME_RC_DUPE = 3
    AME_RC_DUPE_MSG = 'Operation not allowed on duplicate alert'
    
    def __init__(self, msg, rc):
        '''Add rc to the exception'''
        self.rc = rc
        TealError.__init__(self, msg)
        return

    def __str__(self):
        '''Print out additional information'''
        return 'rc = {0}: {1}'.format(self.rc, TealError.__str__(self))  

class InMemAlert(object):
    ''' In memory version of alert that has the minimum amount of information 
        ????? Also keep a weak reference to the alert and reflect updates to it as well ????? 
    '''
    
    def __init__(self, alert):
        ''' initialize with minimal data '''
        self.alert_wr = weakref.ref(alert)
        self.update()
        self.duplicates = set()
        return
    
    def update(self):
        ''' Update values from originally passed in alert '''
        tmp_alert = self.alert_wr()
        if tmp_alert is not None: 
            self.alert_id = tmp_alert.alert_id
            self.event_loc = tmp_alert.event_loc
            self.severity = tmp_alert.severity
            self.urgency = tmp_alert.urgency
            self.state = tmp_alert.state
            self.creation_time = tmp_alert.creation_time
            self.condition_events = [e.rec_id for e in tmp_alert.condition_events]
        return 
        
    
    def set_state(self, new_state):
        ''' Set the in memory alert to closed.   If the original alert is still 
            in memory set its state to closed as well '''
        self.state = new_state
        tmp_alert = self.alert_wr()
        if tmp_alert is not None: 
            tmp_alert.state = new_state
        return 
