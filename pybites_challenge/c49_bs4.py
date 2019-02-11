from collections import namedtuple

from bs4 import BeautifulSoup as Soup
import requests

CONTENT = requests.get('http://bit.ly/2EN2Ntv').text

Book = namedtuple('Book', 'title description image link')


def get_book():
    """make a Soup object, parse the relevant html sections, and return a Book namedtuple"""
    soup = Soup(CONTENT, 'html.parser')
    first = soup.find('div', {'class': 'dotd-main-book-summary float-left'})
    items = [x.getText().strip() for x in first.findAll('div')[1:]]
    second = soup.find('div', {'class': 'dotd-main-book-image float-left'})
    image = second.find("img", src=True)["src"]
    link = second.find("a", href=True)["href"]
    return Book(title=items[0], description=items[1], image=image, link=link)