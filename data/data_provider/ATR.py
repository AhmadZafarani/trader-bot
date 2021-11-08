import pandas as pd
import csv

fd = pd.read_csv("data/forex_data/EURUSD-time.csv")
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

ATR.append(TR[0])
for i in range(1, len(data)):
    current_atr = (ATR[i-1] * (length - 1) + TR[i]) / length
    ATR.append(current_atr)

with open('data/forex_data/EURUSD_ATR.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['atr'])
    for i in range(len(data)):
        writer.writerow([round(ATR[i] , 5)])
