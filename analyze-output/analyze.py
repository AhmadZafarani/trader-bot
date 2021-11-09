import csv
import math
from sys import argv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

percent = []

inp = argv[1] if len(argv) > 1 else ""


def variance_expected(data: list) -> list:
    mean = sum(data) / len(data)
    res = sum((i - mean) ** 2 for i in data) / len(data)
    eee = math.sqrt(res)
    df1 = pd.read_csv("periodical_report.csv")
    final = df1.iloc[-1][' End Of Period Balance']
    return [round(mean, 4), round(eee, 4), round((final - 100000) / 1000, 2)]


def open_output_and_calculate_variance_expected():
    try:
        with open('periodical_report.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line = 0
            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue
                percent.append(float(row[4]))
                line += 1

        s = variance_expected(percent)
        return s
    except FileNotFoundError:
        return [0, 0]


v_e = open_output_and_calculate_variance_expected()
print(str(v_e)[1:-1])

if inp != "only-print":
    xpoints = np.array(range(0, len(percent)))
    ypoints = np.array(percent)
    plt.plot(xpoints, ypoints, 'o', xpoints,
             v_e[0] * np.ones((len(percent), 1)), 'r', xpoints, np.ones((len(percent), 1)), 'g')

    plt.grid()
    plt.show()
