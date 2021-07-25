
import csv
import matplotlib.pyplot as plt 
lead1 = []
lead2 = []
with open('data/BTC_FULL_ICHI.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        lead1.append(float(row[3]))
        lead2.append(float(row[4]))
is_cross = [0]
is_cross_id = [1]
for k in range(len(lead1)):
    if k <= 0 : continue
    is_cross_id.append(k+1)
    if lead1[k] > lead2[k] and lead1[k-1] <= lead2[k-1]:
        is_cross.append(18000)
        continue
    if lead2[k] > lead1[k] and lead2[k-1] <= lead1[k-1]:
        is_cross.append(18000)
        continue
    is_cross.append(0)

# print(is_cross)

# plt.subplot(2,1,1)
plt.plot(is_cross_id , lead1 , 'b')
plt.plot(is_cross_id , lead2 , 'r')
# plt.subplot(2,1,2)

plt.scatter(is_cross_id , is_cross )
plt.show()