import os
import urllib.request
from collections import defaultdict

# PRE-WORK
DICTIONARY = os.path.join('../data/dictionary.txt')
if not os.path.isfile(DICTIONARY):
    urllib.request.urlretrieve('http://bit.ly/2iQ3dlZ', DICTIONARY)
scrabble_scores = [(1, "E A O I N R T L S U"), (2, "D G"), (3, "B C M P"),
                   (4, "F H V W Y"), (5, "K"), (8, "J X"), (10, "Q Z")]
LETTER_SCORES = {letter: score for score, letters in scrabble_scores
                 for letter in letters.split()}


# start coding
def load_words():
    """load the words dictionary (DICTIONARY constant) into a list and return it"""
    lists = []
    with open(DICTIONARY, encoding='utf-8') as f:
        for lines in f:
            lists.append(lines.rstrip())

    return lists


# Using LETTER_SCORES
def calc_word_value(word):
    letters = list(word)
    upped = [x.upper() for x in letters]
    score = []
    for x in upped:
        try:
            score.append(LETTER_SCORES[x])
        except KeyError:
            continue
    return sum(score)


# Using default dict and scrabble scores
def calc_word_values(word):
    """given a word calculate its value using LETTER_SCORES"""
    letters = list(word)
    upped = [x.upper() for x in letters]
    score = defaultdict(int)
    for x in upped:
        for y in range(7):
            if x in scrabble_scores[y][1]:
                score[x] += scrabble_scores[y][0]
    return sum(score.values())


# This loads
def max_word_value(words=None):
    """given a list of words return the word with the maximum word value"""
    if words is None:
        words = load_words()
    word_bank = defaultdict(int)
    for word in words:
        word_bank[word] = calc_word_values(word)
    max_ = max(word_bank, key=word_bank.get)
    return max_


