#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#插入排序 n^2 稳定

L = [3,5,10,2,9,6,4,1,7,8]

def insertionSort(L) :
    for i in range(1,len(L)) :
        k = L[i]
        j = i-1
        while j >= 0 :
            if L[j] > k :
                L[j+1] = L[j]
                L[j] = k
            else :
                break
            j -= 1
    return L

print insertionSort(L)














































