#!/usr/bin/env python
# -*- coding:utf-8 -*-

def divideBy2(num, base) :
    rst = ''
    digits = '0123456789ABCDEF'
    while num > 0 :
        rst = digits[ num % base ] + rst
        num = num / base
    return rst

if __name__ == "__main__" :
    print (divideBy2(5211,16))
