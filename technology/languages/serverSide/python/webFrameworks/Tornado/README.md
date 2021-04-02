# Tornado



## 用户指南

### 介绍

Tornado 是一个 Python  web 框架和异步网络库。通过非阻塞的网络 I/O，Tornado 可扩展到数万个开放链接，非常适合 Long polling 和 WebSocket。

Tornado 大致分为四个主要部分：

* Web 框架
* HTTP 客户端和服务端实现
* 异步网络库，包含 IOLoop 和 IOStream 类
* 协程库，类似于 Python3.5 引入的原生协程。推荐 Python3.5 以前的版本使用

### 异步和非阻塞 I/O

实时 Web 功能要求每个用户都有一个长期的、一般处于空闲状态的连接。

传统 Web 服务器中，这意味着向每个用户投入一个线程，这可能非常昂贵。

为了最小化并发连接的成本，Tornado 使用单线程事件循环。这意味着所有程序代码都应该以异步和非阻塞为目标，因为同一时间只能有一个操作处于活动状态。

函数可能在某些方面是阻塞的，而在其他方面是非阻塞的。在 Tornado 中，通常在网络 I/O 的背景下讨论阻塞。当然所有类型的阻塞都应该尽量减少减小。

异步的函数在完成前返回，通常会导致某些操作在后台执行，然后在应用程序中触发某些未来操作，异步接口有以下几种类型：

* 回调参数
* 返回占位符（Future 等），称之为协程
* 交付给队列
* 回调注册表（posix信号）

Tornado 中的异步操作通常通过关键字 await 和 yield 返回占位符对象（Future）。也有些基础组件使用回调（IOLoop 等）。

相比于回调，协程允许以与同步时相同的方式组织代码，这对错误处理非常友好。

### 协程

协程是 Tornado 中编写异步代码的推荐方法。

#### 本机协程 vs 装饰器协程

Python3.5 引入了 async 和 await 关键字，通常把使用这些关键字的函数称为本机协程。Python3.5 以前使用 tornado.gen.coroutine 使用协程。在可能的情况下使用本机协程。两种协程间差异如下：

* 本机协程
  * 更快
  * 可通过 await for 和 async with 使某些代码实现更简单
  * 只有当 await 或 yield 方法时才开始调用，而装饰器协程被调用时就会开始在后台执行
* 装饰器协程
  * 在 concurrent.futures 包的基础上增加额外功能，允许 executor.submit 的结果直接被 yield。本机协程需要通过 IOLoop.run_in_executor 返回结果。
  * 可直接返回由多个协程结果组成的 list 或 dict。本机协程需要通过 tornado.gen.multi 完成类似需求。
  * 可通过注册表方式使第三方包支持协程。本机协程需要通过 tornado.gen.convert_yielded。
  * 总是返回 Future 对象。本机协程返回 awaitable 对象而并非 Future对象。Tornado 中两者可互相转换。

#### 协程工作原理

调用时返回一个 awaitable 对象，而不是运行到完成。运行完成时，将结果加入 awaitable。

#### 协程使用方法

协程不会正常触发异常，而是捕获异常并存入 awaitable 对象中，这到该对象被 yield。

绝大部分情况，只有协程方法才能调用其他协程方法。而且需要使用 await 或者 yield 调用。继承某个类并重写其方法时也需要注意该方法是否支持协程。

对于不需要等待返回的协程，建议使用 IOLoop.spawn_callback。这样如果协程执行错误，IOLoop 会记录异常。

通常会在 main 方法中启动 IOLoop，执行协程，然后通过 IOLoop.run_sync 停止 IOLoop。

#### 协程模式

* 调用阻塞方法

  最简单的方法是使用 tornado.ioloop.IOLoop.run_in_executor，该方法返回与协程兼容的 Future。

  ```python
  async def call_blocking():
      await IOLoop.current().run_in_executor(None, blocking_func, args)
  ```

* 平行调用多协程

  tornado.gen.multi 方法支持由 Future 组成的 list 或 dict，并同时等待它们。

  ```python
  from tornado.gen import multi
  
  async def parallel_fetch(url1, url2):
      resp1, resp2 = await multi([http_client.fetch(url1),
                                  http_client.fetch(url2)])
  
  async def parallel_fetch_many(urls):
      responses = await multi ([http_client.fetch(url) for url in urls])
      # responses is a list of HTTPResponses in the same order
  
  async def parallel_fetch_dict(urls):
      responses = await multi({url: http_client.fetch(url)
                               for url in urls})
      # responses is a dict {url: HTTPResponse}
  ```

  装饰器协程中，直接 yield list 或 dict 即可。

* 交叉执行多协程

  有时需要保存一个 Future，而不是直接 yield 它，这样就可以在协程开始执行前执行其他操作。

  ```python
  from tornado.gen import convert_yielded
  
  async def get(self):
      # convert_yielded() starts the native coroutine in the background.
      # This is equivalent to asyncio.ensure_future() (both work in Tornado).
      fetch_future = convert_yielded(self.fetch_next_chunk())
      while True:
          chunk = yield fetch_future
          if chunk is None: break
          self.write(chunk)
          fetch_future = convert_yielded(self.fetch_next_chunk())
          yield self.flush()
  ```

  针对该需求，装饰器协程实现起来更容易。

  ```python
  @gen.coroutine
  def get(self):
      fetch_future = self.fetch_next_chunk()
      while True:
          chunk = yield fetch_future
          if chunk is None: break
          self.write(chunk)
          fetch_future = self.fetch_next_chunk()
          yield self.flush()
  ```

* 循环

  本机协程中，可以使用 async for。装饰器协程中很难处理循环，需要将循环条件与访问结果分开。

* 后台运行

  通常协程会使用 while True 和 tornado.gen.sleep，实现周期化执行的需求。

### 队列

tornado.queue 模块为协程实现了生产中/消费者模式，类似于标准库的 queue 模块。

### Tornado Web 应用程序结构

Tornado Web 应用通常包含：

* 一个 main() 方法用来启动服务。
* 一个用来将请求路由到处理程序的 tornado.web.Application 对象。
* 一个或多个 tornado.web.RequestHandler 的子类作为处理程序。

#### Application 对象

Application 对象负责全局配置，包括将请求映射到处理程序的路由表。

路由表是一个由 tornado.web.URLSpec 对象组成的 list 或 tuple。URLSpec 对象至少包含一个正则表达式和一个 handler 类。请求会路由到第一个匹配正则表达式对应的 handler 类。如果正则表达式包含捕获组，那么这些组是路径参数，参数会传给对应 handler 类中对应的 HTTP 谓语方法。如果 URLSpec 的第三个参数传入了一个 dict，那么这个字典将会作为 handler 类初始化的变量，传给 initialize 方法。第四个参数是 name，如果传入则会将该 URLSpec 对象命名，这个名称可以通过 self.reverse_url 方法使用。

Application 还支持很多关键字，可用于启动可选功能和定义其行为。

####tornado.web.RequestHandler 的子类

Tornado Web 应用程序的大部分工作都在 RequestHandler 类的子类中完成。处理程序的主入口是以 HTTP 方法命名的方法（例如 get(), post() 等）。为了能够针对不同的 HTTP 方法做出响应，每个处理程序须定义一或多个此类方法。处理程序可通过 self.render，self.write 这类的方法进行输出。

通常可以定一个继承 RequestHandler 的 BaseHandler 做为公共的基础处理程序，其中重写一些通用方法，例如 self.write_error ，self.get_current_user 等。其他处理程序再继承该基础处理程序。

#### 处理请求输入

可通过 self.request 方法当前请求的对象，这是一个 tornado.httputil.HTTPServerRequest 类的对象。也可通过 self.get_query_argument(s)，self.get_body_argument(s) 这类的方法获取输入。

#### 重写 RequestHandler 方法

Application 路由器请求匹配成功后，会执行以下操作：

1. 创建一个 RequestHandler 子类
2. initialize()
3. prepare()
4. HTTP 谓语方法命名的方法
5. on_finish()

经常被重写的 RequestHandler 方法：

* write_error()
* on_connection_close()
* get_current_user()
* get_user_local()
* set_default_headers()

#### 异常处理

如果处理程序抛出异常，Tornado 会调用 RequestHandler.write_error 生成一个异常页。tornado.web.HTTPError 可以用来定制特殊的异常码，其他异常都报500。

#### 重定向

