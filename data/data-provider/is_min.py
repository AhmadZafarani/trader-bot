# this file will generate a csv file 
# lenght of this csv file is the same with candles
# each row is 1 if it is the minimum ow 0 



import csv
import matplotlib.pyplot as plt
import numpy as np


input_file = "data/BTC_FULL_MACD.csv"
output_file = "/Internal/Projects/Crypto/trader-bot/data/BTC_FULL_MACD_is_min.csv"
name = "close_is_min"
source = 0 # high low open close (1 2 3 4) | 0 if it is indicator
# csv_output_file = open(output_file , mode='w')




csv_file = open(input_file)
csv_reader = csv.reader(csv_file)
print(list(csv_reader)[0])
print(type(csv_reader))
next(csv_reader)
print(list(csv_reader)[0])

# print(len(list(csv_reader)))
# next(csv_reader)
# close_price = []
# for row in csv_reader:
#     close_price.append(float(row[source]))


# is_min = []
# csv_output_file = open(output_file , mode='w')
# csv_writer = csv.writer(csv_output_file)
# csv_writer.writerow("is_min")
# for i in range(len(close_price)) : 
#     if i==0 :
#         csv_writer.writerow('0')
#         is_min.append(0)
#         continue
#     elif i == len(close_price) -1 :
#         csv_writer.writerow('0')
#         is_min.append(0)
#         continue
#     elif close_price[i] <= close_price[i+1] and close_price[i] <= close_price[i-1]:
#         csv_writer.writerow('1')
#         is_min.append(1)
#     else : 
#         csv_writer.writerow('0')
#         is_min.append(0)








# xpoints = np.array(range(0, len(is_min)))
# plt.subplot(2, 1 ,  1)
# plt.plot(xpoints , close_price)

# plt.subplot(2, 1 ,  2)
# plt.scatter(xpoints , is_min)
# plt.show()

