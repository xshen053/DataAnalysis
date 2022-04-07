# -*- coding = utf-8 -*-
# @Time : 2020/9/26 13:16
# @Author : MIKESHEN
# @File : collectdate.py
# @Software : PyCharm
import re
def collect_date(datalist):
    find = re.compile(r'(.*?)-(.*?)-(.*?)')

    date = []
    networth = []
    for i in range(len(datalist)):
        date.append(datalist[i][0])
        networth.append(datalist[i][1])
    date.reverse()
    networth.reverse()

    first = re.findall(find, date[0])
    startdate = []                      #存放开始日期的标签
    enddate = []                        #存放结束日期的标签
    flag = 0
    for i in range(1, len(date)):
        temp = re.findall(find, date[i])
        if (first[0][1] == temp[0][1]):
            if (flag == 0):
                startdate.append(0)
            else:
                continue
        else:
            startdate.append(i)
            if (flag == 1):
                enddate.append(i - 1)
        first = temp
        flag = 1
    # 最后一个月还没结束，则加上最后一天的日期
    if enddate[len(enddate) - 1] != (len(date) - 1):
        enddate.append(len(date) - 1)
    startdate_rise = []             #存放最终数据
    enddate_rise = []               #存放最终数据
    length = len(enddate)
    for i in range(length):
        if(networth[enddate[i]] > networth[startdate[i]]):
            startdate_rise.append(startdate[i])
            enddate_rise.append(enddate[i])
    date_final2 = []
    networth_final2 = []
    for i in range(len(startdate_rise)):
        date_final = []
        networth_final = []
        for j in range(startdate_rise[i], enddate_rise[i]+1):
            date_final.append(date[j])
            networth_final.append(networth[j])
        date_final2.append(date_final)
        networth_final2.append(networth_final)

    len_rise = len(date_final2)                 #收益为正月份数量
    len_all = len(startdate)                    #总月份数量
    print("收益率为正数的月份为:")
    for i in date_final2:
        print(i[0])
    print("正月份数量:%d, 总月份数量:%d" % (len_rise, len_all))
    print("占比%.2f%%" % (len_rise/len_all * 100))
    return date_final2, networth_final2