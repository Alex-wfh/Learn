from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado import gen
from concurrent.futures import ThreadPoolExecutor


@gen.coroutine
def coroutine_visit():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch('http://www.baidu.com')
    print(response.body[:100])


@gen.coroutine
def outer_coroutine():
    print('start call another coroutine')
    yield coroutine_visit()
    print('end of outer coroutine')


def func_normal():
    print('start to call a coroutine')
    IOLoop.current().run_sync(lambda: coroutine_visit())
    print('end of calling a coroutine')


def func_normal_running():
    print('start to call a coroutine')
    IOLoop.current().spawn_callback(coroutine_visit)
    print('end of calling a coroutine')


thread_pool = ThreadPoolExecutor(2)


def my_sleep(count):
    import time
    for i in range(count):
        time.sleep(1)


@gen.coroutine
def call_blocking():
    print('start of call_blocking')
    yield thread_pool.submit(my_sleep, 10)
    print('end of call_blocking')


@gen.coroutine
def coroutine_visit():
    http_client = AsyncHTTPClient()
    list_response = yield [
        http_client.fetch('http://www.baidu.com'),
        http_client.fetch('http://www.taobao.com'),
        http_client.fetch('http://www.jd.com')
    ]
    for response in list_response:
        print(response.body[:100])


@gen.coroutine
def coroutine_visit():
    http_client = AsyncHTTPClient()
    dict_response = yield {
        'baidu': http_client.fetch('http://www.baidu.com'),
        'taobao': http_client.fetch('http://www.taobao.com'),
        'jd': http_client.fetch('http://www.jd.com')
    }
    print(dict_response['baidu'].body[:100])


if __name__ == '__main__':
    # outer_coroutine()
    func_normal()
    # func_normal_running()
    # call_blocking()
    print('end main')