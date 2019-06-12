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

### Redis 常用配置参数
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
* `$redis-cli` 本地redis服务
* `$redis-cli -h host -p port -a password` 远程redis服务
* `PING` 检查redis服务是否启动

### Redis Key
* `SET key value` 存储
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

### Redis String
* `SET key value` 存储
* `GET key` 获取
* `GETRANGE key start end` 获取value的子字符串
* `GETSET key value` 存储新值，返回旧值
* `GETBIT key offset` 获取value指定位上的值
* `MGET key1 [key2...]` 获取一个或多个value
* `SETBIT key offset value` 设定value指定位上的值
* `SETEX key seconds value` 存储，并设置过期时间
* `SETNX key value` key不存在时存储
* `SETRANGE key offset value` 复写从偏移量offset开始的value
* `STRLEN key` 返回value长度
* `MSET key value [key value ...]` 同时存储一个或多个
* `MSETNX key value [key value ...]` 同时存储一个或多个，仅当全部key都不存在时
* `PSETEX key milliseconds value` 存储，并设置过期时间，以毫秒为单位
* `INCR key` 将value加1
* `INCRBY key increment` 将value加increment(int)
* `INCRBYFLOAT key increment` 将value加increment(float)
* `DECR key` 将value减1
* `DECRBY key decrement` 将value减去decrement
* `APPEND key value` 若key已存在，将value追加到原value末尾

### Redis Hash
* `HDEL key field1 [field2...]` 删除一个或多个字段
* `HEXISTS key field` 查看指定字段是否存在
* `HGET key field` 获取指定字段的值
* `HGETALL key` 获取指定key所有的值
* `HINCRBY key field increment` 指定字段加上increment
* `HINCRBYFLOAT key field increment` 指定字段加上increment(float)
* `HKEYS key` 获取所有哈希表中的字段
* `HLEN key` 获取哈希表中字段的数量
* `HMGET key field1 [field2...]` 获取所有给定字段的值
* `HMSET key field1 value1 [field2 value2...]` 同时存储多个字段
* `HSET key field value` 存储一个字段
* `HSETTNX key field value` 不存在时存储一个字段
* `HVALS key` 获取哈希表中的所有值
* `HSCAN key cursor [MATCH pattern] [COUNT count]` 迭代哈希表中的键值对

### Redis List
* `BLPOP key1 [key2] timeout` 移出并获取列表的第一个元素，如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
* `BRPOP key1 [key2] timeout` 移出并获取列表的最后一个元素，如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止
* `BRPOPLPUSH source destination timeout` 从一个列表中弹出一个值，将弹出元素插入到另一个列表中并返回它，无元素列表阻塞
* `LINDEX key index` 通过索引获取列表中的元素
* `LINSERT key BEFORE|AFTER pivot value` 在列表元素的前或后插入元素
* `LLEN key` 获取列表长度
* `LPOP key` 移出并获取列表的第一个元素
* `LPUSH key value1 [value2]` 将一个或多个元素插入列表头部
* `LPUSHX key value` 将一个值插入到已存在的列表头部
* `LRANGE key start stop` 获取列表指定范围的元素
* `LREM key count value` 移除列表元素
* `LSET key index value` 通过索引设置列表元素的值
* `LTRIM key start stop` 只保留指定区间内的元素
* `RPOP key` 移出并获取列表最后一个元素
* `RPOPLPUSH source destination` 移出列表最后一个元素，将该元素添加到另一个列表并返回
* `RPUSH key value1 [value2]` 在列表中添加一个或多个值
* `RPUSHX key value` 为已存在的列表添加值

### Redis Set
* `SADD key member1 [member2]` 向集合添加一个或多个成员
* `SCARD key` 获取集合的成员数
* `SDIFF key1 [key2]` 返回给定所有集合的差集
* `SDIFFSTORE destination key1 [key2]` 返回所有集合的差集并存储在detination中
* `SISMEMBER key member` 判断member是否是集合key的成员
* `SISMEMBERS key` 返回集合中所有成员
* `SMOVE source destination member` 将元素从source移动到destination中
* `SPOP key` 返回一个随机元素
* `SRENDMEMBER key [count]` 返回多个随机元素
* `SREM key member1 [member2]` 移除集合中一个或多个元素
* `SUNION key1 [key2]` 返回集合并集
* `SUNIONSTORE destination key1 [key2]` 取集合并集并存储在destination中
* `SSCAN key cursor [MATCH pattern] [COUNT count]` 迭代集合中的元素

### Redis Sorted Set
* `ZADD key score1 member1 [score2 member2]` 向有序集合添加一个或多个成员，或更新已存在成员分数
* `ZCARD key` 获取有序集合的成员数
* `ZCOUNT key min max` 计算有序集合指定分数区间的成员数
* `ZINCRBY key increment member` 有序集合对指定成员的分数增加increment
* `ZINSERTSTORE destination numKeys key [key...]` 计算给定的一个或多个有序集合的并集并将结果集存储在新的有序集合key中
* `ZLEXCOUNT key min max` 计算有序集合指定字典区间内成员的数量
* `ZRANGE key start stop [WITHSCORES]` 通过索引区间返回有序集合指定区间内的成员
* `ZRANGEBYLEX key min max [LIMIT offset count]` 通过字典区间返回有序集合的成员
* `ZRANGEBYSCORE key min max [WITHSCORES][LIMIT]` 通过分数返回有序集合指定区间内的成员
* `ZRANK key member` 返回有序集合指定成员的索引
* `ZREM key member [member...]` 移除有序集合中一个或多个成员
* `ZREMRANGEBYLEX key min max` 移除有序集合中给定的字典区间的所有成员
* `ZREMRANGEBYRANK key start stop` 移除有序集合中给定的排名区间的所有成员
* `ZRENRANGEBYSCORE key min max` 移除有序集合中给定的分数区间的所有成员
* `ZREVRANGE key start stop [WITHSCORES]` 返回有序集合中指定的成员，通过索引，分数从高到低
* `ZREVRANGEBYSCORE key max min [WITHSCORES]` 返回有序集合中指定分数区间的成员，分数从高到低
* `ZREVRANK key member` 返回有序集合中指定成员的排名，有序集成员按分数递减排序
* `ZSCORE key member` 返回有序集中成员的分数值
* `ZUNIONSTORE destination numkeys key [key...]` 计算给定一个或多个有序集的并集，并存储在新的key中
* `ZSCAN key sursor [MATCH pattern][COUNT count]` 迭代有序集合中的元素

### Redis HyperLogLog
用来做基数统计算法，当输入元素的数量或体积非常大时，计算基数所需的空间总是固定的。

* `PFADD key element [element...]` 添加指定元素到HyperLogLog中
* `PFCOUNT key [key...]` 返回给定HyperLogLog的基数估算值
* `PFMERGE destkey sourcekey [sourcekey...]` 将多个HyperLogLog合并为一个HyperLogLog

### Redis 发布订阅
Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息。

* `PSUBSCRIBE pattern [pattern...]` 订阅一个或多个符合给定模式的频道
* `PUBSUB subcommand [argument [argument...]]` 查看订阅与发布系统状态
* `PUBLISH channel message` 将信息发送给指定的频道
* `PUNSUBSCRIBE [pattern [pattern...]]` 退订所有给定模式的频道
* `SUBSCRIBE channel [channel...]` 订阅给定的一个或多个频道信息
* `UNSUBSCRIBE [channel [channel...]]` 退订给定的频道

### Redis 事务


### Redis 脚本

### Redis 连接

### Redis 服务器