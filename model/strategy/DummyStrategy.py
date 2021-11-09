from model.strategy.Strategy import Strategy
from controller import controller


class DummyStrategy(Strategy):
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
                DummyStrategy, self.moment.timestamp + self.lock_seconds, self.id]

            self.logger.warning(
                f'"{self.short_name}"" locked in {self.moment.get_time_string()} for {self.lock_seconds}s')
        elif self.lock_method == "lock_to_fin":
            lock_strategies["dummy"] = [DummyStrategy, 0]
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
