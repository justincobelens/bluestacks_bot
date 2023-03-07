import ctypes

import win32api
import win32con
import win32gui

from bot.bluestacks.window_test import BaseWindow

class RECT(ctypes.Structure):
    """A nice wrapper of the RECT structure.

    Microsoft Documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/dd162897(v=vs.85).aspx
    """
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]

def _get_all_titles():
    titles = []

    def enum_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            titles.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_handler, None)

    return titles


def get_all_titles():
    return [window.title for window in _get_all_titles()]


def get_windows_with_title(title):
    hWnds_titles = _get_all_titles()

    window_objects = []
    for hWnd, winTitle in hWnds_titles:
        if title.upper() in winTitle.upper():
            window_objects.append(Win32Window(hWnd))

    return window_objects


def get_all_windows():
    hWnds_titles = _get_all_titles()

    window_objects = []
    for hWnd, winTitle in hWnds_titles:
        window_objects.append(Win32Window(hWnd))

    return window_objects


class Win32Window(BaseWindow):
    def __init__(self, hWnd):
        self._hWnd = hWnd
        self._setup_rect_properties()

    def _get_window_rect(self):
        rect = RECT()
        result = ctypes.windll.user32.GetWindowRect(self._hWnd, ctypes.byref(rect))
        if result != 0:
            return rect.left, rect.top, rect.right, rect.bottom
        else:
            raise NotImplementedError



window = get_windows_with_title("BlueStacks App Player 1")[0]
print(window._hWnd)
print(window._get_window_rect())

# all_windows = get_all_windows()
# print(all_windows)
