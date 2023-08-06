# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:47:12
# @Author  : Pane Li
# @File    : setup.py
"""

setup

"""
from distutils.core import setup

setup(
    name='inhandtest',
    version='0.0.6',
    author='liwei',
    author_email='liwei@inhand.com.cn',
    description='https://inhandnetworks.yuque.com/irhb08/mrpu1r/qgu0imvigkm2xry9?singleDoc# 《inhandtest docs》',
    maintainer='liwei',
    maintainer_email='liwei@inhand.com.cn',
    py_modules=['inhandtest.tools', 'inhandtest.telnet', 'inhandtest.inmodbus', 'inhandtest.inmqtt', 'inhandtest.file'],
    long_description='inhand test tools, so easy',
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=['pytz', 'modbus_tk', 'serial', 'paho'  # 这里是依赖列表，表示运行这个包的运行某些功能还需要你安装其他的包
    ]
)
