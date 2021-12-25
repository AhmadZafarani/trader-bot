# YA REZA
import model.Moment
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


lock_strategies = {}


class Dummy_Strategy(Strategy):
    def strategy_works(self) -> bool:
        return self.moment.hour == 13 and self.moment.minute == 0

    def start_strategy(self):
        self.buy_volume = 1
        self.sell_volume = 1
        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_time = [self.moment.hour, self.moment.minute]
        print(self.moment.candle_id)

    def continue_strategy(self):
        if not (controller.get_this_moment().hour == 15 and controller.get_this_moment().minute == 0):
            return
        controller.sell(self.sell_volume, controller.get_this_moment().price)
        self.finish_strategy(f'''date: {self.moment.date}
        Candle : {self.C}
        buy_time : {self.buy_time[0]} : {self.buy_time[1]} 
        ''')


class ICHI_CROSS(Strategy):
    def get_cross_to_span_cross_distance_ids(self):
        id1 = self.moment.candle_id
        id2 = self.moment.candle_id
        while True:
            if int(self.candles[id1 - 1].span_iscross) == 1:
                break
            id1 -= 1
        while True:
            if int(self.candles[id2 - 1].span_iscross) == 1 or id2 == self.moment.candle_id + 26:
                break
            id2 += 1
        return [id1, id2]

    def check_open_con(self, i: int) -> bool:
        if i == 0:
            if self.candles[self.moment.candle_id - 2].DI_plus > self.candles[self.moment.candle_id - 2].DI_minus and \
                    self.candles[self.moment.candle_id - 2].adx > scenario.adx_min:
                return True
            else:
                return False
        if i == 1:
            if 100 * (self.candles[self.moment.candle_id - 2].conversion_line - self.candles[self.moment.candle_id - 3].conversion_line) / self.candles[self.moment.candle_id - 3].conversion_line \
                    - 100 * (self.candles[self.moment.candle_id - 2].base_line - self.candles[self.moment.candle_id - 3].base_line)/self.candles[self.moment.candle_id - 3].base_line > scenario.min_slope_dif:
                return True
            else:
                return False
        if i == 2:
            # TODO
            if ((self.candles[self.moment.candle_id - 1].open_price > self.candles[self.moment.candle_id - 1].leading_line1 and
                    self.candles[self.moment.candle_id - 1].open_price > self.candles[self.moment.candle_id - 1].leading_line2 and
                 self.candles[self.moment.candle_id - 1].close_price > self.candles[self.moment.candle_id - 1].leading_line1 and
                 self.candles[self.moment.candle_id - 1].close_price > self.candles[self.moment.candle_id - 1].leading_line2)):
                return True
            if self.candles[self.moment.candle_id - 2].leading_line1 > self.candles[self.moment.candle_id - 2].leading_line2:
                return False
            if (self.candles[self.moment.candle_id - 2].conversion_line > self.candles[self.moment.candle_id - 2].leading_line1 and
                    self.candles[self.moment.candle_id - 2].conversion_line < self.candles[self.moment.candle_id - 2].leading_line2) or  \
                (self.candles[self.moment.candle_id - 2].base_line > self.candles[self.moment.candle_id - 2].leading_line1 and
                 self.candles[self.moment.candle_id - 2].base_line < self.candles[self.moment.candle_id - 2].leading_line2):
                return False

            ####
            id1, id2 = self.get_cross_to_span_cross_distance_ids()
            distance = id2 - id1 + 1
            width = []
            for i in range(id1, id2+1):
                width.append(100 * abs(self.candles[i - 1].leading_line1 - self.candles[i - 1].leading_line2) / min(
                    self.candles[i - 1].leading_line1, self.candles[i - 1].leading_line2))

            maxwidth = max(width)

            if maxwidth / distance >= scenario.under_cloud_condition2:
                return True
            return False

        if i == 3:
            sgn = 0
            lenght = 100 * (max(self.candles[self.moment.candle_id - 1].open_price, self.candles[self.moment.candle_id - 1].close_price) -
                            min(self.candles[self.moment.candle_id - 1].open_price, self.candles[self.moment.candle_id - 1].close_price)) / \
                min(self.candles[self.moment.candle_id - 1].open_price,
                    self.candles[self.moment.candle_id - 1].close_price)
            if self.candles[self.moment.candle_id - 1].close_price > self.candles[self.moment.candle_id - 1].open_price:
                sgn = 1
            else:
                sgn = -1

            if sgn * lenght > scenario.next_candle_lenght_min:
                return True
            else:
                return False

    def cross_happend(self):
        if self.moment.candle_id < 4:
            return False
        if self.candles[self.moment.candle_id - 2].conversion_line > self.candles[self.moment.candle_id - 2].base_line and \
                self.candles[self.moment.candle_id - 3].conversion_line <= self.candles[self.moment.candle_id - 3].base_line:
            return True

    def strategy_works(self) -> bool:
        if self.cross_happend():
            if scenario.opening_intractions[2] == 1:
                for i in range(len(scenario.opening_intractions)):
                    if scenario.opening_intractions[i] == 1:
                        if not self.check_open_con(i):
                            return False
            else:

                if not ((self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].leading_line1 and
                         self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].leading_line2 and
                         self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].leading_line1 and
                         self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].leading_line2)):
                    return False
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
        self.C = self.candles[self.moment.candle_id-1]
        self.ADX = [self.candles[self.moment.candle_id - 2].adx, self.candles[self.moment.candle_id -
                                                                              1].DI_plus, self.candles[self.moment.candle_id - 1].DI_minus]
        self.ICHI = [self.candles[self.moment.candle_id - 2].conversion_line,
                     self.candles[self.moment.candle_id - 2].base_line]
        self.ICHHI = [self.candles[self.moment.candle_id - 3].conversion_line,
                      self.candles[self.moment.candle_id - 3].base_line]
        self.buy_price = self.moment.price
        controller.buy(self.buy_volume, self.moment.price)
        if scenario.lock_method == 'lock_to_hour':
            lock_strategies["ichi_cross"] = [
                ICHI_CROSS, self.moment.candle_id + scenario.lock_hour]
        elif scenario.lock_method == "lock_to_fin":
            lock_strategies["ichi_cross"] = [ICHI_CROSS, 0]

    def fin_and_before(self):
        # print(self.moment)
        global lock_strategies
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.CC = self.candles[self.moment.candle_id-1]
        self.ADXX = [self.candles[self.moment.candle_id - 2].adx, self.candles[self.moment.candle_id -
                                                                               1].DI_plus, self.candles[self.moment.candle_id - 1].DI_minus]
        self.ICHII = [self.candles[self.moment.candle_id - 2].conversion_line,
                      self.candles[self.moment.candle_id - 2].base_line]
        self.ICHHII = [self.candles[self.moment.candle_id - 3].conversion_line,
                       self.candles[self.moment.candle_id - 3].base_line]

        controller.sell(self.buy_volume, self.sell_price)
        self.finish_strategy(args=f"""
        # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume , 3)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 3)})
        # fee : {0.001*(self.buy_price * self.buy_volume) + 0.001 * (self.sell_price  * self.buy_volume ) } $
        # buy Candle : {self.C}
        # buy ADX prev : {self.ADX}
        # buy ICHI prev : conv : {self.ICHI}
        # buy ICHI prev prev : conv : {self.ICHHI}
        # sell Candle : {self.CC}
        # sell ADX prev : {self.ADXX}
        # sell ICHI prev : conv : {self.ICHII}
        # sell ICHI prev prev : conv : {self.ICHHII}
        # """)
        if scenario.lock_method == "lock_to_fin":
            lock_strategies.pop("ichi_cross")

    def check_clese_con(self, i) -> bool:
        if i == 1:
            if 100 * abs(self.candles[self.moment.candle_id - 2].conversion_line - self.candles[self.moment.candle_id - 2].base_line) / min(self.candles[self.moment.candle_id - 2].base_line, self.candles[self.moment.candle_id - 2].conversion_line) < \
                    scenario.ten_kij_dif_max_then_kij:
                print("less : ", self.moment.candle_id)
                if scenario.closing_con1_red_candle == 1:
                    print("red")
                    if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].close_price \
                            and self.candles[self.moment.candle_id - 2].base_line > \
                        self.candles[self.moment.candle_id - 2].open_price \
                            - ((self.candles[self.moment.candle_id - 2].open_price - self.candles[self.moment.candle_id - 2].close_price) * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        print("false here")
                        return False
                else:
                    if self.candles[self.moment.candle_id - 2].base_line > \
                        max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price) \
                            - ((max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price)
                                - min(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price))
                               * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
            else:
                if scenario.closing_con1_red_candle == 1:
                    if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].close_price \
                            and self.candles[self.moment.candle_id - 2].conversion_line > \
                        self.candles[self.moment.candle_id - 2].open_price \
                            - ((self.candles[self.moment.candle_id - 2].open_price - self.candles[self.moment.candle_id - 2].close_price) * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
                else:
                    if self.candles[self.moment.candle_id - 2].conversion_line > \
                        max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price) \
                            - ((max(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price)
                                - min(self.candles[self.moment.candle_id - 2].open_price, self.candles[self.moment.candle_id - 2].close_price))
                               * (scenario.closing_con1_min/100)):
                        return True
                    else:
                        return False
        if i == 2:
            if self.candles[self.moment.candle_id - 2].conversion_line < self.candles[self.moment.candle_id - 2].base_line and \
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
        for i in range(1, len(scenario.close_intraction) + 1):
            if scenario.close_intraction[i-1] == 1:
                if self.check_clese_con(i):
                    self.fin_and_before()
                    break


