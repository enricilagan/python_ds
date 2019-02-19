import datetime
from programs.config import logging, api, lessons

T_ZONE = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(T_ZONE)
start = datetime.datetime(2018, 12, 20, tzinfo=T_ZONE)  # = PyBites 100 days :)

CURRENT_CHALLENGE_DAY = (now - start - datetime.timedelta(days=1)).days
TWEET_LEN = 280

if CURRENT_CHALLENGE_DAY % 3 == 1:
    d, part = '1', 'lecture'
elif CURRENT_CHALLENGE_DAY % 3 == 2:
    d, part = '2', 'practice'
elif CURRENT_CHALLENGE_DAY % 3 == 0:
    d, part = '3', 'more coding'

s = int((CURRENT_CHALLENGE_DAY+2)/3)


def main():
    tweet = ''
    a = 'Not Done'
    while a == 'Not Done':
        comment = input("Enter Comment for today's progress: \n")
        tweet, a = create_tweet(comment)

    print(f'Tweet length: {len(tweet)}')

    t = input("Do you want to [p]ost tweet or [l]og it: ")
    test = True if t == 'p' else False

    if not test:
        logging.info('Test: tweet to send: {}'.format(tweet))
        print('Tweet logged in 100day_tweet_bot.log')
    else:
        tweet_status(tweet)
        print('Tweet posted!')


def create_tweet(comment):
    ht1, ht2 = '#100DaysOfCode', '#Python'
    acc1, acc2 = '@pybites', '@talkpython'
    title = lessons[s]
    day = str(CURRENT_CHALLENGE_DAY)

    url = 'https://talkpython.fm/100days?s=pybites'
    allowed_len = TWEET_LEN

    if day == '100':
        comment = 'Done with first round of 100 days of code, will take a break then do R2.'
        fmt = 'Day {}: I completed the 100 days of Code in Python course by {} {}! {} {} {} {} #milestone'
        tweet = fmt.format(day, acc1, acc2, comment, url, ht1, ht2)
    elif day == '1':
        fmt = 'Day {}: {} progress: Finally starting today! Today I worked on {} / D{} ({}), {} {} {} {} {}'
        tweet = fmt.format(day, ht1, title, d, part, comment, url, ht2, acc1, acc2)
    else:
        fmt = 'Day {}: {} progress: today I worked on {} / D{} ({}), {} {} {} {} {}'
        tweet = fmt.format(day, ht1, title, d, part, comment, url, ht2, acc1, acc2)

    a = 'Done'

    if len(tweet) > allowed_len:
        print('Tweet Length not allowed, tweet too long.')
        a = 'Not Done'

    return tweet, a


def tweet_status(tweet):
    try:
        api.update_status(tweet)
        logging.info('Posted to Twitter')
    except Exception as exc:
        logging.error('Error posting to Twitter: {}'.format(exc))


if __name__ == '__main__':
    main()
