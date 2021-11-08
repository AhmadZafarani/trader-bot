# YA ZEYNAB
from model.Position import Position
from view.views import *
from model.Moment import Moment
from scenario import scenario
start_of_period_balance = 0
periodical_results = []
balance = []


def control_views(strategy_results: list):
    view_balance(balance)
    view_strategy_results(strategy_results)
    view_periodical_results(periodical_results)


def check_view_essentials(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float , future_balacne : int , position : Position):
    if scenario.mode == 'spot':
        balance.append((dollar_balance, bitcoin_balance , moment.timestamp))
    elif scenario.mode == 'future':
        balance.append((future_balacne, str(position) , moment.timestamp))
    
    periodical_data(moment, moment_index, bitcoin_balance, dollar_balance)


def periodical_data(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float):
    global start_of_period_balance, scenario
    if scenario.mode == 'spot' :
        e = dollar_balance + bitcoin_balance * moment.price
    elif scenario.mode == 'future':
        e = moment.future_liquidity 
    if (moment_index - 1) % scenario.profit_loss_period_step == scenario.profit_loss_period_step - 1:
        p = round(e - start_of_period_balance, 5)
        sa = f'{round(p * 100 / start_of_period_balance, 5)}'
        periodical_results.append(
            (f'{moment.date} {moment.hour}:{moment.minute}', start_of_period_balance, e, p, sa))


def view_before_trade(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float) -> bool:
    global start_of_period_balance
    if (moment_index - 1) % scenario.profit_loss_period_step != 0:
        return False
    if scenario.mode == 'spot' :
        start_of_period_balance = dollar_balance + bitcoin_balance * moment.price
    elif scenario.mode == 'future':
        start_of_period_balance = moment.future_liquidity 
    return True
