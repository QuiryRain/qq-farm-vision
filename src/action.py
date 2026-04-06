#!/usr/bin/env python3
# -*- coding: utf8 -*-
import time

import win32gui
import win32api
import win32con

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
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, lParam)
                time.sleep(0.05)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
            elif button == 'right':
                win32gui.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, 0, lParam)
                time.sleep(0.05)
                win32gui.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lParam)
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
        logger.info(f"滚轮事件: delta={delta}, 位置=({x}, {y})")


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


