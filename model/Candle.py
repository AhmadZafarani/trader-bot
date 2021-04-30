# YA MAHDI
from datetime import datetime


class Candle:
    def __init__(self, identifier: int, time: int, high_price: float, low_price: float, open_price: float, close_price: float,
                 traded_volume: int):
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
        r = round(r, 2)
        s = r / 60
        return s

    def extract_time(self, time: int) -> tuple:
        t = datetime.fromtimestamp(time)
        return t.date().strftime('%x'), t.hour

    def minute_price(self, i: int) -> int:
        p = 0
        if i < 16:
            p = max(int(self.speed * i) + self.open_price, self.high_price)
        elif i < 46:
            p = max(self.high_price - int(self.speed * i), self.low_price)
        elif i < 61:
            p = max(self.low_price + int(self.speed * i), self.high_price)
        return p
