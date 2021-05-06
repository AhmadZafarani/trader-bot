
import csv
import matplotlib.pyplot as plt
import numpy as np

def moving_avrage(len : int , price_list:list):
    ma = []
    i = 0
    for cl in price_list:
        # print(price_list[i])
        if i < len-1:
            sum = 0 
            for cll in price_list[0:i+1]:
                sum += cll 
            ma.append(round( sum/(i+1) , 3))
            # print('neg' , round( sum/(i+1) , 2))
            
        if i >= len-1 :
            sum = 0
            # print(price_list[i - len +1:i+1])
            for cll in price_list[i - len +1:i+1]:
                sum += cll 
                # print(sum)
            ma.append(round(sum/(len) , 3))
            # print('pos', round(sum/(len) , 2))
        i += 1 
    return(ma)

close_price = []
with open('/Internal/Projects/Crypto/trader-bot/data/onehour.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        close_price.append(float(row[4]))
        # print(row[0])
print(close_price)

moving_12 = moving_avrage(12 , close_price)
moving_26 = moving_avrage(26 , close_price)
with open('ma_16_1h.csv', mode='w') as ma_12file:
    ma12 = csv.writer(ma_12file)
    for m in moving_26:
        ma12.writerow([str(m)])
        
    # employee_writer.writerow(['Erica Meyers', 'IT', 'March'])

# x = range(1 , 5601)
# xpoints = np.array(x)
# y1 = np.array(moving_26)
# y2 = np.array(moving_12)

# plt.plot(x , y1,  x , y2)
# plt.show()



# listd = [1 ,5 ,3, 5 ,7, 9, 98]
# mma = moving_avrage(3 ,listd )
# print(mma)