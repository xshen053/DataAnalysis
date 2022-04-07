# -*- coding = utf-8 -*-
# @Time : 2020/9/26 17:58
# @Author : MIKESHEN
# @File : find_info.py
# @Software : PyCharm
from bs4 import BeautifulSoup  #网页解析，获取数据
import re
foundday = re.compile(r'<td><span class="letterSpace01">成 立 日</span>：(.*?)</td>')
findmanager = re.compile(r'<td>基金经理：<a href="(.*?)">(.*?)</a>')
findlink = re.compile(r'<td class="td02"><a href="(.*?)">')
findprice1 = re.compile(r'<td class="zhang">(.*?)%</td>')
findprice2 = re.compile(r'<td class="die">(.*?)%</td>')
def findthings(html):
    date = re.findall(foundday, html)[0]
    manager = re.findall(findmanager, html)[0][1]
    link = re.findall(findlink, html)[0]
    return date, manager, link

#计算这个基金经理管理过的所有产品投资回报率
def find_ROI(html):
    soup = BeautifulSoup(html, "html.parser")
    price = []
    for item in soup.find_all('td', class_=["zhang", "die"]):  # 查找符合要求的字符串，形成列表，class_加下划线代表属性（类别）不是类
        item = str(item)
        if len(re.findall(findprice1, item)) != 0:
            price.append(re.findall(findprice1, item)[0])
        if len(re.findall(findprice2, item)) != 0:
            price.append(re.findall(findprice2, item)[0])
        else:
            continue
    sum = 0
    for i in range(len(price)):
        price[i] = price[i].replace(',', '')
        price[i] = float(price[i])
        sum = sum + price[i]
    #从小到大排序
    price.sort()
    #列表小数转为百分数
    for i in range(len(price)):
        price[i] = "%.2f%%" % price[i]
    return price, sum/len(price)