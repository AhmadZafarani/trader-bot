# YA BAGHER
class Scenario:
    log_file_path = 'logs/cndl-mmnt.log'

    candles_data_csv_file_name = 'BTC_2021_15m_cndl.csv'

    moment_data_csv_file_name = 'BTC_2021_1m_mmnt.csv'

    """
        these are dictionaries like this:
        EXTRA_DATA_NAME: EXTRA_FILE_PATH

        ** we assumed that the files are located some where in data/ directory. **
        ** EXTRA_DATA_NAME would be also used in Candle Class and Moment Class; so be careful at choosing its name. **
    """
    extra_candles_data_files = {
    }

    extra_moments_data_files = {
    }

    fee = 0.001

    start_of_work_dollar_balance = 100000

    start_of_work_crypto_balance = 0

    number_of_moments_in_a_candle = 15

    profit_loss_period_step = 24

    lock_method = "lock_to_hour"
    lock_hour = 16

    # ================ LIVE PARAMETERS ===============================

    live_start_of_work_needed_candles = 10

    live_trading_mode = False


scenario = Scenario()


def set_value(variable_name: str, value):
    scenario.__setattr__(variable_name, value)
