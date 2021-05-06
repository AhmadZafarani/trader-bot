# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path


data_folder = Path("data")
one_hour = data_folder / 'onehour.csv'
candles = data_converter(one_hour)
one_minute = data_folder / 'oneminute.csv'
analyze_data(candles, one_minute)
