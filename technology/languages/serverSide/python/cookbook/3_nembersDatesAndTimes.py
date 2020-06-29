#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from doFunc import doFunc

def func1():
    '''
    对数值进行取整
    '''
    print( round(1.234,1) )
    print( round(1.234,2) )
    print( round(1.253,1) )
    print( round(-1.25,1) )

def func2():
    '''
    执行精确的小数计算
    Decimal适合用在金融类业务，其他业务使用前需三思
    '''
    from decimal import Decimal
    a = Decimal('4.2')
    b = Decimal('2.1')
    print(a+b)

def func3():
    '''
    对树值做格式化输出
    [<>^]?width?,?(.digits)?[eEf]?
    '''
    i = 1234.56789
    print( '|' + format(i, '.2f') + '|' )
    print( '|' + format(i, '<10.2f') + '|' )
    print( '|' + format(i, '^20.2f') + '|' )
    print( '|' + format(i, ',.2f') + '|' )
    print( '|' + format(i, ',.2') + '|' )
    print( '|' + format(i, 'E') + '|' )

def func4():
    '''
    二进制、八进制、十六进制
    '''
    i = 1234
    b = bin(i)
    print( b )
    print( format(i, 'b') )
    o = oct(i)
    print( o )
    print( format(i, 'o') )
    h = hex(i)
    print( h )
    print( format(i, 'x') )
    print( int(b, 2) )
    print( int(o, 8) )
    print( int(h, 16) )

def func5():
    '''
    复数运算
    '''
    a = 1 + 1j
    b = 2 - 3j
    c = complex(1,1)
    print( a + b )
    print( c + b )
    print( a == c )

def func6():
    '''
    无穷大和NaN
    '''
    a = float('inf')
    b = float('-inf')
    c = float('nan')
    print( a, b, c )
    import math
    print( math.isinf(a) )
    print( math.isinf(b) )
    print( math.isnan(c) )

def func7():
    '''
    分数计算
    '''
    from fractions import Fraction
    a = Fraction(5,4)
    b = Fraction(-7,16)
    print( a+b, a*b )

def func8():
    '''
    大型数组
    NumPy是针对科学计算、计算密集型、工程类等需求的最强大最高效的工具(库)之一(不仅限于python)
    '''
    import numpy as np
    ax = np.array([1,2,3,4])
    ay = np.array([5,6,7,8])
    print( ax+2, ax*2, ax+ay, ax*ay )
    print( np.sqrt(ax), np.cos(ax), np.sin(ax) )
    grid = np.zeros(shape=(1000,1000))
    print( grid )
    print( np.where( ax<3, ax, 10) )

def func9():
    '''
    矩阵和线性代数
    '''
    import numpy as np
    m = np.matrix([[1,-2,3],[0,4,5],[7,8,-9]])
    print( m, '\n', m.T )

def func10():
    '''
    随机选择
    random不应该用在加密处理程序中，可考虑ssl模块
    '''
    import random
    values = list(range(10))
    print( random.choice(values) )
    print( random.sample(values,3) )
    random.shuffle(values)
    print( values )
    print( random.randint(-5,5) )
    print( random.random() )

def func11():
    '''
    时间换算
    time模块更接近于操作系统层面，datetime比time高级不少，可以理解为datetime是基于time进行了封装
    datetime
        timedelta   计算时间跨度
        tzinfo      时区
        time        只关注时间
        date        只关注日期
        datetime    同时关注时间和日期
    复杂的日期问题可以尝试实用dateutil模块
    '''
    from datetime import timedelta
    a = timedelta(days=2, hours=7)
    b = timedelta(hours=18)
    c = a+b
    print( c, c.days )

    from datetime import datetime
    a = datetime(2019,12,20)
    print( a + timedelta(days=20) )
    print( a - datetime(2018,10,12) )

    from datetime import date
    a = date(2019,12,20)
    print( a + timedelta(days=20) )
    print( a - date(2018,10,12) )
    print( a.replace(day=2) )

def func12():
    '''
    字符串与日期互转
    '''
    from datetime import datetime
    text = '2020-06-12'
    date = datetime.strptime(text, '%Y-%m-%d')
    print( date )
    print( datetime.strftime(date, '%A %B %d %Y') )

if __name__ == '__main__':
    doFunc()
