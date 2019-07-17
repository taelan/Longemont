# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:27:15 2019

@author: 41223
"""

import os
import pandas as pd
import numpy as np
import datetime

os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
f = pd.read_excel('美团线路.xlsx')

df = f[['套餐名称','份数','总金额','出发时间','订单状态']]
df['下单数'] = 1

def cjs_(s):       
        if '已消费' in s:            
            return(1)
        else:
            return(0)
            
df['成交数'] = df['订单状态'].apply(cjs_)
df['流失数'] = df['下单数'] - df['成交数']
df['成交金额'] = df['成交数'] * df['总金额']
df['流失金额'] = df['流失数'] * df['总金额']
df['成交间夜'] = df['成交数'] * df['份数']
df['流失间夜'] = df['流失数'] * df['份数']

df.drop(['份数','总金额','订单状态'],axis=1,inplace=True)
df.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\美团线路明细.xlsx',index=False)

df.loc[:,'出发时间'] = pd.to_datetime(df['出发时间'], format ='%Y-%m-%d')
df.index=df.出发时间
F1 = pd.DataFrame(df.resample('D').sum().to_period('D'))
F1.reset_index(inplace=True)
F1.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\美团线路.xlsx',index=False)