# 苏州新冠流调地点可视化
库里主要有3个文件：
- 数据处理代码：covid_sz.py
- 处理后可以用到html里的点标记：points.txt
- 可视化地图html: covid_sz.html

## 数据处理代码
导入的是整理好的病例行踪excel**工作表**（注意是工作表，每天更新的信息存在不同表里），格式大概为下面两张图，
数据来源是苏州本地宝（是的，我的信息来源就是这么low，对网速常年2G的我要求不要太高）。

![Sample excel 1](../excel1.png)

![Sample excel 2](../excel2.png)

最后处理好导出的是一串字典，每个字典都对应一个位置，记录经纬度、病例编号/来源，和具体地址，也可以自由添加其他信息，比如病例关系，
只要修改loop里的代码就可以了。

```python
{"lat":31.320396367590526,"lng":120.67596551151783,"id":"3月16日新增无症状感染者","dizhi":"江苏省苏州市工业园区喜士多便利店（苏悦广场南楼）"}
```

在获取经纬度的时候，用到了百度地图的api，需要申请开发者的api key。

```python
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
```

## 可视化地图html
效果如下, 本来想用GitHub Page，但是显示不出来。就需要先下到电脑里再打开。文件里已经删除了我的密钥，所以打开的时候需要加上密钥。

![Sample html](../sample_html.png)

## 待改进的地方
可以改进的地方太多了。做这个网页一天之前，我一个html都没写过。看到sample code，我当场自闭了。    
然后就先从一个点试试，试完了就loop。更别提一开始api类别都申请错了。。。     
    
网页可以有以下几种改进方式：
1. 加入时间戳，显示轨迹
2. 和统计数据结合，做成交互式的前端。大概就是这篇博客里的内容：[百度地图标注及结合ECharts图谱数据可视化](https://blog.51cto.com/jalony/2882428)
