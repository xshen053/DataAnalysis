# -*- coding = utf-8 -*-
# @Time : 2020/9/24 17:10
# @Author : MIKESHEN
# @File : Visualization.py
# @Software : PyCharm

import locale
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import re
from collectdate import collect_date
def calculate3(code, datalist, start_time):
    date = []
    networth = []
    date_final = []
    networth_final = []
    for i in range(len(datalist)):
        date.append(datalist[i][0])
        networth.append(datalist[i][1])
    date.reverse()
    networth.reverse()
    data = networth
    index_j = np.argmax(np.maximum.accumulate(data) - data)  # 结束位置
    # print(index_j)
    index_i = np.argmax(data[:index_j])  # 开始位置
    # print(index_i)
    d = (data[index_i] - data[index_j])/data[index_i]  # 最大回撤
    # 生成横纵坐标信息
    dates = date

    #提取上升阶段的数据
    locale.setlocale(locale.LC_ALL, 'en')
    xs_rise = []
    date_final, networth_final = collect_date(datalist)
    length = len(date_final)
    for i in range(length):
        xs_rise.append([datetime.strptime(a, '%Y-%m-%d').date() for a in date_final[i]])


    xs = [datetime.strptime(a, '%Y-%m-%d').date() for a in dates]
    ys = range(len(xs))
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # 绘制图像
    plt.plot(xs, data)
    plt.plot([xs[index_i], xs[index_j]], [data[index_i], data[index_j]], 'o', color="r", markersize=10)
    for i in range(length):
        plt.plot(xs_rise[i], networth_final[i], color='r', label='networth')

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))      #成功了！！ 设置显示x轴的间隔
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    # plt.title('networth')
    plt.title(code)
    nn = cal33(datalist, start_time, xs)
    
    plt.show()
    return date[index_i], date[index_j], d, nn
    
def cal33(datalist, start_time, xs):
    date = []
    networth = []
    start1 = 0
    for i in range(len(datalist)):
        date.append(datalist[i][0])
        networth.append(datalist[i][1])
    date.reverse()
    networth.reverse()
    for i in range(len(date)):
        if (date[i] == start_time):
            start1 = i
        continue
    rate = []
    date2 = []
    for j in range(start1, len(date)):
        rate.append(((networth[j] - networth[start1])/networth[start1])*1)
        date2.append(date[j])
    max = -100
    flag = 0
    for i in range(len(rate)):
        if (rate[i]>max):
            max = rate[i]
            flag = i
    '''
    locale.setlocale(locale.LC_ALL, 'en')
    xs = [datetime.strptime(a, '%Y-%m-%d').date() for a in date2]
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    '''
    
    # 绘制图像
    plt.plot(xs[flag], rate[flag], 'o', color="r", markersize=10)
    plt.plot(xs, rate, label='yield')
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    #plt.title('yield and networth')
    # plt.show()
    return date2[flag]
    
    