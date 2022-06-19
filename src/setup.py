#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="QQTea",
    version="0.1.0",
    keywords=('crypto', 'qq', 'tea', 'xtea', 'xxtea'),
    description="qq tea crypto lib",
    long_description="qq tea crypto lib support teas",
    license="MIT Licence",
    url="https://github.com/serfend",
    author="serfend",
    author_email="serfend@foxmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'sgt_libc_searcher = sgt_libc_searcher.__main__:main'
        ]
    }
)
