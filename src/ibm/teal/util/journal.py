# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
from abc import ABCMeta, abstractmethod
from datetime import datetime
from ibm.teal.alert import ALERT_ATTR_CREATION_TIME, ALERT_ATTR_REC_ID, \
    ALERT_ATTR_ALERT_ID, ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY, \
    ALERT_ATTR_EVENT_LOC, ALERT_ATTR_EVENT_LOC_TYPE, ALERT_ATTR_FRU_LOC, \
    ALERT_ATTR_RECOMMENDATION, ALERT_ATTR_REASON, ALERT_ATTR_SRC_NAME, \
    ALERT_ATTR_STATE, ALERT_ATTR_RAW_DATA, ALERT_ATTR_ASSOC, ALERT_STATE_AS_STRING, \
    ALERT_COLS_SELECT, ALERT2ALERT_COLS, ALERT2EVENT_COLS, ALERT_STATE_OPEN,\
    ALERT_STATE_CLOSED
from ibm.teal.control_msg import ControlMsg, CONTROL_MSG_ATTR_CREATION_TIME, \
    CONTROL_MSG_ATTR_MSG_TYPE, CONTROL_MSG_TYPE_AS_STRING,\
    CONTROL_MSG_TYPE_END_OF_DATA, CONTROL_MSG_ATTR_DATA_DICT
from ibm.teal.database import db_interface
from ibm.teal.event import Event, EVENT_ATTR_RAW_DATA, EVENT_ATTR_REC_ID, \
    EVENT_ATTR_TIME_LOGGED, EVENT_ATTR_EVENT_ID, EVENT_ATTR_SRC_COMP, \
    EVENT_ATTR_SRC_LOC, EVENT_ATTR_SRC_LOC_TYPE, EVENT_ATTR_TIME_OCCURRED, \
    EVENT_ATTR_RPT_LOC_TYPE, EVENT_ATTR_ELAPSED_TIME, EVENT_ATTR_RPT_COMP, \
    EVENT_ATTR_RPT_LOC, EVENT_ATTR_EVENT_CNT, EVENT_ATTR_RAW_DATA_FMT, EVENT_COLS
from ibm.teal.listener.alert_listener import AlertListener
from ibm.teal.registry import get_logger, SERVICE_ALERT_MGR, get_service, \
    SERVICE_DB_INTERFACE, SERVICE_NOTIFIER
from ibm.teal.util.listenable_queue import QueueListener, ListenableQueueWatcher
from ibm.teal.util.msg_target import MsgTargetLogger, msg_target_ignore
from time import sleep
import binascii
import json
import os
from ibm.teal.location import Location


JE_TYPE_EVENT = 'event'
JE_TYPE_ALERT = 'alert'
JE_TYPE_CONTROL_MSG = 'control_msg'

JE_KEY_TYPE = 'type'
JE_KEY_DELAY = 'delay'
JE_KEY_DATA = 'data'

JSON_KEY_TYPE = 'type'
JSON_KEY_DELAY = 'delay'
JSON_KEY_DATA = 'data'

# Events that a Journal can send
J_EVENT_AS_STRING = ['Entry Added', 'Entry Deleted', 'Entry Edited', 'Saved', \
                     'Loaded', 'Injection_complete', 'Injected', 'Cleared']
J_EVENT_JE_ADD = 0  # + sequence #
J_EVENT_JE_DEL = 1  # + sequence #
#J_EVENT_JE_EDT = 2  # + sequence #
J_EVENT_SAVED = 3   # + file name
J_EVENT_LOADED = 4  # + file name
J_EVENT_INJECTION_COMPLETE = 5 # + target
J_EVENT_INJECTED = 6 # + sequence #
J_EVENT_CLEARED = 7 # 

# Utilities
def _ustr2str(value):
    ''' Translate unicode string to ascii string.
    This is needed so unicode data does not get written to the database
    '''
    if isinstance(value,unicode):
        return str(value)
    else:
        return value    
 

