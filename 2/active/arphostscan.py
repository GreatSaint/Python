#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import optparse
from scapy.all import *

#取IP地址和MAC地址函数
def HostAddress(iface):
    #os.popen执行后返回执行结果
    ipData = os.popen('ipconfig /all'+ iface)
    #对ipData进行类型转换，再用正则进行匹配
    dataLine = ipData.readlines()
    #re.search利用正则匹配返回第一个成功匹配的结果,存在结果则为true
    #取MAC地址
    if re.search('\w\w-\w\w-\w\w-\w\w-\w\w-\w\w',str(dataLine)):
        #取出匹配的结果
        MAC = re.search('\w\w-\w\w-\w\w-\w\w-\w\w-\w\w',str(dataLine)).group(0)
    #取IP地址
    if re.search(r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)',str(dataLine)):
        IP = re.search(r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)',str(dataLine)).group(0)
    #将IP和MAC通过元组的形式返回
    addressInfo = (IP, MAC)
    return addressInfo

#ARP扫描函数
def ArpScan(iface='eth0'):
    #通过HostAddres返回的元组取出MAC地址
    mac = HostAddress(iface)[1]
    #取出本机IP地址
    ip = HostAddress(iface)[0]
    #对本机IP地址并进行分割作为依据元素，用于生成需要扫描的IP地址
    ipSplit = ip.split('.')
    #需要扫描的IP地址列表
    ipList = []
    #根据本机IP生成IP扫描范围
    for i in range(1,255):
        ipItem = ipSplit[0] + '.' + ipSplit[1] + '.' + ipSplit[2] + '.' + str(i)
        ipList.append(ipItem)
    '''
    发送ARP包
    因为要用到OSI二层和三层，所以要写成Ether/ARP。
    因为最底层用到了二层，所以要用srp()发包
    '''
    mac = ':'.join(mac.split('-'))
    print(mac)
    result = srp(Ether(src=mac, dst='FF:FF:FF:FF:FF:FF')/ARP(op=1, hwsrc=mac,hwdst='00:00:00:00:00:00',pdst=ipList),timeout=2,verbose=False)  # iface=iface,
    #读取result中的应答包和应答包内容
    resultAns = result[0].res
    #存活主机列表
    liveHost = []
    #number存回应包总数
    number = len(resultAns)
    print("=====================")
    print("    ARP 探测结果     ")
    print("本机IP地址:"  + ip)
    print("本机MAC地址:" + mac)
    print("=====================")
    for x in range(number):
        IP = resultAns[x][1][1].fields['psrc']
        MAC = resultAns[x][1][1].fields['hwsrc']
        liveHost.append([IP,MAC])
        print("IP:" + IP + "\n\n" + "MAC:" + MAC  )
        print("=====================")
    #把存活主机IP写入文件
    resultFile = open("result","w")
    for i in range(len(liveHost)):
        resultFile.write(liveHost[i][0] + "\n")

    resultFile.close()
if __name__ == '__main__':
    parser = optparse.OptionParser('usage: python %prog -i interfaces \n\n'
                                    'Example: python %prog -i eth0\n')
    #添加网卡参数 -i
    parser.add_option('-i', '--iface', dest='iface', default='', type='string', help='interfaces name')
    (options, args) = parser.parse_args()
    ArpScan(options.iface)