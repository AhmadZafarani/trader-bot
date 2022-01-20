import os
from ichimoku_bemola import ichi
from ma import ma
from rsi import rsi
from P_SAR import P_SAR
from span_cross_calc import iscross
from bolinger_bound import BB
stock = "فملی"
try:
    os.mkdir("data/tse/" + stock + "/")
except:
    pass
data_folder = 'tse_data/'
output_folder = 'tse/' + stock + '/'

# generating andicator data : input1: data folder input2: output folder
ichi(data_folder + stock, output_folder + stock)
rsi(data_folder + stock, output_folder + stock)
BB(data_folder + stock, output_folder + stock)
P_SAR(data_folder + stock, output_folder + stock)
ma(9, data_folder + stock, output_folder + stock)
ma(200, data_folder + stock, output_folder + stock)
