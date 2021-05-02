# YA MAHDI
from datetime import datetime


class Candle:
    def __init__(self, identifier: int, time: int, high_price: float, low_price: float, open_price: float, close_price: float,
                 traded_volume: float):
        self.identifier = identifier
        self.date, self.hour = self.extract_time(time)
        self.high_price = high_price
        self.low_price = low_price
        self.open_price = open_price
        self.close_price = close_price
        self.traded_volume = traded_volume
        self.speed = self.find_speed()

    def find_speed(self) -> float:
        r = 2 * (self.high_price - self.low_price) + \
            (self.close_price - self.open_price)
        s = r / 60
        return round(s, 4)

    def extract_time(self, time: int) -> tuple:
        t = datetime.fromtimestamp(time)
        return t.date().strftime('%x'), t.hour

    def minute_price(self, i: int) -> float:
        p = 0
        if i < 16:
            p = min(self.speed * i + self.open_price, self.high_price)
        elif i < 46:
            p = max(self.high_price - self.speed * i, self.low_price)
        elif i < 61:
            p = min(self.low_price + self.speed * i, self.high_price)
        return round(p, 4)

    def __str__(self) -> str:
        return f'id: {self.identifier}, date: {self.date}, hour: {self.hour}, high: {self.high_price}, low: {self.low_price}, open: {self.open_price}, close: {self.close_price}, speed: {self.speed}'

    def __repr__(self) -> str:
        return self.__str__()
