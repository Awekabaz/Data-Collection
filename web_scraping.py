import requests 
from bs4 import BeautifulSoup 
import pandas as pd 
from urllib.request import urlopen

name=[]
price=[]
change=[]
change_percent=[]
market_cap=[]
total_volume=[]
circulating_supply=[]
 
for i in range(0,10):
  url = "https://in.finance.yahoo.com/cryptocurrencies?offset={}&count=50".format(i)
  page = urlopen(url)
  soup=BeautifulSoup(page, 'html.parser')
 
  for names in soup.find_all('td',{'aria-label':'Name'}):
    name.append(names.text)
  for prices in soup.find_all('td',{'aria-label':'Price (intraday)'}):
    price.append(prices.find('span').text)
  for changes in soup.find_all('td', {'aria-label':'Change'}):
    change.append(changes.text)
  for percent_changes in soup.find_all('td', {'aria-label':'% change'}):
    change_percent.append(percent_changes.text)
  for market_caps in soup.find_all('td', {'aria-label':'Market cap'}):
    market_cap.append(market_caps.text)
  for total_volumes in soup.find_all('td', {'aria-label':'Total volume all currencies (24 hrs)'}):
    total_volume.append(total_volumes.text)
  for circulating_s in soup.find_all('td', {'aria-label':'Circulating supply'}):
    circulating_supply.append(circulating_s.text)

zippedList =  list(zip(name,price,change,change_percent,market_cap,total_volume,circulating_supply))
ncolumns = ['name', 'price', 'change', '%change', 'market_cap', 'total_volume', 'circulating_supply']
dfObj = pd.DataFrame(zippedList, columns = ncolumns)

if(dfObj.isnull().values.any()):
  print('Missing data')
  dfObj.to_csv('temp.csv')
else:
  dfObj.to_json('temp.json', orient='records', lines=True)
  #dfObj.to_json('temp.json', orient='index')
  #dfObj.to_json('temp.json', orient='split')
  

  # Direct comprehension
  #dfObj.to_json('temp.json.gz', orient='records', lines=True, compression='gzip')




