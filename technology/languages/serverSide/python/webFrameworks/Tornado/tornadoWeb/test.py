import tornado.ioloop
import tornado.web
from tornado.routing import HostMatches


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


if __name__ == "__main__":
    application = tornado.web.Application([
        (HostMatches("example.com"), [(r"/", MainHandler)]),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()