# YA ZEYNAB
from view.views import *
from model.Moment import Moment

start_of_day_balance = None
daily_results = []
balance = []


def control_views(strategy_results: list):
    view_balance(balance)
    view_strategy_results(strategy_results)
    view_daily_results(daily_results)


def check_view_essentials(moment: Moment, bitcoin_balance: float, dollar_balance: float):
    balance.append((dollar_balance, bitcoin_balance))
    daily(moment, bitcoin_balance, dollar_balance)


def daily(moment: Moment, bitcoin_balance: float, dollar_balance: float):
    global start_of_day_balance
    if moment.hour == 0 and moment.minute == 0 and start_of_day_balance is None:
        start_of_day_balance = dollar_balance + bitcoin_balance * moment.price
    elif moment.hour == 23 and moment.minute == 59:
        if start_of_day_balance is not None:
            e = dollar_balance + bitcoin_balance * moment.price
            p = round(e - start_of_day_balance, 4)
            if p < 0:
                s = f'{round((-p * 100) / start_of_day_balance, 4)} % Loss'
            else:
                s = f'{round(p * 100 / start_of_day_balance, 4)} % Profit'
            daily_results.append((start_of_day_balance, e, p, s))
            start_of_day_balance = None
