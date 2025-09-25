# -*- coding: utf-8 -*-
"""
@file:      __init__.py
@time:      2025/9/26 04:58
@author:    sMythicalBird
"""
"""
日志模块入口，提供简洁的导入方式。
"""

# 直接使用logger提供一个名称为root的logger
# 对于需要debug的场景，可以直接使用logger_manager生成相关的日志器


from .logger import (
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