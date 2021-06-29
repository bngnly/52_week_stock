import multiprocessing
import yfinance as yf
import datetime
from contextlib import contextmanager
import sys
import os
import csv

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
        stock = yf.Ticker(ticker)
        year_high = stock.info['fiftyTwoWeekHigh']
        current_price = stock.info['previousClose']
        mrkt_cp = stock.info['marketCap']
        if marketCap <= mrkt_cp and current_price <= year_high * threshold:
            return True
        else:
            return False
    except:
        return False

# Create an array of Stock Tickers that are below a threshold
def generate_stocks(tickers, threshold, marketCap, final_tickers):
    for ticker in tickers:
        print(ticker+' worked on process id: ', os.getpid())
        if meets_threshold(ticker, threshold, marketCap):
            final_tickers.append(ticker)

# Conduct analysis on Stock Tickers (main)
def conduct_analysis(datafile, filename, threshold, marketCap, n_procs):
    tickers = get_tickers_into_array('../input_data/' + datafile)
    manager = multiprocessing.Manager()
    tickers_wanted = manager.list()
    processes = []
    for i in range(0, n_procs):
        if i < n_procs - 1:
            process = multiprocessing.Process(target=generate_stocks,
                                              args=(tickers[i*round(len(tickers)/n_procs):(i+1)*round(len(tickers)/n_procs)],
                                                    threshold, marketCap, tickers_wanted))
            process.start()
            processes.append(process)
        else:
            process = multiprocessing.Process(target=generate_stocks,
                                              args=(tickers[i*round(len(tickers)/n_procs): ],
                                                    threshold, marketCap, tickers_wanted))
            process.start()
            processes.append(process)
    for proc in processes:
        proc.join()
    #f = open('../output_data/' + filename, 'w+')
    #for ticker in tickers_wanted:
    #    f.write(ticker + '\n')
    #f.close('../output_data/' + filename, 'w+')
    generate_csv(tickers, filename)

def generate_csv(tickers, filename):
    with open('../output_data/' + filename, 'w+') as csv_file:
        #fieldnames = ['name', 'symbol', 'market_cap', 'industry', 'current % drop', '52_week_high', 'current_price']
        fieldnames = ['symbol', 'market_cap', 'current % drop', '52_week_high', 'current_price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            writer.writerow({#'name': stock.info['shortName'],
                             'symbol': stock.info['symbol'],
                             'market_cap': stock.info['marketCap'],
                             #'industry': stock.info['industry'],
                             'current % drop': 1 - stock.info['previousClose'] / stock.info['fiftyTwoWeekHigh'],
                             '52_week_high': stock.info['fiftyTwoWeekHigh'],
                             'current_price': stock.info['previousClose']})


if __name__ == '__main__':

    print('You have ' + str(os.cpu_count()) + ' processors available')
    my_procs = int(input('How many processors? '))

    my_threshold = float(input('What is the threshold? (percentage in decimal format) '))
    my_marketcap = int(input('What is the market cap? '))

    nasdaq_q = input('NASDAQ? (y = yes): ')
    if nasdaq_q == 'y':
        nasdaq_filename = input('enter new filename (add .csv at the end): ')
        print('start nasdaq @: ', datetime.datetime.now())
        conduct_analysis('testing.txt', nasdaq_filename, my_threshold, my_marketcap, my_procs)
        # conduct_analysis('nasdaqlisted.txt', nasdaq_filename, my_threshold, my_marketcap, my_procs)
        print('end nasdaq @: ', datetime.datetime.now())

    others_q = input('Other Tickers? (y = yes): ')
    if others_q == 'y':
        others_filename = input('enter new filename (add .txt at the end): ')
        print('start others @: ', datetime.datetime.now())
        conduct_analysis('otherlisted.txt', others_filename, my_threshold, my_marketcap, my_procs)
        print('end others @: ', datetime.datetime.now())

