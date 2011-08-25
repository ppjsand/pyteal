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
import re
import socket
import sys

from exceptions import ValueError
from xml.etree.ElementTree import ElementTree

from ibm.teal import registry
from ibm.teal.registry import SERVICE_LOCATION, get_logger


LOCATION_COMP_PATTERN = '^({0})({1})$'
TEAL_LOCATION_VALIDATION = 'TEAL_LOCATION_VALIDATION'


class LocationService(dict):
    '''
    The LocationService class is responsible for validating and creating Location
    objects within the TEAL framework
    
    This is an internal class used by the Location class for Location metadata and should
    not be accessed otherwise except for initialization
    '''

    def __init__(self,locationConfig):
        ''' Constructor
        '''
        dict.__init__(self)

        # Parse the location configuration and store for retrieval
        root = ElementTree().parse(locationConfig)        
        for loc_elem in root.getchildren():
            loc_info = LocationInfo(loc_elem)
            self[loc_info.id] = loc_info
        return

    def is_scope_valid(self, type, scope):
        ''' Verify that the given scope is a part of the giving location type'''
        loc_info = self.get(type, None)
        if (loc_info is not None and loc_info.get(scope, None) is not None):
            return True
        return False

    def get_teal_location(self, loc_instance=None ):
        ''' get a Location that is set to the location for TEAL
            if loc_instance is set then add it as the last part of the location '''
        if loc_instance is not None:
            loc_str = '{0}##{1}##{2}##{3}'.format(socket.gethostname(), os.path.basename(sys.argv[0]), os.getpid(), loc_instance)
        else:
            loc_str = '{0}##{1}##{2}'.format(socket.gethostname(), os.path.basename(sys.argv[0]), os.getpid())

        try:
            teal_location = Location('A', loc_str)
        except:
            get_logger().warning('Unable to create TEAL location')
            teal_location = None
        return teal_location

class LocationInfo(dict):
    def __init__(self, loc_elem):
        dict.__init__(self)

        # Save basic information about the Location
        self.id = loc_elem.get('id')
        self.type = loc_elem.get('type')
        self.separator = loc_elem.get('separator',".")
        self.root = None

        # Now load the component information for this location
        for content_elem in loc_elem.getchildren():
            # Determine the content type of the component info
            location_content = content_elem.tag.split('}')[-1]
            if (location_content == 'simple'):
                parent_comp_info = None
                comp_index = 1
                for comp_elem in content_elem:
                    # Generate and save the current component information
                    comp_info = ComponentInfo(comp_elem, False)
                    comp_info.index = comp_index
                    self[comp_info.type] = comp_info

                    # Child of parent is current element
                    if parent_comp_info is not None:
                        parent_comp_info.children = [comp_info.type]
                    else:
                        # First element without a parent is the root
                        self.root = (comp_info.type,comp_info)

                    parent_comp_info = comp_info
                    comp_index = comp_index + 1   
            else:
                for comp_elem in content_elem:   
                    # Need to create each component before we figure out
                    # where it sits within the hierarchy
                    comp_info = ComponentInfo(comp_elem, True)
                    self[comp_info.type] = comp_info

                # Set the scope of each of the elements loaded
                comp_index = 1
                self.root = self._find_comp_root(self.items())
                self._set_comp_index(self.root[1], comp_index) 
        return

    def _set_comp_index(self, comp_info, index):
        ''' Set the index of each component info based on the child relationship
        with the current element
        '''
        comp_info.index = index
        index = index + 1
        for child in comp_info.children:
            self._set_comp_index(self[child],index)
        return

    def _find_comp_root(self,comps):
        ''' Find the root component within this location.
        
        For a complex location there must be one and only one root
        '''
        # Find the root (element not a child of any other node)
        root_found = False
        root_comp = None
        for search_comp in comps:
            # Assume that the current element will be the root element
            is_root = True
            for test_comp in comps:
                if search_comp[1].type in test_comp[1].children:
                    # This component is a child of another component
                    # and therefore cannot be root
                    is_root = False
                    break

            # Fail if there are multiple roots found
            if (is_root and root_found):
                raise ValueError,"Multiple roots found: {0},{1}".format(root_comp[1].type,search_comp[1].type)

            # If we checked this component against all other components
            # and it was not a child of any other component, then this
            # is the root element
            if (is_root and not root_found):
                root_found = True
                root_comp = search_comp

        # Fail if no Root found
        if (not is_root and not root_found):
            raise ValueError,"No root component found"
        return root_comp


