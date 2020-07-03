#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

from doFunc import doFunc

def func1():
    '''
    编写可接受任意数量参数的函数
    接受任意数量位置参数，可以使用*开头的参数
    接受任意数量关键字参数，可以使用**开头的参数
    在函数定义中，以*打头的参数只能作为最后一个位置参数出现，而以**打头的参数只能作为最后一个参数出现
    '''
    def f1(*args):
        print('args:', args)
    f1(1,2,3,4)
    def f2(**kargs):
        print('kargs:', kargs)
    f2(a=1,b=2,c=3,d=4)

def func2():
    '''
    编写只接受关键字参数的函数
    在函数定义中存在一个很微妙的特性，在*打头的参数后仍然可以有其他的参数出现，这样的参数称之为keyword-only参数
    当指定可选的函数参数时，keyword-only参数常常是一种提高代码可读性的好方法
    '''
    def f(a,*,b):
        print(a,b)
        pass
    # b只能通过关键字传入
    f(1,b=2)

def func3():
    '''
    将元数据信息附加到函数参数上
    Python解释器并不会附加任何语法意义到这些参数注解上，它们既不是类型检查也不会改变Python的行为。但是，参数注解会给其他阅读代码的人带来有用的提示
    函数注解只会保存在函数的__annotations__属性中
    '''
    def add(x:int, y:int) -> int:
        return x + y

    print('do func:', add(1,2))
    print('annotations:', add.__annotations__)

def func4():
    '''
    从函数中返回多个值
    看起来像返回了多个值，实际上只是创建了个元组。
    这看起来有些奇怪，但实际上元组是通过逗号来组成的，而不是那些圆括号。
    '''
    def f():
        return 1,2,[3,4],{'5':5}
    print(f())
    a, b, c, d = f()
    print(a, b, c, d)

def func5():
    '''
    定义带有默认参数的函数
    注意以下两点：
    1. 默认参数的赋值只会在函数定义的时候绑定一次
    2. 给默认参数赋值时应该实用不可变对象，比如None、True、False、数字或字符串。绝对不要使用可变对象！！！
    在函数中检测是否对可选参数提供了值，可以利用object()创建一个独特的私有实例
    '''
    def f(a=1,b=None):
        if b is None:
            b = []
        print('do func, a: {}, b: {}'.format(a,b))
    f()

def func6():
    '''
    定义匿名或内联函数
    lambda通常适用于微型函数和需要用户提供回调函数的时候
    '''
    def add(x,y):
        return x+y
    print('ordinary func:', add(1,2))
    add = lambda x,y: x+y
    print('lambda func:', add(1,2))

def func7():
    '''
    在匿名函数中绑定变量的值
    lambda 表达式中用到的x是一个自由变量，在函数运行时才进行绑定而不是定义的时候。因此lambda表达式中入参的值应该是在执行时确定的
    如果想使用lambda定义时的值，可以通过默认值形式
    '''
    x = 1
    addx1 = lambda y: x+y
    addx2 = lambda y, x=x: x+y
    x = 10
    print('ordinary lambda:', addx1(2))
    print('default value lambda:', addx2(2))

def func8():
    '''
    让带有N个参数的可调用对象以较少的参数形式调用
    from functools import partial
    一般用不上，一旦用上就能解决大问题
    partial()对特定的参数赋了固定值并返回一个全新的可调用对象。这个新的可调用对象仍然需要通过那些未被赋值的参数来调用。这个新的可调用对象将传递给partial()的固定参数结合起来，统一将所有的参数传递给原始的函数。
    partial()对于将看似不兼容的代码结合起来使用是大有裨益的，常常可用来调整其他库中用到的回调函数的参数签名。
    '''
    from functools import partial
    def add(a,b,c,d,e,f):
        print(a,b,c,d,e,f)
        return a+b+c+d+e+f
    add1 = partial(add, 10)
    add2 = partial(add, f=100)
    add3 = partial(add1, 20, 30, f=120)
    print('add:', add(1,2,3,4,5,6))
    print('add1:', add1(2,3,4,5,6))
    print('add2:', add2(1,2,3,4,5))
    print('add3:', add3(4,5))

