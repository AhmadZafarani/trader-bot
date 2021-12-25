import os
from forex_data_provider import forex_data
from ichimoku_bemola import ichi
from ma import ma
from ATR import ATR
from cloud_number import cloud_number_generateor
from span_cross_calc import iscross
from datetime import datetime
from datetime import timezone
import time
from dateutil.relativedelta import relativedelta

months = ['jan20', 'feb20', 'mar20', 'apr20', 'may20', 'jun20', 'jul20', 'aug20', 'sep20', 'oct20', 'nov20', 'dec20',
          'jan21', 'feb21', 'mar21', 'apr21', 'may21', 'jun21', 'jul21', 'aug21', 'sep21', 'oct21', 'nov21']


def get_month_name(month_name: int):

    if month_name == 2:
        return 29
    elif month_name in (4, 6, 9, 11):
        return 30
    elif month_name in (1, 3, 5, 7, 8, 10, 0):
        return 31
    else:
        print("Wrong month name")


time = 1577836800

i = 1
pair = "AAPL_"
base_time = datetime.strptime("01.01.2020 00:00:00", '%m.%d.%Y %H:%M:%S').replace(tzinfo=timezone.utc)

for month in months:
    print(month)
    try: 
        os.mkdir("data/final_test/" + pair + "USDT/" + month + "/")
    except:
        pass
    data_folder = 'final_test/' + pair + 'USDT/' + month + "/"
    output_folder = 'final_test/' + pair + 'USDT/' + month + "/"
    
    # generating a specific month data in data/..
    forex_data('AAPL.us', base_time+relativedelta(months=1), base_time, data_folder + pair + 'USDT')
    base_time += relativedelta(months=1)

    # generating andicator data : input1: data folder input2: output folder
    ichi(data_folder + pair + 'USDT', output_folder + pair + 'USDT')
    iscross(data_folder + pair + 'USDT', output_folder + pair + 'USDT')
    ma(9, data_folder + pair + 'USDT', output_folder + pair + 'USDT')
    ma(26, data_folder + pair + 'USDT', output_folder + pair + 'USDT')
    ATR(data_folder + pair + 'USDT', output_folder + pair + 'USDT')
    cloud_number_generateor(data_folder + pair + 'USDT', output_folder + pair + 'USDT')

    # setting time
    time += (24 * 60 * 60 * get_month_name(i % 12))
    i += 1
