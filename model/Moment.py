# YA ALI
from datetime import datetime

from pytz import timezone


def extract_time(time: int) -> tuple:
    t = datetime.fromtimestamp(time, timezone('GMT'))
    return t.date().strftime('%x'), t.hour, t.minute, t.second, time


class Moment:
    def __init__(self, time: int, price: float, candle_id: int):
        self.date, self.hour, self.minute, self.second, self.timestamp = extract_time(
            time)
        self.price = price
        self.candle_id = candle_id
        self.profit_loss_percentage = 0
        self.moment_id = 0

    def update_moment(self, time: int, price: float, candle_id: int,
                      profit_loss_percentage: float, moment_id: int):
        self.date, self.hour, self.minute, self.second, self.timestamp = extract_time(
            time)
        self.price = price
        self.candle_id = candle_id
        self.profit_loss_percentage = profit_loss_percentage
        self.moment_id = moment_id

    def __str__(self) -> str:
        return f'fields: {self.__dict__}'

    def __repr__(self) -> str:
        return self.__str__()

    def get_time_string(self):
        return f'{self.date} - {self.hour}:{self.minute}:{self.second}'

    def decrease_moment_id(self):
        self.moment_id -= 1

    def set_profit_loss_percentage(self, profit_loss_percentage: float):
        self.profit_loss_percentage = profit_loss_percentage
