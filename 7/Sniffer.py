#!/usr/bin/python3
# -*- coding: utf-8 -*-

from scapy.all import *
import time
import optparse


# 时间戳转换函数
def TimeStamp2Time(timeStamp):
    timeTmp = time.localtime(timeStamp)
    myTime = time.strftime("%Y-%m-%d %H:%M:%S", timeTmp)
    return myTime


# 回调打印函数
def PackCallBack(packet):
     print("*"*30)
     # 打印源IP，源端口，目的IP，目的端口
     print("[%s]Source:%s:%s--->Target:%s:%s"%(TimeStamp2Time(packet.time),packet[IP].src,packet.sport,packet[IP].dst,packet.dport))
     #print("[%s]Source:%s:%s--->Target:%s:%s"%(packet.time, packet[IP].src, 4444, packet[IP].dst, 5555))
     # 打印输出数据包
     print(packet.show())
     print("*"*30)


if __name__ == '__main__':
    parser = optparse.OptionParser("Example:python %prog -i 127.0.0.1 -c 5 -o ms08067.pcap\n")
    #添加IP参数 -i
    parser.add_option('-i', '--IP', dest='hostIP',
                     default="127.0.0.1", type='string',
                    help='IP address [default = 127.0.0.1]')
    #添加数据包总数参数-c
    parser.add_option('-c', '--count', dest='packetCount',
                     default=5, type='int',
                     help='Packet count [default = 5]')
    #添加保存文件名参数-o
    parser.add_option('-o', '--output', dest='fileName',
                     default="ms08067.pcap", type='string',
                     help='save filename [default = ms08067.pcap]')
    (options, args) = parser.parse_args()
    defFilter = "dst " + options.hostIP
    packets = sniff(filter=defFilter, prn=PackCallBack, count=options.packetCount)
    # 保存输出文件
    wrpcap(options.fileName, packets)