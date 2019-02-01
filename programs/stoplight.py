import itertools
import random
from time import sleep
import sys


colors = 'Red Green Amber'.split()
traffic = itertools.cycle(colors)


def rand_timer():
    return random.randint(2, 10)


def traffic_light(traf):
    for x in traf:
        if x == 'Amber':
            sys.stdout.write('\r' + 'Caution! Light is {}'.format(x))
            sys.stdout.flush()
            sleep(3)
        elif x == 'Red':
            sys.stdout.write('\r' + 'Stop! {} Light'.format(x))
            sys.stdout.flush()
            sleep(rand_timer())
        elif x == 'Green':
            sys.stdout.write('\r' + 'Go! Light is {}!!!'.format(x))
            sys.stdout.flush()
            sleep(rand_timer())


if __name__ == '__main__':
    traffic_light(traffic)



