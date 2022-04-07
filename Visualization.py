# -*- coding = utf-8 -*-
# @Time : 2020/9/24 17:10
# @Author : MIKESHEN
# @File : Visualization.py
# @Software : PyCharm

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

def calculate(datalist):
    date = []
    networth = []
    for i in range(len(datalist)):
        date.append(datalist[i][0])
        networth.append(datalist[i][1])
    date.reverse()
    networth.reverse()
    #打印日期
    print(date)
    data = networth
    index_j = np.argmax(np.maximum.accumulate(data) - data)  # 结束位置
    # print(index_j)
    index_i = np.argmax(data[:index_j])  # 开始位置
    # print(index_i)
    d = (data[index_i] - data[index_j])/data[index_i]  # 最大回撤
    # 生成横纵坐标信息
    dates = date

    # dates_temp = []
    # data_temp = []
    # for b in range(20):
    #     dates_temp.append(dates[b])
    #     data_temp.append(data[b])
    # xs_temp = [datetime.strptime(a, '%Y-%m-%d').date() for a in dates_temp]

    xs = [datetime.strptime(a, '%Y-%m-%d').date() for a in dates]
    ys = range(len(xs))
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # 绘制图像
    plt.plot([xs[index_i], xs[index_j]], [data[index_i], data[index_j]], 'o', color="r", markersize=10)

    plt.plot(xs, data)
    # plt.plot(xs_temp, data_temp, color='r')

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))      #成功了！！ 设置显示x轴的间隔
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.title('networth')
    plt.show()
    return date[index_i], date[index_j], d