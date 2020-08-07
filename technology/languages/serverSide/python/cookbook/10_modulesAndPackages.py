#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc

"""
本章介绍一些技巧使项目代码结构变得整洁、有逻辑感。项目刚开始时不会觉得有用，一段时间后就能体现出价值
模块和包是任何大型项目的核心，就连Python安装程序本身也是一个包
"""


def func1():
    """
    把模块按层次结构组成包

    定义一个具有层次结构的模块就像在文件系统上创建目录结构一样简单。__init__.py文件的目的就是包含可选的初始化代码，当遇到软件包中不同层次的模块时会触发运行
    如果写下import graphics语句，文件graphics/__init__.py会被导入并形成graphics命名空间中的内容
    对于import graphics.formats.jpg这样的导入语句，文件graphics/__init__.py和graphics/formats/__init__.py都会在最终导入文件graphics/formats/jpg.py之前优先得到导入

    大部分情况下，把__init__.py文件留空也是可以的。但是，在某些特定的情况下__init__.py文件中是需要包含代码的，例如，可以用__init__.py文件来自动加载子模块
    # graphics/formats/__init__.py
    from . import jpg
    from . import png
    有了这样一个文件，用户只需要使用一条单独的import graphics.formats语句就可以导入jpg和png模块了，不需要再去分别导入
    个人感觉这样自动导入，使用者或者代码阅读者会比较晕，尽量少用

    Python3.3开始就算不存在__init__.py文件似乎也可以执行包的导入操作。如果不定义__init__.py，那么实际上创建一个称之为"命名空间包(namespace package)的东西"
    """


def func2():
    """
    对所有符号的导入进行精确控制

    在模块中定义一个__all__变量，可用来显式列出可导出的符号名

    # some_module.py
    def spam():
        pass
    def grok():
        pass
    blah = 42
    __all__ = ['spam', 'grok']

    尽管强烈反对使用from module import * 这样的导入语句，但是在定义了大量符号的模块中还是能常看到这种用法。如果对此无动于衷的话，这种形式的导入会把所有不以下划线开头的符号名全部导出。
    如果定义了__all__，那么显式列出符号名才会被导出；如果__all__中包含为定义的名称，那么在执行import语句时会产生一个AttributeError异常

    个人看法：如果模块非常关键，那么最好定义__all__来帮助那些使用import * 的人。
    真正的强者，愿意以弱者的自由为边界
    """


def func3():
    """
    用相对名称来导入包中的子模块

    在包的内部，要在其中一个子模块中导入同一个包中其他的子模块，既可以通过给出完整的绝对名称，也可以通过相对名称完成导入
    使用绝对名称的缺点在于这么做会将最顶层的包名称硬编码到源代码中，这使得代码更加脆弱，如果想重新组织目录结构会比较困难

    import语句中的 . 和 .. 语法看起来比较有趣，把它们想象成指定目录名即可。意味着在当前目录中查找，而 ..B 表示在 ../B 目录中查找。这种语法只能在 from xx import yy 这样的导入语句中使用

    尽管看起来似乎可以利用相对导入来访问整个文件系统，但实际上是不允许跳出定义包的那个目录的。也就是说，利用句点的组合形式进入一个不是Python包的目录会使得导入出现错误

    相对导入只有在特定情况下才起作用，即，模块必须位于一个合适的包中。
    注意，位于脚本顶层目录的模块不能使用相对导入，
    此外，如果包的某个部分是以脚本的形式执行的，也不能使用相对导入，可使用 -m 选项来执行，例如 python -m pip install ...

    个人看法：能用相对用相对，用不了再考虑绝对
    """


def func4():
    """
    将模块分解成多个文件

    个人看法：将一个模块分解成多个文件是十分舒爽的事，但也要明白过犹不及

    是否进行模块分解主要取决于一个设计上的问题，即，我们希望用户使用大量的小型模块，还是希望他们只使用一个单独的模块
    通过将模块转换为包的方式将模块分解成多个单独文件

    # 单文件模块
    # my_module.py
    class A:
        def spam(self):
            print('A.spam')

    class B(A):
        def bar(self):
            print('B.bar')

    # 拆分为两个文件
    my_module/
        __init__./py
        a.py
        b.py

    # a.py
    class A:
        def spam(self):
            print('A.spam')

    # b.py
    from .a import A

    class B(A):
        def bar(self):
            print('B.bar')

    # __init__.py

    from .a import A
    from .b import B

    在逻辑上把多个文件拼接成一个单独的命名空间的技术，关键之处在于创建一个包目录，并通过__init__.py文件将各个部分粘合在一起
    当分解模块时，需要对跨文件名的引用多加小心

    可以对本节提到的技术进行扩展，引入"惰性"导入的概念，只希望在实际需要的时候才加载那些组件。为了实现这个目的，可对__init__.py文件做些修改
    # __init__.py

    def A():
        from .a import A
        return A()

    def B():
        from .b import B
        return B()

    惰性加载的主要缺点在于会破坏继承和类型检查机制
    """


