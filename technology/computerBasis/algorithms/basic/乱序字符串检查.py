#!/usr/bin/env python3
#i -*- coding:utf-8 -*-

# 两个字符串，判断第二个能否由第一个打乱生成

str1 = "abcdefg"
str2 = "badegfc1"

def checkStr(str1, str2):
    strDict1 = numberStr(str1)
    strDict2 = numberStr(str2)
    return strDict1 == strDict2

def numberStr(wordStr):
    strDict = dict()
    for s in wordStr : 
        if s in strDict.keys():
            strDict[s] += 1
        else :
            strDict[s] = 1
    return strDict

if __name__ == "__main__" :
    print ( checkStr(str1, str2) )
