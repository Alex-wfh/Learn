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
    contextlib 模块中的 @contextmanager 装饰器可以简单的让某些对象支持上下文管理器, 详见下一章
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
    与其依赖语言特性来封装数据，Python 更推荐通过特定的命名规则来表达出对数据和方法的用途，一般遵循如下规则:
        1. 任何以单下划线(_)开头的名称应该总是被认为只属于内部实现
        2. 以双下滑线(__)开头的名称会导致出现名称重整的行为，具体来说就是名称会被重命名，前面会增加(_类名)，为: _类名__属性i名，因此，这样的属性不能通过继承而覆盖
        3. 如果想定义的名称与保留子产生冲突，应在名称最后加上单下划线(_)以示区别
    '''
    class A:
        def __init__(self):
            self.__private = -1
            self._internal = 0
            self.public = 1
        def __private_method(self):
            print('This is a private method')
        def public_method(self):
            print('This is a public method')
        def _internal_method(self):
            print('This is a internal method')

    class B(A):
        def __init__(self):
            super().__init__()
            self.__private = 0
        def __private_method(self):
            print('This is B\'s private method, not override from A!')

def func6():
    '''
    创建可管理的属性
    要定义对属性的访问，最简单的方式是将其定义为 property，property 属性实际上就是把一系列的方法绑定到一起，其遵循以下规则:
        1. 互相关联的方法必须拥有相同的名称
        2. 必须先有 property 属性，之后才能定义 setter 和 deleter
    property 看起来像一个普通属性，但根据访问它的不同方式会触发 getter、setter 以及 deleter 方法
    注意: 如果 property 不完成任何额外的处理任务，那么就不要使用它！！原因如下:
        1. property 代码更啰嗦，会给使用者带来困惑
        2. 程序运行效率会下降很多
    '''
    class Person:
        def __init__(self, first_name):
            self._first_name = first_name
        # Getter function
        @property
        def first_name(self):
            return self._first_name
        # Setter function
        @first_name.setter
        def first_name(self, value):
            if not isinstance(value, str):
                raise TypeError('Expected a string please.')
            self._first_name = value
        # Deleter function
        @first_name.deleter
        def first_name(self):
            raise AttributeError('Can\'t delete first name. For honor!')
    
    p = Person('wu')
    print(p.first_name)
    try:
        p.first_name = 1
    except TypeError as e:
        print(e)
    try:
        del p.first_name
    except AttributeError as e:
        print(e)

def func7():
    '''
    调用父类中的方法
    可使用super()函数或者通过父类类名调用
        super()函数: 默认继承调用
        父类类名: 精准调用
    python是如何继承的? 针对每一个定义的类, Python都会计算出一个称为方法解析顺序(MRO)的列表, MRO列表只是简单地对所有的基类进行线性排列, Python继承时,会根据MRO列表的顺序一次查找
    '''
    class Base:
        def __init__(self):
            print('Base.__init__')
    class A(Base):
        def __init__(self):
            Base()
            print('A.__init__')
    class B(A, Base):
        def __init__(self):
            super().__init__()
            print('B.__init__')
    B()

def func8():
    '''
    在子类中扩展属性
    要清楚是重新定义属性的所有方法, 还是只扩展其中的部分方法, 其他方法直接继承
    如果只继承部分方法, 注意要使用 父类.属性.方法
    '''
    class Person:
        def __init__(self, first_name):
            self._first_name = first_name
        # Getter function
        @property
        def first_name(self):
            print(1)
            return self._first_name
        # Setter function
        @first_name.setter
        def first_name(self, value):
            if not isinstance(value, str):
                raise TypeError('Expected a string please.')
            self._first_name = value
        # Deleter function
        @first_name.deleter
        def first_name(self):
            raise AttributeError('Can\'t delete first name. For honor!')
    class SubPerson(Person):
        @Person.first_name.getter
        def first_name(self):
            print(2)
            return super().first_name
    class SubSubPerson(SubPerson):
        @SubPerson.first_name.getter # 注意这里使用 @Person.first_name.getter 效果相同
        def first_name(self):
            print(3)
            return super().first_name
    sub_sub_person = SubSubPerson('wu')
    print(sub_sub_person.first_name)

def func9():
    '''
    创建一种新形式的类属性或实例属性
    通过定义描述符, 我们可以在很底层的情况下捕获关键的实例操作(get, set, delete),并可以完全自定义这些操作的行为. 这种能力非常强大, 是编写高级程序库和框架时最为重要的工具之一
    所谓的描述符就是以特殊方法__get__(),__set__()和__delete__()的形式实现了三个核心的属性访问操作的类
    当这么做时,所有针对描述符属性的访问都会被__get__(),__set__()和__delete__()方法所捕获
    __get__()看起来复杂的原因在于实例变量和类变量之间是有区别的, 如果以类变量的形式访问描述符, 参数instance应该设为None. 这种情况下, 标准的做法就是返回描述符实例本身
    注意: 如果只是想访问某个特定的类中的一种属性, 并对次做定制化处理, 那么最好不要通过描述符来实现, 应该使用property属性方法更简单. 只有需要大量重用代码时, 才考虑描述符
    '''
    class Integer:
        def __init__(self, name):
            self.name = name
        def __get__(self, instance, cls):
            print('__get__', instance, cls)
            if instance is None:
                return self
            else:
                return instance.__dict__[self.name]
        def __set__(self, instance, value):
            print('__set__', instance, value)
            if not isinstance(value, int):
                raise TypeError('Expected an int')
            instance.__dict__[self.name] = value
        def __delete__(self, instance):
            print('__delete__', instance)
            del instance.__dict__[self.name]
    class Point:
        x = Integer('x')
        y = Integer('y')
        def __init__(self, x, y):
            self.x = x
            self.y = y
    p = Point(2,3)
    print('do p.x', p.x, sep='\n')
    print('do Point.x', Point.x, sep='\n')
    print('do del p.x')
    del p.x
    print('do set p.y = 4')
    p.y = 4
    print('do set p.y = 2.3')
    p.y = 2.3

def func10():
    '''
    让属性具有惰性求值的能力
    定义一个惰性属性最有效的方法就是利用描述符来完成
    让属性具有惰性求值能力的全部意义就在于提升程序性能
    lazyproperty类通过让__get__()方法以property属性相同的名称来保存计算出的值, 这么做会让值保存在实例字典中, 可以阻止该property属性重复进行计算
    '''
    class lazyproperty:
        def __init__(self, func):
            self.func = func
        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                value = self.func(instance)
                setattr(instance, self.func.__name__, value)
                return value
    def test():
        import math
        class Circle:
            def __init__(self, radius):
                self.radius = radius
            @lazyproperty
            def area(self):
                print('Compution area')
                return math.pi * self.radius ** 2
            @lazyproperty
            def perimeter(self):
                print('Compution perimeter')
                return 2 * math.pi * self.radius
        c = Circle(4)
        print(c.radius)
        print(c.area)
        print(c.perimeter)
        c.area = 25
        print(c.area)
        print(c.perimeter)
    print('test1')
    test()
    '''
    上述技术有个缺点, 计算出的值在创建之后就变成可变的
    如果考虑可变性的问题, 可以使用另一种方式实现, 但执行效率会稍打折扣
    '''
    def lazyproperty(func):
        name = '_lazy_' + func.__name__
        @property
        def lazy(self):
            if hasattr(self, name):
                return getattr(self, name)
            else:
                value = func(self)
                setattr(self, name, value)
                return value
        return lazy
    print('='*50, 'test2', sep='\n')
    try:
        test()
    except Exception as e:
        print(e)
    print('test1')
    '''
    上述例子中如果希望radius修改后, area和perimeter的值跟着改变, 具体怎么做还没想好, 先余着!!!!
    '''

def func11():
    '''
    简化数据结构的初始化过程
    如果程序中有大量小型的数据结构, 那么定义一个通用型的__init__()方法会特别有用. 
    '''
    print('='*10, ' base version ', '='*10)
    class Structure:
        _fields = []
        def __init__(self, *args):
            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))
            for name, value in zip(self._fields, args):
                setattr(self, name, value)
    def test():
        class Stock(Structure):
            _fields = ['name', 'shares', 'price']
        try:
            s = Stock('ACME', 50, 91.1)
        except Exception as e:
            print(e)
        try:
            s = Stock('ACME', 50)
        except Exception as e:
            print(e)
    test()
    '''
    支持关键字参数
    方案1: 对关键字参数做映射, 只对应定义在_fields中的属性名
    '''
    print('='*10, ' kwargs version 1, key map ', '='*10)
    class Structure:
        _fields = []
        def __init__(self, *args, **kwargs):
            if len(args) > len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))
            for name, value in zip(self._fields, args):
                setattr(self, name, value)
            for name in self._fields[len(args):]:
                if name not in kwargs:
                    raise TypeError('Error arguments, name: {}'.format(name))
                setattr(self, name, kwargs.pop(name))
            if kwargs:
                raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))
    def test():
        class Stock(Structure):
            _fields = ['name', 'shares', 'price']
        try:
            s = Stock('ACME', 50, 91.1)
        except Exception as e:
            print(e)
        try:
            s = Stock('ACME', 50, price=91.1)
        except Exception as e:
            print(e)
        try:
            s = Stock('ACME', 50, shares=91.1)
        except Exception as e:
            print(e)
        try:
            s = Stock('ACME', 50, price=91.1, info='123')
        except Exception as e:
            print(e)
    test()
    '''
    支持关键字参数
    方案2: 利用关键字参数给类添加额外的属性, 这些额外的属性没有定义在_fields中
    '''
    print('='*10, ' kwargs version 2, extra keys ', '='*10)
    class Structure:
        _fields = []
        def __init__(self, *args, **kwargs):
            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))
            for name, value in zip(self._fields, args):
                setattr(self, name, value)
            for name, value in kwargs.items():
                setattr(self, name, value)
    def test():
        class Stock(Structure):
            _fields = ['name', 'shares', 'price']
        try:
            s = Stock('ACME', 50, 91.1)
        except Exception as e:
            print(e)
        try:
            s = Stock('ACME', 50, 91.1, info='123')
        except Exception as e:
            print(e)
        try:
            s = Stock('ACME', 50, shares=91.1)
        except Exception as e:
            print(e)
    test()
    '''
    如果使用__dict__代替setattr, 会导致创建出来的类不能使用__slots__和property
    '''
    '''
    该技术存在一个问题: 会影响到IDE的文档和帮助功能
    如果想解决这个问题, 可以采用所谓的“frame hack”技术(编写一个功能函数)
    但是该技术会导致代码量大、效率低, 不推荐
    '''
    print('='*10, ' frame hack ', '='*10)
    def init_fromlocals(self):
        import sys
        locs = sys._getframe(1).f_locals
        for k, v in locs.items():
            if k != 'self':
                setattr(self, k, v)
    class Stock:
        def __init__(self, name, shares, prices):
            init_fromlocals(self)
    s = Stock('ACME', 50, 91.1)

def func12():
    '''
    定义一个接口或抽象基类
    要定义一个抽象基类, 可以使用abc模块
    抽象基类的核心特征就是不能被直接实例化
    相反, 抽象基类是用来给其他的类当做基类使用的
    这些子类需要实现基类中要求的方法, 抽象基类的主要用途是强制规定所需的编程接口
    @abstractmethod同样可以施加到静态方法、类方法和property属性上, 注意: @abstractmethod要紧挨着函数定义

    标准库中已经定义好了一些抽象基类. collections 模块中定义了多个和容器还有迭代器(序列、映射、集合等)相关的抽象基类. numbers库中定义了和数值对象(整数、浮点数、复数等)相关的抽象基类. io库中定义类和I/O处理相关的抽象基类. 可以使用这些预定义好的抽象基类来执行更加一般化的类型检查

    尽管抽象基类使得类型检查变得更容易了, 但不应该在程序中过渡使用它.
    Python的核心在于它是一种动态语言, 它带来了极大的灵活性. 如果处处都强制实行类型约束, 会使代码变得更复杂.
    我们应该拥抱Python的灵活性
    '''
    from abc import ABCMeta, abstractmethod
    class IStream(metaclass=ABCMeta):
        @abstractmethod
        def read(self, maxbytes=-1):
            pass
        @abstractmethod
        def write(self, data):
            pass
    print('='*10, ' class to instance ', '='*10)
    try:
        a = IStream()
    except Exception as e:
        print(e)

    print('='*10, ' child class ', '='*10)
    class SocketStream(IStream):
        def read(self, maxbytes=-1):
            return self.data
        def write(self, data):
            self.data = data
    a = SocketStream()
    a.write('123')
    print(a.read())

def func13():
    '''
    实现一种数据模型或类型系统
    设定特定的实例属性时添加检查或者断言
    使用描述符
    '''
    class Descriptor:
        def __init__(self, name=None, **opts):
            self.name = name
            for key, value in opts.items():
                setattr(self, key, value)
        def __set__(self, instance, value):
            instance.__dict__[self.name] = value
    class Typed(Descriptor):
        expected_type = type(None)
        def __set__(self, instance, value):
            if not isinstance(value, self.expected_type):
                raise TypeError('expected {}'.format(self.expected_type))
            super().__set__(instance, value)
    class Unsigned(Descriptor):
        def __set__(self, instance, value):
            if value < 0:
                raise ValueError('Expected >= 0')
            super().__set__(instance, value)
    class MaxSized(Descriptor):
        def __init__(self, name=None, **opts):
            if 'size' not in opts:
                raise ValueError('missing size option')
            super().__init__(name, **opts)
        def __set__(self, instance, value):
            if len(value) >= self.size:
                raise ValueError('size must be < {}'.format(self.size))
            super().__set__(instance, value)
    '''
    这些类可以作为构建一个数据模型或者类型系统的基础组建, 继续实现一些不同类型的数据
    '''
    class Integer(Typed):
        expected_type = int
    class UnsignedInteger(Integer, Unsigned):
        pass
    class Float(Typed):
        expected_type = float
    class UnsignedFloat(Float, Unsigned):
        pass
    class String(Typed):
        expected_type = str
    class SizedString(String, MaxSized):
        pass
    '''
    通过上述对象定义类
    '''
    class Stock:
        name = SizedString('name', size=8)
        shares = UnsignedInteger('shares')
        price = UnsignedFloat('price')
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price
    def test():
        s = Stock('ACME', 50, 91.1)
        try:
            s.shares = -10
        except Exception as e:
            print(e)
        try:
            s.price = 'a lot'
        except Exception as e:
            print(e)
    print('='*10, ' base version ', '='*10)
    test()
    '''
    可以运用一些技术来简化类中设定约束的步骤,
    方法1: 类装饰器
    '''
    def check_attributes(**kwargs):
        def decorate(cls):
            for key, value in kwargs.items():
                if isinstance(value, Descriptor):
                    value.name = key
                    setattr(cls, key, value)
                else:
                    setattr(cls, key, value(key))
            return cls
        return decorate

    @check_attributes(
        name=SizedString(size=8),
        shares = UnsignedInteger,
        price=UnsignedFloat
    )
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price
    print('='*10, ' class decorator ', '='*10)
    test()  

    '''
    方法2: 元类
    '''
    class checkedmeta(type):
        def __new__(cls, clsname, bases, methods):
            for key, value in methods.items():
                if isinstance(value, Descriptor):
                    value.name = key
            return type.__new__(cls, clsname, bases, methods)
    class Stock(metaclass=checkedmeta):
        name = SizedString('name', size=8)
        shares = UnsignedInteger('shares')
        price = UnsignedFloat('price')
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price
    print('='*10, ' meta class ', '='*10)
    test()

    '''
    所有方法中, 类装饰器可以提供最大的灵活性和稳健性, 好处如下:
    1. 不依赖于任何高级机制, 例如元类
    2. 装饰器可以很容易地根据需要在类定义上添加或移除
    '''
    '''
    采用类装饰器的解决方案也可以用来取代mixin类、多重继承以及对super()函数的使用
    该方案能够以完全相同的方式工作, 且每个部分都更快
    '''
    class Descriptor:
        def __init__(self, name=None, **opts):
            self.name = name
            for key, value in opts.items():
                setattr(self, key, value)
        def __set__(self, instance, value):
            instance.__dict__[self.name] = value
    def Typed(expected_type, cls=None):
        if cls is None:
            return lambda cls : Typed(expected_type, cls)
        super_set = cls.__set__
        def __set__(self, instance, value):
            if not isinstance(value, expected_type):
                raise TypeError('expected {}'.format(expected_type))
            super_set(self, instance, value)
        cls.__set__ = __set__
        return cls
    def Unsigned(cls):
        super_set = cls.__set__
        def __set__(self, instance, value):
            if value < 0:
                raise ValueError('Expected >= 0')
            super_set(self, instance, value)
        cls.__set__ = __set__
        return cls
    def MaxSized(cls):
        super_init = cls.__init__
        def __init__(self, name=None, **opts):
            if 'size' not in opts:
                raise TypeError('missing size option')
            super_init(self, name, **opts)
        cls.__init__ = __init__
        super_set = cls.__set__
        def __set__(self, instance, value):
            if len(value) >= self.size:
                raise ValueError('size must be < {}'.format(len(self.size)))
            super_set(self, instance, value)
        cls.__Set__ = __set__
        return cls
    @Typed(int)
    class Integer(Descriptor):
        pass
    @Unsigned
    class UnsignedInteger(Integer):
        pass
    @Typed(float)
    class Float(Descriptor):
        pass
    @Unsigned
    class UnsignedFloat(Float):
        pass
    @Typed(str)
    class String(Descriptor):
        pass
    @MaxSized
    class sizedString(String):
        pass
    print('='*10, ' all class decorator ', '='*10)
    test()

def func14():
    '''
    实现自定义的容器
    模仿内建容器类型 -> 继承collections中基类
    模仿数值数据类型 -> 继承numbers中基类
    '''
    from collections.abc import Iterable
    '''
    从collections.Iterable中继承的好处就是可以确保必须实现所有所需的特殊方法
    在collections库中还有其他一些基类, Sequence、MutableSequence、Mapping、MutableMapping、Set、MutableSet
    '''
    class A(Iterable):
        # 继承Iterable基类, 必须实现__iter__()方法
        def __iter__():
            yield 1
    a = A()

def func15():
    '''
    委托属性的访问
    委托有时候可以作为继承的替代方案, 有时候当直接使用继承可能没多大意义, 或者我们想更多地控制对象之间的关系, 此时委托会很有用
    当使用委托来实现代理时, 有几个细节需要注意:
    1. __getattr__() 实际上是一个回滚(fallback)方法, 它只会在某个属性没有找到的时候才会调用
    2. __setattr__() 和 __delattr__() 方法需要添加一点额外的逻辑来区分代理实例本身的属性和内部对象_obj上的属性, 常用的惯例是代理类只委托那些不以下划线开头的属性
    3. __getattr__() 方法通常不适用于大部分名称以双下滑线开头和结尾的特殊方法
    '''
    class A:
        def spam(self, x):
            print('A.spam', x)
        def foo(self):
            print('A.foo')
    class B:
        def __init__(self):
            self._a = A()
        def spam(self, x):
            print('B.spam', x)
            self._a.spam(x)
        def bar(self):
            print('B.bar')
        def __getattr__(self, name):
            return getattr(self._a, name)
    b = B()
    b.spam('abc')
    b.bar()
    b.foo()

def func16():
    '''
    在类中定义多个构造函数
    可用@classmethod装饰类方法
    类方法的一大主要用途就是定义其他可选的构造函数. 类方法的一个关键特性就是把类作为其接收的第一个参数(cls). 类方法中会用到这个类来创建并返回最终的实例
    当定义一个有着多个构造函数的类时, 应该让 __init__() 函数尽可能简单——除了给属性赋值之外什么都不做. 如果需要的话, 可以在其他备选的构造函数中选择实现更高级的操作
    '''
    import time
    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day
        def __str__(self):
            return 'Date: {}.{}.{}'.format(self.year, self.month, self.day)
        @classmethod
        def today(cls):
            t = time.localtime()
            return cls(t.tm_year, t.tm_mon, t.tm_mday)
    d = Date.today()
    print(d)

def func17():
    '''
    不通过调用init来创建实例
    当需要以非标准的方式来创建实例时常常会遇到需要绕过__init__()的情况. 比如反序列化(deserializing)数据, 或者实现一个类方法将其作为备选的构造函数
    当需要以非标准的方式创建实例时, 通常最好不要对它们的实现做过多假设. 因此, 一般来说不要编写直接操纵底层实例字典__dict__的代码, 除非能保证它已被定义. 否则 如果类中使用来__slots__、property属性、描述符或者其他高级技术, 那么代码就会崩溃. 通过使用setattr()来为属性设定值, 代码就会尽可能通用
    '''
    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day
        def __str__(self):
            return 'Date: {}.{}.{}'.format(self.year, self.month, self.day)
    d = Date.__new__(Date)
    try:
        print(d)
    except Exception as e:
        print(e)
    data = {'year':2020, 'month':6, 'day':12}
    for key, value in data.items():
        setattr(d, key, value)
    print(d)

def func18():
    '''
    用Mixin技术类来扩展类定义
    Python 标准库中到处都是 mixin 类的身影, 大部分都是为了扩展其他类的功能而创建的, mixin类也是多重继承的主要用途之一
    mixin类有以下几个重要的实现细节:
    1. mixin 类绝不是为了直接实例化而创建的
    2. mixin 类一般来说是没有状态的, 这意味着mixin类没有__init__()方法, 也没有实例变量. 定义__slots__ = ()就是一种强烈的提示, 这表示mixin类没有属于自己的实例数据
    '''
    class LoggedMappingMixin:
        __slots__ = ()
        def __getitem__(self, key):
            print('Getting', key)
            return super().__getitem__(key)
        def __setitem__(self, key, value):
            print('Setting {} = {!r}'.format(key, value))
            return super().__setitem__(key, value)
        def __delitem__(self, key):
            print('Deleting', key)
            return super().__delitem__(key)
    class LoggedDict(LoggedMappingMixin, dict):
        pass
    def test():
        d = LoggedDict()
        d['x'] = 23
        d['x']
        del d['x']
    print('='*10, ' simple mixin ', '='*10)
    test()
    '''
    实现mixin的另一种方法是利用类装饰器
    '''
    def LoggedMapping(cls):
        cls_getitem = cls.__getitem__
        cls_setitem = cls.__setitem__
        cls_delitem = cls.__delitem__
        def __getitem__(self, key):
            print('Getting', key)
            return cls_getitem(self, key)
        def __setitem__(self, key, value):
            print('Setting {} = {!r}'.format(key, value))
            return cls_setitem(self, key, value)
        def __delitem__(self, key):
            print('Deleting', key)
            return cls_delitem(self, key)
        cls.__getitem__ = __getitem__
        cls.__setitem__ = __setitem__
        cls.__delitem__ = __delitem__
        return cls
    @LoggedMapping
    class LoggedDict(dict):
        pass
    print('='*10, ' class decorator mixin ', '='*10)
    test()

def func19():
    '''
    实现带有状态的对象或状态机
    编写含有大量复杂的条件判断并合各种状态纠缠在一起的代码是难以维护和解读的
    '''
    '''
    简单方法, 代码引入许多针对状态的条件检查, 过于复杂; 普通操作总要先检查状态, 程序的性能下降了
    '''
    class Connection:
        def __init__(self):
            self.state = 'CLOSE'
        def read(self):
            if self.state != 'OPEN':
                raise RuntimeError('Not open')
            print('reading')
            return self.data
        def write(self, data):
            if self.state != 'OPEN':
                raise RuntimeError('Not open')
            print('writing')
            self.data = data
        def open(self):
            if self.state == 'OPEN':
                raise RuntimeError('Already open')
            self.state = 'OPEN'
            print('opening')
        def close(self):
            if self.state == 'CLOSE':
                raise RuntimeError('Already close')
            print('closing')
            self.state = 'CLOSE'
            del self.data
    def test():
        c = Connection()
        c.open()
        c.write('123')
        c.read()
        c.close()
    print('='*10, ' simple version ', '='*10)
    test()

    '''
    更优雅方法, 将每种操作状态以一个单独的类来定义, 然后在 Connection 类中使用这些状态类
    '''
    class Connection:
        def __init__(self):
            self.new_state(CloseConnectionState)
        def new_state(self, newstate):
            self._state = newstate
        def read(self):
            self._state.read(self)
        def write(self, data):
            return self._state.write(self, data)
        def open(self):
            return self._state.open(self)
        def close(self):
            return self._state.close(self)
    class ConnectionState:
        @staticmethod
        def read(conn):
            raise NoImplementedError()
        @staticmethod
        def write(conn, data):
            raise NoImplementedError()
        @staticmethod
        def open(conn):
            raise NoImplementedError()
        @staticmethod
        def close(conn):
            raise NoImplementedError()
    class CloseConnectionState(ConnectionState):
        @staticmethod
        def read(conn):
            raise RuntimeError('Not open')
        @staticmethod
        def write(conn, data):
            raise RuntimeError('Not open')
        @staticmethod
        def open(conn):
            conn.new_state(OpenConnectionState)
        @staticmethod
        def close(conn):
            raise RuntimeError('Already close')
    class OpenConnectionState(ConnectionState):
        @staticmethod
        def read(conn):
            print('reading')
            return conn.data
        @staticmethod
        def write(conn, data):
            print('writing')
            conn.data = data
        @staticmethod
        def open(conn):
            raise RuntimeError('Already open')
        @staticmethod
        def close(conn):
            conn.new_state(CloseConnectionState)
    print('='*10, ' many class version ', '='*10)
    test()

    '''
    可通过直接修改实例的__class__属性实现, 面向对象编程的用泵通常不喜欢这么做, 个人认为这样挺好
    此外, 这种实现方案的效率更高, 因为调用connection上的所有方法都不必再经过一层额外的间接步骤了
    '''
    class Connection:
        def __init__(self):
            self.new_state(CloseConnectionState)
        def new_state(self, newstate):
            self.__class__ = newstate
        def read(self):
            raise NoImplementedError()
        def write(self, data):
            raise NoImplementedError()
        def open(self):
            raise NoImplementedError()
        def close(self):
            raise NoImplementedError()
    class CloseConnectionState(Connection):
        def read(self):
            raise RuntimeError('Not open')
        def write(self, data):
            raise RuntimeError('Not open')
        def open(self):
            self.new_state(OpenConnectionState)
        def close(self):
            raise RuntimeError('Already close')
    class OpenConnectionState(Connection):
        def read(self):
            print('reading')
            return self.data
        def write(self, data):
            print('writing')
            self.data = data
        def open(self):
            raise RuntimeError('Already open')
        def close(self):
            self.new_state(CloseConnectionState)
    print('='*10, ' __class__ version ', '='*10)
    test()

def func20():
    '''
    调用对象上的方法, 方法名以字符串形式给出
    调用一个方法实际上涉及两个单独的步骤, 一是查询属性, 二是函数调用. 因此, 要调用一个方法, 可以使用getattr()来查询相应的属性. 要调用查询到的方法, 只要把查询的结果当做函数即可.
    operator.methodcall() 创建了一个可调用对象, 而且把所需的参数提供给了被调用的方法. 我们所要做的就是提供恰当的self参数
    '''
    import math
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return 'Point({!r:}, {!r:})'.format(self.x, self.y)
        def distance(self, x, y):
            return math.hypot(self.x - x, self.y - y)
    p = Point(2,3)
    d = getattr(p, 'distance')(0,0)
    print(d)

    import operator
    d = operator.methodcaller('distance', 0, 0)(p)
    print(d)
    d = operator.methodcaller('distance', 0, 0)
    print(d(p))

def func21():
    '''
    实现访问者模式
    我们需要编写代码来处理或遍历一个由许多不同类型的对象组成的复杂数据结构, 每种对象处理的方式都不相同
    解决方案涵盖了两个核心思想:
        1. 设计策略: 把复杂数据结构的代码和数据结构本身进行结偶
        2. 对访问者类本身的实现: 在访问者中, 通过一些小技巧将方法名构建出来, 再利用getattr()函数来获取方法.
    访问者模式的一个缺点就是需要重度依赖递归, 如果要处理一个深度嵌套的数据结构, 那么有可能会达到Python的递归深度限制. 要避免这个问题, 可以在构建数据结构时做一些特定的选择. 例如可以使用普通的Python列表来替代链表, 或者在每个节点中聚合更多数据. 也可以尝试利用生成器和迭代器实现非递归式的遍历算法
    
    '''
    class Node:
        pass
    class UnaryOperator(Node):
        def __init__(self, operand):
            self.operand = operand
    class BinaryOperator(Node):
        def __init__(self, left, right):
            self.left = left
            self.right = right
    class Add(BinaryOperator):
        pass
    class Sub(BinaryOperator):
        pass
    class Mul(BinaryOperator):
        pass
    class Div(BinaryOperator):
        pass
    class Negate(UnaryOperator):
        pass
    class Number(Node):
        def __init__(self, value):
            self.value = value
    t1 = Sub(Number(3), Number(4))
    t2 = Mul(Number(2), t1)
    t3 = Div(t2, Number(5))
    t4 = Add(Number(1), t3)

    class NodeVisitor:
        def visit(self, node):
            methname = 'visit_' + type(node).__name__
            meth = getattr(self, methname, None)
            if meth is None:
                meth = self.generic_visit
            return meth(node)
        def generic_visit(self, node):
            raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))
    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value
        def visit_Add(self, node):
            return self.visit(node.left) + self.visit(node.right)
        def visit_Sub(self, node):
            return self.visit(node.left) - self.visit(node.right)
        def visit_Mul(self, node):
            return self.visit(node.left) * self.visit(node.right)
        def visit_Div(self, node):
            return self.visit(node.left) / self.visit(node.right)
        def visit_Negate(self, node):
            return -node.operand
    e = Evaluator()
    print(e.visit(t4))

def func22():
    '''
    实现非递归的访问者模式
    有时, 巧妙利用生成器可以消除树的遍历或查找算法中的递归, 这种令人费解的技巧常常能带来很大的优势
        1. 在有关遍历树结构的问题中, 为了避免使用递归, 常见的策略就是利用栈或者队列来实现算法
        2. 当遇到yield语句时, 生成器会产生出一个值然后停止执行, 可利用这个特性来取代递归
    yield的主要优势在于能够以优雅的风格编写出非递归式的代码, 而且看起来和递归式的实现几乎一样
    '''
    import types
    class Node:
        pass
    class NodeVisitor:
        def visit(self, node):
            stack = [ node ]
            last_result = None
            while stack:
                try:
                    last = stack[-1]
                    if isinstance(last, types.GeneratorType):
                        stack.append(last.send(last_result))
                        last_result = None
                    elif isinstance(last, Node):
                        stack.append(self._visit(stack.pop()))
                        last_result = None
                    else:
                        last_result = stack.pop()
                except StopIteration:
                    stack.pop()
            return last_result
        def _visit(self, node):
            methname = 'visit_' + type(node).__name__
            meth = getattr(self, methname, None)
            if meth is None:
                meth = self.generic_visit
            return meth(node)
        def generic_visit(self, node):
            raise RuntimeError('No {} method'.format('visit_' + type(nade).__name__))
    class UnaryOperator(Node):
        def __init__(self, operand):
            self.operand = operand
    class BinaryOperator(Node):
        def __init__(self, left, right):
            self.left = left
            self.right = right
    class Add(BinaryOperator):
        pass
    class Sub(BinaryOperator):
        pass
    class Mul(BinaryOperator):
        pass
    class Div(BinaryOperator):
        pass
    class Negate(UnaryOperator):
        pass
    class Number(Node):
        def __init__(self, value):
            self.value = value
    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value
        def visit_Add(self, node):
            print('Add:', node)
            lhs = yield node.left
            print('left=', lhs)
            rhs = yield node.right
            print('right=', rhs)
            yield lhs + rhs
        def visit_Sub(self, node):
            print('Sub:', node)
            lhs = yield node.left
            print('left=', lhs)
            rhs = yield node.right
            print('right=', rhs)
            yield lhs - rhs
        def visit_Mul(self, node):
            print('Mul:', node)
            lhs = yield node.left
            print('left=', lhs)
            rhs = yield node.right
            print('right=', rhs)
            yield lhs * rhs
        def visit_Div(self, node):
            print('Div:', node)
            lhs = yield node.left
            print('left=', lhs)
            rhs = yield node.right
            print('right=', rhs)
            yield lhs / rhs
        def visit_Negate(self, node):
            yield -(yield node.operand)

    t1 = Sub(Number(3), Number(4))
    t2 = Mul(Number(2), t1)
    t3 = Div(t2, Number(5))
    t4 = Add(Number(1), t3)
    e = Evaluator()
    print(e.visit(t4))

def func23():
    '''
    在环状数据结构中管理内存
    环状数据结构是Python中一个需要一些技巧才能处理好的方面, 因为普通的垃圾收集规则并不适用于环状数据结构
    Python的垃圾收集器是基于简单的引用计数规则来实现的, 当引用计数为0时就会被立刻删除掉. 而对于环状数据结构来说这是不可能发生的, 针对此问题, 我们应该考虑让环状数据结构其中的一条连接使用weakref库提供的弱引用机制
    弱引用通过消除循环引用来解决这个问题, 本质上说, 弱引用就是一个指向对象的指针, 但不会增加对象本身的引用计数
    '''
    import weakref
    class Node:
        def __init__(self, value):
            self.value = value
            self._parent = None
            self.children = []
        def __repr__(self):
            return 'Node({!r:})'.format(self.value)
        @property
        def parent(self):
            return self._parent if self._parent is None else self._parent()
        @parent.setter
        def parent(self, node):
            self._parent = weakref.ref(node)
        def add_child(self, child):
            self.children.append(child)
            child.parent = self
    root = Node('parent')
    c1 = Node('child')
    root.add_child(c1)
    print(c1.parent)
    del root
    print(c1.parent)

def func24():
    '''
    让类支持比较操作
    方案1: 定义__lt__()、__le__()等一系列方法(不推荐)
    方案2: 使用functools.total_ordering装饰器, 然后定义__eq__()以及另一个比较方法, 那么装饰器会自动为我们实现其他的比较方法
    '''
    from functools import total_ordering
    class Room:
        def __init__(self, name, length, width):
            self.name = name
            self.length = length
            self.width = width
            self.square_feet = self.length * self.width
    @total_ordering
    class House:
        def __init__(self, name, style):
            self.name = name
            self.style = style
            self.rooms = list()
        @property
        def living_space_footage(self):
            return sum(r.square_feet for r in self.rooms)
        def add_room(self, room):
            self.rooms.append(room)
        def __str__(self):
            return '{}: {} square foot {}'.format(self.name, self.living_space_footage, self.style)
        def __eq__(self, other):
            return self.living_space_footage == other.living_space_footage
        def __lt__(self, other):
            return self.living_space_footage < other.living_space_footage
    h1 = House('h1', 'Cape')
    h1.add_room(Room('Master Bedroom', 14, 21))
    h1.add_room(Room('Living Room', 18, 20))
    h1.add_room(Room('Kitchen', 12, 16))
    h1.add_room(Room('Office', 12, 12))
    h2 = House('h2', 'Ranch')
    h2.add_room(Room('Master Bedroom', 14, 21))
    h2.add_room(Room('Living Room', 18, 20))
    h2.add_room(Room('Kitchen', 12, 16))
    h3 = House('h3', 'Split')
    h3.add_room(Room('Master Bedroom', 14, 21))
    h3.add_room(Room('Living Room', 18, 20))
    h3.add_room(Room('Office', 12, 16))
    h3.add_room(Room('Kitchen', 15, 17))
    houses = [h1, h2, h3]
    print('Is h1 bigger than h2?', h1 > h2) # prints True
    print('Is h2 smaller than h3?', h2 < h3) # prints True
    print('Is h2 greater than or equal to h1?', h2 >= h1) # Prints False
    print('Which one is biggest?', max(houses)) # Prints 'h3: 1101-square-foot Split'
    print('Which is smallest?', min(houses)) # Prints 'h2: 846-square-foot Ranch'

def func25():
    '''
    创建缓存实例
    当创建类实例时我们想返回一个缓存引用, 让其指向上一个用同样参数(如果有的话)创建出的类实例
    '''
    '''
    依赖全局变量以及一个与原始类定义相分离的工厂函数
    '''
    class Spam:
        def __init__(self, name):
            self.name = name
    import weakref
    _spam_cache = weakref.WeakValueDictionary()
    def get_spam(name):
        if name not in _spam_cache:
            s = Spam(name)
            _spam_cache[name] = s
        else:
            s = _spam_cache[name]
        return s
    def test():
        a = get_spam('foo')
        b = get_spam('bar')
        c = get_spam('foo')
        print(a is b, a is c)
    print('='*10, ' base version ', '='*10)
    test()
    '''
    改进方案1, 将缓存代码放到另一个单独的管理类中, 然后将这些组件粘合在一起
    这种方法的特点就是为潜在的灵活性提供类更多的支持
    '''
    import weakref
    class CachedSpamManager:
        def __init__(self):
            self._cache = weakref.WeakValueDictionary()
        def get_spam(self, name):
            if name not in self._cache:
                s = Spam(name)
                self._cache[name] = s
            else:
                s = self._cache[name]
            return s
        def clear(self):
            self._cache.clear()
    class Spam:
        manager = CachedSpamManager()
        def __init__(self, name):
            self.name = name
        def get_spam(name):
            return Spam.manager.get_spam(name)
    print('='*10, ' mproved version 1 ', '='*10)
    test()
    '''
    改进方案2, 避免用户直接使用Spam类
    1. 使用_Spam提示用户不应该直接实例化Spam对象
    2. 让__init__()方法抛出一个异常, 然后用一个类方法实现构造函数功能
    '''
    class _Spam:
        def __init__(self, *args, **kwargs):
            raise RuntimeError('Can\'t instantiate directly')
        @classmethod
        def _new(cls, name):
            self = cls.__new__(cls)
            self.name = name
    class CachedSpamManager:
        def __init__(self):
            self._cache = weakref.WeakValueDictionary()
        def get_spam(self, name):
            if name not in self._cache:
                s = _Spam(name)
                self._cache[name] = s
            else:
                s = self._cache[name]
            return s
        def clear(self):
            self._cache.clear()
    print('='*10, ' mproved version 2 ', '='*10)
    test()





















if __name__ == '__main__':
    doFunc()
