# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path
from time import time
from scenario import scenario
from os import remove


def main():
    try:
        remove("balance_report.csv")
        remove("periodical_report.csv")
        remove("strategy_result.txt")
    except:
        pass

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


if __name__ == "__main__":
    main()
