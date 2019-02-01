import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime, timedelta
import logbook
import sys


# Will be used as timestamp
today = datetime.now().strftime("[%b/%d/%Y] %I:%M%p")
app_log = logbook.Logger('Stock')
# Define function to Create DataFrame for the data currently in the stock market
# Combine Gain and Losses in a Single DataFrame (Ver1.3)


def main():
    option = input('Run default(Y/N)? (Will get Oct25 to Jan 28 data for JFC): ')
    num = 0
    df_tot = []
    app_log.trace('Starting Stock Data Acquisition.')

    if option == 'Y':
        user_choice = 'JFC'
        from_date = '10/25/18'
        to_date = (datetime.today()-timedelta(days=1)).strftime('%m/%d/%y')
        app_log.trace('Choosing to have preset data.')

    elif option != 'N':
        raise ValueError

    else:
        app_log.trace('Choosing manual entry for data options.')
        user_choice = 'JFC'  # input('Enter PSE Stock Code you want to create data of: ')
        from_date = '01/02/14'  # input('Enter Start Date (MM/DD/YY): ')
        to_date = '01/29/19'  # input('Enter End Date (MM/DD/YY) :')

    if os.path.isfile(f'data/{user_choice}.csv'):
        os.remove(f'data/{user_choice}.csv')
        app_log.trace('Removing file, as it will be created once again!')

    stock_url = f'https://www.advfn.com/stock-market/PSE/{user_choice}/historical' \
        f'/more-historical-data?current={num}&Date1={from_date}&Date2={to_date}'
    head_, i, opening, closing, change_per = get_stock_details(stock_url)
    df = create_df(head_, i, opening, closing, change_per)
    app_log.trace(f'Creating Data Frames to be saved as CSV, page {num+1}')
    df_tot.append(df)
    num += 1

    while True:
        if len(i) == 1:
            break
        stock_url = f'https://www.advfn.com/stock-market/PSE/{user_choice}/historical' \
            f'/more-historical-data?current={num}&Date1={from_date}&Date2={to_date}'
        head_, i, opening, closing, change_per = get_stock_details(stock_url)
        app_log.trace(f'Creating Data Frames to be saved as CSV, page {num + 1}')
        df = create_df(head_, i, opening, closing, change_per)
        df_tot.append(df)
        num += 1

    app_log.trace(f'Done with looping')

    df_all = pd.concat(df_tot, ignore_index=True)

    app_log.trace(f'Data copied to file')

    df_all[:-1].to_csv(f'data/{user_choice}.csv', mode='w')


# function to scrape the Stock Update table in PESOBILITY
def get_stock_details(url):
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all('tr', class_='result')

    header = [[y.find(text=True) for y in x.findAll('th')] for x in soup.find_all('table', class_="histo-results")]

    ind = [datetime.strptime(x.findAll('td')[0].find(text=True), '%b %d %Y').strftime('%Y-%m-%d') for x in data]

    open_ = [round(float(x.findAll('td')[1].find(text=True)), 2) for x in data]

    close_ = [round(float(x.findAll('td')[2].find(text=True)), 2) for x in data]

    change_pc = [x.findAll('td')[4].find(text=True) for x in data]

    return header[0][0:5], ind, open_, close_, change_pc


def create_df(h, i, o, c, chp):
    return pd.DataFrame({h[0]: i, h[1]: o, h[2]: c, h[4]: chp})


def init_logging(filename: str = None):
    level = logbook.TRACE # trace, error, notices and warnings

    if filename:
        logbook.TimedRotatingFileHandler(filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    msg = 'Logging is initialized, level {}, mode {}'.format(
        level,
        "stdout mode" if not filename else 'file mode: ' + filename)

    logger = logbook.Logger('Startup')
    logger.notice(msg)


if __name__ == '__main__':
    init_logging()
    main()



