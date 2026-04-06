#!/usr/bin/env python3
# -*- coding: utf8 -*-
import time
import ctypes
import pyautogui
import keyboard
import pygetwindow
from PIL import Image

import win32gui
import win32ui
import win32con

from loguru import logger


class Base(object):
    logger = logger
    def __init__(self, window_title):
        self.window_title = window_title
        self.hwnd = None
        self.window_offset = (0, 0)

    def find_window(self):
        try:
            wins = pygetwindow.getWindowsWithTitle(self.window_title)
            if not wins:
                raise Exception(f"未找到窗口")
            win = wins[0]
            win.activate()
            win.moveTo(0, 0)
            win.resizeTo(500, 900)
            time.sleep(2)
            self.hwnd = win32gui.FindWindow(None, self.window_title)
            if not self.hwnd:
                raise Exception("获取窗口句柄失败")

            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            self.logger.info(f"窗口位置: ({left}, {top}), 大小: {right - left}x{bottom - top}")
            if left < 0 or top < 0:
                raise Exception("获取窗口位置失败")

            win32gui.SetWindowPos(self.hwnd, 0, 0, 0, 500, 900,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)
            self.window_offset = (left, top)
            return True
        except Exception as e:
            self.logger.error(f"查找窗口({self.window_title})失败: {e}, 请重新启动-{self.window_title}应用")
            return False

    def capture_window_printwindow(self):
        """使用PrintWindow API后台截图"""
        if not self.hwnd:
            if not self.find_window():
                return None

        try:
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            width, height = right - left, bottom - top
            # self.logger.info(f'width: {width}, height: {height}, left: {left}, top: {top}')

            if width <= 0 or height <= 0:
                self.logger.warning(f"窗口尺寸异常: {width}x{height}")
                return False

            # 获取窗口设备上下文
            hwndDC = win32gui.GetWindowDC(self.hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            # 创建位图
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

            # 将位图选入设备上下文
            old_obj = saveDC.SelectObject(saveBitMap)

            # 使用PrintWindow代替BitBlt
            # PW_RENDERFULLCONTENT = 0x00000002 (Windows 8.1+)
            result = ctypes.windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 2)

            if result == 0:
                # 如果失败,尝试不使用PW_RENDERFULLCONTENT
                result = ctypes.windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0)

            # 恢复原对象
            saveDC.SelectObject(old_obj)

            if result == 0:
                self.logger.warning("PrintWindow调用失败")
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwndDC)
                return False

            # 转换为PIL图像并保存
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            # im.save('captured_image.png')

            # 清理资源
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwndDC)

            return im
        except Exception as e:
            self.logger.warning(f"截图异常: {e}")
            return None

    def capture_window_bitblt(self):
        """使用BitBlt截图"""
        if not self.hwnd:
            if not self.find_window():
                return None

        try:
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            width, height = right - left, bottom - top
            self.logger.info(f'width: {width}, height: {height}, left: {left}, top: {top}')

            hwndDC = win32gui.GetWindowDC(self.hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

            saveDC.SelectObject(saveBitMap)

            saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0),
                          win32con.SRCCOPY | 0x40000000)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwndDC)

            return im
        except Exception as e:
            self.logger.warning(f"截图失败: {e}")
            return False