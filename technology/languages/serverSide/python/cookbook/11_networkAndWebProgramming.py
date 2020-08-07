#!/usr/bin/env python3
# ! -*- coding:utf-8 -*-

from doFunc import doFunc


def func1():
    """
    以客户端的形式同HTTP服务交互

    urllib: python内置库，适合处理简单的任务
    requests: 第三方库，功能强大。能以多种方式从请求中返回响应结果的内容

    如果确实很简单的HTTP客户端代码，通常使用内建的urllib就够了。
    如果要做的不仅是简单的 GET 或 POST 请求，那就需要使用 requests 了.

    个人看法：requests 的唯一劣势就是需要安装。除非是无requests包且不方便安装，同时是比较简单的HTTP请求，否则就使用 requests。
    """
    def urllib_get():
        from urllib import request, parse
        url = 'http://httpbin.org/get'
        parms = {
            'name1': 'value1',
            'name2': 'value2'
        }
        query_string = parse.urlencode(parms)
        u = request.urlopen(url + '?' + query_string)
        return u.read()

    print(urllib_get())

    def urllib_post():
        from urllib import request, parse
        url = 'http://httpbin.org/post'
        parms = {
            'name1': 'value1',
            'name2': 'value2'
        }
        query_string = parse.urlencode(parms)
        u = request.urlopen(url, query_string.encode('ascii'))
        return u.read()

    print(urllib_post())

    def urllib_with_headers():
        from urllib import request, parse
        url = 'http://httpbin.org/post'
        parms = {
            'name1': 'value1',
            'name2': 'value2'
        }
        query_string = parse.urlencode(parms)
        headers = {
            'User-agent': 'none/of/your/business',
            'Spam': 'Eggs'
        }
        req = request.Request(url, query_string.encode('ascii'), headers=headers)
        u = request.urlopen(req)
        return u.read()

    print(urllib_with_headers())

    def requests_test():
        import requests
        url = 'http://httpbin.org/post'
        parms = {
            'name1': 'value1',
            'name2': 'value2'
        }
        headers = {
            'User-agent': 'none/of/your/business',
            'Spam': 'Eggs'
        }
        resp = requests.post(url, data=parms, headers=headers)
        return resp.text

    print(requests_test())


def func2():
    """
    创建一个 TCP 服务器

    socketserver 模块使得创建简单的 TCP 服务器相对来说变得容易了许多。

    默认情况下这个服务器是单线程的，一次只能处理一个客户端。
    如果想要处理多个客户端，可以实例化 ForkingTCPServer 或者 ThreadingTCPServer 对象。
    多进程和多线程服务器会针对每一个客户端连接创建一个新的进程或线程，且没有上限。
    所以应该预先分配好工作者的进程或线程池

    BaseRequestHandler 和 StreamRequestHandler 对比，后者更灵活，而且可以通过指定额外的类变量来提供一些功能

    大部分 Python 中的高级网络模块都是在 socketserver 的功能上构建的。直接使用socket库来实现服务器也不太困难。
    """
    def base_server():
        from socketserver import BaseRequestHandler, TCPServer

        class EchoHandler(BaseRequestHandler):
            def handle(self):
                print('Got connection from', self.client_address)
                while True:
                    msg = self.request.recv(8192)
                    if not msg:
                        break
                    self.request.send(msg)

        serv = TCPServer(('', 20000), EchoHandler)
        serv.serve_forever()

    def conn_server():
        """
        客户端代码，用来测试服务端程序
        """
        from socket import socket, AF_INET, SOCK_STREAM
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 20000))
        print(s.send(b'Hello'))
        print(s.recv(8192))

    def test():
        """
        1. 新启线程运行服务端程序
        2. 运行客户端测试方法
        3. 完成后强杀线程
        """
        import threading
        thread = threading.Thread(target=base_server)
        thread.start()
        print('=' * 20, 'server started', '=' * 20)

        print('=' * 20, 'try to connect server', '=' * 20)
        conn_server()

        import ctypes
        import inspect

        def stop_thread(thread):
            tid = thread.ident
            exc_type = SystemExit

            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exc_type):
                exc_type = type(exc_type)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        stop_thread(thread)

    test()

    # 许多情况下定义一个类型稍有不同的处理类可能会更加简单
    def socket_server():
        from socketserver import StreamRequestHandler, TCPServer

        class EchoHandler(StreamRequestHandler):
            def handle(self):
                print('Got connection from', self.client_address)
                for line in self.rfile:
                    self.wfile.write(line)

        serv = TCPServer(('', 20000), EchoHandler)
        serv.serve_forever()


