# YA SAJJAD
from time import sleep
import ccxt
from ccxt.base.errors import RequestTimeout
from cryptography.fernet import Fernet

from model.Candle import Candle
from controller.view_controller import *


def read_api_key() -> tuple:
    f = Fernet(scenario.live_api_encryption_key)
    with open("api-kucoin.txt", "r") as file:
        key = file.readline().split()[1][1:-2].encode()
        secret = file.readline().split()[1][1:-2].encode()
        password = file.readline().split()[1][1:-1].encode()
    key, secret, password = map(f.decrypt, (key, secret, password))
    return key.decode(), secret.decode(), password.decode()


def connect_to_exchange() -> ccxt.Exchange:
    key, secret, password = read_api_key()
    exchange = ccxt.kucoin(config={
        'apiKey': key,
        'secret': secret,
        'password': password,
    })
    exchange.set_sandbox_mode(False)
    exchange.load_markets(params={'timeout': 20000})
    print("connected to KUCOIN")
    return exchange


def get_n_past_candles(exchange: ccxt.Exchange, n: int, start_index: int) -> list:
    global first_candle_time

    while True:
        # multiply to ensure fetch more than `n` candles
        try:
            candles = exchange.fetch_ohlcv(
                scenario.live_market, scenario.live_timeframe, limit=3 * n)
        except RequestTimeout as e:
            log_warning(e.with_traceback(None))
            sleep(scenario.live_try_again_time_inactive_market)
            continue

        if len(candles) >= n:
            break
        log_debug(
            "couldn't fetch all of your candles. we will try again after 5 seconds.")
        sleep(5)

    return build_candle_objects_from_fetched_data(candles, n, start_index)


def build_candle_objects_from_fetched_data(candles: list, n: int, start_index: int) -> list:
    candle_objects = []
    j = 0
    for i in range(len(candles) - n, len(candles)):
        candle_objects.append(Candle(
            # for start the candle_id from 1 and use it like index
            identifier=start_index + j, open_price=candles[i][1],
            high_price=candles[i][2], low_price=candles[i][3],
            close_price=candles[i][4], traded_volume=candles[i][5]
        ))
        candle_objects[j].set_timestamp(candles[i][0])
        j += 1
    return candle_objects


def get_last_candle(exchange: ccxt.Exchange, start_index: int) -> Candle:
    c = get_n_past_candles(exchange, 1, start_index)
    return c[0]


def get_current_data_from_exchange(exchange: ccxt.Exchange) -> tuple:
    return get_time_from_exchange(exchange), get_current_price(exchange)


def exchange_buy(crypto: float, price: float):
    print(f"exchange buy with price: {price} and volume: {crypto} .")


def exchange_sell(crypto: float, price: float):
    print(f"exchange sell with price: {price} and volume: {crypto} .")


def get_time_from_exchange(exchange: ccxt.Exchange) -> int:
    # not available for all exchanges
    while True:
        try:
            return exchange.fetch_time()
        except ccxt.RequestTimeout as e:
            log_warning(e.with_traceback(None))
            sleep(scenario.live_try_again_time_inactive_market)


def configure_market(exchange: ccxt.Exchange):
    while True:
        market = exchange.market(scenario.live_market)
        market_state = market['active']
        log_debug(
            f"market was at state: {market_state} in time: {get_time_from_exchange(exchange)}")

        if not market_state:
            log_warning(
                f"market isn't active right now. we will try again {scenario.live_try_again_time_inactive_market} seconds later.")
            sleep(scenario.live_try_again_time_inactive_market)
            exchange.load_markets(reload=True)
            continue
        if not (scenario.fee == market['maker'] == market['taker']):
            raise Exception("inconsistent fees")

        log_debug(f"market: {market['info']} fetched successfully")
        return


def get_current_price(exchange: ccxt.Exchange) -> float:
    trades = exchange.fetch_trades(scenario.live_market)
    price = trades[-1]['price']
    log_info(f"now {scenario.live_market} price is: {price}")
    return price
