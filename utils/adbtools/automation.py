# -*- coding: utf-8 -*-
"""
@file:      automation
@time:      2025/9/27 03:53
@author:    sMythicalBird
"""
class AndroidDevice:
    def __init__(self, controller, serial: str):
        self.controller = controller
        self.serial = serial
        self._adb = controller.adb_client.device(serial)

    def tap(self, x, y):
        return self._adb.shell(f"input tap {x} {y}")

    def swipe(self, x1, y1, x2, y2):
        return self._adb.shell(f"input swipe {x1} {y1} {x2} {y2}")

    def screenshot(self, path):
        img = self._adb.screenshot()
        img.save(path)
        return img

class AutomationHelper:
    def __init__(self, controller):
        self.controller = controller

    def batch_tap(self, serial_list, x, y):
        for serial in serial_list:
            dev = self.controller.devices.get(serial)
            dev.tap(x, y)