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
    上述例子中如果希望radius修改后, area和perimeter的值跟着改变, 可修改Circle类
    '''
    def lazyproperty(change_property=None):
        def do_func(func):
            name = '_lazy_' + func.__name__
            if change_property is not None:
                
            @property
            def lazy(self):
                if hasattr(self, name):
                    return getattr(self, name)
                else:
                    value = func(self)
                    setattr(self, name, value)
                    return value
            return lazy
        return do_func

    def test():
        import math
        class Circle:
            def __init__(self, radius):
                self.radius = radius
            @lazyproperty(change_property='radius')
            def area(self):
                print('Compution area')
                return math.pi * self.radius ** 2
            @lazyproperty(change_property='radius')
            def perimeter(self):
                print('Compution perimeter')
                return 2 * math.pi * self.radius
                
        c = Circle(4)
        print(c.radius)
        print(c.area)
        print(c.perimeter)
        c.radius = 8
        print(c.area)
        print(c.perimeter)
    print('='*50, 'test3', sep='\n')
    test()


    




















if __name__ == '__main__':
    doFunc()
