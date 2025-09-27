# -*- coding: utf-8 -*-
"""
@file:      __init__
@time:      2025/9/28 02:12
@author:    sMythicalBird
"""

"""
写一些基本的工具函数，给其他几个工具子模块调用
"""


"""
日志模块
直接使用logger提供一个名称为root的logger
对于需要debug的场景，可以直接使用logger_manager生成相关的日志器
"""

from utils.basic.logger import (
    logger,
    info,
    error,
    debug,
    warning,
    critical,
    logger_manager,
)





__all__ = [
    "logger",
    "info",
    "error",
    "debug",
    "warning",
    "critical",
    "logger_manager",
]


