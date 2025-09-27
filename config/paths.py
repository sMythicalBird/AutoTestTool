# -*- coding: utf-8 -*-
"""
@file:      paths
@time:      2025/9/28 03:09
@author:    sMythicalBird
"""

"""
统一的项目路径管理模块
"""
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent.resolve()

# 路径字典
PATHS = {
    "root":     ROOT_DIR,
    "res":      ROOT_DIR / "res",
    "config":   ROOT_DIR / "config",
    "tests":    ROOT_DIR / "tests",
    "tools":    ROOT_DIR / "tools",
    "utils":    ROOT_DIR / "utils",
    "logs":     ROOT_DIR / "logs",
}




def setup_directories():
    """创建必要的目录"""
    for name, path in PATHS.items():
        if name != "root":  # root 是项目根，不需要创建
            path.mkdir(exist_ok=True, parents=True)
            print(f"📁 确保目录存在: {path} ({name})")

# 可在项目启动时调用
# setup_directories()
