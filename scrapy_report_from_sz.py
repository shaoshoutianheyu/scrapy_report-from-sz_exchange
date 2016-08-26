# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:08:49 2016

@author: Administrator
"""

 
# 加载包
import requests
import xlwt
from bs4 import BeautifulSoup
# 一些重要参数
stock_id = '000002'
endTime = '2016-08-26' 
startTime = "2015-08-26"
# 从第一页开始
pageNo = str(1)

s = requests.session()
# 网址
url = 'http://disclosure.szse.cn/m/search0425.jsp'
# 请求头信息
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'Referer':'http://disclosure.szse.cn/m/search0425.jsp',
        'Host':'disclosure.szse.cn',
        'Cookie':'JSESSIONID=15F0440A4E92E68B9617B84337A3F661',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'DontTrackMeHere':'gzip, deflate',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        "Upgrade-Insecure-Requests	":"1"
    }
# post 信息内容
dt = {'endTime':endTime,'pageNo':pageNo,'noticeType':'','startTime':startTime,'stockCode':stock_id
      }
# 需要post 一些信息
r = s.post(url, data=dt, headers=headers)
# 记得看网页源码的meta  看看编码是什么
h = r.content.decode('gb2312')
# 化成BS对象  
obj = BeautifulSoup(h,'lxml')

# 应该首先弄明白一共多少页
# 页
page_lst =  [] 
 
for i in obj.find_all('td',{'class':'page12'}):
    for q in i.find_all('span'):
       page_lst.append(q.string)
# 当前页
current_page = page_lst[0]
# 总页数
total_page = int(page_lst[1])+1


# 这个时候只是知道有多少页了 需要重新加载网页
for page in range(1,total_page):
  
    print("第"+"%s"%page + "页开始下载")
    
    dt = {'endTime':endTime,'pageNo':str(page),'noticeType':'','startTime':startTime,'stockCode':stock_id
         }
    # 需要post 一些信息
    r = s.post(url, data=dt, headers=headers)
    # 记得看网页源码的meta  看看编码是什么
    h = r.content.decode('gb2312')
    # 化成BS对象  
    obj = BeautifulSoup(h,'lxml')

    # 循环下载report
    for i in obj.find_all('a',{'target':'new'}):
        
        child_path = i.attrs['href'] 
        path = 'http://disclosure.szse.cn' + r'/' + child_path
        name = i.string + '.pdf'
        urllib.request.urlretrieve(path, name)
        print(name + "is over!!!!!!"+"_"*4+"还在第%s页"%page)
 
 
 
 