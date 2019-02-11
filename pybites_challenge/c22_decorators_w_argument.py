from functools import wraps


def make_html(element):
    def create(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            '<' + element + '>'
            result = func(*args, **kwargs)
            return '<' + str(element) + '>' + str(result) + '</' + str(element) + '>'

        return wrapper

    return create



@make_html('p')
@make_html('strong')
def get_text(text='I code with PyBites'):
    return text


# Using Partial
from functools import wraps, partial


def make_html(func=None, *, element=None):
    if func is None:
        return partial(make_html, element=element)
    element = element if element else 'p'

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return '<' + str(element) + '>' + result + '</' + str(element) + '>'

    return wrapper


@make_html
@make_html(element='strong')
def get_text(text='I code with PyBites'):
    return str(text)
