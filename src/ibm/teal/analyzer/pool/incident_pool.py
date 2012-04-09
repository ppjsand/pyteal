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

import threading
from collections import defaultdict, namedtuple
from datetime import timedelta, datetime
from ibm.teal.teal_error import TealError
from ibm.teal.util.extendable_timer import ExtendableTimer
from ibm.teal.analyzer.analyzer import EventAnalyzerCheckpoint
from ibm.teal.checkpoint_mgr import CheckpointRecoveryComplete
from ibm.teal.util.msg_target import MsgTargetLogger
import sys
import json
from abc import ABCMeta, abstractmethod
import os
import re
from ibm.teal.util.teal_thread import ThreadKilled

POOL_STATE_AS_STRING = ['New', 'Running', 'Closed', 'Failed']
POOL_STATE_NEW = 0
POOL_STATE_RUNNING = 1
POOL_STATE_CLOSED = 2
POOL_STATE_FAILED = 3

POOL_MODE_AS_STRING = ['Logged', 'Occurred']
POOL_MODE_LOGGED = 0
POOL_MODE_OCCURRED = 1

POOL_ASSOC_AS_STRING = ['Suppressed', 'SuppressedBy']
POOL_ASSOC_SUPPRESSES = 0
POOL_ASSOC_SUPPRESSEDBY = 1

POOL_CLOSE_REASON_AS_STRING = ['Unknown', 'Timer', 'Incident time', 'Shutdown', 'Flush', 'Rule']
POOL_CLOSE_REASON_UNKNOWN = 0
POOL_CLOSE_REASON_TIMER = 1
POOL_CLOSE_REASON_INCIDENT_TIME = 2
POOL_CLOSE_REASON_SHUTDOWN = 3 
POOL_CLOSE_REASON_FLUSH = 4
POOL_CLOSE_REASON_RULE = 5

TEAL_TEST_POOL_LOG_ON_CLOSE = 'TEAL_TEST_POOL_LOG_ON_CLOSE'

POOL_DEFAULT_DURATION = 300 # 5 minutes is the default

# Named tuple: ArrivalCheckCtl
#   window_size -> Number of events to use in calculating events per second
#   minimum -> Minimum number of entries in window needed to do check
#   threshold -> Events per second threshold. 
#   extension --> Number of seconds to extend the pool processing
ArrivalCheckCtl = namedtuple('ArrivalCheckCtl', 'window_min, window_max, arrival_rate, extension')


class IncidentPoolClosedError(TealError):
    '''Error occurred trying to use a pool that has been closed'''
    pass


class IncidentPoolFailedError(TealError):
    '''Error occurred trying to use a pool that has failed'''
    pass


class IncidentPoolStateTransitionError(TealError):
    '''Error occurred because an illegal transition was requested'''
    pass


class IncidentPoolNotClosedError(TealError):
    '''Error occurred because the pool is not closed '''
    pass


class IncidentPoolConfigError(TealError):
    '''Error occurred because of a configuration problem'''
    pass


