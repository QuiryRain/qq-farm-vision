#!/usr/bin/env python3
# -*- coding: utf8 -*-
import cv2
import numpy as np
from PIL import Image
from loguru import logger


class RedDotDetector(object):
    def __init__(self, runner):
        self.runner = runner

    def detect_red_dot(self, image=None, rois=None):
        """
        检测红点
        :param image: 完整截图
        :param rois: 感兴趣区域，支持单个 (x1, y1, x2, y2) 或多个区域 [(x1, y1, x2, y2), ...]
        :return: 红点中心坐标列表 [(x, y), ...] 或字典 {roi_id: [(x, y), ...]}
        """
        if image is None:
            image = self.runner.capture_window_printwindow()
        if image is None:
            return []

        if isinstance(image, Image.Image):
            img_np = np.array(image)
        else:
            img_np = image

        # 统一转换为列表格式
        if rois is None:
            rois = {'full': None}

        all_results = {}

        for idx, current_roi in rois.items():
            if current_roi:
                x1, y1, x2, y2 = current_roi
                img_crop = img_np[y1:y2, x1:x2]
            else:
                img_crop = img_np
                x1, y1 = 0, 0
                current_roi = "full_image"

            # 转换到 HSV 色彩空间
            hsv = cv2.cvtColor(img_crop, cv2.COLOR_RGB2HSV)

            # 红色在 HSV 中有两个区间（0-10 和 160-180）
            # 针对小区域红点优化：降低饱和度阈值，提高亮度阈值
            lower_red1 = np.array([0, 50, 80])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 50, 80])
            upper_red2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)

            # 形态学操作，去除噪点
            kernel = np.ones((2, 2), np.uint8)
            dilated_mask = cv2.dilate(mask, kernel, iterations=1)
            eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)

            # 查找轮廓
            contours, _ = cv2.findContours(eroded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            red_dots = []
            for contour in contours:
                area = cv2.contourArea(contour)

                # 根据ROI大小动态调整面积过滤范围
                roi_area = (x2 - x1) * (y2 - y1) if current_roi != "full_image" else \
                img_crop.shape[0] * img_crop.shape[1]

                # 小区域使用更宽松的面积范围
                if roi_area < 10000:  # 小区域
                    min_area, max_area = 10, 500
                else:  # 大区域
                    min_area, max_area = 50, 2000

                # 过滤面积，避免太小（噪点）或太大（背景）
                if min_area < area < max_area:
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"]) + x1
                        cY = int(M["m01"] / M["m00"]) + y1
                        red_dots.append((cX, cY))

            # 使用 ROI 索引或名称作为键
            key = f"{idx}" if current_roi != "full_image" else "full_image"
            all_results[key] = {
                'roi': current_roi,
                'dots': red_dots
            }

        return all_results

    @staticmethod
    def detect_template_in_image(template_img, target_img, threshold=0.8,
                                 method='TM_CCOEFF_NORMED'):
        """
        检测图片A（模板）是否在图片B（目标图）中
        :param template_img: 模板图片（图片A），可以是PIL Image、numpy数组或文件路径
        :param target_img: 目标图片（图片B），可以是PIL Image、numpy数组
        :param threshold: 匹配置信度阈值（0-1），默认0.8
        :param method: 匹配方法，可选：
                       'TM_CCOEFF_NORMED' - 相关系数匹配（推荐）
                       'TM_CCORR_NORMED' - 相关匹配
                       'TM_SQDIFF_NORMED' - 平方差匹配
        :return: 匹配结果列表 [{'top_left': (x, y), 'bottom_right': (x2, y2), 'confidence': score}, ...]
        """

        # 加载图片
        def load_image(img):
            if isinstance(img, str):
                return cv2.imread(img)
            elif isinstance(img, Image.Image):
                return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            elif isinstance(img, np.ndarray):
                return img if len(img.shape) == 3 else cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            else:
                raise ValueError(f"不支持的图片类型: {type(img)}")

        # 转换为numpy数组
        template = load_image(template_img)
        target = load_image(target_img)

        # 检查图像有效性
        if template is None or target is None:
            logger.warning("错误: 无法加载图片")
            return []

        # 检查模板是否大于目标图
        if template.shape[0] > target.shape[0] or template.shape[1] > target.shape[1]:
            logger.warning("错误: 模板图片不能大于目标图片")
            return []

        # 获取模板尺寸
        h_t, w_t = template.shape[:2]
        h, w = target.shape[:2]

        # 选择匹配方法
        methods = {
            'TM_CCOEFF_NORMED': cv2.TM_CCOEFF_NORMED,
            'TM_CCORR_NORMED': cv2.TM_CCORR_NORMED,
            'TM_SQDIFF_NORMED': cv2.TM_SQDIFF_NORMED
        }

        if method not in methods:
            logger.warning(f"警告: 未知匹配方法 {method}，使用默认的TM_CCOEFF_NORMED")
            method = 'TM_CCOEFF_NORMED'

        match_method = methods[method]

        # 执行模板匹配
        result = cv2.matchTemplate(target, template, match_method)

        # 查找匹配位置
        locations = []

        while True:
            # 根据方法选择最值
            if match_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                confidence = 1.0 - min_val  # 平方差越小越好
                top_left = min_loc
            else:
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                confidence = max_val  # 相关系数越大越好
                top_left = max_loc

            # print(confidence)
            # 检查置信度
            if confidence < threshold:
                break

            # 记录匹配位置
            bottom_right = (top_left[0] + w_t, top_left[1] + h_t)
            locations.append({
                'top_left': top_left,
                'bottom_right': bottom_right,
                'confidence': float(confidence),
                'relative_position': (
                        int(top_left[0] + bottom_right[0]) // 2,
                        int(top_left[1] + bottom_right[1]) // 2
                )
            })

            # 在结果矩阵中屏蔽已匹配区域，避免重复检测
            cv2.rectangle(result,
                          (max(0, top_left[0] - w_t // 2), max(0, top_left[1] - h_t // 2)),
                          (min(w - w_t // 2, top_left[0] + w_t // 2),
                           min(h - h_t // 2, top_left[1] + h_t // 2)),
                          0, -1)

        return locations