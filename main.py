# -*- coding = utf-8 -*-
# @Time : 2020/9/18 21:35
# @Author : MIKESHEN
# @File : spider.py
# @Software : PyCharm


import urllib.request, urllib.error #制定URL，获取网页数据
from bs4 import BeautifulSoup  #网页解析，获取数据
import re
import xlrd
import xlwt
from xlutils.copy import copy
from Yield import yield1
from Visualization_second import calculate
from YieldCal import cal
from find_info import findthings, find_ROI
findpage = re.compile(r'pages:(\d*)')
finddate = re.compile(r'<td>(.*?)</td>')
findrate = re.compile(r'<td class="tor bold">(.*?)</td>')
findname = re.compile(r'<title>(.*?)基金净值_估值_行情走势—天天基金网</title>')
#成立日
foundday = re.compile(r'<td><span class="letterSpace01">成 立 日</span>：(.*?)</td>')
def main():
    baseurl = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code="
    price = []
    print("请输入股票代码：6位")
    code = input()
    name = anaName(code)
    print("您查询的基金为\'%s'" % name)
    url = "http://fund.eastmoney.com/%s.html" % code
    html = askURL2(url)
    date, manager, link = findthings(html)
    html_ROI = askURL(link)
    price, ROI = find_ROI(html_ROI)
    print("该基金成立日为\'%s'" % date)
    print("基金经理为\'%s'" % manager)
    print("详细信息：%s" % link)
    print(price)
    print("平均回报率为:%.2f%%" % ROI)
    print("请输入结束日期，格式xxxx-xx-xx")
    enddate = input()
    print("清输入开始日期，计算开始日期——结束日期的收益率，格式xxxx-xx-xx")
    start_time = input()

    #获得第一页page
    page= ana_getData_page(baseurl, code, enddate)
    #获得完整数据
    datalist = getData_single(baseurl, code, enddate, page)
    #可视化部分
    datalist = data_process(datalist)
    rate = yield1(datalist, start_time)
    date_yield_max = cal(datalist, start_time)
    high, low, maxrate = calculate(datalist)
    print("最高点日期%s" % high)
    print("最低点日期%s" % low)
    print("最大回撤率:")
    print("%.2f%%" % (maxrate * 100))
    print("%s到%s的收益率为:" %(start_time, enddate))
    print("%.2f%%" % (rate * 100))
    print("自%s算起%s卖出收益率最大" % (start_time, date_yield_max))
    savepath = "基金数据\%s基金的3年净值.xls" % code
    saveData(datalist, savepath, code)

#得到一个URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
    }
    request =urllib.request.Request(url, headers = head)
    html = ""
    try:
        response = urllib.request.urlopen(request, timeout=500)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e, "code"): #判断e这个对象里面是否包含code这个类型
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html
#得到成立日，用的请求头是谷歌的
def askURL2(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"): #判断e这个对象里面是否包含code这个类型
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html
#爬取网页
def getData(baseurl, code, j):
    datalist = []
    for i in range(1, 41):
    # for i in range(1, 150):
        url = baseurl + code[j] + str("&sdate=2001-12-18&edate=2020-09-18&per=50&page=%d" % i)
        html = askURL(url)
        anaData(datalist, html)
        # 休息1秒再做
        # if (i % 10 == 0):
        #     time.sleep(0.1)
    return datalist

#爬取单个基金版本:从成立开始爬
def getData_single(baseurl, code, date, page):
    datalist = []
    # for i in range(1, 41):
    for i in range(1, page+1):
        url = baseurl + code + str("&sdate=2001-12-18&edate=%s&per=50&page=%d" % (date, i))
        html = askURL(url)
        anaData(datalist, html)
        # 休息1秒再做
        # if (i % 10 == 0):
        #     time.sleep(0.1)
    return datalist
#获取开始页数，从成立开始爬
def ana_getData_page(baseurl, code, date):
    url = baseurl + code + str("&sdate=2001-12-18&edate=%s&per=50&page=1" % date)
    html = askURL(url)
    page = re.findall(findpage, html)[0]
    page = int(page)
    return page

def anaData(datalist, html):
    i = 0
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('tr'):
        if i == 0:
            i += 1
            continue
        data = []
        item = str(item)
        if (len(re.findall(finddate, item))<1 or len(re.findall(findrate, item))<1 ):
            continue
        elif (re.findall(findrate, item)[0] == ''):         #防止出现某一天数据为''的情况
            date = re.findall(finddate, item)[0]
            data.append(date)
            data.append(0)
        else:
            date = re.findall(finddate, item)[0]
            data.append(date)
            price = re.findall(findrate, item)[1]       #1是累计净值
            data.append(price)
        datalist.append(data)
#根据基金代码获取名字信息
def anaName(code):
    html = askURL("http://fund.eastmoney.com/%s.html" % code)
    soup = BeautifulSoup(html, "html.parser")
    i = 0
    item = []
    for item in soup.find_all('title'):
        if i == 0:
            i += 1
            continue
    item = str(item)
    name = re.findall(findname, item)[0]
    return name
#保存数据到excel
def saveData(datalist, savepath, code):
    print("保存中")
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet("%s基金的3年净值" % code, cell_overwrite_ok=True)
    col = ("日期", code)
    for i in range(0, 2):
        sheet.write(0, i, col[i])
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(0, 2):
            sheet.write(i+1, j, data[j])

    book.save(savepath)
    # print("done!")



def write_excel_xls_append(path, value, namelist, page):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[page])  # 获取工作簿中所有表格中的的第一个表格
    cols_old = worksheet.ncols  # 获取表格中已存在的数据的列数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(page)  # 获取转化后工作簿中的第一个表格
    for j in range(len(namelist)):

        new_worksheet.write(0, cols_old+j, namelist[j])   #追加标题
        for i in range(len(value[j])):
            new_worksheet.write(i+1, cols_old+j, value[j][i][1])  # 追加写入数据
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def data_process(datalist):                     #把日期和净值分离成两个列表
    for i in range(len(datalist)):
        datalist[i][1] = float(datalist[i][1])

    return datalist


if  __name__ == '__main__':
   main()
   print("完成")
