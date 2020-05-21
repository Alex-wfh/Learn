#!/usr/bin/env Python
# coding=utf-8
a = int(input("输入第一个数字:"))
b = int(input("输入第二个数字:"))
"""
#速度测试
a = 113547654
b = 113547652
"""
"""
#一种2b方法，用时8.897s
while a != b :
    if a < b :
        b = b - a
    else :
        a = a - b
print a
"""
#辗转相除法，用时0.025s
def gcd(x,y):
    return gcd(y,x%y) if y != 0 else x
    
print gcd(a,b)
