# YA ALI
from datetime import datetime
from pytz import timezone


class Moment:
    def __init__(self, time: int, price: int, candle_id: int):
        self.minute, self.date, self.hour = self.extract_time(time)
        self.price = price
        self.candle_id = candle_id
        self.profit_loss_percentage = 0

    def update_moment(self, time: int, price: int, candle_id: int,
                      profit_loss_percentage: float):
        self.date, self.hour, self.minute = self.extract_time(time)
        self.price = price
        self.candle_id = candle_id
        self.profit_loss_percentage = profit_loss_percentage

    def extract_time(self, time: int) -> tuple:
        t = datetime.fromtimestamp(time, timezone('GMT'))
        return t.date().strftime('%x'), t.hour, t.minute

    def __str__(self) -> str:
        return f'minute: {self.minute}, hour: {self.hour}, date: {self.date}, price: {self.price}'

    def __repr__(self) -> str:
        return self.__str__()
