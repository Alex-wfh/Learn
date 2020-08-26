#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc


def func1():
    """
    启动和停止线程

    threading 库可用来在单独的线程中执行任意的 Python 可调用对象。

    由于全局解释器锁(GIL)的存在，Python 线程的执行模型被限制为在任一时刻只允许在解释器中运行一个线程。
    基于这个原因，不应该使用 Python 线程来处理计算密集型的任务，因为在这种任务中我们希望在多个 CPU 核心上实现并行处理。
    Python 线程更适合于 I/O 处理以及阻塞操作的并发执行任务。

    尽量不要继承 Thread 进行开发，因为这样会使类只能在线程中使用。最好把代码从依赖关系中解放出来。
    """

    # 创建线程实例是，线程不会开始执行，调用它的 start() 方法，线程执行。
    import time

    def count_down(n):
        while n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(1)

    from threading import Thread
    t = Thread(target=count_down, args=(10,))
    t.start()

    # 线程实例会在它们自己所属的系统级现层呢中执行，这些线程完全由操作系统管理。一旦启动后，线程就开始独立运行，直到函数返回为止。可以查询线程实例来判断它是否还在运行。
    if t.is_alive():
        print('Still running') # 如果多个线程的 print() 方法同时执行，得到的结果可能有些乱，特别是在IDE中执行时
    else:
        print('Completed')

    # 也可以请求连接(join)到某个线程上，这么做会等待该线程结束。
    t.join()

    #解释器会一直保持运行，直到所有的线程终结为止。对于需要长时间运行的线程或者一直不断运行的后台任务，应该考虑将这些线程设置为守护(daemon)线程。
    # daemon 线程是无法被连接的，但是主线程结束后它们会自动销毁。
    t = Thread(target=count_down, args=(10,), daemon=True)
    t.start()

    # 除了 start() 和 join() 操作外，线程不支持其他操作。终止线程、给线程发信号、调整线程调度属性以及其他高级操作都需要开发者自己处理。
    # 如果想要终止线程，这个线程必须要能够在某个指定的点上轮训退出状态。
    class count_downTask:
        def __init__(self):
            self._running = True

        def terminate(self):
            self._running = False

        def run(self, n):
            while self._running and n > 0:
                print('T-minus', n)
                n -= 1
                time.sleep(1)
    c = count_downTask()
    t = Thread(target=c.run, args=(10,))
    t.start()
    time.sleep(1)
    c.terminate()
    t.join()

    # 线程有可能永远无法返回，所以最好加上超时处理。


