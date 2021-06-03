# YA ALI
class Moment:
    def __init__(self, minute: int, hour: int, date: str, price: int, candle_id: int, 
                 candle_extra_fields: dict, moment_extra_fields: dict):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candle_id = candle_id
        self.profit_loss_percentage = 0
        self.candle_extra_fields = candle_extra_fields
        self.moment_extra_fields = moment_extra_fields

    def update_moment(self, minute: int, hour: int, date: str, price: int, candle_id: int, 
                      profit_loss_percentage: float, candle_extra_fields: dict, moment_extra_fields: dict):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candle_id = candle_id
        self.profit_loss_percentage = profit_loss_percentage
        self.candle_extra_fields = candle_extra_fields
        self.moment_extra_fields = moment_extra_fields

    def __str__(self) -> str:
        return f'minute: {self.minute}, hour: {self.hour}, date: {self.date}, price: {self.price}'

    def __repr__(self) -> str:
        return self.__str__()
