##################################################################################
#                   Stock Gains and Losses email sender - EJI                    #
##################################################################################
# Version                                                                        #
# 1.0 - Primary Version, Stock Gain                                              #
# 1.1 - Created Loss Version, Generates 2 emails                                 #
# 1.2 - Included HTML generation to email function                               #
# 1.3 - Combined Loss and Gain into one DataFrame for simplicity                 #
##################################################################################

# Import Packages
# import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email_creds_url import *


# get the URL using pesobility site now to scrape the data
print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Getting URL for Stocks')

# Will be used as timestamp
today = datetime.now().strftime("[%b/%d/%Y] %I:%M%p")

# Define function to Create DataFrame for the data currently in the stock market
# Combine Gain and Losses in a Single DataFrame (Ver1.3)


# function to scrape the Stock Update table in PESOBILITY
def scrape_web(url, type_):
	page = requests.get(url)
	html = page.text
	soup = BeautifulSoup(html, "html.parser")
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Scraping {type_} data from Pesobility')
	return soup.table


# function to turn scraped table to DataFrame, works only on Pesobility
def create_df(table_bs):
	s = [x.findAll('td')[1].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
	p = [x.findAll('td')[2].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
	m = [x.findAll('td')[3].find(text=True) for x in table_bs.findAll("tr") if len(x.findAll('td')) == 4]
	df = pd.DataFrame({'Stock': s, 'Current Price': p, '% Movement': m})
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Creating dataFrame')
	return df


# Combine 2 dataframe to create a single one.
def stock_df(url_gain, url_loss):
	table1 = scrape_web(url_gain, "Gain")
	table2 = scrape_web(url_loss, "Loss")
	data1 = create_df(table1)
	data2 = create_df(table2)
	return data1, data2


# Send email function
def send_mail():
	# Login user and recipients
	gmail_user = email_user
	gmail_password = email_pw
	recipient = email_r
	msg = MIMEMultipart()
	msg['From'] = gmail_user
	msg['To'] = recipient
	msg['Subject'] = "PSE Stock Update as of " + today
	# Create gain and loss data frames (Ver1.2)
	df_gain, df_loss = stock_df(gain_url, loss_url)
	# Assemble email content (Header, Body and Footer)
	head = '''
	<html>
		<head>
		</head>
		<body>
		<h2>TOP 15 PSE Gainers as of ''' + today
	loss = '''
	<h2>TOP 15 PSE Losers as of ''' + today
	footer = '''	
	"The only thing that we need to count in life are our blessings."
	</body>
	</html>
	'''
	er = '''</h1>

	'''
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Assembling email content')
	with open('update.html', 'w') as f:
		f.write(head + er)
		f.write(df_gain[0:15].to_html(classes='df'))
		f.write(loss + er)
		f.write(df_loss[0:15].to_html(classes='df'))
		f.write(er + footer)

	with open('update.html', 'r') as f:
		attachment = MIMEText(f.read(), 'html')

	msg.attach(attachment)

	"""
		with smtplib.SMTP('smtp.gmail.com', 587) as mail_server:
		mail_server.ehlo()
		mail_server.starttls()
		mail_server.ehlo()
		mail_server.login(gmail_user, gmail_password)
		mail_server.sendmail(gmail_user, recipient, msg.as_string())
		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -  Sending Email')
	"""
# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(gmail_user, gmail_password)
		server.sendmail(
			gmail_user, recipient, msg.as_string()
		)
		print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Sending Email, SSL')


# if __name__ == '__main__':
# 	send_mail()


page = requests.get(gain_url)
html = page.text
soup = BeautifulSoup(html, "html.parser")

print(soup.table.find_all('td')[1].find(text=True))
