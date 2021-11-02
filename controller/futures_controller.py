# YA ZAHRA
from model.Position import Position, Direction
from scenario import scenario


position = Position(scenario.start_of_work_position['direction'], scenario.start_of_work_position['size'],
                    scenario.start_of_work_position['entry_price'], scenario.start_of_work_position['leverage'])
future_balance = scenario.start_of_work_future_dollar


def long(size: int, price: int):
    global position, future_balance
    size = round(size, 4)
    if position.direction == Direction.NONE:
        position.size += size
        position.entry_price = price
        position.direction = Direction.LONG
        future_balance -= (size * price * (1 + scenario.future_fee))
        future_balance = round(future_balance, 4)
        if future_balance < 0:
            raise RuntimeError('future_balance is negative')
    elif position.direction == Direction.SHORT:
        if size < position.size:
            position.size -= size
            future_balance += (size * position.entry_price) + position.pnl
            future_balance - + (size * price) * scenario.future_fee
            future_balance = round(future_balance, 4)
            if future_balance < 0:
                raise RuntimeError('future_balance is negative')
        elif size == position.size:
            position.size = 0
            position.direction = Direction.NONE
            future_balance += (size * position.entry_price) + position.pnl
            future_balance - + (size * price) * scenario.future_fee
            future_balance = round(future_balance, 4)
            position.entry_price = 0
            if future_balance < 0:
                raise RuntimeError('future_balance is negative')
        elif size > position.size:
            future_balance += (position.size *
                               position.entry_price) + position.pnl
            future_balance - + (size * price) * scenario.future_fee
            position.size = size - position.size
            position.direction = Direction.LONG
            position.entry_price = price
            future_balance -= ((size - position.size) * price)
            future_balance = round(future_balance, 4)
            if future_balance < 0:
                raise RuntimeError('future_balance is negative')
    elif position.direction == Direction.LONG:
        position.entry_price = (
            position.entry_price * position.size + size * price) / (size + position.size)
        position.entry_price = round(position.entry_price, 4)
        position.size += size
        future_balance -= (size * price * (1 + scenario.future_fee))
        future_balance = round(future_balance, 4)
        if future_balance < 0:
            raise RuntimeError('future_balance is negative')


def Short(size: int, price: int):
    global position, future_balance
    size = round(size, 4)
    if position.direction == Direction.NONE:
        position.size += size
        position.entry_price = price
        position.direction = Direction.SHORT
        future_balance -= (size * price * (1 + scenario.future_fee))
        future_balance = round(future_balance, 4)
        if future_balance < 0:
            raise RuntimeError('future_balance is negative')
    elif position.direction == Direction.LONG:
        if size < position.size:
            position.size -= size
            future_balance += (size * position.entry_price) + position.pnl
            future_balance - + (size * price) * scenario.future_fee
            future_balance = round(future_balance, 4)
            if future_balance < 0:
                raise RuntimeError('future_balance is negative')
        elif size == position.size:
            position.size = 0
            position.direction = Direction.NONE
            future_balance += (size * position.entry_price) + position.pnl
            future_balance - + (size * price) * scenario.future_fee
            future_balance = round(future_balance, 4)
            position.entry_price = 0
            if future_balance < 0:
                raise RuntimeError('future_balance is negative')
        elif size > position.size:
            future_balance += (position.size *
                               position.entry_price) + position.pnl
            future_balance - + (size * price) * scenario.future_fee
            position.size = size - position.size
            position.direction = Direction.SHORT
            position.entry_price = price
            future_balance -= ((size - position.size) * price)
            future_balance = round(future_balance, 4)
            if future_balance < 0:
                raise RuntimeError('future_balance is negative')
    elif position.direction == Direction.SHORT:
        position.entry_price = (
            position.entry_price * position.size + size * price) / (size + position.size)
        position.entry_price = round(position.entry_price, 4)
        position.size += size
        future_balance -= (size * price * (1 + scenario.future_fee))
        future_balance = round(future_balance, 4)
        if future_balance < 0:
            raise RuntimeError('future_balance is negative')
