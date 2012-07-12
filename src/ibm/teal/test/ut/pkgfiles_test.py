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

import unittest
from ibm.teal.registry import get_logger
import os
from string import replace
from ibm.teal.test.teal_unittest import TealTestCase

EXT_755 = ['.pm', '.py', '.so']
EXT_644 = ['.json', '.xml', '.conf', '.sql', '.pdf', '.sample', '.po', '.mo', '.pot']
NAME_ONLY_644 = ['cfgloc']

def get_files_and_dirs(tup, path, filenames):
    failures, chk_files, chk_dirs, files_to_exclude = tup
    for filename in filenames:
        base, ext = os.path.splitext(filename)
        full_name = path + '/' + filename
        full_name = replace(full_name, '\\', '/')
        if full_name in files_to_exclude:
            #print 'excluded ' + full_name
            continue
        if ext != '.pyc' and base != 'Makefile':
            if os.path.isdir(path + '/' + filename):
                chk_dirs.append(full_name)
            else:
                chk_files.append(full_name)
    return

def walk_path(base_dir, replace_base, files_to_exclude):
    ''' If this is omitted the messages from check_makefile get eaten '''
    failures = []
    tmp_dirs = []
    tmp_files = []
    os.path.walk(base_dir, get_files_and_dirs, (failures, tmp_files, tmp_dirs, files_to_exclude))
    files = []
    for tmp_file in tmp_files:
        files.append('{0}{1}'.format(replace_base, tmp_file[len(base_dir)+1:]) )
    dirs = []
    for tmp_dir in tmp_dirs:
        dirs.append('{0}{1}'.format(replace_base, tmp_dir[len(base_dir)+1:]) )
    return (failures, files, dirs)

def _load_spec_file(spec_loc, area, contains, failures):
    ''' load the named specfile and put the files it contains into
        contains
    '''
    filename = 'teal-{0}.spec'.format(area)
    fullname = '{0}/{1}/{2}'.format(spec_loc, area, filename)
    
    fullname = replace(fullname, '\\', '/')
    f_spec = open(fullname, 'r')
    for line in f_spec:
        line.lstrip()
        if line[:5] == '%attr':
            #print 'Found %attr: ', line
            s_line =  line.split()
            mode = s_line[1].strip()[:3]
            sfn = s_line[5].strip()
            _check_mode(filename, sfn, mode, failures)
            _check_area(filename, sfn, area, failures)
            
            contains.append(sfn)
        elif line[:7] == '%config':
            s_line =  line.split()
            mode = s_line[2].strip()[:3]
            sfn = s_line[6].strip()
            _check_mode(filename, sfn, mode, failures)
            _check_area(filename, sfn, area, failures)
            
            contains.append(sfn)
    return

def _check_area(filename, fn, area, failures):
    # Special checks by area
    if fn[:23] == '/opt/teal/ibm/teal/test':
        # if area is test this is good if not this is bad
        if area != 'test':
            failures.append('AREA: In {0} file {1} is in the test dir but not in the test spec file'.format(filename, fn))
    else:
        if area == 'test':
            failures.append('AREA: In {0} file {1} is NOT in the test dir but is in the test spec file'.format(filename, fn))
    return

def _check_mode(filename, fn, mode, failures ):
    ''' Check the mode '''
    base, ext = os.path.splitext(fn)
    name = base.rsplit('/', 1)[1]
    if (ext == '' and name not in NAME_ONLY_644) or ext in EXT_755:
        if mode != '755':
            failures.append('MODE: In {0} expected file {1} to have mode 755 but it had {2}'.format(filename, fn, mode))
    elif ext in EXT_644 or (ext == '' and name in NAME_ONLY_644):
        if mode != '644':
            failures.append('MODE: In {0} expected file {1} to have mode 644 but it had {2}'.format(filename, fn, mode))
    else:
        failures.append('MODE: In {0} unknown file {1} had mode {2}'.format(filename, fn, mode))
    return

