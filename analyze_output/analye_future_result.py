import json
import pandas as pd
import pprint
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


for K in [20 ,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]:
    res = []
    curr, cnt = None, 0
    for chr in resultss:
        
        # increment for similar character
        if chr == curr:
            cnt += 1
        else:
            curr, cnt = chr, 1
            
        # if count exactly K, element is added
        if cnt == K:
            res.append(K * chr)
    
    if len(res) > 0: 
        if 'LOST' * K in res : 
            out["Consecutive_LOSTs"] = K
            break

print(f'''TOTAL : {out['TOTAL']}
ACCURACY : {out['Accuracy']}
WINs : {out['WINs']}
LOSTs : {out['LOSTs']}
Consecutive_LOSTs : {out['Consecutive_LOSTs']}
''')# print(json.dumps(dict(out) , indent=2))
# printing result

