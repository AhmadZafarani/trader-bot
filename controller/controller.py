# YA FATEMEH
from csv import reader
from model.Candle import Candle
from model.Moment import Moment
from model.strategy import Dummy_Strategy


dollar_balance = 1000   # lock
bitcoin_balance = 0     # lock
this_moment = Moment(0, 0, '', 0)
strategy_results = []


def data_converter(csv_file_name: str) -> list:
    candles = []
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)    # skip field names
        line_count = 1
        for row in csv_reader:
            fields = [f for f in row]
            candles.append(
                Candle(line_count, fields[0], fields[1], fields[2], fields[3], fields[4]))
            line_count += 1
    return candles


def analyze_data(candles: list) -> tuple:
    global this_moment
    balance = []
    for c in candles:
        for i in range(59):
            price = c.minute_price(i)
            this_moment.update_moment(i, c.hour, c.date, price)
            try_strategies(this_moment)
            balance.append((dollar_balance, bitcoin_balance))
    return balance, strategy_results


def try_strategies(moment: Moment):
    # notify all
    Dummy_Strategy(moment)


def buy(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin_balance += bitcoin
    dollar_balance -= (bitcoin * price)


def sell(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin_balance -= bitcoin
    dollar_balance += (bitcoin * price)


def get_this_moment() -> Moment:
    return this_moment


def set_report(r: str):
    strategy_results.append(r)