class Journal(dict, QueueListener):
    '''
    The Journal class is used to internally represent a set of Events, Alerts, and 
    Control Messages and the order they occurred.
    
    It can be saved to and loaded from a file, it can be compared to other Journals, 
    it can be injected into different points in the framework and it can be recorded into
    from different points as well
    
    Note that Journals do not currently support multithreaded access
    '''

    def __init__(self, name, file=None):
        '''
        Constructor: Create an empty journal
        '''
        self.max_seq_num = 0
        self.last_journal_time = None
        self.name = name
        self.jevent_listeners = []
        dict.__init__(self)
        # Need the dict setup 
        self.load(file)
        return
    
    def get_name(self):
        ''' return name -- for Listener'''
        return self.name
    
    def register_for_jevents(self, queue):
        ''' Register a queue to get events '''
        self.jevent_listeners.append(queue)
        return
    
    def unregister_for_jevents(self, queue):
        ''' Unregister a queue to get events '''
        self.jevent_listeners.remove(queue)
        return
    
    def jevent_notify(self, type, data):
        ''' Notify the listeners that the event occurred'''
        get_logger().debug('Notifying listeners with {0} {1}'.format(J_EVENT_AS_STRING[type], str(data)))
        for wimc in self.jevent_listeners:
            wimc.put_nowait((type, data))
        return
    
    def clear(self):
        '''Clear the journal'''
        self.max_seq_num = 0
        self.last_journal_time = None
        dict.clear(self)
        self.jevent_notify(J_EVENT_CLEARED, None)
        return
    
    def deep_match(self, journal, ignore_delay=False, ignore_times=False, msg_tgt=None, ignore_rec_id=True, unordered=False):
        '''Compare two journals for equality'''
        result = True
        if msg_tgt is None:
            msg_tgt = MsgTargetLogger()
        if journal is None:
            msg_tgt.error('Journal to compare to was not specified (None)')
            return False
        msg_tgt.info('Matching ' + self.name + ' and ' + journal.name)
        # Check number of entries
        if len(journal) != len(self):
            msg_tgt.error('    Journals do not have the same number of entries: {0} != {1}'.format(len(journal), len(self)))
            result = False
        if unordered == False:
            for key in self:
                if key not in journal:
                    msg_tgt.error('     Journal sequence # mismatch {0} not found'.format(key))
                    result = False
                if key not in journal:
                    get_logger().debug('    No journal entry for sequence # {0} was found'.format(key))
                    continue
                if self[key].deep_match(journal[key], ignore_delay, ignore_times, msg_tgt, ignore_rec_id) == False:
                    get_logger().debug('     Journal entry mismatch')
                    result = False
        else:
            # unordered was true 
            my_keys_unused = self.keys()
            my_keys_used = []
            tgt_keys_unused = journal.keys()
            tgt_keys_used = []
            for key in self:
                for tgt_key in tgt_keys_unused: 
                    if self[key].deep_match(journal[tgt_key], ignore_delay, ignore_times, msg_target_ignore, ignore_rec_id) == True:
                        # Found a match 
                        my_keys_used.append(key)
                        my_keys_unused.remove(key)
                        tgt_keys_used.append(tgt_key)
                        tgt_keys_unused.remove(tgt_key)
                        break
            if len(my_keys_unused) == 0 and len(tgt_keys_unused) == 0:
                result = True
            else:
                result = False
                msg_tgt.error('    Journal entries {0} and target entries {1} do not have matches'.format(str(my_keys_unused), str(tgt_keys_unused)))
                msg_tgt.error('{0}'.format(str(self)))
                msg_tgt.error('{0}'.format(str(journal)))
                attempt_keys = [k for k in my_keys_unused if k in tgt_keys_unused]
                msg_tgt.error('Attempting comparison of entries {0}'.format(str(attempt_keys)))
                for attempt_key in attempt_keys:
                    self[attempt_key].deep_match(journal[attempt_key], ignore_delay, ignore_times, msg_tgt, ignore_rec_id)
        return result
            
    def __str__(self):
        outstr =  '<Journal: {0} \n'.format(self.name)
        keys = self.keys()
        keys.sort()
        for key in keys:
            outstr += '  {0:5d} {1}'.format(key, str(self[key]))
        outstr += '>\n'
        return outstr

    def save(self, filename):
        ''' Save the file in the format of the file extension'''
        if filename is not None:
            get_logger().debug('Saving file {0}'.format(filename))
            ext = os.path.splitext(filename)[1]
            ext = ext[1:]  #drop period
            save_method = getattr(self, 'save_file_{0}'.format(ext))
            save_method(filename)
            self.jevent_notify(J_EVENT_SAVED, filename)
        else:
            raise ValueError
        return
        
    def save_file_json(self, file_name):
        ''' Save the Journal to a JSON file'''
        json_list = []
        json_dict = {}
        json_list.append(json_dict)
        keys = self.keys()
        keys.sort()
        for sequenceid in keys:
            json_dict[sequenceid] = self[sequenceid].write_to_json()
        with open(file_name, 'wb') as jsonfile:
            json.dump(json_list, jsonfile, sort_keys=True, indent=2)
        return
    
    def load(self, file):
        ''' load the file based on the open file's extension '''
        if file != None:
            with open(file, 'rb') as open_file:
                get_logger().debug('loading file {0}'.format(file))
                ext = os.path.splitext(file)[1]
                ext = ext[1:]  #drop period
                load_method = getattr(self, 'load_file_{0}'.format(ext))
                load_method(open_file)
                self.jevent_notify(J_EVENT_LOADED, file)
        return
    
    def load_file_json(self, file):
        ''' Load Journal from a JSON file'''
        get_logger().debug('loading a JSON file')
        json_list = json.load(file)
        json_dict = json_list[0]
        for sequenceid in json_dict:
            json_type = json_dict[sequenceid][JSON_KEY_TYPE]
            if json_type == JE_TYPE_EVENT:
                self[int(sequenceid)] = JournalEntryEvent(delay=float(json_dict[sequenceid][JSON_KEY_DELAY]), json_dict=json_dict[sequenceid][JSON_KEY_DATA])
            elif json_type == JE_TYPE_ALERT:
                self[int(sequenceid)] = JournalEntryAlert(delay=float(json_dict[sequenceid][JSON_KEY_DELAY]), json_dict=json_dict[sequenceid][JSON_KEY_DATA])
            elif json_type == JE_TYPE_CONTROL_MSG:
                self[int(sequenceid)] = JournalEntryControlMsg(delay=float(json_dict[sequenceid][JSON_KEY_DELAY]), json_dict=json_dict[sequenceid][JSON_KEY_DATA])
            else:
                get_logger().warning('Unrecognized Journal Entry type in json data: {0}'.format(json_type))
            self.max_seq_num = max(self.max_seq_num, int(sequenceid))
        return
    
    def insert_in_db(self, progress_cb=None, truncate=False, use_rec_ids=True, no_delay=False, post=False):
        ''' insert the journal's journal entries into the appropriate tables'''
        # TODO: Add support for use_rec_ids!
        # TODO: Remove truncate ... add dbi.truncate_all() and use that instead (or something with parms?)
        get_logger().debug('Inserting journal into tables')
        keys = self.keys()
        keys.sort()
        # Get a connection
        dbi = get_service(SERVICE_DB_INTERFACE)
        cnxn = dbi.get_connection()
        cursor = cnxn.cursor()
        if truncate:
            # ORDER MATTERS
            dbi.truncate(cursor, db_interface.TABLE_CHECKPOINT)
            cnxn.commit()
            dbi.truncate(cursor, db_interface.TABLE_ALERT2ALERT)
            cnxn.commit()
            dbi.truncate(cursor, db_interface.TABLE_ALERT2EVENT)
            cnxn.commit()
            dbi.delete(cursor, db_interface.TABLE_EVENT_LOG)
            cnxn.commit()
            # Must close all alerts before they can be removed
            #   don't have to worry about relationships because they are all gone
            dbi.update(cursor, ['state'], db_interface.TABLE_ALERT_LOG, parms=(ALERT_STATE_CLOSED,))
            cnxn.commit()
            dbi.delete(cursor, db_interface.TABLE_ALERT_LOG)
            cnxn.commit()
            
        assoc_lists = []
        for key in keys:
            if no_delay == False:
                # delay the amount specified
                get_logger().debug('   delaying {0}'.format(str(self[key].delay)))
                sleep(self[key].delay)
            if self[key].type == JE_TYPE_EVENT:
                # get the journal entry event and insert it into the event log
                get_logger().debug('   inserting event {0}'.format(str(key)))
                keys, values = self[key].write_to_db_tuple(use_rec_ids=use_rec_ids)
                self.jevent_notify(J_EVENT_INJECTED, key)
                dbi.insert(cursor, keys, db_interface.TABLE_EVENT_LOG, values)
                if post: 
                    cnxn.commit()
                    get_service(SERVICE_NOTIFIER).post()
                if progress_cb is not None:
                    progress_cb()
            elif self[key].type == JE_TYPE_ALERT:
                # get the journal entry event and insert it into the alert log
                get_logger().debug('   inserting alert {0}'.format(str(key)))
                keys, values = self[key].write_to_db_tuple(use_rec_ids=use_rec_ids)
                self.jevent_notify(J_EVENT_INJECTED, key)
                dbi.insert(cursor, keys, db_interface.TABLE_ALERT_LOG, values)
                assoc_lists.append((self[key].data_dict[ALERT_ATTR_REC_ID],
                                    self[key].data_dict[ALERT_ATTR_ASSOC]))
                if progress_cb is not None:
                    progress_cb()
            else:
                get_logger().debug('   insert ignored: {0} - {1}'.format(str(key), str(self[key].type)))

        for alert_recid, assoc_list in assoc_lists:                
            # insert associations
            assoc_cursor = cnxn.cursor()
            for a_item in assoc_list:
                a_item = _ustr2str(a_item)
                a_type, t_type, t_rec_id = a_item.split(':')   
                         
                if t_type == 'E':
                    t_event_recid = long(t_rec_id)
                    dbi.insert(assoc_cursor, ALERT2EVENT_COLS, db_interface.TABLE_ALERT2EVENT, [alert_recid, a_type, t_event_recid])

                elif t_type == 'A':
                    t_alert_recid = long(t_rec_id)
                    dbi.insert(assoc_cursor, ALERT2ALERT_COLS, db_interface.TABLE_ALERT2ALERT, [alert_recid, a_type, t_alert_recid])

                else:
                    get_logger().error('Unexpected association target type {0}'.format(t_type))
        get_logger().debug('Insert done')
        cnxn.commit()
        cnxn.close()
        self.jevent_notify(J_EVENT_INJECTION_COMPLETE, 'table')
        return            
    
    def select_from_db(self, type, event_fields = EVENT_COLS, alert_fields=ALERT_COLS_SELECT, include_alert_assoc=True):
        ''' insert the journal's journal entries into the appropriate tables'''
        get_logger().debug('Loading (selecting) journal from tables')
        dbi = get_service(SERVICE_DB_INTERFACE)
        event_cnxn = dbi.get_connection()
        cursor = event_cnxn.cursor()
        if type == 'event' or type == 'all':
            # Read events
            dbi.select(cursor, event_fields, db_interface.TABLE_EVENT_LOG,order=EVENT_ATTR_REC_ID)
            while 1:
                row = cursor.fetchone()
                if row is None:
                    break
                self.max_seq_num += 1
                self[self.max_seq_num] = JournalEntryEvent(db_dict=dict(zip(event_fields,row)))
        if type == 'alert' or type == 'all':
            # Read alerts
            dbi.select(cursor, alert_fields, db_interface.TABLE_ALERT_LOG, order=ALERT_ATTR_REC_ID)
            while 1:
                row = cursor.fetchone()
                if row is None:
                    break
                self.max_seq_num += 1
                tmp_dict = dict(zip(alert_fields,row))
                if include_alert_assoc:
                    tmp_assoc = []
                    # Get alert to alert associations
                    assoc_cursor = event_cnxn.cursor()
                    dbi.select(assoc_cursor, ALERT2ALERT_COLS, db_interface.TABLE_ALERT2ALERT, where='$alert_recid = ?', where_fields=['alert_recid'], parms=[tmp_dict[ALERT_ATTR_REC_ID]])
                    while 1:
                        assoc_row = assoc_cursor.fetchone()
                        if assoc_row is None:
                            break
                        tmp_assoc.append('{0}:{1}:{2}'.format(assoc_row[1],'A',assoc_row[2]))
                    # Get alert to event associations
                    assoc_cursor = event_cnxn.cursor()
                    dbi.select(assoc_cursor, ALERT2EVENT_COLS, db_interface.TABLE_ALERT2EVENT, where='$alert_recid = ?', where_fields=['alert_recid'], parms=[tmp_dict[ALERT_ATTR_REC_ID]])
                    while 1:
                        assoc_row = assoc_cursor.fetchone()
                        if assoc_row is None:
                            break
                        tmp_assoc.append('{0}:{1}:{2}'.format(assoc_row[1],'E',assoc_row[2]))
                    tmp_dict[ALERT_ATTR_ASSOC] = tmp_assoc
                self[self.max_seq_num] = JournalEntryAlert(db_dict=tmp_dict)
        event_cnxn.close()
        self.jevent_notify(J_EVENT_INJECTION_COMPLETE, 'table')
        return            
    
    def inject_queue(self, queue, progress_cb=None, fail_on_invalid=True, no_delay=False, max_key=None):
        ''' inject the journal's journal entries into the specified queue'''
        get_logger().debug('Injecting journal into queue')
        keys = self.keys()
        keys.sort()
        for key in keys:
            if max_key is not None:
                if key > max_key:
                    get_logger().info('Discontinuing injection with key {0}'.format(key))
                    break
            if no_delay == False:
                # delay the amount specified
                get_logger().debug('   delaying {0}'.format(str(self[key].delay)))
                sleep(self[key].delay)
            # get the journal entry item and put it on the queue
            get_logger().debug('   adding to queue {0}'.format(str(key)))
            item = self[key].create_item()
            if item.is_valid() == False:
                get_logger().debug('   sequence # {0} is invalid!'.format(key))
                if fail_on_invalid == True:
                    raise ValueError
            self.jevent_notify(J_EVENT_INJECTED, key)
            queue.put(item)
            if progress_cb is not None:
                progress_cb()
        get_logger().debug('Injection done')
        self.jevent_notify(J_EVENT_INJECTION_COMPLETE, 'queue')
        return

    def notify(self, item):
        '''Process a notification from a ListenableQueue'''
        get_logger().debug('Notify called with {0}'.format(str(item)))
        item.process(self, None)
        # Does not process (analyze) the event
        return False
        
    def calc_delay(self):
        '''Calculate the time between this and the last journaled event'''
        if self.last_journal_time is None:
            self.last_journal_time = datetime.now()
            delay = 0.0
        else:
            right_now = datetime.now()
            #TODO: better granularity ... handle days?
            delay_tmp = (right_now - self.last_journal_time)
            delay = delay_tmp.seconds + (delay_tmp.microseconds/1000000.0)
            self.last_journal_time = right_now
        return delay
    
    def process_event(self, event, context):
        ''' Add event to Journal'''
        self.journal_event(event, self.calc_delay())
        return
    
    def journal_event(self, event, in_delay=0.0):
        '''Add event to the journal'''
        self.max_seq_num += 1
        self[self.max_seq_num] = JournalEntryEvent(delay=in_delay, event=event)
        self.jevent_notify(J_EVENT_JE_ADD, self.max_seq_num)
        return
  
    def process_alert(self, alert, context):
        ''' Add alert to Journal'''
        self.journal_alert(alert, self.calc_delay())
        return
    
    def journal_alert(self, alert, in_delay=0.0):
        '''Add alert to the journal'''
        self.max_seq_num += 1
        self[self.max_seq_num] = JournalEntryAlert(delay=in_delay, alert=alert)
        self.jevent_notify(J_EVENT_JE_ADD, self.max_seq_num)
        return
    
    def process_control_msg(self, control_msg, context):
        ''' Add control_msg to Journal'''
        self.journal_control_msg(control_msg, self.calc_delay())
        return

    def journal_control_msg(self, control_msg, in_delay=0.0):
        '''Add control message to the journal'''
        self.max_seq_num += 1
        self[self.max_seq_num] = JournalEntryControlMsg(delay=in_delay, control_msg=control_msg)
        self.jevent_notify(J_EVENT_JE_ADD, self.max_seq_num)
        return
    
    def add_entry(self, seq, type, delay, in_dict):
        ''' Add a entry '''
        if seq in self:
            get_logger().error('Journal already contains an entry for sequence # {0}'.format(seq))
            raise ValueError
        self.max_seq_num = max(self.max_seq_num, seq)
        if type == JE_TYPE_EVENT:
            self[seq] = JournalEntryEvent(delay=delay, in_dict=in_dict)
        elif type == JE_TYPE_ALERT:
            self[seq] = JournalEntryAlert(delay=delay, in_dict=in_dict)
        elif type == JE_TYPE_CONTROL_MSG:
            self[seq] = JournalEntryControlMsg(delay=delay, in_dict=in_dict)
        else:
            get_logger().error('Journal Entry type {0} not recognized'.format(type))
            raise ValueError
        self.jevent_notify(J_EVENT_JE_ADD, seq)
        return
    
    def del_entry(self, seq):
        ''' Delete an entry '''
        if seq not in self:
            get_logger().error('Journal does not contain seq num {0}.  Nothing deleted'.format(seq))
            return
        del self[seq]
        self.jevent_notify(J_EVENT_JE_DEL, seq)
        return
    
    def wait_for_entries(self, num_entries, seconds=20, msg_mode='log'):
        count = 0  
        while len(self) < num_entries:
            if msg_mode != 'quiet':
                outmsg = 'Waiting: only {2} out of {1} for journal {0} so far'.format(self.get_name(), num_entries, str(len(self)))
                if msg_mode == 'stdout':
                    print outmsg
                else:
                    get_logger().info(outmsg)
            sleep(0) # Yield
            sleep(1.0)
            if count >= seconds:
                if msg_mode != 'quiet':
                    print 'Journal {0} only got {1} of {2} entries'.format(self.get_name(), str(len(self)), num_entries)
                    print self
                return False
            count += 1 
        return True


