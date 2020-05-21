#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 构建一个由指定长度的自己组成的全部排列组合的列表

def subset(l, size):
    if not l or not size:
        return [l[:0]]
    res = []
    for i in range(len(l)):
        rest = l[:i] + l[i+1:]
        for s in subset(rest, size-1):
            res.append( l[i:i+1] + s )
    return res


def subset2(l, size):
    if not l or not size:
        yield l[:0]
    else :
        for i in range(len(l)):
            rest = l[:i] + l[i+1:]
            for s in subset2(rest, size-1):
                yield l[i:i+1] + s


if __name__ == "__main__":
    print(list(subset2("123",2)))
