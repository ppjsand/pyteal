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

from xml.etree.ElementTree import iterparse

class FileWithLineNum:
    def __init__(self, source):
        ''' start at line 0 '''
        self.source = source
        self.line_num = 0
        return
        
    def read(self, bytes):
        ''' read the next line and inc the line number '''
        s = self.source.readline()
        self.line_num += 1
        return s

def read_xml_file(file_name, base_trace_num=0):
    ''' Read the xml file and return the root element and a dictionary tuple
        The Dictionary from element to tuple of line_num and trace id '''
    if file_name is None or file_name == '':
        return (None,{})
    file = FileWithLineNum(open(file_name))
    out_dict = {}
    root_element = None
    trace_nums = [0]*102    # Can't conceive of having > 100 levels
    trace_nums[0] = base_trace_num
    trace_idx = -1

    for event, element in iterparse(file, events=["start", "end"]):
        if root_element is None:
            root_element = element
        if event == "start":
            trace_idx += 1
            trace_nums[trace_idx] += 1
            trace_id = '.'.join([ str(x) for x in trace_nums[:trace_idx+1]])
            out_dict[element] = (file.line_num, trace_id)
            #print out_dict[element]
        else:
            trace_nums[trace_idx+1] = 0 # Restart one level up
            trace_idx -= 1
    return (root_element, out_dict)
