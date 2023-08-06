#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
from setuptools import setup, find_packages

MAJOR = 0
MINOR = 1
PATCH = 7
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

def get_install_requires():
    reqs = []
    return reqs
setup(
	name = "AutoFun",
	version = VERSION,
    author ="wangweidong",
    author_email = "17891967090@163.com",
    description='PDF撕裂者单个功能',
    long_description_content_type="text/markdown",
	url = 'https://mail.163.com/js6/main.jsp?sid=PAlGWIYldfIQjfQTFYllFVEyKXidwtNk&df=mail163_letter#module=welcome.WelcomeModule%7C%7B%7D',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.8",
    install_requires=get_install_requires(),

	packages = find_packages(),
 	license = 'Apache',
   	classifiers = [
       'Programming Language :: Python',

    ],
    #包含的类型
    package_data={'': ['*.csv', '*.txt','.toml', "*.pyd",'*.exe', '*.db']}, #这个很重要
    include_package_data=True #也选上

)