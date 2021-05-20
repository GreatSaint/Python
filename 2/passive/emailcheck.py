#! /usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import getopt
import requests
from bs4 import BeautifulSoup
import re
import time
import threading

#banner信息
def banner():
    print('欢迎来到德莱联盟')
#使用规则
def usage():
    print('-h: --help 帮助;')
    print('-u: --url  域名;')
    print('-p: --pages 页数;')
    print('eg: python -u "www.baidu.com" -p 100'+'\n')
    sys.exit()
##未授权函数检测

#主函数，传入输入参数进入
def start(argv):
    url = ""
    pages = ""
    if len(sys.argv) < 2:
        print("-h 帮助信息;\n")
        sys.exit()
    #定义异常处理
    try:
        banner()
        opts,args = getopt.getopt(argv,"-u:-p:-h")
    except getopt.GetoptError:
        print('Error an argument!')
        sys.exit()
    for opt,arg in opts:
        if opt == "-u":
            url = arg
        elif opt == "-p":
            pages = arg
        elif opt == "-h":
            print(usage())
        threader(url, pages)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        if self.args[1] < 1:
            pass
        else:
            self.result = self.func(*self.args)  # 在执行函数的同时，把结果赋值给result,然后通过get_result函数获取返回的结果

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None


def threader(url,pages):
    launcher(url,pages)

    #漏洞回调函数
def launcher(url,pages):
    if len(pages)< 1:
        pass
    else:
        for page in range(1,int(pages)+1):
            keyword(url,page)


def keyword(url,page):
    threads = []
    email_sum = []
    email_num = []
    key_words = ['email', 'mail', 'mailbox', '邮件', '邮箱', 'postbox']
    for key_word in key_words:
        t = MyThread(emails, args=(url, page,key_word))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()  # 一定执行join,等待子进程执行结束，主进程再往下执行
        email_num.append(t.get_result())
    for email in email_num:
        for list in email:
            if list in email_sum:
                pass
            else:
                email_sum.append(list)
                print(list)

def emails(url,page,key_word):
    bing_emails = bing_search(url, page, key_word)
    baidu_emails = baidu_search(url, page, key_word)
    sum_emails = bing_emails + baidu_emails
    return sum_emails



def bing_search(url,page,key_word):
    referer = "http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=1&FORM=PERE1"
    conn = requests.session()
    bing_url = "http://cn.bing.com/search?q=" + key_word + "+site%3a" + url + "&qs=n&sp=-1&pq=" + key_word + "site%3a" + url + "&first=" + str(
        (page-1)*10) + "&FORM=PERE1"
    conn.get('http://cn.bing.com', headers=headers(referer))
    r = conn.get(bing_url, stream=True, headers=headers(referer), timeout=8)
    emails = search_email(r.text)
    return emails

def baidu_search(url,page,key_word):
    email_list = []
    emails = []
    referer = "https://www.baidu.com/s?wd=email+site%3Abaidu.com&pn=1"
    baidu_url = "https://www.baidu.com/s?wd="+key_word+"+site%3A"+url+"&pn="+str((page-1)*10)
    conn = requests.session()
    conn.get(referer,headers=headers(referer))
    r = conn.get(baidu_url, headers=headers(referer))
    soup = BeautifulSoup(r.text, 'lxml')
    tagh3 = soup.find_all('h3')
    for h3 in tagh3:
        href = h3.find('a').get('href')
        try:
            r = requests.get(href, headers=headers(referer),timeout=8)
            emails = search_email(r.text)
        except Exception as e:
            pass
        for email in emails:
            email_list.append(email)
    return email_list

def search_email(html):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",html,re.I)
    return emails

def headers(referer):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
               'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip,deflate',
               'Referer': referer
               }
    return headers


if __name__ == '__main__':
    #定义异常
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")