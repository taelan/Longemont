# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:59:40 2019

@author: 41223
"""

import os
import pandas as pd
import numpy as np
import datetime

os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
f = pd.read_excel('途牛确认单.xls')

df = f[['资源名称','出游日期','成人结算价','总成本','确认单类型']]
df['下单数'] = 1

def cjs_(s):       
        if '新订' in s:            
            return(1)
        else:
            return(0)
            
df['成交数'] = df['确认单类型'].apply(cjs_)
df['流失数'] = df['下单数'] - df['成交数']
df['成交金额'] = df['成交数'] * df['总成本']
df['流失金额'] = df['流失数'] * df['总成本']
df['间夜'] = df['总成本'] / df['成人结算价']
df['成交间夜'] = df['成交数'] * df['间夜']
df['流失间夜'] = df['流失数'] * df['间夜']

df.drop(['间夜','成人结算价','确认单类型','总成本'],axis=1,inplace=True)
df.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\途牛明细.xlsx',index=False)

df.loc[:,'出游日期'] = pd.to_datetime(df['出游日期'], format ='%Y-%m-%d')
df.index=df.出游日期
F1 = pd.DataFrame(df.resample('D').sum().to_period('D'))
F1.reset_index(inplace=True)
F1.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\途牛.xlsx',index=False)