import socket
import uuid
import sys

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


ip = socket.gethostbyname(socket.gethostname())
mac = get_mac_address()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

info = "ip addr:" + ip + "\n" + "mac addr:" + mac

s.sendto(info.encode(), ("127.0.0.1", 8001))
s.sendto(sys.argv[1].encode(), ("127.0.0.1", 8001))
s.close()