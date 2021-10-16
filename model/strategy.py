# YA REZA
from abc import ABC, abstractmethod
import string
import random

from model.Moment import Moment
import controller.controller as controller
from scenario import scenario
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
        self.id = f'{name}_{str( "".join(random.choice(string.ascii_letters) for i in range(10)) )}'
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
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tProfit\nmore information:\t{args}\n\n'
        else:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tLoss\nmore information:\t{args}\n\n'
        return s


lock_strategies = {}
# lock_all = False


# def lock_all_strategies(working_strategies: list, moment: Moment, start_of_profit_loss_period_balance: int, dollar: int, profit_loss: int):
#     crypto1 = 0
#     for ws in working_strategies:
#         crypto1 += ws.sell_volume

#     price = ((start_of_profit_loss_period_balance *
#               (1 + profit_loss/100)) - dollar) / crypto1
#     for ws in working_strategies:
#         if not ws.sold:
#             controller.sell(ws.sell_volume, price)
#             ws.finish_strategy(ws.finish_txt)
#             if ws.lock_method == "lock_to_fin":
#                 lock_strategies.pop(ws.short_name)


class Dummy_Strategy(Strategy):
    def strategy_works(self) -> bool:
        return True

    def start_strategy(self):
        global lock_strategies
        self.buy_volume = 99000 / self.moment.price
        self.sell_volume = self.buy_volume
        controller.buy(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        self.buy_time = [self.moment.hour, self.moment.minute]
        self.short_name = 'dummy'
        self.sold = False
        self.lock_seconds = 60
        self.finish_txt = 'EMPTY'
        self.lock_method = "lock_to_fin"
        self.logger.warning(
            f'"{self.id}" - Volume:{self.buy_volume} & price={self.buy_price}')
        if self.lock_method == 'lock_to_hour':
            lock_strategies["dummy"] = [
                Dummy_Strategy, self.moment.timestamp + self.lock_seconds, self.id]

            self.logger.warning(
                f'"{self.short_name}"" locked in {self.moment.get_time_string()} for {self.lock_seconds}s')
        elif self.lock_method == "lock_to_fin":
            lock_strategies["dummy"] = [Dummy_Strategy, 0]
            self.logger.warning(
                f'"{self.short_name}" locked in {self.moment.get_time_string()} until "{self.id}" finish')

    def continue_strategy(self, working_strategies, **kwargs):
        pass
        # if not controller.get_this_moment().minute % 5 == 3:
        #     return
        # self.sold = True
        # self.finish_strategy(self.finish_txt)
        # if self.lock_method == "lock_to_fin":
        #     lock_strategies.pop("ichi_cross")

        # controller.sell(self.sell_volume, controller.get_this_moment().price)
        # self.finish_strategy(f'''date: {self.moment.date}
        # buy_time : {self.buy_time[0]} : {self.buy_time[1]}
        # ''')


class ICHI_CROSS(Strategy):
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
        # global log6
        if self.moment.candle_id <= 77:
            return False
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
            # log6.info(self.candles[self.moment.candle_id-1])
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
        self.C = self.candles[self.moment.candle_id-1]
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
        global lock_all
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
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume , 3)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 3)})
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
                if self.check_close_con(i=i, working_strategies=working_strategies,
                                        start_of_profit_loss_period_balance=kwargs[
                                            'start_of_profit_loss_period_balance'],
                                        dollar_balance=kwargs["dollar_balance"]):
                    self.fin_and_before()
                    break


