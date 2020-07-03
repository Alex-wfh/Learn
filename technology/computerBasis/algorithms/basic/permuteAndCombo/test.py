#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# permute 构建一个由全部可能的组合方式组成的列表
def permute(l):
    if not l:
        yield l[:0]
    else:
        for i in range(len(l)):
            for p in permute(l[:i]+l[i+1:]):
                yield l[i:i+1] + p


# subset 构建一个由指定长度的自己组成的全部排列组合的列表
def subset(l, size):
    if not l or not size:
        yield l[:0]
    else:
        for i in range(len(l)):
            for s in subset( l[:i]+l[i+1:], size-1 ):
                yield l[i:i+1] + s


# combo 构建一个由指定长度的子集组成的全部排列组合的列表，但是不考虑顺序
def combo(l, size):
    if not l or not size:
        yield l[:0]
    else:
        for i in range(len(l)-size+1):
            for c in combo(l[i+1:], size-1):
                yield l[i:i+1]+c



if __name__ == '__main__':
    print(list(permute("123")))
    print(list(subset("123", 2)))
    print(list(combo("123", 3)))
