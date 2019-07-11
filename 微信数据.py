# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:50:41 2019

@author: 41223
"""

import os
import pandas as pd
import numpy as np
import datetime


os.chdir(r'C:/Users/41223/Desktop/网络数据分析')
df = pd.read_excel('微信.xls')[:-1]
df['下单数'] = 1

#转字符串
df.loc[:,'手机号'] = df.手机号.astype('str').str[:-2]
df.loc[:,'串码'] = df.串码.astype('str').str[:-2]
df.loc[:,'已退数量'] = df.已退数量.astype('str')
df.loc[:,'游玩开始日期'] = pd.to_datetime(df['游玩开始日期'], format ='%Y-%m-%d')
df.loc[:,'游玩结束日期'] = pd.to_datetime(df['游玩结束日期'], format ='%Y-%m-%d')
#df.loc[:,'交易日期'] = df.交易日期.astype('str')
df.index=df.交易日期
#df.drop(['交易日期'],axis=1)

df1 = df[['交易日期','下单数','产品名称','产品价格','支付状态','游玩开始日期','游玩结束日期','交易数量','交易金额','已退数量','已退金额']]
#df1 = df[['下单数','产品名称','产品价格']]

#df_jd = df1[df1['产品名称'].str.contains('钻石酒店' )]
#df_mp = df1[df1['产品名称'].str.contains('动物世界车行区|梦幻钻石')]

   
#print(df_mp.resample('D').sum().to_period('D'))
datalist = []
def cjs_(s):       
        if '0' in s:            
            return(1)
        else:
            return(0)

'''def lsdd_(s):
    if '0' in s:
        return(0)
    else:
        return(1)'''
   
for i in range(0, len(df)): 
    jyrq = df.iloc[i]['交易日期']
    xds = df.iloc[i]['下单数']
    cjs = cjs_(df.iloc[i]['已退数量'])
    cjrs = df.iloc[i]['交易数量']
    cjje = df.iloc[i]['交易金额'] - df.iloc[i]['已退金额']
    cjl = '%0.2f'%(cjs/xds)
    lsdd = xds - cjs
    lsrs = int(df.iloc[i]['已退数量'])
    lsje = df.iloc[i]['已退金额']
    cpmc = df.iloc[i]['产品名称']
    cjys = int(str(df.iloc[i]['游玩结束日期'] - df.iloc[i]['游玩开始日期'])[0])
    data_list2 = [['交易日期',jyrq],
                  ['下单数',xds],
                  ['成交数',cjs],
                  ['成交人数',cjrs],
                  ['成交金额',cjje],
                  #['成交率',cjl],
                  ['流失订单',lsdd],
                  ['流失金额',lsje],
                  ['流失人数',lsrs],
                  ['产品名称',cpmc],
                  ['成交夜数',cjys]]
    datalist.append(dict(data_list2))
dfsj = pd.DataFrame(datalist)
dfsj.index=df.交易日期
dfsj.drop(['交易日期'],axis=1)
df_jd = dfsj[dfsj['产品名称'].str.contains('钻石酒店' )]
df_mp = dfsj[dfsj['产品名称'].str.contains('动物世界车行区|梦幻钻石')]
df_mp.drop(['成交夜数'],axis=1)
