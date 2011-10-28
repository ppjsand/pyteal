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
            for t_id in self.events[loc].iterkeys():
                for inst in self.events[loc][t_id].iterkeys():
                    for r_event in self.events[loc][t_id][inst]:
                        if r_event in r_events:
                            tmp_remove_dps.append((loc, t_id, inst, r_event))
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

    def get_truth_space(self, prime_set, min_num, dups):
        ''' Prime the condition with the event '''
        point_list = self._collect_at_loc(self.events, min_num, dups)

        if prime_set is None:
            return set(point_list)
        
        truth_space = set()
        #print _print_events_struct(self.events, title='get_truth_space')
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
    # Collection routines
    #
    # Collect at location level 
    #    Returns list of truth points
    def _collect_at_loc(self, dict_by_loc, min_needed, dups):
        ''' Collect values by location for ignore and identical locations 
        
            For ignore there is one key: None so loops only once
            For identical it will look for each key: location (scoped)
        ''' 
        tmp_events_list = []
        for loc, dict_by_id in dict_by_loc.items():
                tmp_events = self._collect_at_id([dict_by_id], min_needed, dups)
                if len(set(tmp_events)) >= min_needed:  
                    tmp_events_list.append((frozenset([loc]), frozenset(tmp_events)))
        return tmp_events_list
    
    def _collect_at_loc_unique(self, dict_by_loc, min_needed, dups):
        ''' Collect values by location for unique locations ''' 
        if len(dict_by_loc.keys()) < min_needed:
            return list()
        tmp_events_dict = {}
        # Get results for each combination
        for t_locs in itertools.combinations(dict_by_loc.keys(), min_needed):
            dict_by_id_list = [dict_by_loc[t_loc] for t_loc in t_locs]
                
            tmp_events = self._collect_at_id(dict_by_id_list, min_needed, dups)
            if tmp_events is not None and len(set(tmp_events)) >= min_needed:
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
    def _collect_at_id(self, dict_by_id_list, min_needed, dups):
        ''' Collect at id level 
            Default is to ignore the id '''
        dict_by_inst_list = []
        for dict_by_id in dict_by_id_list:
            # There should be only one key that is None ... so don't really need to do this.
            for dict_by_inst in dict_by_id.values():
                dict_by_inst_list.append(dict_by_inst)
        return self._collect_at_inst(dict_by_inst_list, min_needed, dups)
    
    def _collect_at_id_unique(self, dict_by_id_list, min_needed, dups):
        ''' Collect at id level -- with unique ids ''' 
        # Input is a list of dict_by_id that we have to pick from
        # If there is only one, then we pick from that one (it wasn't unique above us)
        #  Call down with a list of each perm of dicts by instance (contained dict)
        tmp_events = []
        if len(dict_by_id_list) == 1:
            tmp_dict_by_id = dict_by_id_list[0]
            if len(tmp_dict_by_id.keys()) >= min_needed:
                for t_ids in itertools.combinations(tmp_dict_by_id.keys(), min_needed):
                    tmp_dict_by_inst_list = [tmp_dict_by_id[t_id] for t_id in t_ids]
                    tmp_events.extend(self._collect_at_inst(tmp_dict_by_inst_list, min_needed, dups))
        else:
            # It was unique above us so we'll get min_needed entries in the dict and have
            # to look at combinations over that
            tmp_ids_list_list = [t_dict.keys() for t_dict in dict_by_id_list]
            for ids_prod in itertools.product(*tmp_ids_list_list):
                if len(set(ids_prod)) < min_needed:
                    # Must all be unique
                    continue
                tmp_dict_by_inst_list = [dict_by_id_list[t_idx][t_id] for t_idx, t_id in enumerate(ids_prod)]
                tmp_events.extend(self._collect_at_inst(tmp_dict_by_inst_list, min_needed, dups))
        return tmp_events    
            
    # Collect at instance level
    def _collect_at_inst(self, dict_by_inst_list, min_needed, dups):
        ''' Collect at instance level -- default is to ignore '''
        tmp_events = []
        for dict_by_inst in dict_by_inst_list:
            for e_list in dict_by_inst.values():
                tmp_events.extend(e_list)
        return tmp_events
      
    def _collect_at_inst_unique(self, dict_by_inst_list, min_needed, dups):
        ''' Collect at instance level when unique instances are required ''' 
        # Collect into one dictionary
        dict_by_inst = defaultdict(list)
        for t_dict in dict_by_inst_list:
            for t_key, t_list in t_dict.items():
                dict_by_inst[t_key].extend(t_list)
        return _perm_checker(dict_by_inst, min_needed, dups)
              
    def _collect_at_inst_comp(self, dict_by_inst_list, min_needed, dups):
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
    
    def __str__(self):
        return _print_events_struct(self.events)
    
    def _state_str(self, excluded):
        return _print_events_struct_with_summary(self.events, excluded=excluded, verbose=(self.condition.ruleset.gear_rule_debug == 'V'))
    
