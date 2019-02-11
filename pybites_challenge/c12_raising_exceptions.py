from collections import namedtuple

User = namedtuple('User', 'name role expired')
USER, ADMIN = 'user', 'admin'
SECRET = 'I am a very secret token'

julian = User(name='Julian', role=USER, expired=False)
bob = User(name='Bob', role=USER, expired=True)
pybites = User(name='PyBites', role=ADMIN, expired=False)
USERS = (julian, bob, pybites)


# define exception classes here

def get_secret_token(username):
    for x in USERS:
        if username == x.name:
            if not x.expired:
                if x.role == ADMIN:
                    return SECRET
                else:
                    raise UserNoPermission
            else:
                raise UserAccessExpired

    raise UserDoesNotExist


class UserNoPermission(Exception):
    """ Weak ref proxy used after referent went away. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class UserAccessExpired(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class UserDoesNotExist(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

