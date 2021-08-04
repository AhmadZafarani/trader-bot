import csv
import pandas as pd
import math


def moving_avrage(len: int, price_list: list):
    ma = []
    i = 0
    for cl in price_list:
        if i < len - 1:
            sum = 0
            for cll in price_list[0:i + 1]:
                sum += cll
            ma.append(round(sum / (i + 1), 3))

        if i >= len - 1:
            sum = 0
            for cll in price_list[i - len + 1:i + 1]:
                sum += cll
            ma.append(round(sum / (len), 3))
        i += 1
    return ma


length = 20 # int(input("enter lenght: "))  # usually 20

sdev = 2 # int(input("enter standard dev: "))  # usually 2
source = 3 # int(input("enter source: "))  # high or low or open or close

fd = pd.read_csv("data/BTC_FULL_1h-time.csv")
data0 = fd.values
data = []
for i in range(len(data0)):
    data.append(data0[i][source + 1])

ma = moving_avrage(length, data)

div = []

for i in range(length - 1):
    div.append(0)

for i in range(length - 1, len(data)):
    sum = 0.0
    for j in range(length):
        sum += math.pow(data[i - j] - ma[i], 2.0)
    div.append(math.sqrt(sum / float(length)))

BUP = []
BDOWN = []

for i in range(length - 1):
    BDOWN.append(0)
    BUP.append(0)

for i in range(length - 1, len(data)):
    hold = sdev * div[i]
    BUP.append(ma[i] + hold)
    BDOWN.append(ma[i] - hold)

with open('data/BTC_FULL_BB.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['time', 'BUP', 'MA', 'BDOWN'])
    for i in range(len(data)):
        writer.writerow([data0[i][0], round(BUP[i], 3), ma[i], round(BDOWN[i], 3)])