# HELPER
def _print_events_struct(events, title=''):
    ''' print the events structure '''
    outstr = title + '\n'
    for loc_k, loc_v in events.items():
        outstr += '  ' + str(loc_k) +'\n'
        for id_k, id_v in loc_v.items():
            outstr += '    ' + str(id_k) + '\n'
            if len(id_v) == 0:
                outstr += '        -empty\n'
            else:
                for inst_k, inst_v in id_v.items():
                    outstr += '      ' + str(inst_k) + '\n'
                    if inst_v is not None:
                        outstr += '          ' + ','.join([e.brief_str() for e in inst_v]) + '\n'
                    else:
                        outstr += '          ' + '-empty-\n'
    return outstr

def _perm_checker(in_dict, num, dups): 
    ''' Check the in_dict to see if num keys can be choosen such that each has a unique event.
        A max of dups duplicate entries are allowed. 
        
        msg is only for debugging
        
        This could have been done using bute force:
            found = False
            for keycomb in itertools.combinations(dict_by_inst.keys(), min_needed):
                t_lists = [dict_by_inst[k] for k in keycomb]
                for eventprod in itertools.product(*t_lists):
                    p rint str([e.brief_str() for e in eventprod])
                    if len(set(eventprod)) >= min_needed:
                        found = True
                        break
            if found == False:
                p rint "DONE ... dind't find"
                return []
                
        However this method takes advantage of tree pruning to dramatically reduce the perms checked.

    ''' 
    key_start_idx = 0
    key_idx = 0
    used_events = []
    key_list = in_dict.keys()
    event_idx_list = [None] * len(key_list)
    
#    if msg:
#        p rint 
#        p rint 'key_list = ' + str(key_list)
#        p rint 'num = ' + str(num)
    if len(key_list) < num:
#        if msg:
#            p rint 'NOT ENOUGH keys'
        return []
    
    result_set = set()
    # Collect all the events
    for t_list in in_dict.values():
        result_set.update(t_list)
    if len(result_set) < num:
#        if msg:
#            p rint "NOT ENOUGH events"
        return []
    
    if dups == 1 or len(key_list) >= ((num - 1) * dups) + 1:
        # Either enough because without duplicates passing the earlier check that there was enough 
        # keys is sufficient OR even with worst case duplication there are enough to be assured true
#        if msg:
#            p rint 'NO dupes or MORE than enough'
        return list(result_set)
           
    found = None
    adding_key = True
    while True:
#        if msg:
#            p rint '  used_events = ' + str(used_events)
#            p rint '  key_idx = ' + str(key_idx)
#            p rint '  key_start_idx = ' + str(key_start_idx)
#            p rint '  event_idx_list = ' + str(event_idx_list)
        if adding_key == True:
            # Adding keys so see if we have enough left to continue adding 
            if (key_idx + key_start_idx + (num -len(used_events))) > len(key_list):
                adding_key = False 
                key_idx -= 1 
        else:
            # Removing keys so see if we got back to the start 
            if key_idx < key_start_idx:
                key_start_idx += 1
                key_idx = key_start_idx
                #p rint 'MOVING START! ' + str(num) + '   ' + str(key_start_idx)
                # See if enough left to continue 
                if (key_start_idx + num) > len(key_list):
                    found = False
                    break 
            
        if adding_key == True:
            # process adding this key
            work_list = in_dict[key_list[key_idx]]
            work_idx = event_idx_list[key_idx]
            
            if work_idx is None:
                # Haven't had one yet 
                work_idx = 0
            else:
                # need to start checking with next one 
                work_idx += 1 
            
            # Find the next one we can use ... until we run out 
            while work_idx < len(work_list) and work_list[work_idx] in used_events:
                work_idx += 1
                
            if work_idx == len(work_list):
                # We ran out
                event_idx_list[key_idx] = None   # in case we had one 
                key_idx += 1 
            else:
                # We found one
                if len(used_events) + 1 == num:
                    found = True
#                    if msg:
#                        used_events.append(work_list[work_idx]) # removed in production PRINT
#                        p rint '    FOUND used_events = ' + str(used_events)
                    break 
                used_events.append(work_list[work_idx])
                event_idx_list[key_idx] = work_idx
                key_idx += 1 

        else:
            # Process removing this key
            if event_idx_list[key_idx] is None:
                # Not used
                key_idx -= 1  
            else:
#                if used_events[-1] != in_dict[key_list[key_idx]][event_idx_list[key_idx]]:
#                    p rint "!!!!!! something is wrong.  Expected to remove " + str(in_dict[key_list[key_idx]][event_idx_list[key_idx]]) + ' but removing ' + str(used_events[-1])
                del used_events[-1]
                adding_key = True
                # Process this key again, because there are more 
    
    if found == False:
#        if msg:
#            p rint 'IT WAS NOT NOT NOT found'
        return []
    
#    if msg:
#        p rint 'It was FOUND FOUND '
    return list(result_set)

