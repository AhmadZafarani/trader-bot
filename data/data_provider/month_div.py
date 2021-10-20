
import os 
from hourly_data import h
from ichimoku_bemola import ichi
from ma import ma
from span_cross_calc import iscross
months = ['jan20', 'feb20', 'mar20', 'apr20' , 'may20', 'jun20' , 'jul20' , 'aug20' , 'sep20', 'oct20' , 'nov20' , 'dec20',
'jan21', 'feb21', 'mar21', 'apr21' , 'may21', 'jun21' , 'jul21' , 'aug21' , 'sep21'
]

def get_month_name(month_name : int):
    
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

for month in months : 
    try : 
        os.mkdir("data/"+month)
    except : 
        pass

    h('btc', time + (24 * 60 * 60 * get_month_name(int(i % 12))) , time , month+'/BTC_'+month)
    ichi(month+'/BTC_'+month , month+'/BTC_'+month)
    iscross(month+'/BTC_'+month ,month+'/BTC_'+month)
    ma(9 , month+'/BTC_'+month , month+'/BTC_'+month)
    ma(26 , month+'/BTC_'+month , month+'/BTC_'+month)
    time += (24 * 60 * 60 * get_month_name(i % 12))
    i += 1 