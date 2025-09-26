# -*- coding: utf-8 -*-
"""
@file:      core.py
@time:      2025/9/27 03:52
@author:    sMythicalBird
"""

import logging
from .config import AdbControllerConfig
from adbutils import AdbClient

from .devices import DeviceManager
from .scrcpy import ScrcpyController
from .automation import AutomationHelper


logger = logging.getLogger(__name__)


class AndroidController:
    _instance = None

    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config=None):
        if hasattr(self, 'initialized'):
            return

        self.config = config or AdbControllerConfig()
        self.adb_client = AdbClient(host=self.config.adb_host, port=self.config.adb_port)

        # 子功能模块（组合模式）
        self.devices = DeviceManager(self)
        self.scrcpy = ScrcpyController(self)
        self.auto = AutomationHelper(self)

        self.initialized = True
        logger.info("AndroidController 初始化完成")