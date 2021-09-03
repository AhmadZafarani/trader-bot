# YA FATEMEH
from csv import reader
from time import time, sleep

from model.Candle import Candle
from model.Moment import Moment
import model.strategy as strategies
from controller.view_controller import *
from scenario import scenario
from controller.exchange_controller import get_last_candle, get_current_data_from_exchange, exchange_sell, exchange_buy, get_time_from_exchange


dollar_balance = scenario.start_of_work_dollar_balance
bitcoin_balance = scenario.start_of_work_crypto_balance
start_of_profit_loss_period_balance = 0
this_moment = Moment(0, 0, 0)
strategy_results = []
working_strategies = []


def open_extra_files(extra_files: dict) -> list:
    files = []
    for file in extra_files:
        csv_file = open(extra_files[file])
        files.append(list(reader(csv_file)))
    return files


def candle_maker(candles_data: list, i: int, files: list) -> Candle:
    fields = [f for f in candles_data[i]]
    c = Candle(i, float(fields[0]), float(fields[1]), float(
        fields[2]), float(fields[3]), float(fields[4]))

    for file in files:  # extract extra fields from extra files
        field_names = file[0]
        field_length = len(field_names)
        fields = [f for f in file[i]]

        for j in range(field_length):
            c.__setattr__(field_names[j], float(fields[j]))
    return c


# read data from candles csv file and make candles list
def data_converter(candles_file: str, extra_candle_files: dict) -> list:
    files = open_extra_files(extra_candle_files)

    candles = []
    with open(candles_file) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        candles_data = list(csv_reader)
        candles_number = len(candles_data)
        for i in range(1, candles_number):
            c = candle_maker(candles_data, i, files)
            candles.append(c)
    return candles


def analyze_each_moment(csv_reader: list, moment_index: int, moments_extra_files: list, candle: Candle, candles: list):
    time, price, volume = csv_reader[moment_index]        # volume MAY be used!
    price = float(price)
    time = int(time) // 1000

    profit_loss_percentage = profit_loss_calculator(moment_index, price)
    this_moment.update_moment(
        time, price, candle.identifier, profit_loss_percentage)

    # exract extra fields from extra files
    for file in moments_extra_files:
        field_names = file[0]
        field_length = len(field_names)
        fields = [f for f in file[moment_index]]

        for j in range(field_length):
            this_moment.__setattr__(field_names[j], float(fields[j]))

    try_strategies(this_moment, candles)
    check_view_essentials(this_moment, moment_index,
                          bitcoin_balance, dollar_balance)


def analyze_data(candles: list, csv_file_name: str, moments_extra_files: dict):
    files = open_extra_files(moments_extra_files)

    control_logs()

    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        moments_data = list(csv_reader)
        moment_index = 1
        for c in candles:   # the i th moment of candle
            log_info(c)

            for _ in range(scenario.number_of_moments_in_a_candle):
                analyze_each_moment(
                    moments_data, moment_index, files, c, candles)
                moment_index += 1

                log_info(f"    {this_moment}")

            print('Analyzing :', round(100 * c.identifier / len(candles), 2), '%')

        control_views(strategy_results)


def profit_loss_calculator(moment_index: int, this_moment_price: float) -> float:
    global start_of_profit_loss_period_balance
    x = dollar_balance + bitcoin_balance * this_moment_price
    if (moment_index - 1) % scenario.profit_loss_period_step == 0:
        start_of_profit_loss_period_balance = x
        return 0
    else:
        return round((x - start_of_profit_loss_period_balance) * 100 / start_of_profit_loss_period_balance, 4)


def try_strategies(moment: Moment, candles: list):
    global working_strategies, bitcoin_balance, dollar_balance
    if scenario.lock_method == 'lock_to_hour':
        for locked in list(strategies.lock_strategies):       # unlock strategies
            if strategies.lock_strategies[locked][1] == moment.candle_id:
                strategies.lock_strategies.pop(locked)

    for ws in working_strategies:   # continue the work of opened strategies
        ws.continue_strategy()

    # remove finished strategies from working_strategies
    working_strategies = [ws for ws in working_strategies if ws.working]

    for s in strategies.strategies:     # try to start not locked strategies
        if not s in strategies.lock_strategies:
            strtg = strategies.strategies[s](
                moment, bitcoin_balance, dollar_balance, candles)
            if strtg.working:
                working_strategies.append(strtg)


def buy(bitcoin: int, price: int):
    if scenario.live_trading_mode:
        exchange_buy(bitcoin, price)
        return

    global bitcoin_balance, dollar_balance
    bitcoin_balance += bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    dollar_balance -= (bitcoin * price * (1 + scenario.fee))
    dollar_balance = round(dollar_balance, 4)
    if dollar_balance < 0:
        raise RuntimeError('dollar balance is negative')


def sell(bitcoin: int, price: int):
    if scenario.live_trading_mode:
        exchange_sell(bitcoin, price)
        return

    global bitcoin_balance, dollar_balance
    bitcoin_balance -= bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    if bitcoin_balance < 0:
        raise RuntimeError('bitcoin balance is negative')
    dollar_balance += (bitcoin * price * (1 - scenario.fee))
    dollar_balance = round(dollar_balance, 4)


def get_this_moment() -> Moment:
    return this_moment


def set_report(r: str):
    strategy_results.append(r)


# ================= LIVE TRADING =======================
def calculate_indicators_and_bundle_into_candles(candles: list):
    log_debug("constructed candles:")
    for c in candles:
        log_debug(f"\t{c}")


def set_this_moment(moment: Moment):
    global this_moment
    this_moment = moment


def analyze_live_data(candles: list, start_time: int):
    global this_moment
    moment_index = 1

    calculate_indicators_and_bundle_into_this_moment()
    try_strategies(this_moment, candles)
    while True:
        sleep_till_end_of_moment(start_time)

        start_time = time()
        moment_index += 1
        sync_bot_data_with_exchange(candles)

        try_strategies(this_moment, candles)


def sleep_till_end_of_moment(last_wake_time: int):
    x = get_time_from_exchange() - last_wake_time + \
        scenario.live_sleep_between_each_moment + scenario.live_calculations_threshold
    x = x // 60 * 60    # round the sleep time into minutes
    sleep(x)    # TODO: release system resources at this time


def sync_bot_data_with_exchange(candles: list, moment_index: int):
    global this_moment
    candle = get_last_candle()
    t, p, cid = get_current_data_from_exchange()
    this_moment.update_moment(
        t, p, cid, profit_loss_calculator(moment_index, p))
    calculate_indicators_and_bundle_into_this_moment()

    if is_same_as(candle, candles[-1]):
        new_candle = [candle]
        calculate_indicators_and_bundle_into_candles(new_candle)

        # for compatibility with first moment
        candles.pop(0)
        candles.append(candle)


def is_same_as(c1: Candle, c2: Candle) -> bool:
    pass


def calculate_indicators_and_bundle_into_this_moment():
    global this_moment
    log_debug(f"constructed this_moment: {this_moment}")