def func2():
    """
    判断线程是否已经启动
    简单的、基于事件的线程间通信

    线程的核心特性就是其能够以非确定性的方式（完全由系统来调度管理）独立执行。这导致线程同步变得复杂。

    threading 库中，Event、Condition、Semaphore 都可解决线程见通信。
    Event: 一次性事件，针对多个线程
    Condition: 重复事件
    Semaphore: 信号量

    尽量不要在代码中涉及过多线程间同步技巧，可读性会很差。
    更明智的做法是利用队列或 actor 模式来完成线程间通信。
    """

    def threading_event():
        """
        使用 threading 库中的 Event 对象。Event 对象和条件标记(sticky flag)类似，允许线程等待某个事件发生。
        初始状态时，事件被设置为0，如果事件没被设置而线程正在等待该事件，那么线程会被阻塞，直到事件被设置位置。
        当有线程设置了这个事件时，就会唤醒所有正在等待该事件的线程。如果线程等待的事件已经被设置，那么线程会继续执行。
        注意: 下面代码中，"count_down is running" 总会在 "count_down starting" 之后显示。这里使用了事件来同步线程，使得主线程等待。
        """
        from threading import Thread, Event
        import time

        def count_down(n, _started_evt):
            print('count_down starting')
            _started_evt.set()
            while n > 0:
                print('T-minus', n)
                n -= 1
                time.sleep(1)
        started_evt = Event()
        t = Thread(target=count_down, args=(10, started_evt))
        t.start()
        started_evt.wait()
        print('count_down is running')
        t.join()

    print('=' * 20, 'threading_event', '=' * 20)
    threading_event()

    def threading_condition():
        """
        如果线程打算一遍又一遍地重复通知某个事件，那么最好使用 Condition 对象。
        """
        from threading import Thread, Condition
        import time

        class PeriodicTimer:
            def __init__(self, interval):
                self._interval = interval
                self._flag = 0
                self._cv = Condition()

            def start(self):
                t = Thread(target=self.run)
                t.daemon = True
                t.start()

            def run(self):
                while True:
                    time.sleep(self._interval)
                    with self._cv:
                        self._flag ^= 1
                        self._cv.notify_all()

            def wait_for_tick(self):
                with self._cv:
                    last_flag = self._flag
                    while last_flag == self._flag:
                        self._cv.wait()

        p_timer = PeriodicTimer(1)
        p_timer.start()
    
        def count_down(n_ticks):
            while n_ticks > 0:
                p_timer.wait_for_tick()
                print('T-minus', n_ticks)
                n_ticks -= 1
    
        def count_up(last):
            n = 0
            while n < last:
                p_timer.wait_for_tick()
                print('Counting', n)
                n += 1

        t1 = Thread(target=count_down, args=(10,))
        t1.start()
        t2 = Thread(target=count_up, args=(5,))
        t2.start()
        t1.join()
        t2.join()
    print('=' * 20, 'threading_condition', '=' * 20)
    threading_condition()

    """
    Event 对象的关键特性就是它会唤醒所有等待的线程。
    如果只希望唤醒一个单独的等待线程，那么最好使用 Semaphore 或者 Condition 对象
    """
    def threading_semaphore():
        from threading import Thread, Semaphore

        def worker(n, sema):
            sema.acquire()
            print('Working semaphore', n)

        sema = Semaphore()
        n_workers = 10
        t = dict()
        for n in range(n_workers):
            print(n)
            t[n] = Thread(target=worker, args=(n, sema))
            t[n].start()

        for n in range(n_workers):
            sema.release()

    print('=' * 20, 'threading_semaphore', '=' * 20)
    threading_semaphore()


