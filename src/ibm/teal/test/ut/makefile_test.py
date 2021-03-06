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
from ibm.teal.registry import get_logger, TEAL_ROOT_DIR
import os
from string import replace
from ibm.teal.test.teal_unittest import TealTestCase

def check_makefile(tup, path, filenames):
    failures, files_to_exclude = tup
    chk_files = []
    chk_dirs = []
    make_file_found = False
    for filename in filenames:
        base, ext = os.path.splitext(filename)
        full_name = path + '/' + filename
        full_name = replace(full_name, '\\', '/')
        if full_name in files_to_exclude:
            # print 'excluded ' + full_name
            continue
        if ext != '.pyc' and base != 'Makefile':
            if os.path.isdir(path + '/' + filename):
                chk_dirs.append(filename)
            else:
                chk_files.append(filename)
        elif base == 'Makefile' and ext == '':
            make_file_found = True
     
    if not make_file_found and len(chk_files) != 0:
        print 'FAILURE ... missing make file for ' + str(path)
        failures.append(path)
    # Now get the SCRIPT line from the Makefile
    f_make = open(path + '/Makefile', 'r')
    chk_files_left = chk_files[:]
    chk_dirs_left = chk_dirs[:]
    for line in f_make:
        line.lstrip()
        if line[:7] == 'SCRIPTS':
            script_files = line.split()[2:] # drop SCRIPTS =
            # now compare script_files to chk_files
            for tmp_file in script_files:
                if tmp_file in chk_files:
                    chk_files_left.remove(tmp_file)
                else:
                    tmp_file = replace(str(path)+'/'+str(tmp_file), '\\', '/')
                    if tmp_file in files_to_exclude:
                        continue
                    print 'FAILURE ... extra file in ' + str(path) + '/Makefile -> ' + str(tmp_file)
                    failures.append(tmp_file)
            if len(chk_files_left) != 0:
                for tmp_file in chk_files_left:
                    print 'FAILURE ... file not in ' + str(path) + '/Makefile -> ' + str(tmp_file)
                    failures.append(str(path) + '/' + str(tmp_file))
        elif line[:7] == 'SUBDIRS':
            script_dirs = line.split()[2:] # drop SUBDIRS
            for tmp_dir in script_dirs:
                if tmp_dir in chk_dirs:
                    chk_dirs_left.remove(tmp_dir)
                else:
                    print 'FAILURE ... extra dir in ' + str(path) + '/Makefile -> ' + str(tmp_dir)
                    failures.append(str(path) + '/' + str(tmp_dir))
            if len(chk_dirs_left) != 0:
                for tmp_dir in chk_dirs_left:
                    print 'FAILURE ... directory not in ' + str(path) + '/Makefile -> ' + str(tmp_dir)
                    failures.append(str(path) + '/' + str(tmp_dir))
        elif line[:4] == 'IDIR':
            idir = line.split()[2:]
            if len(path) > 8:
                ckpath = '/opt/teal/ibm/' + replace(path, '\\', '/')[9:] + '/'
            else:
                ckpath = '/opt/teal/ibm/'
            if idir[0] != ckpath:
                print 'FAILURE ... IDIR is not correct in ' + str(path) + '/Makefile -> found ' + str(idir[0]) + '   expected ' + str(ckpath) 
                failures.append(str(path) + '/Makefile')
    f_make.close()

def walk_path(base_dir, files_to_exclude):
    ''' If this is omitted the messages from check_makefile get eaten '''
    failures = []
    os.path.walk(base_dir, check_makefile, (failures, files_to_exclude))
    return failures

class TestMakefiles(TealTestCase):

    def testMakefiles(self):

        # Make sure logging is setup
        self.create_temp_logger('info')
        
        # Check if TEAL_ROOT_DIR is set ... if it is not, do not run the test
        if os.environ[TEAL_ROOT_DIR] == os.path.join(os.sep, 'opt', 'teal'):
            get_logger().info('Make file test not run because using default install directory')
            return 
       
        base_dir = '../../..' # This should be ibm
        ## ADD EXCLUSIONS BELOW
        files_to_exclude = ['../../../teal/monitor/teal_semaphore.cc', 
                            '../../../teal/test/ut/data/restart_test/test.log',
                            '../../../teal/monitor/teal_semaphore.so']
        failures = walk_path(base_dir, files_to_exclude)
        self.assertEquals(str(failures), '[]')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMakeFiles']
    unittest.main()