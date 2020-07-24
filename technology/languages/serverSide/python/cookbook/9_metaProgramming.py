#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc

"""
软件开发中最重要的一条真理就是"不要重复自己的工作(Don't repeat yourself)"。
也就是说，任何时候当创建高度重复的代码（或者需要复制粘贴源代码）时，通常都需要寻找一个更加优雅的解决方案。
在Python中，这类问题常常会归类为"源编程"。
简而言之，源编程的主要目的是创建函数和类，并用它们来操纵代码（比如说修改、生成或者包装已有代码）。
Python中基于这个目的主要特性包括装饰器、类装饰器以及元类。
同时，也包括对象签名、用exec()来执行代码以及检查函数和类的内部结构。
"""


def func1():
    """
    给函数添加一个包装 -> 装饰器
    装饰器就是一个函数，它可以接受一个函数作为输入并返回一个新的函数作为输出
    装饰器内部的代码一般会涉及创建一个新的函数，利用*args和**kwargs来接受任意的参数。在这个函数内部，我们需要调用原来的输入函数（即被包装的那个函数）并返回它的结果。也可以添加任何想要添加的额外代码。这个新创建的函数会作为装饰器的返回，取代了原来的函数
    需要重点注意的是，通常情况下，装饰器不会修改调用签名，也不会修改被包装函数返回的结果
    """
    import time
    from functools import wraps

    def time_this(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(func.__name__, end - start)
            return result

        return wrapper

    @time_this
    def countdown(n):
        while n > 0:
            n -= 1

    countdown(100000)


def func2():
    """
    装饰器保存函数的元数据
    from functools import wraps
    wraps: 外衣、包裹
    wraps 的原理就是将原对象的属性取出来，再一一赋值给装饰器
    编写装饰器的一个重要的部分就是拷贝元数据。否则被包装函数会丢失所有有用的信息，例如函数名、文档字符串、函数注解以及通用签名
    """

    import time
    from functools import wraps

    def time_this(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(func.__name__, end - start)
            return result

        return wrapper

    @time_this
    def countdown(n):
        """
        Count down
        """
        while n > 0:
            n -= 1

    print('func name', countdown.__name__)
    print('func doc', countdown.__doc__)
    print('func annotations', countdown.__annotations__)


def func3():
    """
    对装饰器进行解包装
    想访问已被装饰器包装的原始函数，直接访问装饰器背后的未包装过的函数对于调试、反射（introspection，也可称为"自省"）以及其他一些涉及函数的操作是很有帮助的
    对于装饰器实现中已经使用了@wraps，我们可以通过访问__wrapped__属性来获取对原始函数的访问
    对于未使用@wraps的装饰器，访问原始函数的方式跟我们期望会有所区别，特别是，由内建的装饰器@staticmethod和@classmethod创建的描述符，会把原始函数保存在__func__属性中
    具体问题具体分析
    """
    from functools import wraps

    def decorator1(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 1')
            return func(*args, **kwargs)

        return wrapper

    def decorator2(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 2')
            return func(*args, **kwargs)

        return wrapper

    @decorator1
    @decorator2
    def add(x, y):
        return x + y

    print(add(2, 3))
    print(add(2, 3))
    print(add.__wrapped__(2, 3))
    print(add.__wrapped__.__wrapped__(2, 3))


def func4():
    """
    可接受参数的装饰器
    最外层的函数接收所需的参数，并让它们对装饰器的内层函数可见
    内层函数接收一个函数并给它加上一个包装层
    """
    from functools import wraps
    import logging

    def logged(level, name=None, message=None):
        def decorator(func):
            log_name = name if name else func.__module__
            log = logging.getLogger(log_name)
            log_msg = message if message else func.__name__

            @wraps(func)
            def wrapper(*args, **kwargs):
                log.log(level, log_msg)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @logged(logging.DEBUG)
    def add(x, y):
        return x + y

    @logged(logging.CRITICAL, 'example')
    def spam():
        print('Spam!')

    add(2, 3)
    spam()


def func5():
    """
    属性可由用户修改的装饰器
    访问器函数以属性的形式附加到包装函数上，每个访问器函数允许对nonlocal变量赋值来调整内部参数
    该方法存在一个令人惊叹的特性，访问器函数可以跨域多个装饰器层进行传播，即装饰器除在任何位置，修改属性的访问器都能调用
    本节的解决方案实际上是类装饰器的一种替代方案
    """
    from functools import wraps, partial
    import logging

    def attach_wrapper(obj, func=None):
        if func is None:
            return partial(attach_wrapper, obj)
        setattr(obj, func.__name__, func)
        return func

    def logged(level, name=None, message=None):
        def decorator(func):
            log_name = name if name else func.__module__
            log = logging.getLogger(log_name)
            log_msg = message if message else func.__name__

            @wraps(func)
            def wrapper(*args, **kwargs):
                log.log(level, log_msg)
                return func(*args, **kwargs)

            # 另一种并不是很好的方案
            @wraps(func)
            def wrapper2(*args, **kwargs):
                """
                如果完全基于对函数属性的直接访问，那么只有装饰器处在最顶层时，才能生效
                """
                wrapper2.log.log(wrapper2.level, wrapper2.log_msg)
                return func(*args, **kwargs)

            @attach_wrapper(wrapper)
            def set_level(new_level):
                nonlocal level
                level = new_level

            @attach_wrapper(wrapper)
            def set_message(new_msg):
                nonlocal log_msg
                log_msg = new_msg

            return wrapper
        return decorator

    @logged(logging.DEBUG)
    def add(x, y):
        return x + y

    @logged(logging.CRITICAL, 'example')
    def spam():
        print('Spam!')

    add(2, 3)
    add.set_level(logging.ERROR)
    add(2, 3)
    add.set_message('Add called')
    add(2, 3)


def func6():
    """
    能接收可选参数的装饰器
    本节的技术可以让装饰器以一致的方式使用，既可以带括号，也可以不带括号
    """
    from functools import wraps, partial
    import logging

    def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
        # 实现一致性的巧妙方式就在这个判断中
        if func is None:
            return partial(logged, level=level, name=name, message=message)
        log_name = name if name else func.__module__
        log = logging.getLogger(log_name)
        log_msg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, log_msg)
            return func(*args, **kwargs)
        return wrapper

    @logged
    def add(x, y):
        return x + y

    @logged(level=logging.ERROR, name='example')
    def spam():
        print('Spam!')

    add(2, 3)
    spam()


def func7():
    """
    利用装饰器对函数参数强制执行类型检查
    装饰器的一个特性就是它们只会在函数定义时应用一次、
    inspect.signature()函数，允许我们从一个可调用对象中提取出参数签名信息
    注意，该解决方案有个巧妙的地方，对于具有默认值的函数，如果未提供参数，则断言机制不会作用在其默认值上
    装饰器参数与函数注解的对比：
        1. 函数的每个参数只能赋予一个单独的注解，如果把注解用于类型断言，就不能用在别处
        2. 该装饰器可强制限制参数类型，而注解是非强制性的
    """
    from inspect import signature
    from functools import wraps

    def type_assert(*ty_args, **ty_kwargs):
        def decorate(func):
            if not __debug__:
                return func
            sig = signature(func)
            bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_values = sig.bind_partial(*args, **kwargs)
                for name, value in bound_values.arguments.items():
                    if name in bound_types:
                        if not isinstance(value, bound_types[name]):
                            raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
                return func(*args, **kwargs)
            return wrapper
        return decorate

    @type_assert(int, int)
    def add(x, y):
        return x + y

    @type_assert(int, z=int)
    def spam(x, y, z=42):
        print(x, y, z)

    try:
        add(5, 'fck')
    except Exception as e:
        print(e)
    try:
        spam(5, 'a', 'fck')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    doFunc()
