#!/usr/bin/env python
# -*-coding: utf-8 -*-

try :
    from setuptools import setup
except :
    from distutils.core import setup
setup(
    name='wx-sdk',
    version='1.0.0',
    description='wangxiang Python SDK',
    long_description=open('README.txt').read(),
    author='Alex',
    author_email='wufeihao@jd.com',
    maintainer='Alex',
    maintainer_email='wufeihao@jd.com',
    license='BSD License',
    packages=['wx-sdk'],
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
    ],
)