def func9():
    '''
    用函数代替只有单个方法的类
    单个方法的类 -> 闭包 <- 保存额外状态的方法
    简单来说，闭包就是一个函数，但是它还保存着额外的环境变量，使得这些变量可以在函数中使用。闭包的核心特性就是它可以记住定义闭包时的环境
    无论何时，当在编写代码中遇到需要附加额外的状态给函数时，请考虑使用闭包
    常用，好用，要记得用！
    '''
    from urllib.request import urlopen
    print('单个方法的类')
    class UrlTemplate:
        def __init__(self, template):
            self.template = template
        def open(self, **kwargs):
            return urlopen(self.template.format_map(kwargs))
    baidu = UrlTemplate('https://www.baidu.com/s?wd={wd}')
    for line in baidu.open(wd='a'):
        print(line.decode('utf-8'))

    print('='*40)
    print('闭包')
    def urltemplate(template):
        def opener(**kwargs):
            return urlopen(template.format_map(kwargs))
        return opener
    baidu = urltemplate('https://www.baidu.com/s?wd={wd}')
    for line in baidu(wd='a'):
        print(line.decode('utf-8'))
        
def func10():
    '''
    在回调函数中携带额外的状态
    '''
    print('基础需求')
    def apply_async(func, args, *, callback):
        result = func(*args)
        callback(result)
    def print_result(result):
        print('Got:', result)
    def add(x,y):
        return x+y
    apply_async(add,(2,3), callback=print_result)
    apply_async(add,('hello','world'), callback=print_result)
    print('='*40)
    print('希望回调函数可以同其他变量或者部分环境进行交互，例如绑定一个内部的序号，每当接收到一个结果时就递增这个号码')
    print('='*40)
    print('类，使用绑定方法(bound-method)，不推荐')
    class ResultHandler:
        def __init__(self):
            self.sequence = 0
        def handler(self, result):
            self.sequence += 1
            print('[{}] Got: {}'.format(self.sequence, result))
    r = ResultHandler()
    apply_async(add, (2, 3), callback=r.handler)
    apply_async(add, ('hello', 'world'), callback=r.handler)
    print('='*40)
    print('闭包，简洁且常用')
    def make_handler():
        sequence = 0
        def handler(result):
            nonlocal sequence # 注意这里的 nonlocal 别忘了
            sequence += 1
            print('[{}] Got: {}'.format(sequence, result))
        return handler
    handler = make_handler()
    apply_async(add, (2, 3), callback=handler)
    apply_async(add, ('hello', 'world'), callback=handler)
    print('='*40)
    print('协程，简洁，甚至比闭包更清晰，但人们对其理解程度较低')
    def make_handler():
        sequence = 0
        while True:
            result = yield
            sequence += 1
            print('[{}] Got: {}'.format(sequence, result))
    print('使用它的send()方法作为回调函数')
    handler = make_handler()
    next(handler) # 注意使用协程前需要先对其调用一次next()
    apply_async(add, (2, 3), callback=handler.send)
    apply_async(add, ('hello', 'world'), callback=handler.send)

def func11():
    '''
    内联回调函数
    本节很考验装饰器、生成器、回调函数、程序控制流的掌握情况。目前，本人对装饰器的掌握程度不足
    '''
    def apply_async(func, args, *, callback):
        result = func(*args)
        callback(result)
    from queue import Queue
    from functools import wraps
    class Async:
        def __init__(self, func, args):
            self.func = func
            self.args = args
    def inlined_async(func):
        @wraps(func)
        def wrapper(*args):
            f = func(*args)
            result_queue = Queue()
            result_queue.put(None)
            while True:
                result = result_queue.get()
                try:
                    a = f.send(result)
                    apply_async(a.func, a.args, callback=result_queue.put)
                except StopIteration:
                    break
        return wrapper
    def add(x,y):
        return x+y

    @inlined_async
    def test():
        r = yield Async(add, (2, 3))
        print(r)
        r = yield Async(add, ('hello', 'world'))
        print(r)
        for n in range(10):
            r = yield Async(add, (n, n))
            print(r)
        print('Goodbye')

    test()

def func12():
    '''
    访问定义在闭包内的变量
    一般来说，在闭包内层定义的变量对于外界来说是完全隔离的，但是，可以通过编写存取函数(accessor function，即 getter/setter 方法)并将它们作为函数属性追加到闭包上来提供对内层变量的访问支持
    本节的技术稍作扩展就可以让闭包模拟成类实例，我们要做的就是将内层函数拷贝到一个实例的字典中然后将它返回。但是应对这种奇技淫巧持谨慎态度。相比于真正的类，继承、属性、描述符或类方法这样的主要特性都无法使用。
    '''
    def sample():
        n = 0
        def func():
            print('n=', n)
        def get_n():
            return n
        def set_n(value):
            nonlocal n
            n = value
        func.get_n = get_n
        func.set_n = set_n
        return func
    f = sample()
    f()
    f.set_n(10)
    f()
    print('f.get_n():', f.get_n())

if __name__ == '__main__':
    doFunc()
