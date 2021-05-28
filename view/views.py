# YA MOHAMMAD
def view_strategy_results(strategy_results: list):
    with open('strategy_results.txt', 'w') as file:
        file.writelines(strategy_results)


def view_balance(balance: list):
    with open('balance_report.csv', 'w') as file:
        file.write('Dollar Balance, Bitcoin Balance\n')
        for b in balance:
            file.write(f'{b[0]}, {b[1]}\n')


def view_daily_results(daily_results: list):
    with open('daily_report.csv', 'w') as file:
        file.write('Date, Start Of Day Balance, End Of Day Balance, Delta Balance,  ( delta percentage)\n')
        for dr in daily_results:
            file.write(f'{dr[0]}, {dr[1]}, {dr[2]}, {dr[3]} , {round(float(100 * dr[3] / dr[1]) , 4)}\n')
