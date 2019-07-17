# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:55:56 2019

@author: 41223
"""

import os
import pandas as pd
import numpy as np
import datetime

os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
f = pd.read_excel('驴妈妈线路.xlsx')

df = f[['产品名称','确认类型','结算总价','预订份数','出游时间']]
df['下单数'] = 1

def cjs_(s):       
        if '新订' in s:            
            return(1)
        elif '修改' in s:
            return(1)
        else:
            return(0)
            
df['成交数'] = df['确认类型'].apply(cjs_)
df['流失数'] = df['下单数'] - df['成交数']
df['成交金额'] = df['成交数'] * df['结算总价']
df['流失金额'] = df['流失数'] * df['结算总价']
df['成交间夜'] = df['成交数'] * df['预订份数']
df['流失间夜'] = df['流失数'] * df['预订份数']

df.drop(['确认类型','预订份数','结算总价'],axis=1,inplace=True)
df.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\驴妈妈线路明细.xlsx',index=False)

df.loc[:,'出游时间'] = pd.to_datetime(df['出游时间'], format ='%Y-%m-%d')
df.index=df.出游时间
F1 = pd.DataFrame(df.resample('D').sum().to_period('D'))
F1.reset_index(inplace=True)
F1.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\驴妈妈线路.xlsx',index=False)