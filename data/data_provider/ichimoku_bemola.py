import csv
import pandas as pd


def min_finder(data: list):
    minimum = data[0]
    for i in data:
        minimum = min(minimum, i)
    return minimum


def max_finder(data: list):
    maximum = data[0]
    for i in data:
        maximum = max(maximum, i)
    return maximum


def ichi(input: str, out: str):
    fd = pd.read_csv("data/" + input + "-time.csv")
    data = fd.values
    low_values = []
    high_values = []

    for i in range(len(data)):
        low_values.append(data[i][2])
        high_values.append(data[i][1])

    cll = 9  # int(input("Conversion line len: "))
    bsl = 26  # int(input("Base line len: "))
    lsl = 52  # int(input("Leading Span B len: "))
    lag = 26  # int(input("Lagging len: "))

    base_line = []
    conversion_line = []
    leading_line1 = []
    leading_line2 = []
    lagging_span = []

    for i in range(len(data)):
        if i < cll:
            minimum = min_finder(low_values[0:i + 1])
            maximum = max_finder(high_values[0:i + 1])
        else:
            minimum = min_finder(low_values[i - cll + 1:i + 1])
            maximum = max_finder(high_values[i - cll + 1:i + 1])
        conversion_line.append((maximum + minimum) / 2.0)

        if i < bsl:
            minimum = min_finder(low_values[:i + 1])
            maximum = max_finder(high_values[:i + 1])
        else:
            minimum = min_finder(low_values[i - bsl + 1:i + 1])
            maximum = max_finder(high_values[i - bsl + 1:i + 1])
        base_line.append((maximum + minimum) / 2.0)

        lagging_span.append(data[i][4])

    for i in range(len(data) + lag - 1):
        k = lag - 1
        if i < k:
            leading_line2.append(0)
            leading_line1.append(0)
            continue

        leading_line1.append((base_line[i - k] + conversion_line[i - k]) / 2.0)

        if i < lsl + k:
            minimum = min_finder(low_values[:i + 1 - k])
            maximum = max_finder(high_values[:i + 1 - k])
        else:
            minimum = min_finder(low_values[i - lsl + 1 - k:i + 1 - k])
            maximum = max_finder(high_values[i - lsl + 1 - k:i + 1 - k])
        leading_line2.append((maximum + minimum) / 2.0)

    # with open('/Internal/Projects/Crypto/trader-bot/data/BTC_FULL_1h_ichi1.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['conversion_line', 'base_line', 'lagging_span', 'leading_line1', 'leading_line2'])
    #     for i in range(lag):
    #         writer.writerow([0, 0, round(lagging_span[i], 3), 0, 0])
    #     for i in range(len(data) + lag - 1):
    #         if i < len(data) - lag + 1:
    #             writer.writerow([round(conversion_line[i], 3), round(base_line[i], 3), round(lagging_span[i + lag - 1], 3),
    #                              round(leading_line1[i], 3), round(leading_line2[i], 3)])
    #         elif i < len(data):
    #             writer.writerow([round(conversion_line[i], 3), round(base_line[i], 3), 0,
    #                              round(leading_line1[i], 3), round(leading_line2[i], 3)])
    #         else:
    #             writer.writerow([0, 0, 0, round(leading_line1[i], 3), round(leading_line2[i], 3)])

    with open('data/'+out + '_ICHI.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['conversion_line', 'base_line',
                         'lagging_span', 'leading_line1', 'leading_line2'])
        for i in range(len(data) + lag - 1):
            if i < len(data) - lag + 1:
                writer.writerow([round(conversion_line[i], 3), round(base_line[i], 3), round(lagging_span[i + lag - 1], 3),
                                 round(leading_line1[i], 3), round(leading_line2[i], 3)])
            elif i < len(data):
                writer.writerow([round(conversion_line[i], 3), round(base_line[i], 3), 0,
                                 round(leading_line1[i], 3), round(leading_line2[i], 3)])
            else:
                writer.writerow(
                    [0, 0, 0, round(leading_line1[i], 3), round(leading_line2[i], 3)])


ichi(input='BTC_2021/BTC', out='BTC_2021/BTC')
