# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:55:32 2019

@author: 41223
"""

import os
import pandas as pd
import numpy as np
import datetime

os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
f = pd.read_excel('驴妈妈.xlsx')

df = f[['类型','房型 ','入住日期','离店日期','房间数','结算单价','结算总价']]
df['下单数'] = 1

def cjs_(s):       
        if '新订' in s:            
            return(1)
        elif '修改' in s:
            return(1)
        else:
            return(0)
            
def getBetweenDay(b,e):
    date_list1 = []
    begin_date = b
    end_date = e
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list1.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list1

def getJy(s):
    #s.drop(['入住日期'],axis=1,inplace=True)
    #s.reset_index(inplace=True)
    s.loc[:,'住店时间'] = s.住店时间.astype('str')
    F2 = s['住店时间'].str.split(',', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'住店时间'}).join(s.drop('住店时间', axis=1))
    F2['住店时间'] = F2.住店时间.apply(lambda x: x.split('\'')[1])
    #F2.index=F2.住店时间
    return F2


df['成交数'] = df['类型'].apply(cjs_)
df['流失数'] = df['下单数'] - df['成交数']            
df['成交金额'] = df['成交数'] * df['结算总价']
df['流失金额'] = df['流失数'] * df['结算总价']
df['成交间夜'] = df['成交数'] * df['房间数']
df['流失间夜'] = df['流失数'] * df['房间数']

datalist = []
for i in range(0, len(df)):
    #xds = df.iloc[i]['下单数']
    cjjy = df.iloc[i]['成交间夜']
    lsjy = df.iloc[i]['流失间夜']
    zdsj = getBetweenDay(df.iloc[i]['入住日期'],df.iloc[i]['离店日期'])
    data_list2 = [['住店时间',zdsj],
                  ['成交间夜',cjjy],
                  ['流失夜数',lsjy],           
                  #['下单数',xds]
                  ]
    datalist.append(dict(data_list2))
f2 = pd.DataFrame(datalist)

jysj = getJy(f2)
jysj.loc[:,'住店时间'] = pd.to_datetime(jysj['住店时间'], format ='%Y-%m-%d')
jysj.index=jysj.住店时间

F2 = pd.DataFrame(jysj.resample('D').sum().to_period('D'))

df.drop(['结算单价','房间数','结算总价','成交间夜','流失间夜'],axis=1,inplace=True)
df.loc[:,'入住日期'] = pd.to_datetime(df['入住日期'], format ='%Y-%m-%d')
df.index=df.入住日期
F1 = pd.DataFrame(df.resample('D').sum().to_period('D'))
F3 = pd.merge(F1,F2,left_index=True,right_index=True) 
F3.reset_index(inplace=True)         