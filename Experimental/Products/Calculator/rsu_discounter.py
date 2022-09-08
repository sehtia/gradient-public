from decimal import Decimal

import datetime
import yfinance as yf


'''
    Utility class to discount RSUs.
    TODO(): Add input validation (e.g. ticker, dollar amount set incorrectly)
'''

TICKER_TO_IV_MAP = {
 'FB' : .075, #.0753,
 'AMZN' : .17, #.40,
 'AAPL' : .21, #.0991,
 'NFLX' : .152, #.1242,
 'GOOG' : .255 #.1706
}

TICKER_TO_IV_STDEV_MAP = {
 'FB' : .03,
 'AMZN': .028,
 'AAPL': .19,
 'NFLX': .067,
 'GOOG': .056
}

# Discount rsu using csv file data
def computeRsuValueCsv(rsu_ticker, rsu_dollar_amount):
    return rsu_dollar_amount * (1 - ticker_info.loc[rsu_ticker,'implied_vol'])

# Discount rsu using hardcode above (copied from csv file)
# Update method name to say IV
# TODO(): check if key exsts in dict
def computeRsuValue(rsu_ticker, rsu_dollar_amount):
    implied_volatility = Decimal(TICKER_TO_IV_MAP[rsu_ticker])
    return rsu_dollar_amount * (1 - implied_volatility)

# An approach: Look at all the IV's across option chain and calc stdev
# Use max IV - (1,2,3)*stdev to get lower bound of band
# Max IV (current result) is upper bound of band
def computeRsuBand(rsu_ticker, rsu_dollar_amount, stdev=1):
    implied_volatility = Decimal(TICKER_TO_IV_MAP[rsu_ticker])
    implied_volatility_stdev = stdev*Decimal(TICKER_TO_IV_STDEV_MAP[rsu_ticker])
    lower_bound_iv = implied_volatility + implied_volatility_stdev

    lower_bound_rsu = rsu_dollar_amount * (1 - lower_bound_iv)
    upper_bound_rsu = computeRsuValue(rsu_ticker, rsu_dollar_amount)
    return {
        "LowerBoundRsuValue": lower_bound_rsu,
        "UpperBoundRsuValue": upper_bound_rsu
    }

# Discount rsu using 52-week average share price
def compute52WeekAvgRsuValue(rsu_ticker, rsu_dollar_amount):
    #today_close_share_price = yf.download(rsu_ticker, start=datetime.datetime.today()).Close.values[0]
    all_closing_prices = get52WeekClosePrices(rsu_ticker)
    today_close_share_price = all_closing_prices.values[-1]
    num_shares = rsu_dollar_amount / today_close_share_price
    fifty_two_week_avg_price = all_closing_prices.mean()
    return num_shares * fifty_two_week_avg_price

# Get 52 week average stock price for the given ticker
def get52WeekClosePrices(rsu_ticker):
    today_datetime = datetime.datetime.today()
    fifty_two_weeks_ago_datetime = today_datetime - datetime.timedelta(weeks=52)
    return yf.download(rsu_ticker, start=fifty_two_weeks_ago_datetime, end=today_datetime).Close

def getAllDiscounts(rsu_ticker, rsu_dollar_amount):
    return {
        "ImpliedVolatility": computeRsuValue(rsu_ticker, rsu_dollar_amount),
        "52WeekAverage": compute52WeekAvgRsuValue(rsu_ticker, rsu_dollar_amount)
    }

# Main method for running
def main():
    # print(f"RSU Discounts for $200K in assets for da habibis: \n{getAllDiscounts('GOOG', 144555)}")
    print(f"RSU discount band: {computeRsuBand('GOOG', 144555)}")

# Using the special variable
if __name__=="__main__":
    main()
