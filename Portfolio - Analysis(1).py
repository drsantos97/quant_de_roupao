#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from random import *
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from scipy.stats import norm
import statsmodels.api as sm
import datetime as dt
from yahooquery import Ticker
import yfinance as yf
from yahoofinancials import YahooFinancials


# In[2]:


#Acoes_tickers = pd.read_excel('C:/Users/hudsm/Documents/Quantitative Fund/Portfolio/Atividades/InstrumentsConsolidatedFile_20200703_1.xlsx')


# In[3]:


def CAGR(DF):
    yd = DF.copy()   
    Acoes_precos_longo_prazo_ret_d = yd.pct_change()
    Acoes_precos_longo_prazo_ret_d_cum_ret = (1 + Acoes_precos_longo_prazo_ret_d).cumprod()
    n = len(yd)/(252)
    CAGR = (Acoes_precos_longo_prazo_ret_d_cum_ret.iloc[-1]/1)**(1/n)-1
    return CAGR


# In[4]:


def vol(DF):
    yd = DF.copy() 
    Acoes_precos_longo_prazo_ret_d = yd.pct_change()
    Acoes_precos_longo_prazo_vol_a = Acoes_precos_longo_prazo_ret_d.std()*np.sqrt(252)
    return Acoes_precos_longo_prazo_vol_a


# In[5]:


def sharpe(DF,rf):
    yd = DF.copy() 
    sr = (CAGR(yd) - rf)/vol(yd)
    return sr


# In[6]:


#Acoes_tickers.set_index('SgmtNm',inplace=True)
#Acoes_tickers = Acoes_tickers.loc['CASH']
#Acoes_tickers.set_index('SctyCtgyNm',inplace=True)
#Acoes_tickers = Acoes_tickers.loc[['SHARES','UNIT']]
#Acoes_tickers.set_index('CorpGovnLvlNm',inplace=True)
#Acoes_tickers = Acoes_tickers.drop(['MERCADO DE BALCÃO','BOVESPA MAIS','M2'])
#Acoes_tickers.set_index('SpcfctnCd',inplace=True)
#Acoes_tickers = Acoes_tickers[Acoes_tickers.MktCptlstn > 70000000]
#Acoes_tickers.set_index('Asst',inplace=True)
#Acoes_tickers_final = pd.DataFrame()
#Acoes_tickers_final = Acoes_tickers['TckrSymb']
#Acoes_tickers_final = Acoes_tickers_final.astype(str) + '.SA'
#Acoes_tickers_final = Acoes_tickers_final.values.tolist()
#try:
#    Acoes_tickers_final = Acoes_tickers_final.drop('PNVL3.SA')
#except:
#    pass 
#try:
#    Acoes_tickers_final = Acoes_tickers_final.drop('IDNT3.SA')
#except:
#    pass 
#try:
#    Acoes_tickers_final = Acoes_tickers_final.drop('CPLE5.SA')
#except:
#    pass  
#try:
#    Acoes_tickers_final = Acoes_tickers_final.drop('VSPT3.SA')
#except:
#    pass


# In[7]:


Acoes_precos_longo_prazo_ret_d = Acoes_precos_longo_prazo.pct_change()


# In[ ]:


#tickers_15mai = {'BBAS3.SA','VVAR3.SA','COGN3.SA','BBDC4.SA','ITUB4.SA','PCAR3.SA','HAPV3.SA','VALE3.SA','BOVA11.SA','JBSS3.SA','RENT3.SA'}


# In[ ]:


#tickers_22mai = {'BBAS3.SA','VVAR3.SA','COGN3.SA','BBDC4.SA','ITUB4.SA','PCAR3.SA','HAPV3.SA','VALE3.SA','BOVA11.SA','JBSS3.SA','RENT3.SA','PETR4.SA','IVVB11.SA','SMAL11.SA','VIVA3.SA'}


# In[ ]:


#tickers_29mai = {'BBAS3.SA','VVAR3.SA','COGN3.SA','BBDC4.SA','ITUB4.SA','PCAR3.SA','HAPV3.SA','VALE3.SA','BOVA11.SA','JBSS3.SA','RENT3.SA','PETR4.SA','IVVB11.SA','SMAL11.SA','VIVA3.SA'}


# In[ ]:


