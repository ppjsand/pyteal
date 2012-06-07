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
import os
from ibm.teal import teal
from ibm.teal.registry import get_service, SERVICE_ALERT_DELIVERY, SERVICE_EVENT_Q
from ibm.teal.util.journal import Journal
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.control_msg import ControlMsg, CONTROL_MSG_TYPE_FLUSH,\
    CONTROL_MSG_ATTR_CREATION_TIME
from datetime import datetime, timedelta


class GearRulesetExecution(TealTestCase):
    '''Test running GEAR rulesets'''
    
    def test_execution(self):
        ''' Run gear execution tests'''
        # TODO: Remove restriction
        #   8, 23 - Problem is optimization of location_match=unique not working the same way with instances option.
        skip = [8, 23]
        num_tests = 27  
        for x in xrange(1, num_tests+1):  # one more than max dir num
            if x in skip:
                continue
            test_dir = 't' + str(x).zfill(3)
            print '>>>> Testing ' + test_dir
            
            self._execute_rule(test_dir, debug=False)
        return
    
#    def test_execution_next(self):
#        ''' Run gear execution tests'''
#        #save_env = self.force_env('TEAL_ALERT_PRIORITIZATION', 'NO')
#        #save_env2 = self.force_env('TEAL_LOCATION_VALIDATION', 'IMMEDIATE')
#        test = 28 # 28 is NEXT
#        for x in xrange(test, test+1):  # one more than max dir num
#            test_dir = 't' + str(x).zfill(3)
#            print '>>>> Testing ' + test_dir
#            self._execute_rule(test_dir, debug=True)#, wait_sec=100, wait_num=10, force_save=True)#, wait_sec=100)
#            #, max_key=2--, inject_flush=True, wait_sec=10)#wait_num=100)#, force_save=True)
#        #self.restore_env('TEAL_ALERT_PRIORITIZATION', save_env)
#        #self.restore_env('TEAL_LOCATION_VALIDATION', save_env2)
#        return
    
    def _execute_rule(self, dir, debug=False, wait_sec=60, wait_num=None, force_save=False, 
                      max_key=None, inject_flush=False):
        '''Run the test defined in the specified directory'''
 
        config = 'data/gear_ruleset_test/' + dir + '/config.conf'
        input = 'data/gear_ruleset_test/' + dir + '/event_input.json'
        base_output = 'data/gear_ruleset_test/' + dir
        test_files =  os.listdir('data/gear_ruleset_test/' + dir)
        # Figure out what output files need to be checked
        out_prefix = 'alert_output'
        out_to_check = [] 
        for filename in test_files:
            base, ext = os.path.splitext(filename)
            if ext != '.json':
                continue
            if base[:len(out_prefix)] == out_prefix:
                out_to_check.append(base[len(out_prefix):])
        # out_to_check now contains the unique part of the output file name
        
        if debug:
            msg_level = 'debug'
        else:
            msg_level = self.msglevel
        # TODO: Make work with duplicate checking
        keep_ADC = self.force_env('TEAL_ALERT_DUPLICATE_CHECK', 'No')
        myteal = teal.Teal(config, 'stderr', msgLevel=msg_level, commit_alerts=False, commit_checkpoints=False) 
        j_in = Journal('j_in', input)
        # get the listeners to get the journals from
        #   Make a list to find
        jl_names = []
        j_out_list = {}
        list_prefix = 'ListenerJournal'
        for up in out_to_check:
            jl_names.append( list_prefix + up)
        listeners = get_service(SERVICE_ALERT_DELIVERY).listeners
        for listener in listeners:
            if listener.get_name() in jl_names:
                j_out_list[listener.get_name()[len(list_prefix):]] = listener.journal
        
        event_q = get_service(SERVICE_EVENT_Q)
        if debug:
            # Print before injection in case problem with injection
            print j_in
        j_in.inject_queue(event_q, no_delay=False, max_key=max_key)
        if inject_flush == True:
            self._inject_flush(event_q)
        for up in out_to_check:
            output = base_output + '/' + out_prefix + up + '.json'
            j_exp = Journal('j_exp' + up, output )
            if wait_num is None:
                wait_num = len(j_exp)
            self.assertTrue(j_out_list[up].wait_for_entries(wait_num, seconds=wait_sec))
            if debug:
                print j_exp
                print j_out_list[up]
                if force_save == True:
                    j_out_list[up].save(output)
            self.assertTrue(j_out_list[up].deep_match(j_exp, ignore_delay=True, ignore_times=True, unordered=True)) 
        myteal.shutdown()
        self.restore_env('TEAL_ALERT_DUPLICATE_CHECK', keep_ADC)
        return
    
    def _inject_flush(self, event_q, time=0):
        ''' create a flush command msg '''
        ctl_msg = ControlMsg(CONTROL_MSG_TYPE_FLUSH, {CONTROL_MSG_ATTR_CREATION_TIME: datetime.now()+ timedelta(seconds=time)})
        event_q.put_nowait(ctl_msg)
        return

if __name__ == "__main__":
    unittest.main()