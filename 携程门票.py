# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:14:00 2019

@author: 41223
"""
import os
import pandas as pd
import numpy as np


os.chdir(r'C:/Users/41223/Desktop/网络数据分析')

#df = pd.read_excel(r'C:/Users/41223/Desktop/网络数据分析/20190601150415.xls',encoding = 'utf8')
f = pd.read_excel('test.xlsx')[:-1]


def cjs_(s):   
        if '已取消' in s:
            return('订单已取消')
        else:
            return(s)

def cjrc_(s):       
        if '未取票' in s:            
            return('未取票')
        else:
            return(s)


datalist = [] 
for i in range(0, len(f)):
#xds下单数，cjs成交数，cjl成交率，cjje成交金额，lsdd流失订单，lsrs流失人数，lsje流失金额
    xds = f.iloc[i]['使用日期']
    cjs = cjs_(f.iloc[i]['订单状态'])
    qps = cjrc_(f.iloc[i]['取票数'])
    zdj = f.iloc[i]['总底价']
    dps = f.iloc[i]['订票数']
    ydzymc = f.iloc[i]['预订资源名称']
    #ddzt_c = f[f['订单状态'].str.contains('已取消')]
    #cjs = len(f[~f['订单状态'].str.contains('已取消')])
   # qps_c = f[f['取票数'].str.contains('未取票')]
    data_list2 = [['时间',xds],
                  ['成交数',cjs],
                  ['取票数',qps],
                  ['总底价',zdj],
                  ['订票数',dps],
                  ['预订资源名称',ydzymc]]
    
    datalist.append(dict(data_list2))
    
df1 = pd.DataFrame(datalist)

#xcjdbig大床房,xcjdn标准间，xcmhzs演艺，xczoom动物园
xc_jd_big = df1[df1['预订资源名称'].str.contains('大床房')]   
xc_jd_n = df1[df1['预订资源名称'].str.contains('标准间')]
xc_mhzs = df1[df1['预订资源名称'].str.contains('《梦幻钻石》')]
xc_zoom = df1[df1['预订资源名称'].str.contains('动物世界车行区')]


list_cjrs = []
list_zdj = []
list_lsrs = []
list_lsje = []

#下单数
xds = len(df1)

#成交数
df_paid = df1[~df1['成交数'].str.contains('已取消')]
cjs = len(df_paid)

#成交人数
df_cjrs = df_paid[~df_paid['取票数'].str.contains('未取票')]
for i in range(0,len(df_cjrs)): 
    list_cjrs.append(int(df_cjrs.iloc[i]['取票数']))
cjrs = sum(list_cjrs) 
#成交金额
df_paid = df1[~df1['成交数'].str.contains('已取消')]
for i in range(0,len(df_paid)):    
    list_zdj.append(df_paid.iloc[i]['总底价'])
    
cjje = sum(list_zdj)


#成交率
cjl = '%0.2f'%(cjs/xds)

#流失订单
df_lsdd = df1[df1['成交数'].str.contains('已取消')]
lsdd = len(df_lsdd)
#流失金额
#流失人数
for i in range(0,len(df_lsdd)):
    list_lsrs.append(df_lsdd.iloc[i]['订票数'])
    list_lsje.append(df_lsdd.iloc[i]['总底价'])
lsrs = sum(list_lsrs)    
lsje = sum(list_lsje)

data_list3 = [['下单数',xds],
              ['成交数',cjs],
              ['成交人数',cjrs],
              ['成交金额',cjje],
              ['成交率',cjl],
              ['流失订单',lsdd],
              ['流失金额',lsje],
              ['流失人数',lsrs]]

df_xiaoji = pd.DataFrame(data_list3)

print(cjrs)