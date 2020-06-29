#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

from doFunc import doFunc

txt_file_name = '__pycache__/test.txt'
gzip_file_name = '__pycache__/test.gz'
bz2_file_name = '__pycache__/test.bz2'

def func1():
    '''
    读写文本数据
    w: write
    r: read
    a: append
    x: 不存在写入，exist ? FileExistsError : write
    b: binary
    t: text(默认)
    +: 打开用于更新
    '''
    print('with语句，创建上下文环境，文件自动关闭')
    with open(txt_file_name, 'r') as f:
        for line in f:
            print(line)
    print('='*40)
    print('手动方式')
    f = open(txt_file_name, 'r', encoding='ascii', errors='ignore')
    print(f.read())
    f.close()

def func2():
    '''
    将输出重定向到文件中
    '''
    with open(txt_file_name, 'w') as f:
        print('Hello World!', file=f)

def func3():
    '''
    以不同的分隔符或行结尾符完成打印
    '''
    print('A13X', 'WU', 'NIU', 'B', sep=',', end='!!\n\n')

def func4():
    '''
    读写二进制数据
    注意字节串和字符串存在微妙的语意差异，尤其注意索引和迭代操作
    '''
    print('读二进制数据')
    with open(txt_file_name, 'rb') as f:
        print(f.read())
    print('写二进制数据')
    with open(txt_file_name, 'wb') as f:
        f.write(b'Hello World')

def func5():
    '''
    对不存在的文件执行写入操作(exist ? FileExistsError : write)
    '''
    with open(txt_file_name, 'x') as f:
        f.write('Hello')

def func6():
    '''
    在字符串上执行I/O操作
    出于某种原因需要模拟普通文件
    io.StringIO()
    io.BytesIO()
    getvalue()返回流的全部内容，与当前位置无关
    '''
    import io
    s = io.StringIO()
    s.write('Hello World\n')
    print('This is a test', file=s)
    print(s.getvalue())

    s = io.BytesIO(b'Hello World\n')
    print(s.read())

def func7():
    '''
    读写压缩的数据文件
    gzip bz2
    选择正确的文件模式是至关重要的，默认的模式是二进制，gzip.open()和bz.open()所有接受对策参数与内建的open()函数一样
    写入压缩数据时，压缩级别可以通过 compresslevel 关键字来指定，默认级别是9，代表最高的压缩等级。等级越高压缩比越大，性能表现越差
    '''
    import gzip
    with gzip.open(gzip_file_name, 'wt') as f:
        f.write(func7.__doc__)
    with gzip.open(gzip_file_name, 'rt') as f:
        print(f.read())

    import bz2
    with bz2.open(bz2_file_name, 'wt', compresslevel=3) as f:
        f.write(func7.__doc__)
    with bz2.open(bz2_file_name, 'rt') as f:
        print(f.read())

def func8():
    '''
    对固定大小的记录进行迭代
    functools.partial()
    iter()哨兵模式
    '''
    from functools import partial
    RECORD_SIZE = 32
    with open(txt_file_name, 'r') as f:
        records = iter(partial(f.read, RECORD_SIZE), '')
        for r in records:
            print(r)

def func9():
    '''
    将二进制数据读取到可变缓冲区
    readinto
    memoryview(内存映像)
    '''
    buf = bytearray(10)
    with open(txt_file_name, 'rb') as f:
        f.readinto(buf)
    print(buf)
    m1 = memoryview(buf)
    m1[:5] = b'HAHAH'
    print(buf)

def func10():
    '''
    对二进制文件做内存映射
    高效、优雅地访问二进制文件内容
    '''
    import os
    import mmap

    fd = os.open(txt_file_name, os.O_RDWR)
    m = mmap.mmap(fd, 10, access=mmap.ACCESS_WRITE)
    print(len(m))
    print(m[:5])

def func11():
    '''
    处理路径名
    任何需要处理文件名的问题都应该使用os.path
    '''
    import os

    path = os.path.abspath(__file__)
    print('path:', path)
    base_name = os.path.basename(path)
    print('base name:', base_name)
    dir_name = os.path.dirname(path)
    print('dir name:', dir_name)
    dirs = dir_name.split('/')
    print('join path:', os.path.join(*dirs, base_name))
    print('expand user:', os.path.expanduser(path))
    print('splitext:', os.path.splitext(path))

def func12():
    '''
    检测文件是否存在
    '''
    import os
    print('exists:', os.path.exists('/etc/passwd'))
    print('is file:', os.path.isfile('/etc/passwd'))
    print('is dir:', os.path.isdir('/etc/passwd'))
    print('is link:', os.path.islink('/usr/bin/python2.7'))
    print('real path of link:', os.path.realpath('/usr/bin/python2.7'))
    print('size:', os.path.getsize('/etc/passwd'))
    print('mtime:', os.path.getmtime('/etc/passwd'))

def func13():
    '''
    获取目录内容列表
    '''
    import os
    dirs = os.listdir('/etc')
    print( dirs )
    import glob
    print(glob.glob('/etc/*.d'))

def func14():
    '''
    与未知文件名打交道时，可能需要考虑文件名编码问题
    UnicodeEncodeError
    '''
    pass

def func15():
    '''
    为已经打开的文件添加或修改编码方式
    I/O 系统是以一系列的层次来构建的
    '''
    import io
    f = open(txt_file_name, 'w')
    print('文本处理层', f)
    buf = f.buffer
    print('缓冲I/O层，负责二进制数据', buf)
    raw = buf.raw
    print('原始文件层', raw)
    b = f.detach()
    print('detach f', b)
    f = io.TextIOWrapper(b, encoding='latin-1')
    print('encode detached f', f)
    
def func16():
    '''
    将字节数据写入文本文件
    直接将字节串写入缓冲I/O层
    '''
    import sys
    sys.stdout.buffer.write(b'Hello\n')

def func17():
    '''
    将已有的文件描述符包装为文件对象
    open函数中，将整数形式的文件描述符作为第一个参数取代文件名即可
    '''
    import os
    fd = os.open(txt_file_name, os.O_RDWR)
    print(fd)
    with open(fd, 'w') as f:
        f.write('hello\n')
    
def func18():
    '''
    创建临时文件和目录
    '''
    import tempfile
    with tempfile.TemporaryFile('w+') as f:
        f.write('hello')
        f.seek(0)
        print(f.read())

    with tempfile.NamedTemporaryFile('w+') as f:
        print('filename is:', f.name)

    with tempfile.TemporaryDirectory('w+') as d:
        print('dirname is:', d)

    print('makestemp:', tempfile.mkstemp())
    print('makedtemp:', tempfile.mkdtemp())
    print('tempdir:', tempfile.gettempdir())

def func19():
    '''
    串口通信
    串行接口通常很混乱，直接实用 pyserial 即可，没必要考虑其内部复杂的实现
    pyserial 需安装
    '''
    import serial

def func20():
    '''
    序列化python对象
    dump: 转储到文件
    dumps: 转储为字符串
    load: 从文件读取
    loads: 从字符串读取
    '''
    import pickle
    data = [1,2,'3',{'4':5}]
    with open(txt_file_name, 'wb') as f:
        pickle.dump(data, f)

    with open(txt_file_name, 'rb') as f:
        print(pickle.load(f))

if __name__ == '__main__':
    doFunc()
