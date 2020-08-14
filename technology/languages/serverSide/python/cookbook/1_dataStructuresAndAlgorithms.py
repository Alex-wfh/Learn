#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from doFunc import doFunc


def func1():
    """
    多重赋值
    """
    a, *b, c = 1, 2, 3, 4, 5, 6
    print(a, b, c)


def func2():
    """
    队列
    """
    from collections import deque
    q = deque(maxlen=2)
    q.append(1)
    q.append(2)
    q.append(3)
    q.append(0)
    print(q)


def func3():
    """
    最大或最小的n个元素
    """
    import heapq
    nums = [1, 2, 4, 21, 6, 94, 3, -12, 5, -67, -45, -67]
    print(heapq.nlargest(3, nums))
    print(heapq.nsmallest(3, nums))
    prices = [{'name': 'a', 'price': 1.0},
              {'name': 'b', 'price': 2.0},
              {'name': 'c', 'price': 3.0},
              {'name': 'd', 'price': 2.1},
              {'name': 'e', 'price': 1.5}]
    print(heapq.nlargest(2, prices, key=lambda s: s['price']))

    print(heapq.heapify(nums))
    print(heapq.heappop(nums))
    print(heapq.heappop(nums))
    print(heapq.heappop(nums))


def func4():
    """
    优先级队列
    """
    import heapq

    class PriorityQueue:
        def __init__(self):
            self._queue = []
            self._index = 0

        def push(self, item, priority):
            heapq.heappush(self._queue, (-priority, self._index, item))
            self._index += 1

        def pop(self):
            return heapq.heappop(self._queue)[-1]

    class Item:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return 'Item({!r})'.format(self.name)

    q = PriorityQueue()
    q.push(Item('a'), 1)
    q.push(Item('b'), 5)
    q.push(Item('c'), 4)
    q.push(Item('d'), 1)
    print(q.pop())
    print(q.pop())
    print(q.pop())
    print(q.pop())

    _queue = []
    heapq.heappush(_queue, (2, 'a'))
    heapq.heappush(_queue, (5, 'b'))
    heapq.heappush(_queue, (1, 'c'))
    heapq.heappush(_queue, (3, 'd'))
    print(heapq.heappop(_queue))
    print(heapq.heappop(_queue))
    print(heapq.heappop(_queue))
    print(heapq.heappop(_queue))


def func5():
    """
    字典中将键映射到多个值上
    """
    from collections import defaultdict
    d = defaultdict(list)
    d['a'].append(1)
    d['b'].append(2)
    d['a'].append(3)
    print(d)

    d = dict()
    d.setdefault('a', []).append(1)
    d.setdefault('b', []).append(2)
    d.setdefault('a', []).append(3)
    print(d)


def func6():
    """
    有序字典
    """
    from collections import OrderedDict
    d = OrderedDict()
    d['d'] = 4
    d['b'] = 2
    d['a'] = 1
    d['c'] = 3
    print(d)
    import json
    print(json.dumps(d))


def func7():
    """
    字典相关计算
    """
    d = {'a': 1, 'b': 2}
    print(d.keys())
    print(d.values())
    print(d.items())
    z = zip(d.keys(), d.values())
    for zz in z:
        print(zz)
    # zip是个迭代器，内容只能被消费一次
    z = zip(d.keys(), d.values())
    print(dict(z))


def func8():
    """
    对切片命名
    """
    s = slice(1, 10, 2)
    print(s.start)
    print(s.stop)
    print(s.step)
    print(s.indices(5))
    print(s.indices(15))


def func9():
    """
    找出序列中出现次数最多的元素
    对数据制表或计数时
    """
    from collections import Counter
    words = ['a', 'c', 'b', 'a', 'd', 'e', 'f', 'v', 'b', 'a', 'e', 'c']
    word_counts = Counter(words)
    top_three = word_counts.most_common(3)
    print(top_three)


def func10():
    """
    通过公共键对字典列表排序
    """
    prices = [
        {'name': 'a', 'price': 1.0},
        {'name': 'b', 'price': 2.0},
        {'name': 'c', 'price': 3.0},
        {'name': 'd', 'price': 2.1},
        {'name': 'e', 'price': 1.5}
    ]
    from operator import itemgetter
    prices_by_name = sorted(prices, key=itemgetter('name'))
    prices_by_price = sorted(prices, key=itemgetter('price'))
    prices_by_price2 = sorted(prices, key=lambda p: p['price'])
    print(prices_by_name)
    print(prices_by_price)
    print(prices_by_price2)


def func11():
    """
    对不原生支持比较操作的对象排序排序
    """

    class Price:
        def __init__(self, name, price):
            self.name = name
            self.price = price

        def __repr__(self):
            return 'price(name:{}, price:{})'.format(self.name, self.price)

    prices = [
        Price('a', 1.0),
        Price('b', 2.0),
        Price('c', 3.0),
        Price('d', 2.1),
        Price('e', 1.5)
    ]
    from operator import attrgetter
    prices_by_name = sorted(prices, key=attrgetter('name'))
    prices_by_price = sorted(prices, key=attrgetter('price'))
    prices_by_price2 = sorted(prices, key=lambda p: p.price)
    print(prices_by_name)
    print(prices_by_price)
    print(prices_by_price2)


def func12():
    """
    根据字段将记录分组
    """
    from operator import itemgetter
    from itertools import groupby
    prices = [
        {'name': 'a', 'price': 1.0},
        {'name': 'b', 'price': 2.0},
        {'name': 'c', 'price': 2.0},
        {'name': 'd', 'price': 1.0},
        {'name': 'e', 'price': 1.0}
    ]
    prices.sort(key=itemgetter('price'))
    for data, items in groupby(prices, key=itemgetter('price')):
        print(data)
        for i in items:
            print(' ', i)


def func13():
    """
    list中筛选元素
    """
    values = [1, 2, -1, 0, 12, 5, -11]
    ivals = list(filter(lambda v: v > 0, values))
    print(ivals)
    from itertools import compress
    more1 = [v > 1 for v in values]
    ivals = list(compress(values, more1))
    print(ivals)


def func14():
    """
    名称映射到序列元组中
    """
    from collections import namedtuple
    price = namedtuple('price', ['name', 'price'])
    p = price('a', 1.0)
    print(p)
    print(p.name)
    print(p.price)


def func15():
    """
    将多个映射合并为单个映射
    """
    from collections import ChainMap
    a = {'a': 1, 'b': 2}
    b = {'c': 3, 'b': 4}
    c = ChainMap(a, b)
    print(c)
    print(c['a'])
    print(c['b'])
    print(c['c'])


if __name__ == "__main__":
    doFunc()
