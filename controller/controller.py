# YA FATEMEH
from csv import reader
from model.Candle import Candle
from model.Moment import Moment
import model.strategy as strategies


dollar_balance = 1000
bitcoin_balance = 0
this_moment = Moment(0, 0, '', 0)
strategy_results = []
working_strategies = []


def data_converter(csv_file_name: str) -> list:
    candles = []
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)    # skip field names
        line_count = 1
        for row in csv_reader:
            fields = [f for f in row]
            candles.append(Candle(line_count, int(fields[0]), float(fields[1]),
                                  float(fields[2]), float(fields[3]), float(fields[4]), float(fields[5])))
            line_count += 1
    return candles


def analyze_data(candles: list) -> tuple:
    global this_moment, bitcoin_balance, dollar_balance
    balance = []
    for c in candles:
        for i in range(60):
            price = c.minute_price(i)
            this_moment.update_moment(i, c.hour, c.date, price)
            try_strategies(this_moment)
            balance.append((dollar_balance, bitcoin_balance))
    return balance, strategy_results


def try_strategies(moment: Moment):
    global working_strategies
    for ws in working_strategies:
        ws.continue_strategy()
    working_strategies = [ws for ws in working_strategies if ws.working]
    s1 = strategies.Dummy_Strategy(moment)
    if s1.working:
        working_strategies.append(s1)    


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
