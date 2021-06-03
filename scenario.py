# YA BAGHER
candles_data_csv_file_name = 'onehour.csv'


moment_data_csv_file_name = 'oneminute.csv'

"""
    these are dictionaries like this:
    EXTRA_DATA_NAME: EXTRA_FILE_PATH

    ** we assumed that the files are located some where in data/ directory. **
    ** EXTRA_DATA_NAME would be also used in Candle Class and Moment Class; so be careful at choosing its name. **
"""
extra_candles_data_files = {}


extra_moments_data_files = {}


fee = 0.075


start_of_work_dollar_balance = 1000


start_of_work_crypto_balance = 0


number_of_moments_in_a_candle = 60


# locking strategy
# for locking strategy you have two methods
# set lock hour
# lock to finish strategy

# 'lock_hour' : you can adjust lock hour
# values : N
# default  : 1
lock_hour = 3


# 'lock_method'
# values :
# "lock_to_fin"
# "lock_to_hour"
# default: "lock_to_fin"
lock_method = "lock_to_fin"


profit_loss_period_step = 0
