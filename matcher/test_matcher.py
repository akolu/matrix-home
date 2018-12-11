import unittest
from .matcher import PhraseMatcher

phrases = ['Atlanta Falcons', 'New York Jets', 'Dallas Cowboys']

class TestPhraseMatcher(unittest.TestCase):
    def setUp(self):
        pass

    def test_class_default_phrases(self):
        '''
        PhraseMatcher defaults phrases array to empty
        '''
        matcher = PhraseMatcher()
        self.assertEqual(matcher.phrases, [])
    
    def test_class_default_threshold(self):
        '''
        PhraseMatcher defaults threshold to 0
        '''
        matcher = PhraseMatcher()
        self.assertEqual(matcher.threshold, 0)
    
    def test_match_success(self):
        '''
        match() returns matchin phrase when probability is over threshold
        '''
        matcher = PhraseMatcher(phrases)
        result = matcher.match('york new jets')
        self.assertEqual(result, 'New York Jets')
    
    def test_match_fail(self):
        '''
        match() returns null when probability of highest match is below threshold
        '''
        matcher = PhraseMatcher(phrases, 100)
        result = matcher.match('york new jets')
        self.assertEqual(result, None)
    
    def test_match_no_phrases(self):
        '''
        match() returns given phrase (exact match) if phrases list is empty
        '''
        matcher = PhraseMatcher()
        result = matcher.match('york new jets')
        self.assertEqual(result, 'york new jets')
        
    def test_match_none(self):
        '''
        match() returns None if given phrase is None
        '''
        matcher = PhraseMatcher(phrases)
        result = matcher.match(None)
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()
