import json
import pandas as pd
import pprint
import numpy as np
results = open('strategy_results.json')
out = {}
results = json.load(results)
df = pd.DataFrame(results)

# print(df["result"].value_counts().WIN)
out["TOTAL"] = len(results)
out['WINs'] = df["result"].value_counts().WIN
out['LOSTs'] = df["result"].value_counts().LOST
out['Accuracy'] = round(out['WINs'] / out['TOTAL'] , 2)
resultss = list(df['result'])
# print(results)

Max_Consecutive_LOSTs = 0
kk = 0
array_of_lostss = []
for result in results : 
    if result['result'] == 'LOST' : 
        kk += 1
    if result['result'] == 'WIN' :
        array_of_lostss.append({'number' : kk , 'ends_in' : result['more']['Date']['Entrance']})
        kk = 0

array_of_losts = [x['number'] for x in array_of_lostss ]
array_of_ends_in =  [x['ends_in'] for x in array_of_lostss ]
Max_Consecutive_LOSTs = max(array_of_losts)
close_via_cross = 0
close_via_cross_win = 0
close_via_cross_loss = 0 
for result in results : 
    if result['more']['close_via_cross'] : 
        close_via_cross += 1 
        if result['result'] == 'WIN' :
            close_via_cross_win += 1
        elif result['result'] == 'LOST' : 
            close_via_cross_loss += 1

# print(Max_Consecutive_LOSTs)
print(f'''TOTAL : {out['TOTAL']}
ACCURACY : {out['Accuracy']}
WINs : {out['WINs']}
LOSTs : {out['LOSTs']}
Consecutive_LOSTs : {Max_Consecutive_LOSTs}''')# print(json.dumps(dict(out) , indent=2))
print(f'Max_Consecutive_LOSTs ends in : {array_of_ends_in[array_of_losts.index(Max_Consecutive_LOSTs)]}')
# printing result
print(f'close_via_cross:{close_via_cross} (WIN : {close_via_cross_win})')


# Special_analyze 1 
df2 = pd.DataFrame(list(df['more']))
sls = np.array(pd.DataFrame(list(df2['Risk_Managment']))['stop_loss']) # stop_losses
entry_prices = np.array(df['entry_price'])
sl_percentage = np.round(100 *np.abs((sls - entry_prices) / entry_prices ) , 2)
resultsss = np.array(df['result'])

print(np.mean(sl_percentage))
print(np.var(sl_percentage))
# data = {"sl_percentage" : list(sl_percentage) , "winorlost" : list(resultsss)}
# print(data)