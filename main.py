# -*- coding: utf-8 -*-
"""
@file:      main.py
@time:      2025/9/26 04:59
@author:    sMythicalBird
"""
from utils.logger import logger_manager

logger = logger_manager.get_logger(__name__)

def test():
    logger.info("测试日志系统")
    logger.debug("调试信息")
    logger.warning("警告信息")
    try:
        1 / 0
    except Exception as e:
        logger.error("捕获到异常", extra={"error": str(e)})


if __name__ == "__main__":
    test()
