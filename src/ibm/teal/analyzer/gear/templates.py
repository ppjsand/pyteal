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

from ibm.teal.analyzer.gear.rule_condition import evaluatable_creator
from ibm.teal.registry import get_logger

GTPL_CONDITION = 'condition_template'
#GTPL_ACTION = 'action_template'
#GTPL_RULE = 'rule_template'


class GearTemplates(dict):
    ''' Dictionary of GEAR templates by type
    '''

    def __init__(self, context):
        ''' Create the dictionary of GEAR templates
        
            Only condition templates are supported at this point
        '''
        dict.__init__(self)
        self.context = context
        self[GTPL_CONDITION] = {}
        self.trace_id = (0, 'templates')
        return
    
    def read_from_xml(self, xml_templates_element, trace_dict):
        '''Add template info defined in an XML templates element'''
        self.trace_id = trace_dict[xml_templates_element]
        for template_entry in xml_templates_element:
            template_type = template_entry.tag.split('}')[-1]
            if template_type != GTPL_CONDITION:
                self.context.parse_error(self.trace_id[0], '\'templates\' element does not support the sub-element \'{0}\''.format(template_type))
            # Condition template -- only one currently supported 
            # Process attributes
            name = None
            for att_key in template_entry.attrib:
                att_value = template_entry.attrib[att_key]
                if att_key == 'name':
                    name = att_value.strip()
                else:
                    self.ruleset.parse_error(self.trace_id[0], '\'condition_template\' element encountered an unexpected attribute \'{0}\''.format(att_key))
            # Name was required
            if name is None:
                self.context.parse_error(self.trace_id[0], '\'condition_template\' element requires \'name\' attribute')
    
            get_logger().debug('Condition template defined with name {0}'.format(name))
                
            # Must have a contained element
            if len(template_entry) < 1:
                self.context.parse_error(self.trace_id[0], 'template must contain one and only one sub-element')
            # Put in the template dictionary
            self[GTPL_CONDITION][name] = template_entry[0]
        return
    
    def use_condition_template(self, xml_element, trace_dict, usage_context):
        ''' retrieve the specified template, apply the substitution and then 
            create the appropriate rule
        '''
        # get info from the use_template element
        if 'name' not in xml_element.attrib:
            self.usage_context.parse_error(self.trace_id[0], '\'use_template\' element requires the \'name\' attribute')
        name = xml_element.attrib['name']
        get_logger().debug('using condition template: {0}'.format(name))
        # Make sure have a template with that name
        if name not in self[GTPL_CONDITION]:
            self.context.parse_error(self.trace_id[0], 'Invalid condition template name: {0}'.format(name))                    
        # Get the template   
        template = self[GTPL_CONDITION][name]
        
        # Turn the template into the evaluatable and return it
        return evaluatable_creator(template, trace_dict, self.context, self.trace_id)
        