def func5():
    """
    让各个目录下的代码在统一的命名空间下导入

    我们想定义一个顶层的Python包，把它作为命名空间来管理大量单独维护的子模块。这个问题常常会在大型的应用程序框架中出现，框架开发人员希望鼓励用户发布自己的插件或者附加包
    要使各个单独的目录统一在一个公共的命名空间下，可以把代码像普通的Python包那样组织。但对于打算合并在一起的组件，这些目录中的__init__.py文件则需要忽略

    foo-package/
        spam/
            blah.py

    bar-package/
        spam/
            grok.py

    在这两个目录中，spam用来作为公共的命名空间。注意这两个目录中都没有出现__init__.py文件
    如果将 foo-package 和 bar-package 都添加到 Python 的模块查询路径中，然后尝试做一些导入操作
    import sys
    sys.path.extend(['foo-package', 'bar-package'])
    import spam.blah
    import spam.grok
    这两个不同的包目录魔法般地合并在了一起，我们可以随意导入spam.blah或者spam.grok

    这里的工作原理用到了一种称之为"命名空间包(namespace package)的特性。
    命名空间包是一种特殊的包，设计这种特性的意图就是用来合并不同目录下的代码，把它们放在统一的命名空间下管理。
    这样就允许把框架的某些部分分解成单独安装的包，也使制作第三方插件和针对框架的其他扩展的成本降低

    创建命名空间包的关键之处在于确保在统一命名空间的顶层目录中不包含__init__.py文件，当导入包的时候，这个缺失的__init__.py文件会导致发生一个有趣的事情
    解释器并不会因此而产生一个错误，相反，解释器开始创建一个列表，把所有恰好包含有这个包名的目录都囊括在内。
    此时就创建出一个特殊的命名空间包模块，且在__path__变量中会保存一份只读形式的目录列表

    命名空间包的一个重要特性就是任何人都可以用自己的代码来扩展命名空间中的内容

    想知道某个包是不是用来当作命名空间包的主要方式是检查它的__file__属性，如果缺少这个属性，就是命名空间包
    也可以从对包对象的字符串表示中看出来，如果是命名空间的话，其中会有"namespace"的字样
    """


def func6():
    """
    重新加载模块
    在开发和调试阶段，重新加载模块常常很有用。但是一般来说在生产环境这么做是不安全的，因为它并不会总是按照期望的方式工作
    reload()操作会擦除模块底层字典(__dict__)的内容，并通过重新执行模块的源代码来刷新它。模块本身的标识并不会改变。因此，这个操作会使得已经导入到程序中的模块得到更新
    对于使用 from module import name 这样的语句导入的定义，reload() 是不会更新的
    """
    import time
    import importlib

    importlib.reload(time)


def func7():
    """
    让目录或zip文件成为可运行的脚本
    如果应用程序已经进化为由多个文件组成的"庞然大物"，可以把它们放在专属的目录中，并为之添加一个__main__.py文件
    如果有__main__.py，就可以在顶层目录中运行Python解释器，解释器会把__main__.py作为主程序来执行
    这项技术在我们把所有代码打包进一个zip文件中时同样有效

    创建一个目录或zip文件，并为其添加一个__main__.py，这是一种打包规模较大的Python应用程序的可行方法。
    但这和安装到Python标准库中的包有所不同，在这种情况下，代码并不是作为标准库中的模块来使用。相反，这里只是把代码打包起来方便给其他人执行
    """


