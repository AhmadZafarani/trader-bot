# YA BAGHER
from model.indicators import *


class Scenario:
    log_file_path = 'logs/cndl-mmnt.log'

    candles_data_csv_file_name = 'BTC_FULL_1h.csv'

    moment_data_csv_file_name = 'BTC_FULL_1h_moment.csv'

    """
        these are dictionaries like this:
        EXTRA_DATA_NAME: EXTRA_FILE_PATH
        ** we assumed that the files are located some where in data/ directory. **
        ** EXTRA_DATA_NAME would be also used in Candle Class and Moment Class; so be careful at choosing its name. **
    """
    extra_candles_data_files = {
        "ma9": "BTC_FULL_1h_MA9.csv",
        "ma12": "BTC_FULL_1h_MA12.csv",
        "ma26": "BTC_FULL_1h_MA26.csv",
        "ma31": "BTC_FULL_1h_MA31.csv",
        "ma52": "BTC_FULL_1h_MA52.csv",
        "ICHI": "BTC_FULL_1h_ICHI.csv",
        "iscross": "BTC_FULL_1h_ISCROSS.csv"
    }
    extra_moments_data_files = {
    }

    fee = 0.001

    start_of_work_dollar_balance = 100000

    start_of_work_crypto_balance = 0

    number_of_moments_in_a_candle = 1

    profit_loss_period_step = 48 * 60

    peridical_profit_loss_limit = {"enable": 1, "options": {"profit_limit": 19, "loss_limit": -1.11}}
    # periodical_profit_loss_limit_enable = 1
    # periodical_profit_loss_limit['enable'] = periodical_profit_loss_limit_enable
    # =====================================================================
    # strategy configuration
    # name : Moving_average
    # opening conditions

    buy_method = {
        "price_to_line": {"enable": 0, "options": {"line": 9, "min_percentage": 50, "green": True}},
        "line_to_line": {"enable": 1, "options": {"line": [9, 26] ,"cross":1}}

    }
    sell_method = {
        "price_to_line": {"enable": 0, "options": {"line": 12, "min_percentage": 50, "red": True}},
        "line_to_line": {"enable": 0, "options": {"line": [12, 26]}},
        "profit_loss_limit": {"enable": 0, "options": {"profit_limit": 10, "loss_limit": -1}},
        "periodical_profit_loss_limit": {"enable": 1, "options": {"profit_limit": 12, "loss_limit": -1.8}}
    }
    volume_buy_ma = 89
    # buy_method_line_to_line_options_line = [31, 52]

    # buy_method_price_to_line_enable = 1
    # buy_method_line_to_line_enable = 1
    # sell_method_price_to_line_enable = 1
    # sell_method_line_to_line_enable = 1
    # sell_method_profit_loss_limit = 1
    # buy_method['line_to_line']['options']['line'] = buy_method_line_to_line_options_line
    # buy_method['price_to_line']['enable'] = buy_method_price_to_line_enable
    # buy_method['line_to_line']['enable'] = buy_method_line_to_line_enable
    # sell_method['price_to_line']['enable'] = sell_method_price_to_line_enable
    # sell_method['line_to_line']['enable'] = sell_method_line_to_line_enable
    # sell_method['profit_loss_limit']['enable'] = sell_method_profit_loss_limit
    # per_profit_limit = 20
    # per_loss_limit = -1.6
    # periodical_profit_loss_limit['options']['profit_limit'] = per_profit_limit
    # periodical_profit_loss_limit["options"]["loss_limit"] = per_loss_limit
    # =======================================================================
    # strategy configuration
    # name : ichi_cross
    # opening_conditions :

    # adx_min
    # values : 0 - 100
    # default : 15
    adx_min = 15

    # min_slope_dif
    # default :
    min_slope_dif = 0.15

    # under_cloud_condition2
    # values : 0 - 100 (percentage)
    # default : 4
    under_cloud_condition2 = 0.05

    # next_candle_length_min
    # values : -5 , 5
    # default : 1
    next_candle_length_min = 0.2

    # opening conditions intractions :
    # {CHECK_ADX , CHECK_SLOPE ,Buy_UnderCloud, CHECK_NEXT_CANDLE}
    opening_intractions = [0, 0, 1, 0]

    # closing_conditions:
    # methods :
    # method1: Price and T||K Cross
    # closing_con1_min
    # values : percentage
    # default : 50
    closing_con1_min = 50
    # ten_kij_dif_max_then_kij
    # values: percentage
    ten_kij_dif_max_then_kij = 5
    # ten_kij_dif_max_then_kij
    # values: 1 , 0
    closing_con1_red_candle = 1
    # method_2: bearish_tk_cross
    # no variable

    # method3: adx
    # met3_min_adx
    # value:0 - 100
    # default : 15
    closing_met3_min_adx = 15

    # method4 : loss_imit , profit_limit
    # profit limit
    # values : (0 , 100]
    # default : 10
    profit_limit = 5

    # loss limit
    # values : (0 , 100]
    # default : 10
    loss_limit = -2

    # # method5 : profit,loss limit on period
    # # profit limit
    # # values : (0 , 100]
    # # default : 10
    # profit_limit_per = 8

    # # loss limit
    # # values : (0 , 100]
    # # default : 10
    # loss_limit_per = -1.2

    # 'intraction'

    # intraction is a 5 bit binary number
    # example
    # default:11111
    # {Met1, Met2, Met3, Met4, Met5}
    close_intraction = [1, 0, 0, 0]
    volume_buy_ichi = 90

    # ================ LIVE PARAMETERS ===============================

    live_start_of_work_needed_candles = 30

    live_trading_mode = False

    live_candle_indicators = [
        ma12,
        ma26,
        ma9,
    ]

    live_moment_indicators = {
    }

    # in seconds
    live_sleep_between_each_moment = 60

    live_market = 'BTC/USDT'

    # in seconds
    live_try_again_time_inactive_market = 30

    live_timeframe = '1h'

    live_timeframe_in_seconds = 60 * 60

    # fill 4 last characters with what I have send in the Group
    live_api_encryption_key = b'alLePDlzw1-Q_LuB0qGWHcyqgflACUlEdPL0sFI2XgM='


scenario = Scenario()


def set_value(variable_name: str, value):
    scenario.__setattr__(variable_name, value)
