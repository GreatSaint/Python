import os

def banner():
    print('欢迎来到洛圣都')

def start():
    banner()
    info = os.system("whoami\n")
    while True:
        info = input("\n Btea->")
        os.system(info)

if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")