Tornado 支持两种重定向方式：

* tornado.web.RequestHandler.redirect()

  适合临时重定向，有条件重定向。可根据请求内容决定是否重定向以及如何重定向。

* class tornado.web.RedirectHandler

  适合永久重定向。不会随请求内容变化。

#### 异步

处理程序的 prepare() 和 谓语方法可以通过形成实现异步。

### 模版和 UI

tornado.web.RequestHandler.render() 可以使用 tornado 的模版。有以下几个常用功能：

* template_path
* compiled_template_cache
* {{ }}
* {% %}
* 模版内支持一些方法，例如时间处理、JSON解析、国际化等。

### 安全性和身份验证

#### cookie

可以通过 get_cookie 和 set_cookie 操作 cookie，但这样不安全，客户端很容易伪造 cookie。

可通过 cookie_secret，get_secure_cookie，set_secure_cookie 实现安全 cookie。这个 cookie 能保证完整性但是不保密。

Tornado 还支持通过多个 cookie_secret 实现滚动的安全 cookie。

#### 身份验证

重写 tornado.web.RequestHandler 的 get_current_user() 方法可实现用户认证。handler 中调用 self.current_user 可获取当前用户。@tornado.web.authenticated 可使方法做用户登录判断，如果用户未登录，将重定向到 login_url。tornado.auth 可以继承第三方登录认证。

#### 防跨域

xsrf_cookies=True，请求需要从 cookie 中获取 _xsrf 并将其添加到请求参数中。

#### DNS 伪造

可向 Application 路由的第一项插入一个 HostMatches，限制某些特定 url 传入的请求。

### 运营和部署

Tornado 提供了自己的 httpserver，所以不需要配置 wsgi 来查找应用，而是通过 main() 方法启动应用。配置操作系统或进程管理器执行这个 main() 方法以启动服务。

```python
def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
```

#### 进程和端口

由于 Python gil，需要运行多个 Python 进程以充分利用多个 CPU。最好每个 CPU 运行一个进程。

Tornado 内置了一个多进程模式，可一次启动多个进程。

```python
def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    tornado.ioloop.IOLoop.current().start()
```

这是多进程共享一个端口的最简单方法，但存在一些弊端。无法实现无缝重启，日志混乱。所以通常会启动多个进程监听多个端口，然后通过负载监听一个端口，并将请求转发到进程监听的端口上。

#### 静态文件和积极的文件缓存

通过 Application 的关键字参数 static_path 指定静态文件目录。可通过给静态文件增加版本号的方式使浏览器积极地缓存静态文件，并在版本好不同时重新请求。tornado.web.static_url 方法可简单的实现该功能，static_url 方法也可在 tornado 模版中使用。

#### 自动加载和调试模式

通过 Application 的关键字参数 debug=True 进入调试模式。此模式涉及以下几个功能：autoreload=True, compiled_template_cache=False, static_hash_cache=False, server_traceback=True。autoreload=True 与多进程不兼容。可通过命令行启动命令指定运行模式。

```shell
python -m tornado.debug myserver.py
```



## Web Framework

### tornado.web - RequestHandler & Application

提供一个具有异步支持的web框架。

#### Thread-safety

非线程安全，write(), finish(), flush() 这类方法必须由主线程调用。如果使用多线程，在完成请求之前，需要使用 IOLoop.add_callback 将控制权转移回主线程。或者通过 IOLoop.run.run_in_executor 使用子线程，并确保 executor 中的回调不引用 Tornado 对象。

* IOLoop.add_callback()
* IOLoop.run_in_executor()

#### RequestHandler

HTTP Request Handeler 基类，子类需包含至少一个 Entry points，子类不要重写 init 方法。

##### Entry Points

1. initialize()
2. prepare()
3. HTTP verb methods()
4. on_finish()

##### Input

* request
* get_argument(s)
* get_query_argument(s)
* get_body_argument(s)
* path_(kw)args
* data_received

##### Output

* set_status()
* set_header()
* add_header()
* clear_header()
* set_default_headers()
* write()
* flush()
* finish()
* render()
* render_string()
* get_template_namespace()
* redirect()
* send_error()
* write_error()
* clear()
* render_linked/embed_js/css()

##### Cookies

* cookies
* get_cookie()
* set_cookie()
* clear_cookie()
* clear_all_cookies()
* get_secure_cookie()
* get_secure_cookie_key_version()
* set_secure_cookie()
* create_signed_value()
* tornado.web.MIN/MAX_SUPPORTED_SIGNED_VALUE_VERSION
* tornado.web.DEFAULT_SIGNED_VALUE(_MIN)_VERSION

##### Other

* application
* check_xsrf_cookie()
* create_template_loader()
* current_user
* detach()
* get_current_user()
* get_login_url()
* get_status()
* get_template_path()
* get_user_locale()
* locale
* settings
* static_url()
* xsrf_token

#### Application configuration

```python
class tornado.web.Application(handlers: Optional[List[Union[Rule, Tuple]]] = None, 
                              default_host: Optional[str] = None, 
                              transforms: Optional[List[Type[OutputTransform]]] = None, 
                              **settings)
```

通过Application创建的实例可直接使用，也可以入参形式传给 HTTPServer

```python
application.listen(8888)

http_server = httpserver.HTTPServer(application)
http_server.listen(8888)
```

Application 类的构造器可接收 Rule 组成的列表，或者类似 Rule 列构造器的入参列表`(matcher, target, [target_kwargs], [name])`。默认的 matcher 是 PathMathes，也可显示替换为 HostMatches。

接收请求时，按顺序便利列表，选择第一个匹配的 Handler。

* listen()
* add_handlers()
* tornado.web.URLSpec()
  * pattern
  * handler
  * kwargs
  * name

##### settings

* debug, autoreload, compiled_template_cache, static_hash_cache, serve_traceback
* default_handler_class, default_handler_args
* ui_modules
* cookie_secret
* key_version
* login_url
* xsrf_cookies
* xsrf_cookie_version
* template_path
* static_path
* static_url_prefix

#### Decorators

* tornado.web.authenticated()

#### Everything else

* exception tornado.web.HTTPError()
* exception tornado.web.Finish()
* exception tornado.web.MissingArgumentError()
* class tornado.web.UIModule
* class tornado.web.ErrorHandler
* class tornado.web.FallbackHandler
* class tornado.web.RedirectHandler
* class tornado.web.StaticFileHandler

### tornado.template

将模版编译为原生Python

* {% %}
* {{ }}
* {% extends *filename* %}
* {% block *name* %}...{% end %}
* {% for *var* in *expr* %}...{% end%}
* {% if *condition* %}...{% elif *condition* %}...{% else %}...{% end %}
* {% include *filename* %}
* {% set *x* = *y* %}
* {% try %}...{% except %}...{% else %}...{% finally %}...{% end %}
* {% while *condition* %}...{% end %}

#### template 包含的类

* class tornado.template.Template
* class tornado.template.BaseLoader
* class tornado.template.Loader
* class tornado.template.DictLoader
* exception tornado.template.ParseError()

### tornado.routing

实现路由功能，tornado.web.Application 类就是继承自 tornado.routing.Router，Application 可直接使用，也可通过 Router 增加灵活性。可通过 Router 的子类 RuleRouter 实现最大程度的自定义。

Router 类继承自 tornado.httputil.HTTPServerConnectionDelegate 类，这意味着 Router 的实例可以作为 HTTPServer 类构造函数的 request_callback （第一个）入参。

Router 的子类必须实现 find_handler 方法，该方法提供一个 HTTPMessageDelegate 实例，用来处理 request。

Router 的主要功能是提供请求到 HTTPMessageDelegate 实例的映射关系

如果想路由到 RequestHandler 实例，我们需要创建 Application 实例，get_handler_delegate 提供了通过请求和 RequestHandler 创建 HTTPMessageDelegate 的便捷方法。

ReversibleRouter 继承自 Router 提供反向代理能力，Application 即是 ReversibleRouter 的子类。

RuleRouter 和 ReversibleRuleRouter 分别继承自 Router 和 ReversibleRouter 用来创建基于规则的路由配置。

RuleRouter 和 ReversibleRuleRouter 的构造器需要入参 rules，是由 Rule 类的实例组成的列表。通过 Rule 类创建实例需要 Matcher 参数，用来描述请求与目标匹配规则。

