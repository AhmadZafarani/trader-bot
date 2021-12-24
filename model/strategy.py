# YA REZA
from abc import ABC, abstractmethod
from logging import setLoggerClass

from model.Moment import Moment
import controller.controller as controller
from model.Position import Position
from scenario import scenario
from controller.logs import setup_logger, get_logger
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
    def __init__(self, moment: Moment, btc: float, dollar: float, candles: list, feature_balance: float):
        self.moment = moment
        self.candles = candles
        self.working = False
        self.buy_price = 0
        self.sell_price = 0
        self.buy_volume = 0
        self.sell_volume = 0
        self.dollar_balance = dollar
        self.future_balance = feature_balance
        self.sold_volume = 0
        self.sell_time_date = "0/0/0"
        self.sell_time_hour = 0
        self.sell_time_minute = 0
        self.btc_balance = btc
        self.direction = ""
        self.leverage = 0

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
    def continue_strategy(self, working_strategies, **kwargs):
        pass

    def finish_strategy(self, args=''):
        controller.set_report(Strategy.report(self.buy_price, controller.get_this_moment().price,
                                              self.__class__.__name__, self.buy_volume, self.leverage, self.direction, args))
        self.working = False

    @staticmethod
    def report(buy_price: int, sell_price: int, strategy_name: str, bought_volume: int, leverage: int, direction: str, args: dict) -> dict:
        if scenario.mode == 'spot':
            out = {
                "mode": "spot", "Strategy": strategy_name, "buy_price": buy_price, "sell_price": sell_price, "volume": bought_volume, "result": "", "profit": 10000, "percentage": 10, "more": args
            }
            if sell_price > buy_price:
                out["result"] = "WIN"
                out["profit"] = bought_volume * (buy_price - sell_price)
                out["percentage"] = round(
                    100 * (buy_price - sell_price) / sell_price, 2)
            else:
                out["result"] = "LOST"
                out["profit"] = bought_volume * (sell_price - buy_price)
                out["percentage"] = round(
                    100 * (buy_price - sell_price) / sell_price, 2)
        elif scenario.mode == 'future':
            out = {
                "mode": "future", "Strategy": strategy_name, "direction": direction, "entry_price": buy_price, "closing price": sell_price, "volume": bought_volume, "leverage": leverage, "result": "", "more": args
            }
            if sell_price > buy_price:
                if direction == 'short':
                    out['result'] = "LOST"
                elif direction == 'long':
                    out["result"] = 'WIN'
            else:
                if direction == 'short':
                    out['result'] = "WIN"
                elif direction == 'long':
                    out["result"] = 'LOST'
        return out


lock_strategies = {}


class Dummy_Strategy(Strategy):

    def strategy_works(self) -> bool:
        return True

    def start_strategy(self):
        self.short_name = 'dummy'
        self.sold = False
        self.lock_hour = 0
        self.lock_method = "lock_to_fin"
        self.buy_id = self.moment.candle_id
        self.buy_volume = 0.995 * self.dollar_balance/self.moment.price
        self.sell_volume = self.buy_volume

        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_time = [self.moment.hour, self.moment.minute]
        self.buy_date = self.moment.date
        if self.lock_method == 'lock_to_hour':
            lock_strategies["dummy"] = [
                Dummy_Strategy, self.moment.candle_id + self.lock_hour, "normal"]
        elif self.lock_method == "lock_to_fin":
            lock_strategies["dummy"] = [Dummy_Strategy, 0]

    def continue_strategy(self, working_strategies: list):
        # global lock_all, lock_strategies
        global lock_strategies
        self.finish_txt = f'''date: {self.moment.date}
        Candle : {self.C}
        buy_time : {self.buy_date} {self.buy_time[0]}:{self.buy_time[1]} 
        sell_time : {self.moment.date} {self.moment.hour}:{self.moment.minute} 
        '''
        if self.moment.profit_loss_percentage <= -1:
            lock_all = True
            # lock_all_strategies(
            # working_strategies=working_strategies, moment=self.moment)
            return
        if not(self.moment.hour == 19 and self.moment.minute == 44):
            return
        controller.sell(self.sell_volume, controller.get_this_moment().price)
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            lock_strategies.pop("dummy")


