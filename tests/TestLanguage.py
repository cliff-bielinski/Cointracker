import unittest
import nltk
import cointracker.sanitize


class TestSanitize(unittest.TestCase):
    """Unit Testing for text sanitization."""

    def test_sanitize(self):
        test_str = "This is a test. 123   "
        mod_str = cointracker.sanitize.sanitize_text(test_str)
        self.assertEqual(['this', 'is', 'a', 'test', '123'], mod_str)

    def test_whitespace(self):
        test_str = "   Extra   whitespace    "
        mod_str = cointracker.sanitize.remove_whitespace(test_str)
        self.assertEqual('Extra whitespace', mod_str)

    def test_remove_punctuation(self):
        test_str = 'No... more, punctuation!!//#^*'
        mod_str = cointracker.sanitize.remove_punctuation(test_str)
        self.assertEqual('No more punctuation', mod_str)


class TestProcessing(unittest.TestCase):
    """Unit testing for language processing"""
    pass