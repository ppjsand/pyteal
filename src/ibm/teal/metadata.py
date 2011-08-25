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

import os
from ibm.teal.constants import EVENT_LIMIT_ATTR_EVENT_ID, ALERT_LIMIT_ATTR_ALERT_ID
from ibm.teal.registry import get_logger, get_service, TEAL_DATA_DIR
from ibm.teal.teal_error import XMLParsingError, ConfigurationError
from xml.etree import ElementTree

META_TYPE_EVENT = 'event'
META_TYPE_ALERT = 'alert'

META_EVENT_ID = 'id'
META_EVENT_COMP = 'comp'
META_EVENT_MSG = 'message'
META_EVENT_DESCRIPTION = 'description'

META_ALERT_ID = 'id'
META_ALERT_MSG_TEMPLATE = 'msg_template'
META_ALERT_RECOMMENDATION = 'recommendation'
META_ALERT_URGENCY = 'urgency'
META_ALERT_SEVERITY = 'severity'
META_ALERT_CALL_HOME = 'call_home'
META_ALERT_CUST_NOTIFICATION = 'cust_notification'
META_ALERT_FRU_CLASS = 'fru_class'
META_ALERT_FRU_LIST = 'fru_list'
META_ALERT_DESCRIPTION = 'description'
META_ALERT_PRIORITY = 'priority'

META_ALERT_SEVERITY_VALUES = ['F','E','W','I']
META_ALERT_URGENCY_VALUES = ['I','S','N','D','O']


class Metadata(dict):
    '''
    Dictionary of event metadata
    '''

    def __init__(self, type, xmlfiles):
        '''
        Load the list of specified xml files and register
        '''
        get_logger().debug('Creating {0} Metadata Service'.format(type))
        dict.__init__(self)
        if type == META_TYPE_EVENT or type == META_TYPE_ALERT:
            self.type = type   
        else:
            raise ConfigurationError('Unrecognized metadata type: {0}'.format(type))
        self.add_files(xmlfiles)
        return
        
    def add_files(self, xmlfiles, use_data_dir=True):
        if use_data_dir: 
            data_dir = get_service(TEAL_DATA_DIR)     
        for file in xmlfiles:
            if use_data_dir:
                xml_file = os.path.join(data_dir, file.strip())
            else:
                xml_file = file
            self.parse_file(xml_file)
        return
        
    def parse_file(self, file):
        '''Parse the xml metadata file
        '''
        get_logger().debug('parsing file %s', file)
        xmldoc = ElementTree.parse(file)
        top_elem = xmldoc.getroot()
        for meta_entry in top_elem:
            entry_name = meta_entry.tag.split('}')[-1]
            if entry_name != self.type:
                raise XMLParsingError('{0} metadata file {1} error: unexpected element {2}'.format(self.type, file, entry_name))
            if 'id' not in meta_entry.attrib:
                raise XMLParsingError('{0} metadata file {1} error: element does not have id attribute'.format(self.type, file)) 
            meta_id = meta_entry.attrib['id']
            if meta_id in self:
                get_logger().warning('Duplicate metadata, ignoring entry in file {0}'.format(file))
                continue
            else:
                pass
                #get_logger().debug('Found entry {0}'.format(meta_id))
            if self.type == META_TYPE_EVENT:
                if 'comp' not in meta_entry.attrib:
                    raise XMLParsingError('{0} metadata file {1} error: element does not have comp attribute'.format(self.type, file)) 
                meta_comp = meta_entry.attrib['comp']
                meta = MetadataEvent(meta_comp, meta_id)
                key = (meta_comp, meta_id)
            else:
                # Know it is alert because we validated
                meta = MetadataAlert(meta_id)
                key = meta_id
            for event_child in meta_entry:
                child_name = event_child.tag.split('}')[-1]
                child_data = event_child.text  
                meta.update_entry(child_name, child_data)
            meta.check_validity()
            self[key] = meta
        return
        
        