class ICHI_CROSS(Strategy):
    setup_logger('log6', r'logs/ichi.log')
    logger = get_logger('log6')

    def get_cross_to_span_cross_distance_ids(self):
        id1 = self.moment.candle_id
        id2 = self.moment.candle_id
        while True:
            if int(self.candles[id1 - 1].span_iscross) == 1:
                break
            id1 -= 1
        while True:
            if int(self.candles[id2 - 1].span_iscross) == 1 or id2 == self.moment.candle_id + 26 or id2 == len(self.candles):
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
            length = 100 * (max(self.candles[self.moment.candle_id - 1].open_price, self.candles[self.moment.candle_id - 1].close_price) -
                            min(self.candles[self.moment.candle_id - 1].open_price, self.candles[self.moment.candle_id - 1].close_price)) / \
                min(self.candles[self.moment.candle_id - 1].open_price,
                    self.candles[self.moment.candle_id - 1].close_price)
            if self.candles[self.moment.candle_id - 1].close_price > self.candles[self.moment.candle_id - 1].open_price:
                sgn = 1
            else:
                sgn = -1

            if sgn * length > scenario.next_candle_length_min:
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
        if self.moment.candle_id <= 27:
            return False
        if self.cross_happend():
            if scenario.opening_intractions[2] == 1:
                for i in range(len(scenario.opening_intractions)):
                    if scenario.opening_intractions[i] == 1:
                        if not self.check_open_con(i):
                            return False
            else:

                if not (self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].leading_line1 and
                        self.candles[self.moment.candle_id - 2].close_price > self.candles[self.moment.candle_id - 2].leading_line2 and
                        self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].leading_line1 and
                        self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].leading_line2):
                    return False
                for i in range(len(scenario.opening_intractions)):
                    if scenario.opening_intractions[i] == 1:
                        if not self.check_open_con(i):
                            return False
            self.logger.info(self.candles[self.moment.candle_id - 1])
            return True

    def start_strategy(self):
        global lock_strategies
        self.short_name = 'ichi_cross'
        self.sold = False
        self.lock_hour = 0
        self.finish_txt = 'EMPTY'
        self.lock_method = "lock_to_fin"
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.buy_volume = (self.dollar_balance /
                           self.moment.price) * (scenario.volume_buy_ichi / 100)
        self.sell_volume = self.buy_volume
        self.C = self.candles[self.moment.candle_id - 1]
        self.ICHI = [self.candles[self.moment.candle_id - 2].conversion_line,
                     self.candles[self.moment.candle_id - 2].base_line]
        self.ICHHI = [self.candles[self.moment.candle_id - 3].conversion_line,
                      self.candles[self.moment.candle_id - 3].base_line]
        self.buy_price = self.moment.price
        controller.buy(self.buy_volume, self.moment.price)
        if self.lock_method == 'lock_to_hour':
            lock_strategies["ichi_cross"] = [
                ICHI_CROSS, self.moment.candle_id + self.lock_hour]
        elif self.lock_method == "lock_to_fin":
            lock_strategies["ichi_cross"] = [ICHI_CROSS, 0]

    def fin_and_before(self):
        global lock_strategies
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute

        controller.sell(self.buy_volume, self.sell_price)
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            lock_strategies.pop("ichi_cross")

    def check_close_con(self, i, working_strategies, start_of_profit_loss_period_balance: int, dollar_balance: int) -> bool:
        if i == 1:
            if 100 * abs(self.candles[self.moment.candle_id - 2].conversion_line - self.candles[self.moment.candle_id - 2].base_line) / min(self.candles[self.moment.candle_id - 2].base_line, self.candles[self.moment.candle_id - 2].conversion_line) < \
                    scenario.ten_kij_dif_max_then_kij:
                if scenario.closing_con1_red_candle == 1:
                    if self.candles[self.moment.candle_id - 2].open_price > self.candles[self.moment.candle_id - 2].close_price \
                            and self.candles[self.moment.candle_id - 2].base_line > \
                        self.candles[self.moment.candle_id - 2].open_price \
                            - ((self.candles[self.moment.candle_id - 2].open_price - self.candles[self.moment.candle_id - 2].close_price) * (scenario.closing_con1_min/100)):
                        return True
                    else:
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
        # if i == 5:
        #     if self.moment.profit_loss_percentage >= scenario.profit_limit_per:
        #         lock_all = True
        #         lock_all_strategies(
        #             working_strategies=working_strategies, moment=self.moment, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar=dollar_balance, profit_loss=scenario.profit_limit_per)
        #         return True
        #     if self.moment.profit_loss_percentage <= scenario.loss_limit_per:
        #         lock_all = True
        #         lock_all_strategies(
        #             working_strategies=working_strategies, moment=self.moment, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar=dollar_balance, profit_loss=scenario.loss_limit_per)
        #         return True
        #     return False

    def continue_strategy(self, working_strategies, **kwargs):
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.CC = self.candles[self.moment.candle_id-1]
        self.ICHII = [self.candles[self.moment.candle_id - 2].conversion_line,
                      self.candles[self.moment.candle_id - 2].base_line]
        self.ICHHII = [self.candles[self.moment.candle_id - 3].conversion_line,
                       self.candles[self.moment.candle_id - 3].base_line]
        self.finish_txt = f"""
        # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume , 5)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 5)})
        # fee : {0.001*(self.buy_price * self.buy_volume) + 0.001 * (self.sell_price  * self.buy_volume ) } $
        # buy Candle : {self.C}
        # buy ICHI prev : conv : {self.ICHI}
        # buy ICHI prev prev : conv : {self.ICHHI}
        # sell Candle : {self.CC}
        # sell ICHI prev : conv : {self.ICHII}
        # sell ICHI prev prev : conv : {self.ICHHII}
        # """
        # if scenario.close_intraction[4] == 1:
        #     if self.check_close_con(i=5, working_strategies=working_strategies, start_of_profit_loss_period_balance=kwargs['start_of_profit_loss_period_balance'], dollar_balance=kwargs["dollar_balance"]):
        #         return
        for i in range(1, len(scenario.close_intraction)):
            if scenario.close_intraction[i-1] == 1:
                if self.check_close_con(i=i, working_strategies=working_strategies, start_of_profit_loss_period_balance=kwargs['start_of_profit_loss_period_balance'], dollar_balance=kwargs["dollar_balance"]):
                    self.fin_and_before()
                    break


