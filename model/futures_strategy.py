# YA ALI
from model.strategy import Strategy, lock_strategies , strategies
from controller.futures_controller import short_position, long_position
import controller.controller as controller
from scenario import scenario


class Dummy_Strategy_Futures(Strategy):
    def strategy_works(self) -> bool:
        if self.moment.hour == 13 and self.moment.minute == 0:
            return True
        return False

    def start_strategy(self):
        self.short_name = 'dummy_futures'
        self.lock_hour = 10
        self.lock_method = "lock_to_fin"
        self.buy_id = self.moment.candle_id
        self.buy_volume = 0.995 * self.future_balance / self.moment.price
        self.sell_volume = self.buy_volume

        short_position(self.buy_volume, self.moment.price)
        self.buy_price = self.moment.price
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_time = [self.moment.hour, self.moment.minute]
        self.buy_date = self.moment.date

        if self.lock_method == 'lock_to_hour':
            lock_strategies["dummy_futures"] = [
                Dummy_Strategy_Futures, self.moment.candle_id + self.lock_hour, "normal"]
        elif self.lock_method == "lock_to_fin":
            lock_strategies["dummy_futures"] = [Dummy_Strategy_Futures, 0]

    def continue_strategy(self, working_strategies, **kwargs):
        if not (self.moment.hour == 16 and self.moment.minute == 0):
            return
        self.finish_txt = f'''date: {self.moment.date}
        Candle : {self.C}
        buy_time : {self.buy_date} {self.buy_time[0]}:{self.buy_time[1]} 
        sell_time : {self.moment.date} {self.moment.hour}:{self.moment.minute} 
        '''
        long_position(self.sell_volume, controller.get_this_moment().price)
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            lock_strategies.pop("dummy_futures")


class Ichi_future(Strategy):
    def check_short_con(self, key, value) -> bool:

        try:
            candle_26 = self.candles[self.moment.candle_id + 24]
        except:
            print('26_false')
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
            print('26_false')
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
        print('h')
        flag_short = 1
        flag_long = 1
        if self.moment.candle_id < 77:
            return False
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
            print(
                f'short happaend in {self.moment}\n{self.candles[self.moment.candle_id-1]}')
            return True
        if flag_long:
            print(
                f'long happaend in {self.moment}\n{self.candles[self.moment.candle_id-1]}')
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
                            value['option']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
                        tp = self.moment.price - \
                            value['options']['r2r']*value['option']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
                    if self.direction == 'long':
                        sl = self.moment.price - \
                            value['option']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
                        tp = self.moment.price + \
                            value['options']['r2r']*value['option']['sl'] * \
                            self.candles[self.moment.candle_id - 2].atr
        sl = round(sl, 2)
        tp = round(tp, 2)
        return sl, tp

    def manage_found(self, found_management):  # will return size & levrage
        loss_limit = 100 * abs(self.stop_loss -
                               self.entry_price) / self.entry_price
        total_risk = found_management['total_risk']
        print(f'loss_limit = {loss_limit}')
        total_found = 0.9 * self.future_balance

        r = (total_risk / loss_limit)
        print(f'r = {r}')
        if r < 1:
            found = total_found * r
            leverage = 1
        else:  # r > 1
            found = total_found
            leverage = r
        size = found / self.moment.price
        return size, leverage

    def start_strategy(self):
        global lock_strategies
        self.short_name = 'ichi_future'
        self.finish_txt = 'EMPTY'
        self.lock_hour = 0
        self.lock_method = "lock_to_fin"
        self.buy_time_date = self.moment.date
        self.buy_time_hour = self.moment.hour
        self.buy_time_minute = self.moment.minute
        self.C = self.candles[self.moment.candle_id-1]
        self.entry_price = self.moment.price

        # stoploss_calculation
        close_conditions = scenario.ichi_future['close_conditions']
        self.stop_loss, self.take_profit = self.calculate_stoploss(
            close_conditions)
        print(f'sl : {self.sl} , tp : {self.tp}')

        # managing_found :
        found_management = scenario.ichi_future['found_management']
        self.size, self.leverage = self.manage_found(found_management)
        print(f'size : {self.size} , leverage = {self.leverage}')

        # change leverage if needed
        if self.leverage != 1:
            controller.position.change_leverage(self.leverage)
            print('leverage changed')

        # Open Positions
        if self.direction == 'long':
            long_position(self.size, self.entry_price)
        elif self.direction == 'short':
            short_position(self.size, self.entry_price)

        if self.lock_method == 'lock_to_hour':
            lock_strategies[self.short_name] = [
                Ichi_future, self.moment.candle_id + self.lock_hour]
        elif self.lock_method == "lock_to_fin":
            lock_strategies[self.short_name] = [Ichi_future, 0]

    def continue_strategy(self, working_strategies, **kwargs):
        # if self.direction == 'short' :
        #     if self.moment.price >= self.sl
        pass