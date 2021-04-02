# Redis 命令归纳

## 通用名词

### 数据结构名词

| 表示       | 结构        |
| ---------- | ----------- |
| 默认（空） | String      |
| H          | Hash        |
| L          | List        |
| S          | Set         |
| Z          | Zset        |
| PF         | Hyperloglog |
| BIT        | Bitmap      |
| GEO        | Geospatial  |
| X          | Stream      |

### 其他名词

| KEYS   | 键     |
| ------ | ------ |
| VALS   | 值     |
| MEMBER | 成员   |
| FLOAT  | 浮点数 |
| STR    | 字符   |
| SCORE  | 分数   |

## 通用动词

| SET     | 设置         |
| ------- | ------------ |
| GET     | 取           |
| PUSH    | 推入         |
| POP     | 弹出         |
| REM     | 删除         |
| DEL     | 删除         |
| UNLINK  | 非阻塞删除   |
| FLUSH   | 删除         |
| TTL     | 查询过期时间 |
| EXISTS  | 判断是否存在 |
| EXPIRE  | 设置过期时间 |
| PERSIST | 删除过期时间 |
| STORE   | 转存         |
| ADD     | 加           |
| APPEND  | 追加         |
| INCR    | 自增         |
| DECR    | 自减         |
| MEMBERS | 求成员       |
| COUNT   | 数量         |
| CARD    | 数量         |
| LEN     | 长度         |
| INDEX   | 序号         |
| RANK    | 排名         |
| RANGE   | 范围         |
| TRIM    | 裁剪         |
| MERGE   | 合并         |
| UNION   | 并集         |
| INTER   | 交集         |
| SCAN    | 迭代         |
| DIFF    | 找不同       |
| RANDOM  | 随即返回     |
| RENAME  | 重命名       |
| POS     | 位置         |
| HASH    | 哈希         |
| DIST    | 求距离       |
| RADIUS  | 半径范围内   |
| FIELD   | 处理         |
| OP      | 处理         |
| SORT    | 排序         |

## 通用形容词

| BG   | 后台         |
| ---- | ------------ |
| L    | 左           |
| R    | 右           |
| B    | 阻塞         |
| MIN  | 最小         |
| MAX  | 最大         |
| M    | 多个         |
| NX   | 如果不存在   |
| X    | 如果存在     |
| P    | 毫秒级       |
| EX   | 伴随过期时间 |
| UN   | 否定         |
| IS   | 判断         |
| RAND | 随机的       |
| LEX  | 范围性的     |
| REV  | 反向         |

## 通用副词

| BY   |
| ---- |
| AT   |

## 特殊命令

### 数据库

| TYPE     | 返回保存的数据类型    |
| -------- | --------------------- |
| TIME     | 返回服务器时间        |
| PING     | ping                  |
| MONITOR  | 监听                  |
| SELECT   | 选数据库              |
| WAIT     | 等待                  |
| COMMAND  | 命令大全              |
| DBSIZE   | 键数量                |
| ACL      | 访问控制              |
| CLIENT   | 客户端                |
| CONFIG   | 配置                  |
| MEMORY   | 管理内存              |
| DUMP     | 序列化                |
| ECHO     | 打印                  |
| LATENCY  | 潜在的，分析Redis状态 |
| MOVE     | 移动                  |
| TOUCH    | 返回多个key存在的数量 |
| SHUTDOWN | 软关闭服务端          |
| QUIT     | 关闭连接              |
| SWAPDB   | 交换数据库            |
| INFO     | 服务端详情            |

### 事务

| MULTI   | 开始事务       |
| ------- | -------------- |
| EXEC    | 执行事务       |
| WATCH   | 监听           |
| DISCARD | 放弃事务中命令 |

### Lua

| SCRPIT | Lua 脚本       |
| ------ | -------------- |
| SHA    | Lua 脚本的 key |
| EVAL   | 执行 Lua 脚本  |

### 持久化

| AOF     | append only file |
| ------- | ---------------- |
| RDB     | Redis database   |
| SAVE    | 静态化           |
| REWRITE | 重写             |

### 发布与订阅

| P         | 模式              |
| --------- | ----------------- |
| SUBSCRIBE | 订阅              |
| PUBSUB    | 订阅/发布系统状态 |
| PUBLISH   | 发布              |

### 模块

| MODULE | 模块 |
| ------ | ---- |
| LOAD   | 载入 |

### 多机

| CLUSTER     | 集群               |
| ----------- | ------------------ |
| SLOT        | 槽                 |
| REPLICA     | 复制               |
| SLAVE       | 奴役               |
| ROLE        | 实例在复制中的角色 |
| RESET       | 重置               |
| SYNC、PSYNC | 同步主从服务器     |