def _load_il_file(il_loc, area, contains_files, contains_dirs, failures):
    ''' load the named il and put the files it contains into
        contains_files the the directories into contains_dirs
    '''
    link_tgts = []
    filename = 'teal.{0}.il'.format(area)
    fullname = '{0}/{1}/{2}'.format(il_loc, area, filename)
    
    fullname = replace(fullname, '\\', '/')
    f_spec = open(fullname, 'r')
    for line in f_spec:
        line.lstrip()
        if line[:1] == '#':
            continue
        elif line[:1] == 'D' or line[:1] == 'd':
            # Directory entry
            type, s1, s2, mode, dir = line.split()
            if s1 != '2' or s2 != '2':
                failures.append('FMT: In {0} expected dir {1} to have \'2 2\' but had {2} {3}'.format(filename, dir, s1, s2))
            if mode != '755':
                    failures.append('MODE: In {0} expected dir {1} to have mode 755 but it had {2}'.format(filename, dir, mode))
            _check_area(filename, dir, area, failures)
            tmp_dir = dir.rstrip('/')
            contains_dirs.append(tmp_dir)
        elif line[:1] == 'F' or line[:1] == 'f':
            # File entry
            type, s1, s2, mode, fn = line.split()
            _check_mode(filename, fn, mode, failures)
            _check_area(filename, fn, area, failures)
            contains_files.append(fn)
        elif line[:1] == 'S' or line[:1] == 's':
            # Symbolic link -- ignore for now
            type, s1, s2, mode, s_link, t_file = line.split()
            if s1 != '2' or s2 != '2':
                failures.append('FMT: In {0} expected link {1} to have \'2 2\' but had {2} {3}'.format(filename, dir, s1, s2))
            if mode != '755':
                    failures.append('MODE: In {0} expected link {1} to have mode 755 but it had {2}'.format(filename, dir, mode))
            link_tgts.append(t_file)
        else:
            if line.strip() != '':
                failures.append('FMT: In {0} unexpected entry {1}'.format(filename, line.strip()))

    # Check link targets specified
    if len(link_tgts) != 0:
        for link_tgt in link_tgts:
            if link_tgt not in contains_files:
                failures.append('LINKTGT: In {0} link target {1} is not specified'.format(filename, link_tgt))
    
    return

def _compare_file_lists(l1_name, list1, l2_name, list2, area, failures):
    ''' compare the two lists '''
    list1_left = list1[:]
    for fn2 in list2:
        if fn2 in list1_left:
            list1_left.remove(fn2)
        elif fn2 in list1:
            failures.append('DUPE: Area {0} -> file {1} duplicated in {2}'.format(area, fn2, l1_name))
        else:
            failures.append('MISMATCH: Area {0} -> file {1} from {2} not in {3}'.format(area, fn2, l2_name, l1_name))
    for fn1 in list1_left:
        if fn1 in list2:
            failures.append('DUPE: Area {0} -> file {1} duplicated in {2}'.format(area, fn1, l2_name))
        else:
            failures.append('MISMATCH: Area {0} -> file {1} from {2} not in {3}'.format(area, fn1, l1_name, l2_name))
    return
    

TEAL_UT_PKG_DIR = 'TEAL_UT_PKG_DIR'

# Control how the spec files are interpreted
# Dict from pkg to tuple of 
#                       list of files to add to the il file list before comparing to spec
#                       list of files to add to the spec file list before comparing to il
#                       dict of existing_dir to replacement_dir (used to fix file names and to fix dirs)
#                       files not in all check
#                       dirs not in all check    
TEAL_PKGS_CTL = {
                  'base': (
                           # Add to il
                           ['/usr/lib64/libteal_common.so', '/etc/init.d/teal'],
                           # Add to spec
                           [],
                           # Dir replacements
                           {'/install/postscripts/rmcmon/' : '/opt/xcat/lib/perl/xCAT_monitoring/rmc/'},
                           # Files not in all check
                           ['/opt/teal/ibm/teal/monitor/teal_semaphore.so', 
                           '/usr/lib/libteal_common.so', 
                           '/usr/lib64/libteal_common.so'],
                           # Dirs not in all check
                           []
                          ),
                  'test': (
                           # Add to il
                           [],
                           # Add to spec
                           [],
                           # Dir replacements
                           {},
                           # Files not in all check
                           [],
                           # Dirs not in all check
                           []
                           ),
                  'll': (
                           # Add to il
                           ['/etc/init.d/teal_ll'],
                           # Add to spec
                           [],
                           # Dir replacements
                           {},
                           # Files not in all check
                           [],
                           # Dirs not in all check
                           []
                           ),
                  'isnm': (
                           # Add to il
                           ['/usr/lib64/libteal_isnm.so'],
                           # Add to spec
                           [],
                           # Dir replacements
                           {},
                           # Files not in all check
                           ['/usr/lib/libteal_isnm.so', 
                            '/usr/lib64/libteal_isnm.so'],
                           # Dirs not in all check
                           []
                           ),
                  'sfp': (
                           # Add to il
                           [],
                           # Add to spec
                           [],
                           # Dir replacements
                           {},
                           # Files not in all check
                           [],
                           # Dirs not in all check
                           []
                           ),
                  'pnsd': (
                           # Add to il
                           [],
                           # Add to spec
                           [],
                           # Dir replacements
                           {'/install/postscripts/rmcmon/' : '/opt/xcat/lib/perl/xCAT_monitoring/rmc/'},
                           # Files not in all check
                           [],
                           # Dirs not in all check
                           []
                           ),
                 'gpfs': (
                           # Add to il 
                           ['/usr/lib64/libteal_gpfs.so'],
                           # Add to spec
                           ['/usr/lib/libteal_gpfs.so'],
                           # Dir replacements
                           {'/install/postscripts/rmcmon/' : '/opt/xcat/lib/perl/xCAT_monitoring/rmc/'},
                           # Files not in all check
                           ['/usr/lib64/libteal_gpfs.so',
                            '/usr/lib/libteal_gpfs.so',
                            '/opt/teal/bin/tlgpfsstatus',
                            '/opt/teal/bin/tlgpfschnode',
                            '/opt/teal/bin/tlgpfspurge'
                           ],
                           # Dirs not in all check
                           []
                           ),
                 'gpfs-sn': (
                           # Add to il
                           ['/usr/lib64/libteal_gpfs.so',
                            '/usr/lib64/libteal_common.so'],
                           # Add to spec
                           ['/usr/lib/libteal_gpfs.so',
                            '/usr/lib/libteal_common.so'],
                           # Dir replacements
                           {},
                           # Files not in all check
                           ['/usr/lib/libteal_gpfs.so',
                            '/usr/lib/libteal_common.so',
                            '/usr/lib64/libteal_gpfs.so',
                            '/usr/lib64/libteal_common.so',
                            '/opt/teal/bin/tlgpfsmon',
                            '/opt/teal/bin/tlgpfsrefresh',
                            '/opt/teal/bin/tlgpfserrhandler',
                            '/opt/teal/bin/tlgpfslauncher'],
                           # Dirs not in all check
                           ['/opt/teal', '/opt/teal/bin']   # Added by base package
                           ),
                 'ib': (
                        # Add to il
                        ['/etc/init.d/teal_ufm'],
                        # Add to spec
                        [],
                        # Dir replacments
                        {'/install/postscripts/rmcmon/' : '/opt/xcat/lib/perl/xCAT_monitoring/rmc/'},
                        # Files not in all check
                        [],
                        # Dirs not in all check
                        []
                        )
                 }

# Control the collection of source info from the TEAL dirs
#  tuple of tuples
#               base_dir
#               Name of the directory (prepended)
#               list of dirs to exclude
#               list of files to exclude
#               list of dirs to add
#               list of files to add
TEAL_SRC_CTL = (
                  ( '../../..',                                            
                    '/opt/teal/ibm/', 
                    # Exclude
                    [],                                      
                    ['../../../teal/monitor/teal_semaphore.cc', 
                     '../../../teal/test/ut/data/restart_test/test.log',
                     '../../../teal/monitor/teal_semaphore.so'
                    ],   
                    # Add                                                   
                    ['/opt/teal',
                     '/opt/teal/ibm'
                    ],
                    []
                  ),
                  ( '../../../../data',
                    '/opt/teal/data/',
                    # Exclude
                    [],
                    [],
                    # Add
                    ['/opt/teal/data'],
                    []
                  ),
                  ( '../../../../bin',
                    '/opt/teal/bin/',
                    # Exclude
                    [],
                    [],
                    # Add
                    ['/opt/teal/bin'],
                    []
                  ),
                  ( '../../../../sbin',
                    '/opt/teal/sbin/',
                    # Exclude
                    [],
                    [],
                    # Add
                    ['/opt/teal/sbin'],
                    []
                  ),
                  ( '../../../../locale',
                    '/opt/teal/locale/',
                    # Exclude
                    [],
                    [],
                    # Add
                    ['/opt/teal/locale'],
                    []
                  ),
                  ( '../../../../doc',
                    '/opt/teal/doc/',
                    # Exclude
                    [],
                    ['../../../../doc/teal_guide.odt'],
                    # Add
                    ['/opt/teal/doc'],
                    []
                  ),
                  ( '../../../../etc',
                    '/etc/',
                    # Exclude
                    [],
                    [],
                    # Add
                    [],   
                    []
                  ),
                  ( '../../../../perl',
                    '/opt/xcat/lib/perl/',
                    # Exclude
                    ['/opt/xcat/lib/perl/xCAT_monitoring', 
                     '/opt/xcat/lib/perl/xCAT_schema', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/node', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/sn', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Sensor', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/sn/IBM.Condition', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/sn/IBM.EventResponse', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/sn/IBM.Sensor', 
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/node/IBM.Condition',
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/node/IBM.EventResponse',
                     '/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/node/IBM.Sensor'],
                    [],
                    # Add
                    [],
                    ['/opt/xcat/lib/perl/xCAT_monitoring/rmc/scripts/tlpnsd_sensor'] 
                  )              
                )

