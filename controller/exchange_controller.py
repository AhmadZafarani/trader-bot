# YA SAJJAD
from random import randint
from time import sleep
import ccxt

from model.Candle import Candle
from controller.view_controller import *


def read_api_key() -> tuple:
    key = None
    secret = None
    with open("../api-key-kucoin.txt", "r") as file:
        key = file.readline().split()[1][1:-2]
        secret = file.readline().split()[1][1:-1]
    return key, secret


def connect_to_exchange() -> ccxt.Exchange:
    key, secret = read_api_key()
    exchange = ccxt.kucoin(config={
        'apiKey': key,
        'secret': secret,
        'password': '13467978aA',
    })
    exchange.set_sandbox_mode(True)
    exchange.load_markets()
    print("connected to KUCOIN")
    return exchange


def get_n_past_candles(exchange: ccxt.Exchange, n: int) -> list:
    while True:
        # multiply to ensure fetch more than `n` candles
        candles = exchange.fetch_ohlcv(
            scenario.live_market, scenario.live_timeframe, limit=3*n)
        if len(candles) >= n:
            break
        log_debug(
            "couldn't fetch all of your're candles. we will try after 5 seconds.")
        sleep(5)
    candle_objects = []
    for i in range(n):
        candle_objects.append(Candle(
            candles[i][0] // 1000, candles[i][1], candles[i][2], candles[i][3], candles[i][4], candles[i][5]))
    return candle_objects


def get_last_candle() -> Candle:
    pass


def get_current_data_from_exchange() -> tuple:
    log_debug("current data: request sent to KUCOIN")
    return randint(1, 100), randint(1, 100), randint(1, 100)


def exchange_buy(crypto: float, price: float):
    pass


def exchange_sell(crypto: float, price: float):
    pass


def get_time_from_exchange(exchange: ccxt.Exchange) -> int:
    # not available for all exchanges
    return exchange.fetch_time()


def configure_market(exchange: ccxt.Exchange):
    market = exchange.market(scenario.live_market)
    market_state = market['active']
    log_debug(
        f"market was at state: {market_state} in time: {get_time_from_exchange(exchange)}")

    if market_state:
        if not (scenario.fee == market['maker'] == market['taker']):
            raise Exception("inconsistent fees")

        log_debug(f"market: {market['info']} fetched successfully")
        return market
    return None