class JournalEntry():
    '''
    The JournalEntry class is used to internally represent and entry in the Journal.  It can contain the
    information for an Event, Alert or Control Message.   
    
    It contains the type of the entry, the delay if the journal is to be injected, and the data for the 
    Incident it is for in a dictionary
    '''
    
    __metaclass__ = ABCMeta
        
    def __init__(self, delay, je_type, in_dict=None):
        '''
        Constructor: Create the journal entry from the passed in information (if provided)
        
        '''
        self.delay = delay
        self.type = je_type
        if in_dict is not None:
            # Assume if None it was set by the child class
            self.data_dict = in_dict
        else:
            self.data_dict = {}
        return
    
    @abstractmethod
    def create_item(self):
        ''' Create an instance of the thing the Journal Entry is for '''
        pass
    
    @abstractmethod
    def read_from_json(self, json_data):
        ''' Read journal entry data from json '''
        pass
        
    @abstractmethod
    def read_from_db_tuple(self, db_dict):
        ''' Read journal entry data from db tuple returned from a select '''
        pass
   
    @abstractmethod
    def _write_to_dict_of_str(self):
        ''' Write to Journal Entry as a dictionary of strings '''
        pass
    
    def write_to_json(self):
        ''' Write out Journal Entry in json format '''
        out_dict = {}
        out_dict[JSON_KEY_TYPE] = self.type
        out_dict[JSON_KEY_DELAY] = str(self.delay)
        out_dict[JSON_KEY_DATA] = self._write_to_dict_of_str()
        return out_dict
    
    @abstractmethod
    def write_to_db_tuple(self, use_rec_ids=True):
        ''' Write out Journal Entry in tuple ready for use with the DB
            Returns ((fields),(values))
        '''
        pass
    
    def deep_match(self, je, ignore_delay, ignore_times, msg_tgt, ignore_rec_id):
        ''' Check if the journal entry is equal to another one'''
        if self.type != je.type:
            msg_tgt.error('     Journal entry type mismatch \'{0}\' != \'{1}\''.format(self.type, je.type))
            return False
        if ignore_delay == False:
            if self.delay != je.delay:
                msg_tgt.error('     Journal entry delay mismatch {0} != {1}'.format(self.delay, je.delay))
                return False
        result = True
        if len(self.data_dict) != len(je.data_dict):
            msg_tgt.error('      Journal entry data len mismatch {0} != {1}'.format(len(self.data_dict), len(je.data_dict)))
            result = False
        for key in self.data_dict:
            # TODO: What about the other times?
            if key not in je.data_dict:
                msg_tgt.error('      JE1 contained \'{0}\' with value \'{1}\' but JE2 did not'.format(key, str(self.data_dict[key])))
                result = False
            else:
                # If it is a time, do something special
                if key == ALERT_ATTR_CREATION_TIME or key == EVENT_ATTR_TIME_LOGGED or key == EVENT_ATTR_TIME_OCCURRED:
                    if ignore_times == True:
                        continue
                    time_delta = abs(self.data_dict[key] - je.data_dict[key])
                    # TODO: Allow time delta check amount to be specified
                    if time_delta.seconds <= 0:
                        continue
                    msg_tgt.error('      JE time value mismatch for key \'{0}\': \'{1}\' != \'{2}\''.format(key, self.data_dict[key], je.data_dict[key]))
                    result = False
                else:
                    if ignore_rec_id == True and (key == ALERT_ATTR_REC_ID):
                        continue
                    if self.data_dict[key] != je.data_dict[key]:
                        msg_tgt.error('      JE data value mismatch for key \'{0}\': \'{1}\' != \'{2}\''.format(key, self.data_dict[key], je.data_dict[key]))
                        result = False
        for key in je.data_dict:
            if key not in self.data_dict:
                msg_tgt.error('      JE2 contained \'{0}\' with value \'{1}\' but JE1 did not'.format(key, str(je.data_dict[key])))
        if result == False:
            outstr = '       JE 1 = {{{0}}}'.format(self._get_data_as_str())
            msg_tgt.info(outstr)
            outstr = '       JE 2 = {{{0}}}'.format(je._get_data_as_str())
            msg_tgt.info(outstr)
        return result
    
    def __str__(self):
        float_str = '{0:4.3f}'.format(self.delay)
        return '{0:12s} {1:8s} {2}\n'.format(self.type, float_str, self._get_data_as_str())
    
    def _get_data_as_str(self):
        ''' sort the data dictionary and put into a string '''
        outstr = ''
        keys = self.data_dict.keys()
        keys.sort()
        if 'rec_id' in keys:
            keys.remove('rec_id')
            keys.insert(0,'rec_id')
        for key in keys:
            if key == 'rec_id':
                outstr += '{0}: {1:5d} '.format(key, self.data_dict[key])
            elif key == 'associations':
                sorted_assoc = sorted(self.data_dict[key])
                outstr += '{0}: {1} '.format(key, str(sorted_assoc))
            else:
                outstr += '{0}: {1} '.format(key, str(self.data_dict[key]))
        return outstr
     
    
