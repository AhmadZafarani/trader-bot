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

l = int(input("enter len: "))

fd = pd.read_csv("btc1h.csv")
data0 = fd.values
data = []
for i in range(len(data0)):
    data.append(data0[i][4])

ema_data = ema(l, data)
print(ema_data)
with open('ema.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ema'])
    for line in ema_data:
        writer.writerow([line])