class TestPkgfiles(TealTestCase):


    def test_pkg_files(self):
        # Make sure we want to check
        # Should be the root dir that contains
        #   /base /devel /test
        
        # Make sure logging is setup
        self.create_temp_logger('info')
            
        # Get the environment variable
        spec_loc = os.environ.get(TEAL_UT_PKG_DIR, None)
        if not spec_loc:
            get_logger().info('Environment variable {0} not set, so nothing to test'.format(TEAL_UT_PKG_DIR))
            return

        # load up the spec files from each of the subdirectories
        # and get a complete list of files
        failures = []
        pkg_files = []
        pkg_dirs = []
        src_files = []
        src_dirs = []
        
        for g_pkg in TEAL_PKGS_CTL.keys():
            spec_files = []
            il_files = []
            il_dirs = []
            # Read control 
            ctl_add_il, ctl_add_spec, ctl_dir_map, not_all_files, not_all_dirs = TEAL_PKGS_CTL[g_pkg]
            _load_spec_file(spec_loc, g_pkg, spec_files, failures )
            _load_il_file(spec_loc, g_pkg, il_files, il_dirs, failures)
            il_files.extend(ctl_add_il)
            spec_files.extend(ctl_add_spec)
            
            # Makes sure spec and il list the same files 
            _compare_file_lists('spec',spec_files, 'il', il_files, g_pkg, failures)
            
            # remove files from all
            for r_file in not_all_files:
                if r_file not in spec_files:
                    failures.append('UNREMOVEABLE: pkg {0} -> file {1} could not be removed'.format(g_pkg, r_file))
                else:
                    spec_files.remove(r_file)
                    
            # remove dirs from all
            for r_dir in not_all_dirs:
                if r_dir not in il_dirs:
                    failures.append('UNREMOVEABLE: pkg {0} -> dir {1} could not be removed'.format(g_pkg, r_dir))
                else:
                    il_dirs.remove(r_dir)
            
            # Make list of all files 
            if len(ctl_dir_map) != 0:
                ## Correct dirs 
                for from_dir, to_dir in ctl_dir_map.items():
                    for t_file in spec_files:
                        if t_file.startswith(from_dir) == True:
                            pkg_files.append(to_dir + t_file[len(from_dir):])
                        else:
                            pkg_files.append(t_file)
                
                # Make list of all dirs
                ## Replace dirs that changed
                for from_dir, to_dir in ctl_dir_map.items():
                    for t_dir in il_dirs:
                        if t_dir.startswith(from_dir) == True:
                            pkg_dirs.append(to_dir + t_dir[len(from_dir):])
                        else:
                            pkg_dirs.append(t_dir)
            else:
                pkg_files.extend(spec_files)
                pkg_dirs.extend(il_dirs)
                
            for t_file in pkg_files:
                if t_file.startswith('/install') == True:
                    print 'pkg ', g_pkg
                    print t_file
        # Collect files from TEAL source
        for base_dir, gath_dir, dirs_to_exclude, files_to_exclude, add_dirs, add_files in TEAL_SRC_CTL:      
            new_failures, teal_files, teal_dirs = walk_path(base_dir, gath_dir, files_to_exclude)
            src_files.extend(teal_files)
            failures.extend(new_failures)
            if len(dirs_to_exclude) != 0:
                for c_dir in teal_dirs:
                    if c_dir not in dirs_to_exclude:
                        src_dirs.append(c_dir)
            else:
                src_dirs.extend(teal_dirs)
            # Add stuff from control
            src_dirs.extend(add_dirs)
            src_files.extend(add_files)

        # Add the log directory
        src_dirs.append('/var/log/teal')
        # Ignore these
        src_files.remove('/etc/xcat/cfgloc')
        src_dirs.remove('/etc/init.d')
        src_dirs.remove('/etc/xcat')
        
        _compare_file_lists('pkg', pkg_files, 'teal', src_files, 'all files', failures)
        _compare_file_lists('pkg', pkg_dirs, 'teal', src_dirs, 'all dirs', failures)
       
        #########################
        # Compare base and base-bg
        base_spec_files = []
        base_bg_spec_files = []
        _load_spec_file(spec_loc, 'base', base_spec_files, failures )
        _load_spec_file(spec_loc, 'base-bg', base_bg_spec_files, failures )
        base_spec_files.remove('/etc/teal/teal.conf')
        base_spec_files.remove('/etc/teal/snmp.conf') 
        base_spec_files.remove('/etc/init.d/teal')
        base_spec_files.remove('/opt/teal/doc/teal_guide.pdf')
        base_spec_files.remove('/opt/teal/data/ibm/teal/sql/install/Teal_db2.sql')
        base_spec_files.remove('/opt/teal/data/ibm/teal/sql/install/Teal_dba_db2.sql')
        base_spec_files.remove('/opt/teal/data/ibm/teal/sql/install/Teal_mysql.sql')
        base_spec_files.remove('/opt/teal/data/ibm/teal/sql/uninstall/Teal_dba_db2.sql')
        base_spec_files.remove('/opt/teal/data/ibm/teal/sql/uninstall/Teal_rm_db2.sql')
        base_spec_files.remove('/opt/teal/data/ibm/teal/sql/uninstall/Teal_rm_mysql.sql')
        base_spec_files.remove('/opt/teal/data/ibm/teal/xml/AMM_1.xml')
        base_spec_files.remove('/opt/teal/data/ibm/teal/xml/IPMI_1.xml')
        base_spec_files.remove('/opt/teal/data/ibm/teal/xml/percs_location.xml')
        base_spec_files.remove('/opt/teal/data/ibm/teal/xml/MM_GEAR_rules.xml') 
        base_spec_files.remove('/opt/teal/data/ibm/teal/xml/IPMI_GEAR_event_metadata.xml') 
        base_spec_files.remove('/opt/teal/bin/tlrmevent')
        base_spec_files.remove('/opt/teal/sbin/tltab')
        base_spec_files.remove('/opt/teal/sbin/tlconfig')
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_schema/Teal_db2.pm')
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_schema/Teal_mysql.pm')
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_schema/Teal_amm.pm') 
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_schema/Teal_ipmi.pm') 
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Sensor/TealSendAlert.pm')
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodeEventNotify.pm')
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodeEventNotify_H.pm')
        base_spec_files.remove('/opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealNotifyEventLogged.pm')
        base_spec_files.remove('/install/postscripts/rmcmon/resources/sn/IBM.Sensor/TealEventNotify.pm') 
        base_spec_files.remove('/install/postscripts/rmcmon/resources/sn/IBM.Condition/TealAnyNodeEventNotify.pm') 
        base_spec_files.remove('/install/postscripts/rmcmon/resources/node/IBM.Sensor/TealEventNotify.pm') 
        base_spec_files.remove('/opt/teal/ibm/teal/connector/tlammtraphandler.py') 
        base_spec_files.remove('/opt/teal/ibm/teal/connector/tlipmitraphandler.py') 
        base_spec_files.remove('/opt/teal/ibm/teal/util/snmp_config.py') 
        base_spec_files.remove('/opt/teal/ibm/teal/util/gear.py') 
        _compare_file_lists('base', base_spec_files, 'base-bg', base_bg_spec_files, 'base spec files', failures)
           
        for fail in failures:
            print fail
        self.assertEquals(str(failures), '[]')
        return

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMakeFiles']
    unittest.main()