class JournalEntryEvent(JournalEntry):
    ''' Journal entry for events '''
    
    def __init__(self, delay=0.0, json_dict=None, event=None, in_dict=None, db_dict=None):
        '''initialize from whatever data is available '''
        self.raw_data_values = None
        JournalEntry.__init__(self, delay, JE_TYPE_EVENT)
        count = 0   # Validate only one input 
        if json_dict is not None:
            self.read_from_json(json_dict)
            count += 1
        if event is not None:
            #p rint 'NOT NONE EVENT entry'
            self.data_dict = event.write_to_dictionary(as_objects=False)
            #p rint 'created journal entry ', str(self.data_dict)
            count += 1
        if in_dict is not None:
            self.data_dict = in_dict
            count += 1
        if db_dict is not None:
            self.read_from_db_tuple(db_dict)
            count += 1
        if count > 1:
            get_logger().error('JournalEntry for Event can only be created from one thing')
            raise ValueError
        return
    
    def create_item(self):
        ''' create the event from the Journal Entry and return it'''
        new_event = Event.fromDict(self.data_dict)
        if self.raw_data_values is not None:
            # Format is name,type,value; name,type,value
            values = self.raw_data_values.split(';')
            for value in values:
                name, type, init = value.split(',')
                if type == 'Location':
                    loc_type, loc_init = init.split(':')
                    use_init = Location(loc_type, loc_init)
                else:
                    use_init = value
                new_event.raw_data[name] = use_init
        return new_event
    
    def read_from_json(self, json_dict):
        '''Set the attributes of Event from information from json data
        
        the data is a dict with type, delay and data in it with data containing the incident's info
        '''
        try:
            for key in json_dict:
                value = _ustr2str(json_dict[key])
                if key == EVENT_ATTR_REC_ID:
                    self.data_dict[EVENT_ATTR_REC_ID] = long(value)
                elif key == EVENT_ATTR_TIME_OCCURRED:
                    if value.find('.') == -1:
                        self.data_dict[EVENT_ATTR_TIME_OCCURRED] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    else:
                        self.data_dict[EVENT_ATTR_TIME_OCCURRED] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
                elif key == EVENT_ATTR_TIME_LOGGED:
                    if value.find('.') == -1:
                        self.data_dict[EVENT_ATTR_TIME_LOGGED] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    else:
                        self.data_dict[EVENT_ATTR_TIME_LOGGED] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
                elif key == EVENT_ATTR_EVENT_ID:
                    self.data_dict[EVENT_ATTR_EVENT_ID] = value
                elif key == EVENT_ATTR_SRC_COMP:
                    self.data_dict[EVENT_ATTR_SRC_COMP] = value
                elif key == EVENT_ATTR_SRC_LOC:
                    self.data_dict[EVENT_ATTR_SRC_LOC] = value
                elif key == EVENT_ATTR_SRC_LOC_TYPE:
                    self.data_dict[EVENT_ATTR_SRC_LOC_TYPE] = value       
                elif key == EVENT_ATTR_RPT_COMP:
                    self.data_dict[EVENT_ATTR_RPT_COMP] = value
                elif key == EVENT_ATTR_RPT_LOC:
                    self.data_dict[EVENT_ATTR_RPT_LOC] = value
                elif key == EVENT_ATTR_RPT_LOC_TYPE:
                    self.data_dict[EVENT_ATTR_RPT_LOC_TYPE] = value
                elif key == EVENT_ATTR_EVENT_CNT:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_EVENT_CNT] = int(value)
                elif key == EVENT_ATTR_ELAPSED_TIME:
                    if value is not None: 
                        self.data_dict[EVENT_ATTR_ELAPSED_TIME] = int(value)
                elif key == EVENT_ATTR_RAW_DATA_FMT:
                    self.data_dict[EVENT_ATTR_RAW_DATA_FMT] = long(value,16)
                # May get as a raw data entry with a dictionary, hex value or as ext.name entries
                ## dictionary or hex value 
                elif key == EVENT_ATTR_RAW_DATA:
                    if value[0:2] == '0x':
                        self.data_dict[EVENT_ATTR_RAW_DATA] = binascii.unhexlify(value[2:])
                    else:
                        self.data_dict[EVENT_ATTR_RAW_DATA] = value
                elif key == 'raw_data_values':
                    self.raw_data_values = value.strip()
                # See if raw data entry 
                elif key.split('.')[0] == 'ext': 
                    if EVENT_ATTR_RAW_DATA not in self.data_dict:
                        self.data_dict[EVENT_ATTR_RAW_DATA] = dict()
                    if EVENT_ATTR_RAW_DATA_FMT not in self.data_dict:
                        self.data_dict[EVENT_ATTR_RAW_DATA_FMT] = long(0)
                    try: 
                        rd_key = key.split('.')[1]
                        self.data_dict[EVENT_ATTR_RAW_DATA][rd_key] = value
                    except:
                        get_logger().warning('ext.* entry \'{0}\' ... entry ignored'.format(key))
                else:
                    get_logger().warning('Read from event json encountered unexpected element {0}'.format(key))
        except:
            get_logger().fatal('JournalEntry read from event json failed with an exception')
            raise
        return
    
    def read_from_db_tuple(self, db_dict):
        '''Set the attributes of Event from information from db data
        
        the data is a dictionary containing the incident's info from the db
        '''
        try:
            for key in db_dict:
                value = db_dict[key]
                # Required
                if key == EVENT_ATTR_REC_ID:
                    self.data_dict[EVENT_ATTR_REC_ID] = value
                elif key == EVENT_ATTR_TIME_OCCURRED:
                    self.data_dict[EVENT_ATTR_TIME_OCCURRED] = value
                elif key == EVENT_ATTR_TIME_LOGGED:
                    self.data_dict[EVENT_ATTR_TIME_LOGGED] = value
                elif key == EVENT_ATTR_EVENT_ID:
                    self.data_dict[EVENT_ATTR_EVENT_ID] = value
                elif key == EVENT_ATTR_SRC_COMP:
                    self.data_dict[EVENT_ATTR_SRC_COMP] = value.strip()
                elif key == EVENT_ATTR_SRC_LOC:
                    self.data_dict[EVENT_ATTR_SRC_LOC] = value.strip()
                elif key == EVENT_ATTR_SRC_LOC_TYPE:
                    self.data_dict[EVENT_ATTR_SRC_LOC_TYPE] = value   
                # Optional    
                elif key == EVENT_ATTR_RPT_COMP:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_RPT_COMP] = value.strip()
                elif key == EVENT_ATTR_RPT_LOC:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_RPT_LOC] = value.strip()
                elif key == EVENT_ATTR_RPT_LOC_TYPE:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_RPT_LOC_TYPE] = value
                elif key == EVENT_ATTR_EVENT_CNT:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_EVENT_CNT] = value
                elif key == EVENT_ATTR_ELAPSED_TIME:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_ELAPSED_TIME] = value
                elif key == EVENT_ATTR_RAW_DATA_FMT:
                    if value is not None:
                        self.data_dict[EVENT_ATTR_RAW_DATA_FMT] = value
                elif key == EVENT_ATTR_RAW_DATA:
                    if value is not None:
