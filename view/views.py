# YA MOHAMMAD
def view_strategy_results(strategy_results: list):
    with open('strategy_results.txt', 'w') as file:
        file.writelines(strategy_results)


def view_balance(balance: list):
    with open('balance_report.csv', 'w') as file:
        file.write('Dollar Balance, Crypto Balance\n')
        for b in balance:
            file.write(f'{b[0]}, {b[1]}\n')


def view_periodical_results(periodical_results: list):
    with open('periodical_report.csv', 'w') as file:
        file.write(
            'Date, Start Of Period Balance, End Of Period Balance, Delta Balance, delta percentage\n')
        for pr in periodical_results:
            file.write(
                f'{pr[0]}, {pr[1]}, {pr[2]}, {pr[3]} , {round(float(100 * pr[3] / pr[1]), 4)}\n')


def view_strategy_result(strategy_result: str):
    with open('strategy_results.txt', 'a') as file:
        file.write(strategy_result + '\n')


def view_balance(balance: tuple):
    with open('balance_report.csv', 'a') as file:
        file.write(f'{balance[0]}, {balance[1]}\n')


def view_periodical_result(periodical_result: list):
    with open('periodical_report.csv', 'a') as file:
        file.write(
            f'{periodical_result[0]}, {periodical_result[1]}, {periodical_result[2]}, {periodical_result[3]} , {round(float(100 * periodical_result[3] / periodical_result[1]), 4)}\n')


def start_live_view():
    with open('balance_report.csv', 'w') as file:
        file.write('Dollar Balance, Crypto Balance\n')
    with open('periodical_report.csv', 'w') as file:
        file.write(
            'Date, Start Of Period Balance, End Of Period Balance, Delta Balance, delta percentage\n')
    with open('strategy_results.txt', 'w') as file:
        pass
