#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc

"""
很多地方都会介绍，测试是很棒的事，但调试就比较枯燥了。
个人感觉：调试清晰且优雅的代码，并使其变得更出色，是十分有趣的事。
"""


def func1():
    """
    unittest

    unittest 是 Python 内置的，最常见的，用于单元测试的模块
    """
    from io import StringIO
    import unittest
    from unittest import TestCase, TestLoader, TextTestRunner
    from unittest.mock import patch

    def url_print(protocol, host, domain):
        url = '{}://{}.{}'.format(protocol, host, domain)
        print(url, end='')

    def parse_int(s):
        return int(s)

    global MyTest

    class MyTest(TestCase):
        def test_url_gets_to_stdout(self):
            """
            测试发送到 stdout 上的输出
            unittest.mock.patch() 函数用来当做上下文管理器，把 sys.stdout 的值替换为一个 StringIO 对象。
            在这个过程中会创建一个模拟对象，即 fake_out 变量。可以在 with 语句块中使用 fake_out 来执行各种检查。
            当 with 语句块执行完毕后，patch() 函数会非常方便地将所有状态还原为测试运行之前时的状态。
            """
            protocol = 'http'
            host = 'www'
            domain = 'example.com'
            expected_url = '{}://{}.{}'.format(protocol, host, domain)
            with patch('sys.stdout', new=StringIO()) as fake_out:
                url_print(protocol, host, domain)
                self.assertEqual(fake_out.getvalue(), expected_url)

        def test_patch(self):
            """
            patch() 更广义的使用方式，
            unittest.mock.patch() 接受一个已有对象的完全限定名称并将其替换为一个新值。在装饰器函数或上下文管理器结束执行后会将对象恢复为原始值。
            """
            with patch('__main__.func1', 123):
                print(func1)

        """
        unittest 模块中有一些装饰器可作用于所选的测试方法上，以此控制它们的处理行为。
        装饰器的 skip() 可用来跳过某个分测试，skipIf() 和 skipUnless() 根据条件判断是否执行测试。
        对于已知会失败的测试项，不想让测试框架生成更多报告信息，可使用 @expectedFailure 装饰器对其进行标注
        """
        @unittest.skipIf(True, 'Do not test!!!')
        def test_bad_int(self):
            """
            assertRaise() 方法提供了一个简单的方式来测试是否出现异常。
            若 parse_int('N/A') 不出现 ValueError 异常，则上报 AssertionError 异常。
            """
            self.assertRaises(ValueError, parse_int, 'N/A')

    # 正常执行 unittest
    # 注意，执行 main() 方法后，程序会停止运行，并打印测试结果。
    unittest.main()

    def unittest_reload():
        """
        如果想对输出做重定向，需要将 unittest 的 main() 展开，编写自己的 main() 函数。

        重新编写 main() 函数暴露来 unittest 模块内部的一些工作原理。
        从基本层次来书，unittest 模块首先会组装一个测试它套件。这个测试套件中包含了各种定义的测试方法。一旦套件装配完成，它所包含的测试就开始执行。
        """
        import sys

        def main(out=sys.stderr, verbosity=2):
            loader = TestLoader()
            suite = loader.loadTestsFromModule(sys.modules[__name__])
            TextTestRunner(out, verbosity=verbosity).run(suite)

        with open('__pycache__/testing.out', 'w') as f:
            main(f)

    unittest_reload()


def func2():
    """
    异常

    Exception(绝大部分异常) + ( SystemExit + KeyboardInterrupt + GeneratorExit ) = BaseException(全部异常)
    """
    """
    要捕获异常，可以为异常类编写一个异常处理程序。
    处理异常时应尽可能使用精确的异常类。
    如果捕获所有异常，最好针对异常产生的实际原因做日志记录或报告。
    """
    try:
        pass
    except Exception as e:
        print('Exception', e)

    """
    自定义的异常类应该总是继承自内建的 Exception 类，或者继承自一些继承自 Exception 的其他类。
    不要使用 BaseException 做基类，它是预留给系统退出异常的。
    在自己的应用中使用自定义的异常，能帮助阅读源代码的人更好地理解程序的行为。
    可以通过定义有逻辑的树状的异常类，为用户提供多维度的捕获错误的能力。
    """
    class NetworkError(Exception):
        pass

    class NetworkTimeoutError(NetworkError):
        pass

    """
    要将异常串联起来，可以用 raise from 语句来替代普通的 raise。这么做能够提供这两个异常的有关信息。
    raise from None 可以阻止异常链产生。
    尽量多使用 raise from 语句。因为我们需要显式将异常产生的原因串联起来。异常的关系会在 traceback 回溯中显式给出。
    """
    try:
        pass
    except ValueError as e:
        raise RuntimeError('test error') from e

    """
    需要对某个异常做出响应，之后再传播出去。
    只需要单独使用 raise 语句即可。
    """
    try:
        pass
    except ValueError as e:
        # do something
        pass
        raise


