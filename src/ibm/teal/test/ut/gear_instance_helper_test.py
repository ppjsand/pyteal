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

import unittest 
from ibm.teal import teal
from ibm.teal.test.teal_unittest import TealTestCase
from ibm.teal.analyzer.gear.instance_helper import Comparitor
from ibm.teal.teal_error import XMLParsingError
from ibm.teal.analyzer.gear.rule_condition_data import _perm_checker

''' NAME is MISLEADING

    This module is now for testing ALL of the GEARs helpers, not just the instance support,\
    _perm_checker
''' 
    
class GearInstanceHelper(TealTestCase):
    '''Test running GEAR instance helper '''
    
    def test_single_token1(self):
        ''' Test that a single token works '''
        c = Comparitor('abc')
        self.assertEqual('False: abc', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['abc']))
        self.assertEqual('True: abc+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: abc', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['ab', 'bd', 'ef']))
        self.assertTrue(c.check(['ab', 'bd', 'abc']))
        self.assertTrue(c.in_comparison('abc'))
        self.assertFalse(c.in_comparison('ac'))
        return
    
    def test_single_token2(self):
        ''' Test that a single token in parenthesis works '''
        c = Comparitor('(abc)')
        self.assertEqual('False: abc', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['abc']))
        self.assertEqual('True: abc+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: abc', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['ab', 'bd', 'ef']))
        self.assertTrue(c.check(['ab', 'bd', 'abc']))
        self.assertTrue(c.in_comparison('abc'))
        self.assertFalse(c.in_comparison('ac'))
        return
    
    def test_single_token3(self):
        ''' Test that a single token and with itself works '''
        c = Comparitor('abc&abc')
        self.assertEqual('False: (abc & abc)', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['abc']))
        self.assertEqual('True: (abc+ & abc+)+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: (abc & abc)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['ab', 'bd', 'ef']))
        self.assertTrue(c.check(['ab', 'bd', 'abc']))
        self.assertTrue(c.in_comparison('abc'))
        self.assertFalse(c.in_comparison('ac'))
        return
    
    def test_single_token4(self):
        ''' Test that a single token and with itself and parenthesis works '''
        c = Comparitor('((abc)&(abc))')
        self.assertEqual('False: (abc & abc)', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['abc']))
        self.assertEqual('True: (abc+ & abc+)+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: (abc & abc)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['ab', 'bd', 'ef']))
        self.assertTrue(c.check(['ab', 'bd', 'abc']))
        self.assertTrue(c.in_comparison('abc'))
        self.assertFalse(c.in_comparison('ac'))
        return
    
    def test_single_token5(self):
        ''' Test that a single token and with itself and parenthesis and spacing works '''
        c = Comparitor('  (  ( abc)  & (abc )          )       ')
        self.assertEqual('False: (abc & abc)', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['abc']))
        self.assertEqual('True: (abc+ & abc+)+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: (abc & abc)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['ab', 'bd', 'ef']))
        self.assertTrue(c.check(['ab', 'bd', 'abc']))
        self.assertTrue(c.in_comparison('abc'))
        self.assertFalse(c.in_comparison('ac'))
        return
    
    def test_two_token1(self):
        ''' Test that a two tokens and works '''
        c = Comparitor('  (  ( a)  & (b))       ')
        self.assertEqual('False: (a & b)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['b']))
        self.assertEqual('False: (a & b+)', str(c))
        self.assertFalse(c.check(['b']))
        self.assertEqual('False: (a & b+)', str(c))
        self.assertTrue(c.check(['a']))
        self.assertEqual('True: (a+ & b+)+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: (a & b)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['c', 'd', 'ef']))
        self.assertTrue(c.check(['a', 'b']))
        self.assertTrue(c.in_comparison('a'))
        self.assertTrue(c.in_comparison('b'))
        self.assertFalse(c.in_comparison('c'))
        return
    
    def test_two_token2(self):
        ''' Test that a two tokens or works '''
        c = Comparitor('a|b')
        self.assertEqual('False: (a | b)', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['b']))
        self.assertEqual('True: (a | b+)+', str(c))
        self.assertTrue(c.check(['b']))
        self.assertEqual('True: (a | b+)+', str(c))
        self.assertTrue(c.check(['a']))
        # Not a+ because shortcuts once true
        self.assertEqual('True: (a | b+)+', str(c))
        self.assertTrue(c.check([]))
        c.clear()
        self.assertEqual('False: (a | b)', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['a']))
        self.assertEqual('True: (a+ | b)+', str(c))
        self.assertTrue(c.check(['a']))
        self.assertEqual('True: (a+ | b)+', str(c))
        self.assertTrue(c.check(['b']))
        # Not b+ because shortcuts once true
        self.assertEqual('True: (a+ | b)+', str(c))
        self.assertTrue(c.check([]))
        
        c.clear()
        self.assertEqual('False: (a | b)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['c', 'd', 'ef']))
        self.assertTrue(c.check(['a', 'b']))
        self.assertTrue(c.in_comparison('a'))
        self.assertTrue(c.in_comparison('b'))
        self.assertFalse(c.in_comparison('c'))
        return
    
    def test_complex1(self):
        ''' Test that first complex example works '''
        c = Comparitor('a|b & (c) | b|d&e&f')
        self.assertEqual('False: ((((a | b) & c) | b | d) & e & f)', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['b']))
        self.assertEqual('False: ((((a | b+)+ & c) | b+ | d)+ & e & f)', str(c))
        self.assertFalse(c.check(['b']))
        self.assertEqual('False: ((((a | b+)+ & c) | b+ | d)+ & e & f)', str(c))
        self.assertFalse(c.check(['a']))
        self.assertTrue(c.check(['e', 'f']))
        self.assertEqual('True: ((((a+ | b+)+ & c) | b+ | d)+ & e+ & f+)+', str(c))
        c.clear()
        self.assertEqual('False: ((((a | b) & c) | b | d) & e & f)', str(c))
        self.assertFalse(c.check([]))
        self.assertTrue(c.check(['d','e','f']))
        self.assertEqual('True: ((((a | b) & c) | b | d+)+ & e+ & f+)+', str(c))
        self.assertTrue(c.in_comparison('a'))
        self.assertTrue(c.in_comparison('e'))
        self.assertFalse(c.in_comparison('k'))
        return
    
    def test_complex2(self):
        ''' Test that first complex example works '''
        c = Comparitor('((a|b) & (c|d)) | (f&q)')
        self.assertEqual('False: (((a | b) & (c | d)) | (f & q))', str(c))
        self.assertFalse(c.check([]))
        self.assertFalse(c.check(['b', 'f']))
        self.assertTrue(c.check(['a', 'd']))
        self.assertEqual('True: (((a+ | b+)+ & (c | d+)+)+ | (f+ & q))+', str(c))
        return
    
    def test_zzzfailure1(self):
        ''' Test failures '''
        myteal = teal.Teal('data/teal_test/good_01.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
        self.assertRaisesTealError(XMLParsingError, 'nothing specified', Comparitor, '')
        self.assertRaisesTealError(XMLParsingError, 'empty parenthesis', Comparitor, '()')
        self.assertRaisesTealError(XMLParsingError, 'empty parenthesis', Comparitor, '(a()')
        self.assertRaisesTealError(XMLParsingError, 'unmatched parenthesis', Comparitor, '(a')
        self.assertRaisesTealError(XMLParsingError, 'unmatched parenthesis', Comparitor, '(a))')
        self.assertRaisesTealError(XMLParsingError, 'unmatched parenthesis', Comparitor, '(((a))')
        self.assertRaisesTealError(XMLParsingError, 'unmatched parenthesis', Comparitor, 'a)')
        self.assertRaisesTealError(XMLParsingError, 'missing token', Comparitor, 'a&&b')
        self.assertRaisesTealError(XMLParsingError, 'missing token', Comparitor, 'a||b')
        self.assertRaisesTealError(XMLParsingError, 'missing token', Comparitor, 'a&|b')
        self.assertRaisesTealError(XMLParsingError, 'missing token', Comparitor, 'a|&b')
        myteal.shutdown()
        return 
    
#            myteal = teal.Teal('data/gear_ruleset_test/bugs/x000001/config.conf', 'stderr', msgLevel=self.msglevel, commit_alerts=False, commit_checkpoints=False)
#        myteal.shutdown()
#
#           #my_str = "[1,2] or [3,4]"
#    #my_str = "[2]"
#    #my_str = "2,27,45"
#    #my_str = "4 or [1,2 or 4,5 or [7 or 2]] or 3"
#    # my_str = "[1,2],[3,4]"
#    #my_str = "[1 or 2]"
#    ##### my_str = "[2,3,4] or [1,3,4] or [7,3]"
#    my_str = "[2,3,4],[1,3,4], [7,3] or [2] or [25, 2, [7, 8]]"
#    #my_str = "[1,2]"
#    #my_str = "3|4"
#    print my_str
#    
#    c = Comparitor(my_str, unique_loc=True)
#    print c.direct_map
#    print c
#    print 'asserted 2: ' + str(c.assert_value('2'))
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
#    print 'asserted 3: ' + str(c.assert_value('3'))
#    print c
#    print 'asserted 4: ' + str(c.assert_value('4'))
#    print c
#    print 'clear'
#    c.clear()
#    print c
#    print 'asserted 3: ' + str(c.assert_value('3'))
#    print c
#    print 'clear'
#    c.clear()
#    print c
#    print 'asserted 4: ' + str(c.assert_value('4'))
#    print c
#    print 'assert 73: ' + str(c.assert_value('73'))
#    print c
#    print 'assert 7: ' + str(c.assert_value('7'))
#    print c
#    print 'asserted 3: ' + str(c.assert_value('3'))
#    print c
#    print 'is 72 in the string? ' + str(c.in_comparison('72'))
#    print 'is 2 in the string? ' + str(c.in_comparison('2'))
#    c.clear()
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
#    print 'asserted 1: ' + str(c.assert_value('1'))
#    print c
     
class GearPermCheckerHelper(TealTestCase):
    '''Test running GEAR perm checker helper '''
    
    def test01(self):
        ''' Test 01 '''

        in_dict1 = { 'loc1':['A'],
                    'loc2':['B'],
                    'loc3':['C']
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set([]))
        return 
        
    def test02(self):
        ''' Test 02 '''

        in_dict1 = { 'loc1':['A'],
                     'loc2':['B'],
                     'loc3':['B']
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['A', 'B']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set(['A', 'B']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['A', 'B']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set(['A', 'B']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['A', 'B']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set(['A', 'B']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set([]))
        return 
        
    def test03(self):
        ''' Test 03 '''
       
        in_dict1 = { 'loc1':['A'],
                     'loc2':['B','C','D','E','F'],
                     'loc3':['B'],
                     'loc4':['B','Q'],
                     'loc5':['B']
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 5, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 6, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 4)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 5)), set(['A', 'B','C','D','E','F', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 6)), set(['A', 'B','C','D','E','F', 'Q']))
        return 
        
    def test04(self):
        ''' Test 04 '''
       
        in_dict1 = { 'loc1':['B'],  #3
                     'loc2':['B'],  #1
                     'loc3':['B'],  #2 
                     'loc4':['B', 'Q'],
                     'loc5':['B', 'Q', 'M']
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set(['B', 'M', 'Q']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 5, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 6, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 4)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 5)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 6)), set([]))
        return 
        
    def test05(self):
        ''' Test 05 '''

        in_dict1 = { 'loc1':['B'],  #3
                     'loc2':['A'],  #1
                     'loc3':['B','A', 'C']  #2 
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set(['A','B','C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 5, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 6, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 4)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 5)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 6)), set([]))
        return 
        
    def test06(self):
        ''' Test 06 '''

        in_dict1 = { 'loc1':['A'],  
                     'loc2':['A'],  
                     'loc3':['A'],  
                     'loc4':['A'],  
                     'loc5':['A'],  
                     'loc6':['A'],  
                     'loc7':['A'],  
                     'loc8':['A'],  
                     'loc9':['A']
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['A']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['A']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['A']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 5, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 6, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 4)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 5)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 6)), set([]))
        return 
        
    def test07(self):
        ''' Test 07 '''

        in_dict1 = { 'loc1':['A', 'B', 'C'],  
                     'loc2':['A', 'B', 'C'],  
                     'loc3':['A', 'B', 'C'],  
                     'loc8':['A', 'B'],  
                     'loc9':['A', 'C']
                    }
        self.assertEqual(set(_perm_checker(in_dict1, 1, 1)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 1)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 1)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 1)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 2)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 2)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 2)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 2)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 1, 3)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 2, 3)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 3, 3)), set(['A', 'B', 'C']))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 5, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 6, 3)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 4)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 5)), set([]))
        self.assertEqual(set(_perm_checker(in_dict1, 4, 6)), set([]))
        return


if __name__ == "__main__":
    unittest.main()