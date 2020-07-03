#!/usr/bin/env python3
# -*- coding:utf8 -*-

# 中缀转后缀
def infixToPostfix( infixExpr ) :
    # 定义优先级
    prec = {
        "*" : 3 ,
        "/" : 3 ,
        "+" : 2 ,
        "-" : 2 ,
        "(" : 1
    }
    opStack = list()
    postExpr = ""

    for e in infixExpr :
        if e in prec :
            if opStack and e != "(" :
                while prec[e] <= prec[opStack[-1]] :
                    postExpr += opStack.pop()
                    if not opStack :
                        break
                opStack.append(e)
            else :
                opStack.append(e)
        elif e == ")" :
            while opStack[-1] != "(" :
                postExpr += opStack.pop()
            postExpr += opStack.pop()
        else :
            postExpr += e
    postExpr += "".join(opStack[::-1])

    return postExpr.replace("(","")

# 后缀求值
def postfixEval( postfixExpr ) :
    prec = [ "*", "/", "+", "-" ]
    opStack = list()
    for e in postfixExpr :
        if e in prec :
            opStack.append( doMath( e, opStack ) )
        else :
            opStack.append(e)
    return opStack

def doMath( e, opStack ) :
    o2 = int( opStack.pop() )
    o1 = int( opStack.pop() )
    if e == "*" :
        return o1*o2
    elif e == "/" :
        return o1/o2
    elif e == "+" :
        return o1+o2
    else :
        return o1-o2


if __name__ == "__main__" :
    print ( postfixEval( infixToPostfix("(1+2)*3-(4-5)*(6+7)") ) )