def func8():
    """
    读取包中的数据文件

    import pkgutil
    data = pkgutil.get_data(package, resource)

    pkgutil.get_data()函数是一种高级工具，无论包以什么样的形式安装或安装到哪里，都能够用它来获取数据文件。它能共完成工作并把文件内容以字节串的形式返回给我们
    也可编写代码利用内建的I/O函数进行数据读取，但对比pkgutil，I/O函数有以下缺点
    1. 对于包来说，他无法控制解释器的当前工作目录，因此，任何I/O操作都必须使用文件名的绝对路径
    2. 包通常会安装为.zip或者.egg文件，它们与文件系统中普通的目录保存文件的方式不同，因此无法用open()这样的I/O函数读取数据文件
    """


def func9():
    """
    添加目录到sys.path中

    有两种常见的方法可以将新的目录添加到sys.path中去
    1. 使用PYTHONPATH环境变量添加
    env PYTHONPATH=/some/dir:/other/dir python3
    2. 创建一个.pth文件，然后将目录列出来。这个文件需要放在Python的其中一个site-packages目录中
    #my_application.pth
    /some/dir
    /other/dir

    如果在确定文件的位置时遇到了麻烦，可能会倾向于编写代码来手动调整 sys.path 值
    import sys
    sys.path.insert(0, '/some/dir')
    尽管这可以"工作"，但在实践中这种做法极度脆弱，应该尽可能避免。
    这种方法的问题主要在于将目录名称硬编码到了源码中。如果要将代码转移到一个新的位置时，就会产生维护方面的问题。通常更好的方法是在其他的地方对路径做配置，不用去直接编辑代码。
    有时候，如果利用模块级的变量，比如__file__来精心构建一个合适的绝对路径，也能够规避硬编码目录所带来的问题。

    目录site-packages通常是第三方模块的包安装的位置，目前常见的做法是使用包管理软件管理包，现在最火的是PyPI。
    """


def func10():
    """
    使用字符串中给定的名称来导入模块

    当模块或者包的名称以字符串的形式给出时，可以使用 importlib.import_module() 函数来手动导入这个模块。
    import_module 基本上和 import 完成的步骤相同，但是 import_module 会把模块对象作为结果返回给你。
    我们只需要将它保存在一个变量里，之后把它当做普通的模块使用即可。

    如果要同包打交道，import_module()也可以用来实现相对导入。但是，需要提供一个额外的参数。

    采用 import_module()手动导入模块的需求最常出现在当编写代码以某种方式来操作成包装模块时
    内建的__import__()函数也能实现类似需求，但import.import_module()更容易使用一些
    """
    import importlib

    # same as 'import math as math1'
    math1 = importlib.import_module('math')
    print(math1.sin(2))

    # same as 'from . import doFunc'
    b = importlib.import_module('doFunc', '.')