def func3():
    """
    创建一个 UDP 服务器

    与 TPC 类似，只是不需要建立连接
    同样提供 ForkingUDPServer 和 ThreadingUDPServer 支持并发
    """
    def base_server():
        import time
        from socketserver import BaseRequestHandler, UDPServer

        class EchoHandler(BaseRequestHandler):
            def handle(self):
                print('Got connection from', self.client_address)
                msg, sock = self.request
                resp = time.ctime()
                sock.sendto(resp.encode('ascii'), self.client_address)

        serv = UDPServer(('', 20000), EchoHandler)
        serv.serve_forever()

    def conn_server():
        """
        客户端代码，用来测试服务端程序
        """
        from socket import socket, AF_INET, SOCK_DGRAM
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(b'', ('localhost', 20000))
        print(s.recvfrom(8192))

    def test():
        """
        1. 新启线程运行服务端程序
        2. 运行客户端测试方法
        3. 完成后强杀线程
        """
        import threading
        thread = threading.Thread(target=base_server)
        thread.start()
        print('=' * 20, 'server started', '=' * 20)

        print('=' * 20, 'try to connect server', '=' * 20)
        conn_server()

        import ctypes
        import inspect

        def stop_thread(thread):
            tid = thread.ident
            exc_type = SystemExit

            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exc_type):
                exc_type = type(exc_type)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        stop_thread(thread)

    test()


def func4():
    """
    从 CIDR 地址中生成 IP 地址的范围

    类似需求直接使用 ipaddress

    ipaddress 模块中有一些类可用来表示 IP 地址、网络对象以及接口。如果需要处理网络地址的话，直接使用 ipaddress 即可
    需要注意：ipaddress 模块同其他网络相关的模块比如 socket 库之间的交互是有局限性的。特别是，通常不能用 IPv4Address 的实例作为地址字符串代替，需要通过 str() 进行转换。
    """
    import ipaddress

    net = ipaddress.ip_network('123.45.67.64/27')
    print(net)
    for a in net:
        print(a)
    net6 = ipaddress.ip_network('12:3456:78:90ab:cd:ef01:23:30/125')
    print(net6)
    for a in net6:
        print(a)
    i_net = ipaddress.ip_interface('123.45.67.73/27')
    print(i_net.network)
    print(i_net.ip)


def func5():
    """
    创建基于 REST 风格的简单接口

    REST: Representational State Transfer, 具象派的 状态 传递

    要实现一个简单的 REST 风格的接口，通常只要根据 Python 的 WSGI 标准来做就可以了。标准库和绝大多数第三方的Web框架都支持REST。
    """
    import cgi

    def not_found_404(environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not Found']

    class PathDispatcher:
        def __init__(self):
            self.path_map = {}

        def __call__(self, environ, start_response):
            path = environ['PATH_INFO']
            params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)
            method = environ['REQUEST_METHOD'].lower()
            environ['params'] = {key: params.getvalue(key) for key in params}
            handler = self.path_map.get((method, path), not_found_404)
            return handler(environ, start_response)

        def register(self, method, path, function):
            self.path_map[method.lower(), path] = function
            return function


def func6():
    """
    利用 XML-RPC 实现简单的远端过程调用

    RPC: Remote Procedure Call 远端过程调用

    要配置一个简单的远端过程调用服务，可以用 XML-RPC 实现，
    所要做的就是创建一个服务器实例，通过 register_function() 方法注册处理函数，然后通过 serve_forever() 方法加载即可。

    通常，不应该将 XML-RPC 服务作为公有 API 暴露给外部用户。

    XML-RPC 的缺点在于它的性能。SimpleXMLRPCServer 是以单线程来实现的，不适合用来扩展大型的应用。
    由于 XML-RPC 会将所有数据序列化为 XML 格式，因此会比其他方法慢一些。

    XML-RPC 的优点在于简单，而且适用于很多语言。
    """
    from xmlrpc.server import SimpleXMLRPCServer

    class KeyValueServer:
        _rpc_methods = ['get', 'set', 'delete', 'exists', 'keys']

        def __init__(self, address):
            self.data = {}
            self._serv = SimpleXMLRPCServer(address, allow_none=True)
            for name in self._rpc_methods:
                self._serv.register_function(getattr(self, name))

        def get(self, name):
            return self._data[name]

        def set(self, name, value):
            self._data[name] = value

        def delete(self, name):
            del self._data[name]

        def exists(self, name):
            return name in self._data

        def keys(self):
            return self._data.keys()

        def service_forever(self):
            self._serv.serve_forever()

    kv_serv = KeyValueServer(('', 15000))
    kv_serv.service_forever()


