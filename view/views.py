# YA MOHAMMAD
def view_results(results: tuple):
    balance, strategy_results = results
    with open('balance report.txt', 'w') as file:
        for b in balance:
            file.write(f'{b[0]}, {b[1]}\n')

    with open('strategy results.txt', 'w') as file:
        file.writelines(strategy_results)
