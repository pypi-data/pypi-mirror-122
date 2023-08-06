#!PycharmProjects\pythonProject

# -*- coding:utf-8 -*-
# @FileName   :setup.py
# @Time       :2021/10/8 21:25
# @Author     :Gct.windy
# @ProductName:PyCharm

from distutils.core import setup

setup(
    name="GctSuperMath",    #这是我们对外的名字：GctSuperMath
    version="1.0.0",    #版本号
    description="这是第一个对外发布的模块，里面目前只有加法和乘法，仅用于测试",   #对于发布的模块的描述说明
    author="Gctwindy",  #模块的作者
    author_email="windyxuh@163.com",    #作者的邮箱
    py_modules=['GctSuperMath.demo_01','GctSuperMath.demo_02']  #发布的模块
)