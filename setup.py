#! /usr/bin/env python
# coding:utf-8

from setuptools import setup


setup(
    name="typecheck",
    version="0.1",
    description="Type check module",
    author="Noriyuki Abe",
    author_email="kenko.py@gmail.com",
    url="http://kenkov.jp",
    #packages=find_packages(),
    py_modules=["expression", "typecheck"],
    test_suite="test"
)
