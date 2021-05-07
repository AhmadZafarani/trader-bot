# YA ALI
from model.Candle import Candle 
from model.Candle import get_Candle_byID
class Moment:
    def __init__(self, minute: int, hour: int, date: str, price: int , candleid : int ):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candleid = candleid 
        
        # self.moving12 = 0

    def update_moment(self, minute: int, hour: int, date: str, price: int, candleid : int , candles ):
        self.minute = minute
        self.date = date
        self.price = price
        self.hour = hour
        self.candleid = candleid
        if self.candleid <= 1:
            self.moving12 = price 
        elif self.candleid <= 12 and self.candleid > 1 : 
            self.moving12 = round((((self.candleid - 1)*candles[self.candleid -2].moving12) + self.price)/self.candleid , 3) 
        else:
            self.moving12 = round(((self.price - candles[self.candleid -13].close_price) /12) + candles[self.candleid -2].moving12 , 3)

    def __str__(self) -> str:
        return f'minute: {self.minute}, hour: {self.hour}, date: {self.date}, price: {self.price}'

    def __repr__(self) -> str:
        return self.__str__()
