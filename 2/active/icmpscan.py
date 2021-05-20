#!/usr/bin/python
#coding:utf-8
from scapy.all import *
from random import randint
from optparse import OptionParser

def Scan(ip):
    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)
    packet=IP(dst=ip, ttl=64, id=ip_id)/ICMP(id=icmp_id, seq=icmp_seq)/b'rootkit'
    result = sr1(packet, timeout=1, verbose=False)
    if result:
        for rcv in result:
            scan_ip = rcv[IP].src
            print(scan_ip + '--->' 'Host is up')
    else:
        print(ip + '--->' 'host is down')

def main():
    parser = OptionParser("Usage:%prog -i <target host> ")   # 输出帮助信息
    parser.add_option('-i',type='string',dest='IP',help='specify target host')   # 获取ip地址参数
    options,args = parser.parse_args()
    print("Scan report for " + options.IP + "\n")
    # 判断是单台主机还是多台主机
    # ip中存在-,说明是要扫描多台主机
    if '-' in options.IP:
    # 代码意思举例：192.168.1.1-120
    # 通过'-'进行分割，把192.168.1.1和120进行分离
    # 把192.168.1.1通过','进行分割,取最后一个数作为range函数的start,然后把120+1作为range函数的stop
    # 这样循环遍历出需要扫描的IP地址
        for i in range(int(options.IP.split('-')[0].split('.')[3]), int(options.IP.split('-')[1]) + 1):
            Scan(
            options.IP.split('.')[0] + '.' + options.IP.split('.')[1] + '.' + options.IP.split('.')[
                2] + '.' + str(i))
            time.sleep(0.2)
    else:
        Scan(options.IP)

    print("\nScan finished!....\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")