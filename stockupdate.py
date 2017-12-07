## import packages
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime

## get the URL using pesobility site now to scrape the data
gain_url = "http://www.pesobility.com/reports/top-gainers"
loss_url = "http://www.pesobility.com/reports/worst-losers"

## will be used as timestamp
today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

## Define function to Create DataFrame for the data currently in the stock market
def create_stock(url):
    page = requests.get(url)
    html_doc = page.text
    soup = BeautifulSoup(html_doc)
    pretty_soup = soup.prettify()
    chart = soup.table
    stock = []
    price = []
    move = []
    for row in chart.findAll("tr"):
        cells = row.findAll('td')
        if len(cells)==4: #Only extract table body not heading
            stock.append(cells[1].find(text=True))
            price.append(cells[2].find(text=True))
            move.append(cells[3].find(text=True))
    df = pd.DataFrame(stock, columns = ['Symbol'])
    df['Current Price'] = price
    df['% Movement'] = move
    return df

# Create gain and loss data frames
stock_gain = create_stock(gain_url)
stock_loss = create_stock(loss_url)

# Assemble email content (Header, Body and Footer)	
head = '''
<html>
    <head>
    </head>
    <body>
    <h1>TOP 15 PSE Stocks''' 

loss = ''' Loss as of '''
gain = ''' Gainers as of '''
er = '''</h1>

'''
HEADER_LOSS = head + loss + today + er
HEADER_GAIN = head + gain + today + er

FOOTER = '''
Keep on dreaming!!
</body>
</html>
'''

with open('loss.html', 'w') as f:
    f.write(HEADER_LOSS)
    f.write(stock_loss[0:15].to_html(classes='df'))
    f.write(FOOTER)

with open('gains.html', 'w') as f:
    f.write(HEADER_GAIN)
    f.write(stock_gain[0:15].to_html(classes='df'))
    f.write(FOOTER)
    
loss_file = 'loss.html'
gain_file = 'gains.html'

# Send email function
def send_mail(files, type):    
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    gmailUser = 'email@gmail.com'
    gmailPassword = 'password'
    recipient = 'email@outlook.com'
    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = "PSE Stock " + type
    filename = files
    f = file(filename)
    attachment = MIMEText(f.read(),'html')
    msg.attach(attachment)
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()
	
send_mail(gain_file, 'Gain')
send_mail(loss_file, 'Loss')