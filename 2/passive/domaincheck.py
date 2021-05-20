#! /usr/bin/env python
# _*_  coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys


def bing_search(site, pages):
    Subdomain = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
               'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip,deflate',
               'referer': "http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=2&FORM=PERE1"
               }
    for i in range(1,int(pages)+1):
        url = "https://cn.bing.com/search?q=site%3a"+site+"&go=Search&qs=ds&first="+ str((int(i)-1)*10) +"&FORM=PERE"
        conn = requests.session()
        conn.get('http://cn.bing.com', headers=headers)
        html = conn.get(url, stream=True, headers=headers, timeout=8)
        # print(html.content)
        soup = BeautifulSoup(html.content, 'html.parser')
        job_bt = soup.findAll('h2')
        for i in job_bt:
            link = i.a.get('href')
            print(link)
            domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            if domain in Subdomain:
                pass
            else:
                Subdomain.append(domain)
                print(domain)

if __name__ == '__main__':
    # site=baidu.com
    if len(sys.argv) == 3:
        site = sys.argv[1]
        page = sys.argv[2]
    else:
        print ("usage: %s baidu.com 10" % sys.argv[0])
        sys.exit(-1)

    Subdomain = bing_search(site, page)




