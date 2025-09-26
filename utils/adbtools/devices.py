# -*- coding: utf-8 -*-
"""
@file:      devices
@time:      2025/9/27 03:52
@author:    sMythicalBird
"""


from .automation import AndroidDevice

class DeviceManager:
    def __init__(self, controller):
        self.controller = controller
        self._devices = {}

    def add(self, serial: str):
        if serial in self._devices:
            return self._devices[serial]
        self._devices[serial] = AndroidDevice(self.controller, serial)
        return self._devices[serial]

    def get(self, serial: str):
        return self._devices.get(serial)

    def list(self):
        return [d.serial for d in self.controller.adb_client.device_list()]

    def remove(self, serial: str):
        self._devices.pop(serial, None)