# YA ZEYNAB
import logging

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


def check_view_essentials(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float):
    balance.append((dollar_balance, bitcoin_balance))
    __periodical_data(moment, moment_index, bitcoin_balance, dollar_balance)


def __periodical_data(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float):
    global start_of_period_balance, scenario
    e = dollar_balance + bitcoin_balance * moment.price

    if (moment_index - 1) % scenario.profit_loss_period_step == 0:
        start_of_period_balance = e
    elif (moment_index - 1) % (scenario.profit_loss_period_step - 1) == 0:
        p = round(e - start_of_period_balance, 4)
        sa = f'{round(p * 100 / start_of_period_balance, 4)}'
        periodical_results.append(
            (moment.date, start_of_period_balance, e, p, sa))


# ============= LOG CONTROL =========================================


def control_logs():
    logging.basicConfig(level=logging.DEBUG, filename=scenario.log_file_path,
                        filemode='w', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def log_debug(message: str):
    logging.debug(message)


def log_info(message: str):
    logging.info(message)


def log_warning(message: str):
    logging.warning(message)


def log_error(message: str):
    logging.error(message)
