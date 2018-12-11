import unittest
from unittest.mock import patch, call, ANY, Mock
from snowboy.wakeword import Wakeword

def glob_side_effect (arg): 
    pmdl_mask = '/models/*.pmdl'
    umdl_mask = '/models/*.umdl'
    return ['foo.pmdl', 'bar.pmdl'] if pmdl_mask in arg else ['baz.umdl'] if umdl_mask in arg else None

class TestWakewordMatcher(unittest.TestCase):
    def setUp(self):
        self.callback = Mock()
        
    @patch('snowboy.wakeword.glob')
    @patch('snowboy.wakeword.HotwordDetector')
    def test_constructor(self, mock_detector, mock_glob):
        '''
        constructor calls HotwordDetector with correct params
        '''
        mock_glob.side_effect = glob_side_effect
        
        Wakeword(self.callback, 0.25)
        
        mock_detector.assert_called_with(['foo.pmdl', 'bar.pmdl', 'baz.umdl'], sensitivity=[0.25, 0.25, 0.25])
        
    @patch('snowboy.wakeword.glob')
    @patch('snowboy.wakeword.HotwordDetector')
    def test_constructor_default_sensitivity(self, mock_detector, mock_glob):
        '''
        constructor defaults sensitivity to 0.5
        '''
        mock_glob.side_effect = glob_side_effect
        
        Wakeword(self.callback)
        
        mock_detector.assert_called_with(['foo.pmdl', 'bar.pmdl', 'baz.umdl'], sensitivity=[0.5, 0.5, 0.5])        
        
    @patch('snowboy.wakeword.glob')
    @patch('snowboy.wakeword.HotwordDetector')
    def test_listen_calls_start_and_terminate(self, mock_detector, mock_glob):
        '''
        listen() sets listening to true and calls detector.start() (thread-blocking) and
        terminate when start() finishes
        '''
        instance = mock_detector.return_value
        mock_glob.side_effect = glob_side_effect
        wakeword = Wakeword(self.callback)
        
        wakeword.listen()
        
        instance.start.assert_called_with(detected_callback=ANY, interrupt_check=ANY, sleep_time=0.03)
        instance.terminate.assert_called_with()
    
    @patch('snowboy.wakeword.glob')
    @patch('snowboy.wakeword.HotwordDetector')        
    def test_callback_invoke(self, mock_detector, mock_glob):
        '''
        callback gets called with the name of detected model when invoked with the corresponding ordinal in start()
        '''
        instance = mock_detector.return_value
        mock_glob.side_effect = glob_side_effect
        instance.start.side_effect = lambda detected_callback, interrupt_check, sleep_time: detected_callback(2)
        wakeword = Wakeword(self.callback)
        
        wakeword.listen()
        
        self.callback.assert_called_with('bar.pmdl')
        
        
        
if __name__ == '__main__':
    unittest.main()        
    
    
    
    