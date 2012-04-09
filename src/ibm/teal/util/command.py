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

import sys
import os
import json
import re
import calendar
import optparse
import errno
import tempfile
from datetime import datetime
import gettext
t = gettext.translation('tllsevents', './locale', fallback=True)
_ = t.lgettext

from ibm.teal import location
from ibm.teal import registry

# Daemon information
if sys.platform.find('aix') != -1:
    TEAL_LOCK_DIR = os.path.join(os.sep,'var','locks')
else:
    TEAL_LOCK_DIR = os.path.join(os.sep,'var','lock')

# Query field info constants
EQUALITY_OPS = ['=','>=','<=','<','>']
FIELD_NAME = 0
FIELD_OPS = 1
FIELD_IS_LIST = 2
FIELD_TYPE = 3
FIELD_TYPE_INT = 1
FIELD_TYPE_STRING = 2
FIELD_TYPE_TIMESTAMP = 3

# Timestamp constants
min_yr = '-01-01 00:00:00.000000'
max_yr = '-12-31 23:59:59.999999'
min_mo = '-01 00:00:00.000000'
max_mo = '-{0} 23:59:59.999999'
min_dy = ' 00:00:00.000000'
max_dy = ' 23:59:59.999999'
min_hr = ':00:00.000000'
max_hr = ':59:59.999999'
min_mn = ':00.000000'
max_mn = ':59.999999'
min_sc = '.000000'
max_sc = '.999999'

class JSONEventEncoder(json.JSONEncoder):
    ''' THis is a subclass of the base JSONEncoder class
    that understands how to format datetime objects
    '''
    def default(self,o):
        ''' Additional serializing support for JSON
        '''
        if isinstance(o, datetime):
            return str(o)
        elif isinstance(o, location.Location):
            return o.get_location()
        else:
            return json.JSONEncoder.default(self,o)

