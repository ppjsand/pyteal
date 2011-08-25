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

from ibm.teal.analyzer.gear.external_base_classes import ExtEvaluate, ExtExecute


class Class052(ExtEvaluate, ExtExecute):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def evaluate(self, dict_in):
        ''' '''
#        print 'Values for Class052 Evaluate >> START'
#        for key in dict_in:
#            print str(key) + ' = ' + str(dict_in[key])
#        print 'Values for Class052 Evaluate >> END'
        try:
            if dict_in['Elvis'] != 'is in the building':
                print 'fail 1'
                return False
            if dict_in['name'] != 'AnalyzerTest052':
                print 'fail 2'
                return False
            if dict_in['mode'] != 1:
                print 'fail 3'
                return False
            event = dict_in['cur_event']
            if event.get_event_id() != dict_in['event_id']:
                print 'fail 4'
                return False
            if event.get_src_loc() != dict_in['src_loc']:
                print 'fail 5'
                return False
            if event.get_rpt_loc() != dict_in['rpt_loc']:
                print 'fail 6'
                return False
            if dict_in['neighbor'] is not None and event.raw_data['neighbor'] != dict_in['neighbor']:
                print 'fail 7'
                return False
            if dict_in['from_conf'] != "evaluate this!":
                print 'fail 8'
                return False
        except:
            print 'fail Exception'
            return False 
        return True
    
    def execute(self, dict_in):
#        print 'Values for Class052 Execute >> START'
#        for key in dict_in:
#            print str(key) + ' = ' + str(dict_in[key])
#        print 'Values for Class052 Execute >> END'
        out_dict = {}
        if dict_in['cur_event'] != dict_in['last_condition_event']:
            print 'events do not match'
            out_dict['alert_id'] = 'Alert 02'
        else:
            out_dict['alert_id'] = 'Alert 03'
        return out_dict