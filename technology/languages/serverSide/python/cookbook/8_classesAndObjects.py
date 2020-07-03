#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

from doFunc import doFunc

def func1():
    '''
    修改实例的字符串表示
    __repr__() -> 实例的代码表示，通常可以用该方法返回的字符串文本来重新创建这个实例，即满足: obj = eval(repr(obj))
    __str__() -> 将实例转换为一个字符串
    print() 函数优先输出 __str__() 的返回值，未定义则返回 __repr__() 的返回值，若两者皆未定义，则会上溯到父类
    交互模式会打印 __repr__() 的返回值
    定义 __str__() 和 __repr__() 通常被认为是好的编程实践，可以简化调试过程和实例的输出
    '''
    class Pair:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
           return 'Pair({0.x!r},{0.y!r})'.format(self)
        def __str__(self):
            return '({0.x!s},{0.y!s})'.format(self)

    p = Pair(1,2)
    print('print p:', p)
    print('repr p:', repr(p))
    print('str p:', str(p))

def func2():
    '''
    自定义字符串的输出格式
    __format__() -> 自定义字符串的输出格式
    __format__() 方法在 Python 的字符串格式化功能中提供了一个钩子，对格式化代码的解释完全取决于类本身，因此格式化代码几乎可以为任何形式
    '''
    class Date:
        _formats = {
            'ymd': '{d.year}-{d.month}-{d.day}',
            'mdy': '{d.month}/{d.day}/{d.year}',
            'dmy': '{d.day}/{d.month}/{d.year}'
        }
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day
        def __format__(self, code):
            if code == '':
                code = 'ymd'
            fmt = self._formats[code]
            return fmt.format(d=self)

    d = Date(2020,7,31)
    print('ymd:', format(d, 'ymd'))
    print('This date is {:mdy}'.format(d))
    print('This date is {:dmy}'.format(d))

def func3():
    '''
    让对象支持上下文管理器
    要编写一个上下文管理器，其背后的主要原则就是我们编写的代码需要包含在由 with 语句定义的代码块中
    需要实现 __enter__() 和 __exit__() 方法
    当遇到 with 语句时，__enter__() 方法首先被触发执行；__enter__() 的返回值(如果有的话)被放置在由 as 限定的变量当中
    之后开始执行 with 代码块中的语句
    最后 __exit__() 方法被触发来执行清理工作
    __exit__() 方法的三个参数分别代表异常类型、值、对挂起异常的追溯，可以选择以某种方式来使用异常信息，如果 __exit__() 返回 True，异常就会被清理干净，而程序也会立即继续执行 with 语句之后的代码
    contextlib 模块中的 @contextmanager 装饰器可以简单的让某些对象支持上下文管理器，详见下一章
    '''
    class WithDemo:
        def __init__(self):
            print('init')
        def __enter__(self):
            print('enter with')
            return self
        def __exit__(self, exc_ty, exc_val, tb):
            print('exit with')
        def __str__(self):
            return 'WithDemo object'
    with WithDemo() as w:
        print('withDemo:', w)

def func4():
    '''
    当创建大量实例时如何节省内存
    对于那些主要用作简单数据结构的类，通常可以在类定义中增加 __slots__ 属性，以此来大量减少对内存的使用
    当定义类 __slots__ 属性时，Python 就会针对实例采用一种更加紧凑的内部表示，不再让每个实例都创建一个 __dict__ 字典，而是围绕着一个固定长度的小型数组来构建，在 __slots__ 中列出的属性名会在内部映射到这个数组的特定索引上
    使用 __slots__ 带来的副作用是我们没法再对实例添加任何新的属性
    使用 __slots__ 前要三思，使用它会导致类灵活性降低，而且不支持某些特定的功能，不如多重继承
    '''
    class Date:
        __slots__ = ['year', 'month', 'day']
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day

def func5():
    '''
    将名称封装到类中
    与其依赖语言特性来封装数据，Python 更推荐通过特定的命名规则来表达出对数据和方法的用途，一般遵循如下规则：
        1. 任何以单下划线(_)开头的名称应该总是被认为只属于内部实现
        2. 以双下滑线(__)开头的名称会导致出现名称重整的行为，具体来说就是名称会被重命名，前面会增加(_类名)，为: _类名__属性i名，因此，这样的属性不能通过继承而覆盖
        3. 如果想定义的名称与保留子产生冲突，应在名称最后加上单下划线(_)以示区别
    '''







if __name__ == '__main__':
    doFunc()
