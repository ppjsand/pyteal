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

from ibm.teal.database import db_interface
import os
import struct
from xml.etree.ElementTree import ElementTree

from ibm.teal import registry
from ibm.teal.registry import TEAL_DATA_DIR, get_logger, SERVICE_DB_INTERFACE
from ibm.teal.location import Location

EXT_DATA_RAW_DATA = 'raw_data'

EXT_DATA_COMP_MASK = 0xFFFFFFFF00000000
EXT_DATA_CTL_MASK  = 0x00000000FF000000
EXT_DATA_VER_MASK  = 0x0000000000FF0000
EXT_DATA_ID_MASK   = 0x000000000000FFFF

EXT_DATA_CTL_DB    = 0x80

EXT_FILE_DIR = os.path.join('ibm','teal','xml')

TEAL_ELEM_BIGINT = 'BIGINT'
TEAL_ELEM_INTEGER = 'INTEGER'
TEAL_ELEM_CHAR = 'CHAR'
TEAL_ELEM_VARCHAR = 'VARCHAR'
TEAL_ELEM_TEXT = 'TEXT'
TEAL_ELEM_LOCATION = 'LOC' 

teal_elem_str_types = 'sp'
teal_elem_map = {
                 TEAL_ELEM_BIGINT:'q',
                 TEAL_ELEM_INTEGER:'i',
                 TEAL_ELEM_CHAR:'s',
                 TEAL_ELEM_VARCHAR:'p',
                 TEAL_ELEM_TEXT:'p',
                 TEAL_ELEM_LOCATION:'3p256p'# 2-character type + 255 character code
                 }

class ExtensionData(dict):
    '''
    ExtensionData is responsible for extracting user-defined data from a raw data buffer
    and creating a dictionary of values baesd on that data
    
    The data is retrived from a file determined by the comp_format number passed to the
    constructor. The comp_format is broken down into the following components
    
    - 4-byte comp (ascii hex)
    - 1-byte control, (bit 7 = DB) 
    - 1-byte version, 
    - 2-byte structure id id

    The comp and version number are used to find the correct file for the definition
    of the data
    
    By default, the dictionary is always populated with a 'raw_data' entry to retrieve
    the buffer again
    '''
    def __init__(self, comp_format, ext_key, raw_data=None, in_dict=None):
        '''
        Constructor
        '''
        dict.__init__(self)

        if (raw_data and in_dict):
            raise ValueError,'Must specify only one of raw_data or in_dict'
        
        self.format = comp_format
        self.ext_key = ext_key
        
        if in_dict is not None:
            self.read_from_dictionary(in_dict)
        else:
            self[EXT_DATA_RAW_DATA] = raw_data        
            
            if (self.format != 0):
                # Format Spec=<4-byte comp, 1-byte control, 1-byte version, 2-byte struct id>
                (comp,self.ctrl,ver,self.ident) = _split_fmt(self.format)
                        
                # Parse the users extension data
                self.base_name = comp + '_' + '{0:X}'.format(ver)
                data_dir = registry.get_service(TEAL_DATA_DIR)
                ext_file_name = os.path.join(data_dir, EXT_FILE_DIR, self.base_name +'.xml')
                get_logger().debug("File to open: {0}".format(ext_file_name))
            
                root = ElementTree().parse(ext_file_name)
                table = self._find_table(root,self.ident)
                
                if (self.ctrl & EXT_DATA_CTL_DB):
                    items = self._unpack_from_db(table, ext_key)
                else:
                    items = self._unpack_from_data(table, raw_data)
                     
                self._populate(table, items)
        return
    
    def _populate(self, table_elem, items):
        ''' Take the list of data items and add them to the dictionary '''
        # Insert the extension data into the dictionary
        if (items is not None):
            i = 0
            for column_elem in table_elem.getchildren():
                column_name = column_elem.get('name')
                if (column_elem.get('type') == TEAL_ELEM_LOCATION):
                    if (items[i] is not None):
                        self[column_name] = Location(items[i],items[i+1])
                    else:
                        self[column_name] = None    
                    i = i + 2
                else:
                    self[column_name] = items[i]
                    i = i + 1
        else:
            raise ValueError, 'No extension data found for format {0}'.format(self.format)
              
    def write_to_dictionary(self):  
        ''' Write out to a dictionary that contains only basic types '''
        out_dict = self.copy()
        for key, item in self.items():
            if isinstance(item, Location):
                out_dict[key+'_type'] = item.get_id()
                out_dict[key] = item.get_location()
        return out_dict
    
    def read_from_dictionary(self, in_dict):
        ''' Read input from a dictionary '''
        self.update(in_dict)
        for key, item in in_dict.items():
            if key[-5:] == '_type':
                loc_key = key[0:-5]
                self[loc_key] = Location(item, in_dict[loc_key])
                del self[key]
        return
        
    def _unpack_from_db(self, table_elem, ext_key):
        ''' Populate the dictionary from an external database table'''
        # Determine column names to select
        columns = []
        for column_elem in table_elem.getchildren():
            column_name = column_elem.get('name')
            if (column_elem.get('type') == TEAL_ELEM_LOCATION):
                columns.append('{0}_type'.format(column_name))
            columns.append(column_name)  
        
        # Create the query to return all of the specified extension data
        table_id = '{0}_{1:X}'.format(self.base_name,self.ident)
        table_name = db_interface.TABLE_TEMPLATE.format(table_id)

        # Fetch the extension data from the table
        db = registry.get_service(SERVICE_DB_INTERFACE)
        query = db.gen_select(columns, table_name, where='$rec_id = ?',where_fields=['rec_id'])
        get_logger().debug(query)
        cnxn = db.get_connection()
        cursor = cnxn.cursor()
        cursor.execute(query, ext_key)
        cols = cursor.fetchone()
        cnxn.close()
        return cols
        
        
    def _unpack_from_data(self, table_elem, raw_data):
        ''' Populate the dictionary from the packed data '''
        fmt = self._gen_format_str(table_elem)
        s = struct.Struct(fmt)
        return s.unpack_from(raw_data)
                    
    def _find_table(self, ext_root_elem, ident):
        ''' Find the table specified by the user format id '''
        for table_elem in ext_root_elem.getchildren():
            if (int(table_elem.get('id')) == ident):
                return table_elem
        raise ValueError, "Invalid identifier specified: {0}".format(fmt2str(self.format))
            
    def _gen_format_str(self,table_elem):
        ''' Generate the format string and extension dictionary '''
        fmt = ""
 
        for column_elem in table_elem.getchildren():
            # Determine the type from the type mappings
            elem_type = teal_elem_map[column_elem.get('type')]
            
            # Now add any size value for the given type
            tmp_elem_size = column_elem.get('size')
            if (tmp_elem_size is not None) and (elem_type in teal_elem_str_types):
                if (elem_type == 's'):
                    elem_size = tmp_elem_size
                else:
                    # Must include the length character in the total size for
                    # pascal strings
                    elem_size = str(int(tmp_elem_size) + 1)
            else:
                elem_size = ""
                                
            # Append this type to the format string    
            fmt = fmt + elem_size + elem_type
            
        return fmt            
    
    def get_format(self):
        ''' Return the format field for this extension data '''
        return self.format
        
    def get_ext_key(self):
        ''' Return the format field for this extension data '''
        return self.ext_key
        