* class tornado.routing.Router
* class tornado.routing.ReversibleRouter
* class tornado.routing.RuleRouter
* class tornado.routing.ReversibleRuleRouter
* class tornado.routing.Rule
* class tornado.routing.Matcher
  * class tornado.routing.AnyMatches
  * class tornado.routing.HostMatches
  * class tornado.routing.DefaultHostMatches
  * class tornado.routing.PathMatches
* class tornado.routing.URLSpec

### tornado.escape

* tornado.escape.xhtml_escape(), tornado.escape.xhtml_unescape()
* tornado.escape.url_escape(), tornado.escape.url_unescape()
* tornado.escape.json_encode(), tornado.escape.json_decode()
* tornado.escape.utf8()
* tornado.escape.to_unicode()
* tornado.escape.recursive_unicode()

### tornado.locale

* tornado.locale.get()
* tornado.locale.set_default_locale()
* tornado.locale.load_translations()

### tornado.websocket

##### class tonado.websocket.WebSocketHandler

WebSockets不是标准的HTTP连接。“握手”是HTTP，但握手之后，协议是基于消息的。因此，大多数Tornado HTTP设施在这种类型的处理程序中不可用。

#### Event handlers

* WebSocketHandler.open()
* WebSocketHandler.on_message()
* WebSocketHandler.on_close()
* WebSocketHandler.select_subprotocol(), WebSocketHandler.selected_subprotocol()
* WebSocketHandler.on_ping()

#### Output

* WebSocketHandler.write_message()
* WebSocketHandler.close()

#### Configuration

* WebSocketHandler.check_origin()
* WebSocketHandler.get_compression_options()
* WebSocketHandler.set_nodelay()

#### Others

* WebSocketHandler.ping()
* WebSocketHandler.on_pong()
* exception tornado.webSocket.WebSocketClosedError()

#### Client-side support

* tornado.webSocket.websocket_connect()
* class tornado.webSocket.WebSocketClientConnection



## HTTP servers and clients

### tornado.httpserver - Non-blocking HTTP server

通常，应用程序与 tornado.httpserver.HTTPServer 类没有直接交互，只有在程序启动时，tornado.web.Application.listen() 进行的间接交互。

* class tornado.httpserver.HTTPServer

  三种初始化模式

  * listen - 单进程
  * bind - 多进程
  * add_sockets - 高定制化模式

### tornado.httpclient - Asynchronous HTTP client

* simple_httpclient vs curl_httpclient

  * simple_httpclient 为默认方法
  * curl_httpclient 包含额外的特征，支持HTTP代理，支持某些特定的网络接口
  * curl_httpclient 更容易实现非常规的HTTP请求
  * curl_httpclient 更快
  * curl_httpclient 需要最新版本的 libcurl 和 pycurl

  通过在启动时调用 AsyncHTTPClient.configure 选择 curl_httpclient。

  ```python
  AsyncHTTPClient.configure("tornado.httpclient.CurlAsyncHTTPClient")
  ```

#### HTTP client interfaces

* class tornado.httpclient.HTTPClient, class tornado.httpclient.AsyncHTTPClient
  * fetch()
  * close()
  * classmethod configure()

#### Request objects

* class tornado.httpclient.HTTPRequest
  * url
  * method
  * headers
  * body

#### Response objects

* class tornado.httpclient.HTTPResponse
  * request
  * code
  * reason
  * headers
  * body
  * error

#### Exceptions

* exception tornado.httpclient.HTTPClientError()
  * code
  * response
* exception tornado.httpclient.HTTPError()

#### Command-line interface

```shell
# Fetch the url and print its body
python -m tornado.httpclient http://www.google.com

# Just print the headers
python -m tornado.httpclient --print_headers --print_body=false http://www.google.com
```

#### Implementations

* class tornado.simple_httpclient.SimpleAsyncHTTPClient
* class tornado.curl_httpclient.CurlAsyncHTTPClient

### tornado.httputil - Manipulate HTTP headers and URLs

HTTP 相关的通用代码，服务端、客户端都可使用。

该模块也定义了 HTTPServerRequest 类，该类通过 tornado.web.RequestHandler.request 暴露给用户使用。

* class tornado.httputil.HTTPHeaders

  维护 HTTP Header 的字典。

  * add()
  * get_list()
  * get_all()
  * parse_line()
  * classmethod parse()

* class tornado.httputil.HTTPServerRequest

  HTTP Request 类。

* exception tornado.httputil.HTTPInputError

* exception tornado.httputil.HTTPOutputError

* class tornado.httputil.HTTPServerConnectionDelegate

  tornado.httpserver.HTTPServer 的父类之一

  * start_request()

    新request创建后，server 调用此方法。

  * on_close()

    链接关闭后，此方法被调用。

* class tornado.httputil.HTTPMessageDelegate

  处理 HTTP request 和 response

  * headers_received()

    接收并解析 HTTP headers 时调用

  * data_received()

    接收数据块时调用

  * finish()

    接收最后一个数据块后调用

  * on_connection_close()

    request 未完成的情况下，链接关闭时调用。

* class tornado.httputil.HTTPConnection

  Application 通过该方法写 responses

  * write_headers()

    写入 headers

  * write()

    写入 body

  * finish()

    body写入完成

* tornado.httputil.url_concat()

  拼接 url 和 入参

* class tornado.httputil.HTTPFile

  表示通过表单上传的文件

* tornado.httputil.parse_body_arguments()

  解析表单提交的 body

* tornado.httputil.parse_multipart_form_data()

  解析 multipart/form-data 提交的 body

* tornado.httputil.format_timestamp()

  格式化时间戳

* class tornado.httputil.RequestStartLine

  `RequestStartLine(method, path, version)` 根据 method, path, version 创建 RequestStartLine，RequestStartLine 是 tornado.httputil.HTTPServerRequest 的入参之一。

* tornado.httputil.parse_request_start_line()

  根据字符串解析生成 RequestStartLine。

* class tornado.httputil.ResponseStartLine

  `ResponseStartLine(version, code, reason)`

* tornado.httputil.parse_response_start_line()

* tornado.httputil.encoding_username_password()

  以 HTTP 身份验证格式对 用户名/密码 对进行编码

* tornado.httputil.split_host_and_port()

  分割 netloc，返回 (host, port)

* tornado.httputil.qs_to_qsl()

  输入 qs，返回 items() 的生成器。

* tornado.httputil.parse_cookie()

  将 cookie 解析为字典

### tornado.http1connection

HTTP/1.x 的服务端和客户端的实现。

* class tornado.http1connection.HTTP1ConnectionParameters

  HTTP1Connection 和 HTTP1ServerConnection 

* class tornado.http1connection.HTTP1Connection

  实现 HTTP/1.x 协议

  可以单独为客户端服务，或者通过 HTTP1ServerConnection 为服务端服务

  * read_response()
  * set_close_callback()
  * detch()
  * set_body_timeout()
  * set_max_body_size()
  * write_headers()
  * write()
  * finish()

* class tornado.http1connection.HTTP1ServerConnection

  HTTP/1.x server

  * close()
  * start_serving()



## Asynchoronous networking

### tornado.ioloop - Main event loop

非阻塞套接字的 I/O 事务循环。

IOLoop 是 asyncio 事件循环的包装器，应用程序可直接使用 IOLoop，也可使用基础的 asyncio 事件循环（为了与旧版本兼容）。推荐使用 IOLoop。

典型的应用通过 IOLoop.current 类方法访问单个 IOLoop 对象。IOLoop.start() 方法通常在 main() 方法的最后调用。

非典型的应用也可能使用多个 IOLoop，例如多线程（每个线程一个 IOLoop），或单元测试时。

#### IOLoop.objects

* class tornado.ioloop.IOLoop

  默认情况下，新建的 IOLoop 会成为 current IOLoop，除非已经有 current IOLoop。可以使用 IOLoop 构造函数的 make_current 参数控制此行为。make_current=True，新建的 IOLoop 会尝试成为 current IOLoop，如果已存在 current IOLoop，会报错。make_current=False，新建的 IOLoop 不会尝试成为 current IOLoop。

  通常，IOLoop 无法派生，也无法在进程间共享。使用多进程时，每个进程都该创建自己的 IOLoop，这意味着依赖 IOLoop 的任何对象都必须在子进程中创建。建议，任何启动进程的操作都应尽早创建 IOLoop。

#### Running an IOLoop

