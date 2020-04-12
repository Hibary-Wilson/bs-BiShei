#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 18:19
# @Author  : Mr.Huang
# @File    : shujuHuoQu.py
# @Software: PyCharm

import urllib
from urllib.parse import *
from bs4 import BeautifulSoup
import string
import random
import pandas as pd
import os
headers = ["Mozilla/5.0 (Windows NT 6.1; Win64; rv:27.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" 
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:27.0) Gecko/20100101 Firfox/27.0"
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"  
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:10.0) Gecko/20100101 Firfox/10.0"  
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/21.0.1180.110 Safari/537.36"  
      "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:10.0) Gecko/20100101 Firfox/27.0"  
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36"  
       "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:27.0) Gecko/20100101 Firfox/27.0"  
       "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"  
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'  
        ]
def get_content(url,headers,str):
    random_header = random.choice(headers)
    req = urllib.request.Request(url)
    req.add_header("User-Agent",random_header)
    req.add_header("Get",url)
    req.add_header("Host","{0}.zhaopin.com".format(str))
    req.add_header("refer","http://{0}.zhaopin.com/".format(str))
    try:
        html = urllib.request.urlopen(req)
        contents = html.read()
        #print(contents)
        #判断输出内容contents是否是字节格式
        if isinstance(contents,bytes):
            #转成字符串格式
            contents = contents.decode('utf-8')
        else:
            print('输出格式正确，可以直接输出')
        #输出的是字节格式，需要将字节格式解码转成‘utf-8’
        return (contents)
    except Exception as e:
        print(e)
def get_links_from(job,city,page):
    #job:工作名称
    #city：工作城市
    #page：表示第几页
    #urls:所有列表的超链接，即子网网址
    urls = []
    for i in range(page):
        url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?j1={0}&kw={1}&p={2}&isadv=0'.format(str(city),str(job),i)
        url = quote(url,safe=string.printable)
        info = get_content(url,headers,'sou')
        soup = BeautifulSoup(info,'lxml')  #设置解析器为“lxml”
        #print(soup)
        link_urls = soup.select('td.zwmc a')
        for url in link_urls:
            urls.append(url.get('href'))
    #print(urls)
    return (urls)
def get_recuite_info(job,city,page):
    #获取招聘网页信息
    urls = get_links_from(job,city,page)
    path = '/data/zhilian/'
    if os.path.exists(path) == False:
        os.makedirs(path)
    for url in urls:
        print(url)
        file = url.split('/')[-1]
        print(file)
        str = url.split('/')[2].split('.')[0]
        html = get_content(url,headers,str)
        if html != None and file !='':
            with open(path+file,'w') as f:
                f.write(html)
"""
**************获取招聘信息**************
"""
if __name__ == '__main__':
    city = '北京%2b 上海%2b 广州%2b 深圳'
    get_recuite_info('大数据',city,100)