class MetadataEvent(dict):
    '''Individual event metadata
    
       Access attributes directly.
       See xsd for field descriptions
    '''

    def __init__(self, comp, id):
        '''Construct the event metadata from the id and set 
        '''
        dict.__init__(self)
        self[META_EVENT_ID] = id
        self[META_EVENT_COMP] = comp
        self[META_EVENT_MSG] = None
        self[META_EVENT_DESCRIPTION] = None
        return
    
    def update_entry(self, key, value):
        '''Update the entry ... if entry for key donesn't exist then fail'''
        if (key in self):
            self[key] = value
            # Note adding non-string types might require transformation
        else:
            raise XMLParsingError('Event metadata file {0} error: unexpected element {1}'.format(file, key))
        return
        
    def check_validity(self):
        '''Make sure all of the required fields were specified
        '''
        if len(self[META_EVENT_ID]) > EVENT_LIMIT_ATTR_EVENT_ID:
            raise XMLParsingError('Event metadata file error: event id larger than {0} characters: {1} is length {2}'.format(EVENT_LIMIT_ATTR_EVENT_ID, self[META_EVENT_ID],len(self[META_EVENT_ID])))
        if self[META_EVENT_MSG] is None:
            raise XMLParsingError('Event metadata file error: missing message element')
        return    
    
    
class MetadataAlert(dict):
    '''Individual event metadata
    
       Access attributes directly.
       See xsd for field descriptions
    '''

    def __init__(self, id):
        '''Construct the event metadata from the id and set 
        '''
        dict.__init__(self)
        # Required
        self[META_ALERT_ID] = id
        self[META_ALERT_MSG_TEMPLATE] = None
        self[META_ALERT_RECOMMENDATION] = None
        self[META_ALERT_URGENCY] = None
        self[META_ALERT_SEVERITY] = None
        # Optional
        self[META_ALERT_CALL_HOME] = 'N'
        self[META_ALERT_CUST_NOTIFICATION] = 'N'
        self[META_ALERT_FRU_CLASS] = None
        self[META_ALERT_FRU_LIST] = None
        self[META_ALERT_DESCRIPTION] = None
        self[META_ALERT_PRIORITY] = None
        return
    
    def update_entry(self, key, value):
        '''Update the entry ... if entry for key does not exist then fail'''
        if (key in self):
            if key == META_ALERT_PRIORITY:
                self[key] = int(value)
            else:
                self[key] = value
        else:
            raise XMLParsingError('Alert metadata file {0} error: unexpected element {1}'.format(file, key))
        return
        
    def check_validity(self):
        '''Make sure all of the required fields were specified
        '''
        if len(self[META_ALERT_ID]) > ALERT_LIMIT_ATTR_ALERT_ID:
            raise XMLParsingError('Alert metadata file error: alert id larger than {0} characters: {1} is length {2}'.format(ALERT_LIMIT_ATTR_ALERT_ID, self[META_ALERT_ID],len(self[META_ALERT_ID])))
        if self[META_ALERT_MSG_TEMPLATE] is None:
            raise XMLParsingError('Alert metadata file error: missing message template element')
        if self[META_ALERT_RECOMMENDATION] is None:
            raise XMLParsingError('Alert metadata file error: missing recommendation element')
        if self[META_ALERT_URGENCY] is None:
            raise XMLParsingError('Alert metadata file error: missing urgency element')
        if self[META_ALERT_URGENCY] not in META_ALERT_URGENCY_VALUES:
            raise XMLParsingError('Alert metadata file error: invalid urgency value: {0}'.format(self[META_ALERT_URGENCY]))
        if self[META_ALERT_SEVERITY] is None:
            raise XMLParsingError('Alert metadata file error: missing severity element')
        if self[META_ALERT_SEVERITY] not in META_ALERT_SEVERITY_VALUES:
            raise XMLParsingError('Alert metadata file error: invalid severity value: {0}'.format(self[META_ALERT_SEVERITY]))
        return

