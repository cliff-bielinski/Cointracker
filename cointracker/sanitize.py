import re

def remove_punctuation(comment):
    """takes string and returns it with non-alphanumeric or whitespace characters removed"""
    return re.sub(r'[^\w\s]', '', comment)

def remove_whitespace(comment):
    """takes string and returns it with excess whitespace removed"""
    comment = re.sub(r'\s+', ' ', comment)
    return comment.strip()

def sanitize_text(comment):
    """takes string and returns a tokenized list of words without punctuation, whitepace or capitalization"""
    comment = comment.lower()
    comment = remove_punctuation(comment)
    comment = remove_whitespace(comment)
    comment = comment.split()
    return comment