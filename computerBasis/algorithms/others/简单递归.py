#!/usr/bin/env python
# -*- coding:utf-8 -*-

def sumList(numList) :
    if len(numList) == 1 :
        return numList[0]
    else :
        return numList[0] + sumList(numList[1:])

def systemConversion(n, base) :
    convertStr = "0123456789ABCDEF"
    if n < base :
        return convertStr[n]
    else :
        return systemConversion(n/base, base) + convertStr[n%base]

# 汉诺塔
def moveTower( height, fromPole, withPole, toPole ) :
    if height >= 1 :
        moveTower( height-1, fromPole, toPole, withPole )
        moveDisk( fromPole, toPole )
        moveTower( height-1, withPole, fromPole, toPole )

def moveDisk( fromPole, toPole ) :
    print ( fromPole + " -> " + toPole )


if __name__ == "__main__" :
    print ( sumList([1,2,3,4,5]) )
    print ( systemConversion(1453,16) )
    print ( moveTower( 3, "A", "B", "C" ) )
