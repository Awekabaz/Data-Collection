import pandas as pd
import numpy as np
from datetime import datetime
import time
import requests

def scrape(url, name):
    rList = []
    temp = requests.get(url).json()['result']
        rList.extend(temp)
    while len(temp) >= 4500:
        temp = requests.get(f'{url}&end_time={temp[0]["time"]/1000}').json()['result']
            rList.extend(temp)
    df = pd.DataFrame(rList)
    df['time'] = pd.to_datetime(df.time, unit='ms')
    df.drop('startTime', axis=1,inplace=True)
    df.sort_values('time',inplace=True)
    df.drop_duplicates(inplace=True)
    df = df[['time', 'close']]
    df.columns = ['time', name]
    return df

perps = ['HT-PERP','TOMO-PERP']
dList = []
for i in range(len(perps)):
    url = 'https://ftx.com/api/markets/{}/candles?resolution=300&limit=5000'.format(perps[i])
    df = scrape(url, perps[i])
    dList.append(df)

dList = [a.set_index('time') for a in dfs]
data = dfs[0].join(dfs[1:])
data = data.dropna()
data.to_json('temp.json', orient='records', lines=True)
#data.to_json('temp.json', orient='index')
#data.to_json('temp.json', orient='split')