def func3():
    """
    发出告警信息

    可使用 warnings.warn() 函数 产生告警信息。
    可以让没必要上升到异常层面的问题以告警信息的形式表达出来

    warn() 函数的参数是一条告警信息附带的一个告警类别，
    通常为 UserWarning, DeprecationWarning, SyntaxWarning, RuntimeWarning, ResourceWarning, FutureWarning 其中的一种。

    默认情况下，只显示部分告警信息。
    -W 选项能控制告警信息的输出。
    也可使用 warnings.simplefilter() 函数来控制输出。
    -W all : 输出所有告警信息，等同于 warnings.simplefilter('always')。
    -W ignore : 忽略所有告警信息，等同于 warnings.simplefilter('ignore')。
    -W error : 将告警转换为异常，等同于 warnings.simplefilter('error')。
    """
    import warnings
    warnings.warn('test warning', DeprecationWarning)
    """
    $ python -W all 14_testingDebuggingAndExceptions.py
    """


def func4():
    """
    对基本的程序崩溃问题进行调试

    注意：不要把调试弄的过于复杂

    可以通过插入一些 print() 调用来帮助我们了解程序的工作方式。traceback.print_stack() 函数会在程序调用的地方立刻打印出调用栈的信息。

    针对一些特别复杂的程序，可以插入像 pdb.set_trace() 这样的语句。从本质上说，程序会一直运行，直到遇到 set_trace() 调用为止，此时会立即进入调试器。
    """
    def func(n):
        return n + 10

    def test_i():
        """
        如果程序由于产生异常崩溃来，
        通过 python -i 的方式运行程序，可以简单地查看产生问题的原因。
        一旦程序终止，-i 选项就会开启一个交互式 shell，此时就可以探究程序的崩溃原因。
        """
        func('Hello')
        """
        $ python -i 14_testingDebuggingAndExceptions.py
        >>> func(10)
        >>> import pdb # 程序崩溃后还可以加载 python 调试器。
        >>> pdb.pm()
        """
    # test_i()

    def test_traceback():
        """
        如果代码深埋在一个难以获取交互式 shell 的环境中，通常可以捕获错误并自己生成 traceback 回溯。
        """
        import traceback
        import sys

        try:
            func('Hello')
        except:
            print('='*10, 'AN ERROR OCCURRED', '='*10)
            traceback.print_exc(file=sys.stderr)
    # test_traceback()

    def test_print_stack():
        import traceback
        import sys

        def sample(n):
            if n > 0:
                sample(n-1)
            else:
                traceback.print_stack(file=sys.stderr)
        sample(5)

    # test_print_stack()

    def test_pdb():
        import pdb

        def func():
            pdb.set_trace()
        func()

    test_pdb()