def func7():
    """
    在不同的解释器间进行通信

    multiprocessing.connection 库只需要使用几个简单的原语(primitive)，就能轻易地将各个解释器联系在一起并在它们之间交换消息。

    multiprocessing 模块不适合实现面向公众型的服务。

    multiprocessing 模块更适合于能长时间运行的连接，而不是大量的短连接。同时也不适合需要对连接实现更多底层控制的需求。
    """
    from multiprocessing.connection import Listener
    import traceback

    def echo_client(conn):
        try:
            while True:
                msg = conn.recv()
                conn.send(msg)
        except EOFError:
            print('Connection closed')

    def echo_server(address, authkey):
        serv = Listener(address, authkey=authkey)
        while True:
            try:
                client = serv.accept()
                echo_client(client)
            except Exception:
                traceback.print_exc()

    echo_server(('', 25000), authkey=b'peekaboo')


def func8():
    """
    远端过程调用

    RPCHandler 和 RPCProxy 类的总体思想比较简单。
    客户端调用远端函数，代理类就创建出一个包含了函数名和参数的元组。这个元组经pickle序列化处理后通过连接发送出去。
    服务端接收到消息后执行反序列化处理，检查函数名是否注册，如已注册，则执行函数，最终把结果（或异常）进行pickle序列化处理后发送回去。
    """
    import pickle

    class RPCHandler:
        def __init__(self):
            self._functions = {}

        def register_function(self, func):
            self._functions[func.__name__] = func

        def handle_connection(self, connection):
            try:
                while True:
                    func_name, args, kwargs = pickle.loads(connection.recv())
                    try:
                        r = self._functions[func_name](*args, **kwargs)
                        connection.send(pickle.dumps(r))
                    except Exception as e:
                        connection.send(pickle.dumps(e))
            except EOFError:
                pass

    from multiprocessing.connection import Listener
    from threading import Thread

    def rpc_server(handler, address, authkey):
        sock = Listener(address, authkey=authkey)
        while True:
            client = sock.accept()
            t = Thread(target=handler.handle_connection, args=(client,))
            t.daemon = True
            t.start()

    def add(x, y):
        return x + y

    def sub(x, y):
        return x - y

    handler = RPCHandler()
    handler.register_function(add)
    handler.register_function(sub)

    rpc_server(handler, ('localhost', 17000), authkey=b'peekaboo')


def func9():
    """
    以简单的方式验证客户端身份

    可使用 hmac 模块实现一个握手连接来达到简单且高效的身份验证目的。
    hmac采用的身份验证算法是基于加密哈希函数的。

    总体思路:
        1. 在发起连接时，服务端将一段由随机字节组成的消息发送给客户端
        2. 客户端和服务器通过 hmac 模块以及双方事先都知道的密钥计算出随机数据的加密hash
        3. 客户端发送它计算出的摘要值(digest)给服务器
        4. 服务器对摘要值进行比较，以此来决定是否接受这个连接

    内部消息系统以及进程间通信常常会用 hmac 来验证身份。multiprocessing 库中，进程间通信的身份验证基于hmac的。
    注意: 验证某个连接和加密连接是不同的，在经过验证的连接上，后续的通信都是以明文发送的。也就是说信息能被嗅探的。
    """

    import hmac
    import os

    def client_authenticate(connection, secret_key):
        message = connection.recv(32)
        hash_ = hmac.new(secret_key, message)
        digest = hash_.digest()
        connection.send(digest)

    def server_authenticate(connection, secret_key):
        message = os.urandom(32)
        connection.send(message)
        hash_ = hmac.new(secret_key, message)
        digest = hash_.digest()
        response = connection.recv(len(digest))
        return hmac.compare_digest(digest, response)


def func10():
    """
    为网络服务增加SSL支持

    ssl 模块可以为底层的 socket 连接添加对 SSL 的支持。
    具体来说就是ssl.wrap_socket()函数可接受一个已有的socket，并为其包装一个SSL层。

    也可以对已有的服务可以通过混入类(mixin class)添加对SSL的支持。
    """
    def server_demo():
        """
        服务端为发起连接的客户端提供证书
        """
        from socket import socket, AF_INET, SOCK_STREAM
        import ssl

        KEYFILE = 'server_key.pem'  # Private key of the server
        CERTFILE = 'server_cert.pem'  # Server certificate (given to client)

        def echo_client(s):
            while True:
                data = s.recv(8192)
                if data == b'':
                    break
                s.send(data)
            s.close()
            print('Connection closed')

        def echo_server(address):
            s = socket(AF_INET, SOCK_STREAM)
            s.bind(address)
            s.listen(1)
            # Wrap with an SSL layer requiring client certs
            s_ssl = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)
            # Wait for connections
            while True:
                try:
                    c, a = s_ssl.accept()
                    print('Got connection', c, a)
                    echo_client(c)
                except Exception as e:
                    print('{}: {}'.format(e.__class__.__name__, e))

        echo_server(('', 20000))

    def client_demo():
        """
        客户端要求服务器出示自己的证书并完成验证
        """
        from socket import socket, AF_INET, SOCK_STREAM
        import ssl

        s = socket(AF_INET, SOCK_STREAM)
        s_ssl = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs='server_cert.pem')
        s_ssl.connect(('localhost', 20000))
        print(s_ssl.send(b'Hello World?'))
        print(s_ssl.recv(8192))


