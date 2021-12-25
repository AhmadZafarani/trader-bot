import csv
import pandas as pd

iaf = 0.02 # float(input("enter start: "))  # usually 0.02
step = 0.02 # float(input("enter step: "))  # usually 0.2
maxaf = 0.2 # float(input("enter max: "))  # high or low or Open or close

fd = pd.read_csv('data/fameli-time.csv')

data0 = fd.values
low = []
high = []
Open = []
close = []
length = len(data0)

for i in range(len(data0)):
    high.append(data0[i][1])
    low.append(data0[i][2])
    Open.append(data0[i][3])
    close.append(data0[i][4])

bull = True
ep = low[0]
hp = high[0]
lp = low[0]
af = iaf
psar = []
psar.append(close[0])
psar.append(close[1])
for i in range(2, length):
    if bull:
        psar.append(psar[i - 1] + af * (hp - psar[i - 1]))
    else:
        psar.append(psar[i - 1] + af * (lp - psar[i - 1]))
    reverse = False
    if bull:
        if low[i] < psar[i]:
            bull = False
            reverse = True
            psar[i] = hp
            lp = low[i]
            af = iaf
    else:
        if high[i] > psar[i]:
            bull = True
            reverse = True
            psar[i] = lp
            hp = high[i]
            af = iaf
    if not reverse:
        if bull:
            if high[i] > hp:
                hp = high[i]
                af = min(af + step, maxaf)
            if low[i - 1] < psar[i]:
                psar[i] = low[i - 1]
            if low[i - 2] < psar[i]:
                psar[i] = low[i - 2]
        else:
            if low[i] < lp:
                lp = low[i]
                af = min(af + step, maxaf)
            if high[i - 1] > psar[i]:
                psar[i] = high[i - 1]
            if high[i - 2] > psar[i]:
                psar[i] = high[i - 2]


with open('data/Fameli_FULL_P_SAR.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['SAR'])
    for i in range(len(data0)):
        writer.writerow([round(psar[i], 3)])
