#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 09:09:29 2022

@author: shiqimeng
"""

import pandas as pd
import os
import json
import requests

# 读取文件信息
path = '/Users/shiqimeng/Desktop'
data = pd.read_excel(path + os.sep + 'covid_sz.xlsx','3月16日')  # 读取某日病例信息,放在一个工作表

# 删掉重复地址
data = data.drop_duplicates(subset = '完整地址')

# 构建抓取经纬度函数
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = '<你的密钥>'  # 百度地图密钥
    add = address # 由于地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    r = requests.get(uri)
    temp = json.loads(r.text)
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lat,lng

# 抓取经纬度
loc = data['完整地址'].to_list()
lat = [] # 纬度
lng = [] # 经度

for place in loc:
    get_loc = getlnglat(place)
    lat.append(get_loc[0])
    lng.append(get_loc[1])

data['纬度'] = lat
data['经度'] = lng

# 生成 HTML 适配的格式，写入一个txt文件
data_html = pd.DataFrame(columns=['content'])

for idx in data.index:
    data_html.loc[idx,'content'] = '{' + \
 '"lat":' + str(data.loc[idx,'纬度']) + ',' +  \
 '"lng":' + str(data.loc[idx,'经度']) + ',' +  \
 '"id":' + '"' + str(data.loc[idx,'编号']) +'"' + ',' +  \
 '"dizhi":' + '"' + str(data.loc[idx,'完整地址']) +'"' +   \
 '}' + ','

     # '"guanxi":' + str(data.loc[idx,'病例关系']) + ',' +  \

with open(path + os.sep + 'points.txt','a') as f:
    points = data_html.to_string(header = False, index = False)
    f.write(points)
