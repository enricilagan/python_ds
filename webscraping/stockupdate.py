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
import ssl
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
	print(f'{t_stamp} Scraping {type_} data from Pesobility')
	return soup.table


# function to turn scraped table to DataFrame, works only on Pesobility
def create_df(table_bs):
	s = [x.findAll('td')[1].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
	p = [x.findAll('td')[2].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
	m = [x.findAll('td')[3].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
	df = pd.DataFrame({'Stock': s, 'Current Price': p, '% Movement': m})
	print(f'{t_stamp} Creating dataFrame')
	return df


# Combine 2 dataframe to create a single one.
def stock_df(url_gain, url_loss):
	table1 = scrape_web(url_gain, "Gain")
	table2 = scrape_web(url_loss, "Loss")
	data1 = create_df(table1)
	data2 = create_df(table2)
	return data1, data2


def create_tweet(df, gain=True):
	t = f"[TEST]: Today's Top 5 {'Gainers' if gain else 'Losers'}\n| Stock | C.Price  |  %Move  |"
	for a in df[0:5].values:
		t += f'\n| {a[0].center(5)} | {a[1].center(8)} | {a[2].center(7)} |'
	return t


def send_tweet(tweet, gain=True):
	try:
		api.update_status(tweet)
		logging.info(f"Posted Top {'Gainers' if gain else 'Losers'} to Twitter")
	except Exception as exc:
		logging.error(f'Error posting to Twitter: {exc}')


# Send email function
def send_mail(df_gain, df_loss):
	"""
	composes email to be sent.
	"""
	# Login user and recipients
	gmail_user = EMAIL_USER
	gmail_password = EMAIL_PW
	recipient = EMAIL_REC
	msg = MIMEMultipart()
	msg['From'] = gmail_user
	msg['To'] = recipient
	msg['Subject'] = f"PSE Stock Update as of {today}"

	# Create gain and loss data frames (Ver1.2)
	print(f'{t_stamp} Assembling email content')
	with open('update.html', 'w') as f:
		f.write(head + er)
		f.write(df_gain[0:15].to_html(classes='df'))
		f.write(loss + er)
		f.write(df_loss[0:15].to_html(classes='df'))
		f.write(er + footer)

	with open('update.html', 'r') as f:
		attachment = MIMEText(f.read(), 'html')

	msg.attach(attachment)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(gmail_user, gmail_password)
		server.sendmail(
			gmail_user, recipient, msg.as_string()
		)
		print(f'{t_stamp} Sending Email, SSL')

	# delete file Update.html
	os.remove("update.html")
	print("Removing Update.html")


def main():
	test = input('[t]est and log or [s]end mail and tweet: ')
	df_gain, df_loss = stock_df(GAIN_URL, LOSS_URL)
	gain_tweet = create_tweet(df_gain)
	loss_tweet = create_tweet(df_loss, False)
	if test == 't':
		logging.info(f'Test: tweet to send Gainers:\n {gain_tweet}, {len(gain_tweet)}')
		logging.info(f'Test: tweet to send Losers\n {loss_tweet}, {len(loss_tweet)}')
		print('Tweet logged in stock_update.log')
	else:
		send_tweet(gain_tweet)
		send_tweet(loss_tweet, False)
		send_mail(df_gain, df_loss)
		print('Tweet posted!')


if __name__ == '__main__':
	main()
