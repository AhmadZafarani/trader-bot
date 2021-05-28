# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path
from time import time

start_time = time()
data_folder = Path("data")
one_hour = data_folder / 'onehour.csv'
print('loading data...')

data_loading_start_time = time()
candles = data_converter(one_hour)
print('data loaded in : ', time() - data_loading_start_time)

one_minute = data_folder / 'oneminute.csv'
analyze_data(candles, one_minute)

print('total runtime : ', time() - start_time)