def func11():
    """
    利用import钩子从远端机器上加载模块
    本节内容适合深入理解import语句的工作原理，不要实际应用
    业务需求: 已知url，加载远程模块

    Python的模块、包和导入机制是整个语言中最为复杂的部分之一。如果想要深入了解，可以阅读importlib模块和PEP 302的文档

    本节要点:
        1. 如果想创建一个新的模块对象(module object)，可以使用types.MethodType()函数。模块对象通常会有几个常用的属性，包括 __file__ (所加载模块的源文件名)和 __package__ (包的名称，如果有的话)。
        2. 模块会被解释器做缓存处理，以避免重复导入。模块缓存可以在字典 sys.modules 中找到。由于存在缓存处理，通常我们会把缓存和模块创建联合成一个的步骤来做。

    创建模块很简单，可以直接编写简单的函数处理。这种方法的缺点在于处理复杂情况(例如处理包)会相当棘手。需要重新实现大部分的底层逻辑，而这些逻辑是普通的import语句实现过的，所以最好直接扩展import语句的功能，而不是定义自己的处理函数。

    扩展import可以很很直接，但涉及到一些组件。
    从高层来看，import操作需要处理一系列"元路径"查询器，这些查询器可以在sys.meta_path中找到，当执行一条import语句时，解释器会遍历sys.meta_path中的查询器对象，并调用它们的find_module()方法来找到合适的模块加载器
    在find_module()方法中，参数path用来处理包。当导入的是包时，参数path表示包的__path__属性中列出来的子目录。需要检查这些路径来找出包中的子模块。

    基于路径的import钩子是更深入的扩展，思想相似，机制不同。
    sys.path是一个路径列表，其中保存的是Python查询模块的路径。sys.path中的每一个条目都会同一个查询器对象关联起来。
    当执行import语句时，sys.path中的目录会按顺序逐个接受检查。对于每个目录，import的模块的名称会被传递给sys.path_import_cache（记录所有已知的代码中被加载的目录的查询器）中与目录相关联的查询器。也可创建查询器，并手动添加到sys.path_import_cache中
    利用sys.path的处理机制，可以安装一个自定义的路径检查函数来检查特定的文件名模式，比如URL。
    hooks方案的核心工作原理：在sys.path_hooks中安装一个用来寻找URL的自定义路径检查函数。当遇到自定义检查函数时，会产生一个新的UrlPathFinder实例并将其安装到sys.path_importer_cache中。
    从此之后，对于所有的导入语句，只要在遍历sys.path的过程中遇到这个部分，就会尝试使用自定义的查询器了。
    find_loader()需要针对普通包、目录列表、命名空间包做出不同的处理。

    利用sys.meta_path安装的导入器可以自由地以任何希望的方式处理模块
    基于路径的钩子方法则同sys.path的处理联系得更紧密，更接近普通的import操作
    """

    """
    简单方法: 创建显式的加载函数
    
    对于简单模块这么做是可行的。
    但是，这个功能并没有嵌入到常用的import语句中。
    而且要支持更加高级的组件，例如包，就需要扩展代码。
    """
    def load_module(url):
        import types
        import urllib.request
        import sys
        # 下载源码
        u = urllib.request.urlopen(url)
        source = u.read().decode('utf-8')
        # 利用compile将其编译为code对象
        code = compile(source, url, 'exec')
        # 在新创建的模块对象的字典中执行它
        mod = sys.modules.setdefault(url, types.MethodType(url))
        mod.__file__ = url
        mod.__package__ = ''
        exec(code, mod.__dict__)
        return mod

    """
    高级方法: 创建一个自定义的导入器(importer)
    """
    
    """
    方案1: 创建一个称之为元路径导入器(meta path importer)的组件
    
    把一个特殊对象————UrlMetaFinder的实例安装到sys.meta_path的最后一个条目中。
    每当要导入模块时就会在sys.meta_path中查找对应的查询对象，以此来寻找模块。
    如果所有正常位置上都找不到所需的模块，此时UrlMetaFinder实例就成类最后的救命稻草，会触发它来寻找所需的模块。
    
    UrlMetaFinder类对用户指定的URL进行包装。
    在内部，查询器会通过给定的URL构建一组合法的链接。
    当出现导入动作时，用模块名来同已知的链接进行对比。如果有匹配，此时就用UrlModuleLoader类来从远端机器上加载模块的源代码并创建出最终的模块对象作为结果。
    缓存链接的主要原因是避免重复导入产生的不必要的网络请求。
    """
    import sys
    import types
    import importlib.abc
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError
    from html.parser import HTMLParser

    # Debugging
    import logging
    log = logging.getLogger(__name__)

    # Get links from a given URL
    def _get_links(url):
        class LinkParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'a':
                    attrs = dict(attrs)
                    links.add(attrs.get('href').rstrip('/'))

        links = set()
        try:
            log.debug('Getting links from %s' % url)
            u = urlopen(url)
            parser = LinkParser()
            parser.feed(u.read().decode('utf-8'))
        except Exception as e:
            log.debug('Could not get links. %s', e)
        log.debug('links: %r', links)
        return links

    class UrlMetaFinder(importlib.abc.MetaPathFinder):
        def __init__(self, base_url):
            self._base_url = base_url
            self._links = {}
            self._loaders = {base_url: UrlModuleLoader(base_url)}

        def find_module(self, fullname, path=None):
            log.debug('find_module: fullname=%r, path=%r', fullname, path)
            if path is None:
                base_url = self._base_url
            else:
                if not path[0].startswith(self._base_url):
                    return None
                base_url = path[0]
            parts = fullname.split('.')
            basename = parts[-1]
            log.debug('find_module: base_url=%r, basename=%r', base_url, basename)

            # Check link cache
            if basename not in self._links:
                self._links[base_url] = _get_links(base_url)

            # Check if it's a package
            if basename in self._links[base_url]:
                log.debug('find_module: trying package %r', fullname)
                full_url = self.base_url + '/' + basename
                # Attempt to load the package (which accesses __init__.py)
                loader = UrlPackageLoader(full_url)
                try:
                    loader.load_module(fullname)
                    self._links[full_url] = _get_links(full_url)
                    self._loaders[full_url] = UrlModuleLoader(full_url)
                    log.debug('find_module: package %r loaded', fullname)
                except ImportError as e:
                    log.debug('find_module: package failed. %s', e)
                    loader = None
                return loader
            # A normal module
            filename = basename + '.py'
            if filename in self._links[base_url]:
                log.debug('find_module: module %r found', fullname)
                return self._loaders[base_url]
            else:
                log.debug('find_module: module %r not found', fullname)
                return None

        def invalidate_caches(self):
            log.debug('invalidating link cache')
            self._links.clear()

    # Module Loader for a URL
    class UrlModuleLoader(importlib.abc.SourceLoader):
        def __init__(self, base_url):
            self._base_url = base_url
            self._source_cache = {}

        def module_repr(self, module):
            return '<urlmodule %r from %r>' % (module.__name__, module.__file__)

        # Required method
        def load_module(self, fullname):
            code = self.get_code(fullname)
            mod = sys.modules.setdefault(fullname, types.MethodType(fullname))
            mod.__file__ = self.get_filename(fullname)
            mod.__loader__ = self
            mod.__package__ = fullname.rpartition('.')[0]
            exec(code, mod.__dict__)
            return mod

        # Optional extensions
        def get_code(self, fullname):
            src = self.get_source(fullname)
            return compile(src, self.get_filename(fullname), 'exec')

        def get_data(self, path):
            pass

        def get_filename(self, fullname):
            return self._base_url + '/' + fullname.split('.')[-1] + '.py'

        def get_source(self, fullname):
            filename = self.get_filename(fullname)
            log.debug('loader: reading %r', filename)
            if filename in self._source_cache:
                log.debug('loader: cached %r', filename)
                return self._source_cache[filename]
            try:
                u = urlopen(filename)
                source = u.read().decode('utf-8')
                log.debug('loader: %r loaded', filename)
                self._source_cache[filename] = source
                return source
            except (HTTPError, URLError) as e:
                log.debug('loader: %r failed. %s', filename, e)
                raise ImportError("Can't load %s" % filename)

        def is_package(self, fullname):
            return False

    # Package loader for a URL
    class UrlPackageLoader(UrlModuleLoader):
        def load_module(self, fullname):
            mod = super().load_module(fullname)
            mod.__path__ = [self._base_url]
            mod.__package__ = fullname

        def get_filename(self, fullname):
            return self._base_url + '/' + '__init__.py'

        def is_package(self, fullname):
            return True

    # Utility functions for installing/uninstalling the loader
    _installed_meta_cache = {}

    def install_meta(address):
        if address not in _installed_meta_cache:
            finder = UrlMetaFinder(address)
            _installed_meta_cache[address] = finder
            sys.meta_path.append(finder)
            log.debug('%r installed on sys.meta_path', finder)

    def remove_meta(address):
        if address in _installed_meta_cache:
            finder = _installed_meta_cache.pop(address)
            sys.meta_path.remove(finder)
            log.debug('%r removed from sys.meta_path', finder)

    """
    方案2: 编写一个钩子(hook)，直接将其插入到sys.path变量中，用来识别特定的目录命名格式
    
    关键在于handle_url()函数，我们将它添加到了sys.path_hooks中。
    当开始处理sys.path中的条目时，位于sys.path_hooks中的函数就会被调用。
    如果这些函数有任何一个返回一个查询对象(finder object)，就用这个查询对象来尝试为sys.path中的条目加载模块。
    
    要使用这个基于路径的查询器，只需要将URL添加到sys.path中
    """

    class UrlPathFinder(importlib.abc.PathEntryFinder):
        def __init__(self, base_url):
            self._links = None
            self._loader = UrlModuleLoader(base_url)
            self._base_url = base_url

        def find_loader(self, fullname):
            log.debug('find_loader: %r', fullname)
            parts = fullname.split('.')
            basename = parts[-1]
            # Check link cache
            if self._links is None:
                self._links = []  # See discussion
                self._links = _get_links(self._base_url)

            # Check if it's a package
            if basename in self._links:
                log.debug('find_loader: trying package %r', fullname)
                full_url = self._base_url + '/' + basename
                # Attempt to load the package (which accesses __init__.py)
                loader = UrlPackageLoader(full_url)
                try:
                    loader.load_module(fullname)
                    log.debug('find_loader: package %r loaded', fullname)
                except ImportError as e:
                    log.debug('find_loader: %r is a namespace package', fullname)
                    loader = None
                return loader, [full_url]

            # A normal module
            filename = basename + '.py'
            if filename in self._links:
                log.debug('find_loader: module %r found', fullname)
                return self._loader, []
            else:
                log.debug('find_loader: module %r not found', fullname)
                return None, []

        def invalidate_caches(self):
            log.debug('invalidating link cache')
            self._links = None

    # Check path to see if it looks like a URL
    _url_path_cache = {}

    def handle_url(path):
        if path.startswith(('http://', 'https://')):
            log.debug('Handle path? %s. [Yes]', path)
            if path in _url_path_cache:
                finder = _url_path_cache[path]
            else:
                finder = UrlPathFinder(path)
                _url_path_cache[path] = finder
            return finder
        else:
            log.debug('Handle path? %s. [No]', path)

    def install_path_hook():
        sys.path_hooks.append(handle_url)
        sys.path_importer_cache.clear()
        log.debug('Installing handle_url')

    def remove_path_hook():
        sys.path_hooks.remove(handle_url)
        sys.path_importer_cache.clear()
        log.debug('Removing handle_url')


