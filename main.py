# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path
import time

time0 = time.time()
data_folder = Path("data")
one_hour = data_folder / 'onehour.csv'
print('loading data')
time1 = time.time()
candles = data_converter(one_hour)
one_minute = data_folder / 'oneminute.csv'
time2 = time.time()
print('data loaded in ' , time2-time1)
time.sleep(1)
analyze_data(candles, one_minute)
time3 = time.time()

print('runtime : ' , time3 - time0)  