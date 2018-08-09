# Bottle
A fast, simple and lightweight WSGI micro web-framework for Python.

## 安装 Install
```
$ wget http://bottlepy.org/bottle.py
```
```
$ sudo pip install bottle
```

## 快速开始 HELLO WORLD
```
from bottle import route, run
@route('/hello')
def hello():
    return "Hello World!"
run(host='localhost', port=8080, debug=True)
```

## 请求路由 Request Routing
```
@route('/hello')
```

### 动态路由 Dynamic Routes
```
@route('/')
@route('/hello/<name>')
```
```
@route('/hello/<param:int>')
@route('/hello/<param:float>')
@route('/hello/<param:path>')
@route('/hello/<param:re:[a-z]+>')
```

### HTTP请求方法 HTTP Request Method
```
from bottle import get, post, request # or route
@get('/login') # or @route('/login')
@post('/login') # or @route('login', method='POST')
```

### 错误页 Error Pages
```
from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'
```

## 生成内容 Generating Content
```
from bottle import response
@route('/iso')
def get_iso():
    response.charset = 'ISO-8859-15'
    return u'This will be sent with ISO-8859-15 encoding.'
@route('/latin9')
def get_latin():
    response.content_type = 'text/html; charset=latin9'
    return u'ISO-8859-15 is also known as latin9.'
```

### 静态文件 Static Files
```
from bottle import static_file
@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='/path/to/image/files', mimetype='image/png')
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/path/to/static/files')
```

#### 强制下载 Forced Download
```
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='/path/to/static/files', download=filename)
```

### HTTP错误和重定向 HTTP Errors and Redirects
```
from bottle import route, abort
@route('/restricted')
def restricted():
    abort(401, "Sorry, access denied.")
```
```
from bottle import redirect
@route('/wrong/url')
def wrong():
    redirect("/right/url")
```

### Response对象 The Response Object
```
@route('/wiki/<page>')
def wiki(page):
    response.set_header('Content-Language', 'en')
    response.add_header('Set-Cookie', 'name2=value2')
```

### Cookies
```
@route('/hello')
def hello_again():
    if request.get_cookie("visited"):
        return "Welcome back! Nice to see you again"
    else:
        response.set_cookie("visited", "yes")
        return "Hello there! Nice to meet you"
```
```
@route('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie("account", username, secret='some-secret-key')
        return template("<p>Welcome {{name}}! You are now logged in.</p>", name=username)
    else:
        return "<p>Login failed.</p>"
@route('/restricted')
def restricted_area():
    username = request.get_cookie("account", secret='some-secret-key')
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."
```
## 请求数据 Request Data
```
@route('/hello')
def hello():
    name = request.cookies.username or 'Guest'
    return template('Hello {{name}}', name=name)
```

Attribute | GET Form fields | POST Form fields | File Uploads
----------|-----------------|------------------|-------------
BaseRequest.query  | yes | no  | no
BaseRequest.forms  | no  | yes | no
BaseRequest.files  | no  | no  | yes
BaseRequest.params | yes | yes | no
BaseRequest.GET    | yes | no  | no
BaseRequest.POST   | no  | yes | yes


### FormsDict介绍 Introducting FormsDict
```
python2
>>> request.query['city']
'G\xc3\xb6ttingen'  # A utf8 byte string
>>> request.query.city
u'Göttingen'        # The same string as unicode
```
```
python3
>>> request.query['city']
'GÃ¶ttingen' # An utf8 string provisionally decoded as ISO-8859-1 by the server
>>> request.query.city
'Göttingen'  # The same string correctly re-encoded as utf8 by bottle
```

### HTTP头部 HTTP Headers
```
from bottle import route, request
@route('/is_ajax')
def is_ajax():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return 'This is an AJAX request'
    else:
        return 'This is a normal request'
```

### 查询变量 Query Variables
```
from bottle import route, request, response, template
@route('/forum')
def display_forum():
    forum_id = request.query.id
    page = request.query.page or '1'
    return template('Forum ID: {{id}} (page {{page}})', id=forum_id, page=page)
```

### HTML表单处理 HTML Form Handing
```
from bottle import route, request
@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''
@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
```

### 文件上传 File Uploads
```
@route('/upload', method='POST')
def do_upload():
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'
    save_path = get_save_path_for_category(category)
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'
```

### JSON内容 JSON Content
```
@route('/json')
def do_json():
	json = request.json()
	return 'OK'
```

