# YA BAGHER
candles_data_csv_file_name = 'test/btc_two_days_for_test_1h.csv'


moment_data_csv_file_name = 'test/btc_two_days_for_test_1m.csv'


"""
    these are dictionaries like this:
    EXTRA_DATA_NAME: EXTRA_FILE_PATH

    ** we assumed that the files are located some where in data/ directory. **
    ** EXTRA_DATA_NAME would be also used in Candle Class and Moment Class; so be careful at choosing its name. **
"""
extra_candles_data_files = {
    "moving12": "test/btc_test_ma12.csv", "ADX": "test/btc_test_adx.csv"}


extra_moments_data_files = {}


fee = 0.001


start_of_work_dollar_balance = 100000


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


# in moments
profit_loss_period_step = 1440


# Opening Conditiotions
# in this section you can configuire when this strategy will open

# we have two conditions , these two conditions work together (see strategy docs for more details

# condition1
# as you know this condition work base on the relation between moving 12 and candles
# you can inspect 1 , 2 or 3 candles . anyway strategy check the 'close_price' of first candle .

# Using 'Opening_Con1_num_of_candles' property you can determine the number of candles to inspect
# values can be : {1, 2, 3}
# default : 3
opening_con1_num_of_candles = 2


# using 'opening_con1_min_first' property you can determine the minimum percentage of 'close_price' of the firts candle to be more than the moving12
# values can be : [1 , 99]
# default : 30 %
opening_con1_min_first = 1


# condition 2
# condition 2 is based on ADX , DI+ , DI-

# 'opening_con2_min_adx'   : fixing the minimum adx for opening
# values can be : [25-50]
# default: 25
opening_con2_min_adx = 12.5


# 'opening_con2_di_method'
# for inspectiong DI+ and DI- you have two methods (for more details check strategy docs)
# values:
# "positive" => DI+(-1) -  DI-(-1) > 0
# "increasing" => (DI+(-1) -  DI-(-1)) - (DI+(-2) -  DI-(-2)) > 0
# default : "positive"
opening_con2_di_method = "positive"


# Closing condtitions
# for closing we have 3 methods
# defrent mechanism of closing depends on the intraction of these methods and each method configutation
# in this section you can fix each method and the intraction of the methods

# method 1
# it is just like the first condition of opening

# Using 'closing_meth1_num_of_candles' property you can determine the number of candles to inspect
# values can be : {1, 2, 3}
# default : 3
closing_meth1_num_of_candles = 2

# using 'closing_met1_min_first' property you can determine the minimum percentage of 'close_price' of the firts candle to be more than the moving12
# values can be : [1 , 99]
# default : 70 %
closing_met1_min_first = 1


# method 2
# this method and condition 2 are the same

# 'closing_met2_max_adx'   : fixing the maximum adx for closing
# values can be : [25-10]
# default: 25
closing_met2_max_adx = 12.5


# method3
# this method is just based on profit and loss limit

# profit limit
# values : (0 , 100]
# default : 10
profit_limit = 3

# loss limit
# values : (0 , 100]
# default : 10
loss_limit = -1.5


# 'intraction'

# intraction is a 3 bit binary number
# from MSB to LSB each bit belongs to one of the method
# at the end it will OR the methods
# example
# if intraction = 0b011
# it will OR(meh2 , met 3)
# values : binary number  : [000 , 111]
# dufault:101

intraction = int('110', 2)


# volume_buy
# value (percent) : ( 0  , 100]
# default : 50
volume_buy = 80
