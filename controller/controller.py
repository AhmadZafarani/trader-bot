# YA FATEMEH
import time
from csv import reader
from model.Candle import Candle
from model.Moment import Moment
import model.strategy as strategies
from controller.view_controller import control_views, check_view_essentials
import os

dollar_balance = 1000
bitcoin_balance = 0
this_moment = Moment(0, 0, '', 0  , 0 )
strategy_results = []
working_strategies = []


def data_converter(csv_file_name: str) -> list:
    candles = []
    movingfile = open('data/ma_12_1h.csv')
    movingcsv12 = reader(movingfile)
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)    # skip field names
        line_count = 1
        next(movingcsv12)  
        for row in csv_reader:
            fields = [f for f in row]
            moving12 = next(movingcsv12)
            cndl = Candle(line_count, int(fields[0]) // 1000, float(fields[1]),
                                  float(fields[2]), float(fields[3]), float(fields[4]), float(fields[5]),
                                  float(moving12[0]))
            # print(cndl.__str__)
            candles.append(cndl)
            line_count += 1
    return candles


def analyze_data(candles: list, csv_file_name: str):
    global this_moment, bitcoin_balance, dollar_balance
    with open(csv_file_name) as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        next(csv_reader)    # skip field names
        for c in candles:
            time1 = time.time()
            for i in range(60):  # the i th minute of hour
                price, volume = next(csv_reader)
                price = float(price)
                this_moment.update_moment(i, c.hour, c.date, price , c.identifier , candles)
                
                # if c.identifier == 102 :
                #     print(this_moment.moving12)
                # if c.identifier == 103 : 
                #     exit(0)
                try_strategies(this_moment , candles)
                check_view_essentials(this_moment, bitcoin_balance, dollar_balance)
            print('Analyzing :' , round(100 * c.identifier/len(candles) , 1),'%')
            # print(c.identifier)
            # time2 = time.time()
            # print(time2 - time1)
            # os.system("clear")
        control_views(strategy_results)


def try_strategies(moment: Moment , candles: list):
    global working_strategies,  bitcoin_balance, dollar_balance
    for ws in working_strategies:
        ws.continue_strategy()
    working_strategies = [ws for ws in working_strategies if ws.working]
    for s in strategies.strategies:
        if not s in strategies.lock_strategies:
            strtg = strategies.strategies[s](moment ,bitcoin_balance, dollar_balance , candles)
            if strtg.working:
                working_strategies.append(strtg)


def buy(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin_balance += bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    dollar_balance -= (bitcoin * price * 1.00075)
    # dollar_balance -= (bitcoin * price)

    # dollar_balance -= (bitcoin * price)
    dollar_balance = round(dollar_balance, 4)
    if dollar_balance < 0:
        raise RuntimeError('dollar balance is negative')


def sell(bitcoin: int, price: int):
    global bitcoin_balance, dollar_balance
    bitcoin_balance -= bitcoin
    bitcoin_balance = round(bitcoin_balance, 4)
    if bitcoin_balance < 0:
        raise RuntimeError('bitcoin balance is negative')
    dollar_balance += (bitcoin * price * 0.99925)
    # dollar_balance += (bitcoin * price)

    # dollar_balance += (bitcoin * price)
    dollar_balance = round(dollar_balance, 4)


def get_this_moment() -> Moment:
    return this_moment


def set_report(r: str):
    strategy_results.append(r)
