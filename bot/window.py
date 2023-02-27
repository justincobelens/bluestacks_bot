import os

import pygetwindow
import pyautogui
import time
import numpy
import win32api
import win32con
import win32gui

from subprocess import Popen, call, DEVNULL


def left_click(hwnd, pos):
    lParam = win32api.MAKELONG(pos[0], pos[1])

    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    time.sleep(0.1)


def find_close_btn(region):
    image = pyautogui.screenshot(region=region)

    image = numpy.array(image, dtype=numpy.uint8)
    pixel_color = [235, 85, 62]

    for i in range(0, len(image), 5):
        for j in range(0, len(image[i]), 5):
            if list(image[i][j]) == pixel_color:
                return j, i


class Window:

    def __init__(self):
        self.process = None

    def open(self, path: str):
        self.process = Popen(path)

    def close(self, instance_title):
        process = call(f"TASKKILL /PID {self.process.pid}", stdout=DEVNULL)
        time.sleep(0.5)
        if self.is_window(f'Close {instance_title}'):
            close_whndl = win32gui.FindWindowEx(0, 0, None, f'Close {instance_title}')
        else:
            close_whndl = win32gui.FindWindowEx(0, 0, None, f'BlueStacks Exit Window')

        region = win32gui.GetWindowRect(close_whndl)
        dx, dy = find_close_btn([*region])
        left_click(close_whndl, (dx, dy))

    @staticmethod
    def is_window(instance_title: str):
        if len(pygetwindow.getWindowsWithTitle(instance_title)) != 0:
            return True
        else:
            return False

    def wait_for_process(self, state: str):
        for _ in range(0, 60):
            process = self.in_process()

            if state == 'start' and process is True:
                return True
            elif state == 'stop' and process is False:
                return True

            time.sleep(1)
        return False

    def wait_for_window(self, instance_title: str):
        for _ in range(0, 60):
            if self.is_window(instance_title):
                return True
            time.sleep(1)
        return False

    def in_process(self):
        tasklist = os.popen("tasklist").read().split()
        if str(self.process.pid) in tasklist:
            return True
        else:
            return False

    @staticmethod
    def arrange(window_title, region: list):
        bluestacks_window = pygetwindow.getWindowsWithTitle(window_title)[0]

        # set position of window
        bluestacks_window.moveTo(region[0], region[1])

        # set size of window
        bluestacks_window.resizeTo(region[2], region[3])

