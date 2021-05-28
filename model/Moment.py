# YA ALI
class Moment:
    def __init__(self, minute: int, hour: int, date: str, price: int, candleid: int, 
                 extra_fields: dict):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candleid = candleid
        self.extra_fields = extra_fields

    def update_moment(self, minute: int, hour: int, date: str, price: int, candleid: int,
                      extra_fields: dict):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candleid = candleid
        self.extra_fields = extra_fields

    def __str__(self) -> str:
        return f'minute: {self.minute}, hour: {self.hour}, date: {self.date}, price: {self.price}'

    def __repr__(self) -> str:
        return self.__str__()
