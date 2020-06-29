#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
###############################################################################
the scanner (lexical analyser)
扫描器 (词法分析器)
###############################################################################
"""

import string
class SyntaxError(Exception): pass           # local errors
class LexicalError(Exception): pass          # used to be strings

class Scanner:
    def __init__(self, text):
        self.next = 0
        self.text = text + '\0'

    def newtext(self, text):
        Scanner.__init__(self, text)

    def showerror(self):
        print('=> ', self.text)
        print('=> ', (' ' * self.start) + '^')

    def match(self, token):
        if self.token != token:
            raise SyntaxError(token)
        else:
            value = self.value
            if self.token != '\0':
                self.scan()                  # next token/value
            return value                     # return prior value

    def scan(self):
        self.value = None
        ix = self.next                            # 注意，这里光标从self.next开始移动
        while self.text[ix] in string.whitespace: # 跳过开通空字符
            ix += 1
        self.start = ix

        if self.text[ix] in ['(', ')', '-', '+', '/', '*', '\0']: # 以特定字符开头，记录token
            self.token = self.text[ix]
            ix += 1

        elif self.text[ix] in string.digits: # 以数字开头，设置token为num并记录数字值
            v_str = ''
            while self.text[ix] in string.digits:
                v_str += self.text[ix]
                ix += 1
            if self.text[ix] == '.': # 处理小数
                v_str += '.'
                ix += 1
                while self.text[ix] in string.digits:
                    v_str += self.text[ix]
                    ix += 1
                self.token = 'num'
                self.value = float(v_str)
            else:
                self.token = 'num'
                self.value = int(v_str)           # subsumes long() in 3.x

        elif self.text[ix] in string.ascii_letters: # 以字母开头，如果是字符串是set设置token为set，否则设置token为var并记录value值
            v_str = ''
            while self.text[ix] in (string.digits + string.ascii_letters):
                v_str += self.text[ix]
                ix += 1
            if v_str.lower() == 'set':
                self.token = 'set'
            else:
                self.token = 'var'
                self.value = v_str

        else: # 未匹配到合法值，报错
            raise LexicalError()
        self.next = ix # 移动光标
