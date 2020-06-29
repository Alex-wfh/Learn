#!/usr/bin/env python
# -*- coding: utf-8 -*-

from doFunc import doFunc

s = ' yeah, but no, but yeah; but no, but yeah '

def func1():

    '''
    多分隔符拆分字符串
    '''
    import re
    print( re.split(r'\s*[;,\s]\s*', s) )

def func2():
    '''
    开头/结尾文本匹配
    '''
    print( s.startswith('y') )
    print( s.startswith('yeah') )
    print( s.startswith('abc') )
    print( s.endswith('h') )
    print( s.endswith(('yeah','abcv')) )
    print( s.endswith('abc') )

def func3():
    '''
    shell通配符做字符串匹配
    '''
    from fnmatch import fnmatch, fnmatchcase
    print( fnmatch(s,'*yeah') )
    # fnmatch 采用的大小写区分规则和底层文件系统相同
    print( fnmatch(s,'*YEAH') )
    # fnmatchcase 区分大小写
    print( fnmatchcase(s,'*YEAH') )

def func4():
    '''
    文本模式的匹配和查找
    '''
    print( s.find('yeah') )
    print( s.startswith('y') )
    print( s.endswith('h') )
    print( re.match(r'.*but.*', s) )

    import re
    c = re.compile(r'.*but.*')
    print( c.match(s) )
    m = c.match(s)
    print( m.group() )
    print(re.finditer('but', s) )
    print(re.findall('but', s) )

def func5():
    '''
    查找和替换文本
    '''
    print( s.replace('but', 'and') )
    
    import re
    print( re.sub(r'but', r'or', s) )
    print( re.subn(r'but', r'or', s) )
    
def func6():
    '''
    以不区分大小写的方式对文本做查找和替换
    '''
    import re
    print( re.sub(r'BUT', r'or', s, flags=re.IGNORECASE) )
    
def func7():
    '''
    正则表达式的贪婪与非贪婪
    '''
    import re
    print( re.findall(r'but.*', s) )
    print( re.findall(r'but.*?', s) )
    
def func8():
    '''
    正则跨行
    '''
    import re
    s = '''yeah, but no,
            but yeah, 
            but no, 
            but yeah'''
    print( re.findall(r'but.*', s) )
    print( re.findall(r'but.*', s, flags=re.DOTALL) )


def func9():
    '''
    从字符串中去掉不需要的字符
    '''
    print( s.strip(' y') )
    print( s.lstrip(' y') )
    print( s.rstrip(' y') )

def func10():
    '''
    文本的过滤和清理
    '''
    remap = {ord(';'): '?', ord(','): '.'}
    print( s.translate(remap) )

def func11():
    '''
    对齐文本字符串
    '''
    print( s.rjust(50) )
    print( s.ljust(50, '=') )
    print( s.center(50, '*') )

def func12():
    '''
    字符串连接与合并
    '''
    l = s.split()
    print(l)
    print( '*'.join(l) )
    ss = ' yeah, but {}, but yeah; but {}, but yeah '
    print( ss.format(*['*','=']) )

def func13():
    '''
    给字符串中变量名做差值处理
    '''
    s = ' yeah, but {n}, but {y}; but {n}, but {y} '
    print(s.format(n='no', y='yes'))
    n = 'no'
    y = 'yes'
    print(s.format_map(vars())) 

def func14():
    '''
    固定宽度格式化文本
    '''
    ss = s*10
    import textwrap
    print(textwrap.fill(ss,10))

def func14():
    '''
    大部分情况字符串上执行的操作同样也能在字节串上执行，
    分片、打印、格式化、文件系统相关操作时，字节串与字符串有所不同。
    '''
    pass

def func15():
    '''
    递归下降解析器
    有趣且实用
    在清楚需求的基础上，确定语法规则与规划解析器最好齐头并进！
    '''
    pass



if __name__ == '__main__':
    doFunc()
   
