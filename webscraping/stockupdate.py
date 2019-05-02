##################################################################################
#                   Stock Gains and Losses email sender - EJI                    #
##################################################################################
# Version                                                                        #
# 1.0 - Primary Version, Stock Gain                                              #
# 1.1 - Created Loss Version, Generates 2 emails                                 #
# 1.2 - Included HTML generation to email function                               #
# 1.3 - Combined Loss and Gain into one DataFrame for simplicity                 #
# 1.4 - Added Tweet using tweepy, will tweet the top 5 gains and losses          #
##################################################################################

# Import Packages
# import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# imported os from stocks_config
from stocks_config import *

# get the URL using pesobility site now to scrape the data
print(f'{t_stamp} Getting URL for Stocks')


# Define function to Create DataFrame for the data currently in the stock market
# Combine Gain and Losses in a Single DataFrame (Ver1.3)
# function to scrape the Stock Update table in PESOBILITY


def scrape_web(url, type_):
    r = requests.get(url)
    resp = r.text
    soup = BeautifulSoup(resp, "html.parser")
    print(f'[Scrape] <{t_stamp}>: Scraping {type_} data from Pesobility')
    return soup.table


# Function to turn scraped table to DataFrame, works only on Pesobility
# Use _type
def create_df(table_bs, _active=False):
    s = [x.findAll('td')[1].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td'))
         == (3 if _active else 4)]
    p = [x.findAll('td')[2].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td'))
         == (3 if _active else 4)]

    if not _active:
        m = [x.findAll('td')[3].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
        df = pd.DataFrame({'Stock': [a.center(5) for a in s], 'Curr Price': [a.center(8) for a in p],
                           '%Change': [a.center(7) for a in m]})
    else:
        df = pd.DataFrame({'Stock': [a.center(5) for a in s], 'Movement': [a.center(8) for a in p]})

    print(f'[DF] <{t_stamp}>: Creating dataFrame')
    return df


# Combine 2 dataframe to create a single one.
def stock_df():
    table_gain = scrape_web(GAIN_URL, "Gain")
    table_loss = scrape_web(LOSS_URL, "Loss")
    table_active = scrape_web(MOST_ACTIVE, "Loss")
    data_gain = create_df(table_gain)
    data_loss = create_df(table_loss)
    data_active = create_df(table_active, True)
    return data_gain, data_loss, data_active


# Create string to be tweeted,
# active = True will send the most active tweet else will send gain or losses
def create_tweet(df, active=False, gain_type=True):
    if active:
        t = f"[PSE] Today's Top 5 Most Active Stock:\n| Stock | Movement  |"

        for a in df[0:5].values:
            t += f'\n| {a[0].center(5)} | {a[1].center(8)} |'

    else:
        t = f"[PSE] Today's Top 5 {'Gainers' if gain_type else 'Losers'}\n| Stock | C.Price  |  %Move  |"

        for a in df[0:5].values:
            t += f'\n| {a[0].center(5)} | {a[1].center(8)} | {a[2].center(7)} |'

    return t


def send_tweet(df, test=False):
    tweets = dict()

    tweets['gain'] = create_tweet(df['gain'], False)
    tweets['loss'] = create_tweet(df['loss'], False, False)
    tweets['active'] = create_tweet(df['active'], True)

    if test:
        logging.info(f"Test: tweet to send Most Active:\n {tweets['active']}, {len(tweets['active'])}")
        logging.info(f"Test: tweet to send Gainers:\n {tweets['gain']}, {len(tweets['gain'])}")
        logging.info(f"Test: tweet to send Losers:\n {tweets['loss']}, {len(tweets['loss'])}")
        print('Tweet logged in stock_update.log')

    else:
        try:
            api.update_status(tweets['active'])
            api.update_status(tweets['gain'])
            api.update_status(tweets['loss'])
            logging.info(f"Posted Top Movements to Twitter")
        except Exception as exc:
            logging.error(f'Error posting to Twitter: {exc}')


# Create file, separate it from compose email for testing
def create_body(df, test=False):
    # Create gain and loss data frames (Ver1.2)
    # added stock_df inside the function to make script cleaner
    print(f'[E-mail] <{t_stamp}>: Creating email content')

    if not test:
        with open('update.html', 'w') as f:
            f.write(head + er)
            f.write(df['active'][0:10].to_html(classes='df', index=False, border=2, col_space=12, justify='center'))
            f.write(gain + er)
            f.write(df['gain'][0:15].to_html(classes='df', index=False, border=2, col_space=12, justify='center'))
            f.write(loss + er)
            f.write(df['loss'][0:15].to_html(classes='df', index=False, border=2, col_space=12, justify='center'))
            f.write(er + footer)

        # Create secure connection with server and send email via TLS
        with open('update.html', 'r') as f:
            return MIMEText(f.read(), 'html')


# Send email function
def send_mail(df, test=False):
    """
    composes email to be sent.
    """
    if test:
        print("Test Run, will not send email")

    else:
        # Login user and recipients
        gmail_user = user_email
        gmail_password = user_pass
        recipient = email_rec
        msg = MIMEMultipart()
        msg['From'] = "Enric's PSE Update"
        msg['To'] = recipient
        msg['Subject'] = f"PSE Stock Update as of {today}"

        attachment = create_body(df, test)

        msg.attach(attachment)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(
                gmail_user, recipient, msg.as_string()
            )
        print(f'[E-mail] <{t_stamp}>: Sending Email, TLS')

        # delete file Update.html
        os.remove("update.html")
        print(f"[File] <{t_stamp}>: Removing Update.html")


# use t to create test and log the tweet instead
def main():
    df = dict()
    df['gain'], df['loss'], df['active'] = stock_df()

    t = 's'  # input('[t]est and log or [s]end mail and tweet: ')
    test = True if t == 't' else False

    send_tweet(df, test)
    send_mail(df, test)

    print(f'[E-mail] <{t_stamp}> Email sent!')


if __name__ == '__main__':
    main()
