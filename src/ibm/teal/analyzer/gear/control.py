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

import re

from ibm.teal.registry import get_logger

# Dual support
GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS = 'default_create_alert_init_class'

# Event analysis support
GCTL_DEFAULT_EVENT_COMP = 'default_event_comp'
GCTL_ANALYZE_EVENTS = 'analyze_events'

# Alert analysis support
#GCTL_ANALYZE_ALERTS = 'analyze_alerts'


class GearControl(dict):
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
        
        # Init dual
        self[GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS] = None

        # Event analysis support
        self[GCTL_DEFAULT_EVENT_COMP] = None
        self.use_event_regx = False
        # Make so if only one specified the other matches
        self.event_comp_regx_string = '.*'
        self.event_comp_regx = re.compile('.*')
        self.event_id_regx_string = '.*'
        self.event_id_regx = re.compile('.*')
        self.trace_id = (0,'Control')

        # Alert analysis support
        self.use_alert_regx = False
        self.alert_id_regx_string = '.*'
        self.alert_id_regx = re.compile('.*')
        return
    
    def read_xml(self, xml_constants_element, trace_dict):
        '''Read the GEAR control XML'''
        self.trace_id = trace_dict[xml_constants_element]
        for xml_entry in xml_constants_element:
            entry_name = xml_entry.tag.split('}')[-1]
            get_logger().debug('Processing  {0}'.format(entry_name))
            
            ## Dual support
            if entry_name == GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS:
                # supported by both, so don't need to check
                if 'class' not in xml_entry.attrib:
                    self.ruleset.parse_error(self.trace_id[0], 'default_create_alert_init_class element requires a \'class\' attribute')
                tmp_class = xml_entry.attrib['class']
                try:
                    module_name, class_name = tmp_class.rsplit('.', 1)
                    module = __import__(module_name, globals(), locals(), [class_name])
                except ImportError, ie:
                    get_logger().error(ie)
                    self.ruleset.parse_error(self.trace_id[0], 'gear control unable to load specified create alert init class: {0}'.format(tmp_class))
                    raise ie
                self[GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS] = getattr(module, class_name)
            
            ## Event analysis support
            elif entry_name == GCTL_DEFAULT_EVENT_COMP:
                if not self.ruleset.event_input:
                    self.ruleset.parse_error(self.trace_id[0], 'gear control element \'{0}\' is not supported for this analyzer'.format(GCTL_DEFAULT_EVENT_COMP))
                self[GCTL_DEFAULT_EVENT_COMP] = xml_entry.attrib['value'].strip()
                if self[GCTL_DEFAULT_EVENT_COMP] is None or len(self[GCTL_DEFAULT_EVENT_COMP]) == 0:
                    self.ruleset.parse_error(self.trace_id[0], 'gear_control element is missing \'value\' attribute')
            elif entry_name == GCTL_ANALYZE_EVENTS:
                if not self.ruleset.event_input:
                    self.ruleset.parse_error(self.trace_id[0], 'gear control element \'{0}\' is not supported for this analyzer'.format(GCTL_ANALYZE_EVENTS))
                if 'comp_regx' in xml_entry.attrib:
                    self.event_comp_regx_string = xml_entry.attrib['comp_regx']
                    self.event_comp_regx = re.compile(self.event_comp_regx_string)
                    self.use_event_regx = True
                if 'id_regx' in xml_entry.attrib:
                    self.event_id_regx_string = xml_entry.attrib['id_regx']
                    self.event_id_regx = re.compile(self.event_id_regx_string)
                    self.use_event_regx = True
                # At least one of the attributes had to be specified
                if not self.use_event_regx:
                    self.ruleset.parse_error(self.trace_id[0], 'event_spec element requires either a \'comp_regx\' or \'id_regx\' attribute')

#            ## Alert analysis support 
#            elif entry_name == GCTL_ANALYZE_ALERTS:
#                if not self.ruleset.alert_input:
#                    self.ruleset.parse_error(self.trace_id[0], 'gear control element \'{0}\' is not supported for this analyzer'.format(GCTL_ANALYZE_ALERTS))
#                if 'id_regx' in xml_entry.attrib:
#                    self.alert_id_regx_string = xml_entry.attrib['id_regx']
#                    self.alert_id_regx = re.compile(self.alert_id_regx_string)
#                    self.use_alert_regx = True
#                else:
#                    # Required attribute
#                    self.ruleset.parse_error(self.trace_id[0], 'alert_spec element requires a \'id_regx\' attribute')
            else:
                self.ruleset.parse_error(self.trace_id[0], 'gear_control element encountered an unexpected element \'{0}\''.format(entry_name))
        return
            