#                        if value[0:2] == '0x':
#                            self.data_dict[EVENT_ATTR_RAW_DATA] = binascii.unhexlify(value[2:])
#                        else:
                        self.data_dict[EVENT_ATTR_RAW_DATA] = value
                else:
                    get_logger().warning('Read from event db dict encountered unexpected element {0}'.format(key))
        except:
            get_logger().fatal('JournalEntry read from event db dict failed with an exception')
            raise
        return
    
    def _write_to_dict_of_str(self):
        ''' Output Event Journal Entry as a dictionary of strings''' 
        out_dict = {}
        for key in self.data_dict:
            value = self.data_dict[key]
            if key == EVENT_ATTR_REC_ID:
                out_dict[EVENT_ATTR_REC_ID] = value
            elif key == EVENT_ATTR_TIME_OCCURRED:
                out_dict[EVENT_ATTR_TIME_OCCURRED] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')
            elif key == EVENT_ATTR_TIME_LOGGED:
                out_dict[EVENT_ATTR_TIME_LOGGED] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')
            elif key == EVENT_ATTR_EVENT_ID:
                out_dict[EVENT_ATTR_EVENT_ID] = value
            elif key == EVENT_ATTR_SRC_COMP:
                out_dict[EVENT_ATTR_SRC_COMP] = value
            elif key == EVENT_ATTR_SRC_LOC:
                out_dict[EVENT_ATTR_SRC_LOC] = value
            elif key == EVENT_ATTR_SRC_LOC_TYPE:
                out_dict[EVENT_ATTR_SRC_LOC_TYPE] = value       
            elif key == EVENT_ATTR_RPT_COMP:
                out_dict[EVENT_ATTR_RPT_COMP] = value
            elif key == EVENT_ATTR_RPT_LOC:
                out_dict[EVENT_ATTR_RPT_LOC] = value
            elif key == EVENT_ATTR_RPT_LOC_TYPE:
                out_dict[EVENT_ATTR_RPT_LOC_TYPE] = value
            elif key == EVENT_ATTR_EVENT_CNT:
                out_dict[EVENT_ATTR_EVENT_CNT] = str(value)
            elif key == EVENT_ATTR_ELAPSED_TIME:
                out_dict[EVENT_ATTR_ELAPSED_TIME] = value
            elif key == EVENT_ATTR_RAW_DATA_FMT:
                out_dict[EVENT_ATTR_RAW_DATA_FMT] = hex(value)
            elif key == EVENT_ATTR_RAW_DATA:
                if value is not None: 
                    out_dict[EVENT_ATTR_RAW_DATA] = str(value) #.write_to_dictionary())                 
                # out_dict[EVENT_ATTR_RAW_DATA] = binascii.hexlify(value)                    
            else:
                get_logger().warning('Event Journal Entry contains unrecognized key: {0}'.format(key))
        return out_dict
    
    def write_to_db_tuple(self, use_rec_ids=True):
        ''' Write out Journal Entry in tuple ready for use with the DB
            Returns ((fields),(values))
        '''
        tmp_dict = dict(self.data_dict)
        raw_data = tmp_dict.get(EVENT_ATTR_RAW_DATA, None)
        if raw_data is not None:
            if isinstance(raw_data, dict) == True:
                # Get original raw data out of dictionary
                raw_data = raw_data[EVENT_ATTR_RAW_DATA]
            tmp_dict[EVENT_ATTR_RAW_DATA] = raw_data
        if not use_rec_ids:
            del tmp_dict[EVENT_ATTR_REC_ID]
        return (tmp_dict.keys(),map(_ustr2str,tmp_dict.values()))

