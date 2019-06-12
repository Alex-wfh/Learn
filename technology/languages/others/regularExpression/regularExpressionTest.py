#!usr/bin/env python
# -*- coding: utf-8 -*-

import re

string = "<div id='123' name='456'>reTest</div>"

def double( matched ) :
    value = matched.group('value')
    return str(2*int(value))

"""
r = re.match("^\<.*?\>", string, flags=0)

r = re.search("(?<=\>)\w+(?=\<)", string, flags=0)

if r :
    print r.group()
else :
    print 'not match!'
"""

r = re.sub("(?P<value>(?<=\=\')\d+?(?=\'\>))", double, string, count=0, flags=0)

print r


