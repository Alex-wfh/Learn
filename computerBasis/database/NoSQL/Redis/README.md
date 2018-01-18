# Redis

## 简介
Redis(REmote DIctionary Server) 是完全开源免费的，遵守BSD协议，是一个高性能的 key-value 数据库。

### 优势
* 性能极高，Redis 能读的速度是110000次/s,写的速度是81000次/s；
* 丰富的数据类型，Redis 支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作；
* 原子，Redis 单个操作是原子性的，多个操作也支持事物；
* 丰富的特性，Redis 支持 publish/subscribe，通知，key 过期等等特性。
* 可持久化，运行在内存中，但是可以持久化到磁盘。

## 配置
* 配置查看：`CONFIG GET CONFIG_SETTING_NAME`
* 配置编辑：`CONFIG SET CONFIG_SETTING_NAME NEW_CONFIG_VALUE`

### Redis 常用参数
* `daemonize no` 是否以守护进程的方式运行
* `pidfile /var/run/redis.pid` 以守护进程方式运行时，pid存储位置
* `port 6397` 监听端口
* `bind 127.0.0.1` 绑定主机地址
* `timeout 300` 客户端闲置多长时间后关闭连接，如果指定为0，表示关闭该功能
* `loglevel verbose` 日志记录级别，Redis 总共支持四个级别：debug、verbose、notice、warning
* `logfile stdout` 日志记录方式
* `databases 16` 数据库数量
* `save <seconds> <changes>` 在多长时间，多少次更新操作，就将数据同步到数据文件，可以多个条件配合，默认提供三个条件：`save 900 1`、`save 300 10`、`save 60 10000`
* `rdbcompression yes` 存储至本地数据库时是否压缩
* `dbfilename dump.rdb` 本地数据库文件名
* `dir ./` 本地数据库存放目录
* `slaveof <masterip> <masterport>` 当本机为 slav 服务时，设置 master 服务的IP地址及端口，在Redis启动时，它会自动从 master 进行数据同步
* `masterauth <master-password>` 当master服务设置了密码保护时，slav服务连接master的密码
* `requirepass <password>` Redis 连接密码，默认为空
* `maxclients 10000` 同一时间最大客户端连接数
* `maxmemory 0` Redis 最大内存限制，达到最大内存后 Redis 会尝试清除已到期或即将到期的 key
* `appendonly no` 每次更新后是否进行内存记录
* `appendfilename appendonly.aof` 更新日志的文件名
* `appendsfync everysec` 更新日志的条件，三个可选值：`no`等操作系统进行数据缓存同步时、`always`每次更新操作后、`everysec`每秒
* `vm-enabled no` 是否启用虚拟内存机制
* `vm-swap-file /tmp/redis.swap` 虚拟内存文件路径
* `vm-max-memory 0` 将大于`vm-max-memory`的数据存入虚拟内存，注意：Redis索引数据（keys）只存于内存中
* `vm-page-size 32` Redis swap 文件分成很多 page，一个对象可保于多个 page，但一个 page 不能被多个对象共享
* `vm-page 134217728` swap 文件中的 page 数量
* `vm-max-threads 4` 访问 swap 的线程数，最好不要超过机器的核数
* `glueoutputbuf yes` 向客户端应答时，是否把较小的包合并为一个包发送
* `hash-max-zipmap-entries 64` `hash-max-zipmap-value 512` 元素超过一定数量，或最大元素超过一定临界值时，采用一种特殊的哈希算法
* `activerehashing yes` 是否激活重置哈希
* `include <path>` 包含其他的配置文件，默认为空

## 数据类型
Redis 支持五种数据类型：string(字符串)、hase(哈希)、list(列表)、set(集合)及 zset(有序集合)。

### String
string 是 redis 最基本的类型，是二进制安全的(可以包含任何数据)，一个键最多存储512MB。  

```
SET name "alex"
Get name
```

### Hash
hash 是键值对集合，特别适合用于存储对象，每个 hash 可以存储 2<sup>32</sup>-1 键值对（40多亿）。

```
HMSET myhash field1 "Hello" field2 "World"
HGET myhash field1
HGET myhash field2
```

### List
简单的字符串列表，按插入顺序排序，可以在头部或尾部添加元素，每个 list 可以存储 2<sup>32</sup>-1 键值对（40多亿）。

```
LPUSH mylist l1
LPUSH mylist l2
LPUSH mylist l3
LRANGE mylist 0 10
```

### Set
字符串集合，通过哈希表实现，添加、删除、查找的复杂度都是 O(1)，set 的最大成员数为 2<sup>32</sup>-1

```
SADD myset s1
SMEMBERS myset
```

### Zset
字符串集合，且不允许重复，每个元素都会关联一个 double 类型的分数，redis 通过分数来为集合中的成员排序，分数可重复。

```
ZADD myzset 0 z1
ZADD myzset 1 z2
ZRANGEBYSCORE myzset 0 1000
```

## Redis 命令
Redis 命令用于在 redis 服务上执行操作，要在 redis 服务上执行命令需要一个 redis 客户端。
### Redis 启动客户端

```
$redis-cli #本地redis服务
$redis-cli -h host -p port -a password #远程redis服务
```
```
PING #检查redis服务是否启动
```

### Redis Key
* `SET key value` 插入
* `DEL key` 删除
* `DUMP key` 序列化，返回序列化的值
* `EXISTS key` 检查是否存在
* `EXPIRE key seconds` 设置过期时间 
* `EXPIREAT key timestamp` 设置过期时间戳
* `PEXPIRE key milliseconds` 设置过期时间毫秒
* `PEXPIREAT key milliseconds-timestamp` 设置过期时间戳毫秒
* `KEYS pattern` 查找所有符合给定格式的key
* `MOVE key db` 当前数据库中的key移到给定数据库中
* `PERSIST key` 移除key过期时间
* `PTTL key` 以毫秒为单位返回key过期时间
* `TTL key` 以秒为单位返回key过期时间
* `RANDOMKEY` 从当前数据库中随机返回一个key
* `RENAMENX key newkey` 修改key的名称
* `TYPE key` 返回key的类型

