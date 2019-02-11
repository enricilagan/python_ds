import csv
from collections import defaultdict, namedtuple
import os
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/movies/'
fname = 'data/movie_metadata.csv'
remote = os.path.join(BASE_URL, fname)

if os.path.isfile(fname):
    local = os.path.join(fname)
else:
    local = os.path.join(fname)
    urlretrieve(remote, local)

MOVIE_DATA = local
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    directors = defaultdict(list)
    with open(local, encoding='utf-8') as f:  # open data for default movies, this is the dataset we retrieved
        for line in csv.DictReader(f):
            try:
                drctr = line['director_name']
                movie = line['movie_title'].replace('\xa0', '')
                year = int(line['title_year'])
                score = float(line['imdb_score'])
            except ValueError:  # use except to ignore empty rows or bad data.
                continue
            if year > MIN_YEAR:
                values_ = Movie(title=movie, year=year, score=score)  # creates a namedtuple Movie
                directors[drctr].append(values_)  # inserts all values of the CSV into a dictionary

    return directors


def calc_mean_score(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    score = 0
    for movie in range(len(movies)):
        score = score + movies[movie][2]
    return round((score/len(movies)), 1)


def get_average_scores(directors=None):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    if directors is None:
        directors = get_movies_by_director()
    Ave = namedtuple('Score', 'director score')
    avg_score = [Ave(director=keys, score=calc_mean_score(directors[keys]))
                 for keys in directors.keys() if len(directors[keys]) >= MIN_MOVIES]
    avg_scores = sorted(avg_score, key=lambda x: x.score, reverse=True)
    return avg_scores


print(get_average_scores())
