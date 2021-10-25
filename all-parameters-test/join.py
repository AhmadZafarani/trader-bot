import pandas as pd 

inputs = pd.read_csv('all-parameters-test/test-inputs-1.csv')
outs = pd.read_csv('all-parameters-test/test-variance-and-expected-1.csv')

combs = pd.concat([inputs, outs], axis=1)

combs.to_csv('all-parameters-test/final.csv' , index=False)
