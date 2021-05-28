# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path
from time import time
from scenario import candles_data_csv_file_name, moment_data_csv_file_name, extra_data_files

start_time = time()
data_folder = Path("data")
one_hour = data_folder / candles_data_csv_file_name
extra_files = {}
for edf in extra_data_files:
    extra_files[edf] = data_folder / extra_data_files[edf]
print('loading data...')

data_loading_start_time = time()
candles = data_converter(one_hour, extra_files)
print('data loaded in : ', time() - data_loading_start_time)

one_minute = data_folder / moment_data_csv_file_name
analyze_data(candles, one_minute)

print('total runtime : ', time() - start_time)
