# -*- coding:utf-8 -*-
# --author： jingfeng
# time: 2018/11/16

import gevent
import gevent.monkey

gevent.monkey.patch_all()

import requests
from lxml import etree
from fake_useragent import UserAgent
import re
import csv

file = open(r'G:\python3code\爬虫实战\51job\协程版python.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(file)
writer.writerow(['job', 'company_name', 'adress', 'money', 'time'])

ua = UserAgent()
headers = {'User-Agent': ua.random}
print(headers)


def get_page_number():
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html'
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    html = response.text
    number = re.findall('<span class="td">(.*?)</span>', html)[0]
    page = re.search(r'(\d+)', number).group()

    return page


def get_info(numbers, writer):
    for i in numbers:
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html'.format(str(i))
        print('爬取第{}页'.format(i))

        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'
        html = response.text

        selector = etree.HTML(html)

        # 职位    公司名   工作地点  薪资 发布时间
        # print(html)
        jobs = selector.xpath('//p[contains(@class,"t1")]/span/a[@target="_blank"]/text()')
        company_names = selector.xpath('//span[@class="t2"]/a[@target="_blank"]/text()')
        adresses = selector.xpath('//span[@class="t3"]/text()')[1:]
        moneys = re.findall(r'<span class="t4">(.*?)</span>', html)[1:]
        times = selector.xpath('//span[@class="t5"]/text()')[1:]
        print(len(jobs), len(company_names), len(moneys))

        for job, company_name, adress, money, time in zip(jobs, company_names, adresses, moneys, times):
            list = [job.strip(), company_name, adress, money, time]
            print(list)
            writer.writerow(list)


pages_number = get_page_number()

# 构建协程对列
mylist = [x for x in range(1, eval(pages_number) + 1)]

xclist = [[], [], [], [], [], [], [], [], [], []]
N = len(xclist)

for i in range(len(mylist)):
    xclist[i % N].append(mylist[i])  # 取余寻找列表，均匀分配数据

tasklist = []

for i in range(10):
    tasklist.append(gevent.spawn(get_info, xclist[i], writer))

gevent.joinall(tasklist)
