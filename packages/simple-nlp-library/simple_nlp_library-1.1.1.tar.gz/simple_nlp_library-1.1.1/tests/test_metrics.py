import unittest

from src.simple_nlp_library.metrics import (
    dot_product,
    frobenius_norm,
    cosine_similarity,
    inserting_distance,
    inserting_similarity,
)


class TestMetrics(unittest.TestCase):
    def test_dot_product(self):
        self.assertEqual(dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]), 32)

    def test_frobenius_norm(self):
        self.assertEqual(frobenius_norm([1.0, 1.0, 1.0, 2.0, 3.0]), 4.0)

    def test_cosine_similarity(self):
        self.assertAlmostEqual(
            cosine_similarity([1.0, 1.0, 1.0], [4.0, 4.0, 4.0]), 1.0, 1
        )

    def test_inserting_distance(self):
        self.assertEqual(inserting_distance("simple", "simple"), 0)
        self.assertEqual(inserting_distance("simple", "simpler"), 1)
        self.assertEqual(inserting_distance("easy", "hard"), 4)

    def test_inserting_similarity(self):
        self.assertEqual(inserting_similarity("simple", "simple"), 1.0)
        self.assertEqual(inserting_similarity("simple", "simpler"), 1.0 - 1 / 7)
        self.assertEqual(inserting_similarity("easy", "hard"), 0.0)
