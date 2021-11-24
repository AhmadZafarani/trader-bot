# YA BAGHER
from model.Position import Direction


class Scenario:
    mode = "future" # mode can be future or spot 
    month = "jan20"
    strtgg = "ichi"

    candles_data_csv_file_name = f'BTC_2021/BTC.csv'

    moment_data_csv_file_name = f'BTC_2021/BTC_moment.csv'

    """
        these are dictionaries like this:
        EXTRA_DATA_NAME: EXTRA_FILE_PATH
        ** we assumed that the files are located some where in data/ directory. **
        ** EXTRA_DATA_NAME would be also used in Candle Class and Moment Class; so be careful at choosing its name. **
    """
    extra_candles_data_files = {
        "ICHI": f"BTC_2021/BTC_ICHI.csv",
        "ATR" : f'BTC_2021/BTC_ATR.csv',
        "cloud_number" : "BTC_2021/BTC_Cloud_num.csv"
        # "ma9" : f'BTC_2021/BTC_MA9.csv',
        # "ma26" : f'BTC_2021/BTC_MA26.csv'
        # "ma26": f'jan20/BTC_jan20_MA26.csv'
    }
    extra_moments_data_files = {
    }

    fee = 0.001

    future_fee = 0.001 / 4
    # future_fee = 0
    start_of_work_dollar_balance = 100000

    start_of_work_crypto_balance = 0

    start_of_work_position = {"direction":Direction.NONE,
                              "size": 0, "entry_price": 0, "leverage": 1.25}

    start_of_work_future_dollar = 100000

    number_of_moments_in_a_candle = 1

    profit_loss_period_step = 24 * 30

    periodical_profit_loss_limit = {"enable": 0, "options": {
        "profit_limit": 18, "loss_limit": -1.11}}
    # periodical_profit_loss_limit_enable = 1

    global_limit = 0
    global_loss_limit = -1.0
    global_profit_limit = 1.0

    # periodical_profit_limit = 18.0
    # periodical_loss_limit = -1.5
    # periodical_profit_loss_limit['options']['loss_limit'] = periodical_loss_limit
    # periodical_profit_loss_limit['options']['profit_limit'] = periodical_profit_limit
    # periodical_profit_loss_limit['enable'] = periodical_profit_loss_limit_enable
    # =====================================================================
    # strategy configuration
    # name : Moving_average
    # opening conditions

    buy_method = {
        "price_to_line": {"enable": 0, "options": {"line": 9, "min_percentage": 50, "green": True}},
        "line_to_line": {"enable": 1, "options": {"line": [9, 26], "cross": 1}}
    }
    sell_method = {
        "price_to_line": {"enable": 0, "options": {"line": 12, "min_percentage": 50, "red": True}},
        "line_to_line": {"enable": 0, "options": {"line": [9, 26]}},
        "profit_loss_limit": {"enable": 0, "options": {"profit_limit": 10, "loss_limit": -1}},
    }
    volume_buy_ma = 80
    # buy_method_line_to_line_options_line = [31, 52]

    # buy_method_price_to_line_enable = 1
    # buy_method_line_to_line_enable = 1
    # buy_method_line_to_line_cross = 1
    # sell_method_line_to_line_enable = 0
    # sell_method_price_to_line_enable = 1
    # sell_method_line_to_line_enable = 0
    # sell_method_profit_loss_limit = 1
    # buy_method['line_to_line']['options']['line'] = buy_method_line_to_line_options_line
    # buy_method['price_to_line']['enable'] = buy_method_price_to_line_enable
    # buy_method['line_to_line']['enable'] = buy_method_line_to_line_enable
    # buy_method['line_to_line']['options']['cross'] = buy_method_line_to_line_cross
    # sell_method['line_to_line']['enable'] = sell_method_line_to_line_enable
    # sell_method['price_to_line']['enable'] = sell_method_price_to_line_enable
    # sell_method['line_to_line']['enable'] = sell_method_line_to_line_enable
    # sell_method['profit_loss_limit']['enable'] = sell_method_profit_loss_limit
    # per_profit_limit = 20
    # per_loss_limit = -1.6
    # peridical_profit_loss_limit['options']['profit_limit'] = per_profit_limit
    # peridical_profit_loss_limit["options"]["loss_limit"] = per_loss_limit

# =======================================================================

    #  strategy = ichi_future 
    
    # opening conditins 
    ichi_future = {
        "enterance" : {
            "short" : {
                "red_cloud" : {"enable" : 1 , } ,
                "ten_under_kij" : {"enable" : 1 } , 
                "close_under_cloud" : {"enable" : 1},
                "span_under_cloud" : {"enable" : 1} 
            },
            "long" : {
                "green_cloud" : {"enable" : 1} ,
                "kij_inder_ten" : {"enable" : 1 } , 
                "close_upper_cloud" : {"enable" : 1},
                "span_upper_cloud" : {"enable" : 1} 
            },
            "options" : {'only_one_in_a_cloud' : 1, 'on_border' : 0}
        },
        "close_conditions" : {
            "based_on_cloud" : {"enable" : 0 , "options" : {"r2r" : 2}},
            "based_on_atr" : {"enable" : 1 , "options":{"sl" : 1.7,"r2r" : 3}},
            "span_close_signal" : {"enable" : 0},
            "cross_close_signal" : {"enable" : 0}
        }, 
        "found_management" : {
            "total_risk" : 4
        }
    }
     
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
    opening_intractions = [0, 0, 0, 0]

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
    close_intraction = [0, 0, 0, 0]
    volume_buy_ichi = 90


scenario = Scenario()


def set_value(variable_name: str, value):
    scenario.__setattr__(variable_name, value)
