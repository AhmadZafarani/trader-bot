import csv
import os
import shutil
from pathlib import Path
import unicodedata

import pandas as pd
import pytse_client as tse

raw_data_dir = "tickers_data"
output_data_dir = "data_dir"


if not os.path.exists(raw_data_dir):
    stocks = tse.download(symbols="all", write_to_csv=True, adjust=True)

dirpath = Path(output_data_dir)
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)
dirpath.mkdir()

for filename in os.listdir(raw_data_dir):
    data = pd.read_csv(os.path.join(raw_data_dir, filename))
    try:
        if '2022' in data.iloc[-1]['date']:
            filename = filename.replace('.csv', '')
            english_letters = []
            for l in filename:
                english_letters.append(''.join(unicodedata.name(l).split()[2:]))
            filename = '_'.join(english_letters) + '.csv'
            with open(dirpath / filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['date', 'high', 'low', 'open', 'close', 'volume'])
                for i in range(len(data)):
                    date = data.iloc[i][0].replace('-', '')
                    writer.writerow([date, data.iloc[i][2], data.iloc[i][3],
                                    data.iloc[i][1], data.iloc[i][9], data.iloc[i][5]])
    except IndexError:
        pass
