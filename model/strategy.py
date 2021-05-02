# YA REZA
from model.Moment import Moment
from abc import ABC, abstractmethod
import controller.controller as controller


class Strategy(ABC):
    def __init__(self, moment: Moment):
        self.moment = moment
        self.working = False
        self.buy_price = 0
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

    @staticmethod
    def report(buy_price: int, sell_price: int, strategy_name: str, bought_volume: int, sold_volume: int) -> str:
        if buy_price <= sell_price:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tProfit\n\n'
        else:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t{bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tLoss\n\n'
        return s


class Dummy_Strategy(Strategy):
    volume = 1

    def strategy_works(self) -> bool:
        return self.moment.hour == 13 and self.moment.minute == 0

    def start_strategy(self):
        controller.buy(self.volume, self.moment.price)
        self.buy_price = self.moment.price

    def continue_strategy(self):
        if not (controller.get_this_moment().hour == 15 and controller.get_this_moment().minute == 0):
            return
        controller.sell(self.volume, controller.get_this_moment().price)
        controller.set_report(Strategy.report(self.buy_price,
                                              controller.get_this_moment().price, 'Dummy', self.volume, self.volume))
        self.working = False
