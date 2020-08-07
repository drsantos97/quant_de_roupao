#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


# In[3]:


#importando base
qtd = pd.read_excel(r'C:\Users\drsan\OneDrive\Área de Trabalho\Python\Analise Carteira - Python.xlsx',sheet_name = 'Quantidades')
qtd.head()


# In[4]:


def CAGR(x):
    df = x.copy()
    df['return'] = df.pct_change()
    df['cum_return'] = (1+df['return']).cumprod()
    n = len(df)/252
    CAGR = (df['cum_return'].tolist()[-1])**(1/n)-1
    return CAGR

def vol(x):
    df = x.copy()
    df['return'] = df.pct_change()    
    vol = df['return'].std()*np.sqrt(252)
    return vol

def sharpe(x):
    df = x.copy()
    sharpe = CAGR(x)/vol(x)
    return sharpe

def max_dd(x):
    df = x.copy()
    df['return'] = df.pct_change() 
    df['cum_return'] = (1+df['return']).cumprod()
    df['cum_return_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_return_max'] - df['cum_return']
    df['drawdown_pct'] = df['drawdown']/df['cum_return_max']
    max_dd = df['drawdown_pct'].max()
    return max_dd


# In[5]:


# definicoes -> end tem que ser segunda
start = '2020-05-15'
end = '2020-08-06' 


# In[6]:


dates = pd.date_range(start = start, end = end)
prices_onshore = pd.DataFrame(index = dates)
prices_offshore = pd.DataFrame(index = dates)
tickers = qtd['Ativos']

# precos
for t in tickers:
    
#    if (qtd[qtd['Ativos']==t]['Tipo'] == 'Acoes Onshore').bool() or (qtd[qtd['Ativos']==t]['Tipo'] == 'ETF Onshore').bool():
    if (qtd[qtd['Ativos']==t]['Tipo'] == 'Acoes Onshore').bool():
        prices_onshore[t+'.SA'] = yf.download(t+'.SA',start,end)['Adj Close']
        
    elif (qtd[qtd['Ativos']==t]['Tipo'] == 'Acoes Offshore').bool() or (qtd[qtd['Ativos']==t]['Tipo'] == 'ETF Offshore').bool():
        prices_offshore[t] = yf.download(t,start,end)['Adj Close']
        


# In[7]:


#dando aquele tapa
prices_onshore.dropna(how='all',inplace=True)
prices_offshore.dropna(how='all',inplace=True)

#qtd_on
qtd2 = qtd.T.drop(index='Tipo')
qtd2.columns = qtd2.iloc[0]+'.SA'
qtd2 = qtd2.drop(index='Ativos')
qtd2.index = pd.to_datetime(qtd2.index)


# In[8]:


#qtd diaria
qtd_onshore = pd.DataFrame(index = prices_onshore.index, columns = prices_onshore.columns)

for n in range(len(qtd_onshore.index)-1):
    
    if n == 0:
        for m in range(len(qtd_onshore.columns)):
            qtd_onshore.iloc[n,m] = qtd2.loc[qtd_onshore.index[n],qtd_onshore.columns[m]]
    
    elif qtd_onshore.index[n] in qtd.columns:
        for m in range(len(qtd_onshore.columns)):
            qtd_onshore.iloc[n+1,m] = qtd2.loc[qtd_onshore.index[n],qtd_onshore.columns[m]]

qtd_onshore.fillna(method='ffill', inplace=True)
qtd_onshore.dropna(how='all', inplace = True)

#carteira em $
balance_onshore = (qtd_onshore*prices_onshore)


# In[9]:


qtd_cotas = pd.DataFrame(index = prices_onshore.index, columns = ['qtd'])

for n in range(len(qtd_cotas.index)):
    
    if n == 0:
        qtd_cotas['qtd'][n] = balance_onshore.iloc[0].sum()/100
        qtd_cotas['qtd'][n+1] = qtd_cotas['qtd'][n]
           
    elif qtd_cotas.index[n] not in qtd.columns and qtd_cotas.index[n-1] not in qtd.columns:
        qtd_cotas['qtd'][n] =  qtd_cotas['qtd'][n-1]   
    
    elif qtd_cotas.index[n] in qtd.columns:
        qtd_cotas['qtd'][n] = qtd_cotas['qtd'][n-1]
        qtd_cotas['qtd'][n+1] = (qtd_onshore.iloc[n+1]*prices_onshore.iloc[n]).sum()/balance_onshore.iloc[n].sum()*qtd_cotas['qtd'][n]


# In[10]:


valor_cotas = pd.DataFrame(index = prices_onshore.index, columns = ['cota'])

for n in range(len(valor_cotas.index)):
    
    if n == 0:
        valor_cotas['cota'][n] = 100
    
    else:
        valor_cotas['cota'][n] = balance_onshore.iloc[n].sum()/qtd_cotas['qtd'][n]
        


# In[11]:


#retorno do ETF
prices_bench_onshore = pd.DataFrame(index=valor_cotas.index)
prices_bench_onshore = yf.download('^BVSP',start,end)['Adj Close']
prices_bench_onshore.dropna(how='all',inplace=True)


# In[12]:


#filtro
filtro_start = '2020-05-15'
filtro_end = '2020-07-31'

#retornos
daily_returns_bench_onshore = prices_bench_onshore[(prices_bench_onshore.index>=filtro_start) & (prices_bench_onshore.index<=filtro_end)].pct_change()
daily_returns_bench_onshore_cum = (daily_returns_bench_onshore+1).cumprod()

daily_returns_portfolio = valor_cotas[(valor_cotas.index>=filtro_start) & (valor_cotas.index<=filtro_end)].pct_change()
daily_returns_portfolio_cum = (daily_returns_portfolio+1).cumprod()

#grafico
plt.figure(figsize=(15,5))
plt.plot(daily_returns_portfolio_cum, label ='portfolio')
plt.plot(daily_returns_bench_onshore_cum, label = 'BOVA')
plt.legend()
plt.show()


# In[13]:


CAGR(prices_bench_onshore), CAGR(valor_cotas)


# In[14]:


vol(prices_bench_onshore), vol(valor_cotas)


# In[15]:


sharpe(prices_bench_onshore), sharpe(valor_cotas)


# In[16]:


max_dd(prices_bench_onshore), max_dd(valor_cotas)


# In[15]:


plt.plot(qtd_cotas)


# In[14]:


plt.plot(balance_onshore.sum(axis=1))


# In[ ]:




