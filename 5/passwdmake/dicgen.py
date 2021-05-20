#!/usr/bin/python3
# -*- coding: utf-8 -*-

import itertools


def ReadInformationList():
    try:
        # 读取个人信息文件，并按行存入lines
        informationFile = open('person_information', 'r')
        lines = informationFile.readlines()
        for line in lines:
            infolist.append(line.strip().split(':')[1])
    except Exception as e:
        print(e + "\n")
        print("Read person_information error!")


def CreateNumberList():
    # 数字元素
    words = "0123456789"
    # 利用itertools来产生不同数字排列,数字组合长度为3
    itertoolsNumberList = itertools.product(words, repeat=3)
    for number in itertoolsNumberList:
        # 写入数字列表备用
        numberList.append("".join(number))


def AddTopPwd():
    try:
        # 读取TopPwd文件，并先存入password字典文件
        informationFile = open('TopPwd', 'r')
        lines = informationFile.readlines()
        for line in lines:
            dictionaryFile.write(line)
    except Exception as e:
        print(e + "\n")
        print("Read TopPwd error!")


def CreateSpecialList():
    specialWords = "`~!@#$%^&*()?|/><,."
    for i in specialWords:
        specialList.append("".join(i))


def Combination():
    for a in range(len(infolist)):
        # 把个人信息大于等于8为的直接输出到字典
        if (len(infolist[a]) >= 8):
            dictionaryFile.write(infolist[a] + '\n')
        # 对于小于8位的个人信息利用数字进行补全到8位输出
        else:
            needWords = 8 - len(infolist[a])
            for b in itertools.permutations("1234567890", needWords):
                dictionaryFile.write(infolist[a] + ''.join(b) + '\n')
        # 把个人信息元素两两进行相互拼接，大于等于8位的输出到字典
        for c in range(0, len(infolist)):
            if (len(infolist[a] + infolist[c]) >= 8):
                dictionaryFile.write(infolist[a] + infolist[c] + '\n')
                # 在2个个人信息元素加入特殊字符组合起来，大于等于8位就输出到字典
        for d in range(0, len(infolist)):
            for e in range(0, len(specialList)):
                if (len(infolist[a] + specialList[e] + infolist[d]) >= 8):
                    # 特殊字符加中间
                    dictionaryFile.write(infolist[a] + infolist[d] + specialList[e] + '\n')
                    # 特殊字符加头部
                    dictionaryFile.write(infolist[a] + specialList[e] + infolist[d] + '\n')
                    # 特殊字符加尾部
                    dictionaryFile.write(specialList[e] + infolist[a] + infolist[d] + '\n')
    # 关闭字典文件对象
    dictionaryFile.close()


if __name__ == '__main__':
    # 字典文件对象
    global dictionaryFile
    # 创建字典文件
    dictionaryFile = open('passwords', 'w')
    # 用户信息列表
    global infolist
    infolist = []
    # 数字列表
    global numberList
    numberList = []
    # 特殊字符列表
    global specialList
    specialList = []
    # 读取个人信息文件dictionaryFile
    ReadInformationList()
    # 创建数字列表
    CreateNumberList()
    # 创建特殊字符列表
    CreateSpecialList()
    # 把常见密码先写入字典文件
    AddTopPwd()
    # 字典生成主体，将 个人信息+数字列表+特殊字符列表，进行组合加入字典
    Combination()
    print('\n' + u"字典生成成功！" + '\n' + '\n' + u"字典文件名：passwords")
