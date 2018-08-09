#!/usr/bin/env python
# -*- coding: utf-8 -*-

#冒泡排序 n^2 不需要额外的存储空间 稳定

L = [3,5,10,2,9,6,4,1,7,8]

def bubbleSort(L) :
    i = len(L) - 1
    while i > 0 :
        for j in range(i) :
            if L[j] > L[j+1] :
                L[j], L[j+1] = L[j+1], L[j]
        i -= 1
    return L

def shortBubbleSort(L) :
    i = len(L) - 1
    exchanges = True
    while i > 0 and exchanges :
        exchanges = False
        for j in range(i) :
            if L[j] > L[j+1] :
                exchanges = True
                L[j], L[j+1] = L[j+1], L[j]
        i -= 1
    return L

print( bubbleSort(L) )
