import pytse_client as tse
import csv
import os
import pandas as pd
import time
import datetime
import scenario

stock = scenario.scenario.stock

def tse_data():
    stocks = tse.download(symbols="فملی", write_to_csv=True)
    for flag in stocks.keys():
        fd = pd.read_csv("tickers_data/" + flag + ".csv")
        data = fd.values
        try:
            os.mkdir("data/tse/" + flag + "/")
        except:
            print("problem")

        with open('data/tse/' + flag + '/' + flag + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['high', 'low', 'open', 'close', 'Volume'])
            for i in range(len(data)):
                date = time.mktime(datetime.datetime.strptime(
                    data[i][1], "%Y-%m-%d").timetuple())
                if data[i][6] == 0:
                    continue
                writer.writerow([int(date)*1000, data[i][3], data[i]
                                [4], data[i][2], data[i][10], data[i][6]])

        with open('data/tse/' + flag + '/' + flag + '-time.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'high', 'low', 'open', 'close', 'Volume'])
            for i in range(len(data)):
                date = time.mktime(datetime.datetime.strptime(
                    data[i][1], "%Y-%m-%d").timetuple())
                if data[i][6] == 0:
                    continue
                writer.writerow([int(date)*1000, data[i][3], data[i]
                                [4], data[i][2], data[i][10], data[i][6]])

        with open('data/tse/' + flag + '/' + flag + '-moment.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'open', 'Volume'])
            for i in range(len(data)):
                date = time.mktime(datetime.datetime.strptime(
                    data[i][1], "%Y-%m-%d").timetuple())
                if data[i][6] == 0:
                    continue
                writer.writerow([int(date)*1000, data[i][3], data[i]
                                [4], data[i][2], data[i][10], data[i][6]])

tse_data()
