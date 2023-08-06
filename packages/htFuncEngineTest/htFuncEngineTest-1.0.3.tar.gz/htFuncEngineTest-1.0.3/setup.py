#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages

import hito

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="htFuncEngineTest",
    version=hito.__version__,
    author="wanglie",
    author_email="lie_wangxy@163.com",
    description="海拓算法可视化配置",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="",
    packages=find_packages(),
    install_requires=[
        'importlib'
        ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
