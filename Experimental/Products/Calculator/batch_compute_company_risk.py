# -*- coding: utf-8 -*-
"""
Created on Thu May 19 07:30:58 2022

@author: Raghav Sehtia
"""

import requests
import pandas as pd
import numpy as np
import datetime as dt
from yahoo_fin import stock_info as si
import yfinance as yf

#link to FRED for fed funds rate
from fredapi import Fred
fred = Fred(api_key='dafd65e2d9cac6f03aeb39aedf45fe88 ')

#standards
#ff_rate = fred.get_series('FEDFUNDS')[-1] # note this is updated monthly you'll probably want something that's quicker but you might need to pay for it
#tbill_30 = fred.get_series('DGS30')[-1] # note this is updated monthly you'll probably want something that's quicker but you might need to pay for it

#pull IV as proxy for stock volatilty
def pull_option_chain(ticker):
    yf_ticker = yf.Ticker(ticker)
    exp_dates = yf_ticker.options
    options = pd.DataFrame()
    # Need to specify what expiry date to get options for
    for exp in exp_dates:
        opt = yf_ticker.option_chain(exp)
        # if it breaks change concat back to append
        opt = pd.DataFrame().append(opt.calls).append(opt.puts) #columns are contract size, currensy, and IV
        opt['expirationDate'] = exp

        # Next 3 lines are for data clarity
        # Expiration finance are written on saturday's, but market closed.
        opt['expirationDate'] = pd.to_datetime(opt['expirationDate']) + dt.timedelta(days = 1)
        opt.loc[:,'daysToExpiration'] = (opt['expirationDate'] - dt.datetime.today()).dt.days
        options = options.append(opt, ignore_index = True)

    # Creating new column
    options.loc[:,'optionType'] = np.where(options['contractSymbol'].apply(lambda a: 'C' in a[len(ticker):]), 'Call', 'Put')

    #options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])

    return options

#ticker_list = si.tickers_nasdaq() # to be expanded, just faang + top employers in the bay for now
ticker_list = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG','TSLA', 'WFC', 'V', 'CVX',
               'ADBE', 'WDC', 'EBAY', 'SNPS', 'WDAY','JNPR', 'CRM', 'VMW',
               'GILD', 'TWTR','NVDA', 'PANW']

#pull 5 year topline projection
#pull all imp_vol maxes to calc rsu applied values
if 'ticker_info' not in locals():
    ticker_info = pd.DataFrame()
    for t in ticker_list:
        print(f'Starting data collection for {t}')
        try:
            t_anal = si.get_analysts_info(t)['Growth Estimates']
        except Exception as e:
            print(f'{t} has no analyst projections\n{e}')
            break
        proj_5yr_gr = t_anal.loc[t_anal['Growth Estimates'] == 'Next 5 Years (per annum)', t].iloc[0]
        ticker_info.loc[t, 'projected_5yr_growth'] = proj_5yr_gr

        #pull IV
        ticker_imp_vol = pull_option_chain(t)['impliedVolatility']
        # print(f"type of ticker vol: {type(ticker_imp_vol)}")
        # print(f"ticker vol: {ticker_imp_vol}")
        quantiles = ticker_imp_vol.quantile([.25, .5, .75, .8, .9])
        stdev = ticker_imp_vol.std()
        # print(f" quantiles: {quantiles}")
        ticker_info.loc[t, 'implied_vol_quantile_25'] = quantiles[.25]
        ticker_info.loc[t, 'implied_vol_quantile_50'] = quantiles[.5]
        ticker_info.loc[t, 'implied_vol_quantile_75'] = quantiles[.75]
        ticker_info.loc[t, 'implied_vol_quantile_85'] = quantiles[.8]
        ticker_info.loc[t, 'implied_vol_quantile_90'] = quantiles[.9]
        ticker_info.loc[t, 'implied_vol_max'] = ticker_imp_vol.max()
        ticker_info.loc[t, "implied_vol_stdev"] = stdev


ticker_info.to_csv('implied_volatility_top20tech_20220605.csv')
