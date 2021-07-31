# YA MAHDI
"""
    extra_fields is a dictionary like:
    INDICATOR_NAME: INDICATOR_VALUE_IN_THAT_CANDLE

    all values of this dictionary are of str type. so you are responsible for casting them to other types 
    in the Strategies.
"""


class Candle:
    def __init__(self, identifier: int, high_price: float, low_price: float, open_price: float,
                 close_price: float, traded_volume: float):
        self.identifier = identifier
        self.high_price = high_price
        self.low_price = low_price
        self.open_price = open_price
        self.close_price = close_price
        self.traded_volume = traded_volume

    def __str__(self) -> str:
        return f'id: {self.identifier}, high: {self.high_price}, low: {self.low_price}, open: {self.open_price}, close: {self.close_price}'

    def __repr__(self) -> str:
        return self.__str__()
