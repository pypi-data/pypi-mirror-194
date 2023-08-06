import unittest

from src.simple_nlp_library.preprocessing import remove_multiple_spaces, leave_only_uncased_letters, remove_stop_words, \
    retrieve_semantic_tokens


class TestPreprocessing(unittest.TestCase):
    def test_remove_multiple_spaces(self):
        self.assertEqual(
            remove_multiple_spaces('The  quick \t brown \n fox jumps'),
            'The quick brown fox jumps'
        )

    def test_leave_only_uncased_letters(self):
        self.assertEqual(
            leave_only_uncased_letters('The quick brown fox jumps!'),
            'the quick brown fox jumps'
        )

    def test_remove_stop_words(self):
        self.assertEqual(
            remove_stop_words(['the', 'quick', 'brown', 'fox', 'jumps']),
            ['quick', 'brown', 'fox', 'jumps']
        )

    def test_retrieve_semantic_tokens(self):
        self.assertEqual(
            retrieve_semantic_tokens('The  quick \t brown fox jumps, over the lazy dog!'),
            ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']
        )
