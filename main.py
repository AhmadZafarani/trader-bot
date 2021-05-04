# YA HOSSEIN
from controller.controller import data_converter, analyze_data


candles = data_converter('data/bnblastyear_hourlydata.csv')
analyze_data(candles)
