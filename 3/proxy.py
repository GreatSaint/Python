#urllib代理设置
# from urllib.error import URLError
# from urllib.request import ProxyHandler,build_opener
#
# proxy='127.0.0.1:1087'  #代理地址
#proxy='username:password@IP:port'
# proxy_handler=ProxyHandler({
#     'http':'http://'+proxy,
#     'https':'https://'+proxy
# })
# opener=build_opener(proxy_handler)
# try:
#     response = opener.open('http://httpbin.org/get') #测试ip的网址
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)
#

#requests代理设置
# import requests
#
# proxy='127.0.0.1:1087'  #代理地址
# proxies={
#     'http':'http://'+proxy,
#     'https':'https://'+proxy
# }
# try:
#     response=requests.get('http://httpbin.org/get',proxies=proxies)
#     print(response.text)
# except requests.exceptions.ConnectionError as e:
#     print('error:',e.args)


#
# from selenium import webdriver
#
#
# proxy='127.0.0.1:1087'
# chrome_options=webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://'+proxy)
# browser=webdriver.Chrome(chrome_options=chrome_options)
# browser.get('http://httpbin.org/get'


#代理爬虫
import json
import time
from datetime import datetime
from datetime import timedelta
import requests



def get_data(url):
    proxy = '127.0.0.1:1087'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    try:
        print(url)
        response = requests.get(url,headers=headers, proxies=proxies, timeout=3)
        if response.status_code == 200:
            print(response.text)
            return response.text
        return None
    except requests.exceptions.ConnectionError as e:
        print('error:', e.args)

def parse_data(html):
    data = json.loads(html)['cmts']
    comments = []
    for item in data:
        comment = {
            'id': item['id'],
            'nickName': item['nickName'],
            'cityName': item['cityName'] if 'cityName' in item else '',
            'content': item['content'].replace('\n', ' ', 10),
            'score': item['score'],
            'startTime': item['startTime']
        }
        comments.append(comment)
    return comments



def save_to_txt():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(start_time)
    end_time = '2018-08-10 00:00:00'
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/1203084.json?_v_=yes&offset=0&startTime=' + start_time.replace(' ', '%20')
        try:
            html = get_data(url)    #获取数据方法
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)

        comments = parse_data(html)
        print(comments)
        start_time = comments[14]['startTime']  # 获得末尾评论的时间
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')

        for item in comments:
            with open('data.txt', 'a', encoding='utf-8') as f:
                f.write(str(item['id'])+','+item['nickName'] + ',' + item['cityName'] + ',' + item['content'] + ',' + str(item['score'])+ ',' + item['startTime'] + '\n')


if __name__ == '__main__':
    save_to_txt()
