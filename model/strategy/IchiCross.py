# YA SATTAR
from controller import controller
from model.Moment import Moment
from model.strategy.Strategy import Strategy
from scenario import scenario


class IchiCross(Strategy):
    def __init__(self, moment: Moment, btc: float, dollar: float, candles: list, logger, name: str):
        super().__init__(moment, btc, dollar, candles, logger, name)
        self.sold = None
        self.finish_txt = None
        self.lock_seconds = None
        self.lock_method = None
        self.buy_time_date = None
        self.buy_time_hour = None
        self.buy_time_minute = None
        self.C = None
        self.CC = None
        self.lock_hour = None
        self.ICHI = None
        self.ICHHI = None
        self.ICHII = None
        self.ICHHII = None

    def get_cross_to_span_cross_distance_ids(self):
        id1 = self.moment.candle_id
        id2 = self.moment.candle_id
        while True:
            if int(self.candles[id1 - 1].span_iscross) == 1:
                break
            id1 -= 1
        while True:
            if int(self.candles[id2 - 1].span_iscross) == 1 or id2 == self.moment.candle_id + 26 or id2 == len(
                    self.candles):
                break
            id2 += 1
        return [id1, id2]

    def check_open_con(self, i: int) -> bool:
        if i == 0:
            return self.candles[self.moment.candle_id - 2].DI_plus > self.candles[
                self.moment.candle_id - 2].DI_minus and \
                   self.candles[self.moment.candle_id - 2].adx > scenario.adx_min
        if i == 1:
            return 100 * (self.candles[self.moment.candle_id - 2].conversion_line -
                          self.candles[self.moment.candle_id - 3].conversion_line) / \
                   self.candles[self.moment.candle_id - 3].conversion_line - 100 * \
                   (self.candles[self.moment.candle_id - 2].base_line -
                    self.candles[self.moment.candle_id - 3].base_line) / \
                   self.candles[self.moment.candle_id - 3].base_line > scenario.min_slope_dif
        if i == 2:
            if self.candles[self.moment.candle_id - 1].open_price > \
                    self.candles[self.moment.candle_id - 1].leading_line1 and \
                    self.candles[self.moment.candle_id - 1].open_price > \
                    self.candles[self.moment.candle_id - 1].leading_line2 and \
                    self.candles[self.moment.candle_id - 1].close_price > \
                    self.candles[self.moment.candle_id - 1].leading_line1 and \
                    self.candles[self.moment.candle_id - 1].close_price > \
                    self.candles[self.moment.candle_id - 1].leading_line2:
                return True
            if self.candles[self.moment.candle_id - 2].leading_line1 > \
                    self.candles[self.moment.candle_id - 2].leading_line2:
                return False
            if (self.candles[
                    self.moment.candle_id - 2].leading_line1 < self.candles[self.moment.candle_id - 2].conversion_line <
                self.candles[
                    self.moment.candle_id - 2].leading_line2) or \
                    (self.candles[
                         self.moment.candle_id - 2].leading_line1 < self.candles[self.moment.candle_id - 2].base_line <
                     self.candles[
                         self.moment.candle_id - 2].leading_line2):
                return False

            id1, id2 = self.get_cross_to_span_cross_distance_ids()
            distance = id2 - id1 + 1
            width = []
            for i in range(id1, id2 + 1):
                width.append(100 * abs(self.candles[i - 1].leading_line1 - self.candles[i - 1].leading_line2) / min(
                    self.candles[i - 1].leading_line1, self.candles[i - 1].leading_line2))

            return max(width) / distance >= scenario.under_cloud_condition2

        if i == 3:
            length = 100 * (max(self.candles[self.moment.candle_id - 1].open_price,
                                self.candles[self.moment.candle_id - 1].close_price) - min(
                self.candles[self.moment.candle_id - 1].open_price,
                self.candles[self.moment.candle_id - 1].close_price)) / min(
                self.candles[self.moment.candle_id - 1].open_price, self.candles[self.moment.candle_id - 1].close_price)
            if self.candles[self.moment.candle_id - 1].close_price > self.candles[self.moment.candle_id - 1].open_price:
                sgn = 1
            else:
                sgn = -1

            return sgn * length > scenario.next_candle_length_min

    def cross_happened(self):
        if self.moment.candle_id < 4:
            return False
        if self.candles[self.moment.candle_id - 2].conversion_line > self.candles[
            self.moment.candle_id - 2].base_line and \
                self.candles[self.moment.candle_id - 3].conversion_line <= \
                self.candles[self.moment.candle_id - 3].base_line:
            return True

    def strategy_works(self) -> bool:
        if self.moment.candle_id <= 77:
            return False
        if self.cross_happened():
            if scenario.opening_intractions[2] == 1:
                for i in range(len(scenario.opening_intractions)):
                    if scenario.opening_intractions[i] == 1:
                        if not self.check_open_con(i):
                            return False

            else:
                if not ((self.candles[self.moment.candle_id - 2].close_price > self.candles[
                    self.moment.candle_id - 2].leading_line1 and
                         self.candles[self.moment.candle_id - 2].close_price > self.candles[
                             self.moment.candle_id - 2].leading_line2 and
                         self.candles[self.moment.candle_id - 2].open_price > self.candles[
                             self.moment.candle_id - 2].leading_line1 and
                         self.candles[self.moment.candle_id - 2].open_price > self.candles[
                             self.moment.candle_id - 2].leading_line2)):
                    return False
                for i in range(len(scenario.opening_intractions)):
                    if scenario.opening_intractions[i] == 1:
                        if not self.check_open_con(i):
                            return False
            return True

    def start_strategy(self):
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
            controller.lock_strategies["ichi_cross"] = [
                IchiCross, self.moment.candle_id + self.lock_hour]
        elif self.lock_method == "lock_to_fin":
            controller.lock_strategies["ichi_cross"] = [IchiCross, 0]

    def fin_and_before(self):
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        controller.sell(self.buy_volume, self.sell_price)
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            controller.lock_strategies.pop("ichi_cross")

    def check_close_con(self, i) -> bool:
        if i == 1:
            if 100 * abs(self.candles[self.moment.candle_id - 2].conversion_line - self.candles[
                self.moment.candle_id - 2].base_line) / min(self.candles[self.moment.candle_id - 2].base_line,
                                                            self.candles[self.moment.candle_id - 2].conversion_line) < \
                    scenario.ten_kij_dif_max_then_kij:
                if scenario.closing_con1_red_candle == 1:
                    return self.candles[self.moment.candle_id - 2].open_price > \
                           self.candles[self.moment.candle_id - 2].close_price and \
                           self.candles[self.moment.candle_id - 2].base_line > \
                           self.candles[self.moment.candle_id - 2].open_price - \
                           ((self.candles[self.moment.candle_id - 2].open_price -
                             self.candles[self.moment.candle_id - 2].close_price) * (scenario.closing_con1_min / 100))
                else:
                    return self.candles[self.moment.candle_id - 2].base_line > \
                           max(self.candles[self.moment.candle_id - 2].open_price,
                               self.candles[self.moment.candle_id - 2].close_price) \
                           - ((max(self.candles[self.moment.candle_id - 2].open_price,
                                   self.candles[self.moment.candle_id - 2].close_price)
                               - min(self.candles[self.moment.candle_id - 2].open_price,
                                     self.candles[self.moment.candle_id - 2].close_price))
                              * (scenario.closing_con1_min / 100))
            else:
                if scenario.closing_con1_red_candle == 1:
                    return self.candles[self.moment.candle_id - 2].open_price > self.candles[
                        self.moment.candle_id - 2].close_price and self.candles[
                               self.moment.candle_id - 2].conversion_line > self.candles[
                               self.moment.candle_id - 2].open_price - (
                                   (self.candles[self.moment.candle_id - 2].open_price -
                                    self.candles[
                                        self.moment.candle_id - 2].close_price) * (
                                           scenario.closing_con1_min / 100))
                else:
                    return self.candles[self.moment.candle_id - 2].conversion_line > \
                           max(self.candles[self.moment.candle_id - 2].open_price,
                               self.candles[self.moment.candle_id - 2].close_price) \
                           - ((max(self.candles[self.moment.candle_id - 2].open_price,
                                   self.candles[self.moment.candle_id - 2].close_price)
                               - min(self.candles[self.moment.candle_id - 2].open_price,
                                     self.candles[self.moment.candle_id - 2].close_price))
                              * (scenario.closing_con1_min / 100))
        if i == 2:
            return self.candles[self.moment.candle_id - 2].conversion_line < self.candles[
                self.moment.candle_id - 2].base_line and self.candles[self.moment.candle_id - 3].conversion_line >= \
                   self.candles[self.moment.candle_id - 3].base_line
        if i == 3:
            return self.candles[self.moment.candle_id - 2].DI_plus < self.candles[
                self.moment.candle_id - 2].DI_minus and \
                   self.candles[self.moment.candle_id -
                                2].adx > scenario.closing_met3_min_adx
        if i == 4:
            return ((self.moment.price - self.buy_price) / self.buy_price) * 100 >= scenario.profit_limit or \
                   ((self.moment.price - self.buy_price) / self.buy_price) * 100 <= scenario.loss_limit

    def continue_strategy(self, working_strategies, **kwargs):
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.CC = self.candles[self.moment.candle_id - 1]
        self.ICHII = [self.candles[self.moment.candle_id - 2].conversion_line,
                      self.candles[self.moment.candle_id - 2].base_line]
        self.ICHHII = [self.candles[self.moment.candle_id - 3].conversion_line,
                       self.candles[self.moment.candle_id - 3].base_line]
        self.finish_txt = f"""
        # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        # profit(%): {round((controller.get_this_moment().price - self.buy_price) * self.buy_volume, 3)}({round(100 * (self.sell_price - self.buy_price) / self.buy_price, 3)})
        # fee : {0.001 * (self.buy_price * self.buy_volume) + 0.001 * (self.sell_price * self.buy_volume)} $
        # buy Candle : {self.C}
        # buy ICHI prev : conv : {self.ICHI}
        # buy ICHI prev prev : conv : {self.ICHHI}
        # sell Candle : {self.CC}
        # sell ICHI prev : conv : {self.ICHII}
        # sell ICHI prev prev : conv : {self.ICHHII}
        # """
        for i in range(1, len(scenario.close_intraction)):
            if scenario.close_intraction[i - 1] == 1:
                if self.check_close_con(i=i):
                    self.fin_and_before()
                    break
