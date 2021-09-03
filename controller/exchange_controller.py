# YA SAJJAD
from time import time
from random import randint

from model.Candle import Candle
from controller.view_controller import *


def connect_to_exchange():
    print("connected to KUCOIN")


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


def get_time_from_exchange() -> int:
    log_debug("connection successfull to KUCOIN")
    return int(time())
