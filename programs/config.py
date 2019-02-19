import logging
import os

import tweepy

"""
to run this in a virtual environment, make sure that the TWITTER_KEY and SECRET and the ACCESS_KEY and SECRET 
are stored in the activate file. To run this in Pycharm, copy and paste the keys into the environment variables
in edit config.
"""

TWITTER_KEY = os.environ["TWITTER_KEY"]
TWITTER_SECRET = os.environ["TWITTER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["ACCESS_SECRET"]

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filename='100day_autotweet.log',
                    filemode='a')

lessons = {1: 'Playing with Datetimes', 2: 'Collections module', 3: 'Python Data Structures',
           4: 'Testing your code with pytest', 5: 'Text-based games (and classes)',
           6: 'List comprehensions and generators', 7: 'Iteration with itertools', 8: 'Decorators',
           9: 'Error Handling', 10: 'Regular Expressions', 11: 'Logging', 12: 'Refactoring', 13: 'Using CSV data',
           14: 'JSON in Python', 15: 'Consuming HTTP services', 16: 'Web Scraping with BeautifulSoup4',
           17: 'Measuring performance', 18: 'Parsing RSS feeds with Feedparser',
           19: 'Structured API clients with uplink', 20: 'Twitter data analysis with Python',
           21: 'Using the Github API with Python', 22: 'Sending emails with smtplib',
           23: 'Copy and Paste with Pyperclip', 24: 'Excel automation with openpyxl',
           25: 'Automate tasks with Selenium', 26: 'Getting Started with Python Flask',
           27: 'Basic Database Access with SQLite3', 28: 'Data visualization with Plotly',
           29: 'Fullstack web apps made easy', 30: 'Home Inventory App', 31: 'Database access with SQLAlchemy',
           32: 'Rich GUI apps in Python', 33: 'Building JSON APIs'}
