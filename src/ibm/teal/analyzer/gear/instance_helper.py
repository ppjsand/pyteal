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

from ibm.teal.teal_error import XMLParsingError

ISP_PREV_TYPE_AS_STRING = ['None', 'And', 'Or', 'Token']
ISP_PREV_TYPE_NONE = 0
ISP_PREV_TYPE_AND = 1
ISP_PREV_TYPE_OR = 2
ISP_PREV_TYPE_TOKEN = 3

def instance_str_parser(data, index=0, top=True):
    ''' This method parses an instances string definition into comparitor classes '''
    current = None
    result = None
    while index < len(data):
        c_char = data[index]
        if  c_char == '(':
            # get result of contained 
            current, index = instance_str_parser( data, index+1, top=False)
            
        elif c_char == ')':
            if top is True:
                raise XMLParsingError('unmatched parenthesis')
            if result is None:
                # Just a token
                if current is None:
                    raise XMLParsingError('empty parenthesis' )
                current.check()
                return current, index
            else:
                current.check()
            result.items.append(current)
            return result, index 
        
        elif c_char == '&':
            if result is None:
                result = AndComparitor()
                current.check()
                result.items.append(current)
                current = None
            else:
                if current is None:
                    raise XMLParsingError('missing token')
                current.check()
                result.items.append(current)
                current = None
                if result.type() == ISP_PREV_TYPE_OR:
                    new_result = AndComparitor()
                    new_result.items.append(result)
                    result = new_result 
                
        elif c_char == '|':
            if result is None:
                result = OrComparitor()
                current.check()
                result.items.append(current)
                current = None
            else:
                if current is None:
                    raise XMLParsingError('missing token')
                current.check()
                result.items.append(current)
                current = None
                if result.type() == ISP_PREV_TYPE_AND:
                    new_result = OrComparitor()
                    new_result.items.append(result)
                    result = new_result 
                
        else: # Collect in token 
            if current is None:
                if c_char is ' ':
                    index += 1
                    continue
                current = TokenComparitor()
            current.add_char(c_char)
            
        index += 1
    
    if top == False:
        raise XMLParsingError('unmatched parenthesis')
    if result is None:
        if current is None:
            raise XMLParsingError('nothing specified')
        # Just a token 
        current.check()
        return current, index 
        # Just a token 
    
    # If closed by ) was returned above so have dangling token
    current.check()
    result.items.append(current)
    return result, index 
    
    
class ComparitorElementParent(object): 
    ''' Special methods for thing that can be a parent '''
    
    def child_now_true(self):
        ''' Notify parent of a state change '''
        pass


class Comparitor(ComparitorElementParent):
    ''' Provide a root for comparison '''
    
    def __init__(self, xml_str, unique_loc=False):
        ''' Constructor ... take an xml string and create a hierarchy of objects '''
        self.state = False
        self.root = instance_str_parser(xml_str)[0]
        self.direct_map = self.root.get_mapping()
        self.root.assign_control(self) #parent
        return
    
    def in_comparison(self, value):
        ''' check if value is in comparision string '''
        return value in self.direct_map
    
    def check(self, values):
        ''' Check if true for all of the values '''
        if self.state is True:
            return True
        for value in values:
            if self.assert_value(value) == True:
                break
        return self.state
    
    def assert_value(self, value):
        ''' assert the value is true '''
        if value not in self.direct_map:
            return False
        for comptr in self.direct_map[value]:
            comptr.assert_value(value)
        return self.state
    
    def clear(self):
        ''' clear state '''
        self.root.clear()
        self.state = False
        return
    
    def child_now_true(self):
        ''' child changed state '''
        self.state = True
        return
    
    def __str__(self):
        ''' print out prefix of overall state ''' 
        if self.state:
            outstr = 'True: '
        else:
            outstr = 'False: '
        outstr += str(self.root)
        return outstr
    

class ComparitorElement(object):
    ''' Base comparitor class to allow checking instance specification '''
    
    def __init__(self): 
        ''' constructor '''
        # Start with nothing matched
        self.state = False
        self.parent = None
        return
    
    def clear(self):
        ''' Clear state '''
        self.state = False
        return
    
    def assert_value(self, value):
        ''' Assert a value to update state and return if makes true or not '''
        pass
        
    def assign_control(self, parent):
        ''' Assign passed parent and pass yourself as parent to children '''
        pass
    
    def type(self):
        ''' type of comparitor '''
        pass
    
    def add_char(self, char):
        ''' Add a character to to the comparitor ''' 
        pass
    
    def check(self):
        ''' Accumulation complete, check for validity '''
        pass

       