def func3():
    """
    线程间通信

    把多线程按照简单的队列机制来实现，这有助于保持程序的清晰性。
    如果把所有任务都分解成简单的线程安全型队列来处理，就会发现不需要使用那些把程序弄的一团糟的锁和其他的底层同步原语。
    此外，使用队列进行通信常常使得程序的设计可以在稍后扩展到其他类型的基于消息通信的模式上。例如分解为多个进程，甚至做成分布式系统。

    在线程中使用队列时，将某个数据放入队列并不会产生该数据的拷贝。因此，通信过程实际上涉及在不同的线程间传递对象的引用。
    如果需要关心共享状态，那么要么只传递不可变的数据结构，要么对队列中的数据做深拷贝(deepcopy)。
    """

    """
    也许将数据从一个线程发往另一个线程最安全的做法就是使用 queue 模块中的 Queue(队列)了。要做到这些，首先创建一个 Queue 实例，它会被所有的线程共享。之后线程可以使用 put() 和 get() 操作来给队列添加或移除元素。
    """
    def simple_queue():
        from queue import Queue
        from threading import Thread

        def producer(out_q):
            for i in range(5):
                data = 'data_test, {}'.format(i)
                out_q.put(data)

        def consumer(in_q):
            while True:
                data = in_q.get()
                print(data)
                if data == 'data_test, 4':
                    break

        q = Queue()
        t1 = Thread(target=consumer, args=(q,))
        t2 = Thread(target=producer, args=(q,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    print('=' * 20, 'simple_queue', '=' * 20)
    simple_queue()

    """
    当使用队列时，如果对生产者(producer)和消费者(consumer)的关闭过程进行同步协调需要用到一些技巧，
    一般化的解决方法是使用一个特殊的终止值，当我们将它放入队列中时就使消费者退出。
    注意: 当 consumer 接收到特殊的终止值后，会立即将其重新放回队列中。这么做可使得在同一队列上监听的其他 consumer 也能接收到终止值。因此可以一个一个将 consumer 全部关闭。
    """
    def simple_queue_quit():
        from queue import Queue
        from threading import Thread

        _sentinel = object()

        def producer(out_q):
            for i in range(5):
                data = 'data_test'
                out_q.put(data)
            out_q.put(_sentinel)

        def consumer(in_q):
            while True:
                data = in_q.get()
                print(data)
                if data is _sentinel:
                    in_q.put(_sentinel)
                    break

        q = Queue()
        t1 = Thread(target=consumer, args=(q,))
        t2 = Thread(target=producer, args=(q,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    print('=' * 20, 'simple_queue_quit', '=' * 20)
    simple_queue_quit()

    """
    尽管队列是线程间通信的最常见的机制，但只要添加了所需的锁和同步功能，就可以构建自己的线程安全型的数据结构。最常见的做法就是将数据结构和条件变量打包在一起。
    构建一个线程安全的优先级队列
    """
    def self_queue():
        import heapq
        import threading

        class PriorityQueue:
            """
            可以用这个自定义的类来代替Queue，作为线程安全的优先级队列。
            """
            def __init__(self):
                self._queue = []
                self._count = 0
                self._cv = threading.Condition()

            def put(self, item, priority):
                with self._cv:
                    heapq.heappush(self._queue, (-property, self._count, item))
                    self._count += 1
                    self._cv.notify()

            def get(self):
                with self._cv:
                    while len(self._queue) == 0:
                        self._cv.wait()
                    return heapq.heappop(self._queue)[-1]

    """
    通过队列实现的线程间通信是一种单方向且不确定的过程。
    一般来说我们无法得知 consumer 何时会实际接收信息并开始工作。但是 Queue 对象提供了一些基本的事件完成功能(completion feature)。
    例如 task_done() 和 join() 方法
    """
    def queue_task_done():
        import time
        from queue import Queue
        from threading import Thread

        def producer(out_q):
            for i in range(5):
                data = 'data_test, {}'.format(i)
                out_q.put(data)

        def consumer(in_q):
            while True:
                data = in_q.get()
                print(data)
                in_q.task_done()
                time.sleep(1)
                if data == 'data_test, 4':
                    break

        q = Queue()
        t1 = Thread(target=consumer, args=(q,))
        t2 = Thread(target=producer, args=(q,))
        t1.start()
        t2.start()
        # Wait for all produced items to be consumed
        q.join()

    print('=' * 20, 'queue_task_done', '=' * 20)
    queue_task_done()

    """
    当 consumer 处理了某项特定的数据，而 producer 需要对此立刻感知的话，那么就应该将发送的数据和一个 Event 对象配对在一起，这样就允许 producer 可以监视这一过程。
    """
    def queue_with_event():
        import time
        from queue import Queue
        from threading import Thread, Event

        def producer(out_q):
            for i in range(5):
                data = 'data_test, {}'.format(i)
                evt = Event()
                out_q.put((data, evt))
                print('put data', data)
                evt.wait()

        def consumer(in_q):
            while True:
                data, evt = in_q.get()
                print(data)
                evt.set()
                time.sleep(1)
                if data == 'data_test, 4':
                    break

        q = Queue()
        t1 = Thread(target=consumer, args=(q,))
        t2 = Thread(target=producer, args=(q,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    print('=' * 20, 'queue_with_event', '=' * 20)
    queue_with_event()

    """
    如果通过一个可选的大小参数来创建 Queue 对象，例如 Queue(N)，那么这就在 put() 操作阻塞 producer 之前对可以入队列的元素个数进行了限制。
    如果 producer 和 consumer 处理数据的速度存在差异时，给队列的大小设置一个上限就显得很有意义了。
    总的来说，线程间通信的控制流是一个看似简单实则困难的问题。如果发现需要通过调整队列的大小来修正问题，那么就表明程序的设计不够健壮，或者存在固有的扩展问题。
    get() 和 put() 方法都支持非阻塞和超时机制。这两种机制都可用来避免在特定的队列操作上无限期阻塞的问题。
    """
    def queue_extra():
        import queue

        q = queue.Queue()

        try:
            data = q.get(block=False)
        except queue.Empty:
            pass

        try:
            data = q.put('item', block=False)
        except queue.Full:
            pass

        try:
            data = q.get(timeout=0.5)
        except queue.Empty:
            pass

    """
    还有一些很实用的方法，比如 q.qsize(), q.full(), q.empty()。它们能够表示队列当前的大小和状态。
    但要注意，这些方法在多线程环境中都是不可靠的。也就是说，编写代码时最好不要依赖这些函数。
    """


def func4():
    """
    对临界区加锁

    要想让可变对象安全地用在多线程环境中，可以利用 threading 库中的 Lock 对象来解决。
    当使用 with 语句时，Lock 对象可确保产生互斥的行为，也就是说，同一时间只允许一个线程执行 with 语句块中的代码。with 语句会执行缩进的代码块时获取到锁，当控制流离开缩进的代码块时释放这个锁。

    线程的调度从本质上来说是非确定性的。正因为如此，在多线程程序中如果不用好锁就会使得数据被随机地破坏掉，以及产生称之为竞态条件的奇怪行为。要避免这些问题，只要共享的可变状态需要被多个线程访问，那么就得使用锁。

    也可手动调用 Lock 对象的 acquire() 和 release() 方法来添加和释放锁，但是 with 语句更优雅，更不容易出错。

    要避免可能出现的死锁，用到了锁的程序应该保证每个线程一次只允许获取一把锁。如果无法做到，那么就需要引入更为高级的避免死锁的技术。

    treading 库中还存在其他的同步原语。例如 RLock 和 Semaphore。这些对象一般不用在简单的加锁处理，而是有更特殊的用途。
    RLock 被称为可重入锁，它可以被同一个线程多次获取，主要用来编写基于锁的代码，或者基于"监视器"的同步处理。
    Semaphore 可以像 Lock 一样使用，但其实现更为复杂，会对程序的性能带来负面影响。此外，Semaphore 对象对于那些涉及在线程之间发送信号或者需要实现字节流处理的应用更加有用。
    """

    import threading

    class ShareCounter:
        def __init__(self, initial_value=0):
            self._value = initial_value
            self._value_lock = threading.Lock()

        def incr(self, delta=1):
            with self._value_lock:
                self._value += delta

        def decr(self, delta=1):
            with self._value_lock:
                self._value -= delta


def func5():
    """
    避免死锁

    方案1: 检查死锁并解决（看门狗定时器）
    方案2: 以不会让程序进入死锁状态的方式使用锁
    """
    """
    在多线程程序中，出现死锁的常见原因是线程一次尝试获取了多个锁。
    避免死锁的一种解决方式就是给程序中每个锁分配一个唯一的数字编号，并且在获取多个锁时只按照编号的生序方式来获取。利用上下文管理器来实现这个机制非常简单。
    
    要使用这个上下文管理器，只用按照正常的方式来分配锁对象，但是当想同一个或多个锁打交道时就使用 acquire() 函数。
    """
    print('=' * 20, 'idx_lock', '=' * 20)
    import threading
    from contextlib import contextmanager

    # 线程本地存储，如果有多个 acquire() 操作嵌套在一起，可以检查可能存在死锁的情况
    _local = threading.local()

    @contextmanager # 支持上下文
    def acquire(*locks):
        # 关键之处，根据对象的数字编号对锁进行排序，无论用户按照什么顺序将锁提供给 acquire() 函数，它们总是会按照统一的顺序来获取。
        locks = sorted(locks, key=lambda x: id(x))
        acquired = getattr(_local, 'acquired', [])
        if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
            raise RuntimeError('Lock Order Violation')
        acquired.extend(locks)
        _local.acquired = acquired
        try:
            for lock in locks:
                lock.acquire()
            yield
        finally:
            for lock in reversed(locks):
                lock.release()
            del acquired[-len(locks):]

    x_lock = threading.Lock()
    y_lock = threading.Lock()

    def thread_1():
        for i in range(10):
            with acquire(x_lock, y_lock):
                print('Thread-1')

    def thread_2():
        for i in range(10):
            with acquire(y_lock, x_lock):
                print('Thread-2')

    t1 = threading.Thread(target=thread_1)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=thread_2)
    t2.daemon = True
    t2.start()

    t1.join()
    t2.join()

    print('=' * 20, 'dining philosopher’s problem', '=' * 20)
    """
    哲学家就餐问题。5位哲学家，5碗米饭，5支筷子
    """
    import threading

    def philosopher(left, right):
        for i in range(5):
            with acquire(left, right):
                print(threading.currentThread(), 'eating')

    n_sticks = 5
    chopsticks = [threading.Lock() for n in range(n_sticks)]

    t_dict = dict()
    for n in range(n_sticks):
        t_dict[n] = threading.Thread(target=philosopher, args=(chopsticks[n], chopsticks[(n+1) % n_sticks]))
        t_dict[n].start()
    for n in range(n_sticks):
        t_dict[n].join()


def func6():
    """
    保存线程专有状态

    在大部分程序中，创建和操作线程专有状态都不会出现什么问题，如果出现问题，通常是因为多个线程使用了同一个对象，而该对象需要操作某种系统资源。
    不该让同一系统资源同时被所有线程共享，如果多个线程同时操作同一个系统资源，那么就会出现混乱。
    线程专有存储通过让这种资源只对一个线程可见，解决了这个问题。

    使用 threading.local() 使得 LazyConnection 类支持每个线程一条连接，而不是之前的整个进程就一条连接。

    在底层，threading.local() 实例为每个线程维护着一个单独的实例字典。所有对实例常见的操作比如获取、设定以及删除都只作用于每个线程专有的字典上。
    每个线程使用一个单独的字典，正式这一事实使得不同线程的数据得到隔离。
    """
    from socket import socket, AF_INET, SOCK_STREAM
    import threading

    class LazyConnection:
        def __init__(self, address, family=AF_INET, type_=SOCK_STREAM):
            self.address = address
            self.family = family
            self.type = type_
            self.local = threading.local()

        def __enter__(self):
            if hasattr(self.local, 'sock'):
                raise RuntimeError('Already connected')
            self.local.sock = socket(self.family, self.type)
            self.local.sock.connect(self.address)
            return self.local.sock

        def __exit__(self, exc_ty, exc_val, tb):
            self.local.sock.close()
            del self.local.sock

    from functools import partial

    def test(connection):
        with connection as s:
            s.send(b'GET /index.html HTTP/1.0\r\n')
            s.send(b'Host: www.python.org\r\n')
            s.send(b'\r\n')
            resp = b''.join(iter(partial(s.recv, 8192), b''))
        print('Got {} bytes'.format(len(resp)))

    conn = LazyConnection(('www.python.org', 80))
    t1 = threading.Thread(target=test, args=(conn,))
    t2 = threading.Thread(target=test, args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def func7():
    """
    创建线程池

    一般来说，应该避免编写允许线程数量无限增长的程序。
    通过使用预先初始化好的线程池，就可以小心地为所能支持的并发总数设定一个上限值。
    无需担心创建大量线程所产生的影响。在现代系统上，创建拥有几千个线程的线程池是不会有什么问题的。此外让一千个线程等待工作并不会对其他部分的代码产生性能上的影响。
    线程池只适用于处理 I/O 密集型的任务。
    创建大型线程池需要考虑的主要问题就是内存的使用。注意虚拟内存和物理内存的区别，
    """
    def thread_pool_executor():
        """
        concurrent.futures 库中包含有一个 ThreadPoolExecutor 类可以用来实现这个目的。
        """
        from socket import AF_INET, SOCK_STREAM, socket
        from concurrent.futures import ThreadPoolExecutor

        def echo_client(sock, client_addr):
            print('Got connection from', client_addr)
            while True:
                msg = sock.recv(65536)
                print(msg)
                if not msg:
                    break
                sock.sendall(msg)
            print('Client closed connection')
            sock.close()

        def echo_server(addr):
            pool = ThreadPoolExecutor(128)
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(addr)
            sock.listen(5)
            while True:
                client_sock, client_addr = sock.accept()
                pool.submit(echo_client, client_sock, client_addr)

        echo_server(('', 15000))

    # thread_pool_executor()

    def thread_pool_queue():
        """
        如果想手动创建线程池，使用 Queue 来实现通常也足够简单。
        """
        from socket import socket, AF_INET, SOCK_STREAM
        from threading import Thread
        from queue import Queue

        def echo_client(q):
            sock, client_addr = q.get()
            print('Got connection from', client_addr)
            while True:
                msg = sock.recv(65536)
                if not msg:
                    break
                sock.sendall(msg)
            print('Client closed connection')
            sock.close()

        def echo_server(addr, n_workers):
            q = Queue()
            for n in range(n_workers):
                t = Thread(target=echo_client, args=(q,))
                t.daemon = True
                t.start()
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(addr)
            sock.listen(5)
            while True:
                client_sock, client_addr = sock.accept()
                q.put((client_sock, client_addr))

        echo_server(('', 15000), 128)

    # thread_pool_queue()

    def thread_pool_result():
        """
        应该使用 ThreadPoolExecutor 而不是手动实现线程池。优势在于使得任务的提交者能够更容易从函数中取得结果。
        """
        from concurrent.futures import ThreadPoolExecutor
        import urllib.request

        def fetch_url(url):
            u = urllib.request.urlopen(url)
            data = u.read()
            return data

        pool = ThreadPoolExecutor(10)
        a = pool.submit(fetch_url, 'http://www.python.org')
        b = pool.submit(fetch_url, 'http://www.pypy.org')
        # 结果对象（即，a 和 b）负责处理所有需要完成的阻塞和同步任务，从工作者线程中取回数据。
        # a.result() 操作会阻塞，直到对应的函数已经由线程池执行完毕并返回结果为止。
        print(a.result())
        print(b.result())

    thread_pool_result()


def func8():
    """
    实现简单的并行编程

    concurrent.futures 库中提供了一个 ProcessPoolExecutor 类，可用来在单独运行的 Python 解释器实例中执行计算密集型的函数。
    尽管进程池使用起来很简单，但是在设计规模更大的程序时有几个重要的因素需要考虑。
    1. 多进程技术只适用于将问题分解成各个独立部分的情况。
    2. 任务必须定义成普通的函数来提交。实例方法、闭包或者其他类型的可调用对象都不支持并行处理。
    3. 函数的参数和返回值必须可兼容于 pickle 编码。因为需要进程间通信。
    4. UNIX 中会使用 fork() 系统调用来创建，这么做会克隆出一个 Python 解释器，在 fork() 时会包含所有的程序状态。
       Windows 中会加载一个独立的解释器拷贝，但不会包含状态。克隆出来的进程在首次调用 pool.map() 或者 pool.submit() 方法之前不会实际运行。
       尤其要注意，不同系统中进程池可能存在不同的表现。
    5. 当将进程池和多线程技术结合在一起时需要格外小心。特别是，很可能我们应该在创建任何线程之前优先创建并加载进程池。
    """

    """
    在底层，ProcessPoolExecutor 创建了 N 个独立运行的 Python 解释器，这里的 N 默认是在系统上检测到的可用的 CPU 个数，也可通过入参指定进程数。
    进程池会一直运行，直到 with 语句块中的最后一条语句执行完毕为止，此时进程池就会关闭。但程序会一直等待所有已经提交的任务都处理完毕为止。
    """
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor() as pool:
        """
        do work in parallel using pool
        """
        pass

    """
    提交到进程池的任务必须定义成函数的形式。
    有两种方法可以提交任务。
    使用 pool.map() 可以并行处理一个列表推导式或者 map() 操作。使用 pool.submit() 可以手动提交一个单独的任务。
    如果手动提交任务，得到的结果就是一个 Future 实例。要获取到实际的结果还需要调用它的 result() 方法。这么做会阻塞进程，直到完成类计算并将结果返回给进程池为止。
    """
    global work # 注意：进程间通过 pickle 通信，而 pickle 只支持序列化包最上层的函数、类。所以需要将 work 函数定义为 golbal 的。

    def work(x):
        return x

    with ProcessPoolExecutor() as pool:
        results = pool.map(work, range(10))
        for result in results:
            print(result)

    with ProcessPoolExecutor() as pool:
        future_result = pool.submit(work, 'data')
        r = future_result.result()
        print(r)

    """
    与其让进程阻塞，也可以提供一个回调函数，让他在任务完成时得到触发执行。
    用户提供的回调函数需要接受一个 Future 实例，必须用它才能获取到实际的结果（即调用它的 result() 方法）。
    """
    def when_done(r):
        print('Got:', r.result())

    with ProcessPoolExecutor() as pool:
        future_result = pool.submit(work, 'data')
        future_result.add_done_callback(when_done)


def func9():
    """
    如何规避 GIL 带来的限制

    尽管 Python 完全支持多线程编程，但是在解释器的 C 语言实现中，有一部分并不是线程安全的，因此不能完全支持并发执行。
    事实上，解释器被一个称之为全局解释器锁(GIL)的东西保护着，在任意时刻只允许一个 Python 线程投入执行。
    GIL 带来的最明显的影响就是多线程的 Python 程序无法充分利用多个 CPU 核心带来的优势。
    即，一个采用多线程技术的计算密集型应用只能在一个 CPU 上运行。

    要规避 GIL 的限制主要有两种常用的策略：
    1. 使用 multiprocessing 模块来创建进程池，把它当做协处理器来使用。
        需要涉及同另一个 Python 解释器之间进行数据序列化和通信处理。为了让这种方法奏效，代执行的操作需要包含在以 def 语句定义的 Python 函数中，且函数参数和返回值必须兼容于 pickle 编码。
        此外，要完成的工作规模必须足够大时才能考虑使用 multiprocessing，这样可以弥补额外产生的通信开销。
    2. 将计算密集型的任务转移到 C 语言中，使其独立于 Python，在 C 代码中释放 GIL。
        确保 C 代码可以独立于 Python 执行。这意味着不适用 Python 的数据结构，也不调用 Python 的 C 语言 API。
        同样，只有 C 语言扩展模块能够完成足够多的任务时才考虑此方案。
    """


def func10():
    """
    定义一个 Actor 任务

    actor 优势：原理简单、可扩展。

    actor 模式是最古老也是最简单的用来解决并发和分布式计算问题的方法之一。
    actor 就是一个并发执行的任务，它只是简单地对发送给它的消息进行处理。
    作为对这些消息的响应，actor 会决定是否要对其他的 actor 发送进一步的信息。
    actor 任务之间的通信是单向且异步的。因此，消息的发送者并不知道消息何时才会实际传递，当消息已经处理完毕时也不会接收到响应或者确认。

    actor 模式之所以吸引人，它的简单性是原因之一。在实践中只有 send() 一个核心操作。
    此外，基于 actor 模式的系统中，"消息"的概念可以扩展到许多不同的方向。
    """
    from queue import Queue
    from threading import Thread, Event

    class ActorExit(Exception):
        pass

    class Actor:
        def __init__(self):
            self._mailbox = Queue()

        def send(self, msg):
            self._mailbox.put(msg)

        def recv(self):
            msg = self._mailbox.get()
            if msg is ActorExit:
                raise ActorExit()
            return msg

        def close(self):
            self.send(ActorExit)

        def start(self):
            self._terminated = Event()
            t = Thread(target=self._bootstrap)
            t.daemon = True
            t.start()

        def _bootstrap(self):
            try:
                self.run()
            except ActorExit:
                pass
            finally:
                self._terminated.set()

        def join(self):
            self._terminated.wait()

        def run(self):
            while True:
                msg = self.recv()

    class PrintActor(Actor):
        def run(self):
            while True:
                msg = self.recv()
                print('Got:', msg)

    p = PrintActor()
    p.start()
    p.send('Hello')
    p.send('World')
    p.close()
    p.join()

    """
    去掉并发和异步消息传递，用生成器定义一个最简化的 actor 对象。
    """
    def print_actor():
        while True:
            try:
                msg = yield
                print('Got:', msg)
            except GeneratorExit:
                print('Actor terminating')

    p = print_actor()
    next(p)
    p.send('Hello')
    p.send('World')
    p.close()


def func11():
    """
    实现发布者/订阅者消息模式

    一般来说需要引入一个单独的"交换"或者"网关"对象，作为所有消息的中介。
    也就是说，不是直接将消息从一个任务发往另一个任务，而是将消息发往交换中介，由中介将消息转发给一个或多个相关联的任务。

    交换中介其实就是一个对象，它保存了活跃的订阅者集合，并提供关联、取消关联以及发送消息的方法。每个交换中介都由一个名称来标识。

    发布者/订阅者模型的好处：
    1. 使用交换中介可以简化很多设定线程通信的工作。
    2. 交换中介具有将消息广播发送给多个订阅者的能力。
    3. 能和各种类似于任务的对象一起工作。

    交换中介的思想可以有许多种可能的扩展。实现一整个消息通道的集合、对交换中介的名称加以模式匹配规则、扩展到分布式计算等。
    """
    from collections import defaultdict

    class Exchange:
        def __init__(self):
            self._subscribers = set()

        def attach(self, task):
            self._subscribers.add(task)

        def detach(self, task):
            self._subscribers.remove(task)

        def send(self, msg):
            for subscriber in self._subscribers:
                subscriber.send(msg)

    _exchanges = defaultdict(Exchange)

    def get_exchange(name):
        return _exchanges[name]

    class Task:
        def __init__(self):
            pass

        def send(self, msg):
            pass

    task_a = Task()
    task_b = Task()

    # Example of getting an exchange
    exc = get_exchange('name')

    # Examples of subscribing tasks to it
    exc.attach(task_a)
    exc.attach(task_b)

    # Example of sending messages
    exc.send('msg1')
    exc.send('msg2')

    # Example of unsubscribing
    exc.detach(task_a)
    exc.detach(task_b)


def func12():
    """
    使用生成器(协程，有时也称为用户级线程或绿色线程)作为线程的替代方案

    优点：执行效率极高、不需要锁机制。
    缺点：执行到阻塞(CPU密集型或者I/O阻塞型)代码会使整个任务调度器挂起，部分 Python 库不能很好地配合协程使用。

    当构建基于生成器的并发框架时，使用一般形式的 yield 是最为常见的。以此形式使用 yield 的函数更常被称为"协程"。
    """

    def count_down(n):
        while n > 0:
            print('T-minus', n)
            yield
            n -= 1
        print('Blastoff!')

    def count_up(n):
        x = 0
        while x < n:
            print('Counting up', x)
            yield
            x += 1

    from collections import deque

    class TaskScheduler:
        def __init__(self):
            self._task_queue = deque()

        def new_task(self, task):
            self._task_queue.append(task)

        def run(self):
            while self._task_queue:
                task = self._task_queue.popleft()
                try:
                    next(task)
                    self._task_queue.append(task)
                except StopIteration:
                    pass

    # Example use
    sched = TaskScheduler()
    sched.new_task(count_down(10))
    sched.new_task(count_down(5))
    sched.new_task(count_up(15))
    sched.run()


def func13():
    """
    轮询多个线程队列

    要对非文件类型的对象比如队列做轮询操作，可以遍历所有队列，分别判断队列是否为空，为避免 CPU 利用率过高还需要使用定时器。
    这种方式很笨重，而且可能会出现性能问题。

    通过把队列放在和 socket 同等的地位上，只要一个单独的 select() 调用就可以轮询这两种对象的活跃性。不需要使用超时或其他基于时间的技巧来做周期性的检查。
    此外，如果数据添加到了队列中，消费者几乎能在同一时间得到通知。
    以底层 I/O 的一点负载，换取更好的响应时间以及简化的代码编写，通常是很值得的。
    """
    import queue
    import socket
    import time

    class PollableQueue(queue.Queue):
        """
        针对每个想要轮询的队列（或任何对象），创建一对互联的 socket。
        然后对其中一个 socket 执行写操作，以表示数据存在。另一个 socket 就传递给 select() 或者类似的函数来轮询数据。
        """
        def __init__(self):
            super().__init__()
            self._put_socket, self._get_socket = socket.socketpair()
            """
            # 兼容不同操作系统
            import os
            if os.name == 'posix':
                self._put_socket, self._get_socket = socket.socketpair()
            else:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind(('127.0.0.1', 0))
                server.listen(1)
                self._put_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._put_socket.connect(server.getsockname())
                self._get_socket, _ = server.accept()
                server.close()
            """

        def fileno(self):
            return self._get_socket.fileno()

        def put(self, item):
            super().put(item)
            self._put_socket.send(b'x')

        def get(self):
            self._get_socket.recv(1)
            return super().get()

    import select
    import threading

    def consumer(queues):
        """
        不管把数据放入哪个队列中，消费者最后都能接收到所有数据。
        """
        while True:
            can_read, _, _ = select.select(queues, [], [])
            for r in can_read:
                item = r.get()
                print('Got:', item)
                if item == 'stop':
                    return

    q1 = PollableQueue()
    q2 = PollableQueue()
    q3 = PollableQueue()
    t = threading.Thread(target=consumer, args=([q1, q2, q3],))
    t.daemon = True
    t.start()

    q1.put(1)
    q2.put(10)
    q3.put('hello')
    q2.put(15)
    time.sleep(1)
    q1.put('stop')
    t.join()


def func14():
    """
    在 UNIX 上加载守护进程

    创建一个守护进程的步骤看上去不是很易懂，但是大体思想是这样的，
    1. 守护进程从父进程中脱离，并将父进程终止。
    2. 将守护进程从终端中分离开来。
    3. 改变工作目录，使守护进程不在工作于加载它的目录之下。
    4. 让守护进程失去获得新控制终端的能力。
    5. 重新初始化标准 I/O 流，使其指向由用户指定的文件。
    6. 将进程 ID 写入到一个文件中，以便稍后给其他的程序使用
    """


if __name__ == '__main__':
    doFunc()