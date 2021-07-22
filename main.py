# YA HOSSEIN
from controller.controller import data_converter, analyze_data
from pathlib import Path
from time import time
from scenario import scenario, set_value
from analyzeOutput.analyze import open_output_and_calculate_variance_expected
from csv import writer

"""
    modify below list in order to test different scenarios.
    it is a list of tuples: (VARIABLE NAME, LIST OF VALUES OF THAT VARIABLE)
    note that the variable name should be de defined in scenario.py
    and the values should all be generated and placed in a list
"""
test_variables_list = [
    ("volume_buy", list(range(20, 80, 5))),
    ("lock_method", ["lock_to_fin", "lock_to_houre"]),
    ("lock_hour", list(range(3, 10, 2))),
    ("opening_con1_num_of_candles", [1, 2, 3]),
    ("opening_con1_min_first", list(range(1, 90, 20))),
    ("opening_con2_min_adx", list(range(10, 25, 2))),
    ("closing_meth1_num_of_candles", [1, 2]),
    ("closing_met2_max_adx", list(range(10, 25, 3))),
    ("profit_limit", list(range(2, 15, 2))),
    ("loss_limit", [-1, -2, -3, -4, -5]),
    ("intraction", [int('100', 2), int('110', 2), int('101', 2),
                    int('111', 2), int('010', 2), int('011', 2), int('001', 2)])
]


def main():
    start_time = time()
    # print('loading data...')

    data_folder = Path("data")
    candles_file = data_folder / scenario.candles_data_csv_file_name
    moments_file = data_folder / scenario.moment_data_csv_file_name

    extra_candle_files = {}
    for ecdf in scenario.extra_candles_data_files:
        extra_candle_files[ecdf] = data_folder / \
            scenario.extra_candles_data_files[ecdf]

    extra_moment_files = {}
    for emdf in scenario.extra_moments_data_files:
        extra_moment_files[emdf] = data_folder / \
            scenario.extra_moments_data_files[emdf]

    candles = data_converter(candles_file, extra_candle_files)
    # print('data loaded in : ', time() - start_time)

    analyze_data(candles, moments_file, extra_moment_files)

    print('total runtime : ', time() - start_time)


def test():
    test_variables_size = len(test_variables_list)
    number_of_tests = 1
    for i in range(test_variables_size - 1, -1, -1):
        number_of_tests *= len(test_variables_list[i][1])
    file = open("test-output-analyzed.csv", "w")
    file_writer = writer(file)
    headers = [h[0] for h in test_variables_list]
    headers.extend(["expected", "variance"])
    file_writer.writerow(headers)
    i = 0
    test_variables_index = [0] * test_variables_size
    while i < number_of_tests:
        out = []
        for j in range(test_variables_size):
            v = test_variables_list[j][1][test_variables_index[j]]
            out.append(v)
            set_value(test_variables_list[j][0], v)

        try:
            main()
            v_e = open_output_and_calculate_variance_expected()
            out.extend(v_e)
            file_writer.writerow(out)
            print('Analyzing :', round(100 * i / number_of_tests, 4), '%')
        except RuntimeError as e:
            print(e.args)

        for j in range(test_variables_size - 1, -1, -1):
            test_variables_index[j] = (
                test_variables_index[j] + 1) % len(test_variables_list[j][1])
            if test_variables_index[j] != 0:
                break
        i += 1
    file.close()


# inp = input(
#     "insert 1 for run the program in normal mode\nor insert 2 for run in test mode:\n")
inp = '2'
if inp == '1':
    main()
elif inp == '2':
    test()
else:
    raise ValueError("only hit 1 or 2 :|")
