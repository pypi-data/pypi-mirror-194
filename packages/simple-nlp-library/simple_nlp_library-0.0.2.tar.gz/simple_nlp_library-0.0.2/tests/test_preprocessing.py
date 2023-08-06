import unittest

from src.simple_nlp_library.preprocessing import remove_multiple_spaces, leave_only_uncased_letters


class TestPreprocessing(unittest.TestCase):
    def test_remove_multiple_spaces(self):
        self.assertEqual(remove_multiple_spaces('The  quick \t brown \n fox jumps'), 'The quick brown fox jumps')

    def test_leave_only_uncased_letters(self):
        self.assertEqual(leave_only_uncased_letters('The quick brown fox jumps!'), 'the quick brown fox jumps')