* static IOLoop.current()

  返回 current IOLoop，有则返回，无则创建。

* IOLoop.make_current()

  使 IOLoop 成为当前线程的 IOLoop。IOLoop 启动时会自动成为当前线程的 IOLoop，但有时也会在启动 IOLoop 之前显式调用 make_current，这样启动时就能找到正确的 IOLoop。

* static IOLoop.clear_current()

  IOLoop 与当前线程解绑，主要用于测试。

* IOLoop.start()

  启动 I/O 循环，保持运行，直到某个回调调用 stop()。

* IOLoop.stop()

  停止 I/O 循环，如果循环未运行，下次 start() 方法会直接返回。

* IOLoop.run_sync()

  开始 IOLoop，运行给定的函数，并停止循环。给定函数必须返回可等待对象或 None。如果函数返回可等待对象，IOLoop 将会一直等待解决。

* IOLoop.close()

  关闭 IOLoop，释放所有使用的资源。主要用于测试。

#### I/O events

* IOLoop.add_handler()

  登记 event 和 handler 的绑定关系。

* IOLoop.update_handler()

  更新 event 和 handler 的绑定关系。

* IOLoop.remove_handler()

  停止时间监听。

#### Callbacks and timeouts

* IOLoop.add_callback(), IOLoop.spawn_callback()

  下一次 I/O 循环中增加回调方法。在任何线程中调用都是安全的。不能用于信号处理程序。

* IOLoop.add_callback_from_signal()

  用于信号处理程序。

* IOLoop.add_future()

  在 IOLoop 上安排 Future 结束的回调。

* IOLoop.add_timeout()

  为 IOLoop 设置等待的超时时间。

* IOLoop.remove_timeout()

* IOLoop.call_at()

  在某一时间执行回调。

* IOLoop.call_later()

  延迟某时间执行回调。

* IOLoop.run_in_executor()

  在 concurrent.futures.Executor。如果  executor 是 None，IOLoop 使用默认的 executor。

* IOLoop.set_default_executor()

  设置 IOLoop 默认的 executor。

* IOLoop.time()

  根据 IOLoop 的时钟返回当前时间戳。

* class tornado.ioloop.PeriodicCallBack

  设置定期调用指定的回调。注意这里的时间参数是以毫秒为单位的。

### tornado.iostream - Convenient wrappers for non-blocking sockets

读写非阻塞文件和套接字的常用类。

####Base class

* class tornado.iostream.BaseIOStream

  支持非阻塞的 write() 方法以及一套 read_*() 方法。

#### Main interface

* BaseIOStream.write()

  异步将给定的数据写入流。

* BaseIOStream.read_bytes(), BaseIOStream.read_into(), BaseIOStream.read_util(), BaseIOStream.read_regex(), BaseIOStream.read_until_close()

  异步读取。

* BaseIOStream.close()

  关闭流。

* BaseIOStream.set_close_callback()

  流关闭时调用给定回调方法。

* BaseIOStream.closed()

  判断流是否关闭。

* BaseIOStream.reading(), BaseIOStream.writing()

  判断流是否正在读取，写入。

* BaseIOStream.set_nodelay()

  设置流无延迟。

#### Methods for subclasses

* BaseIOStream.fileno()

  返回流的文件描述符。

* BaseIOStream.close_fd()

  关闭流的底层文件。

* BaseIOStream.write_to_fd()

  将数据写入底层文件。

* BaseIOStream.read_from_fd()

  从底层文件中读取数据。

* BaseIOStream.get_fd_error()

  返回有关底层文件的基础信息。

#### Implementations

* class tornado.iostream.IOStream

  基于套接字的 IOStream 实现。这个类支持从 BaseIOStream 继承的读写方法，还增加了一个 connect 方法。

  这个类的构造方法需要传入 socket，这个 socket 既可以是已连接的，也可以是未连接的。

  * connect()

    将 socket 以非阻塞的方式连接到远程地址。通过未连接的 socket 构造 IOStream 类时可调用该方法。

    与 socket.connect 一样，都接收 (ip, port) 的元组。支持传入 url，但是会以同步方式解析 url。推荐先利用 TCPClient 中提供的异步 DNS 方法先将 url 解析为 host，再进行 connect。

  * start_tls()

    将 IOStream 转换为 SSLIOStream。可以以明文方式开始，之后转换为 SSL 方式。

    只能在流没有未完成的读写操作且 iostream 的缓冲区没有任何数据时才能执行。

* class tornado.iostream.SSLIOStream

  用于非阻塞 SSL 套接字的读写。

  * wait_for_handshake()

    等待 SSL 握手完成。每个流只能调用一次。

* class tornado.iostream.PipeIOStream

  管道 IOStream 实现。管道 IOStream 通常是单向的，所以 PipeIOStream 可用于读或写，但不能同时用于两者。

#### Exceptions

* exception tornado.iostream.StreamBufferFullError

  缓冲区已满

* exception tornado.iostream.StreamClosedError

  流已经关闭

* exception tornado.iostream.UnstatisfiableReadError

  无法满足读取要求

### tornado.netutil - Miscellaneous network utilities

各种各样的网络相关的常用功能代码。

* tornado.netutil.bind_socket()

  创建绑定到给定地址和端口的监听套接字。

* tornado.netutil.bind_unix_socket()

  创建监听 UNIX 套接字。

* tornado.netutil.add_accept_handler()

  为 sock 上的新连接增加对应的 IOLoop 事件。

* tornado.netutil.is_valid_ip()

  判断字符串是否符合 IP 的格式。

* class tornado.netutil.Resolver

  可配置的异步 DNS 解析器接口。

  * resolve()

    请求地址并异步返回结果。

  * close()

    关闭 Resolver，释放资源。

* class tornado.netutil.DefaultExecutorResolver

  使用基本的 IOLoop.run_in_executor 实现 resolve 方法。

* class tornado.netutil.ExecutorResolver

  使用 concurrent.futures.Executor 实现，多线程无阻塞，比 ThreadedResolver 支持更多配置。

* class tornado.netutil.BlockingResolver

  阻塞解析器实现。

* class tornado.netutil.ThreadedResolver

  多线程无阻塞解析器实现。

* class tornado.netutil.OverrideResolver

  修改本地 DNS 转发的解释器。

* tornado.netutil.ssl_options_to_context()

  将 ssl_options 字典转换为 SSLContext 对象。

* tornado.netutil.ssl_wrap_socket()

  将 socket 包装为 ssl.SSLSocket

### tornado.TCPClient - IOStream connection factory

非阻塞的 TCP 连接工厂。

#### class tornado.tcpclient.TCPClient

连接到给定的主机和端口，异步返回一个 IOStream。

通过 source_ip 入参，在创建连接时指明源 IP 地址。如果用户需要处理和使用特殊的借口，则需要在 tornado 之外进行，因为这很大程度上取决于平台。

如果 timeout 指定的事件前未完成处理，则会抛出 TimeoutError。

通过 source_port 可以指定特定的源端口。

### tornado.tcpserver - Basic IOStream, based TCP server

非阻塞单线程 TCP 服务器。

#### class tornado.tcpserver.TCPServer

继承 TCPServer 的子类需要重写 handle_stream 方法。

通过构造函数的 ssl_options 入参，传入 ssl.SSLContext 对象，可支持 SSL 方式流量。

##### TCPServer 初始化模式

* listen，单进程启动

  ```python
  server = TCPServer()
  server.listen(8888)
  IOLoop.current().start()
  ```

* bind/start，多进程启动

  ```python
  server = TCPServer()
  server.bind(8888)
  server.start(0)
  IOLoop.current().start()
  ```

* add_sockets，更复杂，更灵活的启动配置

  ```python
  sockets = bind_sockets(8888)
  tornado.process.fork_process(0)
  server = TCPServer()
  server.add_sockets(sockets)
  IOLoop.current().start()
  ```

##### listen()

开始接收给定端口上的连接，可以多次调用以监听多个端口。不需要调用 TCPServer.start 方法，但是仍然需要启动 IOLoop。

##### add_sockets()

使服务开始接收给定 sockets 的连接。

sockets参数是套接字对象（例如由bind_sockets返回的那些对象）的列表。 add_sockets通常与该方法和tornado.process.fork_processes结合使用，以更好地控制多进程服务器的初始化。

##### add_socket()

add_sockets() 的单例版本。

