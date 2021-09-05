# YA HOSSEIN
from pathlib import Path
from time import time

from controller.controller import data_converter, analyze_data, calculate_indicators_and_bundle_into_candles, \
    set_this_moment, analyze_live_data
from scenario import scenario
from controller.exchange_controller import connect_to_exchange, get_n_past_candles, get_current_data_from_exchange, \
    get_time_from_exchange
from model.Moment import Moment
from controller.view_controller import *


def main():
    start_time = time()

    data_folder = Path("data")
    candles_file = data_folder / scenario.candles_data_csv_file_name
    moments_file = data_folder / scenario.moment_data_csv_file_name

    extra_candle_files = {}
    for ecdf in scenario.extra_candles_data_files:
        extra_candle_files[ecdf] = data_folder / \
            scenario.extra_candles_data_files[ecdf]

    extra_moment_files = {}
    for emdf in scenario.extra_moments_data_files:
        extra_moment_files[emdf] = data_folder / \
            scenario.extra_moments_data_files[emdf]

    candles = data_converter(candles_file, extra_candle_files)

    analyze_data(candles, moments_file, extra_moment_files)

    print('total runtime : ', time() - start_time)


def live_main():
    exchange = connect_to_exchange()
    start_time = get_time_from_exchange(exchange)
    log_debug(f"live trading started at time: {start_time}")

    # candles = get_n_past_candles(scenario.live_start_of_work_needed_candles)
    # calculate_indicators_and_bundle_into_candles(candles)
    # t, p, cid = get_current_data_from_exchange()
    # this_moment = Moment(t, p, cid)
    # set_this_moment(this_moment)
    # analyze_live_data(candles, start_time)


control_logs()
n = int(input("press 1 for simulate trading on historical data. \npress 2 for live trading. \n"))
if n == 1:
    main()
elif n == 2:
    scenario.live_trading_mode = True
    live_main()
else:
    raise Exception("only press 1 or 2 :|")
