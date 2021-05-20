import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('127.0.0.1', 8002))
except Exception as e:
    print('server not found or not open')
while True:
    c = input('Input the content you want to send:')
    s.sendall(c.encode())
    data = s.recv(1024).decode()
    print('Recv:', data)
    if c.lower() == 'bye':
        break
s.close()