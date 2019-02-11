import string
import random
from secrets import choice


def gen_key(parts=4, chars_per_part=8):
    part = []
    chars = string.ascii_uppercase + string.digits
    for _ in range(parts):
        part.append(''.join([random.choice(chars) for _ in range(chars_per_part)]))
    return '-'.join(part)


def secret_key(parts=4, chars_per_part=8):
    part = []
    chars = string.ascii_uppercase + string.digits
    return '-'.join(''.join(choice(chars)
                            for _ in range(chars_per_part))
                    for _ in range(parts))