def fmt2str(fmt):
    ''' Return a printable breakdown of the format field '''
    (comp,ctrl,ver,ident) = _split_fmt(fmt)
    
    if (ctrl & EXT_DATA_CTL_DB):
        ctrl_str = "DB"
    else:
        ctrl_str = "File"
    fmt_str = 'Component = {0}, Control = \"{1}\", Data Version = {2}, Table Identifier = {3}'    
    
    #base_name = hex2str(comp) + '_' + str(ver)
    #file_name = base_name +'.xml'
    #print file_name
    
    return fmt_str.format(comp,ctrl_str,ver,ident)

def extdata_fmt2table_name(fmt):
    ''' Return the database table name for a given format value. If the fmt
    is not for a database, None is returned
    '''
    table_name = None
    
    (comp,ctrl,ver,ident) = _split_fmt(fmt)
    
    if (ctrl & EXT_DATA_CTL_DB):
        table_id = '{0}_{1:X}_{2:X}'.format(comp,ver,ident)
        table_name = db_interface.TABLE_TEMPLATE.format(table_id)
    
    return table_name    

def _str2hex(comp_str):
    ''' Create a hex number from a 4-character sequence '''
    comp_hex = 0
    for i in xrange(4):
        comp_hex = (comp_hex<<8) + ord(comp_str[i])
    return comp_hex    
      
def _hex2str(comp_hex):
    ''' Take a 4-byte hex number (ascii digits) and return ascii equivalent '''
    comp_str = ""
    for i in xrange(4):
        val = comp_hex&0xff
        comp_hex = comp_hex >> 8
        if (val == 0):
            continue
        comp_str = chr(val) + comp_str
    return comp_str

def _split_fmt(fmt):
    ''' Internal function to split the format string into
    its constiuent parts
    '''
    comp = _hex2str((EXT_DATA_COMP_MASK & fmt) >> 32)
    ctrl = (EXT_DATA_CTL_MASK & fmt) >> 24       
    ver  = (EXT_DATA_VER_MASK & fmt) >> 16
    ident =  EXT_DATA_ID_MASK & fmt
    
    return (comp,ctrl,ver,ident)

if __name__ == '__main__':
    #from ibm.teal import Teal
    #teal = Teal('test/ut/data/common/configurationtest.conf')
    #ed1 = ExtensionData(0x5445535480000003, None, 1)    
    #ed2 = ExtensionData(0x5445535400000003, struct.pack('2p255p','S','riven##xterm##1234'),None)
    #print ed1['neighbor']
    #print ed2['neighbor']
    print fmt2str(0x5445535480000003)
    print fmt2str(0x5445535400000003)
    print '%x' % _str2hex("CNM\0")
    print fmt2str(0x434e4d0000000003)
    print extdata_fmt2table_name(0x434e4d0080000003)
    #print '%x' % str2hex("XCAT")
    #print '%x' % str2hex("TEST")