class TealOptionParser(object):
    def __init__(self, query_info):
        ''' Constructor. The qry_fields is a list of valid fields to parse on
        the query string and qry_ops is a corresponding list of operations
        valid for each qry_field
        '''
        self.query_info = query_info
        self.fields = set()
        self.locations = {}
        self.location_scopes = {}

    def _gen_location_qry(self, locations, location_scopes):
        ''' Take a set of locations and location scopes and create an SQL where
        condition for a query.

        This method is used with the parsing methods provided by this package
        '''

        # Verify if scope is specified that the corresponding location is specified
        key_fields = locations.keys()
        for scope_key in location_scopes.keys():
            test_loc_key = scope_key[0:-5]+'loc'
            if test_loc_key not in key_fields:
                raise optparse.OptionValueError(_('{0} can not be specified without a valid {1}').format(scope_key, test_loc_key))

        # Generate the where clause for the location specifications
        where_str = ""
        for field in key_fields:
            loc = locations[field]
            type_field = '{0}_type'.format(field)
            # Strip off _loc and add _scope and then look it up in the scoping list
            loc_scope = location_scopes.get(field[0:-4]+'_scope',None)

            if loc_scope:
                try:
                    loc = loc.new_location_by_scope(loc_scope)
                    where_cond = "${0} = '{1}' AND ${2} LIKE '{3}%'".format(type_field,loc.get_id(),field,loc.get_location())
                except:
                    raise optparse.OptionValueError(_('Invalid scope specified: {0}').format(loc_scope))
            else:
                where_cond = "${0} = '{1}' AND ${2} = '{3}'".format(type_field,loc.get_id(),field,loc.get_location())

            self.fields.add(type_field)
            self.fields.add(field)

            if (len(where_str) == 0):
                where_str = where_cond
            else:
                where_str = '{0} AND {1}'.format(where_str,where_cond)

        return where_str

    def _parse_location(self, field, val):
        ''' Parse a single query location
        '''
        where_cond = None
        skip = True

        try:
            idx = val.find(':')
            if (idx < 0):
                # Assume the location specified is just a type
                loc_type = val
                loc = ""
            else:
                (loc_type,loc) = val.split(':',1)

            # Create a location if user specified one so we can
            # validate and do proper scoping if necessary
            if (len(loc) != 0):
                loc_obj = location.Location(loc_type,loc)
                if not loc_obj.is_unprocessable():
                    self.locations[field] = loc_obj
                else:
                    raise ValueError('Unprocessable location:{0}'.format(loc_obj))
            else:
                skip = False
                type_field =  '{0}_type'.format(field)
                self.fields.add(type_field)
                where_cond = "${0} = '{1}'".format(type_field,loc_type)

        except (KeyError,ValueError):
            raise optparse.OptionValueError(_('Location specification "{0}" is invalid').format(field))

        return (skip,where_cond)

    def _gen_timestamp_qry(self, field, op, val):
        ''' Create the where condition for the timestamp. Depending on
        how the user specified the time value, it may be a range of values
        rather than a single value. The range is only used if the  "equals"
        operator is specified
        '''
        try:
            # Returns a timestamp range tuple
            timestamp = validate_timestamp(val)

            if (op == '=') and (len(timestamp) > 1):
                # Timestamp range specified
                where_cond = "${0} >= '{1}' AND ${0} <= '{2}'".format(field,
                                                                      timestamp[0],
                                                                      timestamp[1])

            # If greater than, then use the end of the range so we can
            # say things like "greater than 3/7 and it would show only
            # things on 3/8 and beyond rather than 3/7 12 am and beyond
            elif (op == '>') and (len(timestamp) > 1):
                where_cond = "${0} {1} '{2}'".format(field,op,timestamp[1])

            # If less than or equal to, then use the end of the range so
            # we can say thngs like "less than or equal to 3/7 and it would
            # include all of 3/7 as well as anything before it
            elif (op == "<=") and (len(timestamp) > 1):
                where_cond = "${0} {1} '{2}'".format(field,op,timestamp[1])

            else:
                where_cond = "${0} {1} '{2}'".format(field,op,timestamp[0])

        except ValueError:
            raise optparse.OptionValueError(_('Invalid timestamp for {0}: {1}').format(field, val))

        return where_cond

    def _gen_list_qry(self, field, qry_vals, type):
        ''' Create a where clause for list of items in an equality
        '''
        validate_type(field, qry_vals, type, True)
        self.fields.add(field)
        where_cond = "${0} IN ('".format(field)
        where_cond = where_cond + "','".join(qry_vals.split(',')) + "')"

        return (False,where_cond)

    def _gen_field_qry(self, field, op, val, type):
        ''' Create the SQL query for the current field and value
        '''
        if (field.find('_loc') != -1):
            (skip,where_cond) = self._parse_location(field,val)
        elif (field.find('_scope') != -1):
            skip = True
            where_cond = None
            self.location_scopes[field] = val
        else:
            skip = False
            self.fields.add(field)
            if type == FIELD_TYPE_TIMESTAMP:
                where_cond = self._gen_timestamp_qry(field, op, val)
            else:
                validate_type(field, val, type, False)
                sql_val = val
                where_cond = "${0} {1} '{2}'".format(field, op, sql_val)

        return (skip,where_cond)

    def validate_qry_str(self, opt_str):
        ''' Validate the set of queries passed into the command
        '''
        # If no query string was specified, then none should be returned
        if opt_str is None:
            return None

        # Do a quick check to make sure there are no quotes in the string
        loc = re.search('["\']',opt_str)
        if loc:
            raise optparse.OptionValueError(_('Query string must not contain quotes'))

        regex = re.compile(' *(\w+) *('+ '|'.join(EQUALITY_OPS) + ') *(\S+)')
        qry_str = opt_str.strip()
        where_str = ""

        while(len(qry_str) > 0):
            m = regex.match(qry_str)
            if m is not None:
                qry_str = qry_str[m.end():]
                (field,op,val) =  m.groups()

                field_list = [x for x in self.query_info if x[FIELD_NAME] == field]
                if field_list:
                    field_info = field_list[0]
                else:
                    raise optparse.OptionValueError(_('Invalid field specified: {0}').format(field))

                # Validate the operation on the field
                if op not in field_info[FIELD_OPS]:
                    raise optparse.OptionValueError(_('Invalid operation specified for field "{0}": {1}').format(field,op))

                # Parse and validate the value if necessary
                if (field_info[FIELD_IS_LIST] and (op == '=')):
                    # Options could be a list
                    (skip,where_cond) = self._gen_list_qry(field, val, field_info[FIELD_TYPE])
                else:
                    # only individual values can be specified
                    (skip,where_cond) = self._gen_field_qry(field, op, val, field_info[FIELD_TYPE])

                # Continue parsing if we need to get more data - typically location info
                if (skip):
                    continue

                # Generate sub WHERE clause
                if (len(where_str) == 0):
                    where_str = where_cond
                else:
                    where_str = where_str + ' AND ' + where_cond
            else:
                raise optparse.OptionValueError(_('Invalid query string specified'))

        # Done parsing so now generate where clauses for any locations specified
        where_cond = self._gen_location_qry(self.locations, self.location_scopes)

        # Add the location information clauses if specified
        if (where_cond):
            if (len(where_str) > 0):
                where_str = where_str + ' AND ' + where_cond
            else:
                where_str = where_cond

        # Save the select for the program to use
        return (where_str, self.fields)

    def get_location_options(self):
        loc_svc = registry.get_service(registry.SERVICE_LOCATION)
        loc_types = loc_svc.keys()
        print loc_types
        for t in loc_types:
            loc_infos = loc_svc[t].keys()
            print t,":",loc_svc[t].type
            for i in loc_infos:
                print "\t",i

