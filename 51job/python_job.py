# -*- coding:utf-8 -*-
# --author： jingfeng 
# time: 2018/11/11

import requests
from lxml import etree
from fake_useragent import UserAgent
import re
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='*********',
    db='51job',
    charset='UTF8'

)

cursor = conn.cursor()

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
    print(page)

    results = get_info(page)

    for result in results:
        # with open(r'G:\python3code\爬虫实战\51job\python_jobs.txt', 'a', encoding='utf-8')as f:
        #     f.write(str(result)+'\n')
        try:
            values = ','.join(['"%s"'] * len(result))

            sql = 'insert into python_jobs(`job`,`company_name`,`adress`,`money`,`time`) VALUES (%s)' % (values)
            cursor.execute(sql,
                           (result['job'], result['company_name'], result['adress'], result['money'], result['time']))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        print(result)


def get_info(numbers):
    for i in range(1, eval(numbers) + 1):
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html'.format(i)
        print('爬取第{}页'.format(i))

        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'
        html = response.text

        # print(html)
        selector = etree.HTML(html)

        # 职位    公司名   工作地点  薪资 发布时间
        # print(html)
        jobs = selector.xpath('//p[contains(@class,"t1")]/span/a[@target="_blank"]/text()')
        company_names = selector.xpath('//span[@class="t2"]/a[@target="_blank"]/text()')
        adresses = selector.xpath('//span[@class="t3"]/text()')[1:]
        moneys = re.findall(r'<span class="t4">(.*?)</span>', html)[1:]

        times = selector.xpath('//span[@class="t5"]/text()')[1:]
        # print(len(jobs))
        # print(len(company_names))
        # print(len(adresses))
        # print(len(moneys))
        # print(len(times))
        for job, company_name, adress, money, time in zip(jobs, company_names, adresses, moneys, times):
            yield {
                'job': job.strip(),
                'company_name': company_name,
                'adress': adress,
                'money': money,
                'time': time

            }

get_page_number()

conn.close()
