# YA GHAFFAR
from controller import controller
from model.Moment import Moment
from model.strategy.Strategy import Strategy
from scenario import scenario


class MovingAverage(Strategy):
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
                    if 100 * (cndl[-1].close_price - moving_average) / (cndl[-1].close_price - cndl[-1].open_price) >= \
                            value["options"]["min_percentage"]:
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
        for key, value in scenario.buy_method.items():
            if value['enable'] == 1:
                if self.check_open_con(key=key, value=value):
                    return True

    def start_strategy(self):
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
        self.C = self.candles[self.moment.candle_id - 1]
        self.buy_price = self.moment.price
        self.logger.warning(
            f" \"{self.id}\" - Details : volume = {self.buy_volume} , price = {self.buy_price}")
        controller.buy(self.buy_volume, self.moment.price)

        self.logger.warning(
            f'"{self.id}" - Volume:{self.buy_volume} & price={self.buy_price}')
        if self.lock_method == 'lock_to_hour':
            controller.lock_strategies["moving_average"] = [
                MovingAverage, self.moment.timestamp + self.lock_seconds, self.id]

            self.logger.warning(
                f'"{self.short_name}"" locked in {self.moment.get_time_string()} for {self.lock_seconds}s')
        elif self.lock_method == "lock_to_fin":
            controller.lock_strategies["moving_average"] = [MovingAverage, 0]
            self.logger.warning(
                f'"{self.short_name}" locked in {self.moment.get_time_string()} until "{self.id}" finish')

    def fin_and_before(self):
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute

        controller.sell(self.buy_volume, self.sell_price)
        self.sold = True
        self.finish_strategy(self.finish_txt)
        if self.lock_method == "lock_to_fin":
            controller.lock_strategies.pop(self.short_name)

    def check_close_con(self, key: str, value: dict):
        if key == "price_to_line":
            cndl = [self.candles[self.moment.candle_id - 1],
                    self.candles[self.moment.candle_id - 2]]
            moving_average = getattr(
                self.candles[self.moment.candle_id - 2], "ma" + str(value["options"]["line"]))
            if value["options"]["red"]:
                if cndl[-1].close_price < cndl[-1].open_price:
                    if 100 * (moving_average - cndl[-1].close_price) / (cndl[-1].open_price - cndl[-1].close_price) >= \
                            value["options"]["min_percentage"]:
                        if cndl[0].open_price < moving_average:
                            return True
                return False
            else:
                maximum = max(cndl[-1].open_price, cndl[-1].close_price)
                minimum = min(cndl[-1].open_price, cndl[-1].close_price)
                if 100 * (moving_average - minimum) / (maximum - minimum) > value["options"]["min_percentage"]:
                    if cndl[0].open_price < moving_average:
                        return True
                return False
        if key == "line_to_line":
            moving1 = [
                getattr(self.candles[self.moment.candle_id - 2], "ma" + str(value["options"]["line"][0])),
                getattr(self.candles[self.moment.candle_id - 3], "ma" + str(value["options"]["line"][0]))
            ]
            moving2 = [
                getattr(self.candles[self.moment.candle_id - 2], "ma" + str(value["options"]["line"][1])),
                getattr(self.candles[self.moment.candle_id - 3], "ma" + str(value["options"]["line"][1]))
            ]
            if moving1[0] < moving2[0] and moving1[1] >= moving2[1]:
                return True
        if key == "profit_loss_limit":
            profit_limit = self.buy_price * (1 + value["options"]["profit_limit"] / 100)
            loss_limit = self.buy_price * (1 + value["options"]["loss_limit"] / 100)
            if self.moment.price >= profit_limit:
                self.sell_price = profit_limit
                profit = round((self.sell_price - self.buy_price) * self.buy_volume, 3)
                fee = scenario.fee * self.buy_price * self.buy_volume + scenario.fee * self.sell_price * self.buy_volume
                self.finish_txt = f"""
                # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
                # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
                # profit(%): {profit}({round(100 * (self.sell_price - self.buy_price) / self.buy_price, 3)})
                # fee : {fee} $
                # buy Candle : {self.C}
                # sell Candle : {self.CC}
                # """
                return True
            elif self.moment.price <= loss_limit:
                self.sell_price = loss_limit
                profit = round((self.sell_price - self.buy_price) * self.buy_volume, 3)
                fee = scenario.fee * self.buy_price * self.buy_volume + scenario.fee * self.sell_price * self.buy_volume
                self.finish_txt = f"""
                # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
                # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
                # profit(%): {profit}({round(100 * (self.sell_price - self.buy_price) / self.buy_price, 3)})
                # fee : {fee} $
                # buy Candle : {self.C}
                # sell Candle : {self.CC}
                # """
                return True
            return False

    def continue_strategy(self, working_strategies, **kwargs):
        self.sell_price = controller.get_this_moment().price
        self.sell_time_date = self.moment.date
        self.sell_time_hour = self.moment.hour
        self.sell_time_minute = self.moment.minute
        self.CC = self.candles[self.moment.candle_id - 1]
        profit = round((self.sell_price - self.buy_price) * self.buy_volume, 3)
        fee = scenario.fee * self.buy_price * self.buy_volume + scenario.fee * self.sell_price * self.buy_volume
        self.finish_txt = f"""
        # buy time: {self.buy_time_date} {self.buy_time_hour}:{self.buy_time_minute}
        # sell time: {self.sell_time_date} {self.sell_time_hour}:{self.sell_time_minute}
        # profit(%): {profit}({round(100 * (self.sell_price - self.buy_price) / self.buy_price, 3)})
        # fee : {fee} $
        # buy Candle : {self.C}
        # sell Candle : {self.CC}
        # """
        for key, value in scenario.sell_method.items():
            if value['enable']:
                if self.check_close_con(key=key, value=value):
                    self.fin_and_before()
                    break
