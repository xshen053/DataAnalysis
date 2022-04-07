# -*- coding = utf-8 -*-
# @Time : 2020/9/24 23:30
# @Author : MIKESHEN
# @File : YieldCal.py
# @Software : PyCharm
#每天收益率可视化
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
def cal(datalist, start_time):
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
        rate.append(((networth[j] - networth[start1])/networth[start1])*100)
        date2.append(date[j])
    max = -100
    flag = 0
    for i in range(len(rate)):
        if (rate[i]>max):
            max = rate[i]
            flag = i
    xs = [datetime.strptime(a, '%Y-%m-%d').date() for a in date2]
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # 绘制图像
    plt.plot(xs[flag], rate[flag], 'o', color="r", markersize=10)
    plt.plot(xs, rate)
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.title('yield')
    plt.show()
    return date2[flag]
