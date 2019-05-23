# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:15:13 2019

@author: daman

This module provides methods for pulling the stock tickers for the most 
recent list of the S&P 500 companies and downloads their stock data saving each 
to it's own individual CSV, and then cleaning and aggregating each into
an aggregate dataframe that is stored as its own csv file.
"""

import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader as pdr


def retrieve_sp500():
    """
    Retrieves an updated list of tickers for companies included in the 
    S&P 500. Saves to a pickle file.
    """
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


def get_data(retrieve = False, start='2019-01-01', comp = False):
    """
    Uses the most recent pickle file of stock tickers and retrieves the stock
    data for each ticker via the pandas-datreader get_yahoo_data() method.
    It saves each stock ticker as it's own csv file. The default time period
    is 2018-01-01 to either the current day if after 4:00pm market close or 
    the previous day if the markets are open.
    """
    if retrieve == True:
        tickers = retrieve_sp500()
    else:
        with open('sp500_tickers.pickle', 'rb') as file:
            tickers = pickle.load(file)
    if not os.path.exists('sp500_data'):
        os.mkdir('sp500_data')
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
        if comp == True:
            compile_data()
            
            
def compile_data():
    """
    Formats and joins each individual stock's csv file into one large 
    dataframe and writes it to a csv file. This can be automatically 
    done during the initial data downloaded of the stock data within the 
    get_data() method by setting the argument: comp=True.
    """
    with open('sp500_tickers.pickle', 'rb') as file:
         tickers = pickle.load(file)
    metasp = pd.DataFrame()
    for count, ticker in enumerate(tickers):
       df = pd.read_csv('sp500_data\{}.csv'.format(ticker))
       df.set_index('Date', inplace=True)
       df.rename(columns={'Adj Close': ticker}, inplace=True)
       df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
       if metasp.empty:
           metasp = df
       else:
           metasp = metasp.join(df, how = 'outer')
    if count % 10 == 0:
            print(count)
    metasp.to_csv('sp500_meta.csv')
    
    