##### bind()

将 server 与给定的地址和接口绑定。要启动服务器，可以调用 start 方法。如果想在单进程中运行，可以调用 listen 作为绑定和开始监听的快捷方式。bind 方法可以被调用多次，用来监听多个接口或端口。

##### start()

在 IOLoop 中开始服务。默认情况下，在此方法中启动服务，并且不派生任何子进程。如果 num_processes 为空或者0，tornado 将检测检测计算机上可用的内核数，并派生等量的子进程。由于是多进程，程序间没有共享的内存。debug 模式与 多进程不兼容。只有全部进程都调用 start 后，才能创建或引用 IOLoop。

##### stop()

停止监听新连接，服务停止后，当前正在进行的请求可能会继续执行。

##### handle_stream()

重写连接传入的新 IOStream。可能是协程，会异步记录异常日志，该协程不会阻塞传入的连接。如果此 TCPServer 支持 SSL，handle_stream 方法能够在 SSL 握手完成之前调用。



## Coroutines and concurrency

### tornado.gen - Generator-based coroutines

基于生成器的协程实现。

基于生成器和装饰器的 tronado.gen 方法是 async 协程的前身。Python3.5 及以后使用 async，如需兼容 3.5 以前版本，推荐使用 tornado.gen。

协程提供了比回调更容易的异步环境中的工作方法。协程代码在技术上是异步的，但它以生成器形式存在，而不是独立的函数回调。

```python
class GenAsyncHandler(RequestHandler):
  	@gen.coroutine
    def get(self):
      	http_client = AsyncHTTPClient()
        response = yield http_client.fetch('http://example.com')
        do_something_with_response(response)
        self.render('template.html')
```

Python 中的异步函数返回一个 Awaitable 或 Future。yield 这个对象返回其结果。也可以直接 yield 一个 yieldable 对象的列表或字典。它们会同时启动并运行，完成后会返回结果的列表或字典。

#### Decorators

* tornado.gen.coroutine()

  异步生成器的装饰器。为了与旧版 Python 兼容，协程也可抛出异常 tornado.gen.Return 作为返回。

  使用此装饰器的函数将返回 Future 对象。

  当异常发生在协程内时，异常信息将储藏在 Future 对象中。如果不主动检查协程返回的 Future 对象，异常将被忽略。

* exception tornado.gen.Return()

  特殊的异常类，可以从协程中返回值。如果协程发生异常，则返回 tornado.gen.Return() 中的值。Return() 也可以不带任何值。

#### Utility functions

* tornado.gen.with_timeout()

  将 Future 或其他 yieldable 对象包装在 timeout 中。如果 Future 在超时时间内未执行完成，则出发 tornado.util.TimeoutError 异常。触发 TimeoutError 后 Future 不被取消，它可以被重新使用。

* tornado.gen.sleep()

  等待给定秒数后再执行 Future。这里的等待与 time.sleep() 不同，是非阻塞的。

* class tornado.gen.WaitIterator

  提供一个迭代器，在 awaitables 执行完成时 yield 其结果。

  类似于 `result = yield [*awaitables]`，但是这种方式暂停协程，等待全部 awaitables 执行完成，然后返回其结果。如果其中一个 awaitable 报错，则抛出异常，然后丢弃全部结果。

  而 WaitIterator 中，每个 awaitables 执行完毕直接返回，而且当其中一个 awaitable 报错时，不会影响其他的。由于执行完毕直接返回，所以返回的顺序与输入的顺序不一致，可使用 WaitIterator.current_index 解决这个问题。

  ```python
  wait_iterator = gen.WaitIterator(awaitable1, awaitable2)
  while not wait_iterator.done():
      try:
          result = yield wait_iterator.next()
      except Exception as e:
          print("Error {} from {}".format(e, wait_iterator.current_future))
      else:
          print("Result {} received from {} at {}".format(
              result, wait_iterator.current_future,
              wait_iterator.current_index))
  ```

  Python3.5 之后，WaitIterator 可支持 async 迭代协议。所以可通过 async for 来使用。

  ```python
  	async for result in gen.WaitIterator(future1, future2):
      print("Result {} received from {} at {}".format(
          result, wait_iterator.current_future,
          wait_iterator.current_index))
  ```

  * done()

    如果迭代器没有更多的结果则返回 True。

  * next()

    返回迭代器的下一个结果。

* tornado.gen.multi()

  并行运行多个异步操作。children 入参是一个由 yieldable 对象组成的 list 或 dict。返回一个由结果的并行结果组成的新的 yieldable 对象。下面两段代码是等效的：

  ```python
  results = yield multi(list_of_futures)
  ```

  ```python
  results = [yield future for future in list_of_futures]
  ```

  如果任何子协程报错，multi() 会抛出第一个，记录其他的。

  通常以 yield 方式使用的协程执行者会自动运行该方法，所以不需要主动调用。但是以 await 方式使用的携程需要主动调用该方法。

  multi 取消 children Future 的返回并不会真正将其终止。

* tornado.gen.multi_future()

  并行等待多个异步 Future。6.0 开始此方法与 tornado.gen.multi() 完全相同。

* tornado.gen.convert_yielded()

  将 yieldable 对象转换为 Future。

* tornado.gen.maybe_future()

  将任意对象转化为 Future。

* tornado.gen.is_coroutine_function()

  判断方法是否是协程方法。

* tornado.gen.moment()

  产生一个特殊的对象，以允许 IOLoop 运行。通常用于长期运行的协程立刻执行某个指定的 Future。

### tornado.locks - Synchronization primitives

使用与标准库提供给线程的同步语法类似的语法来处理协程。这些类的作用和用法与标准库的 asyncio 中提供的类很相似。

注意，这些语法不是线程安全的，无法替代标准库中的线程同步语法。它们用于处理单线程应用中的协程，而不是保护多线程应用中的共享对象。

* Condition
* Event
* Semaphore
* BoundSemaphore
* Lock

#### Condition - class tornado.locks.Condition

condition 可使一个或多个 awaitable 阻塞。类似于 threading.Condition，但是不需要获取和释放基础锁。

通过使用 condition，协程可以等待其他协程的通知。

```python
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Condition

condition = Condition()

async def waiter():
    print("I'll wait right here")
    await condition.wait()
    print("I'm done waiting")

async def notifier():
    print("About to notify")
    condition.notify()
    print("Done notifying")

async def runner():
    # Wait for waiter() and notifier() in parallel
    await gen.multi([waiter(), notifier()])

IOLoop.current().run_sync(runner)
```

* wait()

  等待通知。

* notify()

  唤醒 n 个阻塞协程。

* notify_all()

  唤醒全部阻塞协程。

#### Event - class tornado.locks.Event

Event 会阻塞协程，直到内部标识被设置为 True。一旦事件被设置，再次调用 wait() 方法不会阻塞协程，需要调用 clear() 方法清除 Event，才能通过 wait() 方法重新阻塞。

```python
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Event

event = Event()

async def waiter():
    print("Waiting for event")
    await event.wait()
    print("Not waiting this time")
    await event.wait()
    print("Done")

async def setter():
    print("About to set the event")
    event.set()

async def runner():
    await gen.multi([waiter(), setter()])

IOLoop.current().run_sync(runner)
```

* is_set()

  判断 Event 内部标识是否为 True。

* set()

  将 Event 内部标识设置为 True，唤醒全部阻塞协程。

* clear()

  将 Event 内部标识设置为 False，再此调用 wait() 方法可在此阻塞协程。

* wait()

  Event 内部标识变为 True 前阻塞协程。

#### Semaphore - class tornado.locks.Semaphore

一个可以计数的锁，通过 Semaphore实例的计数器来控制是否阻塞，Semaphore 的构造函数的入参指定允许同时解锁的协程数。

```python
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Semaphore

sem = Semaphore(2)

async def worker(worker_id):
    await sem.acquire()
    try:
        print("Worker %d is working" % worker_id)
        await use_some_resource()
    finally:
        print("Worker %d is done" % worker_id)
        sem.release()

async def runner():
    # Join all workers.
    await gen.multi([worker(i) for i in range(3)])

IOLoop.current().run_sync(runner)
```

Semaphore 实例支持上下文管理协议。

```python
async def worker(worker_id):
    async with sem:
        print("Worker %d is working" % worker_id)
        await use_some_resource()

    # Now the semaphore has been released.
    print("Worker %d is done" % worker_id)
```

