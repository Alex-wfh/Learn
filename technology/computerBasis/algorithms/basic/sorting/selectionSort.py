#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#选择排序 n^2 不稳定

L = [3,5,10,2,9,6,4,1,7,8]

def selectionSort(L) :
    for i in range(len(L)) :
        m = i
        for j in range(i+1, len(L)) :
            if L[m] > L[j] :
                m = j
        L[i], L[m] = L[m], L[i]
    return L
            

#一种介于选择和冒泡之间的排序算法 不稳定
def bubbleSelectionSort(L) :
    for i in range(len(L)) :
        for j in range(i+1, len(L)) :
            if L[i] > L[j] :
                L[i], L[j] = L[j], L[i]
    return L

print selectionSort(L)