class Moving_average(Strategy):
    setup_logger('log5', r'logs/moving_average.log')
    logger = get_logger('log5')

    def check_open_con(self, key: str, value: dict):
        if key == 'price_to_line':
            cndl = [self.candles[self.moment.candle_id-1],
                    self.candles[self.moment.candle_id-2]]
            moving_average = getattr(
                self.candles[self.moment.candle_id-2], "ma"+str(value["options"]["line"]))

            if moving_average == 0:
                return False

            if value["options"]["green"]:
                if cndl[-1].close_price > cndl[-1].open_price:
                    if 100*(cndl[-1].close_price - moving_average) / (cndl[-1].close_price - cndl[-1].open_price) >= value["options"]["min_percentage"]:
                        if cndl[0].open_price > moving_average:
                            return True
                return False

            else:
                maximum = max(cndl[-1].open_price, cndl[-1].close_price)
                minimum = min(cndl[-1].open_price, cndl[-1].close_price)
                if 100*(maximum - moving_average) / (maximum - minimum) > value["options"]["min_percentage"]:
                    if cndl[0].open_price > moving_average:
                        return True
                return False

        if key == 'line_to_line':
            moving1 = [
                getattr(self.candles[self.moment.candle_id - 2],
                        "ma" + str(value["options"]["line"][0])),
                getattr(self.candles[self.moment.candle_id - 3],
                        "ma" + str(value["options"]["line"][0]))
            ]
            moving2 = [
                getattr(self.candles[self.moment.candle_id - 2],
                        "ma" + str(value["options"]["line"][1])),
                getattr(self.candles[self.moment.candle_id - 3],
                        "ma" + str(value["options"]["line"][1]))
            ]

            if 0 in moving1:
                return False
            if 0 in moving2:
                return False
            if value["options"]['cross']:
                if moving1[0] > moving2[0] and moving1[1] <= moving2[1]:
                    return True
            else:
                if moving1[0] > moving2[0]:
                    return True

    def strategy_works(self):
        if self.moment.candle_id <= 26:
            return False

        for key, value in scenario.buy_method.items():
            if value['enable'] == 1:
                if self.check_open_con(key=key, value=value):
                    self.logger.info(self.candles[self.moment.candle_id-1])
                    return True

    def start_strategy(self):
        global lock_strategies
        self.short_name = 'moving_average'
        self.sold = False
        self.finish_txt = 'EMPTY'
        self.lock_hour = 0
        self.lock_method = "lock_to_fin"
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.buy_volume = (self.dollar_balance /
                           self.moment.price) * (scenario.volume_buy_ma / 100)
        self.sell_volume = self.buy_volume
        self.C = self.candles[self.moment.candle_id-1]
        self.buy_price = self.moment.price

        controller.buy(self.buy_volume, self.moment.price)
        if self.lock_method == 'lock_to_hour':
            lock_strategies[self.short_name] = [
                Moving_average, self.moment.candle_id + self.lock_hour]
        elif self.lock_method == "lock_to_fin":
            lock_strategies[self.short_name] = [Moving_average, 0]

    def fin_and_before(self):
        global lock_strategies
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute

        controller.sell(self.buy_volume, self.sell_price)
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            lock_strategies.pop(self.short_name)

    def check_close_con(self, key: str, value: dict, working_strategies: list, start_of_profit_loss_period_balance: int, dollar_balance: int):
        if key == "price_to_line":
            cndl = [self.candles[self.moment.candle_id - 1],
                    self.candles[self.moment.candle_id - 2]]
            moving_average = getattr(
                self.candles[self.moment.candle_id - 2], "ma" + str(value["options"]["line"]))
            if value["options"]["red"]:
                if cndl[-1].close_price < cndl[-1].open_price:
                    if 100*(moving_average - cndl[-1].close_price) / (cndl[-1].open_price - cndl[-1].close_price) >= value["options"]["min_percentage"]:
                        if cndl[0].open_price < moving_average:
                            return True
                return False
            else:
                maximum = max(cndl[-1].open_price, cndl[-1].close_price)
                minimum = min(cndl[-1].open_price, cndl[-1].close_price)
                if 100*(moving_average - minimum)/(maximum - minimum) > value["options"]["min_percentage"]:
                    if cndl[0].open_price < moving_average:
                        return True
                return False

        if key == "line_to_line":
            moving1 = [
                getattr(self.candles[self.moment.candle_id - 2],
                        "ma" + str(value["options"]["line"][0])),
                getattr(self.candles[self.moment.candle_id - 3],
                        "ma" + str(value["options"]["line"][0]))
            ]
            moving2 = [
                getattr(self.candles[self.moment.candle_id - 2],
                        "ma" + str(value["options"]["line"][1])),
                getattr(self.candles[self.moment.candle_id - 3],
                        "ma" + str(value["options"]["line"][1]))
            ]
            if moving1[0] < moving2[0] and moving1[1] >= moving2[1]:
                return True

        if key == "profit_loss_limit":
            profit_limit = self.buy_price * \
                (1 + value["options"]["profit_limit"] / 100)
            loss_limit = self.buy_price * \
                (1 + value["options"]["loss_limit"] / 100)
            if self.moment.price >= profit_limit:
                self.sell_price = profit_limit
                self.finish_txt = f"""
                # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
                # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
                # profit(%): {round((self.sell_price - self.buy_price) * self.buy_volume , 5)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 5)})
                # fee : {scenario.fee*(self.buy_price * self.buy_volume) + scenario.fee * (self.sell_price  * self.buy_volume ) } $
                # buy Candle : {self.C}
                # sell Candle : {self.CC}
                # """
                return True
            elif self.moment.price <= loss_limit:
                self.sell_price = loss_limit
                self.finish_txt = f"""
                # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
                # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
                # profit(%): {round((self.sell_price - self.buy_price) * self.buy_volume , 5)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 5)})
                # fee : {scenario.fee*(self.buy_price * self.buy_volume) + scenario.fee * (self.sell_price  * self.buy_volume ) } $
                # buy Candle : {self.C}
                # sell Candle : {self.CC}
                # """
                return True
            return False
        # if key == "periodical_profit_loss_limit":
        #     if self.moment.profit_loss_percentage >= value['options']['profit_limit']:
        #         lock_all = True
        #         lock_all_strategies(
        #             working_strategies=working_strategies, moment=self.moment, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar=dollar_balance, profit_loss=value['options']['profit_limit'])
        #     elif self.moment.profit_loss_percentage <= value['options']['loss_limit']:
        #         lock_all = True
        #         lock_all_strategies(
        #             working_strategies=working_strategies, moment=self.moment, start_of_profit_loss_period_balance=start_of_profit_loss_period_balance, dollar=dollar_balance, profit_loss=value['options']['loss_limit'])

    def continue_strategy(self, working_strategies, **kwargs):
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.CC = self.candles[self.moment.candle_id-1]
        self.finish_txt = f"""
        # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume , 5)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 5)})
        # fee : {scenario.fee*(self.buy_price * self.buy_volume) + scenario.fee * (self.sell_price  * self.buy_volume ) } $
        # buy Candle : {self.C}
        # sell Candle : {self.CC}
        # """

        for key, value in scenario.sell_method.items():
            if value['enable']:
                if self.check_close_con(key=key, value=value, working_strategies=working_strategies,  start_of_profit_loss_period_balance=kwargs["start_of_profit_loss_period_balance"], dollar_balance=kwargs['dollar_balance']):
                    self.fin_and_before()
                    break


