# YA SAJJAD
from random import randint
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
        'key': key,
        'secret': secret
    })
    exchange.set_sandbox_mode(True)
    exchange.load_markets()
    print("connected to KUCOIN")
    return exchange


def get_n_past_candles(n: int) -> list:
    candles = []
    for i in range(n):
        candles.append(Candle(i, randint(1, 100), randint(
            1, 100), randint(1, 100), randint(1, 100), randint(1, 100)))
    log_debug("successfull response from KUCOIN")
    return candles


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
    return exchange.fetch_time()