class Moving_average(Strategy):
    def check_open_con(self, key: str, value: dict):
        if key == 'price_to_line':
            cndl = [self.candles[self.moment.candle_id - 1],
                    self.candles[self.moment.candle_id - 2]]
            moving_average = getattr(
                self.candles[self.moment.candle_id - 2], "ma" + str(value["options"]["line"]))
            if moving_average == 0:
                return False
            if value["options"]["green"]:
                if cndl[-1].close_price > cndl[-1].open_price:
                    if 100 * (cndl[-1].close_price - moving_average) / (cndl[-1].close_price - cndl[-1].open_price) >= value["options"]["min_percentage"]:
                        if cndl[0].open_price > moving_average:
                            return True
                return False
            else:
                maximum = max(cndl[-1].open_price, cndl[-1].close_price)
                minimum = min(cndl[-1].open_price, cndl[-1].close_price)
                if 100 * (maximum - moving_average) / (maximum - minimum) > value["options"]["min_percentage"]:
                    if cndl[0].open_price > moving_average:
                        return True
                return False
        if key == 'line_to_line':
            moving1 = [
                getattr(self.candles[self.moment.candle_id-2],
                        "ma"+str(value["options"]["line"][0])),
                getattr(self.candles[self.moment.candle_id-3],
                        "ma"+str(value["options"]["line"][0]))
            ]
            moving2 = [
                getattr(self.candles[self.moment.candle_id-2],
                        "ma"+str(value["options"]["line"][1])),
                getattr(self.candles[self.moment.candle_id-3],
                        "ma"+str(value["options"]["line"][1]))
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
                    print("buy")
                    return True

    def strategy_works(self):
        for key, value in scenario.buy_method.items():
            if value['enable'] == 1:
                if self.check_open_con(key=key, value=value):
                    return True

    def start_strategy(self):
        global lock_strategies
        self.short_name = 'moving_average'
        self.sold = False
        self.finish_txt = 'EMPTY'
        self.lock_seconds = scenario.moving_average_lock_seconds
        self.lock_method = scenario.moving_average_lock_method
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.buy_volume = (self.dollar_balance /
                           self.moment.price) * (scenario.volume_buy_ma / 100)
        self.sell_volume = self.buy_volume
        self.C = self.candles[self.moment.candle_id-1]
        self.buy_price = self.moment.price
        self.logger.warning(
            f" \"{self.id}\" - Details : volume = {self.buy_volume} , price = {self.buy_price}")
        controller.buy(self.buy_volume, self.moment.price)

        self.logger.warning(
            f'"{self.id}" - Volume:{self.buy_volume} & price={self.buy_price}')
        if self.lock_method == 'lock_to_hour':
            lock_strategies["dummy"] = [
                Dummy_Strategy, self.moment.timestamp + self.lock_seconds, self.id]

            self.logger.warning(
                f'"{self.short_name}"" locked in {self.moment.get_time_string()} for {self.lock_seconds}s')
        elif self.lock_method == "lock_to_fin":
            lock_strategies["dummy"] = [Dummy_Strategy, 0]
            self.logger.warning(
                f'"{self.short_name}" locked in {self.moment.get_time_string()} until "{self.id}" finish')

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
        global lock_all

        if key == "price_to_line":
            cndl = [self.candles[self.moment.candle_id-1],
                    self.candles[self.moment.candle_id-2]]
            moving_average = getattr(
                self.candles[self.moment.candle_id-2], "ma"+str(value["options"]["line"]))
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
                # profit(%): {round((self.sell_price - self.buy_price) * self.buy_volume , 3)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 3)})
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
                # profit(%): {round((self.sell_price - self.buy_price) * self.buy_volume , 3)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 3)})
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
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume , 3)}({round(100 * (self.sell_price - self.buy_price)/self.buy_price , 3)})
        # fee : {scenario.fee*(self.buy_price * self.buy_volume) + scenario.fee * (self.sell_price  * self.buy_volume ) } $
        # buy Candle : {self.C}
        # sell Candle : {self.CC}
        # """
        for key, value in scenario.sell_method.items():
            if value['enable']:
                if self.check_close_con(key=key, value=value, working_strategies=working_strategies,  start_of_profit_loss_period_balance=kwargs["start_of_profit_loss_period_balance"], dollar_balance=kwargs['dollar_balance']):
                    self.fin_and_before()
                    break


strategies = {'dummy': Dummy_Strategy}
# strategies = {'moving_average': Moving_average}
