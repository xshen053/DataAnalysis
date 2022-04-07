import urllib.request, urllib.error #制定URL，获取网页数据
import re
from bs4 import BeautifulSoup  #网页解析，获取数据
findpage = re.compile(r'pages:(\d*)')
findmanager = re.compile(r'<td>基金经理：<a href="(.*?)">(.*?)</a></td>')
findlink = re.compile(r'<td class="td02"><a href="(.*?)">')
findprice1 = re.compile(r'<td class="zhang">(.*?)%</td>')
findprice2 = re.compile(r'<td class="die">(.*?)%</td>')
finddate = re.compile(r'<td>(.*?)</td>')
findrate = re.compile(r'<td class="tor bold">(.*?)</td>')
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
    print(html)
    return html
# askURL('http://fund.eastmoney.com/003321.html')
html = askURL("http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=006401&sdate=2001-12-18&edate=2020-05-18&per=20&page=1")
datalist = []
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
    print(datalist)
anaData(datalist, html)
# soup = BeautifulSoup(html, "html.parser")
# price = []
# for item in soup.find_all('td', class_=["zhang", "die"]):  # 查找符合要求的字符串，形成列表，class_加下划线代表属性（类别）不是类
#     item = str(item)
#     print(item)
#     if len(re.findall(findprice1, item)) != 0:
#         price.append(re.findall(findprice1, item)[0])
#     if len(re.findall(findprice2, item)) != 0:
#         price.append(re.findall(findprice2, item)[0])
#     else:
#         continue
# print(price)
# sum = 0
# for i in range(len(price)):
#     price[i] = float(price[i])
#     sum = sum + price[i]
#
# price.sort()
# for i in range(len(price)):
#     price[i] = "%.2f%%" % price[i]
# print(price)
# print(sum/len(price))