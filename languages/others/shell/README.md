# Shell
Shell本身是一个用 C 语言编写的解释型语言，它是用户使用 Unix/Linux 的桥梁。Shell既是一种命令语言，又是一种程序设计语言。
### Shell的两种执行方法
* 交互式(Interactive)
* 批处理(Batch)

### 常见的Shell种类
* bash: Linux默认Shell
* sh: Unix默认Shell

### Shell变量
##### 定义
`variableName="value"`

* 变量名、等号、变量值之间不能存在空格
* 首个字符必须是字母
* 不能有空格，可以有下划线(`-`)
* 不能使用标点符号
* 不能使用Bash关键字

##### 使用
`$variableName` or `${variableName}`

##### 只读变量
`readonly variableName`

##### 删除变量
`unset variableName`

### 特殊变量
* `$0` 当前脚本文件名
* `$n` 传递给脚本或函数的参数，n是数字，代表第几个参数。
* `$#` 传递给脚本或函数的参数个数
* `$*` 传递给脚本或函数的所有参数
* `$@` 传递给脚本或函数的所有参数，被`""`包含时会将各参数分开
* `$?` 上个命令的退出状态，或函数的返回值
* `$$` 当前Shell进程ID

### Shell替换
##### 命令替换
Shell可以先执行命令，将结果保存，在适当的地方输出。
``USER=`who | wc -l` ``

##### 变量替换
根据变量的状态(是否为空、是否定义等)来改变它的值。

* `${var}` 变量本来的值
* `${var:-word}` 如果var为空或未定义，返回word，但不改变var的值
* `${var:=word}` 如果var为空或未定义，返回word，并将var的值设置为word
* `${var:?message}` 如果var为空或未定义，那么将message送到标准错误输出，且脚本停止运行
* `${var:+word}` 如果var被定义，返回word，但不改变var的值

### Shell运算符
##### 算术运算符
原生 bash 不支持简单的数学运算，但是可以通过其他命令来实现，例如 awk 和 expr，expr 最常用。

`+` `-` `*` `/` `%` `=` `==` `!=`
##### 关系运算符
关系运算符只支持数字，不支持字符串，除非字符串的值是数字。

`-eq` `-ne` `-gt` `-lt` `-ge` `-le`
##### 布尔运算符
`!` `-o` `-a`
##### 字符串运算符
`=` `!=` `-z` `-n` `str`
##### 文件测试运算符
`-b` `-c` `-d` `-f` `-g` `-k` `-p` `-u` `-r` `-w` `-x` `-s` `-e`

### Shell字符串
##### 单引号
单引号中任何字符都会原样输出  

`str='this is a string'`

##### 双引号
双引号中可存在变量及转义字符  

```
s='string'  
str="this is a $s"
```

##### 拼接字符串
```
name='Alex'
greeting="hello, "$name" !"
greeting_1="hello, ${name} !"

echo $greeting $greeting_1
```

##### 获取字符串长度
```
string="abcd"
echo ${#string}
```

##### 提取子字符串
```
string="abcdefg"
echo ${string:1:4}
```

### Shell数组
##### 定义数组
```
array_name=(v0 v1 v2 v3 v4)

array_name[0]=v0
array_name[1]=v1
array_name[2]=v2
array_name[3]=v3
```

##### 读取数组
```
${array_name[index]}
```

##### 获取数组长度
```
${#array_name[@]}
${#array_name[*]}
${#array_name[n]}
```

### 条件语句
###### if else
```
if [ expression ]
then
	Statement(s) to be executed if expression is true
fi

if [ expression ]
then
	Statement(s) to be executed if expression is true
else
	Statement(s) to be executed if expression is false
fi

if [ expression1 ]
then
	Statement(s) to be executed if expression1 is true
elif [ expression2 ]
	Statement(s) to be executed if expression2 is true
then
	Statement(s) to be executed if no expression is true
fi
```

##### case
```
case value in
v1)
	command1
	command2
	;;
v2)
	command1
	command2
	;;
*)
	command1
	command2
	;;
esac
```

### 循环语句
##### for
```
for v in array
do
	command1
	command2
done
```

##### while
```
while command
do
	Statement(s) to be executed if command is true
done
```

##### until
```
until command
do
	Statement(s) to be executed until command is true
done
```

##### break continue
`break` `break n` `continue`

### Shell函数
##### 函数定义
```
function_name1(){
	return 'this is a function!'
}

function function_name2(){
	echo $1
	echo $2
}
```

##### 函数调用
```
function_name1

function_name2 a b
```

### Shell输入输出
##### echo
`echo str`

##### printf
echo命令的升级版，不自动换行

`printf str\n`

##### 重定向
```
command > file
command >> file

command < file
```

### 文件包含
```
. filename
source filename
```