class JournalEntryAlert(JournalEntry):
    ''' Journal entry for alerts '''
    
    def __init__(self, delay=0.0, json_dict=None, alert=None, in_dict=None, db_dict=None):
        '''initialize from whatever data is available '''
        JournalEntry.__init__(self, delay, JE_TYPE_ALERT)
        count = 0   # Validate only one input 
        if json_dict is not None:
            self.read_from_json(json_dict)
            count += 1
        if alert is not None:
            self.data_dict = alert.write_to_dictionary()
            count += 1
        if in_dict is not None:
            self.data_dict = in_dict
            count += 1
        if db_dict is not None:
            self.read_from_db_tuple(db_dict)
            count += 1
        if count > 1:
            get_logger().error('JournalEntry for Alert can only be created from one thing')
            raise ValueError
        return
    
    def create_item(self):
        ''' create the alert from the Journal Entry and return it'''
        alert_mgr = get_service(SERVICE_ALERT_MGR)
        t_data_dict = dict(self.data_dict)
        del t_data_dict[ALERT_ATTR_STATE]
        alert = alert_mgr.allocate(self.data_dict[ALERT_ATTR_ALERT_ID], t_data_dict)
        if self.data_dict[ALERT_ATTR_STATE] == ALERT_STATE_OPEN or self.data_dict[ALERT_ATTR_STATE] == ALERT_STATE_CLOSED:
            alert_mgr.commit(alert)
        if self.data_dict[ALERT_ATTR_STATE] == ALERT_STATE_CLOSED:
            alert_mgr.close(alert.rec_id)
        return alert
    
    def read_from_json(self, json_dict):
        '''Set the attributes of Alert from information from json data
        
        the data is a dict with type, delay and data in it with data containing the incident's info
        '''
        try:
            for key in json_dict:
                value = _ustr2str(json_dict[key])
                if key == ALERT_ATTR_ALERT_ID:
                    self.data_dict[ALERT_ATTR_ALERT_ID] = value
                elif key == ALERT_ATTR_CREATION_TIME:
                    if value.find('.') == -1:
                        self.data_dict[ALERT_ATTR_CREATION_TIME] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    else:
                        self.data_dict[ALERT_ATTR_CREATION_TIME] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
                elif key == ALERT_ATTR_SEVERITY:
                    self.data_dict[ALERT_ATTR_SEVERITY] = value
                elif key == ALERT_ATTR_URGENCY:
                    self.data_dict[ALERT_ATTR_URGENCY] = value
                elif key == ALERT_ATTR_EVENT_LOC:
                    self.data_dict[ALERT_ATTR_EVENT_LOC] = value
                elif key == ALERT_ATTR_EVENT_LOC_TYPE:
                    self.data_dict[ALERT_ATTR_EVENT_LOC_TYPE] = value
                elif key == ALERT_ATTR_FRU_LOC:
                    self.data_dict[ALERT_ATTR_FRU_LOC] = value
                elif key == ALERT_ATTR_RECOMMENDATION:
                    self.data_dict[ALERT_ATTR_RECOMMENDATION] = value
                elif key == ALERT_ATTR_REASON:
                    self.data_dict[ALERT_ATTR_REASON] = value
                elif key == ALERT_ATTR_SRC_NAME:
                    self.data_dict[ALERT_ATTR_SRC_NAME] = value
                elif key == ALERT_ATTR_STATE:
                    index = 0
                    self.data_dict[ALERT_ATTR_STATE] = None
                    for state in ALERT_STATE_AS_STRING:
                        if state == value:
                            self.data_dict[ALERT_ATTR_STATE] = index
                            break
                        index += 1
                    if self.data_dict[ALERT_ATTR_STATE] is None:
                        get_logger().fatal('Alert state name {0} is invalid'.format(value))
                        self.data_dict[ALERT_ATTR_STATE] = ALERT_STATE_OPEN
                        # TODO: Need to change back to error
                        #raise ValueError()
                elif key == ALERT_ATTR_RAW_DATA:
                    self.data_dict[ALERT_ATTR_RAW_DATA] = value
                elif key == ALERT_ATTR_ASSOC:
                    self.data_dict[ALERT_ATTR_ASSOC] = value
                elif key == ALERT_ATTR_REC_ID:
                    self.data_dict[ALERT_ATTR_REC_ID] = value
                else:
                    get_logger().warning('Read from alert json encountered unexpected element {0}'.format(key))
        except:
            get_logger().fatal('JournalEntry read from alert json failed with an exception')
            raise
        return
   
    def read_from_db_tuple(self, db_dict):
        '''Set the attributes of Event from information from db data
        
        the data is a dictionary containing the incident's info from the db
        '''
        try:
            for key in db_dict:
                value = db_dict[key]
                if key == ALERT_ATTR_ALERT_ID:
                    self.data_dict[ALERT_ATTR_ALERT_ID] = value
                elif key == ALERT_ATTR_CREATION_TIME:
                    self.data_dict[ALERT_ATTR_CREATION_TIME] = value
                elif key == ALERT_ATTR_SEVERITY:
                    self.data_dict[ALERT_ATTR_SEVERITY] = value
                elif key == ALERT_ATTR_URGENCY:
                    self.data_dict[ALERT_ATTR_URGENCY] = value
                elif key == ALERT_ATTR_EVENT_LOC:
                    self.data_dict[ALERT_ATTR_EVENT_LOC] = value.strip()
                elif key == ALERT_ATTR_EVENT_LOC_TYPE:
                    self.data_dict[ALERT_ATTR_EVENT_LOC_TYPE] = value
                elif key == ALERT_ATTR_FRU_LOC:
                    if value is not None:
                        self.data_dict[ALERT_ATTR_FRU_LOC] = value
                elif key == ALERT_ATTR_RECOMMENDATION:
                    self.data_dict[ALERT_ATTR_RECOMMENDATION] = value
                elif key == ALERT_ATTR_REASON:
                    self.data_dict[ALERT_ATTR_REASON] = value
                elif key == ALERT_ATTR_SRC_NAME:
                    self.data_dict[ALERT_ATTR_SRC_NAME] = value.strip()
                elif key == ALERT_ATTR_STATE:
                    self.data_dict[ALERT_ATTR_STATE] = value
                elif key == ALERT_ATTR_RAW_DATA:
                    if value is not None:
                        self.data_dict[ALERT_ATTR_RAW_DATA] = value
                elif key == ALERT_ATTR_ASSOC:
                    self.data_dict[ALERT_ATTR_ASSOC] = value
                elif key == ALERT_ATTR_REC_ID:
                    self.data_dict[ALERT_ATTR_REC_ID] = value
                else:
                    get_logger().warning('Read from alert db dict encountered unexpected element {0}'.format(key))
        except:
            get_logger().fatal('JournalEntry read from alert db dict failed with an exception')
            raise
        return
 
    def _write_to_dict_of_str(self):
        ''' Output Event Journal Entry as a dictionary of strings''' 
        out_dict = {}
        for key in self.data_dict:
            value = self.data_dict[key]
            if key == ALERT_ATTR_REC_ID:
                out_dict[ALERT_ATTR_REC_ID] = value
            elif key == ALERT_ATTR_ALERT_ID:
                out_dict[ALERT_ATTR_ALERT_ID] = value
            elif key == ALERT_ATTR_CREATION_TIME:
                out_dict[ALERT_ATTR_CREATION_TIME] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')
            elif key == ALERT_ATTR_SEVERITY:
                out_dict[ALERT_ATTR_SEVERITY] = value
            elif key == ALERT_ATTR_URGENCY:
                out_dict[ALERT_ATTR_URGENCY] = value
            elif key == ALERT_ATTR_EVENT_LOC:
                out_dict[ALERT_ATTR_EVENT_LOC] = value
            elif key == ALERT_ATTR_EVENT_LOC_TYPE:
                out_dict[ALERT_ATTR_EVENT_LOC_TYPE] = value
            elif key == ALERT_ATTR_FRU_LOC:
                out_dict[ALERT_ATTR_FRU_LOC] = value
            elif key == ALERT_ATTR_RECOMMENDATION:
                out_dict[ALERT_ATTR_RECOMMENDATION] = value
            elif key == ALERT_ATTR_REASON:
                out_dict[ALERT_ATTR_REASON] = value
            elif key == ALERT_ATTR_SRC_NAME:
                out_dict[ALERT_ATTR_SRC_NAME] = value
            elif key == ALERT_ATTR_STATE:
                out_dict[ALERT_ATTR_STATE] = ALERT_STATE_AS_STRING[value]
            elif key == ALERT_ATTR_RAW_DATA:
                out_dict[ALERT_ATTR_RAW_DATA] = value
            elif key == ALERT_ATTR_ASSOC:
                out_dict[ALERT_ATTR_ASSOC] = value
            else:
                get_logger().warning('Alert Journal Entry contains unrecognized key: {0}'.format(key))
        return out_dict
    
    def write_to_db_tuple(self, use_rec_ids=True):
        ''' Write out Journal Entry in tuple ready for use with the DB
            Returns ((fields),(values))
        '''
        tmp_dict = dict(self.data_dict)
        if ALERT_ATTR_ASSOC in tmp_dict:
            del tmp_dict[ALERT_ATTR_ASSOC]
        if not use_rec_ids:
            del tmp_dict[ALERT_ATTR_REC_ID]
        return (tmp_dict.keys(),map(_ustr2str,tmp_dict.values()))
    
    
