# YA MOHAMMAD
from pathlib import Path

result_folder = Path("results")


def view_strategy_result(strategy_result: str):
    with open(result_folder / 'strategy_results.txt', 'a') as file:
        file.write(strategy_result + '\n')


def view_live_balance(balance: tuple):
    with open(result_folder / 'balance_report.csv', 'a') as file:
        file.write(f'{balance[0]}, {balance[1]}\n')


def view_periodical_result(periodical_result: list):
    with open(result_folder / 'periodical_report.csv', 'a') as file:
        file.write(f'{periodical_result[0]}, {periodical_result[1]}, {periodical_result[2]}, {periodical_result[3]},'
                   f' {round(float(100 * periodical_result[3] / periodical_result[1]), 4)}\n')


def start_live_view():
    result_folder.mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)

    with open(result_folder / 'balance_report.csv', 'w') as file:
        file.write('Dollar Balance, Crypto Balance\n')
    with open(result_folder / 'periodical_report.csv', 'w') as file:
        file.write('Date, Start Of Period Balance, End Of Period Balance, Delta Balance, delta percentage\n')


def log_cndl_mmnt(logger, moment, candles):
    log_string = f'''C[0] : {candles[moment.candle_id - 1]}
         M : {moment}'''
    logger.info(log_string)
