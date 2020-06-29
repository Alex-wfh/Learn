#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Separate expression parsing from evaluation by building an explicit parse tree
通过建立一个显式的解析树，将表达式解析与求值分离
"""

TraceDefault = False
class UndefinedError(Exception): pass

from scanner import Scanner, SyntaxError, LexicalError

#################################################################################
# the interpreter (a smart objects tree)
# 解析器 (一个智能的对象树)
#################################################################################

class TreeNode:
    def validate(self, v_dict):           # default error check
        pass
    def apply(self, v_dict):              # default evaluator
        pass
    def trace(self, level):             # default unparser
        print('.' * level + '<empty>')

# ROOTS
# 根节点
class BinaryNode(TreeNode):
    def __init__(self, left, right):            # inherited methods
        self.left, self.right = left, right     # left/right branches
    def validate(self, v_dict):
        self.left.validate(v_dict)                # recurse down branches 向下一层分支递归
        self.right.validate(v_dict)
    def trace(self, level):
        print('.' * level + '[' + self.label + ']')
        self.left.trace(level+3)
        self.right.trace(level+3)

class TimesNode(BinaryNode):
    label = '*'
    def apply(self, v_dict):
        return self.left.apply(v_dict) * self.right.apply(v_dict)

class DivideNode(BinaryNode):
    label = '/'
    def apply(self, v_dict):
        return self.left.apply(v_dict) / self.right.apply(v_dict)

class PlusNode(BinaryNode):
    label = '+'
    def apply(self, v_dict):
        return self.left.apply(v_dict) + self.right.apply(v_dict)

class MinusNode(BinaryNode):
    label = '-'
    def apply(self, v_dict):
        return self.left.apply(v_dict) - self.right.apply(v_dict)

# LEAVES
# 叶节点
class NumNode(TreeNode):
    def __init__(self, num):
        self.num = num                 # already numeric
    def apply(self, v_dict):             # use default validate
        return self.num
    def trace(self, level):
        print('.' * level + repr(self.num))   # as code, was 'self.num'

class VarNode(TreeNode):
    def __init__(self, text, start):
        self.name   = text                    # variable name
        self.column = start                   # column for errors
    def validate(self, v_dict):
        if not self.name in v_dict.keys():
            raise UndefinedError(self.name, self.column)
    def apply(self, v_dict):
        return v_dict[self.name]                # validate before apply
    def assign(self, value, v_dict):
        v_dict[self.name] = value               # local extension
    def trace(self, level):
        print('.' * level + self.name)

# COMPOSITES
# 复合型
class AssignNode(TreeNode):
    def __init__(self, var, val):
        self.var, self.val = var, val
    def validate(self, v_dict):
        self.val.validate(v_dict)               # don't validate var
    def apply(self, v_dict):
        self.var.assign( self.val.apply(v_dict), v_dict )
    def trace(self, level):
        print('.' * level + 'set ')
        self.var.trace(level + 3)
        self.val.trace(level + 3)

#################################################################################
# the parser (syntax analyser, tree builder)
# 解析器 (句法分析器，解析树建立器)
#################################################################################
class Parser:
    def __init__(self, text=''):
        self.lex     = Scanner(text)           # make a scanner
        self.vars    = {'pi':3.14159}          # add constants
        self.traceme = TraceDefault

    def parse(self, *text):                    # external interface
        if text:
            self.lex.newtext(text[0])          # reuse with new text
        tree = self.analyse()                  # parse string
        if tree:
            if self.traceme:                   # dump parse-tree?
                print(); tree.trace(0)
            if self.errorCheck(tree):          # check names
                self.interpret(tree)           # evaluate tree

    def analyse(self):
        try:
            self.lex.scan()                    # get first token
            return self.Goal()                 # build a parse-tree
        except SyntaxError:
            print('Syntax Error at column:', self.lex.start)
            self.lex.showerror()
        except LexicalError:
            print('Lexical Error at column:', self.lex.start)
            self.lex.showerror()

    def errorCheck(self, tree):
        try:
            tree.validate(self.vars)           # error checker
            return 'ok'
        except UndefinedError as instance:     # args is a tuple
            varinfo = instance.args            
            print("'%s' is undefined at column: %d" % varinfo)
            self.lex.start = varinfo[1]
            self.lex.showerror()               # returns None

    def interpret(self, tree):
        result = tree.apply(self.vars)         # tree evals itself
        if result != None:                     # ignore 'set' result
            print(result)                      # ignores errors

    def Goal(self):
        if self.lex.token in ['num', 'var', '(']:
            tree = self.Expr()
            self.lex.match('\0')
            return tree
        elif self.lex.token == 'set':
            tree = self.Assign()
            self.lex.match('\0')
            return tree
        else:
            raise SyntaxError()

    def Assign(self):
        self.lex.match('set')
        vartree = VarNode(self.lex.value, self.lex.start)
        self.lex.match('var')
        valtree = self.Expr()
        return AssignNode(vartree, valtree)               # two subtrees

    def Expr(self):
        left = self.Factor()                              # left subtree
        while True:
            if self.lex.token in ['\0', ')']:
                return left
            elif self.lex.token == '+':
                self.lex.scan()
                left = PlusNode(left, self.Factor())      # add root-node
            elif self.lex.token == '-':
                self.lex.scan()
                left = MinusNode(left, self.Factor())     # grows up/right
            else:
                raise SyntaxError()

    def Factor(self):
        left = self.Term()
        while True:
            if self.lex.token in ['+', '-', '\0', ')']:
                return left
            elif self.lex.token == '*':
                self.lex.scan()
                left = TimesNode(left, self.Term())
            elif self.lex.token == '/':
                self.lex.scan()
                left = DivideNode(left, self.Term())
            else:
                raise SyntaxError()

    def Term(self):
        if self.lex.token == 'num':
            leaf = NumNode(self.lex.match('num'))
            return leaf
        elif self.lex.token == 'var':
            leaf = VarNode(self.lex.value, self.lex.start)
            self.lex.scan()
            return leaf
        elif self.lex.token == '(':
            self.lex.scan()
            tree = self.Expr()
            self.lex.match(')')
            return tree
        else:
            raise SyntaxError()

#################################################################################
# self-test code: use my parser, parser1's tester
# 自测代码: 使用我的解析器, parser1的测试器
#################################################################################
if __name__ == '__main__':
    import testparser
    testparser.test(Parser, 'parser2')    #  run with Parser class here