#portfolio_qtys = pd.read_excel('C:/Users/hudsm/Documents/Quantitative Fund/Portfolio/Atividades/Portfolio_Qtys.xlsx')
#portfolio_qtys['Ativo'] = portfolio_qtys['Ativo'] + ".SA"
#portfolio_qtys
#for i in portfolio_qtys:
    #for ticker in portfolio_qtys['Ativo']:
        #portfolio_qtys


# In[ ]:


xls = pd.ExcelFile('C:/Users/hudsm/Documents/Quantitative Fund/Portfolio/Atividades/Simulador - Gestores (2).xlsx')
aba_Huds = pd.read_excel(xls, 'Huds')


# In[ ]:


aba_Huds.iloc[1,:].fillna(method='bfill',inplace=True)


# In[ ]:


aba_Huds.drop([0],inplace=True)


# In[ ]:


aba_Huds_Ativos = aba_Huds.loc[:,aba_Huds.iloc[1].str.contains('^Ativos')]


# In[ ]:


aba_Huds_Qtde = aba_Huds.loc[:,aba_Huds.iloc[1].str.contains('^Qtde Total')]


# In[ ]:


aba_Huds = pd.concat([aba_Huds_Ativos,aba_Huds_Qtde],axis=1)


# In[ ]:


aba_Huds = aba_Huds.rename(columns={aba_Huds.columns[0]:'Ativos'})


# In[ ]:


aba_Huds.set_index(aba_Huds.columns[0],inplace=True)


# In[ ]:


aba_Huds.columns = aba_Huds.iloc[0]


# In[ ]:


aba_Huds = aba_Huds.iloc[3:]


# In[ ]:


aba_Huds.dropna(how='all',inplace=True)


# In[ ]:


range(len(aba_Huds.columns))


# In[ ]:


portfolio = dict()


# In[ ]:


Acoes_precos_longo_prazo = pd.DataFrame()
for t in Acoes_tickers_final:
    try:
        Acoes_precos_longo_prazo[t] = wb.DataReader(t,data_source='yahoo',start='2017-6-1')['Adj Close']
    except:
        pass


# In[ ]:


i=0
for i in range(len(aba_Huds.columns)):
    portfolio[i] = aba_Huds.iloc[:,i]
    print(portfolio[i])


# In[ ]:


Acoes_precos_desc = (Acoes_precos.iloc[-1]/Acoes_precos_longo_prazo_avg.loc[Acoes_precos.index[0]])-1


# In[ ]:


Acoes_precos_desc = Acoes_precos_desc.sort_values(ascending=True)


# In[ ]:


try:
    Acoes_precos_desc = Acoes_precos_desc.dropna()
except:
    pass     


# In[ ]:


Acoes_precos_desc = pd.DataFrame({'Ação':Acoes_precos_desc.index, 'Desconto':Acoes_precos_desc.values})
Industria = [None] * len(Acoes_precos_desc)
Acoes_precos_desc['Industria'] = Industria


# In[ ]:


Sharpe = sharpe(Acoes_precos_longo_prazo,0.0225)


# In[ ]:


Sharpe = pd.DataFrame({'Ação':Sharpe.index, 'Sharpe':Sharpe.values})
Sharpe_values = [None] * len(Acoes_precos_desc)
Acoes_precos_desc['Sharpe'] = Sharpe_values


# In[ ]:


Beta_values = [None] * len(Acoes_precos_desc)
Acoes_precos_desc['Beta'] = Beta_values


# In[ ]:


Acoes_precos_desc


# In[ ]:


Sharpe.set_index('Ação',inplace=True)


# In[ ]:


Sharpe.loc['BBAS3.SA','Sharpe']


# In[ ]:


i = 0
for ticker in Acoes_precos_desc.iloc[:,0]:
    t = Ticker(ticker)
    data = t.asset_profile
    data_beta = t.key_stats
    try:
        Acoes_precos_desc.iloc[i,2] = data[ticker]['industry']
        Acoes_precos_desc.iloc[i,4] = data_beta[ticker]['beta']
        Acoes_precos_desc.iloc[i,3] = Sharpe.loc[ticker,'Sharpe']
    except:
        pass
    i += 1


# In[ ]:


#CAGR_ret = CAGR(Acoes_precos_longo_prazo)


# In[ ]:


#vol_a = vol(Acoes_precos_longo_prazo)


# In[ ]:




