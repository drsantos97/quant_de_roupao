#!/usr/bin/env python
# coding: utf-8

# In[47]:


import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt
import copy
import matplotlib.pyplot as plt


# In[48]:


def CAGR(x):
    df = x.copy()
    df['cum_return'] = (1+df['ret']).cumprod()
    n = len(df)/(252*84)
    CAGR = (df['cum_return'].tolist()[-1])**(1/n)-1
    return CAGR

def vol(x):
    df = x.copy()
    vol = df['ret'].std()*np.sqrt(252*84)
    return vol

def sharpe(x, rf):
    df = x.copy()
    sharpe = (CAGR(x)-rf)/vol(x)
    return sharpe

def max_dd(x):
    df = x.copy()
    df['cum_return'] = (1+df['ret']).cumprod()
    df['cum_return_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_return_max'] - df['cum_return']
    df['drawdown_pct'] = df['drawdown']/df['cum_return_max']
    max_dd = df['drawdown_pct'].max()
    return max_dd

def ATR(x,n):
    df = x.copy()
    df['H-L']=abs(df['High'] - df['Low'])
    df['H-PC']=abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC']=abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'], axis=1)
    return df2['ATR']


# In[49]:


#importando base
df_ibrx = pd.read_excel(r'C:\Users\drsan\OneDrive\Área de Trabalho\Python\ETFs_Onshore.xlsx',sheet_name = 'IBRX100')

# dando aquele tapa
df = df_ibrx
df = pd.DataFrame(df) 
df = df.dropna()
df['Part. (%)'] /= 100000
df.rename(columns={'Código\xa0':'Codigo'}, inplace = True)
df['Codigo'] = df['Codigo'] + ".SA"
tickers = df['Codigo']


# In[50]:


start = dt.date.today() + dt.timedelta(1) - dt.timedelta(59)
end = dt.date.today() + dt.timedelta(1)
prices = {}
for t in tickers:
    try:
        prices[t] = yf.download(t,start,end,interval='5m')
    except: 
        pass
    prices[t].dropna(how='all', inplace = True)


# In[51]:


prices2 = copy.deepcopy(prices)
tickers_signal = {}
tickers_ret = {}
for t in tickers:
    prices2[t]['ATR'] = ATR(prices2[t],20)
    prices2[t]['roll_max_cp'] = prices2[t]['High'].rolling(20).max()
    prices2[t]['roll_min_cp'] = prices2[t]['Low'].rolling(20).min()
    prices2[t]['roll_max_vol'] = prices2[t]['Volume'].rolling(20).max()
    prices2[t].dropna(inplace=True)
    tickers_signal[t] = ""
    tickers_ret[t] = []


# In[52]:


i = -45

for t in tickers:

    try:
        print('running'+t)

        if prices2[t].index[i].strftime("%d") != prices2[t].index[i+1].strftime("%d"):

            if tickers_signal[t] == "":
                tickers_ret[t].append(0)
            elif tickers_signal[t] == "Buy":
                tickers_ret[t].append((prices2[t]['Adj Close'][i]/prices2[t]['Adj Close'][i-1])-1)
            elif tickers_signal[t] == "Sell":
                tickers_ret[t].append((prices2[t]['Adj Close'][i-1]/prices2[t]['Adj Close'][i])-1)

            tickers_signal[t] == ""

        elif tickers_signal[t] == "":
            print("oi")
            tickers_ret[t].append(0)
            if prices2[t]['High'][i] >= prices2[t]['roll_max_cp'][i] and             prices2[t]['Volume'][i] > 0.5*prices2[t]['roll_max_vol'][i-1]:
                tickers_signal[t] = "Buy"
            elif prices2[t]['Low'][i] <= prices2[t]['roll_min_cp'][i] and             prices2[t]['Volume'][i] > 0.5*prices2[t]['roll_max_vol'][i-1]:
                tickers_signal[t] = "Sell"

        elif tickers_signal[t] == "Buy":
            if prices2[t]['Adj Close'][i] < prices2[t]['Adj Close'][i-1] - prices2[t]['ATR'][i-1]:
                tickers_signal[t] = ""
            elif prices2[t]['Low'][i] <= prices2[t]['roll_min_cp'][i] and             prices2[t]['Volume'][i] > 1.5*prices2[t]['roll_max_vol'][i-1]:
                tickers_signal[t] = "Sell"

            tickers_ret[t].append((prices2[t]['Adj Close'][i]/prices2[t]['Adj Close'][i-1])-1)

        elif tickers_signal[t] == "Sell":
            if prices2[t]['Adj Close'][i] > prices2[t]['Adj Close'][i-1] + prices2[t]['ATR'][i-1]:
                tickers_signal[t] = ""
            elif prices2[t]['High'][i] >= prices2[t]['roll_max_cp'][i] and             prices2[t]['Volume'][i] > 1.5*prices2[t]['roll_max_vol'][i-1]:
                tickers_signal[t] = "Buy"

            tickers_ret[t].append((prices2[t]['Adj Close'][i-1]/prices2[t]['Adj Close'][i])-1)

    except:
        print('error'+t)

        if tickers_signal[t] == "":
            tickers_ret[t].append(0)
        elif tickers_signal[t] == "Buy":
            tickers_ret[t].append((prices2[t]['Adj Close'][i]/prices2[t]['Adj Close'][i-1])-1)
        elif tickers_signal[t] == "Sell":
            tickers_ret[t].append((prices2[t]['Adj Close'][i-1]/prices2[t]['Adj Close'][i])-1)            


# In[53]:


tickers_signal


# In[46]:


prices2[t].iloc[i]


# In[112]:


return_port = pd.DataFrame()

for t in tickers:
    return_port[t] = prices2[t]['ret']

return_port['ret'] = return_port.mean(axis=1)
CAGR(return_port), vol(return_port), sharpe(return_port,0), max_dd(return_port)


# In[113]:


plt.figure(figsize=(15,5))
for t in tickers:
    plt.plot((1+return_port[t]).cumprod(),label = t)
plt.plot((1+return_port['ret']).cumprod(),label = 'strategy')
plt.legend()
plt.show()


# In[117]:


(1+return_port['GGBR4.SA']).cumprod()


# In[89]:


i


# In[36]:


tickers_signal


# In[ ]:




