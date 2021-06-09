# YA ALI
from datetime import datetime


class Moment:
    def __init__(self, time: int, price: int, candle_id: int, candle_extra_fields: dict, moment_extra_fields: dict):
        self.minute, self.date, self.hour = self.extract_time(time)
        self.price = price
        self.candle_id = candle_id
        self.profit_loss_percentage = 0
        self.candle_extra_fields = candle_extra_fields
        self.moment_extra_fields = moment_extra_fields

    def update_moment(self, time: int, price: int, candle_id: int,
                      profit_loss_percentage: float, candle_extra_fields: dict, moment_extra_fields: dict):
        self.minute, self.date, self.hour = self.extract_time(time)
        self.price = price
        self.candle_id = candle_id
        self.profit_loss_percentage = profit_loss_percentage
        self.candle_extra_fields = candle_extra_fields
        self.moment_extra_fields = moment_extra_fields

    def extract_time(self, time: int) -> tuple:
        t = datetime.fromtimestamp(time)
        return t.date().strftime('%x'), t.hour, t.minute

    def __str__(self) -> str:
        return f'minute: {self.minute}, hour: {self.hour}, date: {self.date}, price: {self.price}'

    def __repr__(self) -> str:
        return self.__str__()
