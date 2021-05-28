import csv
import math
import matplotlib.pyplot as plt
import numpy as np


def variance_expected(datas: list) -> list:
    mean = sum(datas) / len(datas)
    res = sum((i - mean) ** 2 for i in datas) / len(datas)
    eee = math.sqrt(res)
    return([mean, eee])


percent = []
with open('daily_report.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue
        percent.append(float(row[4]))
        line += 1

s = variance_expected(percent)
print(variance_expected(percent))
xpoints = np.array(range(0, len(percent)))
ypoints = np.array(percent)
plt.plot(xpoints, ypoints, 'o', xpoints,
         s[0]*np.ones((len(percent), 1)), 'r', xpoints, np.ones((len(percent), 1)), 'g')

plt.grid()
plt.show()
