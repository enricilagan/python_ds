import random

names = 'Julian Bob PyBites Dante Martin Rodolfo'.split()
aliases = 'Pythonista Nerd Coder'.split() * 2
points = random.sample(range(81, 101), 6)
awake = [True, False] * 3
SEPARATOR = ' | '


def generate_table(*args):
    lst = [*args]
    lst = [[str(y) for y in x] for x in lst]
    lst = list(zip(*lst))
    return [SEPARATOR.join(x) for x in lst]