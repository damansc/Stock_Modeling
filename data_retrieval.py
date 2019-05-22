# -*- coding: utf-8 -*-
"""
Spyder Editor

This module provides functions for pulling the stock tickers for the most 
recent list of S&P 500 companies and downloads their stock data saving each 
to it's own individual CSV.

The starting date for the data is manually hardcoded. The end date is set to 
the current day if it is after market close at 4:00pm est or the previous day
if the markets have not closed for the day.
"""

import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas_datareader as pdr


def retrieve_sp500():
    source = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    resp = requests.get(source)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.replace('.','-')
        tickers.append(ticker.rstrip())
    with open('sp500_tickers.pickle', 'wb') as file:
        pickle.dump(tickers, file)
        
    return tickers


def get_data(retrieve = False):
    if retrieve == True:
        tickers = retrieve_sp500()
    else:
        with open('sp500_tickers.pickle', 'rb') as file:
            tickers = pickle.load(file)
            
    if not os.path.exists('sp500_data'):
        os.mkdir('sp500_data')
    
    # start is manually set, end is     
    start = '2018-01-01'
    exchg_close = dt.time(16,0,0,0)
    # use todays date if markets have closed.
    if dt.datetime.today().time() > exchg_close:
        end = dt.datetime.now()
    # use yesterdays dates if markets have not yet closed.
    else:   
        end = dt.datetime.now() - dt.timedelta(1)
       
    for ticker in tickers:
        # updates data for tickers not currently stored.
        if not os.path.exists('sp500_data/{}.csv'.format(ticker)):
            df = pdr.get_data_yahoo(ticker, start, end)
            df.to_csv('sp500_data/{}.csv'.format(ticker))
        # updates data for tickers that have not been updated today.
        elif dt.datetime.fromtimestamp(os.path.getmtime('sp500_data/{}.csv'.format(ticker))).day != dt.datetime.today().day:
            df = pdr.get_data_yahoo(ticker, start, end)
            df.to_csv('sp500_data/{}.csv'.format(ticker))
        # prints out data that was not and does not need udpating.
        else:
            print('{} is already saved'.format(ticker))