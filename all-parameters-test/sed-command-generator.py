# YA HEYDAR
from csv import writer
"""
    modify below list in order to test different scenarios.
    it is a list of tuples: (VARIABLE NAME, LIST OF VALUES OF THAT VARIABLE)
    note that the variable name should be de defined in scenario.py
    and the values should all be generated and placed in a list
"""


test_variables_list = [
    ("volume_buy", list(range(20, 80, 10))),
    ("lock_method", ["lock_to_fin", "lock_to_hour"]),
    ("lock_hour", list(range(3, 10, 3))),
    ("profit_limit", list(range(2, 15, 3))),
    ("loss_limit", [-1, -2, -3, -4, -5]),
    ("opening_intractions", [[int(x) for x in list(
        bin(m).replace("0b", "").zfill(4))] for m in range(16)]),
    ("close_intraction", [[int(x) for x in list(
        bin(m).replace("0b", "").zfill(5))] for m in range(32)]),
]

test_variables_size = len(test_variables_list)
number_of_tests = 1
for i in range(test_variables_size - 1, -1, -1):
    number_of_tests *= len(test_variables_list[i][1])

file = open("sed-commands.txt", "w")
csv_file = open("test-output-analyzed.csv", "w")
csv_writer = writer(csv_file)
headers = [h[0] for h in test_variables_list]
csv_writer.writerow(headers + ["expected", "variance"])

i = 0
test_variables_index = [0] * test_variables_size
while i < number_of_tests:
    out = []
    for j in range(test_variables_size):        # construct the i th jaygasht
        v = test_variables_list[j][1][test_variables_index[j]]
        out.append(v)
    csv_writer.writerow(out)

    string = ""
    for j in range(len(out)):       # construct sed commands regarding to 'out'
        if isinstance(out[j], str):
            string = string + \
                f'sed -i "s/\({headers[j]} = \).*/\\1\"{out[j]}\"/" scenario.py' + ';'
        else:
            string = string + \
                f'sed -i "s/\({headers[j]} = \).*/\\1{out[j]}/" scenario.py' + ';'
    file.write(string + '\n')

    for j in range(test_variables_size - 1, -1, -1):        # indecies of next jaygasht
        test_variables_index[j] = (
            test_variables_index[j] + 1) % len(test_variables_list[j][1])
        if test_variables_index[j] != 0:
            break

    i += 1

file.close()
csv_file.close()
