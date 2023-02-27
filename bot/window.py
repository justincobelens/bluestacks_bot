import pygetwindow
import json
import time

from subprocess import Popen
from dataclasses import dataclass, field

import const


class Window:

    def __init__(self):
        self.process = None

    def open(self, path: str):
        self.process = Popen(path)

    def close(self):
        pass

    @staticmethod
    def is_window(instance_title: str):
        if len(pygetwindow.getWindowsWithTitle(instance_title)) != 0:
            return True
        else:
            return False

    def wait(self, instance_title: str):
        for _ in range(0, 60):
            if self.is_window(instance_title):
                return
            else:
                time.sleep(1)

    @staticmethod
    def arrange(window_title, region: list):
        bluestacks_window = pygetwindow.getWindowsWithTitle(window_title)[0]

        # set position of window
        bluestacks_window.moveTo(region[0], region[1])

        # set size of window
        bluestacks_window.resizeTo(region[2], region[3])
