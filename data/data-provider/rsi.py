import csv
import pandas as pd


def sma(len: int, price_list: list):
    ma = []
    i = 0
    for cl in price_list:
        # print(price_list[i])
        if i < len - 1:
            sum = 0
            for cll in price_list[0:i + 1]:
                sum += cll
            ma.append(round(sum / (i + 1), 3))
            # print('neg' , round( sum/(i+1) , 2))

        if i >= len - 1:
            sum = 0
            # print(price_list[i - len +1:i+1])
            for cll in price_list[i - len + 1:i + 1]:
                sum += cll
                # print(sum)
            ma.append(round(sum / (len), 3))
            # print('pos', round(sum/(len) , 2))
        i += 1
    return (ma)


def rma(l: int, price: list):
    out = []
    k = 1.0 / l
    out.extend(sma(l, price[0:l]))
    for i in range(l, len(price)):
        current_ema = k * price[i] + (1 - k) * out[i - 1]
        out.append(current_ema)
    return out


fd = pd.read_csv('data/fameli-time.csv')
data0 = fd.values
data = []
for i in range(len(data0)):
    data.append(data0[i][4])

l = int(input("len: "))

up_data = []
down_data = []
up_data.append(data[0])
down_data.append(data[0])

for i in range(1, len(data)):
    up_data.append(max(data[i] - data[i - 1], 0.0))
    down_data.append(-min(data[i] - data[i - 1], 0.0))

up = rma(l, up_data)
down = rma(l, down_data)

rsi = []
for i in range(len(data)):
    if down[i] == 0.0:
        rsi.append(100.0)
    else:
        if up[i] == 0.0:
            rsi.append(0.0)
        else:
            rsi.append(100 - (100.0 / (1.0 + up[i] / down[i])))

with open('data/Fameli_RSI.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['rsi'])
    for i in range(len(data)):
        writer.writerow([round(rsi[i], 3)])
