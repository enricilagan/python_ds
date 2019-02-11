import itertools
import os
import urllib.request
from collections import defaultdict

# PRE-WORK
DICTIONARY = os.path.join('../data/dictionary.txt')
if not os.path.isfile(DICTIONARY):
    urllib.request.urlretrieve('http://bit.ly/2iQ3dlZ', DICTIONARY)

with open(DICTIONARY) as f:
    dictionary = set([word.strip().lower() for word in f.read().split()])

# Included the codes in Byte 3
scrabble_scores = [(1, "E A O I N R T L S U"), (2, "D G"), (3, "B C M P"),
                   (4, "F H V W Y"), (5, "K"), (8, "J X"), (10, "Q Z")]
LETTER_SCORES = {letter: score for score, letters in scrabble_scores
                 for letter in letters.split()}


def load_words():
    """load the words dictionary (DICTIONARY constant) into a list and return it"""
    with open(DICTIONARY, encoding='utf-8') as f:
        return set([word.strip().lower() for word in f.read().split()])


print(load_words())


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


def max_word_value(words=None):
    """given a list of words return the word with the maximum word value"""
    if words is None:
        words = load_words()
    word_bank = defaultdict(int)
    for word in words:
        word_bank[word] = calc_word_values(word)
    max_ = max(word_bank, key=word_bank.get)
    return max_


# Code for this bite
def _get_permutations_draw(draw):
    """Helper to get all permutations of a draw (list of letters), hint:
       use itertools.permutations (order of letters matters)"""
    lst = []
    for i in range(1, len(draw)):
        lst += list(itertools.permutations(draw, r=i))
    return set([''.join(a).lower() for a in lst])


def get_possible_dict_words(draw):
    """Get all possible words from a draw (list of letters) which are
       valid dictionary words. Use _get_permutations_draw and provided
       dictionary"""
    words = _get_permutations_draw(draw)
    return [word for word in words if word in dictionary]


# Additional: will get max word value with score
def max_possible_word(draw):
    word = max_word_value(get_possible_dict_words(draw))
    return {word: calc_word_value(word)}