class IncidentPool(object):
    '''Base pool to work with incidents, which are typically events and alerts
    
       This should not be created directly but should be created via the class methods to 
       make sure the appropriate processing is done
       
       Internal variables of interest
       
       min_time_incidents is a dictionary: key of incident; value of (min_left, added_at_sec, dur_ext)
          where min_left is the number of seconds left from the min time in pool
          added_at_sec is the number of seconds into the pool the incident was added
          dur_ext is the duration extension (to remove need to re-lookup when moving forward)
       suppressed is a dict keyed by incident id to a list of the incidents in the pool that 
          have been suppressed.   This allows quicker suppression processing.
       suppressions is a dictionary: key of incident; value of a list of incidents suppressed
       
       The dict nature is a dict keyed by incident id to a list of incidents in the pool that have 
          not been suppressed ... yet.  This allows quicker suppression processing.
       
       The total set of all events in the pool is the combination of the lists from the nature and 
       the contained suppressed dict's lists.
    '''
    
    @classmethod
    def new_pool(cls, mode, init_duration, max_duration, close_callback=None, msg_target=None, use_timer=False, arrival_check_ctl=None):
        ''' Create the next pool using the current one 

            Input pool should be closed 
        ''' 

        # create the instance to return
        new_obj = cls(mode)

        # setup the message target information 
        if msg_target is None:
            # This only happens when testing 
            new_obj.msg_target = MsgTargetLogger(prefix='TESTING: ')
        else:
            new_obj.msg_target = msg_target
        new_obj.msg_target.debug('Creating NEW Incident Pool init={0} max={1}'.format(str(init_duration), str(max_duration)))

        # Input validation 
        if init_duration < 0:
            raise IncidentPoolConfigError('Negative initial duration specified on creation')
        if max_duration is not None:
            if max_duration < 0:
                raise IncidentPoolConfigError('Negative maximum duration specified on creation')
        else:
            max_duration = POOL_DEFAULT_DURATION # 5 minutes is the default
        if init_duration > max_duration:
            raise IncidentPoolConfigError('Initial duration {0} is larger than maximum duration {1}'.format(str(init_duration), str(max_duration)))
        if mode < 0:
            raise IncidentPoolConfigError('Invalid mode specified {0}'.format(mode))
        try:
            POOL_MODE_AS_STRING[mode]
        except:
            raise IncidentPoolConfigError('Invalid mode specified {0}'.format(mode))

        # Set duration information 
        new_obj.duration = init_duration
        new_obj.init_duration = init_duration
        new_obj.max_duration = max_duration

        # Set close callback 
        new_obj.close_callback = close_callback

        # Indicate if timer should be used
        new_obj.use_timer = use_timer

        # Validate arrival check values
        new_obj.arrival_check_ctl = arrival_check_ctl
        if arrival_check_ctl is not None:
            if arrival_check_ctl.window_max is None or \
               arrival_check_ctl.arrival_rate is None or \
               arrival_check_ctl.extension is None or \
               arrival_check_ctl.window_min is None:
                raise IncidentPoolConfigError('If arrival rate control is specified, then all three values must be specified')
            new_obj.arrival_window_values = [-1] * arrival_check_ctl.window_max
            new_obj.add_arrival_window_value = new_obj.add_arrival_window_value_CHECKED
        return new_obj

    @classmethod
    def next_pool(cls, cur_pool):
        ''' Create the next pool using the current one ''' 

        # Create new instance
        new_obj = cls(cur_pool.mode)
        
        # Copy over msg target values
        new_obj.msg_target = cur_pool.msg_target
        new_obj.msg_target.debug('Creating NEXT Incident Pool init={0} max={1}'.format(str(cur_pool.init_duration), str(cur_pool.max_duration)))

        # Copy over duration values
        new_obj.duration = cur_pool.init_duration
        new_obj.init_duration = cur_pool.init_duration
        new_obj.max_duration = cur_pool.max_duration

        # Copy over close callback
        new_obj.close_callback = cur_pool.close_callback

        new_obj.arrival_check_ctl = cur_pool.arrival_check_ctl
        if cur_pool.arrival_check_ctl is not None:
            new_obj.arrival_window_values = [-1] * cur_pool.arrival_check_ctl.window_max
            new_obj.add_arrival_window_value = new_obj.add_arrival_window_value_CHECKED

        new_obj.use_timer = cur_pool.use_timer

        # Check for incidents moving forward
        # Note: Pool is closed so min_time_incidents only contains incidents to move forward
        if len(cur_pool.min_time_incidents) != 0:
            # Process the incidents moving forward
            # Need to determine start time from current pool
            #  close times may not be filled in so use start times and duration 
            start_time = cur_pool.start_time + timedelta(seconds=cur_pool.duration)
            new_obj.start_time = start_time

            for incident in cur_pool.min_time_incidents.keys():
                # Put in new pool
                new_obj.moved_forward.append(incident)
                # If suppressed in current pool, make suppressed in new
                tid = incident.get_incident_id()
                if tid in cur_pool.suppressed.keys() and incident in cur_pool.suppressed[tid]:
                    new_obj.suppressed[incident.get_incident_id()].append(incident)
                else:
                    new_obj.incidents[incident.get_incident_id()].append(incident)
                # Move things it suppresses
                key = (incident.get_type(), incident.get_rec_id())
                if key in cur_pool.suppressions:
                    new_obj.suppressions[key] = cur_pool.get_suppressed(incident)

                # For events moving forward: update duration, add to moving forward list  
                min_left, added_at_sec, dur_ext = cur_pool.min_time_incidents[incident]
                # Update duration 
                new_obj.duration = min(new_obj.duration + dur_ext, new_obj.max_duration)

                # Calculate new min time in pool  (note: we know positive because if it wasn't, it 
                #  would not have moved forward -- cleanup in close)
                new_min = min_left - (cur_pool.duration - added_at_sec)
                # Add to moving forward list in new pool
                new_obj.min_time_incidents[incident] = (new_min, 0, dur_ext)

                # Process next as a subsequent 
                new_obj.add_incident = new_obj._add_incident_ACTIVE_SUBSEQUENT

            # Start the pool
            # Note: sets the state, the start times, the planned close times, and, if needed,  starts the timer
            new_obj.start(start_time)

        #p rint cur_pool.dump()
        #p rint new_obj.dump()
        return new_obj

    def __init__(self, mode):
        '''Constructor

           This should not be created directly.  It should be created using the class methods above.
           
           mode -- indicate if the pool should use time logged or time occurred
        '''
        self.state = POOL_STATE_NEW

        # Mode controls which time to use 
        self.mode = mode
        if self.mode == POOL_MODE_LOGGED:
            self.get_time = self.get_time_LOGGED
        else:
            self.get_time = self.get_time_OCCURRED

        # New so first incident starts the pool 
        self.add_incident = self._add_incident_ACTIVE_FIRST

        # Lock because timer thread may be accessing asynchronously
        self.lock = threading.RLock()

        # Setup incidents
        self.incidents = defaultdict(list)
        self.last_incident = None 

        # Start with no suppressions 
        self.suppressions = defaultdict(set)
        self.suppressed = defaultdict(list)

        # set start and close times 
        self.start_time = None
        self.planned_close_time = None
        self.close_time = None

        # Initialize timer info
        self.use_timer = False
        self.timer = None

        # Nothing moving forward
        self.moved_forward = []
        self.min_time_incidents = {}

        # Arrival Rate variables
        self.arrival_check_ctl = None
        self.arrival_window_values = [-1]
        
        if os.environ.get(TEAL_TEST_POOL_LOG_ON_CLOSE, 'NO') == 'YES':
            self.log_on_close = True
        else:
            self.log_on_close = False

        return

    def get_time_OCCURRED(self, incident):
        ''' Get the incident time when in occurred mode '''
        return incident.get_time_occurred()

    def get_time_LOGGED(self, incident):
        ''' Get the incident time when in occurred mode '''
        return incident.get_time_logged()

    def start(self, start_time):
        '''Start or restart the time for the pool
        '''
        self.msg_target.debug('Starting while in state {0} {1} {2}' \
                                 .format(POOL_STATE_AS_STRING[self.state], str(start_time), \
                                         str(self.duration)))
        if self.state == POOL_STATE_NEW: 
            self.state = POOL_STATE_RUNNING
            self.start_time = start_time
            self.planned_close_time = self.start_time + timedelta(seconds=self.duration)
            if self.use_timer == True:
                self.timer = ExtendableTimer(self.duration, self.timer_expired)
                self.timer.start()
        else:
            raise IncidentPoolStateTransitionError('Start when in {0} state'.format(POOL_STATE_AS_STRING[self.state]))
        return

    def flush(self, flush_time):
        ''' Flush the pool ... close it now instead of at duration '''
        if self.state != POOL_STATE_RUNNING:
            return 
        self.duration = abs(flush_time - self.start_time).seconds
        self.close(flush_time, POOL_CLOSE_REASON_FLUSH)
        return

    def close(self, close_time, reason):
        '''Close the pool
        '''
        with self.lock:
            if self.state == POOL_STATE_RUNNING:
                # Pool has stuff in it
                if (close_time is not None and close_time < self.start_time):
                    self.msg_target.debug(str(self))
                    raise IncidentPoolStateTransitionError('End time was before start time')
                if self.timer is not None:
                    self.timer.cancel()
                # turn off ability to add incidents
                self.add_incident = self._add_incident_CLOSED
                self.state = POOL_STATE_CLOSED
                self.close_time = close_time
                if self.log_on_close == False:
                    self.msg_target.debug('Closing due to {0} {1}({2})' \
                                         .format(POOL_CLOSE_REASON_AS_STRING[reason], \
                                                 str(self.close_time), str(self.planned_close_time)))
                else:
                    self.msg_target.warning('Closing due to {0}' \
                                         .format(POOL_CLOSE_REASON_AS_STRING[reason]))
                    self.msg_target.warning('{0}'.format(str(self)))
                # check/clean-up min_time entries
                del_list = []
                for incident in self.min_time_incidents.keys():
                    min_left, added_at_sec = self.min_time_incidents[incident][0:2]
                    if min_left <= self.duration - added_at_sec:
                        del_list.append(incident)
                for incident in del_list:
                    del self.min_time_incidents[incident]
                # Callback 
                if self.close_callback is not None:
                    try:
                        tmp_rec_id = self.last_incident.rec_id
                    except ThreadKilled:
                        raise
                    except:
                        tmp_rec_id = None 
                    self.close_callback(reason, tmp_rec_id)
            elif self.state == POOL_STATE_NEW:
                # Pool doesn't have anything in it (created but no incidents added)
                # Set all the times as close time
                self.close_time = close_time
                # Stop timer (could be an incoming shutdown on a timed pool with no elements yet)
                if self.timer is not None:
                    self.timer.cancel()
                # turn off ability to add incidents
                self.add_incident = self._add_incident_CLOSED
                self.state = POOL_STATE_CLOSED
                self.msg_target.debug('Closing {0}' \
                                         .format(POOL_CLOSE_REASON_AS_STRING[reason]))
                if self.close_callback is not None:
                    self.close_callback(reason, None)
            else:
                #self.lock.release()
                raise IncidentPoolStateTransitionError('Closed when in {0} state'.format(POOL_STATE_AS_STRING[self.state]))
        return

    def shutdown(self):
        '''Shutdown the pool.  This includes closing it with shutdown=True'''
        with self.lock:
            if self.state == POOL_STATE_CLOSED:
                # Nobody cares since callback was already called
                return
            elif self.state == POOL_STATE_NEW:
                # start it so we can close it
                now = datetime.now()
                self.start(now)
            # Now close it with shutdown indicator
            self.close(self.planned_close_time, POOL_CLOSE_REASON_SHUTDOWN)
        return

    def failed(self):
        ''' Mark the pool as failed '''
        # turn off ability to add incidents
        self.add_incident = self._add_incident_FAILED
        self.state = POOL_STATE_FAILED
        self.msg_target.error('Pool failed:')
        try:
            self.msg_target.error('{0}'.format(self.dump()))
        except ThreadKilled:
            raise
        except:
            pass
        return

    def add_incident(self, incident, ext_dur, min_time):
        '''Add an incident to the pool.  Using dynamic method pattern
           Note that the ext_dur and min_time must be positive values
        '''
        pass        

    def _add_incident_CLOSED(self, incident, ext_dur, min_time):
        '''Add an incident to the pool when the pool is closed
           Pool is closed, so can't add anymore so raise exception '''
        raise IncidentPoolClosedError('Attempted to add incident to closed pool', error=False)

    def _add_incident_FAILED(self, incident, ext_dur, min_time):
        ''' Add an incident to a failed pool '''
        raise IncidentPoolFailedError('Attempt to add incident to a failed pool')

    def _add_incident_ACTIVE_FIRST(self, incident, ext_dur, min_time):
        '''Add an incident to the pool when it is the first incident to go into the pool'''
        self.lock.acquire()
        try:
            self.duration = min(self.duration + ext_dur, self.max_duration)
            if min_time > 0:
                self.min_time_incidents[incident] = (min_time, 0, ext_dur)
            self.start(self.get_time(incident))
            self.incidents[incident.get_incident_id()].append(incident)
            self.msg_target.debug('Started and {0} added'.format(incident))
            self.add_incident = self._add_incident_ACTIVE_SUBSEQUENT
        except ThreadKilled:
            raise
        except:
            self.lock.release()
            raise
        self.last_incident = incident
        self.add_arrival_window_value(0)
        return

    def _add_incident_ACTIVE_SUBSEQUENT(self, incident, ext_dur, min_time):
        '''Add an incident to the pool, but not the first         
        '''
        self.lock.acquire()
        try:
            # Check if pool should be closed
            point_in_pool = abs(self.get_time(incident) - self.start_time).seconds
            if self.get_time(incident) > self.planned_close_time:
                extension = min(self.get_arrival_extension(point_in_pool), self.max_duration - self.duration)
                if extension == 0:
                    #close the pool and throw exception
                    self.close(self.planned_close_time, POOL_CLOSE_REASON_INCIDENT_TIME)
                    raise IncidentPoolClosedError('Pool closed by incident past planned close time', error=False)
                # Arrival rate extension occurred
                self.msg_target.debug('Arrival rate caused extension of {0}'.format(str(extension)))
                self.duration += extension
                self.planned_close_time += timedelta(seconds=extension)
                if self.use_timer is True:
                    self.timer.add_time(extension)

            # Add the incident 
            self.incidents[incident.get_incident_id()].append(incident)
            self.msg_target.debug('{0} added'.format(incident))
            # Duration is extended after check
            increment = min(ext_dur, self.max_duration - self.duration)
            self.msg_target.debug('Extending pool duration from {0} by {1}'.format(str(self.duration), str(increment)))
            self.duration += increment
            self.planned_close_time += timedelta(seconds=increment)
            # Record min time info if might need at close
            self.add_arrival_window_value(point_in_pool)
            if min_time != 0:
                self.min_time_incidents[incident] = (min_time, point_in_pool, ext_dur)
            if self.use_timer is True:
                self.timer.add_time(increment)
        except ThreadKilled:
            raise
        except:
            self.lock.release()
            raise
        self.last_incident = incident
        return

    def suppresses(self, suppressor, suppressees): 
        '''Suppressor supresses set of suppressees
        
           Suppressor can be either an event or an alert
        ''' 
        if not suppressees:
            return
        key = (suppressor.get_type(), suppressor.get_rec_id())
        self.suppressions[key].update(suppressees)
        for suppressed in suppressees:
            tid = suppressed.get_incident_id()
            if tid in self.incidents.keys() and suppressed in self.incidents[tid]:
                self.incidents[tid].remove(suppressed)
                if len(self.incidents[tid]) == 0:
                    del self.incidents[tid]
                self.suppressed[tid].append(suppressed)
        return

    def get_suppressed(self, suppressor, result=None):
        ''' Get the items that this suppressor suppresses 
            This is transitive
           Suppressor can be either an event or an alert
        ''' 
        key = (suppressor.get_type(), suppressor.get_rec_id())
        if result is None:
            result = set()
        if key not in self.suppressions:
            return result
        # only drill down for ones we haven't already found
        drill_down = self.suppressions[key].copy()
        drill_down.difference_update(result)
        drill_down.difference_update([suppressor])
        # Add the suppressor's suppressed to the result
        result.update(self.suppressions[key])
        # drill down to get transitive closure
        for i in drill_down:
            result.update(self.get_suppressed(i, result))
        return result

    def is_suppressed(self, incident):
        ''' check if the incident is suppressed in this pool '''
        tid = incident.get_incident_id()
        return (tid in self.suppressed.keys() and incident in self.suppressed[tid])

    def force_suppressed(self, incident):
        ''' force the incident to be suppressed in this pool '''
        tid = incident.get_incident_id()
        if tid in self.incidents.keys() and incident in self.incidents[tid]:
            self.incidents[tid].remove(incident)
            if len(self.incidents[tid]) == 0:
                del self.incidents[tid]
            self.suppressed[tid].append(incident)
        return

    def get_incidents(self, incident_id=None):
        ''' Get all incidents in the pool '''
        result = []
        if incident_id is not None:
            if incident_id in self.incidents.keys():
                result.extend(self.incidents[incident_id])
            if incident_id in self.suppressed.keys():
                result.extend(self.suppressed[incident_id])
        else:
            result = []
            for til in self.incidents.values():
                result.extend(til)
            for tsl in self.suppressed.values():
                result.extend(tsl)
        return result

    def get_suppressed_incidents(self, incident_id=None):
        ''' Get all incidents in the pool '''
        if incident_id is not None:
            result = self.suppressed[incident_id]
        else:
            result = []
            for tsl in self.suppressed.values():
                result.extend(tsl)
        return result

    def contains_incident(self, incident_type, incident_id):
        '''Determine if the pool contains at least one incident of the specified incident_type and incident id'''
        # Check unsuppressed
        return ((incident_id in self.incidents.keys() and len(self.incidents[incident_id]))or 
                (incident_id in self.suppressed.keys() and len(self.suppressed[incident_id]))) 

    def timer_expired(self):
        '''Timer has expired so close the pool'''
        if self.state != POOL_STATE_RUNNING:
            # Nobody cares since either the callback has already been called or we failed
            return
        # Check arrival rate to see if we should wait to close 
        extension = min(self.get_arrival_extension(self.duration), self.max_duration - self.duration)
        if extension == 0:
            # Now close it
            try:
                self.close(self.planned_close_time, POOL_CLOSE_REASON_TIMER)
            except ThreadKilled:
                raise
            except:
                self.msg_target.exception('Closing pool because the timer expired failed')
                self.failed()
        else:
            # Need to restart the timer with the extension time
            self.duration += extension
            self.planned_close_time += timedelta(seconds=extension)
            self.msg_target.debug('Starting new timer for extension of {0}'.format(str(extension)))
            self.timer = ExtendableTimer(extension, self.timer_expired)
            self.timer.start()
        return

    def add_arrival_window_value_CHECKED(self, value):
        ''' Add a rate value for arrival checking 
            When checking is done
        '''
        del self.arrival_window_values[0]
        self.arrival_window_values.append(value)
        return 
    
    def add_arrival_window_value(self, value):
        ''' Nothing to do if not checking arrival rate
            Default behavior
        '''
        return

    def get_arrival_rate(self, current_arrival):
        ''' Calculate the arrival rate '''
        # Check if using or if not enough 
        if self.arrival_check_ctl is None:
            return None
        first = self.arrival_window_values[0]
        if first == -1:
            if self.arrival_window_values[-1] == -1:
                return None
            tmp_values = [v for v in self.arrival_window_values if v != -1]
            first = tmp_values[0]
            tmp_size = len(tmp_values)
            if tmp_size < self.arrival_check_ctl.window_min:
                return None
        else:
            tmp_size = self.arrival_check_ctl.window_max
        time_delta = current_arrival - first
        if time_delta == 0:   # All happened at the same time
            return sys.maxint
        return (tmp_size * 1000) / (time_delta)

    def get_arrival_extension(self, current_arrival):
        ''' Check the arrival rate and 
            return True if the time should be extended because of the arrival rate
        '''
        rate = self.get_arrival_rate(current_arrival)
        if rate is None or rate < (1000 * self.arrival_check_ctl.arrival_rate):
            return 0
        self.msg_target.debug('Arrival threshold met: {0} < {1}'.format(str(rate), str(self.arrival_check_ctl.arrival_rate)))
        # Originally did the next line, but it doesn't make sense because we 
        #    should just keep calculating the arrival rate
        #self.arrival_window_values = [-1] * self.arrival_check_ctl.window_max
        return self.arrival_check_ctl.extension 

    def __str__(self):
        ''' Dump out all of the information about the pool as a string 
        '''
        out_str = '\nIncidentPool {0} state = {1};   last = '.format(str(self.msg_target.prefix), POOL_STATE_AS_STRING[self.state])
        if self.last_incident is not None:
            out_str += '{0}'.format(str(self.last_incident.rec_id))
        else:
            out_str += 'None'
        out_str += '\n  duration: {0} >{1}< {2}'.format(self.init_duration, self.duration, self.max_duration)
        out_str += '        timer = {0}'.format(str(self.use_timer))
        out_str += '\n  times: S: {0}'.format(self.start_time)
        if self.planned_close_time:
            out_str += ' PC: {0}({1:5d})'.format(self.planned_close_time,
                                            abs(self.planned_close_time - self.start_time).seconds)
            if self.close_time:
                out_str += ' C: {0}({1:5d})'.format(self.close_time,
                                                 abs(self.close_time - self.start_time).seconds)
        out_str += '\n  active incidents:'
        if len(self.incidents) == 0:
            out_str += '\n     <none>'  
        else:
            for til in self.incidents.values():
                for incident in til:
                    out_str += '\n     {0:5d}: {1:8s} {2}({3:5d})'.format(incident.get_rec_id(),
                                                          incident.get_incident_id(),
                                                          self.get_time(incident),
                                                          abs(self.get_time(incident) - self.start_time).seconds)               
        out_str += '\n  suppressed incidents:'
        if len(self.suppressed) == 0:
            out_str += '\n     <none>'  
        else:
            for tsl in self.suppressed.values():
                for incident in tsl:
                    out_str += '\n     {0:5d}: {1:8s} {2}({3:5d})'.format(incident.get_rec_id(),
                                                          incident.get_incident_id(),
                                                          self.get_time(incident),
                                                          abs(self.get_time(incident) - self.start_time).seconds)               
        out_str += '\n  suppression relationships:'
        if len(self.suppressions) == 0:
            out_str += '\n     <none>'  
        else:
            for key in self.suppressions.keys():
                sup_list = self.suppressions[key]
                out_str += '\n     {0}({1:5d}) -> '.format(key[0], key[1])
                if len(sup_list) == 0:
                    out_str += '     <none>'  
                else:
                    out_str += ','.join(['{0:8s}({1:5d})'.format(sup.get_incident_id(), sup.get_rec_id())for sup in sup_list])

        out_str += '\n  priming incidents:'
        if len(self.moved_forward) == 0:
            out_str += '\n     <none>'  
        else:
            out_str += '\n     '
            out_str += ','.join(['{0:5d}: {1:8s}'.format(mf.get_rec_id(), mf.get_incident_id())for mf in self.moved_forward])

        out_str += '\n  min time in pool monitoring list:'
        if len(self.min_time_incidents) == 0:
            out_str += '\n     <none>'  
        else:
            for incident in self.min_time_incidents.keys():
                min_left, added_at_sec, dur_ext = self.min_time_incidents[incident]
                #print min_left, added_at_sec, dur_ext, incident.get_rec_id(), incident.get_incident_id()
                out_str += '\n     {0:5d}: {1:8s} left = {2:5d} added = {3:5d} ext = {4:5d}' \
                    .format(incident.get_rec_id(), incident.get_incident_id(),
                            min_left, added_at_sec, dur_ext)
        if self.arrival_check_ctl is not None:
            out_str += '\n  arrival rate:  {0} per sec   {1} sec\n     ['.format(
                                                                str(self.arrival_check_ctl.arrival_rate),
                                                                str(self.arrival_check_ctl.extension))
            out_str += ','.join(['{0}'.format(str(tv)) for tv in self.arrival_window_values])
            out_str += '] rate = {0}/1000 per sec'.format(str(self.get_arrival_rate(self.duration)))
        else:
            out_str += '\n  arrival rate: --not checked--'

        return out_str


