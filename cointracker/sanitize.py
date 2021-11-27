import re
import nltk


class TextProcessing:
    """handles processing text of comments"""

    def __init__(self):
        """creates new TextProcessing object"""
        pass

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
    def sanitize_text(comment):
        """takes string and returns a tokenized list of words without punctuation, whitespace or capitalization"""
        comment = comment.lower()
        comment = TextProcessing.remove_punctuation(comment)
        comment = TextProcessing.remove_whitespace(comment)
        comment = comment.split()
        return comment


