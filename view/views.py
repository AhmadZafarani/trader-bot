# YA MOHAMMAD
import json

from scenario import scenario
def view_strategy_results(strategy_results: list):
    with open('strategy_results.json', 'w') as json_file:
        json.dump(strategy_results, json_file , indent=2)


def view_balance(balance: list):
    with open('balance_report.csv', 'w') as file:
        if scenario.mode == 'spot':
            file.write('Dollar Balance, Crypto Balance, time\n')
        elif scenario.mode == 'future':
            file.write('Dollar Balance, Position, time\n')            
        for b in balance:
            file.write(f'{b[0]}, {b[1]}, {b[2]}\n')


def view_periodical_results(periodical_results: list):
    with open('periodical_report.csv', 'w') as file:
        file.write(
            'Date, Start Of Period Balance, End Of Period Balance, Delta Balance, delta percentage,time\n')
        for pr in periodical_results:
            file.write(
                f'{pr[0]}, {pr[1]}, {pr[2]}, {pr[3]} , {round(float(100 * pr[3] / pr[1]) , 4)}\n')
