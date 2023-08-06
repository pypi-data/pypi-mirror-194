# -*- coding: utf-8 -*- 
"""
========================================================================================================================
@project : pypi
@file: setup.py
@Author: mengying
@email: 652044581@qq.com
@date: 2023/3/1 13:53
@desc: 
========================================================================================================================
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "passaosfriday",
    version = "1.0.1",
    author = "mengying",
    description = "签名数据封装",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/longweiqiang/dada_openapi_python",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires = [
                           'requests==2.27.1',
                       ],
   python_requires = '>=3.6'

)