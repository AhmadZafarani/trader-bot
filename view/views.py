# YA MOHAMMAD
def view_strategy_results(strategy_results: list):
    with open('strategy results.txt', 'w') as file:
        file.writelines(strategy_results)


def view_balance(balance: list):
    with open('balance report.txt', 'w') as file:
        file.write('Dollar Balance, Bitcoin Balance\n')
        for b in balance:
            file.write(f'{b[0]}, {b[1]}\n')


def view_daily_results(daily_results: list):
    with open('daily report.txt', 'w') as file:
        file.write('Start Of Day Price, End Of Day Price, Delta Price, Report\n')
        for dr in daily_results:
            file.write(f'{dr[0]}, {dr[1]}, {dr[2]}, {dr[3]}\n')
