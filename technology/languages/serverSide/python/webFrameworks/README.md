# Python Web Frameworks
以下是我个人比较感兴趣的框架，并未全部使用过，各框架的特点也仅代表个人理解。

### Django - powerful
目前最成熟、使用最广的`python`web框架，囊括web应用的所有内容，很强大，但较重，缺乏灵活性，适用于大项目，社区完善，官方文档很好，而且有中文版本。

### Flask - nimble
基于 Werkzeug，Jinja2。敏捷，微框架，核心非常简单，自由继承其他模块，社区不错。

### Tornado - asynchronous
成熟的异步web框架，协程支持很好，性能较好，社区完善，官方文档内容较少。

### Twisted

Python 编写的事件驱动的网络引擎。Twisted 很快，但是相较于常规的 WebApp，Twisted 更适合底层网络（传输层）开发。

### Pyramid - flexible
较成熟，可用于小的应用，也可面向大型网站，开始新项目时提供很多选项(过多)，与 Flask 类似，但总感觉略逊一筹。

### Bottle - simple
简单，轻量，单文件形式发布，

### Sanic - fastest
支持`python3.5`及以上的异步协程框架，目前速度最快的`python`web框架，代码类似`Flask`，框架较新，仍存在扩展不方便、内部耦合较深、细节处理不严谨等问题。

### Dash - data analysis
专门针对数据分析的框架，高度集成`Flask`和`React`，实现数据可视化，代码密度极高。

### 个人喜好
针对以上框架，如果要我选择一个开始新项目，我会在`Flask、Bottle、Tornado、Dash、Django(尽管本人更喜欢自由)`中选择一个，会根据业务场景进行选择，注意，目前市面上绝大部分的应用、网站都可以归为“小型”。