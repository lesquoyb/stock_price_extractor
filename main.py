import datetime
import math

import pandas as pd
import yfinance as yf
import os, contextlib


if __name__ == '__main__':

    # read all tickers symbols from the file and create an array out of it
    tickers = open("tickers.txt").read().split("\n")

    print("Tickers to be tested:", tickers)

    start_date = datetime.date(2007, 1, 1)
    end_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    print("researching from", start_date, "to", end_date)
    data = yf.download(tickers, start=start_date, end=end_date, interval='1mo', group_by="ticker")

    # we check the list to filter out all the empty data
    filtered_array = []  # each line in the array is the name of the ticker, a date and an adjusted closing price
    tickers_not_found = tickers.copy()  # we'll also check out which ticker has no data at all
    for ticker in tickers:
        if ticker in data:
            df = data[ticker]
            for date, value in df['Adj Close'].items():
                if value and not math.isnan(value):
                    filtered_array += [[ticker, date, value]]
                    if ticker in tickers_not_found:
                        tickers_not_found.remove(ticker)

    print("Those tickers couldn't be found:", tickers_not_found)

    print("Here is the final data:", filtered_array)
    print("Saving it into a csv")
    file = open("data.csv", "w")
    file.writelines("ticker,date,value\n")
    file.writelines(f"{line[0]},{line[1]:%Y-%m-%d},{line[2]}\n" for line in filtered_array)

