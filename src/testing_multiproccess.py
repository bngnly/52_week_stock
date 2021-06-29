import multiprocessing
import datetime

def is_y(old_list, new_list):
    for i in range(0, len(old_list)):
        if old_list[i] == 'x':
            #print(str(i) + ' is odd')
            new_list[i] = old_list[i]
        else:
            new_list[i] = 'y'

def is_ok(old_list, new_list):
    for i in old_list:
        if i == 'ok':
            new_list.append('yerr')

def get_tickers_into_array(filename):
    tickers = []
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        tickers.append(line[:line.index('|')])
        # print(line)
    f.close()
    return tickers

def contains_a(old_list, new_list):
    for i in old_list:
        if 'a' in i:
            new_list.append(i)

start_time = datetime.datetime.now()
#list = multiprocessing.Array('c', ['y', 'y', 'n', 'y', 'n', 'n', 'y', 'n', 'y', 'y'])
#odds = multiprocessing.Array('c', ['z','z','z','z','z','z','z','z','z','z'])

#start = ['ok','not','ok','ok','not','ok','not','not','ok','not']

tickers = get_tickers_into_array('../input_data/nasdaqlisted.txt')

manager = multiprocessing.Manager()
end = manager.list()

process = multiprocessing.Process(target=contains_a, args=(tickers, end))
process.start()
process.join()

print('done multi', datetime.datetime.now() - start_time)
print(end[:])
