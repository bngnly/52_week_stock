import yfinance as yf
import json
import sys
import pandas as pd

if len(sys.argv) - 1 == 2:
    market_cap_threshold = sys.argv[1]
    percentage_threshold = sys.argv[2]
else:
    market_cap_threshold = 2000000000
    percentage_threshold = 0.8

tickers_json =[]

f = open('../input_data/preprocessed/tickers.json',)
tickers = json.load(f)
f.close()

for ticker in tickers:
    print(ticker)
    if ticker['market_cap'] is not None and ticker['market_cap'] >= market_cap_threshold:
        try:
            df = yf.download(ticker['ticker'], period='1y')
            year_high = df['Close'].max()
            previous_close = df.iloc[1]['Close']

            if previous_close <= year_high * percentage_threshold:
                stock = {
                    "ticker" : ticker['ticker'],
                    "market_cap" : ticker['market_cap'],
                    "52_week_high" : year_high,
                    "previous_close" : previous_close
                    }
                tickers_json.append(stock)
                print('Qualified: ' + ticker['ticker'])
            else:
                print('Did not qualify: ' + ticker['ticker'])
            print(ticker['ticker'] + ': was attempted')
        except:
            print('Unable to execute call for yfinance data for: ' + ticker['ticker'])

#for ticker in tickers:
#    try:
#        stock = yf.Ticker(ticker)
#        print(ticker)
#        year_high = stock.info['fiftyTwoWeekHigh']
#        print(year_high)
#        current_price = stock.info['previousClose']
#        print(current_price)
#        mrkt_cp = stock.info['marketCap']
#        print(mrkt_cp)
#
#        wstock = {
#            "ticker" : ticker,
#            "fiftyTwoWeekHigh" : year_high,
#            "current_price" : current_price,
#            "market_cap" : mrkt_cp
#        }
#
#        tickers_json.append(wstock)
#
#    except:
#        print('unable to process: ' + ticker)

with open("../input_data/preprocessed/" + "tickers_finished.json", "w") as outfile:
    json.dump(tickers_json, outfile)