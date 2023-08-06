# -*- coding: utf-8 -*- 
"""
========================================================================================================================
@project : pypi
@file: Pass
@Author: mengying
@email: 652044581@qq.com
@date: 2023/3/1 13:51
@desc: 
========================================================================================================================
"""
import requests

class PassFile:

    def upload(self):
        session = requests.session()
        print('start upload')