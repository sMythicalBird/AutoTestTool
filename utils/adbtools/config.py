# -*- coding: utf-8 -*-
"""
@file:      config
@time:      2025/9/27 03:54
@author:    sMythicalBird
"""
class AdbControllerConfig:
    def __init__(self, **kwargs):
        self.adb_host = kwargs.get("adb_host", "127.0.0.1")
        self.adb_port = kwargs.get("adb_port", 5037)
        self.scrcpy_binary = kwargs.get("scrcpy_binary", "scrcpy")
        self.default_max_width = kwargs.get("default_max_width", 720)
        self.default_bit_rate = kwargs.get("default_bit_rate", "4M")
        self.log_level = kwargs.get("log_level", "INFO")

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)