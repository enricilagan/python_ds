import day9 as d
import pytest


def test_get_every_nth_state():
    assert d.get_every_nth_state() == \
           ['Massachusetts', 'Missouri', 'Hawaii', 'Vermont', 'Delaware']


@pytest.mark.parametrize("state, abv",[
    ('Alabama', 'AL'),
    ('Ohio', 'OH'),
    ('Michigan', 'MI'),
    ('Philippines', 'N/A')
])
def test_get_state_abbrev(state, abv):
    assert d.get_state_abbrev(state) == abv


def test_get_longest_state():
    assert d.get_longest_state(d.us_state_abbrev) == 'North Carolina'
    assert d.get_longest_state(d.states) == 'North Carolina'


def test_combine_state_names_and_abbreviations():
    assert d.combine_state_names_and_abbreviations(d.us_state_abbrev, d.states) \
           == ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
               'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
               'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
