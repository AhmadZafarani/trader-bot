# YA RAHIM
from model.strategy.Strategy import Strategy
from model.Moment import Moment
from controller import controller


class DummyStrategy(Strategy):
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
        self.buy_time = None

    def strategy_works(self) -> bool:
        return True

    def start_strategy(self):
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
            controller.lock_strategies["dummy"] = [
                DummyStrategy, self.moment.timestamp + self.lock_seconds, self.id]

            self.logger.warning(
                f'"{self.short_name}"" locked in {self.moment.get_time_string()} for {self.lock_seconds}s')
        elif self.lock_method == "lock_to_fin":
            controller.lock_strategies["dummy"] = [DummyStrategy, 0]
            self.logger.warning(
                f'"{self.short_name}" locked in {self.moment.get_time_string()} until "{self.id}" finish')

    def continue_strategy(self, working_strategies, **kwargs):
        pass
