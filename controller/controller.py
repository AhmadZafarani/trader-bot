# YA FATEMEH
from csv import reader
from model.Candle import Candle
from model.Moment import Moment
import model.strategy as strategies
from controller.view_controller import control_views, check_view_essentials
from scenario import fee, start_of_work_dollar_balance, start_of_work_crypto_balance, \
    number_of_moments_in_a_candle, lock_hour, lock_method, profit_loss_period_step


dollar_balance = start_of_work_dollar_balance
bitcoin_balance = start_of_work_crypto_balance
start_of_profit_loss_period_balance = 0
this_moment = Moment(0, 0, 0, {}, {})
strategy_results = []
working_strategies = []


def extra_data_converter(extra_files: dict) -> dict:
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
    return extra_data


def data_converter(candles_file: str, extra_candle_files: dict, extra_moment_files: dict) -> tuple:
    extra_data = extra_data_converter(extra_candle_files)

    candles = []
    with open(candles_file) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)        # skip field names

        line_count = 1
        for row in csv_reader:
            fields = [f for f in row]
            extra_fields = {}
            for data in extra_data:
                extra_fields[data] = extra_data[data][line_count - 1]

            c = Candle(line_count, float(fields[1]), float(fields[2]),
                       float(fields[3]), float(fields[4]), float(fields[5]), extra_fields)
            candles.append(c)
            line_count += 1

    extra_data = extra_data_converter(extra_moment_files)
    return candles, extra_data


def analyze_each_moment(csv_reader, moment_index: int, moments_extra_data: list, minute: int, candle: Candle,
                        candles: list):
    time, price, volume = next(csv_reader)        # volume MAY be used!
    price = float(price)
    time = int(time) // 1000

    profit_loss_percentage = profit_loss_calculator(moment_index, price)

    extra_fields = {}       # moments extra fields
    for data in moments_extra_data:
        extra_fields[data] = moments_extra_data[data][moment_index]

    this_moment.update_moment(minute, time, price, candle.identifier,
                              profit_loss_percentage, candle.extra_fields, extra_fields)

    try_strategies(this_moment, candles)
    check_view_essentials(this_moment, bitcoin_balance, dollar_balance)


def analyze_data(candles: list, csv_file_name: str, moments_extra_data: dict):
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)        # skip field names

        moment_index = 0     # zero based
        for c in candles:
            for i in range(number_of_moments_in_a_candle):     # the i th moment of candle
                analyze_each_moment(csv_reader, moment_index,
                                    moments_extra_data, i, c, candles)
                moment_index += 1

            print('Analyzing :', round(100 * c.identifier / len(candles), 2), '%')
        control_views(strategy_results)


def profit_loss_calculator(moment_index: int, this_moment_price: float) -> float:
    global start_of_profit_loss_period_balance
    x = dollar_balance + bitcoin_balance * this_moment_price
    if moment_index % profit_loss_period_step == 0:
        start_of_profit_loss_period_balance = x
        return 0
    else:
        return round((x - start_of_profit_loss_period_balance) * 100 / start_of_profit_loss_period_balance, 4)


def try_strategies(moment: Moment, candles: list):
    global working_strategies, bitcoin_balance, dollar_balance, lock_method, lock_hour
    if lock_method == 'lock_to_hour':
        for locked in strategies.lock_strategies:       # unlock strategies
            if strategies.lock_strategies[locked][1] == moment.candle_id:
                strategies.lock_strategies.pop(locked)

    for ws in working_strategies:
        ws.continue_strategy()
    # remove finished strategies from working_strategies
    working_strategies = [ws for ws in working_strategies if ws.working]

    for s in strategies.strategies:     # trying to start not locked strategies
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
