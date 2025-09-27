# -*- coding: utf-8 -*-
"""
@file:      __init__
@time:      2025/9/28 01:59
@author:    sMythicalBird
"""
"""
将封装好的一些类的常用功能暴漏出来直接调用
"""

"""
基本功能模块：
1、日志管理
2、文件管理，单例文件控制类

"""
from .basic import logger_manager, logger   # logger_manager用于新增日志器分类，logger可以直接使用



__all__ = [
    "logger_manager",
    "logger",
]

