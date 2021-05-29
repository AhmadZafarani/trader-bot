# YA REZA
from model.Moment import Moment
from abc import ABC, abstractmethod
import controller.controller as controller

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
        self.buy_volume = 0
        self.sell_volume = 0
        self.dollar_balance = dollar
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


class Dummy_Strategy(Strategy):
    def strategy_works(self) -> bool:
        return self.moment.hour == 13 and self.moment.minute == 0

    def start_strategy(self):
        self.buy_volume = 1
        self.sell_volume = 1
        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price

    def continue_strategy(self):
        if not (controller.get_this_moment().hour == 15 and controller.get_this_moment().minute == 0):
            return
        controller.sell(self.sell_volume, controller.get_this_moment().price)
        self.finish_strategy(f'date: {self.moment.date}')


lock_strategies = {'Dummy': [Dummy_Strategy , 0]}

# def lock_strategy(name):
#     lock_strategies[name] = strategies[name]
# def unlock_strategy(name):
#     lock_strategies.pop(name)
"""
moving avrage base strategy 
[*] check if last more of 50% of previous candle is upper than the moving avrage 
[*] check if current candle is green and more than 0.3 % long 
[*] lock strategy in buy
[*] sell in +1% and -0.5%
[*] unlock strategy in sell 
"""



strategies = {'Dummy': Dummy_Strategy, 'Moving': MovingAvrage}