class JournalEntryControlMsg(JournalEntry):
    ''' Journal entry for control messages '''
    
    def __init__(self, delay=0.0, json_dict=None, control_msg=None, in_dict=None, db_dict=None):
        '''initialize from whatever data is available '''
        JournalEntry.__init__(self, delay, JE_TYPE_CONTROL_MSG)
        count = 0   # Validate only one input 
        if json_dict is not None:
            self.read_from_json(json_dict)
            count += 1
        if control_msg is not None:
            self.data_dict = control_msg.write_to_dictionary()
            count += 1
        if in_dict is not None:
            self.data_dict = in_dict
            count += 1
        if db_dict is not None:
            get_logger().warning('Journal Entry for Control Msg does not support DB')
        if count > 1:
            get_logger().error('JournalEntry for Control Msg can only be created from one thing')
            raise ValueError
        return
    
    def create_item(self):
        ''' create the alert from the Journal Entry and return it'''
        return ControlMsg(in_dict=self.data_dict)
    
    def read_from_json(self, json_dict):
        '''Set the attributes of Alert from information from json data
        
        the data is a dict with type, delay and data in it with data containing the incident's info
        '''
        try:
            for key in json_dict:
                value = json_dict[key]
                if key == CONTROL_MSG_ATTR_MSG_TYPE:
                    # Convert from string to enumerated value
                    str_value = None
                    index = 0
                    for enum_str in CONTROL_MSG_TYPE_AS_STRING:
                        if value == enum_str:
                            str_value = int(index)
                            break
                        index += 1
                    if str_value is None:
                        get_logger('Journal Entry Control Msg was unable to find enumerated entry for {0}'.format(value))  
                    else: 
                        self.data_dict[CONTROL_MSG_ATTR_MSG_TYPE] = str_value
                elif key == CONTROL_MSG_ATTR_CREATION_TIME:
                    self.data_dict[CONTROL_MSG_ATTR_CREATION_TIME] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
                elif key == CONTROL_MSG_ATTR_DATA_DICT:
                    self.data_dict[CONTROL_MSG_ATTR_DATA_DICT] = value 
                else:
                    get_logger().warning('Read from control msg json encountered unexpected element {0}'.format(key))
        except:
            get_logger().fatal('JournalEntry read from alert json failed with an exception')
            raise
        return
   
    def read_from_db_tuple(self, db_dict):
        '''Set the attributes of Event from information from db data
        
        the data is a dictionrary containing the incident's info from the db
        '''
        get_logger().fatal('JournalEntry read from DB for Control Msg not supported')
        raise ValueError
        return
 
    def _write_to_dict_of_str(self):
        ''' Output Event Journal Entry as a dictionary of strings''' 
        out_dict = {}
        for key in self.data_dict:
            value = self.data_dict[key]
            if key == CONTROL_MSG_ATTR_MSG_TYPE:
                out_dict[CONTROL_MSG_ATTR_MSG_TYPE] = CONTROL_MSG_TYPE_AS_STRING[int(value)]
            elif key == CONTROL_MSG_ATTR_CREATION_TIME:
                out_dict[CONTROL_MSG_ATTR_CREATION_TIME] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')
            elif key == CONTROL_MSG_ATTR_DATA_DICT:
                out_dict[CONTROL_MSG_ATTR_DATA_DICT] = str(value)
            else:
                get_logger().warning('Alert Journal Entry contains unrecognized key: {0}'.format(key))
        return out_dict
    
    def write_to_db_tuple(self, use_rec_ids=True):
        ''' Write out Journal Entry in tuple ready for use with the DB
            Returns ((fields),(values))
        '''
        get_logger().fatal('JournalEntry read from DB for Control Msg not supported')
        raise ValueError
        return

        