为了兼容旧版版，可使用 acquire 方法支持上下文管理协议。

```python
@gen.coroutine
def worker(worker_id):
    with (yield sem.acquire()):
        print("Worker %d is working" % worker_id)
        yield use_some_resource()

    # Now the semaphore has been released.
    print("Worker %d is done" % worker_id)
```

* release()

  计数器加一并唤醒一个阻塞中的协程。

* acquire()

  计数器减一并返回一个 awaitable。如果计数器为零，则阻塞协程并等待 release。

#### BoundedSemphore - class tornado.locks.BoundedSemphore

Semphore 的子类，功能类似，通常用于保护数量有限的资源。如果 release 使计数数量超过初始化时传入的值，不会阻塞，会抛出 ValueError 异常。

* release()
* acquire()

#### Lock - class tornado.locks.Lock

协程锁。初始化时处在未锁定状态，任意协程调用 acquire 方法，进入锁定状态。调用 release 方法解除锁定状态。支持上下文管理协议。

```python
lock = locks.Lock()

async def f():
		async with lock:
				# Do something holding the lock.
				pass
		# Now the lock is released.
```

为了兼容旧版本，可使用 acquire 方法支持上下文管理协议。

```python
async def f2():
		with (yield lock.acquire()):
				# Do something holding the lock.
				pass
		# Now the lock is released.
```

* acquire()

  尝试锁定锁，并返回一个 awaitable。

* release()

  解锁，等待队列中的第一个协程得到锁。如果在非锁定状态调用 release 方法，抛出 RuntimeError。

### tornado.queues - Queues for coroutines

为协程提供的异步队列。这些类与标准库中的 asyncio 包中的类非常相似。

tornado.queues 类不是线程安全的。如果想跨线程使用这些队列，需要先使用 IOLoop.add_callback 转移控制权。

#### Classes

##### Queue - class tornado.queues.Queue

用来协调生产者和消费者协程的队列。

```python
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue

q = Queue(maxsize=2)

@gen.coroutine
def consumer():
  	"""
  	Python version before 3.5
  	"""
    while True:
        item = yield q.get()
        try:
            print('Doing work on %s' % item)
            yield gen.sleep(0.01)
        finally:
            q.task_done()

async def consumer():
    async for item in q:
        try:
            print('Doing work on %s' % item)
            await gen.sleep(0.01)
        finally:
            q.task_done()

async def producer():
    for item in range(5):
        await q.put(item)
        print('Put %s' % item)

async def main():
    # Start consumer without waiting (since it never finishes).
    IOLoop.current().spawn_callback(consumer)
    await producer()     # Wait for producer to put all tasks.
    await q.join()       # Wait for consumer to finish all tasks.
    print('Done')

IOLoop.current().run_sync(main)
```

* maxsize

  队列允许的最大数量，如果队列的 maxsize 为默认值(0)，则队列大小不受限制。

* qsize()

  当前队列中的项目数量。

* put()

  向队列中加入一个项目，如果队列中没有位置就等待。返回一个 Future 对象，超时抛出 Tornado.util.TimeoutError。

* put_nowait()

  立刻向队列中加入一个项目，如果没有位置抛出 QueueFull 异常。

* get()

  从队列中取出一个项目，当队列中存在可选取的项目时，返回一个 awaitable，超时抛出 tornado.util.TimeoutError。

* get_nowait()

  立刻从队列中取出一个项目，如果队列中没有可选取的项目，抛出 QueueEmpty 异常。

* task_down()

  当前任务已完成。消费者调用，每个 get 方法会产生一个任务(task)，调用 task_down 方法告诉队列该任务执行完成。如果使用 join 方法阻塞队列，那么所有 put 进队列的项目全部执行完成并收到 task_down 方法后，阻塞回复。如果 task_down 方法调用的次数比 put 方法多，抛 ValueError。

* join()

  阻塞队列，直到所有项目都被处理。返回一个 awaitable，超时抛出 tornado.util.TimeoutError。

##### PriorityQueue - class tornado.queues.PriorityQueue

支持优先级的队列。队列的输入通常是类似 (priority number, data) 的元组。

##### LifoQueue - class tornado.queues.LifoQueue

后入先出的队列，类似于栈。

#### Exceptions

* exception tornado.queues.QueueEmpty
* exception tornado.queues.QueueFull

### tornado.process - Utilities for multiple process

多进程处理，包含进程分流和子进程管理。

#### tornado.process.cpu_count()

返回计算机 CPU 数量。

#### tornado.process.fork_processes()

启动多个工作进程。num_processes 入参表示派生子进程的数量，如果传 None 或小于等于0的值，则会根据 CPU 的数量派生进程。

由于是多进程而非多线程，所以进程间没有共享内存。多进程不兼容 autoreload，所以 debug 时不能使用多进程。

fork_processes 每个子进程返回它的 task_id。由于异常退出的子进程会使用其 task_id 重启（max_restarts，默认为100）次。所有子进程都退出，父进程会调用 sys.exit(0)，退出。

#### tornado.process.task_id()

返回进程的 task_id，如果进程不是通过 fork_processes 创建的，返回 None。

####class tornado.process.Subprocess

通过 IOStream 的支持包装的 subprocess.Popen。Windows 上不可用。

与 subprocess.Popen 不同的是 tornado.process.Subprocess.STREAM 会将子进程的返回封装成一个 PipeIOStream，输入、输出、错误流可以从中获取信息。

* set_exit_callback()

  设置进程退出时运行的 callback 方法。callback 方法需要进程的返回码作为入参。

  这个方法使用全局设置 SIGCHLD ，避免多个进程同时调用相同信号。如果调用多个 IOLoop，则必须先调用 Subprocess.initialize 来指定一个 IOLoop 来运行信号处理程序。

  回调可根据 stdout、stderr 来判断执行哪个方法。

* wait_for_exit()

  当进程退出时返回一个 Future。可以替代 set_exit_callback 方法，且对协程更友好。

  默认情况下，如果进程退出状态不为零，则会引发 subprocess.CalledProcessError。使用 wait_for_exit(raise_error = False) 可不抛异常，直接返回退出状态。

* classmethod initialize()

  初始化 SIGCHLD，信号处理程序在 IOLoop 上运行，用来避免锁问题。单线程不涉及此方法。

* classmethod uninitialize()

  删除 SIGCHLD



## Inregration with other services

### tornado.auth - Third-party login with OpenID and OAuth

模块提供各种第三方身份验证方案的实现。

模块中所有的类都被设计来被 tornado.web.RequestHandler 类使用。主要有两种使用方式：

1. 在登录处理程序上，使用 authenticate_redirect(), authorize_redirect(), get_authenticated_user() 之类的方法创建用户身份并存储身份认证到数据库和 Cookies 中。
2. 在非登录处理程序中，使用 fecebook_request(), twitter_request() 之类的方法来使用身份认证向响应的服务发出请求。

由于不同服务实现身份认证和授权的方式不同，所以它们的参数也略有不同，使用时参考具体文档。

谷歌用户认证介入方案如下：

```python
class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    async def get(self):
        if self.get_argument('code', False):
            user = await self.get_authenticated_user(
                redirect_uri='http://your.site.com/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            self.authorize_redirect(
                redirect_uri='http://your.site.com/auth/google',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})
```

#### Common protocolols

这些类通常支持 OpenID 和 OAuth 标准，通常，需要创建继承他们的子类才能针对第三方网站使用。所需的自定义程度会有所不同，但多数情况下，重写类的属性能够满足需求。

#####class tornado.auth.OpenIdMixin

OpenID以及与第三方用户登录信息交换相关的抽象类。

类变量：

* _OPENID_ENDPOINT，身份提供者的 URI。

类方法：

* authenticate_redirect()

  重定向此服务到身份验证 URL。身份验证后，服务带着追加的参数（包含 openid.mode），根据 callback 参数重定向回来。通常情况下，会接收已登陆用户传入的 ax_attrs（包含ame, email, language, username）。

* get_auth_http_client()

  返回要用于身份验证请求的 AsyncHTTPClient。

* coroutine get_authenticated_user()

  在重定向中获取用户身份验证信息。

  该方法应该由接收 authenticate_redirect() 重定向的处理方法调用。这个方法的结果通常用于设置 cookie。

##### class tornado.auth.OAuthMixin

