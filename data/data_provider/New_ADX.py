import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from ta.trend import ADXIndicator
# Load datas
df = pd.read_csv("data/BTC_2021/BTC-time.csv")
# Clean NaN values
# df = dropna(df)
df = add_all_ta_features(
    df, open="open", high="high", low="low", close="close", volume="volume")
# print(df['ADX'])

adx = ADXIndicator(df['high'] , df['low'], df['close'], 14 , True)
# # A = adx.adx()
frames = [adx.adx(), adx.adx_pos(), adx.adx_neg()]

final = pd.concat(frames , axis=1)
# print(pd.concat(frames , axis=1))
final.to_csv("data/BTC_2021/BTC_ADX.csv" , index=False , columns= ['adx', "DI_plus", "DI_minus"])