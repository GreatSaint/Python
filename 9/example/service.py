#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File    : Fileserver.py

import socketserver
import os
import re
import json
import struct
from optparse import OptionParser

def sendFile(conn, head_info,head_info_len,filename):
    try:
        conn.send(head_info_len)
        conn.send(head_info.encode('utf-8'))
        with open(filename, 'rb') as f:
            conn.sendall(f.read())
        print('[+]send success! '+filename)
    except:
        print('[-]send fail! ' + filename)

def operafile(filename):
    filesize_bytes = os.path.getsize(filename)
    pattern = re.compile(r'([^<>/\\\|:""\*\?]+\.\w+$)')
    data = pattern.findall(filename)
    head_dir = {
        'filename': data,
        'filesize_bytes': filesize_bytes,
    }
    head_info = json.dumps(head_dir)
    head_info_len = struct.pack('i', len(head_info))
    return head_info_len, head_info

class MyServer(socketserver.BaseRequestHandler):
    buffsize = 1024
    def handle(self):
        print('[+]远程客户端ip地址：', self.client_address[0],'\n')
        while True:
            filename = input('请输入要发送的文件名>>>').strip() #移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
            if(filename == "exit"):
                break
            head_info_len, head_info = operafile(filename)
            sendFile(self.request,head_info,head_info_len,filename)
        self.request.close()

def main():
    parser = OptionParser("Usage:%prog -p <port> ")   # 输出帮助信息
    parser.add_option('-p',type='string',dest='port',help='specify targer port')   # 获取ip地址参数
    options,args = parser.parse_args()
    port = int(options.port)

    print("[+]listening at " + str(port))
    s = socketserver.ThreadingTCPServer(('0.0.0.0', port), MyServer)  #
    s.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")
