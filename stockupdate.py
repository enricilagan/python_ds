##################################################################################
##########          Stock Gains and Losses email sender - EJI           ##########
##################################################################################
## Version                                                                      ##
## 1.0 - Primary Version, Stock Gain                                            ##
## 1.1 - Created Loss Version, Generates 2 emails                               ##
## 1.2 - Included HTML generation to email function                             ##
## 1.3 - Combined Loss and Gain into one DataFrame for simplicity               ##
##################################################################################

## import packages
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime

## get the URL using pesobility site now to scrape the data
gain_url = "http://www.pesobility.com/reports/top-gainers"
loss_url = "http://www.pesobility.com/reports/worst-losers"

#Set whose email address will send the update and to whom.
emailUser = 'email@gmail.com'
emailPW = 'password'
emailRecipients = 'others@outlook.com'

## Will be used as timestamp
today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

## Define function to Create DataFrame for the data currently in the stock market
## Combine Gain and Losses in a Single DataFrame (Ver1.3)

# function to scrape the Stock Update table in PESOBILITY
def scrapeWeb(url):
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html)
    return soup.table

# function to turn scraped table to DataFrame, works only on Pesobility
def createDF(tableBS):
    S = []
    P = []
    M = []
    tableHTML = tableBS
    for row in tableHTML.findAll("tr"):
        cells = row.findAll('td')
        if len(cells)==4: #Only extract table body not heading
            S.append(cells[1].find(text=True))
            P.append(cells[2].find(text=True))
            M.append(cells[3].find(text=True))
    df = pd.DataFrame(S, columns = ['Stock'])
    df['Current Price'] = P
    df['% Movement'] = M
    return df

# Combine 2 dataframe to create a single one.
def stockdf(urlGain, urlLoss):
    table1 = scrapeWeb(urlGain)
    table2 = scrapeWeb(urlLoss)
    df1 = createDF(table1)
    df2 = createDF(table2)
    df = pd.concat([df1,df2], axis=1)
    df.columns = ['Gainers','Price','% Up','Losers','Price','% Down']
    return df

# Send email function
def send_mail(A = 'Yes'):    
    # Import SMTP and email modules
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    # Login user and recipients
    gmailUser = emailUser
    gmailPassword = emailPW
    recipient = emailRecipients
    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = "PSE Stock Update as of " + today
    # Create gain and loss data frames (Ver1.2)
    stockDF = stockdf(gain_url, loss_url)
    # Assemble email content (Header, Body and Footer)	
    head = '''
    <html>
        <head>
        </head>
        <body>
        <h1>TOP 15 PSE Gainers and Losers Stocks as of ''' 
    er = '''</h1>

    '''
    HEADER = head + today + er
    FOOTER = '''
    Keep on dreaming!!
    </body>
    </html>
    '''
    with open('update.html', 'w') as f:
        f.write(HEADER)
        f.write(stockDF[0:15].to_html(classes='df'))
        f.write(FOOTER)
    filename = 'update.html'
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

send_mail()