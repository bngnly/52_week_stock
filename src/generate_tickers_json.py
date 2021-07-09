import json
import yfinance as yf

tickers = []

f = open("../input_data/raw/testing.txt", "r")
lines = f.readlines()
for line in lines:
    ticker = line[:line.index('|')]
    try:
        stock_ticker = {"ticker" : ticker,
                        "market_cap" : yf.Ticker(ticker).info["marketCap"]}
        tickers.append(stock_ticker)
        print("Evaluated properly: " + ticker)
    except:
        print("Could not evaluate: " + ticker)
f.close()

with open("../input_data/preprocessed/" + "tickers.json", "w") as outfile:
    json.dump(tickers, outfile)