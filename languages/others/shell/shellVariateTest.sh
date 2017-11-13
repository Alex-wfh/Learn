#!/bin/bash

# Shell variate

name="Alex"


echo $name

echo ${name}

#readonly name

unset name

echo \$0 is $0

echo \$1 is $1

echo \$# is $#

echo \$* is $*

echo \"\$*\" is "$*"

echo \$@ is $@

echo \"\$@\" is "$@"

echo \$? is $?

echo \$\$ is $$

USER=`who | wc -l`
echo USER is $USER

word="hehe"
echo ${name:-$word}
echo ${name}

echo ${name:=$word}
echo ${name}

message="error"
#unset name 
echo ${name:?$message}

echo ${name:+$word}
echo ${name}
