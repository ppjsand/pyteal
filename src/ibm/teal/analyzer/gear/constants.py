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

from ibm.teal.registry import get_logger
from ibm.teal.constants import EVENT_LIMIT_ATTR_EVENT_ID #, ALERT_LIMIT_ATTR_ALERT_ID

GCON_EVENT_ID = 'event_id'
#GCON_ALERT_ID = 'alert_id'
GCON_EVENT_ID_SET = 'set_of_event_ids'
#GCON_ALERT_ID_SET = 'set_of_alert_ids'


class GearConstants(dict):
    '''
    Dictionary of GEAR constants by type
    '''

    def __init__(self, ruleset):
        '''
        Constructor
        create my parent and init to no constants
        '''
        dict.__init__(self)
        self.ruleset = ruleset
        self[GCON_EVENT_ID] = {}
        #self[GCON_ALERT_ID] = {}
        self[GCON_EVENT_ID_SET] = {}
        #self[GCON_ALERT_ID_SET] = {}
        self.trace_id = (0, 'constants')
        return
    
    def add_constants(self, type, add_dict):
        '''Add constants to the appropriate type dictionary'''
        if type not in self:
            get_logger().warning('type not in constants: {0}'.format(type))
        for const_key in add_dict:
            if const_key in self[type]:
                get_logger().warning('Type {0} constant {1} already defined -- ignoring'.format(type, const_key))
            else:
                self[type][const_key] = add_dict[const_key]
        return
    
    def add_constants_xml(self, xml_constants_element, trace_dict):
        '''Add event info defined in an XML events element'''
        self.trace_id = trace_dict[xml_constants_element]
        found_const_element = False
        for event_entry in xml_constants_element:
            entry_name = event_entry.tag.split('}')[-1]
            if entry_name != 'constant':
                self.ruleset.parse_error(self.trace_id[0], 'constant processing encountered an unexpected element {0}'.format(entry_name))
            found_const_element = True
            if 'name' not in event_entry.attrib:
                self.ruleset.parse_error(self.trace_id[0], 'constant name must be specified')
            name = event_entry.attrib['name'].strip()
            if len(name) == 0:
                self.ruleset.parse_error(self.trace_id[0], 'constant name must be at least one character')
            if 'type' not in event_entry.attrib:
                self.ruleset.parse_error(self.trace_id[0], 'constant type must be specified')
            type = event_entry.attrib['type'].strip()
            if len(type) == 0:
                self.ruleset.parse_error(self.trace_id[0], 'constant type must be at valid value')
            if 'value' not in event_entry.attrib:
                self.ruleset.parse_error(self.trace_id[0], 'constant value must be specified')
            value = event_entry.attrib['value'].strip()
            if len(value) == 0:
                self.ruleset.parse_error(self.trace_id[0], 'constant \'{0}\' value must be at least one character'.format(name))             
            if type == GCON_EVENT_ID:
                if not self.ruleset.event_input:
                    self.ruleset.parse_error(self.trace_id[0], 'gear constant element type \'{0}\' is not supported for this analyzer'.format(GCON_EVENT_ID))
                if name in self[type]:
                    self.ruleset.parse_error(self.trace_id[0], 'duplicate definition for event id constant \'{0}\''.format(name))
                self[type][name] = value
#            elif type == GCON_ALERT_ID:
#                if not self.ruleset.supports_alerts:
#                    self.ruleset.parse_error(self.trace_id[0], 'gear constant element type \'{0}\' is not supported for this analyzer'.format(GCON_ALERT_ID))
#                if name in self[type]:
#                    self.ruleset.parse_error(self.trace_id[0], 'duplicate definition for alert id constant \'{0}\''.format(name))
#                self[type][name] = value
            elif type == GCON_EVENT_ID_SET:
                if not self.ruleset.event_input:
                    self.ruleset.parse_error(self.trace_id[0], 'gear constant element type \'{0}\' is not supported for this analyzer'.format(GCON_EVENT_ID_SET))
                if name in self[type]:
                    self.ruleset.parse_error(self.trace_id[0], 'duplicate definition for event id set constant \'{0}\''.format(name))
                tmp_set = set(value.split(','))
                self[type][name] = set()
                for item in tmp_set:
                    item = item.strip()
                    if len(item) == 0:
                        self.ruleset.parse_error(self.trace_id[0], 'event id in constant set \'{0}\' has a length of zero'.format(name))
                    # Can't check for > 8, because could be const
                    self[type][name].add(item)
