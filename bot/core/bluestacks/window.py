import os
import subprocess
import ctypes

import pygetwindow
import pyautogui
import time
import numpy
import win32api
import win32con
import win32gui


from dataclasses import dataclass, field
from subprocess import Popen, call, DEVNULL


def left_click(hwnd, pos: [str]):
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

    def _execute_cmd(self):
        raise NotImplementedError

    @staticmethod
    def get_pid(instance_title):
        # cmd = f'tasklist /fi "WINDOWTITLE eq {instance_title}"'

        result = subprocess.run(['tasklist', '/fi', f'WINDOWTITLE eq {instance_title}', '/fo', 'csv', '/nh'],
                                capture_output=True, text=True)

        try:
            stdout = result.stdout.split(',')
            pid = stdout[1].strip('"')

            return pid
        except IndexError as e:
            return False

    @staticmethod
    def get_whndl(process_title):
        return win32gui.FindWindowEx(0, 0, None, f'{process_title}')

    def get_title(self, pid):
        raise NotImplementedError

    @staticmethod
    def get_all_titles():
        titles = []

        def enumHandler(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                titles.append(win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(enumHandler, None)

        return titles

    def get_window(self, window_title):
        whndl = self.get_whndl(window_title)
        return whndl

    def moveTo(self, x, y):
        raise NotImplementedError

    def resize(self):
        raise NotImplementedError
    @staticmethod
    def start_process(path: str):
        process = Popen(path)
        return process

    # TODO
    # move to bluestacks class
    def close(self, instance_title):
        pid = self.get_pid(instance_title)
        call(f"TASKKILL /PID {pid}", stdout=DEVNULL)
        time.sleep(0.5)

        if self.is_title(f'Close {instance_title}'):
            close_whndl = self.get_whndl(f'Close {instance_title}')
        else:
            close_whndl = self.get_whndl(f'BlueStacks Exit Window')

        region = win32gui.GetWindowRect(close_whndl)
        dx, dy = find_close_btn([*region])
        left_click(close_whndl, (dx, dy))

    def is_process(self, instance_title):
        if self.get_pid(instance_title):
            return True
        else:
            return False

    def is_title(self, instance_title):
        if instance_title in self.get_all_titles():
            return True
        else:
            return False
