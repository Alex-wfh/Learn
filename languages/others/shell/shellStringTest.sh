#!/bin/bash

#单引号双引号区别
s='string'
echo 'this is a $s'
echo "this is a $s"

#拼接字符串
name='Alex'
echo 'Hello, '$name' !'
echo "Hello, $name !"
echo "Hello, ${name} !"
echo Hello, ${name} !

#获取字符串长度
s='abcdefg'
echo length of s is ${#s}

#提取子字符串
s='abcdefg'
echo ${s:1:4}

