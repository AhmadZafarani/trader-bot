# YA REZA
from model.Moment import Moment
from abc import ABC, abstractmethod
from controller.controller import buy, sell, get_this_moment, set_report
from threading import Thread


class Strategy(ABC):
    def __init__(self, moment: Moment):
        self.moment = moment
        if self.strategy_works():
            self.result, self.bitcoin = self.continue_strategy()

    @abstractmethod
    def strategy_works(self) -> bool:
        pass

    @abstractmethod
    def continue_strategy(self):
        pass

    @staticmethod
    def report(buy_price: int, sell_price: int, strategy_name: str, bought_volume: int, sold_volume: int) -> str:
        if buy_price <= sell_price:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t \
                {bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tProfit'
        else:
            s = f'Strategy:\t{strategy_name}\nBuy Price:\t{buy_price}\nSell Price:\t{sell_price}\nBought Volume:\t \
                {bought_volume}\nSold Volume:\t{sold_volume}\nResult:\tLoss'
        return s


class Dummy_Strategy(Strategy):
    volume = 1

    def strategy_works(self) -> bool:
        return self.moment.hour == 13 and self.moment.minute == 0

    def continue_strategy(self):
        t = Thread(target=self.trade, args=(), daemon=True)
        t.start()

    def trade(self):
        buy(self.volume, self.moment.price)
        # wait
        while not (get_this_moment().hour == 15 and get_this_moment().minute == 0):
            pass
            # wait
        sell(self.volume, get_this_moment().price)
        set_report(Strategy.report(self.moment.price,
                                   get_this_moment().price, 'Dummy', self.volume, self.volume))
