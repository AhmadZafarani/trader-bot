from abc import ABC, abstractmethod

import controller.controller as controller
from model.Moment import Moment

"""
    in order of implementing a new strategy you must do these 2 steps:
        1. implement your strategy as a class (every thing out of a class would ignored) witch inherits from 
            this abstract class; Strategy
        2. register class name into the dictionary 'strategies'; witch defined in last line of this file 
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
    def __init__(self, moment: Moment, btc: float, dollar: float, candles: list, logger, name: str):
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
        self.logger = logger
        self.short_name = name
        self.id = self.__str__()
        if self.strategy_works():
            self.working = True
            self.logger.warning(
                f"strategy \"{self.id}\" started in {self.moment.get_time_string()}")
            self.start_strategy()

    @abstractmethod
    def strategy_works(self) -> bool:
        pass

    @abstractmethod
    def start_strategy(self):
        pass

    @abstractmethod
    def continue_strategy(self, working_strategies, **kwargs):
        pass

    def finish_strategy(self, args=''):
        controller.set_report(Strategy.report(self.buy_price, controller.get_this_moment().price,
                                              self.__class__.__name__, self.buy_volume, self.sell_volume, args))
        self.working = False
        self.logger.warning(
            f'{self.id} finished in {self.moment.get_time_string()}')

    @staticmethod
    def report(buy_price: int, sell_price: int, strategy_name: str, bought_volume: int, sold_volume: int,
               args: str) -> str:
        if buy_price <= sell_price:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\n' \
                f'Bought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tProfit\n' \
                f'more information:\t{args}\n\n'
        else:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\n' \
                f'Bought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tLoss\n' \
                f'more information:\t{args}\n\n'
        return s
