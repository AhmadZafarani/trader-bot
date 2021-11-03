import pandas as pd
import csv

fd = pd.read_csv("data/BTC_2021/BTC-time.csv")
length = 14
data = fd.values
TR = []
ATR = []
TR.append(0.0)

# high low open close
for i in range(1, len(data)):
    previous_candle = data[i - 1]
    current_candle = data[i]
    Hc = current_candle[1]
    Hp = previous_candle[1]
    Lc = current_candle[2]
    Lp = previous_candle[2]
    Cp = previous_candle[4]
    TR.append(max((Hc - Lc), abs(Hc - Cp), abs(Lc - Cp)))

sum = 0.0
for i in range(len(data)):
    if i < 13:
        sum += TR[i]
        ATR.append(sum / (i + 1))
    else:
        sum = 0.0
        for k in range(14):
            sum += TR[i - k]
        ATR.append(sum / 14)

with open('data/BTC_2021/BTC_ATR.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['atr'])
    for i in range(len(data)):
        writer.writerow([ATR[i]])






