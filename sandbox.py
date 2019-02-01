import pandas as pd
import tweepy   # twitter API

from passes import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_TOKEN

# Edit the USERNAME before running the script
USERNAME = 'creingalain'

# Import the Keys and Secret


# API setup
def twitter_set():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api


# We create an extractor object to extract the tweets:
extractor = twitter_set()

# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name=USERNAME)
print(f'Number of tweets extracted: {len(tweets)} \n')

print(extractor.user_timeline(screen_name=USERNAME))