class AlertListenerJournal(AlertListener):
    '''Alert listener to put alerts into Journal'''
    
    def __init__(self, name, config_dict, journal=None): 
        ''' Contructor
        
        journal is optional so that this can either be created and manually
        added or can be configured to be added.
        '''
        if journal is None:
            self.journal = Journal(name + '_journal')
        else:
            self.journal = journal
        AlertListener.__init__(self, name, config_dict)
        return
        
    def process_alert(self, alert):
        get_logger().debug(self.get_name() + ' is journaling {0}'.format(str(alert)))
        self.journal.journal_alert(alert)
        return
    
    def __str__(self):
        '''print the journal'''
        out_str = self.get_name() + ':\n'
        out_str += str(self.journal)
        return out_str

        
class QueueListenerJournal(QueueListener):
    '''The QueueListenerJournal class is logs everything that comes into the
       into the its journal 
    '''

    def __init__(self, name, in_queue, journal=None):
        ''' Initialize '''
        self.name = name
        #p rint 'vampire intialized'
        if journal is None:
            self.journal = Journal(name + '_journal')
        else:
            self.journal = journal
        self.queue = in_queue
        self.queue.register_listener_method(self.notify)  # register
        return

    def get_name(self):
        '''Get the name of the analyzer.'''
        return self.name
    
    def notify(self, item):
        '''Handle incoming items'''
        #p rint 'vampire notify ', item
        item.process(self, None)
        # Indicate that we didn't consume it, since we are just recording 
        return False
  
    def process_alert(self, alert, context):
        '''Handle double dispatch from an alert 
        '''
        get_logger().debug(self.get_name() + ' is journaling {0}'.format(str(alert)))
        self.journal.journal_alert(alert)
        return False
    
    def process_event(self, event, context):
        '''Handle double dispatch from an event 
        '''
        get_logger().debug(self.get_name() + ' is journaling {0}'.format(str(event)))
        self.journal.journal_event(event)
        return False
    
    def process_control_msg(self, control_msg, context):
        '''Handle double dispatch from a control msg '''
        get_logger().debug(self.get_name() + ' is journaling {0}'.format(str(control_msg)))
        self.journal.journal_control_msg(control_msg)
        if (control_msg.msg_type == CONTROL_MSG_TYPE_END_OF_DATA):
            # We have received all events we are going to process so
            # we can unregister ourselves from queue    
            self.queue.unregister_listener_method(self.notify)        
        return True
