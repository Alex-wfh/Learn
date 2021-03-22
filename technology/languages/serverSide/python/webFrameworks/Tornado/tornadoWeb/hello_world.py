import datetime
import os
import threading
import time
import uuid
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.escape
import tornado.websocket
from typing import Optional, Awaitable
from http import HTTPStatus
from tornado.options import define, options, parse_command_line
import asyncio

define('port', default=8888, help='run on the given port', type=int)
dict_sessions = dict()
clients = dict()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        if self.get_secure_cookie('session_id') is None:
            return None
        session_id = self.get_secure_cookie('session_id').decode('utf-8')
        return dict_sessions.get(session_id)


class MainHandler(BaseHandler):
    def initialize(self, data) -> None:
        self.data = data

    @tornado.gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch('http://www.baidu.com')
        print('here come the get')
        self.write(response.body)
        time.sleep(5)

    def post(self):
        print(f'argument a: {self.get_argument("a")}')
        print(f'arguments a: {self.get_arguments("a")}')
        print(f'query argument a: {self.get_query_argument("a")}')
        print(f'query arguments a: {self.get_query_arguments("a")}')
        print(f'body argument a: {self.get_body_argument("a")}')
        print(f'body arguments a: {self.get_body_arguments("a")}')
        print(f'cookie a: {self.get_cookie("a", default=None)}')
        print(f'headers: {self._headers["date"]}')
        self.set_status(HTTPStatus.OK, reason='fck')
        self.set_header('b', 'hei')
        self.add_header('b', 'ha')
        # self.redirect('http://www.baidu.com')
        self.set_cookie('a', '7')
        self.write(f'Post {self.data}')

    def prepare(self) -> Optional[Awaitable[None]]:
        print('main handler prepare')

    def on_finish(self) -> None:
        print('main handler finish')


class EntryBaseHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write(f'Hello {name}')


class EntryHahaHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(404, reason='haha?')


class EntryHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.write(f'Entry Handler, {slug}')


class LoginHanler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        if len(self.get_argument('name')) < 3:
            self.redirect('/login')
        session_id = str(uuid.uuid1())
        dict_sessions[session_id] = self.get_argument('name')
        self.set_secure_cookie('session_id', session_id)
        self.redirect('/entry')


class MyWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument('Id')
        # self.stream.set_nodelay(True)
        clients[self.id] = {'id': self.id, 'object': self}

    def on_message(self, message):
        print(f'Client {self.id} received a message : {message}')

    def on_close(self):
        if self.id in clients:
            del clients[self.id]
        print(f'Client {self.id} is closed')

    def check_origin(self, origin):
        return True


def send_time():
    asyncio.set_event_loop(asyncio.new_event_loop())
    while True:
        for key in clients:
            msg = str(datetime.datetime.now())
            clients[key]['object'].write_message(msg)
            print(f'Write to client {key}: {msg}')
        time.sleep(1)


class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('index.html')


def make_app():
    return tornado.web.Application(
        [
            (r'/', MainHandler, {'data': 'hehe'}),
            (r'/entry', EntryBaseHandler),
            (r'/entry/haha', EntryHahaHandler),
            (r'/entry/([^/]+)', EntryHandler),
            (r'/login', LoginHanler),
            (r'/webSocket', MyWebSocketHandler),
            (r'/index', IndexHandler),
        ],
        cookie_secret='A13X_SECRET_KEY',
        login_url='/login',
        xsrf_cookies=True,
        debug=True,
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )


def main():
    threading.Thread(target=send_time).start()
    app = make_app()
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()