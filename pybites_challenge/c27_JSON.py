import glob
import json
import os
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/omdb/'
MOVIES = ('bladerunner2049 fightclub glengary '
          'horrible-bosses terminator').split()
TMP = '/tmp'

# little bit of prework (yes working on pip installables ...)
for movie in MOVIES:
    fname = f'{movie}.json'
    remote = os.path.join(BASE_URL, fname)
    local = os.path.join(TMP, fname)
    urlretrieve(remote, local)

files = glob.glob(os.path.join(TMP, '*json'))


def get_movie_data(files=files):
    lst = []
    for x in files:
        with open(x) as f:
            lst.append(json.load(f))
    return lst


def get_single_comedy(movies):
    return [x['Title'] for x in movies if 'Comedy' in x['Genre']][0]


def get_movie_most_nominations(movies):
    movie_sorted = sorted(movies, key=lambda r: int(r['Awards'].split(' ')[-2:-1][0]), reverse=True)
    return movie_sorted[0]['Title']


def get_movie_longest_runtime(movies):
    movie_sorted = sorted(movies, key=lambda r: int(r['Runtime'].split(' ')[0]), reverse=True)
    return movie_sorted[0]['Title']
