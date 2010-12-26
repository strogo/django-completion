from completion.tests.base import AutocompleteTestCase
from completion.utils import clean_phrase, partial_complete, create_key


class UtilsTestCase(AutocompleteTestCase):
    def setUp(self):
        pass
    
    def test_clean_phrase(self):
        self.assertEqual(clean_phrase('abc def ghi'), ['abc', 'def', 'ghi'])
        
        self.assertEqual(clean_phrase('a A tHe an a'), [])
        self.assertEqual(clean_phrase(''), [])
        
        self.assertEqual(
            clean_phrase('The Best of times, the blurst of times'),
            ['best', 'of', 'times,', 'blurst', 'of', 'times'])
    
    def test_partial_complete(self):
        self.assertEqual(list(partial_complete('1')), ['1'])
        self.assertEqual(list(partial_complete('1 2')), ['1 2'])
        self.assertEqual(list(partial_complete('1 2 3')), ['1 2 3'])
        self.assertEqual(list(partial_complete('1 2 3 4')), ['1 2 3', '2 3 4'])
        self.assertEqual(list(partial_complete('1 2 3 4 5')), ['1 2 3', '2 3 4', '3 4 5'])
        
        self.assertEqual(
            list(partial_complete('The Best of times, the blurst of times')),
            ['best of times,', 'of times, blurst', 'times, blurst of', 'blurst of times'])
        
        self.assertEqual(list(partial_complete('a the An')), [''])
        self.assertEqual(list(partial_complete('a')), [''])
    
    def test_create_key(self):
        self.assertEqual(
            create_key('the best of times, the blurst of Times'),
            'bestoftimes')
        
        self.assertEqual(create_key('<?php $bling; $bling; ?>'),
            'phpblingbling')
        
        self.assertEqual(create_key(''), '')
        
        self.assertEqual(create_key('the a an'), '')
        self.assertEqual(create_key('a'), '')
