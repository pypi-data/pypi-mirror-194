import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

from datetime import datetime as dt

from tvDatafeed import TvDatafeed, Interval

import seaborn as sns

################## ดึงข้อมูลจากตลาดหลักทรัพย์ ################
import requests

def getURL(symbol,typeurl):
    if(typeurl=='trading-stat'):
       return  'https://www.set.or.th/api/set/stock/'+symbol+'/company-highlight/trading-stat?lang=th'
    elif(typeurl=='financial'):
       return 'https://www.set.or.th/api/set/stock/'+symbol+'/company-highlight/financial-data?lang=th'
    elif(typeurl=='sector'):
       return 'https://www.settrade.com/api/set/stock/list'

def getRatio(symbol,ratio):
  # url จากตลาดหลักทรัพย์
  try:
    url = getURL(symbol,'trading-stat')
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data[-1][ratio]
  except:
    url = getURL(symbol,'financial')
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data[-1][ratio]    
    

def getRatio_info():
  # url จากตลาดหลักทรัพย์

  rp = []
  symbol = 'advanc'
  url = getURL(symbol,'trading-stat')
  headers = {'Accept': 'application/json'}
  r = requests.get(url, headers=headers)
  data = r.json()  
  for i in data[-1]:
    rp.append(i)
    
  url = getURL(symbol,'financial')
  headers = {'Accept': 'application/json'}
  r = requests.get(url, headers=headers)
  data = r.json()  
  for i in data[-1]:
    rp.append(i)
  
  return list(set(rp))

def getSector():
  url = getURL(symbol='',typeurl='sector')
  resp = requests.get(url=url)
  data = resp.json()
  data = pd.DataFrame.from_dict(data['securitySymbols'])
  df = data.groupby('querySector').mean()
  for i in df.index:
    if(i!=''):
      print(i,end=' ')

def getMemberOfSector(sector):
    url = getURL(symbol='',typeurl='sector')
    resp = requests.get(url=url)
    data = resp.json()
    data = pd.DataFrame.from_dict(data['securitySymbols'])
    df = data[(data['querySector']=='BANK') & (~data['symbol'].str.contains('-F'))]
    return df

def getIndustry():
  url = getURL(symbol='',typeurl='sector')
  resp = requests.get(url=url)
  data = resp.json()
  data = pd.DataFrame.from_dict(data['securitySymbols'])
  data = data[['industry','querySector']] 
  data = data[data['querySector']!='']
  data = data.groupby(['industry','querySector']).mean()
  return data
################## End ดึงข้อมูลจากตลาดหลักทรัพย์ ################


def monthlyReturn(symbol,month,engine,market='set',plot=True):
    df = engine.tv.get_hist(symbol=symbol,exchange=market,interval=Interval.in_monthly,n_bars=month)
    
    ######
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    
    df.Date = pd.to_datetime(df.Date)
    df['month'] = df.Date.dt.month.values
    df['year'] = df.Date.dt.year.values
    
    df['pct_change_'] = df.close.pct_change()
    df['pct_change_m'] = df['pct_change_'].shift(-1)
    
    df.drop(index=df.index[-1], 
        axis=0, 
        inplace=True)
    
    df = df.dropna()
    
    
    df['month_win'] = np.where(df.pct_change_m>=0,1,0)
    
    if(plot):
      df.groupby(df.month)['month_win'].sum().plot(kind='bar',title='monthly win')
      plt.show()
      df.groupby(df.index.month)['pct_change_m'].sum().plot(kind='bar',title='total monthly return')
        
  
      sns.set()  
      df = df.set_index('Date') 
      fig, ax = plt.subplots(figsize=(10,10))
      
      #rdgn = sns.diverging_palette(h_neg=130, h_pos=10, s=99, l=55, sep=3, as_cmap=True)
      season = df.pivot("month", "year", "pct_change_m")
      ax = sns.heatmap(season,center=0.00,cmap="PiYG",ax=ax)
      plt.title("Heatmap "+symbol+" Return")
      plt.show()  

    return df

def isset(nameVar):
    return nameVar in globals()

def rankWithRange(data,minScope,maxScope):
    basket = data.sort_values([data.columns[0]],ascending=False)

    basket['RANK'] = list(range(len(basket), 0,-1))
    maxRank = basket['RANK'].max()
    minRank = basket['RANK'].min()
    maxScope = maxScope
    minScope = minScope
    S = (minScope-maxScope)/(minRank-maxRank)
    Int = minScope - S*minRank
    basket['RS_Rank'] = basket['RANK']*S+Int  
    
    return basket

class HistStockPrice():
  def __init__(self):    
     self.tv = TvDatafeed()
    
  def days_between(self,d1, d2):
      d1 = dt.strptime(d1, "%Y-%m-%d")
      d2 = dt.strptime(d2, "%Y-%m-%d")
      return abs((d2 - d1).days)

  def getPrice(self,symbol,start,stop='',exchange='set'):
    
      date_now = dt.today().strftime("%Y-%m-%d") 
    
      if(stop==''):
        stop = date_now
    
      k = self.days_between(start, date_now)
    
      df = self.tv.get_hist(symbol=symbol,exchange=exchange,interval=Interval.in_daily,n_bars=k)
    
      df['Date'] = pd.to_datetime(df.index)
      df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
      df['Date'] = pd.to_datetime(df['Date'])

      df = df[['Date','close']]
      df = df.set_index('Date')
      df.columns = [symbol]
    
      df = df[(df.index>=start) & (df.index<=stop)]
      return df