#!/usr/bin/python3.7
#!coding:utf-8
from optparse import OptionParser
import time
import socket
import os
import re

SIGNS = (
    # 协议 | 版本 | 关键字
    b'FTP|FTP|^220.*FTP',
    b'MySQL|MySQL|mysql_native_password',
    b'oracle-https|^220- ora',
    b'Telnet|Telnet|Telnet',
    b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
    b'VNC|VNC|^RFB',
    b'IMAP|IMAP|^\* OK.*?IMAP',
    b'POP|POP|^\+OK.*?',
    b'SMTP|SMTP|^220.*?SMTP',
    b'Kangle|Kangle|HTTP.*kangle',
    b'SMTP|SMTP|^554 SMTP',
    b'SSH|SSH|^SSH-',
    b'HTTPS|HTTPS|Location: https',
    b'HTTP|HTTP|HTTP/1.1',
    b'HTTP|HTTP|HTTP/1.0',
)
def regex(response, port):
    text = ""
    if re.search(b'<title>502 Bad Gateway', response):
        proto = {"Service failed to access!!"}
    for pattern in SIGNS:
        pattern = pattern.split(b'|')
        if re.search(pattern[-1], response, re.IGNORECASE):
            proto = "["+port+"]" + " open " + pattern[1].decode()
            break
        else:
            proto = "["+port+"]" + " open " + "Unrecognized"
    print(proto)

def request(ip,port):
    response = ''
    PROBE = 'GET / HTTP/1.0\r\n\r\n'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((ip, int(port)))
    if result == 0:
        try:
            sock.sendall(PROBE.encode())
            response = sock.recv(256)
            if response:
                regex(response, port)
        except ConnectionResetError:
            pass
    else:
        pass
    sock.close()

def main():
    parser = OptionParser("Usage:%prog -i <target host> ")   # 输出帮助信息
    parser.add_option('-i',type='string',dest='IP',help='specify target host')   # 获取ip地址参数
    parser.add_option('-p', type='string', dest='PORT', help='specify target host')  # 获取ip地址参数
    options,args = parser.parse_args()
    ip = options.IP
    port = options.PORT
    print("Scan report for "+ip+"\n")
    for line in port.split(','):
        request(ip,line)
        time.sleep(0.2)
    print("\nScan finished!....\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")