import unittest
import nltk
import cointracker.sanitize


class TestSanitize(unittest.TestCase):
    """Unit Testing for text sanitization."""

    def test_sanitize(self):
        text_san = cointracker.sanitize.TextProcessing()
        test_str = "This is a test. 123   "
        mod_str = text_san.sanitize_text(test_str)
        self.assertEqual(['test', '123'], mod_str)

    def test_tokenize(self):
        text_san = cointracker.sanitize.TextProcessing()
        test_str = "This is a test. 123   "
        mod_str = text_san.tokenize(test_str)
        self.assertEqual(['this', 'is', 'a', 'test', '123'], mod_str)

    def test_whitespace(self):
        text_san = cointracker.sanitize.TextProcessing()
        test_str = "   Extra   whitespace    "
        mod_str = text_san.remove_whitespace(test_str)
        self.assertEqual('Extra whitespace', mod_str)

    def test_remove_punctuation(self):
        text_san = cointracker.sanitize.TextProcessing()
        test_str = 'No... more, punctuation!!//#^*'
        mod_str = text_san.remove_punctuation(test_str)
        self.assertEqual('No more punctuation', mod_str)


class TestProcessing(unittest.TestCase):
    """Unit testing for language processing"""
    pass