# YA HUSSEIN
from time import sleep

from controller.controller import calculate_indicators_and_bundle_into_candles, set_this_moment, analyze_live_data, \
    set_start_of_work_balance
from controller.exchange_controller import exchange_controller, SERVER_SIDE_ERROR
from controller.view_controller import *


def live_main():
    get_start_time()

    exchange_controller.configure_market()

    candles = exchange_controller.get_n_past_candles(scenario.live_start_of_work_needed_candles, 1)
    calculate_indicators_and_bundle_into_candles(candles)

    p, t, db, cb = get_current_data()

    this_moment = Moment(t / 1000.0, p, candles[-1].identifier)
    set_this_moment(this_moment)
    set_start_of_work_balance(cb, db)

    analyze_live_data(candles)


def get_current_data() -> tuple:
    while True:
        current_data = exchange_controller.get_current_data_from_exchange()
        if current_data == SERVER_SIDE_ERROR:
            sleep(scenario.live_try_again_time_inactive_market)
        else:
            break
    return current_data[0], current_data[1], current_data[2][0], current_data[2][1]


def get_start_time():
    while True:
        start_time = exchange_controller.get_time_from_exchange()
        if start_time == SERVER_SIDE_ERROR:
            sleep(scenario.live_try_again_time_inactive_market)
            continue
        log_info(f"live trading started at time: {start_time}")
        break


control_logs()
live_main()
