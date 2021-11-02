from cryptocompare import *
import csv


def h(c: str, ct: int, bs: int, out: str):
    # c = 'btc'
    # ct = 1627689600
    ct = ct - (ct % 3600)
    # bs = 1622419200
    bs = bs - (bs % 3600)
    data = []
    left_hours = int((ct - bs) / 3600) + 1

    while True:
        hold_data = []
        if left_hours > 1991:
            bs += 7167600 + 3600
            hold_data = get_historical_price_hour(
                c, 'USDT', 1991, toTs=bs, exchange='BINANCE')
            data.extend(hold_data)
            left_hours -= 1992
        else:
            hold_data = get_historical_price_hour(
                c, 'USDT', left_hours - 1, toTs=ct, exchange='BINANCE')
            data.extend(hold_data)
            break

    with open('data/'+out+'_moment.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'open', 'volume'])
        for line in data:
            if line.get('volumeto') == 0:
                continue
            # writer.writerow([line.get('time'), line.get('high'), line.get('low'), line.get('open'), line.get('close'), line.get('volumeto')])
            writer.writerow(
                [line.get('time')*1000, line.get('open'), line.get('volumeto')])
    with open('data/'+out+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['high', 'low', 'open', 'close', 'volume'])
        for line in data:
            if line.get('volumeto') == 0:
                continue

            writer.writerow([line.get('high'), line.get('low'), line.get(
                'open'), line.get('close'), line.get('volumeto')])
            # writer.writerow([line.get('time'), line.get('close'), line.get('volumeto')])
    with open('data/'+out+'-time.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time',  'high', 'low', 'open', 'close', 'volume'])
        for line in data:
            if line.get('volumeto') == 0:
                continue
            writer.writerow([line.get('time')*1000, line.get('high'), line.get('low'),
                             line.get('open'), line.get('close'), line.get('volumeto')])


h('btc', 1612137600, 1609459200, 'test')
