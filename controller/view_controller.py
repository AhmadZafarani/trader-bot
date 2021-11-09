# YA ZEYNAB
import logging

from model.Moment import Moment
from scenario import scenario
from view.views import *

start_of_period_balance = 0
periodical_results = []


def __periodical_data(moment: Moment, moment_index: int, bitcoin_balance: float, dollar_balance: float) -> bool:
    global start_of_period_balance
    e = dollar_balance + bitcoin_balance * moment.price

    if (moment_index - 1) % scenario.profit_loss_period_step == scenario.profit_loss_period_step - 1:
        p = round(e - start_of_period_balance, 4)
        sa = f'{round(p * 100 / start_of_period_balance, 4)}'
        periodical_results.append(
            (f'{moment.date} {moment.hour}:{moment.minute}', start_of_period_balance, e, p, sa))
        return True
    return False


def control_live_view(loggers: tuple, candles: list, moment: Moment, moment_index: int, bitcoin_balance: float,
                      dollar_balance: float, strategy_results: list):
    global start_of_period_balance

    t = (dollar_balance, bitcoin_balance)
    view_live_balance(t)

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

    log_cndl_mmnt(loggers[0], moment, candles)


def control_start_live_view() -> tuple:
    setup_logger('cndl-mmnt-sync', r'logs/cndl-mmnt-sync.log',
                 level=logging.INFO)
    log1 = get_logger('cndl-mmnt-sync')

    setup_logger('strategy-logs', r'logs/strategy-logs.log',
                 level=logging.INFO, format_log='%(asctime)s - %(message)s')
    log2 = get_logger('strategy-logs')

    start_live_view()
    return log1, log2


# ============= LOG CONTROL =========================================
def setup_logger(logger_name: str, log_file: str, level=logging.INFO, format_log='%(message)s'):
    lg = logging.getLogger(logger_name)
    formatter = logging.Formatter(format_log)
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    lg.setLevel(level)
    lg.addHandler(file_handler)


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
