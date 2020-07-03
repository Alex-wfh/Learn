#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 构建一个由全部可能的组合方式组成的列表

def permute(l):
    if not l:
        return [l]
    else:
        res = []
        for idx in range(len(l)):
            rest = l[:idx] + l[idx+1:]
            for p in permute(rest):
                res.append( l[idx:idx+1] + p )
        return res


def permute2(l):
    if not l:
        yield l
    else:
        for i in range(len(l)):
            rest = l[:i] + l[i+1:]
            for p in permute2(rest):
                yield l[i:i+1] + p


if __name__ == "__main__":
    print(list(permute2([1,2,3])))
