# Tornado



## Web Framework

### tornado.web - RequestHandler & Application

提供一个具有异步功能的web框架

#### Thread-safety

非线程安全

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

  * listen
  * bind
  * add_sockets

### tornado.httpclient - Asynchronous HTTP client

* simple_httpclient vs curl_httpclient
  * simple_httpclient 为默认方法
  * curl_httpclient 包含额外的特征，支持HTTP代理，支持某些特定的网络接口
  * curl_httpclient 更容易实现非常规的HTTP请求
  * curl_httpclient 更快
  * curl_httpclient 需要最新版本的 libcurl 和 pycurl

#### HTTP client interfaces

* class tornado.httpclient.HTTPClient, class tornado.httpclient.AsyncHTTPClient
  * fetch()
  * close()

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

非阻塞套接字的 I/O 事务循环

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