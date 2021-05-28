# YA FATEMEH
from csv import reader
from model.Candle import Candle
from model.Moment import Moment
import model.strategy as strategies
from controller.view_controller import control_views, check_view_essentials
from scenario import fee, start_of_work_dollar_balance, start_of_work_crypto_balance, \
                     number_of_moments_in_a_candle


dollar_balance = start_of_work_dollar_balance
bitcoin_balance = start_of_work_crypto_balance
this_moment = Moment(0, 0, '', 0, 0, {})
strategy_results = []
working_strategies = []


def data_converter(csv_file_name: str, extra_files: dict) -> list:
    extra_data = {}     # dictionary of lists.
    for file in extra_files:
        file_data = []
        with open(extra_files[file]) as csvfile:
            csv_reader = reader(csvfile, delimiter=',')
            next(csv_reader)        # skip field names
            for row in csv_reader:
                fields = [f for f in row]
                file_data.append(fields)        # list of fields(lists)
        extra_data[file] = file_data

    candles = []
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)        # skip field names
        line_count = 1
        for row in csv_reader:
            fields = [f for f in row]
            extra_fields = {}
            for data in extra_data:
                extra_fields[data] = float(extra_data[data][line_count - 1])
            c = Candle(line_count, int(fields[0]) // 1000, float(fields[1]),
                       float(fields[2]), float(fields[3]), float(fields[4]),
                       float(fields[5]), extra_fields)
            candles.append(c)
            line_count += 1
    return candles


def analyze_data(candles: list, csv_file_name: str):
    global this_moment, bitcoin_balance, dollar_balance
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)        # skip field names
        for c in candles:
            for i in range(number_of_moments_in_a_candle):     # the i th moment of candle
                price, volume = next(csv_reader)        # volume MAY be used!
                price = float(price)
                this_moment.update_moment(
                    i, c.hour, c.date, price, c.identifier, c.extra_fields)

                try_strategies(this_moment, candles)
                check_view_essentials(
                    this_moment, bitcoin_balance, dollar_balance)
            print('Analyzing :', round(100 * c.identifier/len(candles), 1), '%')
        control_views(strategy_results)


def try_strategies(moment: Moment, candles: list):
    global working_strategies,  bitcoin_balance, dollar_balance
    for ws in working_strategies:
        ws.continue_strategy()
    working_strategies = [ws for ws in working_strategies if ws.working]
    for s in strategies.strategies:
        if not s in strategies.lock_strategies:
            strtg = strategies.strategies[s](
                moment, bitcoin_balance, dollar_balance, candles)
            if strtg.working:
                working_strategies.append(strtg)


def buy(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin_balance += bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    dollar_balance -= (bitcoin * price * (1 + fee))
    dollar_balance = round(dollar_balance, 4)
    if dollar_balance < 0:
        raise RuntimeError('dollar balance is negative')


def sell(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin_balance -= bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    if bitcoin_balance < 0:
        raise RuntimeError('bitcoin balance is negative')
    dollar_balance += (bitcoin * price * (1 - fee))
    dollar_balance = round(dollar_balance, 4)


def get_this_moment() -> Moment:
    return this_moment


def set_report(r: str):
    strategy_results.append(r)
