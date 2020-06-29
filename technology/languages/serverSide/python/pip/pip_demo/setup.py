#!/usr/bin/env python3
# -*-coding: utf-8 -*-

try :
    from setuptools import setup
except :
    from distutils.core import setup
setup(
    name='pip_demo',
    version='varsion',
    description='description',
    long_description=open('README.txt').read(),
    author='authorName',
    author_email='authorEmail',
    maintainer='maintainerName',
    maintainer_email='maintarnerEmail',
    license='BSD License',
    packages=['pip_demo'],
    url='url',
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
