# YA ROGHAYYEH
"""
    all functions in this file should have this specification:
    @param: index: candle index, witch the function is calculating its indicators
    @param: candles: list of Candles
    @return: dictionary like:
        'INDICATOR_NAME': INDICATOR_VALUE
"""


def moving_average(index: int, candles: list) -> dict:
    return {'moving_average': index}