### 原始请求体 The Raw Request Body
```
@route('/body')
def do_body():
	body = request.body()
	return 'OK'
```

### WSGI环境 WSGI Environment
```
@route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    # or ip = request.get('REMOTE_ADDR')
    # or ip = request['REMOTE_ADDR']
    return template("Your IP is: {{ip}}", ip=ip)
```

## 模板 Template
```
@route('/hello')
@route('/hello/<name>')
def hello(name='World'):
    return template('hello_template', name=name)
```
```
@route('/hello')
@route('/hello/<name>')
@view('hello_template')
def hello(name='World'):
    return dict(name=name)
```
会加载模板文件hello_template.tpl并用设置的name变量来渲染它。Bottle会在./views/文件夹或在bottle.TEMPLATE_PATH中指定的文件夹列表中查找模板。

### 语法 Syntax
```
%if name == 'World':
    <h1>Hello {{name}}!</h1>
    <p>This is a test.</p>
%else:
    <h1>Hello {{name.title()}}!</h1>
    <p>How are you?</p>
%end
```

### 缓存 Caching
```
bottle.TEMPLATES.clear()
```
非debug模式模版会缓存下来

## 插件 Plugins
```
from bottle import route, install, template
from bottle_sqlite import SQLitePlugin
install(SQLitePlugin(dbfile='/tmp/test.db'))
@route('/show/<post_id:int>')
def show(db, post_id):
    c = db.execute('SELECT title, content FROM posts WHERE id = ?', (post_id,))
    row = c.fetchone()
    return template('show_post', title=row['title'], text=row['content'])
@route('/contact')
def contact_page():
    ''' This callback does not need a db connection. Because the 'db'
        keyword argument is missing, the sqlite plugin ignores this callback
        completely. '''
    return template('contact')
```

### 应用范围的安装 Application-wide Installation
```
from bottle_sqlite import SQLitePlugin
install(SQLitePlugin(dbfile='/tmp/test.db'))
```

```
sqlite_plugin = SQLitePlugin(dbfile='/tmp/test.db')
install(sqlite_plugin)
uninstall(sqlite_plugin) # uninstall a specific plugin
uninstall(SQLitePlugin)  # uninstall all plugins of that type
uninstall('sqlite')      # uninstall all plugins with that name
uninstall(True)          # uninstall all plugins at once
```

### 指定路由的安装 Blacklisting Plugins
```
sqlite_plugin = SQLitePlugin(dbfile='/tmp/test.db')
@route('/create', apply=[sqlite_plugin])
def create(db):
    db.execute('INSERT INTO ...')
```

### 黑名单插件 Blacklisting Plugins
```
sqlite_plugin = SQLitePlugin(dbfile='/tmp/test1.db')
install(sqlite_plugin)
dbfile1 = '/tmp/test1.db'
dbfile2 = '/tmp/test2.db'
@route('/open/<db>', skip=[sqlite_plugin])
def open_db(db):
    # The 'db' keyword argument is not touched by the plugin this time.
    # The plugin handle can be used for runtime configuration, too.
    if db == 'test1':
        sqlite_plugin.dbfile = dbfile1
    elif db == 'test2':
        sqlite_plugin.dbfile = dbfile2
    else:
        abort(404, "No such database.")
    return "Database File switched to: " + sqlite_plugin.dbfile
```

### 插件和子应用 Plugins and Sub-Applications
```
root = Bottle()
root.mount('/blog', apps.blog)
@root.route('/contact', template='contact')
def contact():
    return {'email': 'contact@example.com'}
root.install(plugins.WTForms())
```
```
root.mount('/blog', apps.blog, skip=None)
```

## 开发 Development
### 默认应用 Default Application
```
@route('/')
def hello():
    return 'Hello World'

run()
```
```
app = Bottle()

@app.route('/')
def hello():
    return 'Hello World'

app.run()
```

### 调试模式
```
bottle.debug(True)
```
* 默认错误页会显示调用堆栈。
* 模板不会被缓存。
* 插架会被立刻的应用。

### 自动重启 Auto Reloading
```
from bottle import run
run(reloader=True)
```

### 命令行界面 Command Line Interface
```
$ python -m bottle
```

## 部署 Deployment
```
bottle.run(server='paste')
```

## 术语 Glossary
* callback 回调
* decorator 装饰器
* environ 环境变量
* handler function 依附于指定URL上 
* source derictory 项目中包含所有源文件的文件夹及子文件夹