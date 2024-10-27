from abc import ABC, abstractmethod

import cv2
import numpy as np
from ppadb.client import Client as AdbClient


class PhoneController(ABC):
    @abstractmethod
    def get_client_host(self):
        ...

    @abstractmethod
    def get_phone_id(self):
        ...

    def __init__(self):
        self.adb = AdbClient(host=self.get_client_host())
        self.device = self.adb.device(self.get_phone_id())

    def unlock_phone(self):
        self.device.shell("input keyevent 82")
        self.device.shell("input swipe 0 500 0 0")

    def lock_phone(self):
        self.device.shell("input keyevent 26")

    def open_application(self, package: str, activity: str):
        self.device.shell(f"am start -n {package}/{activity}")

    def close_application(self, package: str):
        self.device.shell(f"am force-stop {package}")

    def take_screenshot(self) -> np.array:
        screenshot_path = "./data/screenshot.png"
        self.device.shell("screencap /sdcard/Pictures/screenshot.png")
        self.device.pull("sdcard/Pictures/screenshot.png", screenshot_path)
        return cv2.imread(screenshot_path)

    def tap(self, x: int, y: int):
        self.device.shell(f"input tap {x} {y}")
