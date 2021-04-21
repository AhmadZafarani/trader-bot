# YA MAHDI
class Candle:
    def __init__(self, id: int, time: int, high: float, low: float, open: float, close: float):
        self.id = id
        self.time = time
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.speed = self.find_speed()

    def find_speed(self) -> float:
        r = abs(self.high - self.open) + abs(self.high -
                                             self.low) + abs(self.close - self.low)
        r = round(r, 2)
        s = r / 60
        return s

    def iran_time(self, time: int) -> int:
        pass
