#!/bin/bash

# 函数定义
function_name1(){
	return 123
}

function function_name2(){
	echo $1
	echo $2
}

# 函数调用
function_name1 
echo $?

function_name2 a b

#shell function return can't be string
function_name3(){
    echo 'This is a function!'
}
v=$(function_name3)
echo $v
