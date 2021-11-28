import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class TextProcessing:
    """handles processing text of comments"""

    def __init__(self):
        """creates new TextProcessing object"""
        self.stopwords = nltk.corpus.stopwords.words('English')
        self.sia = SentimentIntensityAnalyzer()

    @staticmethod
    def remove_punctuation(comment):
        """takes string and returns it with non-alphanumeric or whitespace characters removed"""
        return re.sub(r'[^\w\s]', '', comment)

    @staticmethod
    def remove_whitespace(comment):
        """takes string and returns it with excess whitespace removed"""
        comment = re.sub(r'\s+', ' ', comment)
        return comment.strip()

    @staticmethod
    def tokenize(comment):
        """takes a string and removes whitespace, capitalization and punctuation before turning string into a list"""
        words = comment.lower()
        words = TextProcessing.remove_punctuation(words)
        words = TextProcessing.remove_whitespace(words)
        words = words.split()
        return words

    def sanitize_text(self, comment):
        """takes string and tokenizes text and removes common stopwords from resultant list"""
        words = self.tokenize(comment)
        words = [word for word in words if word not in self.stopwords]
        return words

    def get_polarity_score(self, comment):
        """takes a comment (as string, not tokenized) and returns a dictionary of polarity scores"""
        return self.sia.polarity_scores(comment)

