#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

from doFunc import doFunc

def func1():
    '''
    读写CSV数据
    应该实用csv模块来处理，而不是手动分解和解析CSV数据
    '''
    import csv
    csv_file_name = '__pycache__/test.csv'
    headers = ('A', 'B', 'C', 'D')
    rows = [
        (1, 2, 3, 4),
        (11, 22, 33, 44),
        (111, 222, 333, 444)
    ]
    with open(csv_file_name, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    with open(csv_file_name) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            print(row)

def func2():
    '''
    读写JSON数据
    在当下这个移动互联网时代(2020),JSON是最常见、最重要的数据传输格式
    JSON编码支持的基本类型有None、bool、int、float、str以及包含了这些类型的列表、元组和字典。对于字典，JSON会假设键是字符串
    JSON编码的格式化几乎与Pyhton语法一致，不同地方如下：
        True -> true
        False -> false
        None -> null
        ' -> "
    json模块：
        dump: 转储到文件
        dumps: 转储为字符串
        load: 从文件读取
        loads: 从字符串读取
    pprint: 把键按字母顺序排列，并且将字典以更加合理的方式进行输出
    一般来说，JSON解码时会从所提供的数据中创建出字典或者列表，如果想创建其他的类型对象，可以为json.loads()方法提供object_pairs_hook或者object_hook参数，object_pairs_hook的入参是有序的键值对，而object_hook是无序的dict
    如果想让输出格式变得漂亮一些，可以在json.dumps()函数中实用indent参数
    如果想在输出中对键进行排序处理，可以实用sort_keys参数
    类实例一般是无法序列化为JSON的，如果想序列化类实例，可以提供一个函数将类实例作为输入并返回一个可以被序列化处理的字典
    '''
    import json
    import pprint
    data = {
        'name':'A13X',
        'age':28
    }
    json_str = json.dumps(data)
    print('json str:', json_str)
    data = json.loads(json_str)
    print('data:', data)
    print('pprint', pprint.pprint(data))

    from collections import OrderedDict
    obj_data = json.loads(json_str, object_pairs_hook=OrderedDict)
    print('object_pairs_hook:', obj_data)

    class JSONObject:
        def __init__(self, d):
            self.__dict__ = d
        def __repr__(self):
            return 'JSONObject, ditc:{}'.format(self.__dict__)
    obj_data = json.loads(json_str, object_hook=JSONObject)
    print('object_hook:', obj_data)
    json_str = json.dumps(data, indent=4)
    print('indent:', json_str)
    json_str = json.dumps(data, sort_keys=True)
    print('sort_keys:', json_str)

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return 'Point, x:{}, y:{}'.format(self.x, self.y)
    def serialize_instance(obj):
        d = {'__classname__': type(obj).__name__}
        d.update(vars(obj))
        return d
    classes = {'Point': Point}
    def unserialize_object(d):
        clsname = d.pop('__classname__', None)
        if clsname:
            print(vars())
            cls = classes[clsname]
            obj = cls.__new__(cls)
            for k, v in d.items():
                setattr(obj, k, v)
            return obj
        else:
            return obj
    p = Point(2,3)
    s = json.dumps(p, default=serialize_instance)
    print(s)
    a = json.loads(s, object_hook=unserialize_object)
    print(a)

def func3():
    '''
    解析XML
    XML解析的需求不是非常常见，一般较旧的项目中会涉及，记住以下两个库即可：
    xml.etree.ElementTree # 内置库
    lxml.etree # 功能更强大，需安装
    '''
    import xml.etree.ElementTree
    import lxml.etree

def func4():
    '''
    同关系型数据库进行交互
    connect -> cursor -> execute/executemany -> commit -> close
    注意以下两个问题：
        1. sql类型映射
        2. sql注入
    '''
    import sqlite3
    db = sqlite3.connect('__pycache__/database.db')
    c = db.cursor()
    c.execute('create table test (a text, b integer, c real)')
    c.executemany('insert into test values (?,?,?)', [('1',2,3)])
    db.commit()
    for row in db.execute('select * from test'):
        print(row)
    c.execute('drop table test')
    db.close()

def func5():
    '''
    编码和解码十六进制数字
    base64 只能对大写形式的十六进制数进行操作
    binascii 即能处理大写也能处理小写
    '''
    s = b'hello'
    import binascii
    h = binascii.b2a_hex(s)
    print('binascii encode:', h)
    print('binascii decode:', binascii.a2b_hex(h))
    import base64
    h = base64.b16encode(s)
    print('base64 enccode:', h)
    print('base64 devode:', base64.b16decode(h))

def func6():
    '''
    Base64编码和解码
    '''
    s = b'hello'
    import base64
    a = base64.b64encode(s)
    print(a)
    print(base64.b64decode(a))

def func7():
    '''
    与二进制数据打交道
    对于那些必须对二进制数据编码和解码的程序，我们常会用到struct模块
    '''
    import struct

def func8():
    '''
    数据汇总和统计
    对于分析大型数据集、数据归组、执行统计分析或其他类似的需求，Pandas绝对值得一试！
    注意：说的是大数据，杀鸡就没必要用牛刀了
    '''
    import pandas
    
if __name__ == '__main__':
    doFunc()
