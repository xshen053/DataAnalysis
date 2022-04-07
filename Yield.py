# -*- coding = utf-8 -*-
# @Time : 2020/9/24 23:01
# @Author : MIKESHEN
# @File : Yield.py
# @Software : PyCharm
#计算收益率函数
def yield1(datalist, start_time):
    date = []
    networth = []
    start2 = 0
    for i in range(len(datalist)):
        date.append(datalist[i][0])
        networth.append(datalist[i][1])
    date.reverse()
    networth.reverse()
    for i in range(len(date)):
        if (date[i] == start_time):
            start2 = i
        continue
    end = len(networth)
    # print(date[start2])
    # print(date[end-1])
    rate = (networth[end-1] - networth[start2])/networth[start2]
    return rate
