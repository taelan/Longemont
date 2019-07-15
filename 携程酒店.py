# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:28:36 2019

@author: 41223
"""
import os
import pandas as pd
import numpy as np
import datetime


os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
df = pd.read_excel('携程酒店.xlsx')
df['下单数'] = 1

df.loc[:,'离店日期'] = pd.to_datetime(df['离店日期'], format ='%Y-%m-%d')
df.loc[:,'入住日期'] = pd.to_datetime(df['入住日期'], format ='%Y-%m-%d')
#成交数函数
def cjs_(s):       
        if '取消' in s:            
            return(0)
        elif '无效' in s:
            return(0)
        else:
            return(1)
#拆分间夜
def getBetweenDay(b,e):
    date_list1 = []
    begin_date = b
    end_date = e
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list1.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list1
#成交/流失间夜函数
def getCjjy(s):
    dfsj.loc[:,'成交数'] = dfsj.成交数.astype('str')
    cjsj = dfsj[dfsj['成交数'].str.contains(s)]
    cjsj.drop(['入住日期'],axis=1,inplace=True)
    cjsj.reset_index(inplace=True)
    cjsj.loc[:,'住店时间'] = cjsj.住店时间.astype('str')
    F2 = cjsj['住店时间'].str.split(',', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'住店时间'}).join(cjsj.drop('住店时间', axis=1))
    F2['住店时间'] = F2.住店时间.apply(lambda x: x.split('\'')[1])
    F2.index=F2.住店时间
    return F2
#住店时间字段清洗
def getJy(s):
    s.drop(['入住日期'],axis=1,inplace=True)
    s.reset_index(inplace=True)
    s.loc[:,'住店时间'] = s.住店时间.astype('str')
    F2 = s['住店时间'].str.split(',', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'住店时间'}).join(s.drop('住店时间', axis=1))
    F2['住店时间'] = F2.住店时间.apply(lambda x: x.split('\'')[1])
    #F2.index=F2.住店时间
    return F2
#数据集
datalist = []
for i in range(0, len(df)): 
    rzrq = df.iloc[i]['入住日期']
    xds = df.iloc[i]['下单数']
    cjs = cjs_(df.iloc[i]['订单类型'])
    cjrs = df.iloc[i]['房间数'] * cjs
    lsjs = df.iloc[i]['房间数'] * (xds - cjs)
    cjje = df.iloc[i]['房价'] * cjs
    cjl = '%0.2f'%(cjs/xds)
    lsdd = xds - cjs
    #lsrs = int(df.iloc[i]['房间数']) * lsdd
    lsje = df.iloc[i]['房价'] * lsdd
    cpmc = df.iloc[i]['酒店名称']
    fxmc = df.iloc[i]['房型名称']
    #cjys = int(str(df.iloc[i]['离店日期'] - df.iloc[i]['入住日期'])[0])
    zdsj = getBetweenDay(df.iloc[i]['入住日期'],df.iloc[i]['离店日期'])
    data_list2 = [['入住日期',rzrq],
                  ['下单数',xds],
                  ['成交数',cjs],
                  ['成交间数',cjrs],
                  ['流失间数',lsjs],
                  ['成交金额',cjje],
                  #['成交率',cjl],
                  ['流失订单',lsdd],
                  ['流失金额',lsje],
                  #['流失人数',lsrs],
                  ['酒店名称',cpmc],
                  #['成交夜数',cjys],
                  ['住店时间',zdsj],
                  ['房型名称',fxmc]]
    datalist.append(dict(data_list2))
dfsj = pd.DataFrame(datalist)
dfsj.index=dfsj.入住日期
dfsj.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\携程酒店明细.xlsx',index=False)
F1 =  pd.DataFrame(dfsj.resample('D').sum().to_period('D'))

'''
dfsj.loc[:,'流失人数'] = dfsj.流失人数.astype('str')

cjsj = dfsj[dfsj['流失人数'].str.contains('0')]
cjsj.drop(['入住日期'],axis=1,inplace=True)
cjsj.reset_index(inplace=True)
cjsj.loc[:,'住店时间'] = cjsj.住店时间.astype('str')
F2 = cjsj['住店时间'].str.split(',', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'住店时间'}).join(cjsj.drop('住店时间', axis=1))
F2['住店时间'] = F2.住店时间.apply(lambda x: x.split('\'')[1])
F2.index=F2.住店时间
'''

jysj = getJy(dfsj)
jysj.loc[:,'住店时间'] = pd.to_datetime(jysj['住店时间'], format ='%Y-%m-%d')
jysj.index=jysj.住店时间

F2 = pd.DataFrame(jysj.resample('D').sum().to_period('D'))

F1.drop(['成交间数','流失间数'],axis=1,inplace=True)
#F1.reset_index(inplace=True)
f2 = F2[['成交间数','流失间数']]
#f2.reset_index(inplace=True)


#合并数据集
F3 = pd.merge(F1,f2,left_index=True,right_index=True)
F3.reset_index(inplace=True)
F3.to_excel(r'C:\Users\41223\Desktop\网络数据分析\导出\携程酒店.xlsx',index=False)


