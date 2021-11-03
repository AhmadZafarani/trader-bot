# YA ALI
from model.strategy import Strategy, lock_strategies, strategies
from controller.futures_controller import short_position, long_position
import controller.controller as controller


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


strategies['dummy_futures'] = Dummy_Strategy_Futures
