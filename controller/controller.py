# YA FATEMEH
from csv import reader
from model.Candle import Candle
from model.strategy import trade, decisions
from model.Position import Position


def data_converter(csv_file_name: str) -> list:
    candles = []
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)    # skip field names
        line_count = 0
        for row in csv_reader:
            fields = [f for f in row]
            candles.append(
                Candle(line_count, fields[0], fields[1], fields[2], fields[3], fields[4]))
            line_count += 1
    return candles


def analyze_data(candles: list) -> list:
    results = []
    for c in candles:
        decision = trade(c)
        # last element of decisios always is 'do_nothing'
        if decision != decisions[-1]:
            result = Position(decision, c)
            results.append(result)
    return _wrap_data_for_view(results)


def _wrap_data_for_view(results: list) -> list:
    return results
