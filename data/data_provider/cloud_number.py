import csv
import pandas as pd 

def cloud_number_generateor(ichi_file : str , out : str):
    ichi_df = pd.read_csv("data/" + ichi_file + "_ICHI.csv")
    lead1 = list(ichi_df.loc[: , "leading_line1"])
    lead2 = list(ichi_df.loc[: , "leading_line2"])
    # print(lead1)
    # return 0 
    n = 0
    final = []
    for i in range(len(lead1)):
        if i <= 75 :
            final.append(-1)
            continue
        if lead1[i] > lead2[i] and lead1[i-1] <= lead2[i-1] :
            n += 1
        elif lead1[i] < lead2[i] and lead1[i-1] >= lead2[i-1] :
            n += 1
        
        final.append(n)

    final = pd.DataFrame(final , columns=['cloud_number'])
    final.to_csv("data/" + out + "_Cloud_num.csv" , index=False)
    
        
cloud_number_generateor("forex_data/EURO_USD_2021/EUROUSD" , 'forex_data/EURO_USD_2021/EUROUSD')