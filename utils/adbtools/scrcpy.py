# -*- coding: utf-8 -*-
"""
@file:      scrcpy
@time:      2025/9/27 03:53
@author:    sMythicalBird
"""
import subprocess

class ScrcpyController:
    def __init__(self, controller):
        self.controller = controller
        self.processes = {}

    def start(self, serial: str, max_width=None, bit_rate=None):
        cfg = self.controller.config
        max_width = max_width or cfg.default_max_width
        bit_rate = bit_rate or cfg.default_bit_rate
        cmd = [
            cfg.scrcpy_binary, "-s", serial,
            "--max-size", str(max_width),
            "--bit-rate", bit_rate
        ]
        proc = subprocess.Popen(cmd)
        self.processes[serial] = proc

    def stop(self, serial: str):
        proc = self.processes.pop(serial, None)
        if proc:
            proc.terminate()