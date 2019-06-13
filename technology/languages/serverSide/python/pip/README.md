# 上传pip包
### 注册pypi账号
登陆[pypi官网](https://pypi.python.org/pypi)，注册用户并验证邮箱

### 创建目录
按下方目录结构创建文件夹

```
pip-demo #上传pip包所用目录
├── README.txt #较长的说明文件
├── setup.py #pip上传的python文件
└── pip_demo #pip包
    ├── __init__.py
    └── pip_demo.py
```

setup.py文件内容如下

```
#!/usr/bin/env python
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
```

### 上传包
Install twine

```
pip install twine
```
Install wheel

```
pip install wheel
```
Create some distributions in the normal way

```
python setup.py sdist bdist_wheel
```
Upload with twine

```
twine upload dist/*
```
Done!

Twine help

```
twine upload -h #help
```
