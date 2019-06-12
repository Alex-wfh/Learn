#!/usr/bin/env python
# -*-coding: utf-8 -*-

try :
    from setuptools import setup
except :
    from distutils.core import setup
setup(
    name='wx_sdk',
    version='1.0.5',
    description='wangxiang Python SDK',
    long_description=open('README.txt').read(),
    author='wanxiang',
    author_email='wanxiang@jd.com',
    maintainer='wanxiang',
    maintainer_email='wanxiang@jd.com',
    license='BSD License',
    packages=['wx_sdk'],
    url='https://wx.jcloud.com/',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
