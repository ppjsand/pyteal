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

from ibm.teal.registry import get_logger, get_service, SERVICE_ALERT_METADATA,\
    SERVICE_ALERT_MGR, SERVICE_LOCATION
from ibm.teal.analyzer.gear.rule_value import GRVA_TYPE_ANY, GRVA_TYPE_LOC,\
    GRVA_TYPE_SCOPE, GRVA_TYPE_BOOLEAN, GRVA_TYPE_STRING, init_rule_values,\
    read_from_xml_rule_value, resolve_and_validate_rule_values,\
    GRVA_TYPE_NONZERO_UINT
from ibm.teal.analyzer.gear.common import GRUL_PART_ACTION
from ibm.teal.teal_error import XMLParsingError
from ibm.teal.analyzer.gear.control import GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS
from ibm.teal.analyzer.gear.external_base_classes import ExtInitAlert,\
    ExtFatalError
import sys
from ibm.teal.alert import ALERT_ATTR_SRC_NAME, ALERT_ATTR_ALERT_ID,\
    ALERT_ATTR_SEVERITY, ALERT_ATTR_URGENCY, ALERT_ATTR_FRU_LOC,\
    ALERT_ATTR_RECOMMENDATION, ALERT_ATTR_RAW_DATA, ALERT_ATTR_MSG_TEMPLATE,\
    ALERT_ATTR_PRIORITY, ALERT_ATTR_CONDITION_EVENTS, ALERT_ATTR_EVENT_LOC,\
    ALERT_ATTR_EVENT_LOC_TYPE, dict2raw_data
    
#     Entries in bottom dictionary are var name: (type, init_str, required, static_only)
GEHD_HANDLER_ALERT =  {
       'alert_id':        (GRVA_TYPE_ANY, None, True, True),
       'severity':        (GRVA_TYPE_ANY, None, False, True),
       'urgency':         (GRVA_TYPE_ANY, None, False, True),
       'event_loc':       (GRVA_TYPE_LOC, None, False, True),
       'event_loc_scope': (GRVA_TYPE_SCOPE, None, False, True),
       'recommendation':  (GRVA_TYPE_ANY, None, False, True),
       # reason is not supported because generated from msg_template
       'msg_template':    (GRVA_TYPE_ANY, None, False, True),
       'fru_loc':         (GRVA_TYPE_ANY, None, False, True),
       'raw_data':        (GRVA_TYPE_ANY, None, False, True),
       'use_metadata':    (GRVA_TYPE_BOOLEAN, 'true', False, True),
       'init_class':      (GRVA_TYPE_STRING, None, False, True),
       'priority':        (GRVA_TYPE_NONZERO_UINT, None, False, False),                                        'scope': (GRVA_TYPE_SCOPE, False, False), 
       'type':            (GRVA_TYPE_STRING, None, True, True)
                         }

class GearErrorHandlers(object):
    ''' Base class for GEAR engines '''
    
    def __init__(self, ruleset):
        ''' Initialize the context '''
        self.trace_id = (0, 'error handlers')
        self.ruleset = ruleset
        self.loc_handler = None        return

    def read_from_xml_element(self, event_entry, trace_dict):
        ''' Read the error handler from the xml '''
        new_handler = GearErrorHandler(event_entry, trace_dict, self.ruleset)
        new_handler.resolve_and_validate()
        if new_handler.type.get_value() != 'location':
            self.ruleset.parse_error(new_handler.trace_id[0], '\'on_error\' element only supports a type of \'location\'')
        if self.loc_handler is not None:
            self.ruleset.parse_error(new_handler.trace_id[0], '\'on_error\' element with a type of \'location\' can only be specified once')
        self.loc_handler = new_handler
        return
    
    def resolve_and_validate(self):
        # Nothing to do ... done as read in
        return
    
    def check_locations(self):
        ''' Should locations be checked? '''
        return self.loc_handler is not None
    
    def location_error(self, event, location):
        ''' Handle a location error '''
        if self.loc_handler is None:
            get_logger().debug('No location error handler.  Raise the exception')
            location._UNPROCESSABLE()
        self.loc_handler.create_alert(event, location)
        return
        
        
