# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:33:18 2019

@author: 41223
"""

import os
import pandas as pd
import numpy as np
import datetime

os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
f = pd.read_excel('驴妈妈门票.xlsx')

df = f[['产品名称','游玩时间','游玩状态','订购份数','结算单价']]
df['下单数'] = 1

def cjs_(s):       
        if '已游玩' in s:            
            return(1)
        else:
            return(0)
            
df['成交数'] = df['游玩状态'].apply(cjs_)
df['流失数'] = df['下单数'] - df['成交数']
df['成交金额'] = df['成交数'] * df['结算单价']
df['流失金额'] = df['流失数'] * df['结算单价']
df['成交人数'] = df['成交数'] * df['订购份数']
df['流失人数'] = df['流失数'] * df['订购份数']

df.drop(['游玩状态','订购份数','结算单价'],axis=1,inplace=True)
df.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\驴妈妈门票明细.xlsx',index=False)

#df.loc[:,'游玩时间'] = pd.to_datetime(df['游玩时间'], format ='%Y-%m-%d')
df.index=df.游玩时间
F1 = pd.DataFrame(df.resample('D').sum().to_period('D'))
F1.reset_index(inplace=True)
F1.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\驴妈妈门票.xlsx',index=False)