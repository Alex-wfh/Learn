#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#快速排序 nlogn 不稳定

L = [3,5,10,2,9,6,4,1,7,8]

def quickSort(L) :
    if len(L) == 1 :
        return L
    sL = [i for i in L[1:] if i < L[0]]
    bL = [i for i in L[1:] if i >= L[0]]
    return quickSort(sL) + quickSort[bL]

print quickSort(L)
