import pandas as pd
import csv

fd = pd.read_csv("data/BTC_FULL_1h-time.csv")
data = fd.values

DMp = []
DMn = []
TR = []
Smoothed_DMp = []
Smoothed_DMn = []
Smoothed_TR = []
DIp = []
DIn = []
DX = []
ADX = []

# high low open close
for i in range(1, len(data)):
    previous_candle = data[i - 1]
    current_candle = data[i]
    Hc = current_candle[1]
    Hp = previous_candle[1]
    Lc = current_candle[2]
    Lp = previous_candle[2]
    Cp = previous_candle[4]
    if Hc - Hp > Lp - Lc:
        DMp.append(max(Hc - Hp, 0))
    else:
        DMp.append(0)
    if Lp - Lc > Hc - Hp:
        DMn.append(max(Lp - Lc, 0))
    else:
        DMn.append(0)
    # DMp.append(Hc - Hp > Lp - Lc ? max(Hc - Hp, 0): 0)
    # nz(low[1])-low > high-nz(high[1]) ? max(nz(low[1])-low, 0): 0
    TR.append(max((Hc - Lc), abs(Hc - Cp), abs(Lc - Cp)))

Smoothed_DMp.append(0.0)
Smoothed_DMn.append(0.0)
Smoothed_TR.append(0.0)

for i in range(1, len(DMp)):
    Current_S_DMp = Smoothed_DMp[i - 1] - (Smoothed_DMp[i - 1] / 14.0) + DMp[i]
    Current_S_DMn = Smoothed_DMn[i - 1] - (Smoothed_DMn[i - 1] / 14.0) + DMn[i]
    Current_S_TR = Smoothed_TR[i - 1] - (Smoothed_TR[i - 1] / 14.0) + TR[i]
    Smoothed_DMp.append(Current_S_DMp)
    Smoothed_DMn.append(Current_S_DMn)
    Smoothed_TR.append(Current_S_TR)

for i in range(1, len(Smoothed_DMp)):
    Current_DIp = (Smoothed_DMp[i] / Smoothed_TR[i]) * 100
    Current_DIn = (Smoothed_DMn[i] / Smoothed_TR[i]) * 100
    Current_DX = (abs(Current_DIp - Current_DIn) /
                  abs(Current_DIp + Current_DIn)) * 100
    DIp.append(Current_DIp)
    DIn.append(Current_DIn)
    DX.append(Current_DX)

sum_ADX = 0.0
for i in range(14):
    sum_ADX += DX[i]

ADX.append(sum_ADX / 14.0)

for i in range(14, len(DX)):
    sum_ADX = sum_ADX - DX[i - 14] + DX[i]
    ADX.append(sum_ADX / 14.0)

with open('data/BTC_FULL_ADX.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['adx', 'DI_plus', 'DI_minus'])
    for i in range(len(data)):
        if i < 2:
            writer.writerow([0, 0, 0])
        else:
            if i < 16:
                writer.writerow(
                    [0.0, round(DIp[i - 2], 2), round(DIn[i - 2], 2)])
            else:
                writer.writerow(
                    [round(ADX[i - 15], 2), round(DIp[i - 2], 2), round(DIn[i - 2], 2)])
