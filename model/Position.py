# YA MASOOMEH
from enum import Enum


class Direction(Enum):
    LONG = 1
    SHORT = -1
    NONE = 0


class Position:
    def __init__(self, direction: Direction, size: int, entry_price: int, leverage: int):
        self.direction = direction
        self.size = size
        self.entry_price = entry_price
        self.leverage = leverage

    def calculate_pnl(self, price: int):
        if self.direction != Direction.NONE:
            self.pnl = self.size*(price - self.entry_price) * \
                self.leverage*int(self.direction)
        else:
            self.pnl = 0
        return self.pnl

    def __str__(self):
        return f'direction:{self.direction}, size:{self.size}, entry_price:{self.entry_price}, leverage:{self.leverage}, pnl:{self.pnl}'
