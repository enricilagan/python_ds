import re

html = ('<p>pybites != greedy</p>'
        '<p>not the same can be said Regarding ...</p>')

from functools import wraps, partial

def get_border(func=None, count=10):
    if func is None:
        return partial(get_border, count=count)
    count = count if count else 2

    @wraps(func)
    def wrapper(*args, **kwargs):
        return ('==' * count) + '\n\n' + func(*args, **kwargs) + '\n\n' + ('==' * count) + '\n'
    return wrapper


@get_border(count=10)
def generate_xmas_tree(rows=10):
    """Generate a xmas tree of stars (*) for given rows (default 10).
       Each row has row_number*2-1 stars, simple example: for rows=3 the
       output would be like this (ignore docstring's indentation):
         *
        ***
       *****"""
    sp = rows
    word = ''
    for i in range(rows):
        row = ((i+1) * 2) - 1
        space = (sp) - 1
        sp -= 1
        star = (' ' * space) + ('*' * row) + '{}'.format('\n' if i < rows-1 else '')
        word = word + star
    return word


print(generate_xmas_tree())

