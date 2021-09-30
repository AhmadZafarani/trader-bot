# YA HEYDAR
from csv import writer

"""
    change this variable corresponding to how much it took to run the main.py on your machine (calculate its ceil)
"""
run_time = 0.2
num_of_runs_in_colab = 12 * 3600 * int(1 / run_time)

"""
    modify below list in order to test different scenarios.
    it is a list of tuples: (VARIABLE NAME, LIST OF VALUES OF THAT VARIABLE)
    note that the variable name should be de defined in scenario.py
    and the values should all be generated and placed in a list
"""
test_variables_list = [
    # ('buy_method_line_to_line_options_line' , [[9,12], [9,26] ,[9,31] , [9,52], [12,26] , [12,31] , [12,52] , [26,31],[26,52],[31,52] ])
    # ("peridical_profit_loss_limit_enable" , [0,1]),
    # ("buy_method_price_to_line_enable" , [0,1]),
    # ("buy_method_line_to_line_enable" , [0,1]),
    # ("sell_method_price_to_line_enable" , [0,1]),
    # ("sell_method_line_to_line_enable" , [0,1]),
    # ("sell_method_profit_loss_limit" , [0,1])
    ("per_profit_limit", [1*x+10 for x in range(11)]),
    ("per_loss_limit", [-0.7 - 0.1*x for x in range(10)])
    # ("profit_loss_period_step" , [24 , 48 , 72 , 96 , 12 , 36 ])
    # ("loss_limit_per" , [-0.1 - 0.1 * x for x in range(20)])
    # ("volume_buy", list(range(20, 80, 10))),
    # ("lock_method", ["lock_to_fin", "lock_to_hour"]),
    # ("lock_hour", list(range(3, 10, 3))),
    # ("profit_limit", list(range(2, 15, 3))),
    # ("loss_limit", [-1, -2, -3, -4, -5]),
    # ("opening_intractions", [[0] + [int(x) for x in list(
    #     bin(m).replace("0b", "").zfill(3))] for m in range(8)]),
    # ("close_intraction", [[int(x) for x in list(
    #     bin(m).replace("0b", "").zfill(4))] for m in range(16)]),
    # ("min_slope_dif", [x*0.02+0.04 for x in range(16)]),
    # ("under_cloud_condition2", [x*0.01+0.01 for x in range(10)]),
    # ("next_candle_lenght_min", [x*0.2-2 for x in range(20)]),
    # ("closing_con1_min", [x*10+9 for x in range(10)]),
    # ("ten_kij_dif_max_then_kij", list(range(1, 6))),
    # ("closing_con1_red_candle", [0, 1])
]

test_variables_size = len(test_variables_list)
number_of_tests = 1
for i in range(test_variables_size - 1, -1, -1):
    number_of_tests *= len(test_variables_list[i][1])
files_num = number_of_tests // num_of_runs_in_colab + 1

files = iter(
    [open(f"all-parameters-test/sed-commands-{i}.txt", "w") for i in range(1, files_num + 1)])
csv_files = iter(
    [open(f"all-parameters-test/test-inputs-{i}.csv", "w") for i in range(1, files_num + 1)])
file = next(files)
csv_file = next(csv_files)

csv_writer = writer(csv_file)
headers = [h[0] for h in test_variables_list]
csv_writer.writerow(headers)

i = 0
test_variables_index = [0] * test_variables_size
while i < number_of_tests:
    out = []
    for j in range(test_variables_size):  # construct the i th jaygasht
        v = test_variables_list[j][1][test_variables_index[j]]
        out.append(v)
    csv_writer.writerow(out)

    string = ""
    for j in range(len(out)):  # construct sed commands regarding to 'out'
        if isinstance(out[j], str):
            string = string + \
                f'sed -i "s/\\\\({headers[j]} = \\\\).*/\\\\1\\\\\"{out[j]}\\\\\"/" scenario.py' + ';'
        else:
            string = string + \
                f'sed -i "s/\\\\({headers[j]} = \\\\).*/\\\\1{out[j]}/" scenario.py' + ';'
    file.write(string + '\n')

    for j in range(test_variables_size - 1, -1, -1):  # indices of next jaygasht
        test_variables_index[j] = (
            test_variables_index[j] + 1) % len(test_variables_list[j][1])
        if test_variables_index[j] != 0:
            break

    i += 1

    if i % num_of_runs_in_colab == 0:
        file.close()
        csv_file.close()
        file = next(files)
        csv_file = next(csv_files)
        csv_writer = writer(csv_file)
        csv_writer.writerow(headers)

file.close()
csv_file.close()
