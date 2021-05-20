#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File    : Fileclient.py

from socket import *
import os
import sys
import json
import struct
from optparse import OptionParser

def recv_file(head_dir, tcp_client):
    filename = head_dir['filename']
    filesize = head_dir['filesize_bytes']
    print("[+]filename: "+filename[0])
    print("[+]filesize: "+ str(filesize))
    recv_len = 0
    f = open(filename[0], 'wb')
    while recv_len < filesize:
        if(filesize > 1024):
            recv_mesg = tcp_client.recv(1024)
            recv_len += len(recv_mesg)
            f.write(recv_mesg)
        else:
            recv_mesg = tcp_client.recv(filesize)
            recv_len += len(recv_mesg)
            f.write(recv_mesg)
    f.close()
    print('[+]文件传输完成!')

def main():
    parser = OptionParser("Usage:%prog -u <target address> -p <port> ")   # 输出帮助信息
    parser.add_option('-u', type='string', dest='ip', help='specify targer ip')  # 获取ip地址参数
    parser.add_option('-p', type='string', dest='port', help='specify targer port')   # 获取ip地址参数
    options,args = parser.parse_args()
    target_port = int(options.port)
    target_ip = options.ip

    tcp_client = socket(AF_INET, SOCK_STREAM)  # socket初始化
    ip_port = ((target_ip, target_port))
    tcp_client.connect_ex(ip_port)
    print('[+]等待服务端应答数据....')
    struct_len = tcp_client.recv(4)  # 接收报头长度
    struct_info_len = struct.unpack('i', struct_len)[0]  # 解析得到报头信息的长度
    print("[+]接收头信息长度：" + str(struct_info_len))
    head_info = tcp_client.recv(struct_info_len)
    head_dir = json.loads(head_info.decode('utf-8'))  # 将报头的内容反序列化
    print("[+]输出头部信息内容：" + str(head_dir))
    recv_file(head_dir, tcp_client)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")