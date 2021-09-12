# YA SAJJAD
from time import sleep
import ccxt

from model.Candle import Candle
from controller.view_controller import *


def read_api_key() -> tuple:
    with open("../api-key-kucoin.txt", "r") as file:
        key = file.readline().split()[1][1:-2]
        secret = file.readline().split()[1][1:-2]
        password = file.readline().split()[1][1:-1]
    return key, secret, password


def connect_to_exchange() -> ccxt.Exchange:
    key, secret, password = read_api_key()
    exchange = ccxt.kucoin(config={
        'apiKey': key,
        'secret': secret,
        'password': password,
    })
    exchange.set_sandbox_mode(True)
    exchange.load_markets()
    print("connected to KUCOIN")
    return exchange


def get_n_past_candles(exchange: ccxt.Exchange, n: int) -> list:
    while True:
        # multiply to ensure fetch more than `n` candles
        candles = exchange.fetch_ohlcv(
            scenario.live_market, scenario.live_timeframe, limit=3 * n)
        if len(candles) >= n:
            break
        log_debug(
            "couldn't fetch all of your candles. we will try after 5 seconds.")
        sleep(5)
    candle_objects = []
    for i in range(n):
        candle_objects.append(Candle(identifier=candles[i][0] // 1000, open_price=candles[i][1],
                                     high_price=candles[i][2], low_price=candles[i][3], close_price=candles[i][4],
                                     traded_volume=candles[i][5]))
    return candle_objects


def get_last_candle(exchange: ccxt.Exchange) -> Candle:
    c = get_n_past_candles(exchange, 1)
    return c[0]


def get_current_data_from_exchange(exchange: ccxt.Exchange) -> tuple:
    log_debug("current data: request sent to KUCOIN")
    return get_time_from_exchange(exchange), 2, get_last_candle(exchange).identifier


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
