#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def parChecker(symbolString) :
    i = 0
    for s in symbolString :
        if s == '(' :
            i += 1
        elif s == ')' :
            i -= 1
        else :
            i = -1
        if i < 0 :
            break
    return True if i == 0 else False


def parsChecker(symbolString) :
    symbolList = list()
    symbolMap = {'(':')','[':']','{':'}'}
    rst = True
    for s in symbolString :
        if s in "({[" :
            symbolList.append(s)
        elif s in ")}]" :
            if symbolMap[symbolList[-1]] == s :
                symbolList.pop()
            else :
                rst = False
                break
        else :
            rst = False
            break
    return True if rst and symbolList == [] else False


if __name__ == "__main__" :
    print parChecker("()()()()()(())(()()())")
    print parsChecker("({}[({})])(()([]))")