def func12():
    """
    在模块加载时为其打补丁

    定义一个能在打补丁同时将实际的导入委托给sys.meta_path中其它查询器的方法/类，并将其添加到sys.meta_path的首元素位置
    递归调用imp.import_module()来完成导入委托，注意避免无限递归
    """
    import importlib
    import sys
    from collections import defaultdict

    _post_import_hooks = defaultdict(list)

    class PostImportFinder:
        def __init__(self):
            self._skip = set()

        def find_module(self, fullname, path=None):
            if fullname in self._skip:
                return None
            self._skip.add(fullname)
            return PostImportLoader(self)

    class PostImportLoader:
        def __init__(self, finder):
            self._finder = finder

        def load_module(self, fullname):
            importlib.import_module(fullname)
            module = sys.modules[fullname]
            for func in _post_import_hooks[fullname]:
                func(module)
            self._finder._skip.remove(fullname)
            return module

    def when_imported(fullname):
        def decorate(func):
            if fullname in sys.modules:
                func(sys.modules[fullname])
            else:
                _post_import_hooks[fullname].append(func)
            return func
        return decorate

    sys.meta_path.insert(0, PostImportFinder())

    from functools import wraps

    def logged(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Calling', func.__name__, args, kwargs)
            return func(*args, **kwargs)
        return wrapper

    # Example
    @when_imported('math')
    def add_logging(mod):
        mod.cos = logged(mod.cos)
        mod.sin = logged(mod.sin)


def func13():
    """
    安装只为自己所用的包

    python setup.py install -user

    pip install --user package_name
    """


def func14():
    """
    创建一个完全干净且不包含任何第三方插件的虚拟环境，然后从头管理插件，方便打包、部署

    通常创建虚拟环境是为了安装和管理第三方的包
    可以通过pyvenv命令创建一个新的"虚拟"环境。这个命令被安装到同Python解释器一样的目录中

    有了新的虚拟环境，下一步通常是安装一个包管理器，如PyPI

    尽管虚拟环境看起来像是Python安装的一份拷贝，但它实际上只是由几个文件和一些符号链接所组成。
    所有的标准库文件和解释器执行文件都来自于原来的Python安装包。
    因此，创建这样的环境非常简单方便，几乎不占用什么系统资源。

    默认情况下，虚拟环境是完全干净且不包含任何第三方插件的。
    如果想将已安装过的包引入，使其作为虚拟环境的一部分，那么可以使用选项--system-site-packages来创建虚拟环境
    """


def func15():
    """
    发布自定义的包

    1. 编写setup.py文件
    2. 创建MANIFEST.in文件，并在其中列出各种希望包含在包中的非源代码文件
    3. 确保setup.py和MANIFEST.in文件位于包的顶层目录
    4. 执行命令 python setup.pyu sdist
    对于纯Python代码来说，编写setup.py文件是很直接的，但要注意，我们必须手动列出包中的每一个子目录

    个人看法：发布时，兼容PyPI和Python标准的安装模式是现如今通用的做法
    """


if __name__ == '__main__':
    doFunc()
