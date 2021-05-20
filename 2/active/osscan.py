#!/usr/bin/python3.7
#!coding:utf-8
from optparse import OptionParser
import os
import re

def ttl_scan(ip):
    ttlstrmatch = re.compile(r'TTL=\d+')
    ttlnummatch = re.compile(r'\d+')
    result = os.popen("ping -n 1 "+ip)
    res = result.read()
    for line in res.splitlines():
        result = ttlstrmatch.findall(line)
        if result:
            ttl = ttlnummatch.findall(result[0])
            if int(ttl[0]) <= 64:  # 判断目标主机响应包中TTL值是否小于等于64
                print("%s  is Linux/Unix"%ip)  # 是的话就为linux/Unix
            else:
                print("%s is Windwows"%ip)  # 反之就是linux
        else:
            pass

def main():
    parser = OptionParser("Usage:%prog -i <target host> ")   # 输出帮助信息
    parser.add_option('-i',type='string',dest='IP',help='specify target host')   # 获取ip地址参数
    options,args = parser.parse_args()
    ip = options.IP
    ttl_scan(ip)

if __name__ == "__main__":
    main() 