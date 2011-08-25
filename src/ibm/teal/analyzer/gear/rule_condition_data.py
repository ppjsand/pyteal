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

from collections import defaultdict
from ibm.teal.registry import get_logger
from ibm.teal.analyzer.gear.rule_value import GRVA_TYPE_LOCATION_MATCH_IDENTICAL,\
    GRVA_TYPE_LOCATION_MATCH_IGNORE
from ibm.teal.teal_error import TealError
import itertools


class InstanceError(TealError):
    ''' Indicate that there was an error getting the instance or with the instance retreived '''
    pass


class ConditionData(object):
    ''' Condition Data class 
        Able to manage condition data and determine truth spaces from that 
        data
    '''
        
    def __init__(self, condition):
        ''' Initialize the condition data manager '''
        # track the events by scoped location, event id, and instance info
        self.events = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
        self.condition = condition 
        return 
    
    def clear(self):
        ''' clear the data ''' 
        self.events = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
        return
        
    def accumulate(self, event, loc):
        ''' Accumulate the event '''
        self.events[self._get_loc(loc)][self._get_id(event)][self._get_instance(loc)].append(event)
        return 
    
    def remove_events(self, r_events):
        ''' Remove the specified events ''' 
        tmp_remove_dps = []
        for loc in self.events.iterkeys():
            for id in self.events[loc].iterkeys():
                for inst in self.events[loc][id].iterkeys():
                    for r_event in self.events[loc][id][inst]:
                        if r_event in r_events:
                            tmp_remove_dps.append((loc, id, inst, r_event))
        for r_dp in tmp_remove_dps:
            try:
                self.events[r_dp[0]][r_dp[1]][r_dp[2]].remove(r_dp[3])
                if len(self.events[r_dp[0]][r_dp[1]][r_dp[2]]) == 0:
                    del self.events[r_dp[0]][r_dp[1]][r_dp[2]]
                    if len(self.events[r_dp[0]][r_dp[1]]) == 0:
                        del self.events[r_dp[0]][r_dp[1]]
                        if len(self.events[r_dp[0]]) == 0:
                            del self.events[r_dp[0]]
            except InstanceError:
                pass
        return 

    def get_truth_space(self, prime_set, min_num=1):
        ''' Prime the condition with the event '''
        truth_space = set()
        #print _print_events_struct(self.events, title='get_truth_space')
        point_list = self._collect_at_loc(self.events, min_num)
        for point in point_list:
            if point[1].issubset(prime_set) == False:
                truth_space.add(point)
        return truth_space
    
    # Location processing 
    def use_loc(self, location_match, scope=None):
        ''' Indicate that location should be used '''
        if location_match == GRVA_TYPE_LOCATION_MATCH_IGNORE:
            self.loc_scope = None
            # default self._collect_at_loc (does both ignore and identical)
            return
        
        # Scope can be used for either identical or unique 
        if scope is None:
            self._get_loc = self._get_loc_used
        else:
            self.loc_scope = scope
            self._get_loc = self._get_loc_used_scoped
        
        if location_match == GRVA_TYPE_LOCATION_MATCH_IDENTICAL:
            # default (does both ignore and identical)
            return 
        
        self._collect_at_loc = self._collect_at_loc_unique
        return
    
    def _get_loc(self, loc):
        ''' Get the location ... default is location is not used ''' 
        return None
    
    def _get_loc_used(self, loc):
        ''' Location used but not scoped '''
        return loc
    
    def _get_loc_used_scoped(self, loc):
        ''' Location is used and is scoped '''
        return loc.new_location_by_scope(self.loc_scope)
    
    # Id processing
    def use_unique_id(self):
        ''' Indicate that the id should be unique '''
        self._get_id = self._get_id_used
        self._collect_at_id = self._collect_at_id_unique
        return
    
    def _get_id(self, event):
        ''' Default is the id is not used '''
        return None
    
    def _get_id_used(self, event):
        ''' Use the id '''
        return event.event_id
    
    # Instance processing
    def use_comp_instance(self, comp, instances):
        ''' Indicate that an instance component of the location should be used 
            Note: this or set_use_unique_instance should be called, but not both
        '''
        self._collect_at_inst = self._collect_at_inst_comp
        self.comp = comp
        self.instances = instances
        self._get_instance = self._get_instance_comp
        return 
    
    def use_unique_instance(self, scope):
        ''' Indicate that unique instances at the specified scope should be used 
            Note: this or set_use_comp_instance should be called, but not both
        ''' 
        self._collect_at_inst = self._collect_at_inst_unique 
        if scope is None:
            self._get_instance = self._get_instance_unique
        else:
            self.instance_scope = scope
            self._get_instance = self._get_instance_unique_scoped
        return 

    def _get_instance(self, loc):
        ''' Default is to not use instance '''
        return None
    
    def _get_instance_comp(self, loc):
        ''' Use an instance component '''
        try:
            instance = loc.get_comp_value(self.comp)
        except:
            raise InstanceError('Unable to get comp {0} from location {1}'.format(self.comp, str(loc)), error=False)
        if self.instances.in_comparison(instance) == False:
            raise InstanceError('Instance value of {0} not included in comparison'.format(instance), error=False)
        return instance
    
    def _get_instance_unique(self, loc):
        ''' Use the location for the unique instance check '''
        return loc
    
    def _get_instance_unique_scoped(self, loc):
        ''' Use the scoped location for the unique instance check '''
        return loc.new_location_by_scope(self.instance_scope)
    
    #
    # Collection helpers 
    #
    # Collect at location level 
    #    Returns list of truth points
    def _collect_at_loc(self, dict_by_loc, min):
        ''' Collect values by location for ignore and identical locations 
        
            For ignore there is one key: None so loops only once
            For identical it will look for each key: location (scoped)
        ''' 
        tmp_events_list = []
        for loc, dict_by_id in dict_by_loc.items():
                tmp_events = self._collect_at_id([dict_by_id], min)
                if len(tmp_events) >= min:
                    tmp_events_list.append((frozenset([loc]), frozenset(tmp_events)))
        return tmp_events_list
    
    def _collect_at_loc_unique(self, dict_by_loc, min):
        ''' Collect values by location for unique locations ''' 
        if len(dict_by_loc.keys()) < min:
            return list()
        tmp_events_dict = {}
        # Get results for each combination
        for t_locs in itertools.combinations(dict_by_loc.keys(), min):
            dict_by_id_list = [dict_by_loc[t_loc] for t_loc in t_locs]
                
            tmp_events = self._collect_at_id(dict_by_id_list, min)
            if tmp_events is not None and len(tmp_events) >= min:
                # See if overlaps existing key 
                found = False
                ck_loc_set = set(t_locs)
                for key, value in tmp_events_dict.items(): 
                    if key.isdisjoint(ck_loc_set) == False:
                        found = True
                        break
                if found == True:
                    del tmp_events_dict[key]
                    tmp_events.extend(value)
                    ck_loc_set = ck_loc_set.union(key)
                tmp_events_dict[frozenset(ck_loc_set)] = tmp_events
                        
        # Add the truth points 
        truth_points = []
        for key, value in tmp_events_dict.items():
            truth_points.append((key, frozenset(value)))      
        return truth_points     
                
    # Collect at id level
    def _collect_at_id(self, dict_by_id_list, min):
        ''' Collect at id level 
            Default is to ignore the id '''
        dict_by_inst_list = []
        for dict_by_id in dict_by_id_list:
            # There should be only one key that is None ... so don't really need to do this.
            for dict_by_inst in dict_by_id.values():
                dict_by_inst_list.append(dict_by_inst)
        return self._collect_at_inst(dict_by_inst_list, min)
    
    def _collect_at_id_unique(self, dict_by_id_list, min):
        ''' Collect at id level -- with unique ids ''' 
        # Input is a list of dict_by_id that we have to pick from
        # If there is only one, then we pick from that one (it wasn't unique above us)
        #  Call down with a list of each perm of dicts by instance (contained dict)
        tmp_events = []
        if len(dict_by_id_list) == 1:
            tmp_dict_by_id = dict_by_id_list[0]
            for t_ids in itertools.combinations(tmp_dict_by_id.keys(), min):
                tmp_dict_by_inst_list = [tmp_dict_by_id[id] for id in t_ids]
                tmp_events.extend(self._collect_at_inst(tmp_dict_by_inst_list, min))
        else:
            # It was unique above us so we'll get min entries in the dict and have
            # to look at combinations over that
            tmp_ids_list_list = [t_dict.keys() for t_dict in dict_by_id_list]
            for ids_prod in itertools.product(*tmp_ids_list_list):
                if len(set(ids_prod)) < min:
                    # Must all be unique
                    continue
                tmp_dict_by_inst_list = [dict_by_id_list[t_idx][t_id] for t_idx, t_id in enumerate(ids_prod)]
                tmp_events.extend(self._collect_at_inst(tmp_dict_by_inst_list, min))
        return tmp_events    
            
    # Collect at instance level
    def _collect_at_inst(self, dict_by_inst_list, min):
        ''' Collect at instance level -- default is to ignore '''
        tmp_events = []
        for dict_by_inst in dict_by_inst_list:
            for e_list in dict_by_inst.values():
                tmp_events.extend(e_list)
        return tmp_events
      
    def _collect_at_inst_unique(self, dict_by_inst_list, min):
        ''' Collect at instance level when unique instances are required ''' 
        # If only one element then just have to make sure enough keys
        # else have to look at prods of keys of dicts in list 
        tmp_events = []
        if len(dict_by_inst_list) == 1:
            # Only have to see if the enough keys in the one dictionary
            if len(dict_by_inst_list[0]) >= min:
                for i_events in dict_by_inst_list[0].values():
                    tmp_events.extend(i_events)
        else:
            # Have to look at products of instance keys in list of dictionaries
            tmp_inst_list_list = [t_dict.keys() for t_dict in dict_by_inst_list]
            for insts_prod in itertools.product(*tmp_inst_list_list):
                if len(set(insts_prod)) < min:
                    # Must all be unique
                    continue
                for t_idx, t_inst in enumerate(insts_prod):
                    tmp_events.extend(dict_by_inst_list[t_idx][t_inst])  
        return tmp_events
      
    def _collect_at_inst_comp(self, dict_by_inst_list, min):
        ''' Collect at instance level when a instance comparitor is being used ''' 
        # If only one element then just have to make sure enough keys
        # else have to look at prods of keys of dicts in list 
        tmp_events = []
        if len(dict_by_inst_list) == 1:
            # Don't have to see if enough, just check
            self.instances.clear()
            if self.instances.check(dict_by_inst_list[0].keys()) == True: 
                for i_events in dict_by_inst_list[0].values():
                    tmp_events.extend(i_events)
        else:
            # Have to look at products of instance keys in list of dictionaries
            tmp_inst_list_list = [t_dict.keys() for t_dict in dict_by_inst_list]
            for insts_prod in itertools.product(*tmp_inst_list_list):
                # Don't check if unique
                #  it is ok if we have 1,1,2 if only 1&2 is needed 
                self.instances.clear()
                if self.instances.check(insts_prod) == False:
                    continue
                for t_idx, t_inst in enumerate(insts_prod):
                    tmp_events.extend(dict_by_inst_list[t_idx][t_inst])  
        return tmp_events
    
# HELPER
#def _print_events_struct(events, title=''):
#    ''' print the events structure '''
#    outstr = title + '\n'
#    for loc_k, loc_v in events.items():
#        outstr += '  ' + str(loc_k) +'\n'
#        for id_k, id_v in loc_v.items():
#            outstr += '    ' + str(id_k) + '\n'
#            if len(id_v) == 0:
#                outstr += '        -empty\n'
#            else:
#                for inst_k, inst_v in id_v.items():
#                    outstr += '      ' + str(inst_k) + '\n'
#                    if inst_v is not None:
#                        outstr += '          ' + ','.join([e.brief_str() for e in inst_v]) + '\n'
#                    else:
#                        outstr += '          ' + '-empty-\n'
#    return outstr
         
    