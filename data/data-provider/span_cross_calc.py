import csv
# import matplotlib.pyplot as plt


def iscross(input: str, out: str):
    lead1 = []
    lead2 = []

    input_file = "data/" + input + "_ICHI.csv"
    output_file = "data/" + out + "_ISCROSS.csv"
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            lead1.append(float(row[3]))
            lead2.append(float(row[4]))
    is_cross = [0]
    is_cross_id = [1]
    for k in range(len(lead1)):
        if k <= 0:
            continue
        is_cross_id.append(k+1)
        if lead1[k] > lead2[k] and lead1[k-1] <= lead2[k-1]:
            is_cross.append(1)
            continue
        if lead2[k] > lead1[k] and lead2[k-1] <= lead1[k-1]:
            is_cross.append(1)
            continue
        is_cross.append(0)

    # print(is_cross)

    # plt.subplot(2,1,1)
    # plt.plot(is_cross_id , lead1 , 'b')
    # plt.plot(is_cross_id , lead2 , 'r')
    # plt.subplot(2,1,2)

    # plt.scatter(is_cross_id , is_cross)
    # plt.show()

    with open(output_file, mode='w') as outfile:
        snpan_cross = csv.writer(outfile)
        snpan_cross.writerow(['span_iscross'])
        for m in is_cross:
            snpan_cross.writerow([str(m)])


# iscross('test', 'test')