def func5():
    """
    对程序做性能分析以及计时统计

    UNIX 下的 time 命令可以简单地对整个程序做计时统计。
    $ time python doFunc.py

    如果想针对程序的行为产生一份详细的报告，可以使用 cProfile 模块
    $ python -m cProfile doFunc.py

    对代码做性能分析，更常见的情况处于上述两个极端之间。
    一般情况下，我们已经知道大部分运行时间都花费在某几个函数上。要对函数进行性能分析，使用装饰器就能办到。
    """
    def time_decorator_example():
        import time
        from functools import wraps

        def time_this(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                r = func(*args, **kwargs)
                end = time.perf_counter()
                print('{}.{} : {}'.format(func.__module__, func.__name__, end-start))
                return r
            return wrapper

        @time_this
        def countdown(n):
            while n > 0:
                n -= 1

        countdown(10000000)

    time_decorator_example()

    """
    要对语句块进行计时统计，可以定义一个上下文管理器来实现。
    """
    def time_context_example():
        import time
        from contextlib import contextmanager

        @contextmanager
        def time_block(label):
            start = time.perf_counter()
            try:
                yield
            finally:
                end = time.perf_counter()
                print('{} : {}'.format(label, end-start))

        with time_block('counting'):
            n = 10000000
            while n > 0:
                n -= 1

    time_context_example()

    """
    如果要对短小的代码片段做性能统计，timeit 模块会很有帮助。
    timeit 会执行一个参数中指定的语句一百万次，然后计算时间。
    第二个参数是一个配置字符串，在运行测试之前会先执行以设定好环境。
    如修改迭代的次数，只需提供一个 number 参数即可。
    """
    def timeit_example():
        from timeit import timeit
        print(timeit('math.sqrt(2)', 'import math'))

    timeit_example()

    """
    在进行性能测试统计时，只能得到近似值。
    解决方案中使用的函数 time.perf_counter() 能够提供给定平台上精度最高的计时器。但它计算的仍然是墙上时间(wall-clock time)，这会受到许多不同因素的影响。
    一般情况下，我们更感兴趣的是进程时间，可以使用 time.process_time()。
    """
    def time_decorator_example2():
        import time
        from functools import wraps

        def time_this(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.process_time()
                r = func(*args, **kwargs)
                end = time.process_time()
                print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
                return r
            return wrapper

        @time_this
        def countdown(n):
            while n > 0:
                n -= 1

        countdown(10000000)

    time_decorator_example2()


def func14():
    """
    让程序运行得更快

    ================================
    *** 非常重要，一些简单且有效得方法

    性能分析 + 处理热点

    成好的代码习惯，需要优化时抓大放小
    ================================

    在进行优化前，首先分析一下正在使用的算法通常都是很值得的。把算法的复杂度切换为 O(nlgn) 所带来的性能提升绝对比费力调整一个 O(n**2) 的实现要高得多。

    如果仍然决定必须优化，那么就从大的方向考虑。
    一般来说我们不会针对程序的每个部分都去优化，因为这样的修改会降低代码的可读性。
    相反，应该只针对已知的性能瓶颈做修改。

    我们应该特别留意微优化(micro-optimization)所带来的结果。

    聪明的程序员只会把精力集中在程序中会产生性能影响的地方，比如内层循环。而其他地方的速度差异根本无关紧要。

    如果我们对性能提升的要求远远超过了本节所讨论的简单技术，那么就需要考虑使用基于即使编译技术的工具了。
    例如 PyPy项目就是对 Python 解释器的重新实现，可以分析你的程序并针对频繁执行的部分生成原始机器码。有时能使 Python 程序的运行速率快上一个数量级，常常能接近（甚至超越）C代码的执行速度。
    此外，也可以考虑 Numba 项目。Numba 是一个动态编辑器，我们可以选择需要优化的 Python 函数，然后用装饰器来装饰。这些函数就会通过 LLVM 编译成原始的机器码。

    以下是几种简单好用的提升代码运行效率的方法。
    * 使用函数
    定义在全局范围内的代码运行起来比定义在函数中的代码要慢。速度的差异与局部变量和全局变量的实现机制有关。
    如果想让程序运行得更快，只需要将脚本中的语句放入一个函数中即可。
    运行速度的差异与所执行的处理有很大关系，根据经验，提升 15%～30% 的情况并非罕见。

    * 有选择性的消除属性访问
    可以通过 from module import name 的导入形式以及选择性地使用绑定方法来避免出现属性查询操作。
    只有在频繁执行的代码中做这些修改才有意义，比如在循环中。因此，这种优化技术适用的场景有限。

    * 理解变量所处的位置
    对于需要频繁访问的对象，想提高运行速度，可以通过让这些名称尽可能称为局部变量。
    使用来时，局部参数同样能起到提速的效果。一般来说，访问 self.name 会比访问局部变量慢得多。在内层循环中将需要经常访问的属性移到局部变量中会很划算。

    * 避免不必要的抽象
    任何时候，当使用额外的处理层，比如装饰器(decorator)、属性(property)或者描述符(descriptor)来包装代码时，代码的运行速度就会变慢。
    不要因为某些语言中使用 getter/setter 函数非常普遍，就错误地把这种编程风格应用到 Python 上。

    * 使用内建的容器
    内建的数据类型，比如字符串、元组、列表、集合以及字典都是用 C语言实现的，速度非常快。
    如果倾向于构建自己的数据结构作为代替(例如链表、二叉树等)，想再速度上和内建的数据结构相抗衡极其困难。
    因此，通常最好还是直接使用内建的数据结构。

    * 避免产生不必要的数据结构或者拷贝动作
    对代码效率有追求时，减少创建中间态数据结构，减少 copy 都是好习惯。
    """


if __name__ == '__main__':
    doFunc()