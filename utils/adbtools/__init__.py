# -*- coding: utf-8 -*-
"""
@file:      __init__
@time:      2025/9/27 03:51
@author:    sMythicalBird
"""

from .core import AndroidController
from .config import AdbControllerConfig

# 可选：暴露子模块
from .device_manager import DeviceManager
from .scrcpy_controller import ScrcpyController

__all__ = [
    "AndroidController",
    "AdbControllerConfig",
    "DeviceManager",
    "ScrcpyController"
]


# adbtools/
# ├── __init__.py
# ├── core.py           # 核心控制器
# ├── devices.py        # 设备管理
# ├── scrcpy.py         # Scrcpy 投屏
# ├── automation.py     # 自动化操作（点击、滑动）
# ├── config.py         # 配置管理
# └── utils.py          # 工具函数
