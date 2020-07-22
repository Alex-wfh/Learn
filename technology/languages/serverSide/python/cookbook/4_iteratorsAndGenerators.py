#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc


def func1():
    """
    手动访问迭代器中的元素
    """
    l = iter(range(10))
    try:
        while True:
            ll = next(l)
            print(ll)
    except StopIteration:
        pass


def func2():
    """
    委托迭代
    """

    class Node:
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node({!r})'.format(self._value)

        def add_child(self, other_node):
            self._children.append(other_node)

        def __iter__(self):
            return iter(self._children)

    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)


def func3():
    """
    用生成器创建新的迭代模式
    函数只要出现yield语句就会将其转变成一个生成器，生成器只会在相应迭代操作时才运行，否则就是一个安静的迭代器
    """

    def frange(start, stop, increment):
        x = start
        while x < stop:
            yield x
            x += increment

    for n in frange(0, 4, 0.5):
        print(n)


def func4():
    """
    实现迭代协议
    第一份代码（生成器），生成器+递归很巧妙，注意yield from 的用法
    python的迭代协议要求__iter__()返回一个特殊的迭代器对象，该对象必须实现__next()__方法，并使用StopIteration异常来通知迭代的完成，见第二份代码（迭代器）
    迭代器版本和生成器版本工作方式相同，但实现却复杂很多，因为迭代器必须维护迭代过程中许多复杂的状态，没人喜欢这样的代码。把迭代器以生成器方式实现是好的选择
    """
    print('1.generators')

    class Node1:
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node1({!r})'.format(self._value)

        def add_child(self, other_node):
            self._children.append(other_node)

        def __iter__(self):
            return iter(self._children)

        def depth_first(self):
            yield self
            for c in self:
                yield from c.depth_first()

    root = Node1(0)
    child1 = Node1(1)
    child2 = Node1(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node1(3))
    child1.add_child(Node1(4))
    child2.add_child(Node1(5))
    for ch in root.depth_first():
        print(ch)
    print('=' * 40)
    print('2.iterators')

    class Node2():
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node2({!r})'.format(self._value)

        def add_child(self, other_node):
            self._children.append(other_node)

        def __iter__(self):
            return iter(self._children)

        def depth_first(self):
            return DepthFirstIterator(self)

    class DepthFirstIterator(object):
        def __init__(self, start_node):
            self._node = start_node
            self._children_iter = None
            self._child_iter = None

        def __iter__(self):
            return self

        def __next__(self):
            if self._children_iter is None:
                self._children_iter = iter(self._node)
                return self._node
            elif self._child_iter:
                try:
                    nextchild = next(self._child_iter)
                    return nextchild
                except StopIteration:
                    self._child_iter = None
                    return next(self)
            else:
                self._child_iter = next(self._children_iter).depth_first()
                return next(self)

    root = Node2(0)
    child1 = Node2(1)
    child2 = Node2(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node2(3))
    child1.add_child(Node2(4))
    child2.add_child(Node2(5))
    for ch in root.depth_first():
        print(ch)


def func5():
    """
    反向迭代(reversed())
    反向迭代只有在待处理对象拥有可确定的大小，或者对象实现来__reversed__()方法时才能奏效
    """
    print('固定长度')
    a = range(10)
    for x in reversed(a):
        print(x)
    print('=' * 40)
    print('定义__reversed()__方法')

    class CountDown:
        def __init__(self, start):
            self.start = start

        def __iter__(self):
            n = self.start
            while n > 0:
                yield n
                n -= 1

        def __reversed__(self):
            n = 1
            while n <= self.start:
                yield n
                n += 1

    print('正序下降')
    for x in CountDown(10):
        print(x)
    print('倒叙下降')
    for x in reversed(CountDown(10)):
        print(x)


