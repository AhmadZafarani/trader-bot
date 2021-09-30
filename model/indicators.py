# YA ROGHAYYEH
"""
    all functions in this file should have this specification:
    @param: index: candle index, witch the function is calculating its indicators
    @param: candles: list of Candles
    @return: dictionary like:
        'INDICATOR_NAME': INDICATOR_VALUE
"""


def moving_average(length: int, index: int, candles: list) -> float:
    if index < length - 1:
        sum = 0
        for cll in candles[0:index + 1]:
            sum += cll.close_price
        return round(sum / (index + 1), 3)

    if index >= length - 1:
        sum = 0
        for cll in candles[index - length + 1:index + 1]:
            sum += cll.close_price
        return round(sum / (length), 3)


def ma12(index: int, candles: list) -> dict:
    return {'ma12': moving_average(12, index, candles)}


def ma26(index: int, candles: list) -> dict:
    return {'ma26': moving_average(26, index, candles)}


def ma9(index: int, candles: list) -> dict:
    return {'ma9': moving_average(9, index, candles)}
