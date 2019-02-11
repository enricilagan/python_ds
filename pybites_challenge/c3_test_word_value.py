from c3_word_value import calc_word_value, calc_word_values, load_words, max_word_value
import pytest


@pytest.mark.parametrize("word, score", [
    ('dog', 5),
    ('cat', 5),
    ('flamingo', 14),
    ('hero', 7),
    ('Jean-Christophe', 31)
])
def test_calc_word_value(word, score):
    assert calc_word_value(word) == score


@pytest.mark.parametrize("word, score", [
    ('dog', 5),
    ('cat', 5),
    ('flamingo', 14),
    ('hero', 7),
    ('Jean-Christophe', 31)
])
def test_calc_word_values(word, score):
    assert calc_word_values(word) == score


def test_max_word_value():
    assert max_word_value(load_words()) == 'benzalphenylhydrazone'
    assert max_word_value() == 'benzalphenylhydrazone'