OAuth1.0 和 OAuth1.0a 的抽象类。

类变量：

* _OAUTH_AUTHORIZE_URL，服务端 OAuth 授权的 url。
* _OAUTH_ACCESS_TOKEN_URL，服务端 OAuth 访问令牌的 url。
* _OAUTH_VERSION，描述 OAuth 的版本，1.0 或者 1.0a。
* _OAUTH_NO_CALLBACKS，如果是 true 服务需要提前注册 callback。

类方法：

* authorize_redirect()

  重定向用户以获取服务的 OAuth 授权。如果提前向第三方服务注册了回调 URL，则可以省略 callback_uri。有些服务只支持注册URL，不能通过 callback_uri 指定回调。

  这个方法设置了一个称为 _oauth_request_token 的 cookie，供之后的 get_authenticated_user 方法使用。

  这是个异步方法，必须通过 async 和 await 调用。该方法会调用 RequestHandler.finish，所以不需要为其提供响应方法。

* get_authenticated_user()

  获取 OAuth 授权的用户和访问令牌。这个方法应该被 OAuth 的回调 URL 的处理程序调用，用来完成注册。回调的入参是已验证身份的用户的信息字典，字典包含一个 access_key，用来向服务器提出授权请求，以及用户名等其它信息。

* _oauth_consumer_token()

  该类的子类必须重写此方法。返回 OAuth 消费者密钥，一个包含 key，secret 的字典。

* _oauth_get_user_future()

  该类的子类必须重写此方法。获取用户的基本信息，应该是一个返回通过 access_token 向服务器请求到的用户信息字典的协程方法。用户令牌会被添加到返回的字典中，供 get_authenticated_user 使用。

* get_auth_http_client()

  返回用户认证请求使用的 AsyncHTTPClient。

##### class tornado.auth.OAuth2MIxin

OAuth2.0 的抽象类。

类变量：

* _OAUTH_AUTHORIZE_URL，服务端 OAuth 授权的 url。
* _OAUTH_ACCESS_TOKEN_URL，服务端 OAuth 访问令牌的 url。

类方法：

* authorize_redirect()

* get_auth_http_client()

* coroutine oauth2_request()

  获取给定 URL 的 OAuth2 的访问令牌。

### tornado.wsgi - Interoperability with other Python frameworks and servers

tornado web framework 的 wsgi 支持。

WSGI 是 python 的 web 服务实现标准。Tornado 和其他 Python web framework 可通过其进行通信。

此模块通过 WSGIContainer 类提供 WSGI 支持。这样就可以在 Tornado HTTP 服务上使用其他的 WSGI 框架。由于 Tornado 的 Application 和 RequestHandler 类是通过 Tornado 的 HTTPServer 实现的，而不是 WSGI。所以不能在通用的 WSGI 容器中使用 Tornado。

#### class tornado.wsgi.WSGIContainer

是一个符合 WSGI 标准的方法可以在 Tornado HTTP 服务上运行。

注意，WSGI 是同步接口，而 Tornado 的并发模型是基于单线程异步的。这意味着相较于基于多线程的框架，通过 Tornado 的WSGIContainer 调用 WSGI 应用的可扩展性较差。所以使用 WSGI 前要仔细考虑。

WSGIContainer 可以包装一个 WSGI 方法，然后将其传入 HTTPServer来执行它。

```python
def simple_app(environ, start_response):
    status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(status, response_headers)
    return ["Hello world!\n"]

container = tornado.wsgi.WSGIContainer(simple_app)
http_server = tornado.httpserver.HTTPServer(container)
http_server.listen(8888)
tornado.ioloop.IOLoop.current().start()
```

### tornado.platform.caresresolver - Aysnchoronous DNS Resolver using C-A

该模块包含一个使用 c-ares 库的 DNS 解析器。

#### class tornado.platform.caresresolver.CaresResolver

非阻塞且非线程的 DNS 解析器，可能与系统解析器的解析结果不同，适用于非多线程的服务。只适用于 IPv4。

### tornado.platform.twisted - Bridges between Twisted and Tornado

支持 Tornado 集成 Twisted 的模块。

#### class tornado.platform.twisted.TwistedResolver

基于 Twisted 的异步 DNS 解析器。非阻塞且非多线程的解析器，它最多返回一个结果，并且除 host 和 family 以外的参数都将被忽略。

### tornado.platform.asyncio - Bridges between aysncio and Tornado

支持 Tornado IOLoop 集成 asyncio。现在 asyncio 可用时会自动启用该模块，所以应用程序已不需要直接引用该模块。

Tornado 使用基于选择器的事件循环。配置 asyncio 可能能提升 Tornado 的性能。

* class tornado.platform.asyncio.AsyncIOMainLoop

  创建一个与当前 asyncio 事件循环相对应的 IOLoop。

* class tornado.platform.asyncio.AsyncIOLoop

  在异步事件循环上运行的 IOLoop，创建语法与创建常规 IOLoop 类似。创建的 AsyncIOLoop 对象不一定与默认的 asyncio loop 相关联。

* tornado.platform.asyncio.to_tornado_future()

  将 asyncio.Future 转换为 tornado.Future。

* tornado.platform.asyncio.to_asyncio_future()

  将 tornado.Future 转换为 asyncio.Future。

* class tornado.platform.asyncio.AnyThreadEventLoopPolicy

  允许在任何线程上创建循环的事件循环策略。

  默认的 asyncio 事件循环策略仅在主线程中自动创建事件循环。其他线程必须显式创建事务循环，否则 asyncio.get_event_loop 将失败。

* class tornado.platform.asyncio.AddThreadSelectorEventLoop

  包装一个事件循环用来添加 add_reader 系列方法的实例。

  此类的实例启动另一个线程来运行选择器。该线程对用户完全隐藏，所有的回调都在包装事件循环的线程上完成。

  Tornado 会自动使用此类，程序不需要引用它。

  用此类包装任何事务循环都是安全的，尽管它只对未实现 add_render 方法的事件循环才有意义。

  关闭 AddThreadSelectorEventLoop 时会同时关闭该类包装的事件循环。

## Utilities

### tornado.autoreload - Automatically detect code changes in development

修改源文件后自动重新启动服务。

通常不需要直接使用该模块，通过 tornado.web.Application 构造函数的 keyword 入参 autoreload=True 或 debug=True 使用。

注意，重新启动是一种破坏性操作，进程重启时，任何进行中的请求都将中止。

这个模块还可在命令行中使用，例如单元测试的启动语句。

该模块与多进程模式不兼容。

重新加载会丢失所有 Python 解释器命令行参数，因为它使用 sys.executable 和 sys.argv 重新执行 Python。注意，修改这些变量可能导致重新加载不正确。

* tornado.autoreload.start()

  开始监控源文件的修改。

* tornado.autoreload.wait()

  等待监控方法得到修改结果，然后重启进程。

* tornado.autoreload.watch()

  将文件加入监控列表。

* tornado.autoreload.add_reload_hook()

  重新加载进程之间，添加一个需要调用的函数。

* tornado.autoreload.main()

  命令行启动程序时，可在脚本源更改时重新运行脚本，脚本可通过文件名或模块名指定。

  ```shell
  python -m tornado.autoreload -m tornado.test.runtests
  python -m tornado.autoreload tornado/test/runtests.py
  ```

### tornado.concurrent - Work with Future objects

与 Future 相关的工具。

Tornado 以前提供了自己的 Future 类，但现在使用 asyncio.Future。该模块包含一些实用工具，用于处理 asyncio.Future，并兼容 Tornado 的旧 Future 。

尽管该模块是 Tornado 内部实现的重要组成部分，但应用一般不与其交互。

##### class tornado.concurrent.Future

asyncio.Future 的子类。

Tornado 中，应用程序与 Future 对象交互的主要方式是通过在协程中 await 或 yield 他们，而不是在 Future 对象本身上调用方法。

#####  tornado.concurrent.run_on_executor()

在一个执行器上以异步的方式调用同步方法的装饰器。

返回一个 Future 对象。

选取哪种异步方式由执行器的 executor 参数决定。

```python
@run_on_executor(executor='_thread_pool')
def foo(self):
    pass
```

##### tornado.concurrent.chain_future()

将两个 future 连接在一起。第一个 Future 的结果会复制给第二个 future，除非第二个在第一个完成时已经完成或取消。

##### tornado.concurrent.future_set_result_unless_cancelled()

