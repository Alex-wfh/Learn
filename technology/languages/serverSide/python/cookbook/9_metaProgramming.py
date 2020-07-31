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


def func8():
    """
    在类中定义装饰器
    首先要确定装饰器是以实例方法还是类方法形式应用
    如果需要装饰器记录或合并信息，在类中定义装饰器就很适合
    尽管在外层的装饰器函数中使用了self或cls参数，但内层定义的包装函数一般不需要额外的函数，唯一用到这个参数的场景就是需要在包装函数中访问实例的某个部分
    这种定义方式在继承中也有潜在的用途，继承时，装饰器必须定义为类方法，而且使用时须显示地给出父类的名称，因为在定义该方法时，子类根本没有创建
    """

    from functools import wraps

    class A:
        def decorator1(self, func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print('Decorator 1')
                return func(*args, **kwargs)

            return wrapper

        @classmethod
        def decorator2(cls, func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print('Decorator 2')
                return func(*args, **kwargs)

            return wrapper

    a = A()

    @a.decorator1
    def spam():
        pass

    @A.decorator2
    def grok():
        pass

    class B(A):
        @A.decorator2
        def bar(self):
            pass

    spam()
    grok()
    b = B()
    print('b.bar()')
    b.bar()


def func9():
    """
    把装饰器定义成类
    用装饰器来包装函数，希望得到的结果是一个可调用的实例。装饰器既能在类中工作，也可以在类外部使用
    要把装饰器定义成类，需要确保在类中实现__call__()和__get__()方法
    把装饰器定义成类通常是简单明了的，需要注意以下几点：
        1. 对functools.wraps()函数的使用和在普通装饰器中目的一样
        2. __get__()方法不可忽视，如果省略会发现当尝试调用被装饰的实例方法时会出现怪异的行为
    """
    import types
    from functools import wraps

    class Profiled:
        def __init__(self, func):
            wraps(func)(self)
            self.n_calls = 0

        def __call__(self, *args, **kwargs):
            self.n_calls += 1
            return self.__wrapped__(*args, **kwargs)

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return types.MethodType(self, instance)

    @Profiled
    def add(x, y):
        return x + y

    class Spam:
        @Profiled
        def bar(self, x):
            print(self, x)

    print(add(2, 3), add(2, 3), add.n_calls)
    s = Spam()
    s.bar(1)
    s.bar(2)
    print(s.bar.n_calls)


def func10():
    """
    装饰器作用到类和静态方法上
    装饰器作用到类和静态方法上是简单而直接的，但是要保证装饰器在应用的时候需要放在@classmethod和@staticmethod之前
    这里的问题在于@calssmethod和@staticmethod并不会实际创建可直接调用的对象。相反，它们创建的是特殊的描述符对象。
    因此，如果尝试在另一个装饰器中想函数那样使用它们，装饰器就会崩溃。所以要确保这些装饰器出现在@classmethod和@staticmethod之前。
    """


def func11():
    """
    装饰器为被包装函数添加额外的参数
    这并不是装饰器常见的用法，但是，对于某些特定的代码重复模式来说是一项有用的技术
    keyword-only 参数可以很容易地添加到那些以*args和**kwargs作为形参的函数上。keyword-only参数会作为特殊情况从随后的调用中挑选出来，调用函数时只会使用剩下的位置参数和关键字参数
    注意参数名称冲突问题，可通过添加额外检验的方式解决
    """
    from functools import wraps

    def optional_debug(func):
        @wraps(func)
        def wrapper(*args, debug=False, **kwargs):
            if debug:
                print('Calling', func.__name__)
            return func(*args, **kwargs)

        return wrapper

    @optional_debug
    def spam(a, b, c):
        print(a, b, c)

    spam(1, 2, 3)
    spam(1, 2, 3, debug=True)


def func12():
    """
    利用装饰器给类定义打补丁
    类装饰器常常可以直接作为涉及混合类或者元类等高级技术的替代方案
    如果要将多个类装饰器作用于某个类之上，那么可能需要考虑添加的顺序问题
    通过继承也可以解决类似问题，但类装饰器更为直接，而且由于不依赖对super()函数的使用，速度也会稍快一些
    """

    def log_getattribute(cls):
        orig_getattribute = cls.__getattribute__

        def new_getattribute(self, name):
            print('getting:', name)
            return orig_getattribute(self, name)

        cls.__getattribute__ = new_getattribute
        return cls

    @log_getattribute
    class A:
        def __init__(self, x):
            self.x = x

        def spam(self):
            pass

    a = A(42)
    a.x
    a.spam()


def func13():
    """
    利用元类来控制实例的创建
    改变实例创建的方式，以此来实现单例模式、缓存或者其他类似特性
    通过定义一个元类并以某种方式重新实现它的__call__()方法
    通过元类来实现各种创建实例的模式常常比那些不涉及元类的解决方案要优雅，如果不用元类，那就需要将类隐藏在某种额外的工程函数之后
    尽管使用元类的解决方案涉及许多更加高级的概念，但最终的代码看起来会更加清晰，也没有过多花里胡哨的技巧
    """
    # 可以调用定义的静态方法，但是没法以普通的方式创建出实例
    print('=' * 20, '无实例类', '=' * 20)

    class NoInstance(type):
        def __call__(self, *args, **kwargs):
            raise TypeError('Can\'t instantiate directly')

    class Spam(metaclass=NoInstance):
        @staticmethod
        def grok(x):
            print('Spam.grok')

    Spam.grok(42)
    try:
        s = Spam()
    except Exception as e:
        print(e)

    # 单例模式
    print('=' * 20, '单例模式', '=' * 20)

    class Singleton(type):
        def __init__(self, *args, **kwargs):
            self.__instance = None
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            if self.__instance is None:
                self.__instance = super().__call__(*args, **kwargs)
                return self.__instance
            else:
                return self.__instance

    class Spam(metaclass=Singleton):
        def __init__(self):
            print('Creating Spam')

    a = Spam()
    b = Spam()
    print(a is b)

    # 创建缓存实例
    print('=' * 20, '缓存实例', '=' * 20)
    import weakref

    class Cached(type):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__cache = weakref.WeakValueDictionary()

        def __call__(self, *args):
            if args in self.__cache:
                return self.__cache[args]
            else:
                obj = super().__call__(*args)
                self.__cache[args] = obj
                return obj

    class Spam(metaclass=Cached):
        def __init__(self, name):
            print('Creating Spam({!r})'.format(name))
            self.name = name

    a = Spam('A13X')
    b = Spam('CJ')
    c = Spam('A13X')
    print(a is b)
    print(a is c)


def func14():
    """
    获取类属性的定义顺序
    核心就在__prepare__()方法上，该特殊方法定义在元类OrderedMeta中，该方法会在类定义一开始的时候立刻得到调用，调用时以类名和基类名称作为参数。它必须返回一个映射型对象(mapping object)供处理类定义体时使用
    """
    from collections import OrderedDict

    class Typed:
        _expected_type = type(None)

        def __init__(self, name=None):
            self._name = name

        def __set__(self, instance, value):
            if not isinstance(value, self._expected_type):
                raise TypeError('Expected', self._expected_type)
            instance.__dict__[self._name] = value

    class Integer(Typed):
        _expected_type = int

    class Float(Typed):
        _expected_type = float

    class String(Typed):
        _expected_type = str

    class OrderedMeta(type):
        def __new__(cls, cls_name, bases, cls_dict):
            d = dict(cls_dict)
            order = []
            for name, value in cls_dict.items():
                if isinstance(value, Typed):
                    value._name = name
                    order.append(name)
            d['_order'] = order
            return type.__new__(cls, cls_name, bases, d)

        @classmethod
        def __prepare__(cls, cls_name, bases):
            return OrderedDict()

    class Structure(metaclass=OrderedMeta):
        def as_csv(self):
            return ', '.join(str(getattr(self, name)) for name in self._order)

    class Stock(Structure):
        name = String()
        shares = Integer()
        price = Float()

        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

    s = Stock('GOOG', 100, 490.1)
    print(s.as_csv())


def func15():
    """
    可接受可选参数的元类
    要在元类中支持关键字参数，需要保证在定义__prepare__()、__new__()以及__init__()方法时使用keyword-only参数来指定它们
    要对元类添加关键字参数，需要理解类创建过程中涉及的所有步骤。这是因为额外的参数会传递给每一个与该过程相关的方法。
    __prepare__()方法是第一个被调用的，用来创建类的名称空间，这是在处理类的定义体之前需要完成的。一般来说，这个方法只是简单地返回一个字典或者其他的映射型对象
    __new__()方法用来实例化最终得到的类型对象，它会在类的定义体被完全执行完毕后才调用
    最后调用的是__init__()方法，用来执行任何其他额外的初始化步骤

    编写元类时，比较常见的做法是只定义一个__new__()或者__init__()方法。但是，如果打算接受额外的关键字参数，那么这两个方法必须提供，并且要提供可兼容的函数签名。
    默认的__prepare__()方法可接受任意的关键字参数，只是会忽略它们，唯一一种需要自行定义__prepare__()方法的情况就是当额外的参数多少会影响到名称空间的创建管理时

    用关键字参数来配置元类可看作是通过类变量来实现同一目标的另一种方式。这么做的优点在于它们不会污染类的命名空间，因为这些参数只对于类的创建而言有意义
    """
    class MyMeta(type):
        @classmethod
        def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
            print('prepare, debug: {}, synchronize: {}'.format(debug, synchronize))
            return super().__prepare__(name, bases)

        def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
            print('new, debug: {}, synchronize: {}'.format(debug, synchronize))
            return super().__new__(cls, name, bases, ns)

        def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
            print('init, debug: {}, synchronize: {}'.format(debug, synchronize))
            super().__init__(name, bases, ns)

    class Spam(metaclass=MyMeta, debug=True, synchronize=True):
        pass

    s = Spam()


def func16():
    """
    在*args和**kwargs上强制规定一种参数签名（对传入的参数做检查）
    任何关于操作函数调用签名的问题，都应该使用inspect模块中的相应功能。
    较常用的是Signature和Parameter两个类
    """
    import inspect
    from inspect import Signature, Parameter
    parms = [
        Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
        Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=42),
        Parameter('z', Parameter.POSITIONAL_OR_KEYWORD, default=None)
    ]
    sig = Signature(parms)
    print(sig)

    """
    一旦有了签名对象，就可以通过对象的bind()方法轻松将其绑定到*args和**kwargs上
    """
    def func(*args, **kwargs):
        bound_values = sig.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            print(name, value)

    func(1, 2, 3)
    func(1)
    func(1, z=3)
    try:
        func()
    except Exception as e:
        print(e)

    """
    当定义定制化的签名时，把签名对象保存到一个特殊的属性__signature__中常常是很有用的，这么做后，使用inspect模块在执行反射操作时将能够获取签名并将其作为函数的调用约定
    """
    def make_sig(*names):
        parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
        return Signature(parms)

    class StructureMeta(type):
        def __new__(cls, cls_name, bases, cls_dict):
            cls_dict['__signature__'] = make_sig(*cls_dict.get('_fields', []))
            return super().__new__(cls, cls_name, bases, cls_dict)

    class Structure(metaclass=StructureMeta):
        _fields = []

        def __init__(self, *args, **kwargs):
            bound_values = self.__signature__.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                setattr(self, name, value)

    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x', 'y']

    print(inspect.signature(Stock))
    print(inspect.signature(Point))


def func17():
    """
    在类中强制规定编码约定
    适当使用，不要丢掉Python代码的灵活性
    如果想对类的定义进行控制，通常可以用元类来解决。一个基本的元类可以通过从type中继承，然后重定义它的__new__()或者__init__()方法即可
    元类的核心功能之一就是允许在类定义的时候对类本身的内容进行检查。在重新定义的__init__()中，我们可以自由地检查类字典、基类以及其他更多信息。此外，一旦为某个类指定了元类，该类的所有子类都会自动继承这个特性。
    在一个大型的面向对象程序中，有时候通过元类来控制类的定义会十分有用。元类可以监视类定义，可用来警告程序员那些可能被忽视的潜在问题
    """

    # 一个有趣的例子，拒绝类定义中国包含大小写混用的方法名
    class NoMixedCaseMeta(type):
        def __new__(cls, cls_name, bases, cls_dict):
            for name in cls_dict:
                if name.lower() != name:
                    raise TypeError('Bad attribute name:', name)
            return super().__new__(cls, cls_name, bases, cls_dict)

    class Root(metaclass=NoMixedCaseMeta):
        pass

    class A(Root):
        def foo_bar(self):
            pass
    try:
        class B(Root):
            def fooBar(self):
                pass
    except Exception as e:
        print(e)


def func18():
    """
    通过编程的方式来定义类
    可以使用函数types.new_class()来实例化新的类对象。所要做的就是提供类的名称、父类名称组成的元组、关键字参数以及一个用来产生类字典(class dictionary)的回调，类字典中包含着类的成员
    """

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    cls_dict = {
        '__init__': __init__,
        'cost': cost
    }

    import types

    Stock = types.new_class('Stock', (), {}, lambda ns: ns.update(cls_dict))
    """
    第三个参数还可包含其他的关键字参数
    """
    Stock.__module__ = __name__
    """
    在调用完types.new_class()后对Stock.__module__的赋值操作是这个解决方案中的微妙之处。每当定义一个类时，其__module__属性中包含的名称就是定义该类时所在的模块名
    这个名称会用来为__repr__()这样的方法产生输出，同时也会被各种库所用，因此，为了创建的类成为一个"正常"的类，需要保证将__module__属性设置妥当
    """
    s = Stock('ACME', 50, 91.1)
    print(s.cost())

    """
    也可通过"frame hack"技巧，通过sys._getframe()来获取调用者所在的模块名称
    """
    import operator, types, sys

    def named_tuple(class_name, field_names):
        cls_dict = {name: property(operator.itemgetter(n)) for n, name in enumerate(field_names)}

        def __new__(cls, *args):
            if len(args) != len(field_names):
                raise TypeError('Expected {} arguments'.format(len(field_names)))
            return tuple.__new__(cls, args)

        cls_dict['__new__'] = __new__
        cls = types.new_class(class_name, (tuple,), {}, lambda ns: ns.update(cls_dict))
        cls.__module__ = sys._getframe(1).f_globals['__name__']
        return cls

    Point = named_tuple('Point', ['x', 'y'])
    p = Point(4, 5)
    print(len(p))


def func19():
    """
    在定义的时候初始化类成员
    定义类的时候初始化类成员或者配置操作是元类的经典用途，本质上，元类是在定义类的时候触发执行，此时可以执行额外的步骤
    类StructTupleMeta接受类属性_fields中的属性名称，并将它们转换为属性方法，使得这些方法能够访问到元组的某个特定槽位
    与__init__()方法不同，__new__()方法是在类实例创建出来之前得到触发，由于元组是不可改变对象，因此，__init__()方法在类创建的过程中触发的时机太晚，以至于没法按我们想要的方法修改实例，直接是使用__new__()的原因
    """
    import operator

    class StructTupleMeta(type):
        def __init__(cls, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for n, name in enumerate(cls._fields):
                setattr(cls, name, property(operator.itemgetter(n)))

    class StructTuple(tuple, metaclass=StructTupleMeta):
        _fields = []

        def __new__(cls, *args):
            if len(args) != len(cls._fields):
                raise TypeError('{} arguments required'.format(len(cls._fields)))
            return super().__new__(cls, args)

    class Stock(StructTuple):
        _fields = ['name', 'shares', 'price']

    s = Stock('ACME', 50, 91.1)
    print(s)
    print(s[0])
    print(s.shares * s.price)


def func20():
    """
    通过函数注解来实现方法重载
    类似于Java中的多态
    可以通过本方法复习元编程相关知识，但最好不要应用到实际生产中
    """

    import inspect
    import types

    class MultiMethod:
        def __init__(self, name):
            self._methods = {}
            self.__name__ = name

        def register(self, method):
            sig = inspect.signature(method)
            types = []
            for name, parm in sig.parameters.items():
                if name == 'self':
                    continue
                if parm.annotation is inspect.Parameter.empty:
                    raise TypeError('Argument {} must be annotation with a type'.format(name))
                if not isinstance(parm.annotation, type):
                    raise TypeError('Argument {} annotation must be a type'.format(name))
                if parm.default is not inspect.Parameter.empty:
                    self._methods[tuple(types)] = method
                types.append(parm.annotation)
            self._methods[tuple(types)] = method

        def __call__(self, *args):
            types = tuple(type(arg) for arg in args[1:])
            method = self._methods.get(types, None)
            if method:
                return method(*args)
            else:
                raise TypeError('No matching method for types {}'.format(types))

        def __get__(self, instance, cls):
            if instance is not None:
                return types.MethodType(self, instance)
            else:
                return self

    class MultiDict(dict):
        def __setitem__(self, key, value):
            if key in self:
                current_value = self[key]
                if isinstance(current_value, MultiMethod):
                    current_value.register(value)
                else:
                    m_value = MultiMethod(key)
                    m_value.register(current_value)
                    m_value.register(value)
                    super().__setitem__(key, m_value)
            else:
                super().__setitem__(key, value)

    class MultipleMeta(type):
        def __new__(cls, cls_name, bases, cls_dict):
            return type.__new__(cls, cls_name, bases, cls_dict)

        @classmethod
        def __prepare__(cls, name, bases):
            return MultiDict()

    class Spam(metaclass=MultipleMeta):
        def bar(self, x: int, y: int):
            print('Bar 1:', x, y)

        def bar(self, s: str, n: int = 0):
            print('Bar 2:', s, n)

    s = Spam()
    s.bar(1,2)
    s.bar('hello')
    s.bar('hello', 10)


def func21():
    """
    避免出现重复的属性方法
    与其所有属性都用property方法包装，不如创建一个函数，让它为我们定义属性并返回
    本方法说明了内层函数或者闭包的一个重要特性：用它们编写出来的代码工作起来很像宏
    """
    def typed_property(name, expected_type):
        storage_name = '_' + name

        @property
        def prop(self):
            return getattr(self, storage_name)

        @prop.setter
        def prop(self, value):
            if not isinstance(value, expected_type):
                raise TypeError('{} must be a {}'.format(name, expected_type))
            setattr(self, storage_name, value)

        return prop

    class People:
        name = typed_property('name', str)
        age = typed_property('age', int)

        def __init__(self, name, age):
            self.name = name
            self.age = age

    """
    如果使用函数functools.partial()，还可以再次优化代码
    """
    from functools import partial

    String = partial(typed_property, expected_type=str)
    Integer = partial(typed_property, expected_type=int)

    class Person:
        name = String('name')
        age = Integer('age')

        def __init__(self, name, age):
            self.name = name
            self.age = age


def func22():
    """
    以简单的方式定义上下文管理器
    使用contextlib模块中的@contextmanager装饰器
    一般来说，编写上下文管理器，需要定义一个带有__enter__()和__exit__()方法的类，虽然也不难，但是还是比@contextmanager复杂一些
    @contextmanager只适用于编写自给自足型(self-contained)的上下文管理器函数，如果有一些对象需要支持在with语句中使用，那么还是需要__enter__()和__exit__()
    """
    import time
    from contextlib import contextmanager

    @contextmanager
    def time_this(label):
        start = time.time()
        try:
            yield 'sth'
        finally:
            end = time.time()
            print('{}: {}'.format(label, end-start))

    with time_this('counting') as sth:
        print(sth)
        n = 10000000
        while n > 0:
            n -= 1


def func23():
    """
    执行带有局部副作用的代码
    使用exec()在调用方的作用域下执行一段代码，但是执行结束后，得到的结果在当前作用域下不可见
    要解决这类问题，需要使用locals()函数在调用exec()之前获取一个保存类局部变量的字典，之后可以从本地字典中提取出修改过的值
    实践中要正确使用exec()其实是非常具有技巧性的。实际上 ，大多数考虑使用exec()的情况中，可能存在更加优雅的解决方案（如装饰器、闭包、元类等）
    在函数内部，传递给exec()的局部作用域是一个字典，而这个字典是实际局部变量的一份拷贝
    调用locals()时，它将会接受局部变量的当前值，然后覆盖字典中的对应条目
    除了使用local()之外，另一种可选方式是自己创建字典并传递给exec()
    """
    def test():
        print('=' * 20, 'test', '=' * 20)
        a = 13
        loc = locals()
        exec('b = a + 1')
        b = loc['b']
        print(b)
    test()

    def test2():
        print('=' * 20, 'test2', '=' * 20)
        x = 0
        loc = locals()
        print(loc)
        exec('x += 1')
        print(loc)
        locals()
        print(loc)
    test2()

    def test3():
        print('=' * 20, 'test3', '=' * 20)
        a = 13
        loc = {'a': a}
        glb = {}
        exec('b = a + 1', glb, loc)
        b = loc['b']
        print(b)
    test3()


def func23():
    """
    解析并分析Python源代码
    可以使用ast模块将Python源代码编译为一个抽象语法树(AST)，这样就可以分析源代码了
    语法树是由一些AST节点组成的，同这些节点打交道的最简单的方法就是定义一个访问者类，在类中实现各种visit_NodeName()方法，这里的NodeName可以匹配到所感兴趣的节点上
    分析源代码并从中得到有用的信息，可以利用这一特性编写代码分析、代码优化或者验证工具
    """
    import ast

    class CodeAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.loaded = set()
            self.stored = set()
            self.deleted = set()

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                self.loaded.add(node.id)
            elif isinstance(node.ctx, ast.Store):
                self.stored.add(node.id)
            elif isinstance(node.ctx, ast.Del):
                self.deleted.add(node.id)

    code = """
for i in range(10):
    print(i)
del i
    """

    top = ast.parse(code, mode='exec')
    c = CodeAnalyzer()
    c.visit(top)
    print('Loaded:', c.loaded)
    print('Stored:', c.stored)
    print('Deleted:', c.deleted)


def func25():
    """
    将Python源码分解为字节码
    如需在非常底层的层次下研究程序的行为，那么dis模块会非常有用
    dis模块可用来将任何Python函数分解为字节码
    """
    def count_down(n):
        while n > 0:
            print('T-minus', n)
            n -= 1
        print('Blastoff!')

    import dis
    dis.dis(count_down)


if __name__ == '__main__':
    doFunc()
