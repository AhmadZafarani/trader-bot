# YA MAHDI
from datetime import datetime


class Candle:
    def __init__(self, identifier: int, time: int, high_price: float, low_price: float, open_price: float, 
                 close_price: float, traded_volume: float):
        self.identifier = identifier
        self.date, self.hour = self.extract_time(time)
        self.high_price = high_price
        self.low_price = low_price
        self.open_price = open_price
        self.close_price = close_price
        self.traded_volume = traded_volume

    def extract_time(self, time: int) -> tuple:
        t = datetime.fromtimestamp(time)
        return t.date().strftime('%x'), t.hour

    def __str__(self) -> str:
        return f'id: {self.identifier}, date: {self.date}, hour: {self.hour}, high: {self.high_price}, low: {self.low_price}, open: {self.open_price}, close: {self.close_price}'

    def __repr__(self) -> str:
        return self.__str__()
