# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from view.views import view_results


candles = data_converter('data/oneHour.csv')
results = analyze_data(candles)
view_results(results)