def _print_events_struct_with_summary(ievents, title=None, excluded=None, verbose=False):
    ''' print the events structure '''
    prt_events = _compress_events_struct(ievents)
    if excluded is None:
        ck_exclude = []
    else:
        ck_exclude = excluded
    if title is not None:
        outstr = title + '\n'
    else:
        outstr = ''
    
    # Zero totals 
    c_all_events_incl = 0
    c_all_events_excl = 0
    c_mlo_keys_incl = 0
    c_mlo_keys_excl = 0

    for loc_k, loc_v in prt_events.items():
        # Location match entries
        c_mlo_events_incl = 0
        c_mlo_events_excl = 0
        c_id_keys_incl = 0
        c_id_keys_excl = 0  
        
        outstr += '  ' + str(loc_k) +'\n'
        for id_k, id_v in loc_v.items():
            # Id entries 
            c_id_events_incl = 0
            c_id_events_excl = 0 
            c_inst_keys_incl = 0 
            c_inst_keys_excl = 0 
            
            if id_k is not None or verbose == True:
                outstr += '    ' + str(id_k) + '\n'
            if len(id_v) == 0:
                outstr += '        -empty\n'
            else:
                for inst_k, inst_v in id_v.items():
                    # Instance entries 
                    c_inst_events_incl = 0 
                    c_inst_events_excl = 0 
                    if inst_k is not None or verbose == True:
                        outstr += '      ' + str(inst_k) + '\n'
                    if inst_v is not None:
                        exl_list = []
                        rest = []
                        for e in inst_v:
                            # Events in lists 
                            if e in ck_exclude:
                                exl_list.append(e)
                            else:
                                rest.append(e)
                            # Update counts
                        if len(exl_list) != 0 or (verbose == True and excluded is not None):
                            outstr += '          suppressed: '
                            outstr += str(len(exl_list)) + '> '
                            outstr += ','.join([e.brief_str() for e in exl_list]) + '\n'
                        if len(rest) != 0 or verbose == True:
                            outstr += '          ' 
                            outstr += str(len(rest)) + '> '
                            outstr += ','.join([e.brief_str() for e in rest]) + '\n'
                        c_inst_events_incl += len(rest)
                        c_inst_events_excl += len(exl_list)
                        c_id_events_incl += len(rest)
                        c_id_events_excl += len(exl_list)
                        c_mlo_events_incl += len(rest)
                        c_mlo_events_excl += len(exl_list)
                        c_all_events_incl += len(rest)
                        c_all_events_excl += len(exl_list)
                    else:
                        outstr += '          ' + '-empty-\n'
                    if c_inst_events_incl != 0:
                        c_inst_keys_incl += 1
                    else:
                        c_inst_keys_excl += 1
            if (id_v.keys()[0] is not None and (c_id_events_incl + c_id_events_excl) > 4) or verbose == True:
                if excluded is None:
                    outstr += '      SUMMARY instances: total = {0}'.format(c_inst_keys_incl)
                    outstr += '  events: total = {0}'.format(c_id_events_incl)
                else:
                    outstr += '      SUMMARY instances: total = {0} included = {1}  suppressed = {2}'.format(c_inst_keys_incl + c_inst_keys_excl, c_inst_keys_incl, c_inst_keys_excl)
                    outstr += '  events: total = {0} included = {1}  suppressed = {2}'.format(c_id_events_incl + c_id_events_excl, c_id_events_incl, c_id_events_excl)
                outstr +='\n'  
            if c_inst_keys_incl != 0:
                c_id_keys_incl += 1
            else: 
                c_id_keys_excl += 1
        if (loc_v.keys()[0] is not None and (c_mlo_events_incl + c_mlo_events_excl) > 4) or verbose == True:
            if excluded is None:
                outstr += '    SUMMARY ids: total = {0}'.format(c_id_keys_incl)
                outstr += '  events: total = {0}'.format(c_mlo_events_incl)
            else:
                outstr += '    SUMMARY ids: total = {0} included = {1}  suppressed = {2}'.format(c_id_keys_incl + c_id_keys_excl, c_id_keys_incl, c_id_keys_excl)
                outstr += '  events: total = {0} included = {1}  suppressed = {2}'.format(c_mlo_events_incl + c_mlo_events_excl, c_mlo_events_incl, c_mlo_events_excl)
            outstr +='\n' 
        if c_id_keys_incl != 0:
            c_mlo_keys_incl += 1
        else:
            c_mlo_keys_excl += 1 
    if excluded is None:
        outstr += '  SUMMARY matched locs: total = {0}'.format(c_mlo_keys_incl)
        outstr += '  events: total = {0}'.format(c_all_events_incl)
    else:
        outstr += '  SUMMARY matched locs: total = {0} included = {1}  suppressed = {2}'.format(c_mlo_keys_incl + c_mlo_keys_excl, c_mlo_keys_incl, c_mlo_keys_excl)
        outstr += '  events: total = {0} included = {1}  suppressed = {2}'.format(c_all_events_incl + c_all_events_excl, c_all_events_incl, c_all_events_excl)
    outstr +='\n'  
    return outstr

def _compress_events_struct(events):
    ''' print the events structure '''
    new_events = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
    for loc_k, loc_v in events.items():
        for id_k, id_v in loc_v.items():
            if len(id_v) != 0:
                for inst_k, inst_v in id_v.items():
                    if inst_v is not None and len(inst_v) != 0:
                        new_events[loc_k][id_k][inst_k] = inst_v
    return new_events
         