将给定异常设置为 future 的默认异常，future 取消时会自动抛出。

##### tornado.concurrent.future_set_exc_info()

将给定异常列表设置为 future 的默认异常链，future 取消时会自动抛出。

##### tornado.concurrent.future_add_done_callback()

为 future 增加 callback，callback 方法的入参是 future。future 完成后会立即调用 callback。

### tornado.log - Logging support

Tornado 的日志支持。包含三个可分开配置的日志流：

* tornado.access

  Tornado HTTP Server 记录每个单独请求的日志。

* tornado.application

  记录应用程序中的错误日志。

* tornado.general

  通用日志，可记录任何错误或警告。

##### class tornado.log.LogFormatter

日志格式化的类，主要功能：

* 高亮
* 为每行日志打时间戳
* 解决编码问题

这个格式化程序可由 tornado.options.parse_command_line 或者 tornado.options.parse_config_file 自动启用。

##### tornado.log.enable_pretty_logging()

根据配置格式化地输出日志。也通过 tornado.options.parse_command_line 或者 tornado.options.parse_config_file 自动启用。

##### tornado.log.define_logging_options()

为 options 增加日志相关的功能项。选项会自动生效，只有创建了自己的 tornado.options.OptionsParser 才能生效。

### tornado.options - Command-line parsing

命令行解析模块，帮助模块定义自己的选项。该模块的主要特点是使用了全局注册表，因此可在任何模块中定义选项。该模块与 tornado 其余部分是分离的，所有可以使用 argparse 之类的模块代替它。

使用该模块前，必须使用 tornado.options.define 定义，一般定义语句会在模块的最前面。定义完成后，可以将这些选项作为 tornado.options.options 的属性来访问。

应用的 main() 方法不需要知道程序中使用的全部选项，它们在加载模块时都会默认加载。但是在解析命令之前，必须先导入所涉及的选项。

main() 方法可以解析命令行，或者通过 parse_command_line 或者 parse_config_file 解析配置文件。

```python
# myapp/db.py
from tornado.options import define, options

define("mysql_host", default="127.0.0.1:3306", help="Main user DB")
define("memcache_hosts", default="127.0.0.1:11011", multiple=True,
       help="Main user memcache servers")

def connect():
    db = database.Connection(options.mysql_host)
    ...

# myapp/server.py
from tornado.options import define, options

define("port", default=8080, help="port to listen on")

def start_server():
    app = make_app()
    app.listen(options.port)
    
# myapp/main.py
import myapp.db, myapp.server
import tornado.options

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # or
    tornado.options.parse_config_file("/etc/server.conf")
```

注意，需要使用多个 parse_* 函数时，除最后一个函数外，其它都该传入 final = False。否则副作用可能会发生两次（例如日志加倍）。

tornado.options.options 是 tornado.options.OptionParse 的实例，tornado.options 模块中的常用功能都在其方法中使用。可以创建多个 tornado.options.OptionsParse 实例来隔离不同的选项集。

通常调用 parse_command_line 或 parse_config_file 时会有些默认的设置，例如对 logging 模块的设置，这些也可显式修改。

#### Global functions

* tornado.options.define()

  在全局命名空间内定义一个 option。

* tornado.options.options()

  全局 options 对象，所有定义的 options 都可作为该对象的属性。

* tornado.options.parse_config_file()

  从一个配置文件中解析全局 options。

* tornado.options.print_help()

  将所有命令行 options 打印到 stderr。

* tornado.options.add_parse_callback()

  添加一个 callback，在完成选项解析后将被调用。

* exception tornado.options.Error

  options 模块中引起的异常。

####  OptionParser class

* class tornado.options.OptionParser

  options 的集合，可以像访问对象的属性一样访问的字典。

  通常通过 tornado.options 模块中的静态方法访问，这些函数引用了 global 实例。

* tornado.options.OptionsParser.define()

  定义一个新的命令行 option。新定义的配置会覆盖之前的。

* tornado.options.OptionParser.parse_command_line()

  解析命令行上给定的所有选项。

  类似于 --option=value 的 options 会根据类型进行分析。如果 multiple=True，接收逗号分割的值，也可以用 x:y 表示 range(x,y)。args[0] 会被忽略，因为它是程序名称。 返回未解析为 options 的全部参数列表。如果 final 入参传入 false，callbacks 不会被执行。这对合并多个来源的配置文件很有用。

* tornado.options.OptionParser.parse_config_file()

  从给定文件中解析并加载配置。

  配置文件包含将要执行的 Python 代码，因此不要引入不信任的配置。全局命名空间中与定义的选项匹配的所有内容都将用于设置该选项的值。options 的解析方式与 parse_command_line 相同。

* tornado.options.OptionParser.print_help()

  将所有命令行选项打印到 stderr。

* tornado.options.OptionParser.add_parse_callback()

  添加一个 callback，在完成选项解析后将被调用。

* tornado.options.OptionParser.mockable()

  兼容 unittest.mock.patch。

* tornado.options.OptionParser.items()

* tornado.options.OptionParser.as_dict()

* tornado.options.OptionParser.groups()

  返回 key set()。

* tornado.options.OptionParser.group_dict()

  ```python
  application = Application(handlers, **options.group_dict('application'))
  ```

### tornado.testing - Unit testing support for asynchronous code

自动化测试相关的类。

* AsyncTestCase & AsyncHTTPTestCase

  unittest 的子类，对异步代码提供额外支持。

* ExpectLog

  过滤筛选测试日志。

* main()

  一个简单的测试运行器，支持 tornado.autoreload 模块（源代码修改时会重新执行）。

#### Asynchronous test case

* class tornado.testing.AsyncTestCase

  unitteset.TestCase 的子类，提供额外的异步支持，用于测试基于 IOLoop 的异步代码。

* class tornado.testing.AsyncHTTPTestCase

  启动 HTTP 服务的测试用例。

* tornado.test.gen_test()

  类似于 @gen.coroutine，@gen.coroutine 不能用于测试，因为 IOLoop 尚未运行。@gen_test 应该用于装饰 AsyncTestCase 及其子类的测试方法。

#### Controlling log output

* class tornado.testing.ExpectLog

  上下文管理器，用于捕获和抑制预期的日志输出。过滤不需要的测试结果。

#### Test runner

* tornado.testing.main()

  简单的测试运行器。

  这个测试运行器本质上相当于 unittest.main，增加了对 Tornado 风格的选项解析和日志格式化。可以但非必须使用该方法运行 AsyncTestCase。

  使用该运行器最简单的方法是通过命令行。

  ```shell
  python -m tornado.testing tornado.test.web_test
  ```

#### Helper functions

* tornado.testing.bind_unused_port()

  将服务socket绑定到本地的一个可用端口。

* tornado.testing.get_async_test_timeout()

  得到异步测试的全局超时设置。

### tornado.util - Genral-purpose utilies

模块包含各种各样的实用的方法和类。供 Tornado 框架内部使用。

该模块最常用的部分是 Configurable 类以及它的 configure 方法。其中一部分被其他类继承，并称为这些子类的一部分。其子类主要包含 AsyncHTTPClient，IOLoop 和 Resolver。

* exception tornado.util.TimeoutError

  with_timeout 和 IOLoop.run_sync 抛出的异常。

* class tornado.util.ObjectDict

  使字典可以像对象一样通过句号访问属性。

* class tornado.util.GzipDecompressor

  流解压器。

* tornado.util.import_object()

  通过名称 import 模块。

* tornado.util.errno_from_exception()

  从异常中提取 errno。

* tornado.util.re_unscape()

  re.escape 的逆操作。

* class tornado.util.Configurable

  可配置接口的基础类。

  可配置接口是一个抽象类，它的构造行为由子类实现。

  其子类必须实现 configurable_base 和 configurable_default 方法，用 initialize 方法代替 \_\_init\_\_()。

  * classmethod configurable_base()

    返回配置类的基类。通常直接返回创建的子类。

  * classmethod configurable_default()

    返回默认的类。

  * initialize()

    代替\_\_init\_\_()，用来初始化子类。

  * classmethod configure()

    类初始化时添加入参，可用于设置全局的默认入参。

  * classmethod configred_clasee()

    返回当前的类。

* class tornado.util.ArgReplace

  替换 args, kwargs 中的参数。检查函数签名并找到一个参数（位置和参数名均支持），通过装饰器替换它。