import collections
from datetime import datetime
import os
import re
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/dates/'
RSS_FEED = 'all.rss.xml'
PUB_DATE = re.compile(r'<pubDate>(.*?)</pubDate>')
TMP = '/tmp'


def _get_dates():
    """Downloads PyBites feed and parses out all pub dates returning
       a list of date strings, e.g.: ['Sun, 07 Jan 2018 12:00:00 +0100',
       'Sun, 07 Jan 2018 11:00:00 +0100', ... ]"""
    remote = os.path.join(BASE_URL, RSS_FEED)
    local = os.path.join(TMP, RSS_FEED)
    urlretrieve(remote, local)

    with open(local) as f:
        return PUB_DATE.findall(f.read())


dates = _get_dates()


def convert_to_datetime(date_str):
    """Receives a date str and convert it into a datetime object"""
    if type(date_str) == datetime:
        return date_str
    else:
        date_ = date_str.split(' +')[0]
        return datetime.strptime(date_, '%a, %d %b %Y %H:%M:%S')


def get_month_most_posts(dates):
    """Receives a list of datetimes and returns the month (format YYYY-MM)
       that occurs most"""
    dates = [datetime.strftime(convert_to_datetime(x), '%Y-%m') for x in dates]
    cnt = collections.Counter(dates)
    return cnt.most_common(1)[0][0]

