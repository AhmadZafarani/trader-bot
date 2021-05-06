import csv

def variance_expected(datas : list) -> list : 
    mean = sum(datas) / len(datas)
    res = sum((i - mean) ** 2 for i in datas) / len(datas)
    return([mean , res])



datas = []
with open('daily_report.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line = 0 
    for row in csv_reader:
        if line == 0 :
            line += 1
            continue
        datas.append(float(row[3]))
        line += 1

print(datas)