def func6():
    """
    带有额外状态的生成器函数
    带状态=>考虑使用类
    """
    from collections import deque
    class linehistory:
        def __init__(self, lines, histlen=3):
            self.lines = lines
            self.history = deque(maxlen=histlen)

        def __iter__(self):
            for lineno, line in enumerate(self.lines, 1):
                self.history.append((lineno, line))
                yield line

        def clear(self):
            self.history.clear()

    l = linehistory(range(10))
    for i in l:
        for lineno, hline in l.history:
            print('{}:{}'.format(lineno, hline))
        print('=' * 40)


def func7():
    """
    对迭代器做切片操作
    要对迭代器和生成器做切片操作，itertools.islice()函数是完美的选择
    islice()产生的结果是一个迭代器，它可以产生出所需要的切片元素，但这是哦你给过访问并丢弃所有起始索引之前的元素来实现的
    islice()会消耗掉所提供迭代器中的数据，如需重复利用，请转list
    """
    import itertools
    l = iter(range(10))
    for x in itertools.islice(l, 5, 7):
        print(x)


def func8():
    """
    跳过可迭代对象中的前一部分元素，到第一个false为止
    """
    import itertools
    l = range(10)
    for x in itertools.dropwhile(lambda x: x < 3, l):
        print(x)


def func9():
    """
    迭代所有可能的组合或排列
    permutations: 考虑顺序，不可重复
    combinations: 不考虑顺序，不可重复
    combinations_with_replacement: 不考虑顺序，可重复
    """
    items = [1, 2, 3]
    from itertools import permutations, combinations, combinations_with_replacement
    print(list(permutations(items)))
    print(list(combinations(items, 2)))
    print(list(combinations_with_replacement(items, 2)))


def func10():
    """
    以索引-值对的形式迭代序列
    enumerate() 实用且常用
    """
    for idx, i in enumerate(['a', 'b', 'c']):
        print(idx, i)


def func11():
    """
    同时迭代多个序列
    """
    import itertools
    a = [1, 2, 3, 4, 5]
    b = [6, 7, 8, 9]
    print('zip')
    for x, y in zip(a, b):
        print(x, y)
    print('zip_longest')
    for x, y in itertools.zip_longest(a, b):
        print(x, y)
    print('zip_longest with fillvalue')
    for x, y in itertools.zip_longest(a, b, fillvalue=100):
        print(x, y)


def func12():
    """
    在不同容器中进行迭代
    相比于先拼接后迭代，chain()有如下优点：
        1.支持不同类型同时迭代
        2.高效(时间、空间均高效)
    """
    import itertools
    a = [1, 2, 3, 4]
    b = ['x', 'y', 'z']
    c = 'abc'
    for x in itertools.chain(a, b, c):
        print(x)


def func13():
    """
    创建处理数据的管道
    处理大量数据时，生成器函数实现的管道机制是很好的选择，有如下优点：
        1.避免空间复杂度过高
        2.如存在bug，可提前报漏
    """


def func14():
    """
    扁平化处理嵌套型的序列
    yield from 很优雅
    isinstance(x,Iterable)简单地检查元素是否可迭代
    """
    from collections import Iterable
    x = iter(iter(range(3)) for i in range(3))

    def iterx(x):
        for xx in x:
            if isinstance(xx, Iterable):
                yield from xx

    for i in iterx(x):
        print(i)


def func15():
    """
    合并多个有序序列，再对整个有序序列进行迭代
    heapq.merge()对所有提供的序列不会一次性读取，这意味着可利用它处理非常长的序列，而且开销非常小
    heapq.merge()要求所有输入的序列都是有序的
    """
    import heapq
    a = [1, 4, 7, 10]
    b = [2, 5, 6, 11]
    for c in heapq.merge(a, b):
        print(c)


def func16():
    """
    用迭代器取代while循环
    好处：代码密度高。对于需重复调用函数的情况效果比较好
    坏处：其他人容易看不懂
    """
    print('while')
    r = iter(range(10))
    while True:
        i = next(r)
        if i == 5:
            break
        print(i)
    print('迭代器代替while')
    r = iter(range(10))
    for i in iter(lambda: next(r), 5):
        print(i)


if __name__ == '__main__':
    doFunc()
