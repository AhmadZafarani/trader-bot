# YA REZA
from model.Moment import Moment
from abc import ABC, abstractmethod
import controller.controller as controller
from scenario import scenario
from controller.logs import setup_logger
import logging
"""
    in order of implementing a new strategy you must do these 2 steps:
        1. implement your strategy as a class (every thing out of a class would ignored) witch inherits from 
            this abstract class; Strategy
        2. reguster class name into the dictionay 'strategies'; witch defined in last line of this file 
            (all the classes must implemented above this dictionary). dictionary is like: 
            'StrategyName': StrategyClass
"""
""" 
    for inheriting the Strategy class, you must implement 3 methods:
        1. strategy_works: ** returns a bool **
        2. start_strategy
        3. continue_strategy: ** don't forget to call 'finish_strategy' in the case of the strategy doesn't continue
            more (at the last line of that case) **
"""
"""
    'report' method of Strategy accepts an optional argument 'args', as a string (str). every information witch
    needed to logged as Strategy results, can be passed to this method as a string. but this work only can be
    done by passing this argument to 'finish_strategy' method at the time of closing the strategy
"""


class Strategy(ABC):
    def __init__(self, moment: Moment, btc: float, dollar: float, candles: list):
        self.moment = moment
        self.candles = candles
        self.working = False
        self.buy_price = 0
        self.sell_price = 0
        self.buy_volume = 0
        self.sell_volume = 0
        self.dollar_balance = dollar
        self.sold_volume = 0
        self.sell_time_date = "0/0/0"
        self.sell_time_hour = 0
        self.sell_time_minute = 0

        self.btc_balance = btc
        if self.strategy_works():
            self.working = True
            self.start_strategy()

    @abstractmethod
    def strategy_works(self) -> bool:
        pass

    @abstractmethod
    def start_strategy(self):
        pass

    @abstractmethod
    def continue_strategy(self):
        pass

    def finish_strategy(self, args=''):
        controller.set_report(Strategy.report(self.buy_price, controller.get_this_moment().price,
                                              self.__class__.__name__, self.buy_volume, self.sell_volume, args))
        self.working = False

    @staticmethod
    def report(buy_price: int, sell_price: int, strategy_name: str, bought_volume: int, sold_volume: int, args: str) -> str:
        if buy_price <= sell_price:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tProfit\nmore informatons:\t{args}\n\n'
        else:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tLoss\nmore informatons:\t{args}\n\n'
        return s


lock_strategies = {}

setup_logger('cndl-extra', r'logs/cndl-extra.log')   
log2 = logging.getLogger('cndl-extra')

class Dummy_Strategy(Strategy):

    def strategy_works(self) -> bool:
        global log2
        log2.error(f'''Candle => {self.candles[self.moment.candle_id - 1]}
        ADX => {self.candles[self.moment.candle_id - 1].adx}, {self.candles[self.moment.candle_id - 1].DI_plus}, {self.candles[self.moment.candle_id - 1].DI_minus}
        ICHI => {self.candles[self.moment.candle_id - 1].conversion_line}, {self.candles[self.moment.candle_id - 1].base_line}, {self.candles[self.moment.candle_id - 1].lagging_span}, {self.candles[self.moment.candle_id - 1].leading_line1}, {self.candles[self.moment.candle_id - 1].leading_line2}
        ''')
        return self.moment.hour == 13 and self.moment.minute == 0

    def start_strategy(self):
        self.buy_volume = 1
        self.sell_volume = 1
        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_time = [self.moment.hour, self.moment.minute]

    def continue_strategy(self):
        if not (controller.get_this_moment().hour == 15 and controller.get_this_moment().minute == 0):
            return
        controller.sell(self.sell_volume, controller.get_this_moment().price)
        self.finish_strategy(f'''date: {self.moment.date}
        Candle : {self.C}
        buy_time : {self.buy_time[0]} : {self.buy_time[1]} 
        ''')




strategies = {'dummy': Dummy_Strategy}