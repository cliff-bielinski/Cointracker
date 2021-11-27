import re
import nltk


class TextProcessing:
    """handles processing text of comments"""

    def __init__(self):
        """creates new TextProcessing object"""
        self.stopwords = nltk.corpus.stopwords.words('English')

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