PARSE_DATA_DEF = '^(?P<rec_id>[\d]+)(?P<sup>[US])(?P<left>[\d]+)([\+](?P<ext>[\d]+)){0,1}$'


class IncidentPoolEventCheckpoint(EventAnalyzerCheckpoint):
    ''' Handle checkpointing for an incident pool 
    
    self.start_rec_id is the min( last_in_pool, (all priming event rec_ids - 1))
    data is a list of:
       -- pool start time
       -- last in pool
       -- list of primes 
            -- compacted entry <rec_id><U|S><time_left>
               -- optional +<dur_ext_time>
               
    Note that if there is no primes then the start_rec_id is the last in pool so data is not recorded and
    the start_rec_id is used as the last in pool rec_id
    
    '''
    
    __metaclass__ = ABCMeta   
     
    def __init__(self, name, msg_target=None):
        ''' Initialize the checkpoint
            Need the ruleset to enable getting to the current pool
        '''
        # setup the message target information 
        if msg_target is None:
            # This only happens when testing 
            self.msg_target = MsgTargetLogger(prefix='TESTING: ')
        else:
            self.msg_target = msg_target
        self.msg_target.debug('Creating IncidentPoolEventCheckpoint {0}'.format(name))

        EventAnalyzerCheckpoint.__init__(self, name)
        if self.data is None:
            # No data so know pool end was the start 
            self.pool_rec_id = self.start_rec_id
        else: 
            try:
                self.pool_rec_id = long(json.loads(self.data)[1])
            except ThreadKilled:
                raise
            except:
                self.msg_target.warning('Checkpoint data invalid')
                self.pool_rec_id = self.start_rec_id
                self.data = None
        self.rec_ids = self._get_rec_ids_from_data()
        self.prime_incidents = []
        return
    
    @abstractmethod   
    def get_pool(self):
        ''' Get the pool
            Allows subclasses to control where the pool is managed
        '''
        pass

    def need_to_analyze(self, event):
        ''' If before my checkpointed rec_id then don't need to process '''
        chk_rec_id = event.rec_id
        # Check if into new pool
        if chk_rec_id > self.pool_rec_id:
            if len(self.rec_ids) != 0:
                self.msg_target.warning('Not all priming events were available.  Missing: {0}'.format(str(self.rec_ids)))
            self._start_pool()
            raise CheckpointRecoveryComplete(self.pool_rec_id, '{0}'.format(self.name))
        # Check if one of the priming events
        if chk_rec_id in self.rec_ids:
            self.prime_incidents.append(event)
            self.rec_ids.remove(chk_rec_id)
        return False

    def set_checkpoint_from_pool(self):
        ''' Set the checkpoint based on the passed pool
            Should only be called once the pool has been closed
        '''
        # Get the current pool from the ruleset
        pool = self.get_pool()
        # Gather information from pool
        if pool.last_incident is None:
            self.msg_target.debug('Not updated checkpoint because nothing processed (last_incident is None)')
            return 
        t_min, t_data = self._gen_min_and_data(pool)
        self.set_checkpoint(t_min, t_data)
        return
    
    def _start_pool(self):
        ''' Initialize and start the pool using the checkpoint data '''
        # Get the current pool from the ruleset
        pool = self.get_pool()
        # Can't checkpoint unless pool is closed
        if pool.state != POOL_STATE_NEW:
            self.msg_target.warning('Unable start from checkpoint with pool that is not NEW')
            return
        if self.data is not None:
            t_list = json.loads(self.data)
            parse_data = re.compile(PARSE_DATA_DEF)
            # Prime
            t_dict = {}
            for t_ent in t_list[2]:
                t_p = parse_data.search(t_ent)
                # Get extension time
                if t_p.group('ext') is None:
                    t_ext = 0
                else:
                    t_ext = long(t_p.group('ext'))
                t_dict[long(t_p.group('rec_id'))] = (t_p.group('sup'), long(t_p.group('left')), t_ext)
                
            # Know there will be one for each of these because they were used to create it
            for t_event in self.rec_ids:
                t_sup, t_min, t_dur = t_dict[t_event.rec_id]
                pool.moved_forward.append(t_event)
                if t_sup == 'S':
                    pool.suppressed[t_event.event_id].append(t_event)
                else:
                    pool.incidents[t_event.event_id].append(t_event)
                pool.duration = min(pool.duration + t_dur, pool.max_duration)
                pool.min_time_incidents[t_event] = (t_min, 0, t_dur)
        
            # Going to start pool so don't have to start when next incident added
            pool.add_incident = pool._add_incident_ACTIVE_SUBSEQUENT
            # Now start the pool with the checkpoint start time
            pool.start(datetime.strptime(t_list[0], '%Y-%m-%d %H:%M:%S.%f'))
        
        return 
    
    def _get_rec_ids_from_data(self):
        ''' Read from the data '''
        if self.data is None:
            return []
        parse_data = re.compile(PARSE_DATA_DEF)
        return [long(parse_data.search(t_list).group('rec_id')) for t_list in json.loads(self.data)[2]]
    
    def _gen_min_and_data(self, pool):
        ''' generate the data and the min '''
        mf_list = []
        min_rec_id = pool.last_incident.rec_id
        for incident in pool.min_time_incidents.keys():
            mf_entry = str(incident.rec_id)
            # Note that generated rec_id always starts with 1, so OK to subtract 1
            min_rec_id = min(min_rec_id, incident.rec_id - 1)
            tid = incident.get_incident_id()
            if tid in pool.suppressed.keys() and incident in pool.suppressed[tid]:
                mf_entry += 'S'
            else:
                mf_entry += 'U'
            # For events moving forward: update duration, add to moving forward list  
            min_left, added_at_sec, dur_ext = pool.min_time_incidents[incident]
    
            # Calculate new min time in pool  (note: we know positive because if it wasn't, it 
            #  would not have moved forward -- cleanup in close)
            mf_entry += str(min_left - (pool.duration - added_at_sec))
            if dur_ext != 0:
                mf_entry += '+{0}'.format(str(dur_ext))
            mf_list.append('"{0}"'.format(mf_entry))
        if pool.start_time is None:
            return (None, None)
        else:
            t_time = pool.start_time + timedelta(seconds=pool.duration)
        return (min_rec_id, '["{0}", "{1}", [{2}]]'.format(str(t_time), pool.last_incident.rec_id, ','.join(mf_list)))
        