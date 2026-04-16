#!/usr/bin/env python3
# -*- coding: utf8 -*-
import time

import win32gui
import win32api
import win32con
import ctypes
from ctypes import wintypes

from loguru import logger

vk_constants = {
    name: getattr(win32con, name)
    for name in dir(win32con)
    if name.startswith('VK_')
}

class AutoClick:

    @staticmethod
    def click(hwnd, x, y, button='left'):
        """
        点击指定位置
        :param x: x坐标
        :param y: y坐标
        :param button: 按钮, left/right/middle
        :return:
        """

        if not hwnd:
            logger.warning('窗口句柄无效')
            return False

        try:
            lParam = win32api.MAKELONG(int(x), int(y))

            if button == 'left':
                win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                time.sleep(0.05)
                win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
            elif button == 'right':
                win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
                time.sleep(0.05)
                win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, lParam)
            else:
                logger.info(f"不支持的按钮类型: {button}")
                return False

            return True
        except Exception as e:
            logger.warning(f"后台点击失败: {e}")
            return False

    @staticmethod
    def scroll_window(hwnd=None, delta: int =-1000, x=None, y=None):
        """
        向指定窗口发送滚轮事件
        :param hwnd: 窗口句柄
        :param delta: 滚动量（正数向上，负数向下）
        :param x: 相对于窗口客户区的坐标，默认为窗口中心
        :param y: 相对于窗口客户区的坐标，默认为窗口中心
        :return:
        """

        if x is None or y is None:
            # left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(hwnd)

            # 计算客户区中心
            x = (client_right - client_left) // 2
            y = (client_bottom - client_top) // 2

        wParam = win32api.MAKELONG(0, delta)
        lParam = win32api.MAKELONG(int(x), int(y))

        # 发送滚轮消息
        win32gui.PostMessage(hwnd, win32con.WM_MOUSEWHEEL, wParam, lParam)
        # logger.info(f"滚轮事件: delta={delta}, 位置=({x}, {y})")
        time.sleep(0.1)


    @staticmethod
    def send_key(hwnd, vk_code):
        """发送任意虚拟键码"""
        vk_code = vk_code.upper()
        if vk_code not in vk_constants:
            logger.warning(f"无效的虚拟键码: {vk_code}")
            return
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        time.sleep(0.05)
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("mi", MOUSEINPUT)]


def click_with_sendinput(hwnd, x, y):
    """
    使用SendInput模拟鼠标点击（系统级，100%有效）
    :param hwnd: 窗口句柄
    :param x: 窗口相对X坐标
    :param y: 窗口相对Y坐标
    """
    # 获取窗口位置
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    # 计算屏幕绝对坐标
    screen_x = left + x
    screen_y = top + y

    # 获取屏幕分辨率
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # 转换为SendInput的绝对坐标 (0-65535)
    abs_x = int(screen_x * 65535 / screen_width)
    abs_y = int(screen_y * 65535 / screen_height)

    # 鼠标移动
    mi_move = MOUSEINPUT()
    mi_move.dx = abs_x
    mi_move.dy = abs_y
    mi_move.mouseData = 0
    mi_move.dwFlags = 0x0001 | 0x8000  # MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    mi_move.time = 0
    mi_move.dwExtraInfo = None

    input_move = INPUT()
    input_move.type = 0  # INPUT_MOUSE
    input_move.mi = mi_move

    # 鼠标左键按下
    mi_down = MOUSEINPUT()
    mi_down.dx = 0
    mi_down.dy = 0
    mi_down.mouseData = 0
    mi_down.dwFlags = 0x0002  # MOUSEEVENTF_LEFTDOWN
    mi_down.time = 0
    mi_down.dwExtraInfo = None

    input_down = INPUT()
    input_down.type = 0
    input_down.mi = mi_down

    # 鼠标左键释放
    mi_up = MOUSEINPUT()
    mi_up.dx = 0
    mi_up.dy = 0
    mi_up.mouseData = 0
    mi_up.dwFlags = 0x0004  # MOUSEEVENTF_LEFTUP
    mi_up.time = 0
    mi_up.dwExtraInfo = None

    input_up = INPUT()
    input_up.type = 0
    input_up.mi = mi_up

    # 发送输入
    inputs = (INPUT * 3)(input_move, input_down, input_up)
    ctypes.windll.user32.SendInput(3, inputs, ctypes.sizeof(INPUT))



