#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc

"""
熟练掌握使用脚本和系统管理相关技巧后，
会发现打杂能力上升一档，
打杂任务也随之增加。
"""


def func1():
    """
    通过重定向、管道或输入文件作为脚本的输入

    函数 fileinput.input() 创建并返回一个 FileInput 类的实例。除了包含有一些方便实用的帮助函数外，该实例还可以当做上下文管理器来用。
    """
    import fileinput

    def fileinput_test1():
        with fileinput.input() as f_input:
            for line in f_input:
                print(line, end='')
        """
        $ python 13_utilityScriptingAndSystemAdministration.py /etc/passwd
        $ python 13_utilityScriptingAndSystemAdministration.py < /etc/passwd
        """

    def fileinput_test2():
        with fileinput.input('/etc/passwd') as f:
            for line in f:
                print(f.filename(), f.lineno(), line, end='')
    fileinput_test2()


def func2():
    """
    终止程序并显式错误信息

    让程序在终止时向标准错误输出打印一条消息并返回一个非零的状态码，可以发出一个 SystemExit 异常，并提供错误信息作为参数。这会导致提供的信息打印到 sys.stderr 上，且程序退出时的状态码为1。
    """
    raise SystemExit('It failed!')


def func3():
    """
    解析命令行选项

    简单需求用 sys.argv，复杂需求用 argparse。
    argparse 模块是标准库中最为庞大的模块之一，有非常多的配置选项。
    要解析命令行选项，首先需要创建一个 ArgumentParser 实例，并通过使用 add_argument() 方法来添加想要支持的选项声明。
    在每个 add_argument() 调用中，参数 dest 指定了用来保存解析结果的属性名称。
    metavar 参数用来产生帮助信息。
    action 指定了与参数处理相关的行为，通常用 store 表示存储单个值，用 append 来表示将多个值保存到一个列表中。
    """
    import argparse
    parser = argparse.ArgumentParser(description='Search some files')
    parser.add_argument(dest='filenames', metavar='filename', nargs='*')
    parser.add_argument('-p', '--pat', metavar='pattern', required=True,
                        dest='patterns', action='append',
                        help='text pattern to search for')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose mode')
    parser.add_argument('-o', dest='outfile', action='store',
                        help='output file')
    parser.add_argument('--speed', dest='speed', action='store',
                        choices={'slow', 'fast'}, default='slow',
                        help='search speed')
    args = parser.parse_args()
    print(args.filenames)
    print(args.patterns)
    print(args.verbose)
    print(args.outfile)
    print(args.speed)
    """
    $ python 13_utilityScriptingAndSystemAdministration.py -h
    $ python 13_utilityScriptingAndSystemAdministration.py -v -p spam --pat eggs /etc/passwd
    """


def func4():
    """
    运行时提供密码输入提示

    getpass
    """
    import getpass
    # 取用户 shell 环境当前的用户名登录。
    user = getpass.getuser()
    # 如果需要输入用户名
    input_user = input('Enter your username:')
    # 有些系统上可能不支持将输入给 getpass() 方法的密码做隐藏处理，这种情况下，Python 会发出预警信息。
    passwd = getpass.getpass()

    print(user, input_user, passwd)


def func5():
    """
    获取终端大小

    os.get_terminal_size()
    """
    import os
    # 在非终端环境中可能报错
    print(os.get_terminal_size())


