#!/bin/bash

# 条件语句
# if else
echo 'if'
if [ 1 == 1 ]
then
	echo "Statement(s) to be executed if expression is true"
fi

echo 'if else'
if [ 1 == 1 ]
then
	echo "Statement(s) to be executed if expression is true"
else
	echo "Statement(s) to be executed if expression is false"
fi

echo 'if elif'
if [ 1 == 1 ]
then
	echo "Statement(s) to be executed if expression1 is true"
elif [ 2 == 2 ]
	echo "Statement(s) to be executed if expression2 is true"
then
	echo "Statement(s) to be executed if no expression is true"
fi

# case
echo 'case'
case 1 in
1)
	echo '1'
	;;
2)
    echo '2'
	;;
*)
	echo 'else'
	;;
esac

# 循环语句
# for
echo 'for'
for v in 1 2 3 
do
	echo $v
done

# while
echo 'while'
i=0
while [ $i -lt 2 ]
do
    echo $i
    i=`expr $i + 1`
done

# until
echo 'until'
i=0
until [ $i -gt 2 ]
do
    echo $i
    i=`expr $i + 1`
done

#break
echo 'break'
for v in 1 2 3 4
do
    if [ $v == 2 ]
    then
        break
    fi
    echo $v
done

#continue
echo 'continue'
for v in 1 2 3 4
do
    if [ $v == 2 ]
    then
        continue
    fi
    echo $v
done

