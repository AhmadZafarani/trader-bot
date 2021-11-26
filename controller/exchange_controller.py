# YA SAJJAD
from time import sleep

import ccxt
from cryptography.fernet import Fernet

from controller.view_controller import *
from model.Candle import Candle

SERVER_SIDE_ERROR = -1


def read_api_key() -> tuple:
    f = Fernet(scenario.live_api_encryption_key)
    with open("api-kucoin.txt", "r") as file:
        key = file.readline().split()[1][1:-2].encode()
        secret = file.readline().split()[1][1:-2].encode()
        password = file.readline().split()[1][1:-1].encode()
    key, secret, password = map(f.decrypt, (key, secret, password))
    return key.decode(), secret.decode(), password.decode()


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


class ExchangeController:
    def __init__(self):
        key, secret, password = read_api_key()
        exchange = ccxt.kucoin(config={
            'apiKey': key,
            'secret': secret,
            'password': password,
        })
        exchange.set_sandbox_mode(True)
        exchange.load_markets()
        print("connected to KUCOIN")
        self.exchange = exchange

    def get_n_past_candles(self, n: int, start_index: int, handle_failure=True):
        candles = []
        while True:
            # multiply to ensure fetch more than `n` candles
            try:
                candles = self.exchange.fetch_ohlcv(scenario.live_market, scenario.live_timeframe, limit=3 * n)
            except Exception as e:
                log_error("error in get_n_past_candles" + str(e))
                if not handle_failure:
                    return SERVER_SIDE_ERROR

                sleep(scenario.live_try_again_time_inactive_market)
                continue

            if len(candles) >= n:
                break
            log_warning("couldn't fetch all of your candles. we will try again after 5 seconds.")
            sleep(5)
        return build_candle_objects_from_fetched_data(candles, n, start_index)

    def get_current_data_from_exchange(self):
        ret1 = self.get_time_from_exchange()
        ret2 = self.get_current_price()
        ret3 = self.get_current_balance()
        if ret1 == SERVER_SIDE_ERROR or ret2 == SERVER_SIDE_ERROR or ret3 == SERVER_SIDE_ERROR:
            return SERVER_SIDE_ERROR
        else:
            return ret1, ret2, ret3

    def exchange_buy(self, crypto: float, price: float):
        order = self.exchange.create_limit_buy_order(scenario.live_market, crypto, price)
        print(order)
        print(self.exchange.fetch_open_orders())
        print(f"exchange buy with price: {price} and volume: {crypto} .")

    def exchange_sell(self, crypto: float, price: float):
        order = self.exchange.create_limit_sell_order(scenario.live_market, crypto, price)
        print(order)
        print(self.exchange.fetch_open_orders())
        print(f"exchange sell with price: {price} and volume: {crypto} .")

    def get_time_from_exchange(self) -> int:
        # not available for all exchanges
        try:
            return self.exchange.fetch_time()
        except Exception as e:
            log_error("error in get_time_from_exchange => " + str(e))
            return SERVER_SIDE_ERROR

    def configure_market(self):
        while True:
            market = self.exchange.market(scenario.live_market)
            market_state = market['active']
            ret = self.get_time_from_exchange()
            if ret == SERVER_SIDE_ERROR:
                sleep(scenario.live_try_again_time_inactive_market)
                continue
            log_debug(f"market was at state: {market_state} in time: {ret}")

            if not market_state:
                log_warning(f"market isn't active right now. we will try again "
                            f"{scenario.live_try_again_time_inactive_market} seconds later.")
                sleep(scenario.live_try_again_time_inactive_market)
                self.exchange.load_markets(reload=True)
                continue
            if not (scenario.fee == market['maker'] == market['taker']):
                raise RuntimeError("inconsistent fees")

            log_debug(f"market: {market['info']} fetched successfully")
            return

    def get_current_price(self) -> float:
        try:
            exchange: ccxt.kucoin
            trades = self.exchange.fetch_trades(scenario.live_market)
            price = trades[-1]['price']
            log_info(f"now {scenario.live_market} price is: {price}")
            return price
        except Exception as e:
            log_error("error in get_current_price => " + str(e))
            return SERVER_SIDE_ERROR

    def get_current_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            try:
                dollar_balance = balance[scenario.live_quote]['free']
            except KeyError:
                dollar_balance = 0
            try:
                crypto_balance = balance[scenario.live_base]['free']
            except KeyError:
                crypto_balance = 0
            log_info(f"now we have {dollar_balance} dollars and {crypto_balance} crypto.")
            return dollar_balance, crypto_balance
        except Exception as e:
            log_error("error in get_current_balance => " + str(e))
            return SERVER_SIDE_ERROR


exchange_controller = ExchangeController()