class Dummy_Strategy_Futures(Strategy):
    def strategy_works(self) -> bool:
        if self.moment.hour == 13 and self.moment.minute == 0:
            return True
        return False

    def start_strategy(self):
        self.sold = False
        self.short_name = 'dummy_future'
        self.lock_hour = 10
        self.lock_method = "lock_to_fin"
        self.buy_id = self.moment.candle_id
        self.finish_txt = {}
        self.buy_volume = 0.5 * self.future_balance / self.moment.price
        self.sell_volume = self.buy_volume
        self.entry_liquidity = self.moment.future_liquidity
        self.entry_price = self.moment.price
        controller.short_position(self.buy_volume, self.moment.price)

        self.buy_price = self.moment.price
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_time = [self.moment.hour, self.moment.minute]
        self.buy_date = self.moment.date

        if self.lock_method == 'lock_to_hour':
            lock_strategies["dummy_future"] = [
                Dummy_Strategy_Futures, self.moment.candle_id + self.lock_hour, "normal"]
        elif self.lock_method == "lock_to_fin":
            lock_strategies["dummy_future"] = [Dummy_Strategy_Futures, 0]

    def continue_strategy(self, working_strategies, **kwargs):
        return
        # if not (self.moment.hour == 16 and self.moment.minute == 0):
        #     return
        # self.finish_txt = {}
        # controller.short_position(
        #     self.sell_volume, controller.get_this_moment().price)
        # print(controller.position)
        # print(controller.future_balance)
        # exit
        # self.sold = True
        # self.finish_strategy(self.finish_txt)
        # if self.lock_method == "lock_to_fin":
        #     lock_strategies.pop("dummy_futures")


