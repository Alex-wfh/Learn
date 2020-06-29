#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import __main__ as main

def doFunc(func_name=None):
    main_file = vars(main)
    func_name = func_name if func_name else getLatestFuncName(main_file) 
    func = main_file[func_name]
    print('function name: {}\ndoc: {}\ndo:'.format(func_name, func.__doc__))
    result = func()
    print('end')
    print('result: {}'.format(result))

def getLatestFuncName(main_file):
    names = [int(func[4:]) for func in main_file.keys() if func.startswith('func')]
    names.sort()
    return 'func' + str(names[-1])
