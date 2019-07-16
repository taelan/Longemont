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
            
def getLdsj(a,b):
    f = a + datetime.timedelta(b)
    return f

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
    
df = f[['预约数量','消费时间','预约单状态','产品名称','预约房型/项目']]

df['下单数'] = 1
df['单价'] = 600
df['间'] = df.预约数量.apply(lambda x: x.split('*')[0][0])
df['夜'] = df.预约数量.apply(lambda x: x.split('*')[1][0])
df['入住时间'] = df.消费时间.apply(lambda x: x.split('至')[0])
#df['离店时间'] = 
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

#df['成交间夜'] = df['间夜'] * df['成交数']
#df['流失间夜'] = df['间夜'] * df['流失数']
df['流失金额'] = df['金额'] * df['流失数']
df['成交金额'] = df['金额'] * df['成交数']


datalist = []
for i in range(0, len(df)):
    cjjy = df.iloc[i]['间'] * df.iloc[i]['成交数']
    lsjy = df.iloc[i]['间'] * df.iloc[i]['流失数']
    rzsj = df.iloc[i]['入住时间']
    ldsj = getLdsj(df.iloc[i]['入住时间'],int(df.iloc[i]['夜']))
    zdsj = getBetweenDay(rzsj,ldsj)
    data_list2 = [['住店时间',zdsj],
                  ['成交间夜',cjjy],
                  ['流失间夜',lsjy]
                  ]
    datalist.append(dict(data_list2))
f2 = pd.DataFrame(datalist)

df.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\云客赞明细.xlsx',index=False)

jysj = getJy(f2)
jysj.loc[:,'住店时间'] = pd.to_datetime(jysj['住店时间'], format ='%Y-%m-%d')
jysj.index=jysj.住店时间

F2 = pd.DataFrame(jysj.resample('D').sum().to_period('D'))

df.drop(['单价','间','夜','间夜','金额'],axis=1,inplace=True)
df.index=df.入住时间

F1 =  pd.DataFrame(df.resample('D').sum().to_period('D'))
F3 = pd.merge(F1,F2,left_index=True,right_index=True) 
F3.reset_index(inplace=True)       


F3.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\云客赞.xlsx',index=False)