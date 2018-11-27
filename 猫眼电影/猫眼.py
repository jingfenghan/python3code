# -*- coding:utf-8 -*-
# --author： jingfeng
# time: 2018/11/25


import requests
from requests.exceptions import RequestException
import re


def get_one_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.221 Safari/537.36 SE 2.X '
                             'MetaSr 1.0'}
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        print(item)
        yield {'index': item[0],
               'image': item[1],
               'title': item[2].strip(),
               'actor': item[3].strip()[3:],
               'time': item[4].strip()[5:],
               'score': item[5] + item[6]
               }


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    print(url)
    html = get_one_page(url)

    for item in parse_one_page(html):
        print(item)


for i in range(0, 100, 10):
    main(i)