last_trade_cloud_color = -3


class Ichi_future(Strategy):
    def check_short_con(self, key, value) -> bool:

        try:
            candle_26 = self.candles[self.moment.candle_id + 24]
        except:
            # print('26_false')
            return False
        if (self.moment.candle_id < 26):
            print('m26 false')
            return False
        candle_m26 = self.candles[self.moment.candle_id - 28]
        candle_m1 = self.candles[self.moment.candle_id - 2]

        if key == 'red_cloud':
            if candle_26.leading_line1 < candle_26.leading_line2:
                return True
        if key == 'ten_under_kij':
            if candle_m1.conversion_line < candle_m1.base_line:
                return True
        if key == 'close_under_cloud':
            if candle_m1.close_price < min(candle_m1.leading_line1, candle_m1.leading_line2):
                return True
        if key == 'span_under_cloud':
            if candle_m26.lagging_span < min(candle_m26.leading_line1, candle_m26.leading_line2):
                return True
        return False

    def check_long_con(self, key, value) -> bool:
        try:
            candle_26 = self.candles[self.moment.candle_id + 24]
        except:
            # print('26_false')
            return False
        if (self.moment.candle_id < 26):
            print('m26 false')
            return False
        candle_m26 = self.candles[self.moment.candle_id - 28]
        candle_m1 = self.candles[self.moment.candle_id - 2]

        if key == 'green_cloud':
            if candle_26.leading_line1 > candle_26.leading_line2:
                return True
        if key == 'kij_inder_ten':
            if candle_m1.conversion_line > candle_m1.base_line:
                return True
        if key == 'close_upper_cloud':
            if candle_m1.close_price > max(candle_m1.leading_line1, candle_m1.leading_line2):
                return True
        if key == 'span_upper_cloud':
            if candle_m26.lagging_span > max(candle_m26.leading_line1, candle_m26.leading_line2):
                return True
        return False

    def strategy_works(self) -> bool:
        flag_short = 1
        flag_long = 1
        if self.moment.candle_id < 77 + 26:
            return False

        # only 1 trade in a clou
        if scenario.ichi_future['enterance']['options']['only_one_in_a_cloud']:
            try:
                if self.candles[self.moment.candle_id+24].cloud_number == last_trade_cloud_color:
                    return False
            except Exception as ex:
                # print(ex)
                pass

        # chech short conditions
        short_conditions = scenario.ichi_future["enterance"]["short"]
        for key, value in short_conditions.items():
            if value["enable"]:
                if not self.check_short_con(key, value):
                    flag_short = 0
        long_conditions = scenario.ichi_future["enterance"]["long"]
        for key, value in long_conditions.items():
            if value["enable"]:
                if not self.check_long_con(key, value):
                    flag_long = 0
        if flag_short:
            self.direction = "short"
            # print(
            #     f'short happaend in {self.moment}\n{self.candles[self.moment.candle_id-1]}')
            return True
        if flag_long:
            # print(
            # f'long happaend in {self.moment}\n{self.candles[self.moment.candle_id-1]}')
            self.direction = "long"
            return True
        return False

    def calculate_stoploss(self, close_conditioins):
        for key, value in close_conditioins.items():
            if value['enable']:
                if key == 'based_on_cloud':
                    if self.direction == 'short':
                        sl = max(self.candles[self.moment.candle_id - 2].leading_line1,
                                 self.candles[self.moment.candle_id - 2].leading_line2)
                        tp = self.moment.price - \
                            value['options']['r2r'] * (sl - self.moment.price)
                        break
                    elif self.direction == 'long':
                        sl = min(self.candles[self.moment.candle_id - 2].leading_line1,
                                 self.candles[self.moment.candle_id - 2].leading_line2)
                        tp = self.moment.price + \
                            value['options']['r2r'] * (self.moment.price - sl)
                        break
                if key == 'based_on_atr':
                    if self.direction == 'short':
                        sl = self.moment.price + \
                            value['options']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
                        tp = self.moment.price - \
                            value['options']['r2r']*value['options']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
                    if self.direction == 'long':

                        sl = self.moment.price - \
                            value['options']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
                        tp = self.moment.price + \
                            value['options']['r2r']*value['options']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
        return sl, tp

    def manage_found(self, found_management):  # will return size & levrage
        loss_limit = 100 * abs(self.stop_loss -
                               self.entry_price) / self.entry_price
        total_risk = found_management['total_risk']
        # print(f'loss_limit = {loss_limit}')
        total_found = 0.8 * self.future_balance

        r = (total_risk / loss_limit)
        self.ratio = r
        # print(f'r = {r}')
        if r <= 1:
            found = total_found * r
            leverage = 1
        else:  # r > 1
            found = total_found
            leverage = r
        size = found / self.moment.price
        return size, leverage

    def start_strategy(self):
        global last_trade_cloud_color
        global lock_strategies
        self.close_via_span = 0
        self.close_via_cross = 0
        self.short_name = 'ichi_future'
        self.finish_txt = {}
        self.lock_hour = 0
        self.lock_method = "lock_to_fin"
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.C = self.candles[self.moment.candle_id-1]
        self.entry_price = self.moment.price
        self.buy_price = self.entry_price
        self.entry_liquidity = self.moment.future_liquidity
        self.sold = False
        self.finish_txt = "sold_buy_lock_strategy"

        last_trade_cloud_color = self.candles[self.moment.candle_id + 24].cloud_number
        # stoploss_calculation
        close_conditions = scenario.ichi_future['close_conditions']
        self.stop_loss, self.take_profit = self.calculate_stoploss(
            close_conditions)
        # print(f'sl : {self.stop_loss} , tp : {self.take_profit}')

        # managing_found :
        found_management = scenario.ichi_future['found_management']
        self.size, self.leverage = self.manage_found(found_management)
        # print(f'size : {self.size} , leverage = {self.leverage}')
        self.buy_volume = self.size
        # change leverage if needed
        if self.leverage != 1:
            controller.position.multiply_leverage(self.leverage)
            # print('leverage changed')
        # Open Positions
        if self.direction == 'long':
            controller.long_position(self.size, self.entry_price)
            # print(f'Long opende : {controller.position}')
        elif self.direction == 'short':
            controller.short_position(self.size, self.entry_price)
            # print(f'short opende : {controller.position}')

        if self.lock_method == 'lock_to_hour':
            lock_strategies[self.short_name] = [
                Ichi_future, self.moment.candle_id + self.lock_hour]
        elif self.lock_method == "lock_to_fin":
            lock_strategies[self.short_name] = [Ichi_future, 0]
            # print(f'{self.short_name} locked in {self.moment}')

    def strategy_pre_finish(self):
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.sell_price = self.closing_price
        if self.direction == 'short':
            controller.long_position(self.size, self.closing_price)
            if self.entry_price > self.closing_price:
                self.status = "WIN"
            else:
                self.status = "LOST"
        elif self.direction == 'long':
            # print(controller.position)
            # print(controller.future_balance)
            # print(self.moment.future_liquidity)
            controller.short_position(self.size, self.closing_price)
            # print(controller.position)
            # print(self.moment.future_liquidity)

            # print(controller.future_balance)
            # exit(0)
            if self.entry_price < self.closing_price:
                self.status = "WIN"
            else:
                self.status = "LOST"

        self.closing_liquidity = self.moment.future_liquidity
        controller.position.multiply_leverage(1 / self.leverage)
        self.finish_txt = {
            "Date": {
                "Entrance": f'{self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}',
                "Closeing": f'{self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}'
            },
            "Risk_Managment": {
                "stop_loss": self.stop_loss,
                "take_profit": self.take_profit
            },
            "Found_Managment": {
                "entry_liquidity": self.entry_liquidity,
                "closing_liquidity": self.closing_liquidity,
                "ratio": self.ratio,
                "profit/loss": 100*(self.closing_liquidity - self.entry_liquidity) / self.entry_liquidity
            },
            "close_via_span": self.close_via_span,
            "close_via_cross" : self.close_via_cross

        }
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            lock_strategies.pop("ichi_future")
            # print(f'strategy {self.short_name} unlocked in {self.moment}')

    def check_span_close_conditions(self):
        # 26 previus candle
        m26_candle = self.candles[self.moment.candle_id - 28]
        # 27 previus candle
        m27_candle = self.candles[self.moment.candle_id - 29]
        if self.direction == 'short':
            if (m27_candle.lagging_span >= min(m27_candle.open_price, m27_candle.close_price) and m27_candle.lagging_span <= max(m27_candle.close_price, m27_candle.open_price)) and \
                 (m26_candle.lagging_span > max(m26_candle.open_price, m26_candle.close_price)):
                return True
        if self.direction == 'long':
            if (m27_candle.lagging_span >= min(m27_candle.open_price, m27_candle.close_price) and m27_candle.lagging_span <= max(m27_candle.close_price, m27_candle.open_price)) and \
                 (m26_candle.lagging_span < min(m26_candle.open_price, m26_candle.close_price)):
                return True

    def check_cross_close_conditions(self):
        if self.direction == 'short':
            if self.candles[self.moment.candle_id - 2].conversion_line > self.candles[self.moment.candle_id - 2].base_line:
                return True
        elif self.direction == 'long':
            if self.candles[self.moment.candle_id - 2].conversion_line < self.candles[self.moment.candle_id - 2].base_line:
                return True

    def continue_strategy(self, working_strategies, **kwargs):
        if self.direction == 'short':
            if self.moment.price >= self.stop_loss:
                self.closing_price = self.stop_loss
                self.strategy_pre_finish()
            elif self.moment.price <= self.take_profit:
                self.closing_price = self.take_profit
                self.strategy_pre_finish()
            elif scenario.ichi_future["close_conditions"]["span_close_signal"]["enable"] and self.check_span_close_conditions():
                self.closing_price = self.moment.price
                self.close_via_span = 1
                self.strategy_pre_finish()
            elif scenario.ichi_future["close_conditions"]["cross_close_signal"]["enable"] and self.check_cross_close_conditions():
                self.closing_price = self.moment.price
                self.close_via_cross = 1
                self.strategy_pre_finish()
        elif self.direction == 'long':
            if self.moment.price <= self.stop_loss:
                self.closing_price = self.stop_loss
                self.strategy_pre_finish()
            elif self.moment.price >= self.take_profit:
                self.closing_price = self.take_profit
                self.strategy_pre_finish()
            elif scenario.ichi_future["close_conditions"]["span_close_signal"]["enable"] and self.check_span_close_conditions():
                self.closing_price = self.moment.price
                self.close_via_span = 1
                self.strategy_pre_finish()
            elif scenario.ichi_future["close_conditions"]["cross_close_signal"]["enable"] and self.check_cross_close_conditions():
                self.closing_price = self.moment.price
                self.close_via_cross = 1
                self.strategy_pre_finish()

        return


# strategies = {'ichi_future': Ichi_future}
# strategies = {"dummy_future" : Dummy_Strategy_Futures}
# strategies = {'ichi_cross': ICHI_CROSS}
# strategies = {'moving_average':Moving_average}
if scenario.strtgg == 'ma':
    strategies = {'moving_average' : Moving_average }
elif scenario.strtgg == 'ichi':
    strategies = {'ichi_cross' : ICHI_CROSS }
elif scenario.strtgg == 'ichi_future':
    strategies = {'ichi_future' : Ichi_future }
