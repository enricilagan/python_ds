"""A palindrome is a word, phrase, number, or other sequence of characters
which reads the same backward as forward"""
import os
import re
import urllib.request

DICTIONARY = os.path.join('/tmp', 'dictionary_m_words.txt')
urllib.request.urlretrieve('http://bit.ly/2Cbj6zn', DICTIONARY)


def load_dictionary():
    """Load dictionary (sample) and return as generator (done)"""
    with open(DICTIONARY) as f:
        return (word.lower().strip() for word in f.readlines())


def is_palindrome(word):
    """Return if word is palindrome, 'madam' would be one.
       Case insensitive, so Madam is valid too.
       It should work for phrases too so strip all but alphanumeric chars.
       So "No 'x' in 'Nixon'" should pass (see tests for more)"""
    regex = re.compile('\W', re.UNICODE)
    word = regex.sub('', word).lower()
    letters = list(word)
    reverse = [x for x in reversed(letters)]
    reverse = ''.join(reverse)
    return reverse == word


def get_longest_palindrome(words=None):
    """Given a list of words return the longest palindrome
       If called without argument use the load_dictionary helper
       to populate the words list"""
    if words is None:
        words = load_dictionary()
    lst = []
    for x in words:
        if is_palindrome(x):
            lst.append(x)
    return sorted(lst)[0]

print(get_longest_palindrome())