def func6():
    """
    执行外部命令并获取输出

    执行一个外部命令并获取输出，最简单的方法就是使用 subprocess.check_output() 函数。
    如果需要跟一个子进程执行更加高级的通信，例如为其发送输入，那就需要采取不同的方法，可以使用 subprocess.Popen 类。
    """
    import subprocess

    def simple_example():
        out_bytes = subprocess.check_output(['ls', '-l'])
        print(out_bytes)
        out_text = out_bytes.decode('utf-8')
        print(out_text)
    print('=' * 20, 'simple_example', '=' * 20)
    simple_example()

    def senior_example():
        try:
            # 同时获取标准输出和标准错误输出，设置超时时间
            out_bytes = subprocess.check_output(['ls', '-l'], stderr=subprocess.STDOUT, timeout=1)
            print(out_bytes.decode('utf-8'))
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            out_bytes = e.output
            code = e.returncode
            print(out_bytes, code)
    print('=' * 20, 'senior_example', '=' * 20)
    senior_example()

    def popen_example():
        text = b'''
        hello world
        this is a test
        goodbye
        '''
        # wc 命令，用来计算字节数
        p = subprocess.Popen(['wc'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        stdout, stderr = p.communicate(text)

        print(stdout.decode('utf-8') if stdout else "", stderr.decode('utf-8') if stderr else "")
    print('=' * 20, 'popen_example', '=' * 20)
    popen_example()


def func7():
    """
    拷贝或移动文件和目录

    大部分情况下用 shutil 来拷贝文件和目录是非常直接的。
    但需要注意：当考虑到文件的元数据时，类似 copy2() 这样的函数只会尽可能保存这类数据。
    一些基本信息，例如访问时间、创建时间以及权限信息会得到保存。
    但是属主、访问控制列表、资源派生(resource forks)以及其他扩展的文件元数据可能得不到保存。
    这取决于操作系统底层和用户自身的访问权限。

    处理文件名时，应该使用 os.path 中的函数，这样可以获得最佳的可移植性。

    使用 copytree() 拷贝目录时，错误处理是比较棘手的。可以将遇到的异常都收集到一个列表中并将其归组为一个单独的异常。
    """
    import shutil
    import os

    # Copy src to dst. (cp src dst)
    shutil.copy('./__pycache__/test.txt', './__pycache__/test.bak')
    # Copy files, but preserve metadata (cp -p src dst)
    shutil.copy2('./__pycache__/test.txt', './__pycache__/test.bak')
    # Copy directory tree (cp -R src dst)
    os.rmdir('__pycache__/test_bak')
    shutil.copytree('__pycache__/test', '__pycache__/test_bak')
    # Move src to dst (mv src dst)
    shutil.move('__pycache__/test.bak', '__pycache__/test.txt')
    os.rmdir('__pycache__/test_bak')
    shutil.copytree('__pycache__/test', '__pycache__/test_bak', symlinks=True)

    def ignore_pyc_files(dirname, filenames):
        return [name for name in filenames if name.endswith('.pyc')]
    os.rmdir('__pycache__/test_bak')
    shutil.copytree('__pycache__/test', '__pycache__/test_bak', ignore=ignore_pyc_files)
    os.rmdir('__pycache__/test_bak')
    shutil.copytree('__pycache__/test', '__pycache__/test_bak', ignore=shutil.ignore_patterns('*~', '*.pyc'))
    try:
        os.rmdir('__pycache__/test_bak')
        shutil.copytree('__pycache__/test', '__pycache__/test_bak')
    except shutil.Error as e:
        for src, dst, msg in e.args[0]:
            # src is source name
            # dst is destination name
            # msg is error message from exception
            print(dst, src, msg)


def func8():
    """
    创建和解包归档文件

    shutil
    Python 中有很多模块可用来处理各种归档格式的底层细节。
    但是，如果只是创建和解包归档文件，没必要使用底层模块，可直接使用 shutil 模块中的高层函数。
    """
    import shutil
    shutil.unpack_archive('__pycache__/test.zip')
    new_file_name = shutil.make_archive('__pycache__/test', 'zip', '__pycache__/test')
    print(new_file_name)


def func9():
    """
    通过名称来查找文件

    搜索文件可使用 os.walk() 函数，只要将顶层目录提供给它即可。
    os.walk() 有跨平台和已扩展的优点。

    os.walk() 方法会为我们遍历目录层级，且对于进入的每个目录它都会返回一个3元组。
    包含了正在检视的目录的相对路径、该目录中包含的所有目录名的列表、以及该目录中包含的所有文件名的列表。

    对于每个元组，只需要检查目标文件是否在 file 列表中即可。
    如果是就使用 os.path.join() 合并路径。为了避免奇怪的路径名比如 ././foo//bar，使用了另外两个函数来修正结果。
    第一个是 os.path.abspath(),它接受一个路径，可能是相对路径，最后返回绝对路径。
    第二个是 os.path.normpath()，用来返回正常路径，可以解决双斜杆、对目录的多重引用的问题等。
    """
    import os

    def find_file(start, name):
        for real_path, dirs, files in os.walk(start):
            if name in files:
                full_path = os.path.join(start, real_path, name)
                print(os.path.normpath(os.path.abspath(full_path)))

    find_file('__pycache__', 'test.txt')


def func10():
    """
    读取配置文件

    可以使用 configparser 模块来读取 .ini 模式的配置文件

    .ini 配置文件和使用 Python 编写的同样目的的源文件之间有以下显著区别：
    1. .ini 的语法更加宽容和"草率"。例如："=" 和 ":" 均可用来赋值。
    2. .ini 文件中用到的名称是大小写不敏感的。
    3. .ini 文件解析值的时候，像 getboolean() 这样的方法会检查任何合理的值。
    4. .ini 文件不是按照从上到下的方式执行的，配置文件会全部读取，之后执行。

    ConfigParser 可以分别读取多个配置文件并将它们合并成一个单独的配置。

    Python 并不能对其他程序中使用的 .ini 文件的全部特性提供支持。
    """
    from configparser import ConfigParser
    cfg = ConfigParser()
    cfg.read('__pycache__/config.ini')
    print(cfg.sections())
    print(cfg.get('installation', 'library'))
    print(cfg.getboolean('debug', 'log_errors'))
    print(cfg.getboolean('debug', 'log_errors'))
    print(cfg.getint('server', 'nworkers'))
    print(cfg.get('server', 'signature'))
    """
    如果需要，也可以使用 cfg.write() 方法修改配置并写回到配置文件中。
    """
    cfg.set('server', 'port', '10000')


def func11():
    """
    给脚本添加日志记录

    最简单的方法就是使用 logging 模块。
    logging 调用( critical(), error(), warning(), info(), debug() )分别代表不同的严重级别，以降序排列。
    basicConfig() 的 level 参数是一个过滤器，所有等级低于此设定的消息都会被忽略掉。
    每个日志操作的参数都是一条字符串消息，后边跟着零或多个参数。当产生日志消息时，%操作符使用提供的参数来格式化字符串消息。

    logging 模块的配置非常强大且复杂，不需要详细了解。任何 logging 调用前应先调用 basicConfig()。
    如果想让日志消息发送到标准错误输出，不给 basicConfig() 提供任何文件名做参数即可。

    关于 basicConfig()，一个微妙的地方在于它只能在程序中调用一次。如果稍后需要修改日志模块的配置，需要取得根日志对象(root logger)并直接对其修改。
    """
    import logging

    logging.basicConfig(
        # filename='__pycache__/test.log', # filename 参数可以指定日志文件
        level=logging.ERROR,
        format='%(levelname)s:%(asctime)s:%(message)s'
    )

    hostname = 'www.python.org'
    item = 'spam'
    filename = 'data.csv'
    mode = 'r'

    logging.critical('Host %s unknown', hostname)
    logging.error("Couldn't find %r", item)
    logging.warning('Feature is deprecated')
    logging.info('Opening file %r, mode=%r', filename, mode)
    logging.debug('Got here')


def func12():
    """
    给库添加日志记录

    库给日志带来了一个特殊的问题，即，使用日志的环境是未知的。一般来说不应该在库代码中尝试去自行配置日志系统，或者对已有的日志配置做任何假设。因此，需要提供隔离措施。

    getLogger(__name__)创建了一个日志模块，其名称同调用它的模块名相同。由于所有的模块都是唯一的，这么做就创建了一个专用的日志对象，也就与其他的日志对象隔离开来。

    log.addHandler(logging.NullHandler()) 操作绑定了一个空的处理例程到刚刚创建的日志对象上。默认情况下，空处理例程会忽略所有的日志消息。
    因此，如果用到了这个库且日志系统从未配置过，那么就不会出现任何日志消息或警告信息。
    """
    # somelib.py
    import logging

    log = logging.getLogger(__name__)
    log.addHandler(logging.NullHandler)

    def func():
        log.critical('A Critical Error!')
        log.debug('A debug message')

    # 有了这样的配置，默认情况下将不会产生任何日志输出
    # 但如果日志系统得到适当的配置，日志消息开始出现。
    """
    >>> import somelib
    >>> somelib.func()
    >>> import logging
    >>> logging.basicConfig()
    >>> logging.getLogger('somelib').level=logging.DEBUG
    """


def func13():
    """
    创建一个秒表计时器

    time 模块包含了各种与计时相关的函数。
    也可以基于这些函数构建更高层的接口来模拟秒表。这个接口如果支持上下文管理协议，就更方便了。

    在进行计时测量时需要考虑底层所用到的时间函数。
    一般来说，像 time.time() 和 time.clock() 的计时精度根据操作系统的不同而有所区别。
    time.perf_counter() 函数总是会使用系统中精度最高的计时器。
    """
    import time

    class Timer:
        def __init__(self, func=time.perf_counter):
            self.elapsed = 0.0
            self._func = func
            self._start = None

        def start(self):
            if self._start is not None:
                raise RuntimeError('Already started')
            self._start = self._func()

        def stop(self):
            if self._start is None:
                raise RuntimeError('Not started')
            end = self._func()
            self.elapsed += end - self._start
            self._start = None

        def reset(self):
            self.elapsed = 0.0

        @property
        def running(self):
            return self._start is not None

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, *args):
            self.stop()

    def countdown(n):
        while n > 0:
            n -= 1
    t = Timer(time.process_time)
    with t:
        countdown(1000000)
    print(t.elapsed)


def func14():
    """
    给内存和 CPU 使用量设定限制

    想对运行在 UNIX 系统上的程序在内存和 CPU 的使用量上设定一些限制，resource 模块可以用来执行这样的任务。

    可通过 resource.setrlimit() 函数来为特定的资源设定软性和硬性的限制。
    软性限制就是一个值，一般来说操作系统会通过信号机制来限制或通知进程。
    硬性限制代表着软性限制值的上限。
    setrlimit() 函数还可以用来设定子进程数量、可打开的文件数量等系统资源。

    注意：resource.setrlimit() 只能在部分 UNIX 操作系统(Linux)上使用，OS X 中不行。
    """
    import signal
    import resource

    def time_exceeded(signo, frame):
        print("Time's up!")
        raise SystemExit(1)

    def set_max_runtime(seconds):
        """
        限制最长运行时间
        """
        soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
        resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
        signal.signal(signal.SIGXCPU, time_exceeded)

    set_max_runtime(15)
    while True:
        pass

    def limit_memory(maxsize):
        """
        限制内存使用量
        """
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))


def func15():
    """
    加载 Web 浏览器

    webbrowser 模块可用来以独立于平台的方式加载浏览器。
    如果想指定浏览器，可以使用 webbrowser.get() 函数来指定。
    """
    import webbrowser
    webbrowser.open('https://www.baidu.com/')
    c = webbrowser.get('safari')
    c.open('https://www.baidu.com/')


if __name__ == '__main__':
    doFunc()