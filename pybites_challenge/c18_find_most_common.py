import os
import urllib.request
from collections import Counter
import re

# data provided
stopwords_file = os.path.join('/tmp', 'stopwords')
harry_text = os.path.join('/tmp', 'harry')
if not os.path.isfile(stopwords_file):
    urllib.request.urlretrieve('http://bit.ly/2EuvyHB', stopwords_file)
if not os.path.isfile(harry_text):
    urllib.request.urlretrieve('http://bit.ly/2C6RzuR', harry_text)


def get_harry_most_common_word():
    with open(harry_text, encoding='utf-8') as f:
        harry = f.read()

    with open(stopwords_file, encoding='utf-8') as f:
        stopwords = f.read()

    words = harry.lower().split()
    words = [re.sub(r'\W+', r'', word) for word in words]
    stopwords = stopwords.lower().split()
    words = [word for word in words if word.strip() and word not in stopwords]
    cnt = Counter(words)
    return cnt.most_common(1)[0]


print(get_harry_most_common_word())