#            elif type == GCON_ALERT_ID_SET:
#                if not self.ruleset.supports_alerts:
#                    self.ruleset.parse_error(self.trace_id[0], 'gear constant element type \'{0}\' is not supported for this analyzer'.format(GCON_ALERT_ID_SET))
#                if name in self[type]:
#                    self.ruleset.parse_error(self.trace_id[0], 'duplicate definition for alert id set constant \'{0}\''.format(name))
#                tmp_set = set(value.split(','))
#                self[type][name] = set()
#                for item in tmp_set:
#                    item = item.strip()
#                    if len(item) == 0:
#                        self.ruleset.parse_error(self.trace_id[0], 'alert id in constant set \'{0}\' has a length of zero'.format(name))
#                    # Can't check for > 8, because could be const
#                    self[type][name].add(item)
            else:
                self.ruleset.parse_error(self.trace_id[0], 'unexpected constant type \'{0}\''.format(type))
        if found_const_element == False:
            self.ruleset.parse_error(self.trace_id[0], 'no constant elements specified in \'constants\' element')            
        return
    
    def resolve_and_validate(self):
        '''Goes through the alert_id_set and event_id_set and converts constants to
        actual values and removes duplicates that this causes.  It also ensures that the 
        resulting event ids and alert ids are not larger than 8 characters '''
        # TODO: Validate that each id we end up with has an entry in the analysis info!
        get_logger().debug('Process event ids')
        for set_entry_key in self[GCON_EVENT_ID]:
            set_entry = self[GCON_EVENT_ID][set_entry_key]
            if len(set_entry) > EVENT_LIMIT_ATTR_EVENT_ID:
                get_logger().warning('Event id {0} associated with constant {1} is too large'.format(set_entry, set_entry_key))
                # TODO: Should we fail?
                
#        get_logger().debug('Process alert ids')
#        for set_entry_key in self[GCON_ALERT_ID]:
#            set_entry = self[GCON_ALERT_ID][set_entry_key]
#            if len(set_entry) > ALERT_LIMIT_ATTR_ALERT_ID:
#                get_logger().warning('Alert id {0} associated with constant {1} is too large'.format(set_entry, set_entry_key))
#                # TODO: Should we fail?
                
        get_logger().debug('Process event id sets')
        for set_entry_key in self[GCON_EVENT_ID_SET]:
            self[GCON_EVENT_ID_SET][set_entry_key] = self.resolve_id_set_constants(self[GCON_EVENT_ID_SET][set_entry_key], GCON_EVENT_ID, set_entry_key)
            
#        get_logger().debug('Process alert id sets')
#        for set_entry_key in self[GCON_ALERT_ID_SET]:
#            self[GCON_ALERT_ID_SET][set_entry_key] = self.resolve_id_set_constants(self[GCON_ALERT_ID_SET][set_entry_key], GCON_ALERT_ID, set_entry_key)
#        return
    
    def resolve_id_set_constants(self, id_set, single_type, set_entry_key=None):
        ''' Given a set return a set that is resolved '''
        new_set = set()
        already_used = set()
        if set_entry_key is not None:
            already_used.add(set_entry_key)
        if single_type == GCON_EVENT_ID:
            set_type = GCON_EVENT_ID_SET
#        else:
#            set_type = GCON_ALERT_ID_SET
        for id in id_set:
            new_set = self._resolve_set_constant(id, new_set, already_used, single_type, set_type)
        return new_set    
            
    def _resolve_set_constant(self, constant, current_set, in_already_used, single_type, set_type):
        ''' Recursive routine to resolve constants 
        Handles constant list of constant lists '''
        if current_set is None:
            current_set = set()
        if in_already_used is None:
            already_used = set()
        else:
            already_used = in_already_used.copy()
        if constant in already_used:
            self.ruleset.parse_error(self.trace_id[0], 'circular dependency for constant \'{0}\''.format(constant))
        if constant in current_set:
            return current_set
        new_constant = self.get_constant(constant, single_type)
        if new_constant != constant:
            current_set.add(new_constant)
            return current_set
        new_constant = self.get_constant(constant, set_type)
        if new_constant == constant:
            current_set.add(new_constant)
            return current_set
        else:
            already_used.add(constant)
        for item in new_constant:
            if item in current_set:
                continue
            current_set = self._resolve_set_constant(item, current_set, already_used, single_type, set_type)
        return current_set
        
    def get_constant(self, value, type):
        '''Given the value it resolves it to what it is currently defined as
        in the constants table.  If there is no definition, then it returns
        the value 
        
        Note this assumes that sets have been resolved after initial loading
        '''
        if type == GCON_EVENT_ID:
            if value in self[GCON_EVENT_ID]:
                get_logger().debug('replacing {0} with event const {1}' .format(value, self[GCON_EVENT_ID][value]))
                return self[GCON_EVENT_ID][value]
#        elif type == GCON_ALERT_ID:
#            if value in self[GCON_ALERT_ID]:
#                get_logger().debug('replacing {0} with alert const {1}'.format(value, self[GCON_ALERT_ID][value]))
#                return self[GCON_ALERT_ID][value]
        elif type == GCON_EVENT_ID_SET:
            if value in self[GCON_EVENT_ID_SET]:
                get_logger().debug('replacing {0} with event const set {1}'.format(value, str(self[GCON_EVENT_ID_SET][value])))
                return self[GCON_EVENT_ID_SET][value]
#        elif type == GCON_ALERT_ID_SET:
#            if value in self[GCON_ALERT_ID_SET]:
#                get_logger().debug('replacing {0} with alert const set {1}'.format(value, str(self[GCON_ALERT_ID_SET][value])))
#                return self[GCON_ALERT_ID_SET][value]
        else:
            get_logger().warning('unrecognized type ' + type)
        return value

        