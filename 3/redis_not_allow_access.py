#-*- coding:utf-8 -*-
import socket
import sys
import getopt

#banner信息
def banner():
    print('欢迎来到地狱')
#使用规则
def usage():
    print('-h: --help 帮助;')
    print('-p: --port 端口')
    print('-u: --url  域名;')
    print('-s: --type Redis')
    sys.exit()

##未授权函数检测
def redis_unauthored(url,port):
    result = []
    s = socket.socket()
    payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
    socket.setdefaulttimeout(10)
    for ip in url:
        try:
            s.connect((ip, int(port)))
            s.sendall(payload.encode())
            recvdata = s.recv(1024).decode()
            if recvdata and 'redis_version' in recvdata:
                 result.append(str(ip)+':'+str(port)+':'+'\033[1;32;40msuccess\033[0m')
        except:
            pass
            result.append(str(ip) + ':' + str(port) + ':' + '\033[1;31;40mfailed \033[0m')
        s.close()
    return(result)

def url_list(li):
    ss = []
    i = 0
    j = 0
    zi = []
    for s in li:
        a = s.find('-')
        i = i + 1
        if a != -1:
            ss = s.rsplit("-")
            j = i
            break
    for s in range(int(ss[0]), int(ss[1]) + 1):
        li[j - 1] = str(s)
        aa = ".".join(li)
        zi.append(aa)
    return zi

#执行url
def url_exec(url):
    i = 0
    zi = []
    group = []
    group1 = []
    group2 = []
    li = url.split(".")
    if(url.find('-')==-1):
        group.append(url)
        zi = group
    else:
        for s in li:
            a = s.find('-')
            if a != -1:
                i = i+1
        zi = url_list(li)
        if i > 1 :
            for li in zi:
                zz = url_list(li.split("."))
                for ki in zz:
                    group.append(ki)
            zi = group
            i = i-1
        if i > 1 :
            for li in zi:
                zzz = url_list(li.split("."))
                for ki in zzz:
                    group1.append(ki)
            zi = group1
            i = i - 1
        if i > 1 :
            for li in zi:
                zzzz = url_list(li.split("."))
                for ki in zzzz:
                    group2.append(ki)
            zi = group2
    return zi
#主函数，传入输入参数进入
def start(argv):
    thread = 1
    dict = {}
    url = ""
    type = ""
    if len(sys.argv) < 2:
        print("-h 帮助信息;\n")
        sys.exit()
    #定义异常处理
    try:
        banner()
        opts,args = getopt.getopt(argv,"-u:-p:-s:-h")
    except getopt.GetoptError:
        print('Error an argument!')
        sys.exit()
    for opt,arg in opts:
        if opt == "-u":
            url = arg
        elif opt == "-s":
            type = arg
        elif opt == "-p":
            port = arg
        elif opt == "-h":
            print(usage())
    launcher(url,type,port)

#输出结果格式设计
def output_exec(output,type):
    print("\033[1;32;40m"+type+"......\033[0m")
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    print("|         ip         |    port   |     status  |")
    for li in output:
        print("+-----------------+-----------+--------------+")
        print("|   "+li.replace(":","   |    ")+"  | ")
    print("+----------------+------------+---------------+\n")
    print("[*] shutting down....")

#漏洞回调函数
def launcher(url,type,port):
    #未授权访问类型
    if type == "Redis":
        output=redis_unauthored(url_exec(url),port)
        output_exec(output,type)

if __name__ == '__main__':
    #定义异常
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")






