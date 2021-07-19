# YA REZA
from model.Moment import Moment
from abc import ABC, abstractmethod
import controller.controller as controller
from scenario import scenario
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


lock_strategies = {}


class ICHI_CROSS(Strategy):
    def check_open_con(self, i: int) -> bool:
        if i == 0:
            if self.candles[self.moment.candle_id - 2].DI_plus > self.candles[self.moment.candle_id - 2].DI_minus and \
                    self.candles[self.moment.candle_id - 2].adx > scenario.adx_min:
                return True
            else:
                return False
        if i == 1:
            if self.candles[self.moment.candle_id - 2].conversion_line - self.candles[self.moment.candle_id - 3].conversion_line \
                    - self.candles[self.moment.candle_id - 2].base_line + self.candles[self.moment.candle_id - 3].base_line > scenario.min_slope_dif:
                return True
            else:
                return False
        if i == 2:
            return True
        if i == 3:
            return True
        if i == 4:
            if (max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price) -
                    min(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price)) / \
                    min(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price) > scenario.next_candle_lenght_min:
                return True
            else:
                return False

    def cross_happend(self):
        if self.candles[self.moment.candle_id - 2].conversion_line >= self.candles[self.moment.candle_id - 2].base_line and \
                self.candles[self.moment.candle_id - 3].conversion_line <= self.candles[self.moment.candle_id - 3].base_line:
            return True

    def strategy_works(self) -> bool:
        if self.cross_happend():
            for i in range(len(scenario.opening_intractions)):
                if scenario.opening_intractions[i] == 1:
                    if not self.check_open_con(i):
                        return False
            return True

    def start_strategy(self):
        global lock_strategies
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.buy_volume = (self.dollar_balance /
                           self.moment.price) * (scenario.volume_buy / 100)
        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        if scenario.lock_method == 'lock_to_hour':
            lock_strategies["ichi_cross"] = [
                ICHI_CROSS, self.moment.candle_id + scenario.lock_hour]
        elif scenario.lock_method == "lock_to_fin":
            lock_strategies["ichi_cross"] = [ICHI_CROSS, 0]

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
        """)
        if scenario.lock_method == "lock_to_fin":
            lock_strategies.pop("ichi_cross")

    def check_clese_con(self, i) -> bool:
        if i == 1:
            if abs(self.candles[self.moment.candle_id - 2].conversion_line - self.candles[self.moment.candle_id - 2].base_line) < \
                    scenario.ten_kij_dif_max_then_kij:
                if scenario.closing_con1_red_candle == 1:
                    if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].close_price \
                            and self.candles[self.moment.candle_id - 2].base_line > \
                        self.candles[self.moment.candle_id - 2].open_price \
                            - ((self.candles[self.moment.candle_id - 2].open_price - self.candles[self.moment.candle_id - 2].close) * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
                else:
                    if self.candles[self.moment.candle_id - 2].base_line > \
                        max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close) \
                            - ((max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close)
                                - min(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close))
                               * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
            else:
                if scenario.closing_con1_red_candle == 1:
                    if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].close_price \
                            and self.candles[self.moment.candle_id - 2].conversion_line > \
                        self.candles[self.moment.candle_id - 2].open_price \
                            - ((self.candles[self.moment.candle_id - 2].open_price - self.candles[self.moment.candle_id - 2].close) * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
                else:
                    if self.candles[self.moment.candle_id - 2].conversion_line > \
                        max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close) \
                            - ((max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close)
                                - min(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close))
                               * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
        if i == 2:
            if self.candles[self.moment.candle_id - 2].conversion_line <= self.candles[self.moment.candle_id - 2].base_line and \
                    self.candles[self.moment.candle_id - 3].conversion_line >= self.candles[self.moment.candle_id - 3].base_line:
                return True
            else:
                return False
        if i == 3:
            return self.candles[self.moment.candle_id - 2].DI_plus < self.candles[self.moment.candle_id - 2].DI_minus and \
                self.candles[self.moment.candle_id -
                             2].adx > scenario.closing_met3_min_adx
        if i == 4:
            if ((self.moment.price - self.buy_price) / self.buy_price) * 100 >= scenario.profit_limit or \
                    ((self.moment.price - self.buy_price) / self.buy_price) * 100 <= scenario.loss_limit:
                return True
            else:
                return False
        if i == 5:
            return False

    def continue_strategy(self):
        for i in range(len(scenario.close_intraction)):
            if self.check_clese_con(i):
                self.fin_and_before()


strategies = {'dummy': Dummy_Strategy}
