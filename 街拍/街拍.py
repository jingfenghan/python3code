import requests
from urllib.parse import urlencode
import os


def getPage(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)  # js 把data传进来构成完整url
    headers = {'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/63.0.3239.132 Safari/537.36'}
    print(url)
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        html = response.json()
        result = html['data']
        return result

    return None


def download_image(title, image_urls):
    file = os.getcwd() + '\\图片' + '\\' + title
    if not os.path.exists(title):
        os.makedirs(title)
    headers = {'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/63.0.3239.132 Safari/537.36'}

    for url in image_urls:

        if isinstance(url, dict):

            id = url['url'].split('/')[-1]
            print(id)
            url = 'http://p99.pstatp.com/origin/' + id
        else:
            id = url.split('/')[-1][0:30]

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            url = 'http://p99.pstatp.com/origin/pgc-image/' + id

            response = requests.get(url, headers=headers)

        with open(file + '\\' + id + '.jpg', 'wb') as f:
            f.write(response.content)


def main():
    for i in range(0, 200, 20):
        result = getPage(i, '街拍美女')

        for x in result[:]:

            id = x.get('id')
            title = x.get('title')
            if not title:
                title = x.get('summary')

            image_list = x.get('image_list')
            print(title, image_list)
            if title:
                download_image(title, image_list)


if __name__ == '__main__':
    main()
