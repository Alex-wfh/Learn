from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future
from tornado.ioloop import IOLoop
from tornado import gen
import asyncio


async def asynchronous_fetch(url):
    """
    新版协程
    :param url:
    :return:
    """
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body


@gen.coroutine
def async_fetch_gen(url):
    """
    旧版协程
    :param url:
    :return:
    """
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)


def async_fetch_manual(url):
    """
    协程原理
    :param url:
    :return:
    """
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    def on_fetch(f):
        my_future.set_result(f.result().body)
    fetch_future.add_done_callback(on_fetch)
    return my_future


if __name__ == '__main__':
    body = asyncio.run(asynchronous_fetch('http://www.baidu.com'))
    print(body[:100])