class HDR(Strategy):

    def change_SAR_phase(self) -> bool:
        if self.candles[self.moment.candle_id - 2].low_price >= self.candles[self.moment.candle_id - 2].SAR:
            for i in range(scenario.num_of_dots_openning):
                if not self.candles[self.moment.candle_id - 3 - i].high_price > self.candles[self.moment.candle_id - 3 - i].SAR:
                    return False
            return True
        return False

    def check_additional_conditions(self, con: str) -> bool:
        if con == "adx" and scenario.opening_conditions[con]["use"] == 1:
            return True
        if con == "rsi" and scenario.opening_conditions[con]["use"] == 1:
            if self.candles[self.moment.candle_id - 2].rsi <= scenario.opening_conditions["rsi"]["rsi_min"]:
                return True
            else:
                return False
        return True

    def strategy_works(self) -> bool:
        if self.change_SAR_phase():
            for con in scenario.opening_conditions:
                if not self.check_additional_conditions(con):
                    return False
            return True
        return False

    def start_strategy(self):
        global lock_strategies
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.buy_volume = (self.dollar_balance /
                           self.moment.price) * (scenario.volume_buy / 100)
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_price = self.moment.price
        controller.buy(self.buy_volume, self.moment.price)
        if scenario.lock_method == 'lock_to_hour':
            lock_strategies["hdr"] = [
                HDR, self.moment.candle_id + scenario.lock_hour]
        elif scenario.lock_method == "lock_to_fin":
            lock_strategies["hdr"] = [HDR, 0]

    def fin_and_before(self):
        # print(self.moment)
        global lock_strategies
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.CC = self.candles[self.moment.candle_id - 1]
        controller.sell(self.buy_volume, self.sell_price)
        self.finish_strategy(args=f"""
        # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume, 3)}({round(100 * (self.sell_price - self.buy_price) / self.buy_price, 3)})
        # fee : {0.001 * (self.buy_price * self.buy_volume) + 0.001 * (self.sell_price * self.buy_volume)} $
        # buy Candle : {self.C}
        # """)
        if scenario.lock_method == "lock_to_fin":
            lock_strategies.pop("hdr")

    def price_cross_bolling(self):
        if self.candles[self.moment.candle_id - 2].BUP <= self.candles[self.moment.candle_id - 2].high_price:
            return True
        else:
            return False

    def check_close_conditions(self,con :str):
        if con == "bolling" : 
            return self.price_cross_bolling()
        if con == "limit" and scenario.closing_conditions[con]["use"] == 1:
            if ((self.moment.price - self.buy_price) / self.buy_price) * 100 >= scenario.closing_conditions["limit"]["profit_limit"] or \
                    ((self.moment.price - self.buy_price) / self.buy_price) * 100 <= scenario.closing_conditions["limit"]["loss_limit"] :
                print(((self.moment.price - self.buy_price) / self.buy_price) * 100)
                return True
            else:
                return False

    def continue_strategy(self):
        for con in scenario.closing_conditions : 
            if self.check_close_conditions(con):
                self.fin_and_before()
                break 
strategies = {'hdr': HDR}

