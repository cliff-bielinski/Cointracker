import re

def remove_punctuation(comment):
    """returns string with non-alphanumeric or whitespace characters removed"""
    return re.sub(r'[^\w\s]', '', comment)

def remove_whitespace(comment):
    """returns string with excess whitespace removed"""
    comment = re.sub(r'\s+', ' ', comment)
    return comment.strip()

def sanitize_text(comment):
    """takes string as input and returns sanitized version without punctuation, whitepace or capitalization"""
    comment = comment.lower()
    comment = remove_punctuation(comment)
    comment = remove_whitespace(comment)
    return comment