class GearErrorHandler(object):
    ''' Create a handler that creates an alert '''
    
    def __init__(self, xml_element, trace_dict, ruleset):
        ''' Initialize '''
        self.trace_id = (0, 'on_error') 
        self.description = None
        self.ruleset = ruleset
        
        # Initialize values
        init_rule_values(self, GEHD_HANDLER_ALERT)
        # Read the xml
        self._read_from_xml(xml_element, trace_dict)
        return
    
    def _read_from_xml(self, xml_element, trace_dict):
        ''' Read in the hanlder alert from the input XML
        '''
        self.trace_id = trace_dict[xml_element]
        # attributes
        for att_key in xml_element.attrib:
            att_value = xml_element.attrib[att_key]
            if read_from_xml_rule_value(self, att_key, att_value, GEHD_HANDLER_ALERT):
                continue
            else:
                self.ruleset.parse_error(self.trace_id[0], '\'on_error\' element encountered an unexpected attribute \'{1}\''.format(att_key))
        # elements
        # Get description ... if specified
        for rule_element in xml_element:
            element_name = rule_element.tag.split('}')[-1]
            element_value = rule_element.text
            if element_name == 'description':
                self.description = element_value
            else:
                self.ruleset.parse_error(self.trace_id[0], '\'on_error\' element encountered an unexpected subelement: {0}'.format(element_name))
        return
    
    def resolve_and_validate(self):
        '''Resolve and validate the evaluatable'''
        self.src_name = self.ruleset.name
        try:
            # OK to set Rule to None, since not using any of the support the requires
            resolve_and_validate_rule_values(self, self.ruleset, None, GEHD_HANDLER_ALERT, rule_part=GRUL_PART_ACTION)
        except XMLParsingError as e:
            self.ruleset.parse_error(self.trace_id[0], '\'on_error\' element {0}'.format(e.msg))
            
        self.trace_id = (self.trace_id[0], self.trace_id[1] + '-' + self.type.get_value())
        
        # Process init class
        if self.init_class.is_set() == False:
            self.init_class_callable = self.ruleset['gear_control'][GCTL_DEFAULT_CREATE_ALERT_INIT_CLASS]
        else:
            try:
                module_name, class_name = self.init_class.get_value().rsplit('.', 1)
                module = __import__(module_name, globals(), locals(), [class_name])
            except ImportError, ie:
                get_logger().error(ie)
                self.ruleset.parse_error(self.trace_id[0], 'gear create alert unable to load specified init class: {0}'.format(self.init_class))
                raise ie
            self.init_class_callable = getattr(module, class_name)
            
            tmp_instance = self.init_class_callable()
            if isinstance(tmp_instance, ExtInitAlert) == False:
                self.ruleset.parse_error(self.trace_id[0], 'create_alert element init class must be a subclass of ExtInitAlert')

        # validate
        # if using metadata, make sure id has metadata
        if self.use_metadata.get_value() == True:
            try:
                metadata = get_service(SERVICE_ALERT_METADATA)
            except:
                metadata = None
            if metadata is None or len(metadata) == 0:
                self.ruleset.parse_error(self.trace_id[0], 'create_alert element alert id validation failed trying to retrieve the alert metadata')
            try:
                tmp_value = self.alert_id.get_value()
            except:
                # Happens if can't get a value from the alert_id (GEAR variable case)
                get_logger().debug('Exception checking alert id {0}: {1}'.format(self.alert_id.in_str,str(sys.exc_info()[0])))
                tmp_value = None
            if tmp_value is not None and tmp_value not in metadata:
                    self.ruleset.parse_error(self.trace_id[0], 'create_alert element alert id {0} does not have metadata'.format(self.alert_id.get_value()))
        elif not (self.severity.is_set() and self.urgency.is_set() and self.recommendation.is_set() and self.msg_template.is_set()):
            self.ruleset.parse_error(self.trace_id[0],'create_alert element requires msg_template, recommendation, severity, and urgency when use_metadata is false')

        return
    
    def create_alert(self, event, location):
        ''' create the alert '''
        # Populate the dictionary
        alert_dict = {}
        alert_dict[ALERT_ATTR_SRC_NAME] = self.src_name
        alert_dict[ALERT_ATTR_ALERT_ID] = self.alert_id.get_value()
        if self.severity.is_set():
            alert_dict[ALERT_ATTR_SEVERITY] = self.severity.get_value()
        if self.urgency.is_set():
            alert_dict[ALERT_ATTR_URGENCY] = self.urgency.get_value()
        if self.fru_loc.is_set():
            alert_dict[ALERT_ATTR_FRU_LOC] = self.fru_loc.get_value()
        if self.recommendation.is_set():
            alert_dict[ALERT_ATTR_RECOMMENDATION] = self.recommendation.get_value()
        if self.raw_data.is_set():
            alert_dict[ALERT_ATTR_RAW_DATA] = self.raw_data.get_value()
        if self.msg_template.is_set():
            alert_dict[ALERT_ATTR_MSG_TEMPLATE] = self.msg_template.get_value()
        if self.priority.is_set():
            alert_dict[ALERT_ATTR_PRIORITY] = self.priority.get_value()
        alert_dict[ALERT_ATTR_CONDITION_EVENTS] = set([event])
        
        if self.event_loc.is_set():
            loc = self.event_loc.get_value()
        else:
            loc = get_service(SERVICE_LOCATION).get_teal_location(self.ruleset.name)
        alert_dict[ALERT_ATTR_EVENT_LOC] = loc.get_location()
        alert_dict[ALERT_ATTR_EVENT_LOC_TYPE] = loc.get_id()
        
        # Fill in raw data
        raw_data_dict = {}
        raw_data_dict['exception'] = '{0}: {1}'.format(str(location.ex_type), str(location.ex_value))
        alert_dict[ALERT_ATTR_RAW_DATA] = dict2raw_data(raw_data_dict)
        
        # Call init routine if specified 
        if self.init_class_callable is not None:
            try:
                alert_dict = self.init_class_callable().update_init_data_main(alert_dict)
            except ExtFatalError:
                get_logger().exception('FATAL ERROR raised --> kill analyzer')
                raise
            except:
                self.ruleset.trace_error(self.trace_id[1], 'Error in update_init_data_main')
                get_logger().exception('')

        # Allocate the potential alert 
        amgr = get_service(SERVICE_ALERT_MGR)
        alert = amgr.allocate(self.alert_id.get_value(), alert_dict)
        # send the alert to the delivery queue
        get_logger().debug('  creating {0}'.format(str(alert)))
        amgr.commit(alert)
        self.ruleset.send_alert(alert)
        return
    