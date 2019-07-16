# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:39:33 2019

@author: 41223
"""
import os
import pandas as pd
import numpy as np
import datetime

os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
f = pd.read_excel('云客赞.xlsx')

def cjs_(s):       
        if '已消费' in s:            
            return(1)
        elif '已确认' in s:
            return(1)
        else:
            return(0)

df = f[['预约数量','消费时间','预约单状态','产品名称','预约房型/项目']]

df['下单数'] = 1
df['单价'] = 600
df['间'] = df.预约数量.apply(lambda x: x.split('*')[0][0])
df['夜'] = df.预约数量.apply(lambda x: x.split('*')[1][0])
df['入住时间'] = df.消费时间.apply(lambda x: x.split('至')[0])
df['离店时间'] = df.消费时间.apply(lambda x: x.split('至')[1])
df.drop(['消费时间'],axis=1,inplace=True)
df.drop(['预约数量'],axis=1,inplace=True)

df.loc[:,'间'] = df.间.astype('int')
df.loc[:,'夜'] = df.夜.astype('int')
df.loc[:,'入住时间'] = pd.to_datetime(df['入住时间'], format ='%Y-%m-%d')

df['间夜'] = df['间'] * df['夜']
df['金额'] = df['单价'] * df['间夜']
df['成交数'] = df['预约单状态'].apply(cjs_)
df['流失数'] = df['下单数'] - df['成交数']
df.drop(['预约单状态'],axis=1,inplace=True)

df['成交间夜'] = df['间夜'] * df['成交数']
df['流失间夜'] = df['间夜'] * df['流失数']
df['流失金额'] = df['金额'] * df['流失数']
df['成交金额'] = df['金额'] * df['成交数']
df.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\云客赞明细.xlsx',index=False)

df.drop(['单价','间','夜','间夜','金额'],axis=1,inplace=True)

df.index=df.入住时间

F1 =  pd.DataFrame(df.resample('D').sum().to_period('D'))
F1.reset_index(inplace=True)
F1.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\云客赞.xlsx',index=False)
