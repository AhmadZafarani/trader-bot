from forexconnect import fxcorepy, ForexConnect
from datetime import datetime
from datetime import timezone
import csv
import time
from dateutil.relativedelta import relativedelta

# d = datetime.strptime("10.06.2021 00:00:00", '%m.%d.%Y %H:%M:%S').replace(tzinfo=timezone.utc)
# print(time.mktime(d.timetuple()))
# d = d + relativedelta(months=1)
# print(d.strftime('%d/%m/%Y'))

fx = ForexConnect()
fx.login("D291167397", "hBgw3", "fxcorporate.com/Hosts.jsp", "Demo")

def forex_data(pair: str, current_time, base_time, output: str):
    
    data0 = fx.get_history(pair, "H1", base_time, current_time)

    data = []

    for i in range(len(data0)):
        hold = []
        hold.append(str(data0[i][0]))
        hold.append((data0[i][2] + data0[i][6]) / 2.0) #high
        hold.append((data0[i][3] + data0[i][7]) / 2.0) #low
        hold.append((data0[i][1] + data0[i][5]) / 2.0) #open
        hold.append((data0[i][4] + data0[i][8]) / 2.0) #close
        hold.append(data0[i][9])
        data.append(hold)

    for i in range(len(data)):
        dt = datetime.strptime(data[i][0], "%Y-%m-%dT%H:%M:%S.000000000")
        data[i][0] = dt.replace(tzinfo=timezone.utc).timestamp()

    with open('data/' + output + '-time.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'high', 'low', 'open', 'close', 'volume'])
        for line in data:
            if line[5] == 0:
                continue
            writer.writerow([int(line[0]) * 1000, round(line[1], 6), round(line[2], 6),
                            round(line[3], 6), round(line[4], 6), round(line[5], 6)])

    with open('data/' + output + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['high', 'low', 'open', 'close', 'volume'])
        for line in data:
            if line[5] == 0:
                continue
            writer.writerow([round(line[1], 6), round(line[2], 6),
                            round(line[3], 6), round(line[4], 6), round(line[5], 6)])

    with open('data/' + output + '-moment.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'open', 'volume'])
        for line in data:
            if line[5] == 0:
                continue
            writer.writerow(
                [int(line[0]) * 1000, round(line[3], 6), round(line[5], 6)])