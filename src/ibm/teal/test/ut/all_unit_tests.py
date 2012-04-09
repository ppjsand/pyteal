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

import os
import inspect
import unittest

from ibm.teal.test.teal_unittest import truncate_all_teal_tables

def get_suites(tup, path, filenames):
    suites = tup[1]
    filenames.sort()
    for filename in filenames:
        base, ext = os.path.splitext(filename)
        if ext == '':
            continue
        if ext != '.py':
            continue
        if base == 'all_unit_tests':
            continue
        if base == '__init__':            
            continue
        if base == 'cnm_gear':            
            continue
        # TODO: Really need to not process 'test\ut\data and subdirs.
        if base == 'test_class' or base == 'G1_test_class':
            continue
        if base[0] == '.':
            continue
        
        module = __import__(base)
        suites += unittest.defaultTestLoader.loadTestsFromModule(module)
    return

def walk_path(path):
    suites = []
    os.path.walk(path, get_suites, (path, suites))
    return suites


if __name__ == '__main__':
    # inspect is used so that code coverage can work. Code coverage changes
    # the file name to a file in the coverage plugin and screws up the
    # path information for the unit test directory
    my_path = os.path.dirname(inspect.currentframe().f_code.co_filename)

    if my_path == "":
        my_path = os.getcwd()
    
    suites = walk_path(my_path)
    #print suites
    run = 0
    errors = 0
    failures = 0
    error_list =[]
    failure_list = []
    for suite in suites:
        #print "thread stack size: {0}".format(threading.stack_size(32768*2))
        test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        run += test_result.testsRun
        errors += len(test_result.errors)
        for (name,traceback) in test_result.errors:
            error_list.append(name)
        failures += len(test_result.failures)
        for (name,traceback) in test_result.failures:
            failure_list.append(name)
            
    # Clean up the tables
    truncate_all_teal_tables()
    
    print 'Test Complete:'
    print '  Run = ' + str(run)
    print '  Errors = ' + str(errors)
    if len(error_list) != 0:
        print '     Tests with error:'
        for error in error_list:
            print '          ' + str(error)
    print '  Failures = ' + str(failures)
    if len(failure_list) != 0:
        print '     Tests with failure:'
        for fail in failure_list:
            print '          ' + str(fail)
    if(errors != 0) or (failures != 0):
        raise RuntimeError("Tests failed.")