class TokenComparitor(ComparitorElement):
    ''' Support comparision for integers ''' 
    
    def __init__(self):
        ''' constructor '''
        self.token = ''
        ComparitorElement.__init__(self)
        return
    
    def assert_value(self, token):
        ''' assert value ''' 
        if self.state == True:
            return 
        if token == self.token:
            self.state = True
            self.parent.child_now_true()
        return
        
    def get_mapping(self):
        ''' return mapping from value to comparitor '''
        return {self.token: [self]}
    
    def assign_control(self, parent):
        ''' assign parent '''
        self.parent = parent
        return

    def __str__(self):
        ''' print out note suffix with + if true''' 
        outstr = self.token
        if self.state:
            outstr += '+'
        return outstr
    
    def type(self):
        ''' return type '''
        return ISP_PREV_TYPE_TOKEN
    
    def add_char(self, char):
        ''' Add a character '''
        self.token += char
        return 
    
    def check(self):
        ''' Check if valid '''
        self.token = self.token.strip()
        if len(self.token) == 0:
            raise XMLParsingError('token expected')
        return 

    
class OrComparitor(ComparitorElement, ComparitorElementParent):
    ''' Provide an or operation over comparitors ''' 
    
    def __init__(self):
        ''' constructor ''' 
        self.items = []
        ComparitorElement.__init__(self)
        return
    
    def assert_value(self, value):
        ''' Not used with direct map '''
        pass
    
    def clear(self):
        ''' Clear state '''
        ComparitorElement.clear(self)
        for item in self.items:
            item.clear()
        return
    
    def get_mapping(self):
        ''' return mapping from value to comparitor '''
        my_map = {}
        for item in self.items:
            item_map = item.get_mapping()
            for key in item_map:
                if key in my_map:
                    my_map[key].extend(item_map[key])
                else:
                    my_map[key] = item_map[key]
        return my_map
    
    def assign_control(self, parent):
        ''' assign parent and tell children we're their parent'''
        self.parent = parent
        for item in self.items:
            item.assign_control(self)
        return
    
    def child_now_true(self):
        ''' child changed state         '''
        if self.state == True:
            return
        self.state = True
        self.parent.child_now_true()
        return

    def __str__(self):
        ''' print out items in or.  an o suffix means its state is true '''
        if len(self.items) > 1:
            outstr = '('
            close = ')'
        else: 
            outstr = ''
            close = ''
        for item in self.items:
            outstr += str(item)
            if item != self.items[-1]:
                outstr += ' | '
        outstr += close
        if self.state:
            outstr += '+'
        return outstr
      
    def type(self):
        ''' return type '''
        return ISP_PREV_TYPE_OR
    
    def add_char(self, char):
        ''' Add a character '''
        if char != ' ':
            raise XMLParsingError('unexpected character \'{0}\''.format(char))
        return 
    
    def check(self):
        ''' Check validity '''
        return 
            
class AndComparitor(ComparitorElement, ComparitorElementParent):
    ''' Provide an and operation over comparitors ''' 

    def __init__(self):
        ''' constructor '''
        self.items = []
        self.true_items = 0
        ComparitorElement.__init__(self)
        return
    
    def assert_value(self, value, location, event):
        ''' Not used with direct map '''
        pass
    
    def clear(self):
        ''' Clear state '''
        ComparitorElement.clear(self)
        self.true_items = 0
        for item in self.items:
            item.clear()
        return
    
    def get_mapping(self):
        ''' return mapping from value to comparitor '''
        my_map = {}
        for item in self.items:
            item_map = item.get_mapping()
            for key in item_map:
                if key in my_map:
                    my_map[key].extend(item_map[key])
                else:
                    my_map[key] = item_map[key]
        return my_map
        
    def assign_control(self, parent):
        ''' assign parent and tell children we're their parent'''
        self.parent = parent
        for item in self.items:
            item.assign_control(self)
        return
     
    def child_now_true(self):
        ''' child changed state 
        '''
        if self.state == True:
            return 
        self.true_items += 1
        if self.true_items == len(self.items):
            self.state = True 
            self.parent.child_now_true()
        return

    def __str__(self):
        ''' print out items in and.  an a suffix means its state is true '''
        if len(self.items) > 1:
            outstr = '('
            close = ')'
        else: 
            outstr = ''
            close = ''
        for item in self.items:
            outstr += str(item)
            if item != self.items[-1]:
                outstr += ' & '
        outstr += close
        if self.state:
            outstr += '+'
        return outstr
    
    def type(self):
        ''' return type '''
        return ISP_PREV_TYPE_AND
    
    def add_char(self, char):
        ''' Add a character '''
        if char != ' ':
            raise XMLParsingError('unexpected character \'{0}\''.format(char))
        return 
    
    def check(self):
        ''' Check validity '''
        return
    