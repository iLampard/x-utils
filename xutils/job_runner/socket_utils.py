# -*- coding: utf-8 -*-

from ctypes import *

try:
    from win32gui import (windll,
                          IsWindow,
                          IsWindowVisible,
                          GetWindowText,
                          EnumWindows)

    user32 = windll.user32
    kernel32 = windll.kernel32
    psapi = windll.psapi
except ImportError:
    pass
import pandas as pd


# 枚举窗口的回调函数
def enum_windows_callback(hwnd, mouse):
    pid = c_ulong()
    # if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
    try:
        if IsWindow(hwnd) and IsWindowVisible(hwnd):
            # if IsWindow(hwnd):
            user32.GetWindowThreadProcessId(hwnd, byref(pid))
            caption = GetWindowText(hwnd)
            if len(caption) == 0:
                return
            global handles, pids, captions
            handles.append(hwnd)
            pids.append(pid.value)
            captions.append(caption)
    except NameError:
        pass


# 供外部调用
def get_window_info():
    global handles, pids, captions
    handles = []
    pids = []
    captions = []
    try:
        EnumWindows(enum_windows_callback, 0)  # 枚举所有窗口
    except NameError:
        pass
    handle_df = pd.DataFrame(data={'handle': handles, 'pid': pids, 'caption': captions})
    return handle_df