def func11():
    """
    在进程间传递socket文件描述符

    进程间传递文件描述符，首先要将进程连接在一起。在 UNIX 系统上可以使用 UNIX 域 socket，Windows 上可以使用命名管道。
    与其同这些底层的进程间通信机制打交道，利用 multiprocessing 模块来建立这样的连接通常会简单得多。
    一旦进程间的连接建立起来了，就可以使用 multiprocessing.reduction 模块中的 send_handle() 和 recv_handle() 函数来在进程之间传送文件描述符了。
    """
    import multiprocessing
    from multiprocessing.reduction import recv_handle, send_handle
    import socket

    def worker(in_p, out_p):
        out_p.close()
        while True:
            fd = recv_handle(in_p)
            print('CHILD: GOT FD', fd)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as s:
                while True:
                    msg = s.recv(1024)
                    if not msg:
                        break
                    print('CHILD: RECV {!r}'.format(msg))
                    s.send(msg)

    def server(address, in_p, out_p, worker_pid):
        in_p.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.bind(address)
        s.listen(1)
        while True:
            client, addr = s.accept()
            print('SERVER: Got connection from', addr)
            send_handle(out_p, client.fileno(), worker_pid)
            client.close()

    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker, args=(c1, c2))
    worker_p.start()
    server_p = multiprocessing.Process(target=server, args=(('', 15000), c1, c2, worker_p.pid))
    server_p.start()
    c1.close()
    c2.close()


def func12():
    """
    理解事件驱动型I/O

    事物驱动I/O是一种将基本的I/O操作转换成事件的技术，而我们必须在程序中去处理这种事件。

    几乎所有的事件驱动框架的工作原理都和我们给出的解决方案类似，核心部分都有一个循环来轮询 socket 的活跃性并执行响应操作。

    事件驱动型I/O的优势在于它可以在不使用线程和进程的条件下同时处理大量的连接。
    也就是说，select()调用可用来监视成百上千个socket，并且针对他们中间发生的事件作出相应。事件循环一次处理一个事件，不需要任何其他的并发原语参与。

    事件驱动型I/O的缺点在于这里并没有涉及真正的并发。如果任何一个事件处理方法阻塞了或者执行了一个耗时较长的计算，那么就会阻塞整个程序的执行进程。

    对于阻塞型或者需要长时间运行的计算，可以通过将人物发送给您单独的线程或者进程来解决。
    """
    class EventHandler:
        def file_no(self):
            raise NotImplemented('must implement')

        def wants_to_receive(self):
            return False

        def handle_receive(self):
            pass

        def wants_to_send(self):
            return False

        def handle_send(self):
            pass

    import select

    def event_loop(handlers):
        while True:
            wants_recv = [h for h in handlers if h.wants_to_receive()]
            wants_send = [h for h in handlers if h.wants_to_send()]
            can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
            for h in can_recv:
                h.handle_receive()
            for h in can_send:
                h.handle_send()


def func13():
    """
    发送和接收大型数组

    在数据密集型的分布式计算以及采用并行编程技术的应用程序中，编写需要发送和接收大型数据块的程序是很常见的。
    为了实现这个目标，需要以某种方式将数据还原为原始的字节给底层的网络接口所用。可能还需要将数据分片为较小的块。

    可以将数据进行序列化处理，将其转为字节串。但是这样通常要对数据进行拷贝，这是效率较低的做法。

    更好的方案是利用 memoryview 来实现。
    从本质来说，memoryview 是对已有数组的一层覆盖。memoryview 还可以转型为不同的类型，允许数据根据不同的方式进行解释。

    view = memoryview(arr).cast('B')
    这种形式的 memoryview 可以传递给与 socket 相关的函数。
    在底层，这些方法可以直接同内存打交道，不需要进行拷贝。

    多次send的情况，每次操作后，memoryview 都会根据已经发送或者接收的字节数做切片处理，以产生一个新的 memoryview。这个新的 memoryview 同样也是一个内存覆盖层，不会产生拷贝。
    """
    def send_from(arr, dest):
        view = memoryview(arr).cast('B')
        while len(view):
            n_sent = dest.send(view)
            view = view[n_sent:]

    def recv_into(arr, source):
        view = memoryview(arr).cast('B')
        while len(view):
            n_recv = source.recv_into(view)
            view = view[n_recv:]


if __name__ == '__main__':
    doFunc()