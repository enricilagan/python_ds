import re


def remove_punctuation(input_string):
    """Return a str with punctuation chars stripped out"""
    return ''.join(re.findall(r'[A-Za-z0-9 ]', input_string))