class ComponentInfo(object):
    def __init__(self, comp_elem, isComplex):
        self.index = 0
        self.id_info = None
        self.children = []
        self.type = comp_elem.get('type')

        if (isComplex):
            self._load_complex_content(comp_elem)
        return

    def _load_complex_content(self, comp_elem):
        ''' Load the complex component content from the XML file
        '''
        id = comp_elem.get('id')
        pattern = comp_elem.get('pattern', '')
        self.id_info = (id,pattern)
        self.children = self._load_complex_content_children(comp_elem)
        return
    
    def _load_complex_content_children(self,comp_elem):
        ''' Determine the set of children for this complex component
        '''
        ns_idx = comp_elem.tag.find('}')
        if (ns_idx > 0):
            compref_tag = comp_elem.tag[0:ns_idx+1]+'compref'
        else:
            compref_tag = 'compref'

        ref_elems = comp_elem.findall(compref_tag)
        return [ref_elem.get('ref') for ref_elem in ref_elems]


class Location(object):
    '''The Location object class is responsible for encapsulating the string locations

    The constructed location must be a valid location based on the XML configuration
    for this system.
    '''

    def __init__(self, location_id, data):
        ''' Constructor 
        '''
        if not(isinstance(data, str) or isinstance(data, unicode)):
            raise TypeError,"Invalid type of Location data: {0}.".format(type(data))

        loc_service = registry.get_service(SERVICE_LOCATION)
        try:
            self.location_info = loc_service[location_id]
            self.location_code = data.split(self.location_info.separator)

            # Location code is initialized, now validate it
            self._validate_location_code()
        except:
            tmp_env = os.environ.get(TEAL_LOCATION_VALIDATION, 'LOG').upper()
            if tmp_env == 'LOG':
                get_logger().exception('LOGGING Location creation failure and continuing processing')
            elif tmp_env == 'IMMEDIATE':
                raise

            self.loc_id = location_id
            self.data = data

            self.ex_type, self.ex_value = sys.exc_info()[:2]

            self.is_unprocessable = self.is_unprocessable_UNPROCESSABLE
            self.new_location_by_scope = self._UNPROCESSABLE
            self.get_comp_value = self._UNPROCESSABLE
            self.get_substitution_dict = self._UNPROCESSABLE
            self.get_location = self.get_location_UNPROCESSABLE
            self.str_impl = self.str_impl_UNPROCESSABLE
            self.match = self.match_UNPROCESSABLE
            self.get_id = self.get_id_UNPROCESSABLE
        return
    
    def is_unprocessable(self):
        ''' Default is that is is processable '''
        return False
    
    def is_unprocessable_UNPROCESSABLE(self):
        ''' it isn't processable '''
        return True

    def __str__(self):
        ''' Return the string representation of this location code 
        '''
        return self.str_impl()

    def str_impl(self):
        ''' __str__ implementation ''' 
        return '{0}: {1}'.format(self.location_info.id, self.get_location())

    def str_impl_UNPROCESSABLE(self):
        ''' Return the string representation when the location is unprocessable '''
        return '{0}: {1}'.format(self.loc_id, self.get_location())

    def __cmp__(self,other):
        ''' Compare two location codes -- they are the same if the strings match
        '''
        return cmp(str(self),str(other))

    def __hash__(self):
        ''' Since __cmp__ is defined, we need to define this method so Locations can be
        added to hash tables
        '''
        return hash(str(self))

    def _validate_component(self,comps,loc_index):
        ''' Validation routine to validate the specific pieces of a complex Location code
        '''
        if (len(self.location_code) <= loc_index):
            return # validation is complete

        # Grab the component id values
        for comp in comps:
            (id, pattern) = self.location_info[comp].id_info

            # Parse the location into ID and pattern value
            regex = LOCATION_COMP_PATTERN.format(id, pattern)
            m = re.match(regex, self.location_code[loc_index])            

            # If it doesn't match, then this is not the right component at this level. 
            # Check the other components at this level
            if m is None:
                continue

            # Go to the children and find the matching child and validate it
            self._validate_component(self.location_info[comp].children,loc_index+1)
            return

        raise ValueError,"Location Code '{0}' invalid: Invalid component at position {1}".format(self,loc_index)

    def _validate_location_code(self):
        ''' Validate a simple or complex Location Code 
        '''
        # Verify that the location code has no extra components by checking
        # the number of components against the set of component ids for scoping
        loc_code_len = len(self.location_code)
        if loc_code_len not in [comp_info.index for comp_info in self.location_info.values()]:
            raise ValueError,"Location Code '{0}' of type {1} has too many components".format(self.location_info.separator.join(self.location_code),self.location_info.id)

        # Check if this is a simple component type, if so, there is no further validation required
        (root_type, root_info) = self.location_info.root 

        # If no id values for element, then this is a simple location
        if root_info.id_info is None:
            return

        # Complex component so validate the subsections of the location code by walking down the hierarchy
        self._validate_component([root_type],0)

    def match(self, other_loc, trunc_comp=None):
        ''' Compares two location codes at a given truncation scope
        '''
        if (trunc_comp is not None):
            index = self.location_info[trunc_comp].index
        else:
            index = len(self.location_code)

        return ((other_loc.location_info.type == self.location_info.type) and (other_loc.location_code[0:index] == self.location_code[0:index]))        

    def match_UNPROCESSABLE(self, other_loc, trunc_comp=None):
        ''' Compares two location codes at a given truncation scope
            When the location is unprocessable
        '''
        if trunc_comp is not None:
            self._UNPROCESSABLE()
        return self == other_loc

    def new_location_by_scope(self, comp_type):
        '''Return a new Location scoped to the specified component
        '''
        index = self.location_info[comp_type].index
        return Location(self.location_info.id,self.location_info.separator.join(self.location_code[0:index]))

    def get_id(self):
        ''' Return the type of location
        '''
        return self.location_info.id

    def get_id_UNPROCESSABLE(self):
        ''' Return the type of location 
            When unprocessable Location
        '''
        return self.loc_id

    def get_location(self):
        ''' Return the location only
            i.e. without the type prepended
        '''
        return self.location_info.separator.join(self.location_code)

    def get_location_UNPROCESSABLE(self):
        ''' Return the locatio nonly when unprocessable ''' 
        return self.data

    def get_comp_value(self, comp):
        '''Return the component value for the specified component

        If this is a simple component, then the value at the corresponding
        spot will be returned

        If this is a complex component the number portion will be returned
        '''
        index = self.location_info[comp].index
        ident = self.location_info[comp].id_info

        if (ident is None):
            return self.location_code[index-1]
        else:
            comp_value = self.location_code[index-1]
            regex = LOCATION_COMP_PATTERN.format(*ident)
            m = re.match(regex, comp_value)
            # Make sure we are looking at the correct identifier
            # It could be that we are looking at a component at the
            # same level of the queried one            
            if m is not None and (m.group(1) == ident[0]):
                # Make sure that this particular component has a value
                if (len(m.group(2)) > 0):
                    # This is the numeric portion of the component
                    return m.group(2)
                else:
                    raise ValueError,"Component '{0}' of Location {1} does not have a value".format(comp,self)                
            else:
                raise ValueError,"{0} does not have a '{1}' component".format(self,comp)

    def get_substitution_dict(self):
        ''' Return a dictionary of each component to its value 
        in the location
        '''
        max_index = len(self.location_code)
        sub_dict = {}
        for comp in self.location_info:
            index = self.location_info[comp].index
            if index > max_index:
                continue
            comp_value = self.location_code[index-1]
            ident = self.location_info[comp].id_info
            if ident is not None:
                regex = LOCATION_COMP_PATTERN.format(*ident)
                m = re.match(regex, comp_value)

                if m is None:
                    continue

                if m.group(1) != self.location_info[comp].id_info[0]:
                    continue

            sub_dict[comp] = comp_value
        return sub_dict

    def _UNPROCESSABLE(self, dummy=None):
        ''' Raise an exception for the method when the location is unprocessable
        '''
        raise self.ex_type, self.ex_value


if __name__ == '__main__':
    pass