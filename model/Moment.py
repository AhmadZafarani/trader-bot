# YA ALI
class Moment:
    def __init__(self, minute: int, hour: int, date: str, price: int):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour

    def update_moment(self, minute: int, hour: int, date: str, price: int):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