def validate_qry_str(qry_info, qry_str):
    ''' Validate the query string passed in for the command '''
    qry_parser = TealOptionParser(qry_info)
    return qry_parser.validate_qry_str(qry_str)

def opt_validate_type(option, opt_str, value, parser, *args, **kwargs):
    ''' Validate basic types and list of those types '''
    try:
        validate_type(opt_str, value, args[0], args[1])
        setattr(parser.values, option.dest, value)
    except ValueError, ve:
        raise parser.error(ve)

def validate_type(field, val, type, is_list):
    ''' Validate types other than timestamps '''
    if type == FIELD_TYPE_INT:
        if is_list:
            is_match = re.match('^\d+(,\d+)*$', val)
        else:
            is_match = re.match('^\d+$', val)
    elif type == FIELD_TYPE_STRING:
        if is_list:
            is_match = re.match('^[^,]+(,[^,]+)*$', val)
        else:
            is_match = re.match('^[^,]+$',val)
    else:
        # Catch-all for other types
        is_match = None

    if is_match is None:
        raise optparse.OptionValueError(_('Invalid value(s) for {0}: {1}').format(field, val))

def opt_validate_timestamp(option, opt_str, value, parser, *args, **kwargs):
    ''' Validate a timestamp through the option parser'''
    try:
        timestamp_range = validate_timestamp(value)
        setattr(parser.values, option.dest, timestamp_range)
    except:
        parser.error(_('Invalid timestamp for {0}: {1}').format(opt_str, value))

def validate_timestamp(date_str):
    '''Validate and convert the timestamp into a value understood by a general
    ODBC SQL statement. This may return a range of dates to use based on
    the precision passed by the user
    '''
    m = re.match('^\d{4}(-\d{1,2}(-\d{1,2}(-\d{1,2}(:\d{2}(:\d{2}(\.\d{1,6}){0,1}){0,1}){0,1}){0,1}){0,1}){0,1}$',date_str)
    if m is None:
        raise ValueError, "Invalid date format: " + date_str

    dinfo = date_str.split('-')
    date_len = len(dinfo)
    if date_len == 1: # Year only specified
        timestamp = (date_str + min_yr, date_str + max_yr)
    elif date_len == 2: # Year/Month only specified
        timestamp = (date_str + min_mo, date_str + max_mo.format(calendar.monthrange(int(dinfo[0]),int(dinfo[1]))[1]))
    elif date_len == 3: # Year/Month/Day only specified
        timestamp = (date_str + min_dy, date_str + max_dy)
    elif date_len == 4: # Year/Month/Day with time specified
        date_str = '-'.join(dinfo[0:3])
        datetime_str = date_str + ' ' + dinfo[3]
        tinfo = dinfo[3].split(':')
        time_len = len(tinfo)
        if time_len == 1: # Hour only specified
            timestamp = (datetime_str + min_hr, datetime_str + max_hr)
        elif time_len == 2: # Hour:Min only specified
            timestamp = (datetime_str + min_mn, datetime_str + max_mn)
        elif time_len == 3:
            msinfo = tinfo[2].split('.')
            if len(msinfo) == 1:
                timestamp = (datetime_str + min_sc, datetime_str + max_sc)
            else:
                timestamp = (datetime_str,)

    # Validate created timestamp
    datetime.strptime(timestamp[0].split('.')[0],'%Y-%m-%d %H:%M:%S')

    return timestamp

