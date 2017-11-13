#!/bin/bash

a=1
b=2
c=3

#算术运算符
echo '算术运算符'
echo a+b=`expr $a + $b`
echo a-b=`expr $a - $b`
echo a*b=`expr $a \* $b`
echo a/b=`expr $a / $b`
echo a%b=`expr $a % $b`

a=$c

if [ $a == $b ]
then
    echo 'a == b'
fi

if [ $a != $b ]
then
    echo 'a != b'
fi

#关系运算符
echo '关系运算符'
echo "a is $a"
echo "b is $b"

if [ $a -eq $b ]
then
    echo 'a is equal to b'
else
    echo 'a is not equal to b'
fi

if [ $a -ne $b ]
then
    echo 'a is not equal to b'
else
    echo 'a is equal to b'
fi

if [ $a -gt $b ]
then 
    echo 'a is greater than b'
else
    echo 'a is not greater than b'
fi

if [ $a -lt $b ]
then
    echo 'a is less than b'
else
    echo 'a is not less than b'
fi

if [ $a -ge $b ]
then
    echo 'a is greater than or equal to b'
else
    echo 'a is not greater than or equal to b'
fi

if [ $a -le $b ]
then
    echo 'a is less than or equal to b'
else
    echo 'a is not less than or equal to b'
fi

#布尔运算符
echo '布尔运算符'
echo "a is $a"
echo "b is $b"
echo "c is $c"
if [ ! $a == $b ]
then
    echo 'a is not equal to b'
else
    echo 'a is equal to b'
fi

if [ $a == $b -o $a == $c ]
then
    echo 'a is equal to b or a is equal to c'
else
    echo 'a is not euqal to b and a is not equal to c'
fi

if [ $a == $b -a $a == $c ]
then
    echo 'a is equal to b and a is equal to c'
else
    echo 'a is not equal to b or a is not equal to c'
fi

#字符串运算符
echo '字符串运算符'
a='abc'
b='def'
echo "a is $a"
echo "b is $b"

if [ $a = $b ]
then
    echo 'str a is equal to str b'
else
    echo 'str a is not equal to str b'
fi

if [ $a != $b ]
then
    echo 'str a is not equal to str b'
else
    echo 'str a is equal to str b'
fi

if [ -z $a ]
then
    echo 'length of str a is zero'
else
    echo 'length of str a is not zero'
fi

if [ -n $a ]
then
    echo 'length of str a is not zero'
else
    echo 'length of str a is zero'
fi

if [ $a ]
then
    echo 'str a is not empty'
else
    echo 'str a is empty'
fi
