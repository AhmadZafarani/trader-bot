# YA ALI
class Moment:
    def __init__(self, minute: int, hour: int, date: str, price: int, candleid: int):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candleid = candleid

    def update_moment(self, minute: int, hour: int, date: str, price: int, candleid: int):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candleid = candleid

    def __str__(self) -> str:
        return f'minute: {self.minute}, hour: {self.hour}, date: {self.date}, price: {self.price}'

    def __repr__(self) -> str:
        return self.__str__()
