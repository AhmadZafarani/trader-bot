# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path
from time import time
from scenario import candles_data_csv_file_name, moment_data_csv_file_name, extra_candles_data_files, \
    extra_moments_data_files


start_time = time()
print('loading data...')

data_folder = Path("data")
candles_file = data_folder / candles_data_csv_file_name
moments_file = data_folder / moment_data_csv_file_name

extra_candle_files = {}
for ecdf in extra_candles_data_files:
    extra_candle_files[ecdf] = data_folder / extra_candles_data_files[ecdf]

extra_moment_files = {}
for emdf in extra_moments_data_files:
    extra_moment_files[emdf] = data_folder / extra_moments_data_files[emdf]

candles = data_converter(candles_file, extra_candle_files)
print('data loaded in : ', time() - start_time)

analyze_data(candles, moments_file, extra_moment_files)

print('total runtime : ', time() - start_time)
