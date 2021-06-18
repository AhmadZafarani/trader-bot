# YA REZA
from model.Moment import Moment
from abc import ABC, abstractmethod
import controller.controller as controller
from scenario import *
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

        # print(dollar)
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


lock_strategies = {'Dummy': [Dummy_Strategy, 0]}


class ADX12(Strategy):
    def strategy_works(self) -> bool:
        if opening_con1_num_of_candles == 3:
            if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].moving12 and \
               self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].moving12 and \
               self.candles[self.moment.candle_id - 3].open_price > self.candles[self.moment.candle_id - 3].moving12 and \
               self.candles[self.moment.candle_id - 3].close_price > self.candles[self.moment.candle_id - 3].moving12 and \
               self.candles[self.moment.candle_id - 4].close_price > self.candles[self.moment.candle_id - 4].open_price and \
               ((self.candles[self.moment.candle_id - 4].close_price - self.candles[self.moment.candle_id - 4].moving12) / (
                   self.candles[self.moment.candle_id - 4].close_price - self.candles[self.moment.candle_id - 4].open_price)) \
               * 100 > opening_con1_min_first:
                if opening_con2_di_method == "positive":
                    if self.candles[self.moment.candle_id - 2].DI_plus > self.candles[self.moment.candle_id - 2].DI_minus and \
                       self.candles[self.moment.candle_id - 2].adx > opening_con2_min_adx:
                        return True
                elif opening_con2_di_method == "increasing":
                    if self.candles[self.moment.candle_id - 2].DI_plus - self.candles[self.moment.candle_id - 2].DI_minus > \
                            self.candles[self.moment.candle_id - 3].DI_plus - self.candles[self.moment.candle_id - 3].DI_minus and \
                       self.candles[self.moment.candle_id - 2].adx > opening_con2_min_adx:
                        return True
        elif opening_con1_num_of_candles == 2:
            if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].moving12 and \
               self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].open_price and \
               self.candles[self.moment.candle_id - 3].close_price > self.candles[self.moment.candle_id - 3].open_price and \
               ((self.candles[self.moment.candle_id - 3].close_price - self.candles[self.moment.candle_id - 3].moving12) / (
                   self.candles[self.moment.candle_id - 3].close_price - self.candles[self.moment.candle_id - 3].open_price)) \
               * 100 > opening_con1_min_first:
                if opening_con2_di_method == "positive":
                    if self.candles[self.moment.candle_id - 2].DI_plus > self.candles[self.moment.candle_id - 2].DI_minus and \
                       self.candles[self.moment.candle_id - 2].adx > opening_con2_min_adx:
                        return True
                elif opening_con2_di_method == "increasing":
                    if self.candles[self.moment.candle_id - 2].DI_plus - self.candles[self.moment.candle_id - 2].DI_minus > \
                        self.candles[self.moment.candle_id - 3].DI_plus - self.candles[self.moment.candle_id - 3].DI_minus and \
                            self.candles[self.moment.candle_id - 2].adx > opening_con2_min_adx:
                        return True
        elif opening_con1_num_of_candles == 1:
            if self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].open_price and \
                ((self.candles[self.moment.candle_id - 2].close_price - self.candles[self.moment.candle_id - 2].moving12) / (
                    self.candles[self.moment.candle_id - 2].close_price - self.candles[self.moment.candle_id - 2].open_price)) \
                    * 100 > opening_con1_min_first:
                if opening_con2_di_method == "positive":
                    if self.candles[self.moment.candle_id-2].DI_plus > self.candles[self.moment.candle_id-2].DI_minus and \
                            self.candles[self.moment.candle_id - 2].adx > opening_con2_min_adx:
                        return True
                elif opening_con2_di_method == "increasing":
                    if self.candles[self.moment.candle_id - 2].DI_plus - self.candles[self.moment.candle_id - 2].DI_minus > \
                        self.candles[self.moment.candle_id - 3].DI_plus - self.candles[self.moment.candle_id - 3].DI_minus and \
                            self.candles[self.moment.candle_id - 2].adx > opening_con2_min_adx:
                        return True

    def start_strategy(self):
        global lock_strategies
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.buy_volume = (self.dollar_balance /
                           self.moment.price) * (volume_buy / 100)

        self.ADX = [self.candles[self.moment.candle_id - 2].adx, self.candles[self.moment.candle_id - 2].DI_plus,
                    self.candles[self.moment.candle_id - 2].DI_minus]
        self.C = self.candles[self.moment.candle_id - 1]
        self.Mom_str = self.moment.__str__()
        self.id = self.moment.candle_id
        self.MA = [self.candles[self.moment.candle_id - 1].moving12, self.candles[self.moment.candle_id - 2].moving12,
                   self.candles[self.moment.candle_id - 3].moving12, self.candles[self.moment.candle_id - 4].moving12]
        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        if lock_method == 'lock_to_hour':
            lock_strategies["adx"] = [ADX12, self.moment.candle_id + lock_hour]
        elif lock_method == "lock_to_fin":
            lock_strategies["adx"] = [ADX12, 0]

    def sell_method1(self, candle_id: int) -> bool:
        if closing_meth1_num_of_candles == 3:
            if self.candles[candle_id - 2].open_price < self.candles[candle_id - 2].moving12 and \
               self.candles[candle_id - 2].close_price < self.candles[candle_id - 2].moving12 and \
                    self.candles[candle_id - 3].open_price < self.candles[candle_id - 3].moving12 and \
                    self.candles[candle_id - 3].close_price < self.candles[candle_id - 3].moving12 and \
                    self.candles[candle_id - 4].close_price < self.candles[candle_id - 4].open_price and \
                    ((self.candles[candle_id - 4].moving12 - self.candles[candle_id - 4].close_price) / (
                        self.candles[candle_id - 4].open_price - self.candles[candle_id - 4].close_price)) \
               * 100 > closing_met1_min_first:
                return True
        elif closing_meth1_num_of_candles == 2:
            if self.candles[candle_id - 2].open_price < self.candles[candle_id-2].moving12 and \
               self.candles[candle_id - 2].close_price < self.candles[candle_id-2].moving12 and \
               self.candles[candle_id - 3].close_price < self.candles[candle_id-3].open_price and \
               ((self.candles[candle_id - 3].moving12 - self.candles[candle_id-3].close_price) / (
                   self.candles[candle_id - 3].open_price - self.candles[candle_id-3].close_price)) * 100 > closing_met1_min_first:
                return True
        elif closing_meth1_num_of_candles == 1:
            if self.candles[candle_id-2].close_price < self.candles[candle_id-2].open_price and \
               ((self.candles[candle_id-2].moving12 - self.candles[candle_id-2].close_price) / (
                   self.candles[candle_id-2].open_price - self.candles[candle_id-2].close_price)) * 100 > closing_met1_min_first:
                return True
        return False

    def sell_method2(self) -> bool:
        return self.candles[self.moment.candle_id - 2].DI_plus < self.candles[self.moment.candle_id - 2].DI_minus and \
            self.candles[self.moment.candle_id - 2].adx > closing_met2_max_adx

    def sell_method3(self) -> bool:
        return ((self.moment.price - self.buy_price) / self.buy_price) * 100 > profit_limit or \
            ((self.moment.price - self.buy_price) /
             self.buy_price) * 100 < loss_limit

    def fin_and_before(self):
        global lock_strategies
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        controller.sell(self.buy_volume, controller.get_this_moment().price)
        self.finish_strategy(args=f"""
        buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume , 3)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 3)})
        fee : {0.001*(self.buy_price * self.buy_volume) + 0.001 * (self.sell_price  * self.buy_volume ) } $
        ADX(-1) : {self.ADX[0]} , {self.ADX[1]} , {self.ADX[2]}
        MA12 : {self.MA[0]} {self.MA[1]} {self.MA[2]} {self.MA[3]}
        Candel : {self.C}
        Moment : {self.Mom_str}
        ID : {self.id}
        """)
        if lock_method == "lock_to_fin":
            lock_strategies.pop("adx")

    def continue_strategy(self):
        global lock_strategies
        if intraction == 1:
            if self.sell_method3():
                self.fin_and_before()
        elif intraction == 2:
            if self.sell_method2():
                self.fin_and_before()
        elif intraction == 3:
            if self.sell_method2() or self.sell_method3():
                self.fin_and_before()
        elif intraction == 4:
            if self.sell_method1(self.moment.candle_id):
                self.fin_and_before()
        elif intraction == 5:
            if self.sell_method3() or self.sell_method1(self.moment.candle_id):
                self.fin_and_before()
        elif intraction == 6:
            if self.sell_method2() or self.sell_method1(self.moment.candle_id):
                self.fin_and_before()
        elif intraction == 7:
            if self.sell_method3() or self.sell_method2() or self.sell_method1(self.moment.candle_id):
                self.fin_and_before()


strategies = {'adx': ADX12}
