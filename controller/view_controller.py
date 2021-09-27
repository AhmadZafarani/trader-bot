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


def __periodical_data(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float) -> bool:
    global start_of_period_balance, scenario
    e = dollar_balance + bitcoin_balance * moment.price

    if (moment_index - 1) % scenario.profit_loss_period_step == scenario.profit_loss_period_step - 1:
        p = round(e - start_of_period_balance, 4)
        sa = f'{round(p * 100 / start_of_period_balance, 4)}'
        periodical_results.append(
            (f'{moment.date} {moment.hour}:{moment.minute}', start_of_period_balance, e, p, sa))
        return True
    return False


def view_before_trade(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float) -> bool:
    global start_of_period_balance
    if (moment_index - 1) % scenario.profit_loss_period_step != 0:
        return False
    start_of_period_balance = dollar_balance + bitcoin_balance * moment.price
    return True


def control_live_view(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float, strategy_results: list):
    global start_of_period_balance

    t = (dollar_balance, bitcoin_balance)
    view_balance(t)

    if (moment_index - 1) % scenario.profit_loss_period_step == 0:
        start_of_period_balance = dollar_balance + bitcoin_balance * moment.price
    else:
        end_of_period = __periodical_data(moment, moment_index,
                          bitcoin_balance, dollar_balance)
        if end_of_period:
            view_periodical_result(periodical_results[-1])

    if len(strategy_results) > 0:
        view_strategy_result(strategy_results[-1])
        strategy_results.pop()


def control_start_live_view():
    start_live_view()


# ============= LOG CONTROL =========================================


def setup_logger(logger_name: str, log_file: str, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


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
