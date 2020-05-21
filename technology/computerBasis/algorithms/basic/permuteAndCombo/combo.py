#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 构建一个由指定长度的子集组成的全部排列组合的列表，但是不考虑顺序

def combo(l, size):
    if not l or not size:
        return [l[:0]]
    res = []
    for i in range(len(l)-size+1):
        rest = l[i+1:]
        for c in combo(rest, size-1):
            res.append( l[i:i+1] + c )
    return res


def combo2(l, size):
    if not l or not size:
        yield l[:0]
    else:
        for i in range(len(l)-size+1):
            rest = l[i+1:]
            for c in combo2(rest, size-1):
                yield l[i:i+1] + c


if __name__ == "__main__":
    rint(list(combo2("123",2)))
