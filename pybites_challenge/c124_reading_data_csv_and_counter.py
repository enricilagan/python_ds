from collections import namedtuple, Counter
import csv
import re

import requests

MARVEL_CSV = 'https://raw.githubusercontent.com/pybites/marvel_challenge/master/marvel-wikia-data.csv'  # noqa E501

Character = namedtuple('Character', 'pid name sid align sex appearances year')

# csv parsing code provided so this Bite can focus on the parsing


def _get_csv_data():
    """Download the marvel csv data and return its decoded content"""
    with requests.Session() as session:
        return session.get(MARVEL_CSV).content.decode('utf-8')


def load_data():
    """Converts marvel.csv into a sequence of Character namedtuples
       as defined above"""
    content = _get_csv_data()
    reader = csv.DictReader(content.splitlines(), delimiter=',')
    for row in reader:
        name = re.sub(r'(.*?)\(.*', r'\1', row['name']).strip()
        yield Character(pid=row['page_id'],
                        name=name,
                        sid=row['ID'],
                        align=row['ALIGN'],
                        sex=row['SEX'],
                        appearances=row['APPEARANCES'],
                        year=row['Year'])


data = list(load_data())


# start coding

def most_popular_characters(top=5):
    """Get the most popular character by number of appearances,
       return top n characters (default 5)"""
    lst = [(x.name, int(x.appearances)) for x in data if x.appearances.isdigit()]
    return [x for x, y in lst][:top]


def max_and_min_years_new_characters():
    """Get the year with most and least new characters introduced respectively,
       use either the 'FIRST APPEARANCE' or 'Year' column in the csv data, or
       the 'year' attribute of the namedtuple, return a tuple of
       (max_year, min_year)"""
    cnt = Counter(x.year for x in data if x.year)
    return cnt.most_common()[0][0], cnt.most_common()[-1][0]


def percentage_female():
    """Get the percentage of female characters as percentage of all genders,
       return a percentage rounded to 2 digits"""
    lst = [x.sex.split(' ')[0] for x in data]
    cnt = Counter(lst)
    return round((cnt.most_common()[1][1] / sum(cnt.values()))*100, 2)
