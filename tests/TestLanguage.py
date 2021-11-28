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

    def test_get_polarity_scores(self):
        reddit_comment = """Fuck me it just keeps dipping. The only positive is that at least people will stop taking 
        plan b's ridiculous predictions based on made up bullshit seriously now."""
        text_san = cointracker.sanitize.TextProcessing()
        pol_score = text_san.get_polarity_score(reddit_comment)
        print(pol_score)


class TestProcessing(unittest.TestCase):
    """Unit testing for language processing"""
    pass