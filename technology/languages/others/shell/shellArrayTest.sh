#!/bin/bash

#定义数组
array1=(0 1 2 3 4 5 6 7 8)

array2[0]='abc'
array2[1]='def'
array2[2]='ghi'
array2[3]='jkl'
array2[4]='mn'

#读取数组
echo ${array1[0]}

echo ${array2[1]}

#获取数组长度

echo ${#array1[@]}
echo ${#array2[*]}
echo ${#array2[2]}
