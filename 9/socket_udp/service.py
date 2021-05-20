import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 8001))
while True:
    data, addr = s.recvfrom(1024)
    print(data.decode())
    if data.decode().lower() == 'exit':
        break

s.close()