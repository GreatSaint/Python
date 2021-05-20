import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8002))
s.listen(1)
print('Listen  at port：8002')
conn, addr = s.accept()
print('Connected by ', addr)
while True:
    data = conn.recv(1024)
    data = data.decode()
    print('Recv：', data)
    c = input('Input the content you want to send:')
    conn.sendall(c.encode())
    if c.lower() == 'bye':   # 转小写
        break
conn.close()
s.close()