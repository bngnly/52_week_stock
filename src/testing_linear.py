import yfinance as yf
import datetime
from contextlib import contextmanager
import sys, os

# Suppressing Output to make it appear faster
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# Get Stock Tickers into Array form
def get_tickers_into_array(filename):
    tickers = []
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        tickers.append(line[:line.index('|')])
        # print(line)
    f.close()
    return tickers

# Determine if a Stock Ticker is below the threshold
def meets_threshold(ticker, threshold, marketCap):
    try:
        #print(yf.Ticker(ticker).info)
        #if yf.Ticker(ticker).info['marketCap'] < marketCap:
        #    return False
        #df = yf.download(ticker, period='1y')
        #year_high = df['Close'].max()
        #current_price = df.iloc[1]['Close']
        stock = yf.Ticker(ticker)
        #print(stock.info['zip'])
        year_high = stock.info['fiftyTwoWeekHigh']
        current_price = stock.info['previousClose']
        mrkt_cp = stock.info['marketCap']
        if marketCap <= mrkt_cp and current_price <= year_high * threshold:
            print(ticker, ' is selected')
            return True
        else:
            return False
    except:
        return False

# Create an array of Stock Tickers that are below a threshold
def generate_stocks(tickers, threshold, marketCap):
    want = []
    for ticker in tickers:
        # print(ticker)
        if meets_threshold(ticker, threshold, marketCap):
            want.append(ticker)
    return want

# Conduct analysis on Stock Tickers (main)
def conduct_analysis(datafile, filename, threshold, marketCap):
    tickers = get_tickers_into_array('../input_data/' + datafile)
    tickers_wanted = generate_stocks(tickers, threshold, marketCap)
    f = open('../output_data/' + filename, 'w+')
    for ticker in tickers_wanted:
        f.write(ticker + '\n')
    f.close()

start_time = datetime.datetime.now()
print('starting @ ', start_time)

my_threshold = 0.8
my_marketcap = 2000000000


nasdaq_q = input('NASDAQ? (y = yes): ')
if nasdaq_q == 'y':
    nasdaq_filename = input('enter new filename (add .txt at the end): ')
    #with suppress_stdout():
    conduct_analysis('nasdaqlisted.txt', nasdaq_filename, my_threshold, my_marketcap)
nasdaq_time = datetime.datetime.now()
print('finished NASDAQ @ ', start_time - nasdaq_time)

others_q = input('Other Tickers? (y = yes): ')
if others_q == 'y':
    others_filename = input('enter new filename (add .txt at the end): ')
    #with suppress_stdout():
    conduct_analysis('otherlisted.txt', others_filename, my_threshold, my_marketcap)

other_time = datetime.datetime.now()
print('finished all @ ', start_time - other_time)
