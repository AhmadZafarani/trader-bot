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


def ema(l: int, price: list):
    out = []
    k = 2.0 / (l + 1)
    out.extend(sma(l, price[0:l]))
    for i in range(l, len(price)):
        current_ema = k * price[i] + (1 - k) * out[i - 1]
        out.append(current_ema)
    return out


fd = pd.read_csv("data/BTC_FULL_1h.csv")
data0 = fd.values
data = []
for i in range(len(data0)):
    data.append(data0[i][4])

fast_len = 12
slow_len = 26
signal_len = 9

fast_ema = ema(fast_len, data)
slow_ema = ema(slow_len, data)

macd = []

for i in range(len(fast_ema)):
    macd.append(fast_ema[i] - slow_ema[i])

signal_ema = ema(signal_len, macd)

with open('/Internal/Projects/Crypto/trader-bot/data/BTC_FULL_MACD.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['madc', 'signal', 'histogram'])
    for i in range(len(data)):
        writer.writerow([round(macd[i], 2), round(
            signal_ema[i], 2), round(macd[i] - signal_ema[i], 2)])
