#!/usr/bin/python
from optparse import OptionParser
from scapy.all import *


def Scan(ip):
    try:
        dport = random.randint(1, 65535)
        packet = IP(dst=ip)/UDP(dport=80)
        response = sr1(packet,timeout=1.0, verbose=0)
        if response:
            if int(response[IP].proto) == 1:
                time.sleep(0.5)
                print(ip + ' ' + "is up")
            else:
                print(ip + ' ' + "is down")
        else:
            print(ip + ' ' + "is down")
    except:
        pass


def main():

    usage = "Usage: %prog -i <ip address>"	# 输出帮助信息
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="targetIP", help="specify the IP address")	# 获取网段地址
    options, args = parse.parse_args()	#实例化用户输入的参数
    if '-' in options.targetIP:
        # 代码意思举例：192.168.1.1-120
        # 通过'-'进行分割，把192.168.1.1和120进行分离
        # 把192.168.1.1通过','进行分割,取最后一个数作为range函数的start,然后把120+1作为range函数的stop
        # 这样循环遍历出需要扫描的IP地址
        for i in range(int(options.targetIP.split('-')[0].split('.')[3]), int(options.targetIP.split('-')[1]) + 1):
            Scan(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' +
                     options.targetIP.split('.')[2] + '.' + str(i))
    else:
        Scan(options.targetIP)


if __name__ == '__main__':
    main()