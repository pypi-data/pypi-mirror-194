import unittest

from src.simple_nlp_library.preprocessing import remove_multiple_spaces


class TestPreprocessing(unittest.TestCase):
    def test_remove_multiple_spaces(self):
        self.assertEqual(remove_multiple_spaces('The  quick \t brown \n fox jumps'), 'The quick brown fox jumps')
