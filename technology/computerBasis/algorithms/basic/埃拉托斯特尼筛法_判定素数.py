#!/usr/bin/env Python
# coding=utf-8

n = input("判定小于等于多少的所有素数:")
#速度测试
#n = 100000000
"""
#自己写的
#30.152s
#remove这个函数用时过多
intList = range(2,n+1)
def removeInt(parime) :
    for i in intList :
        if i % parime == 0 and i != parime :
            intList.remove(i)

for parime in range(2,int(n**0.5)+1) :
    removeInt(parime)

print intList 
"""
"""
#百度的
#0.060s
def primes(n):
    P = []
    f = []
    for i in range(n+1):
        if i > 2 and i%2 == 0:
            f.append(1)
        else:
            f.append(0)
    i = 3
    while i*i <= n:
        if f[i] == 0:
            j = i*i
            while j <= n:
                f[j] = 1
                j += i+i
        i += 2
 
    P.append(2)
    for x in range(3,n,2):
        if f[x] == 0:
            P.append(x)
 
    return P
 
P = primes(n)
print P
"""
#百度的，简写，速度略有提升
def primes(n) :
    P = [2]
    #偶数只留2
    f = [1 if i > 2 and i%2 == 0 else 0 for i in range(n+1) ]
    #基数处理
    i = 3
    while i*i <= n :
        if f[i] == 0:
            j = i*i
            while j <= n:
                f[j] = 1
                j += 2*i
        i += 2
    P += [x for x in range(3,n,2) if f[x] == 0 ]
    return P 
print primes(n)
