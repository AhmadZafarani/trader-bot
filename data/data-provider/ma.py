import csv


def moving_avrage(len: int, price_list: list):
    ma = []
    i = 0
    for cl in price_list:
        if i < len-1:
            sum = 0
            for cll in price_list[0:i+1]:
                sum += cll
            # ma.append(round(sum/(i+1), 3))
            ma.append(0)

        if i >= len-1:
            sum = 0
            for cll in price_list[i - len + 1:i+1]:
                sum += cll
            ma.append(round(sum/(len), 2))
        i += 1
    return ma


close_price = []
with open('data/BTC_new_1h-time.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        close_price.append(float(row[4]))
# print(close_price)

# moving_12 = moving_avrage(12, close_price)
moving_9 = moving_avrage(9, close_price)

with open('data/BTC_FULL_1h_MA9.csv', mode='w') as ma_12file:
    ma12 = csv.writer(ma_12file)
    ma12.writerow(['ma9'])
    for m in moving_9:
        ma12.writerow([str(m)])
