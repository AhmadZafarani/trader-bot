# YA SAJJAD
from time import time

from model.Candle import Candle


def connect_to_exchange():
    pass


def get_n_past_candles(n: int) -> list:
    pass


def get_last_candle() -> Candle:
    pass


def get_current_data_from_exchange() -> tuple:
    pass


def exchange_buy(crypto: float, price: float):
    pass


def exchange_sell(crypto: float, price: float):
    pass


def get_time_from_exchange() -> int:
    return int(time())