def single_instance(process_name):
    ''' Determine if TEAL is already running. 
    
    This method assumes that teal is always started the same way with
    the same authority. i.e. if the invocation does not have access to 
    the normal lock dir then it never will and will use the tempdir instead
    '''
    import fcntl
    #####################################################################
    # Make sure the process isn't already running
    #####################################################################

    lock_file = os.path.join(TEAL_LOCK_DIR,'{0}.pid'.format(process_name))

    retry = 0
    while (True):
        try:
            prev_mask = os.umask(0o002)
            lock_fd = os.open(lock_file,os.O_RDWR|os.O_CREAT,0660)
            fcntl.lockf(lock_fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
            os.write(lock_fd,'{0}'.format(os.getpid()))
            break
        except IOError, e:
            sys.exit('{0}: {1} already running'.format(e,process_name))
        except OSError, ose:
            if ose.errno == errno.EACCES and retry == 0:
                retry += 1
                lock_file = os.path.join(tempfile.gettempdir(),'{0}.pid'.format(process_name))                
            else:
                raise
        finally:
            os.umask(prev_mask)
    
    return lock_fd



def daemonize(daemon_name):
    ''' Make a daemon out of the process if requested '''
    import signal
    import errno
    import termios
    import resource

    #####################################################################
    # Migrate the daemon to another process, if appropriate
    #####################################################################

    # Only fork if we were not started by the init process
    if ((os.getppid() != 1) and (sys.platform.find('aix') == -1)):
        child = os.fork()
        # Check if we are in the child or parent
        if (child != 0):
            # Parent process - just exit
            sys.exit(0)

    # Make sure the process isn't already running
    lock_fd = single_instance(daemon_name)

    #####################################################################
    # Ignore terminal-generated signals
    #####################################################################

    ignored_signals = [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTSTP, signal.SIGTTIN, signal.SIGTTOU]
    for sig in ignored_signals:
        signal.signal(sig, signal.SIG_IGN)

    #####################################################################
    # Disassociate the daemon from its controlling terminal
    #####################################################################

    try:
        os.setsid()
    except OSError, e:
        # If we couldn't set it, interpret as it already is
        pass

    # if we did become the session leader, release the terminal
    if os.getsid(0) == os.getpid():

        # Check if the process has a controlling terminal and release it if it does
        id = os.ctermid()
        try:
            fd = os.open(id,os.O_RDWR|os.O_NOCTTY)
            fcntl.ioctl(fd, termios.TIOCNOTTY)
            os.close(fd)
        except OSError, e:
            if e.errno != errno.ENXIO:
                raise

    #####################################################################
    # Deal with non-terminal generated signals
    #####################################################################

    # Don't want to be notified if some plug-in's pipe goes belly-up
    signal.signal(signal.SIGPIPE,signal.SIG_IGN)

    #####################################################################
    # Close unnecessary descriptors
    #####################################################################

    max_fds = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
    if(max_fds == resource.RLIM_INFINITY):
        max_fds = 65535 # just make it sufficently large

    standard_fds = [sys.stdin.fileno(), sys.stdout.fileno(), sys.stderr.fileno(), lock_fd]

    # Close all but the standard files and the lock file
    for fd in xrange(max_fds):
        if fd not in standard_fds:
            try:
                os.close(fd)
            except OSError:
                pass

    #####################################################################
    # Ensure certain file descriptors are open
    #####################################################################

    if (sys.platform.find('aix') == -1):
        # Assume these are the only files that are open
        sys.stdin.close()
        sys.stderr.close()
        sys.stdout.close()

        # Order is important here for file descriptors 0,1,2
        sys.stdin = open('/dev/null','r')
        sys.stdout = open('/dev/null','w')
        sys.stderr = open('/dev/null','w')
    else:
        # For AIX we want to keep the descriptors as is so we can log
        # to the console and see errors
        pass

    #####################################################################
    # Set the process file mode creation mask
    #####################################################################

    os.chdir('/')
    os.umask(0)
