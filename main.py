# YA HUSSEIN
from time import sleep

from controller.controller import calculate_indicators_and_bundle_into_candles, \
    set_this_moment, analyze_live_data
from controller.exchange_controller import connect_to_exchange, get_n_past_candles, get_current_data_from_exchange, \
    get_time_from_exchange, configure_market, SERVER_SIDE_ERROR
from controller.view_controller import *


def live_main():
    exchange = connect_to_exchange()

    get_start_time(exchange)

    configure_market(exchange)

    candles = get_n_past_candles(exchange, scenario.live_start_of_work_needed_candles, 1)
    calculate_indicators_and_bundle_into_candles(candles)

    p, t = get_time_and_price(exchange)

    this_moment = Moment(t / 1000.0, p, candles[-1].identifier)
    set_this_moment(this_moment)

    analyze_live_data(exchange, candles)


def get_time_and_price(exchange):
    while True:
        t, p = get_current_data_from_exchange(exchange)
        if t == SERVER_SIDE_ERROR and p == SERVER_SIDE_ERROR:
            sleep(scenario.live_try_again_time_inactive_market)
        else:
            break
    return p, t


def get_start_time(exchange):
    while True:
        start_time = get_time_from_exchange(exchange)
        if start_time == SERVER_SIDE_ERROR:
            sleep(scenario.live_try_again_time_inactive_market)
            continue
        log_info(f"live trading started at time: {start_time}")
        break


control_logs()
live_main()
