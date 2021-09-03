# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from scenario import scenario
from controller.exchange_controller import connect_to_exchange, get_n_past_candles

from pathlib import Path
from time import time


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
    start_time = time()
    connect_to_exchange()
    candles = get_n_past_candles(scenario.live_start_of_work_needed_candles)
    indicators = calculate_indicators(candles)
    try_strategies()
    while True:
        sleep_till_end_of_moment(start_time)

        start_time = time()
        get_last_candle()
        calculate_indicators()
        try_strategies()


n = int(input("press 1 for simulate trading on historical data. \npress 2 for live trading. \n"))
if n == 1:
    main()
elif n == 2:
    live_main()
else:
    raise Exception("only press 1 or 2 :|")
