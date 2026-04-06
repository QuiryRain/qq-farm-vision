#!/usr/bin/env python3
# -*- coding: utf8 -*-
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from loguru import logger
from PIL import Image

DIR_PATH = Path(__file__).parent

class YoloVision:
    def __init__(self, file_path: str, window_offset: tuple[int, int]):
        path = Path(file_path)
        if not path.exists():
            logger.warning(f'模型文件不存在: {file_path}')
            raise Exception(f'模型文件不存在: {file_path}')
        self.model = YOLO(file_path)
        self.window_offset = window_offset

    def change_model(self, file_path: str):
        path = Path(file_path)
        if not path.exists():
            logger.warning(f'模型文件不存在: {file_path}')
            return None
        return YOLO(file_path)

    def detect_capture(self, image=None, model: YOLO=None, confidence_threshold=0.5):
        """检测图片"""
        if image is None:
            logger.warning("截图失败，无法检测")
            return []

        if model is None:
            model = self.model

        results = model(image, verbose=False)
        detected_targets = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                confidence = float(box.conf[0].cpu().numpy())
                if confidence < confidence_threshold:
                    continue

                class_id = int(box.cls[0].cpu().numpy())
                class_name = result.names[class_id]

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                center_x_img = (x1 + x2) / 2
                center_y_img = (y1 + y2) / 2

                screen_x = self.window_offset[0] + int(center_x_img)
                screen_y = self.window_offset[1] + int(center_y_img)

                detected_targets.append({
                    'class_name': class_name,
                    'confidence': confidence,
                    'relative_position': (int(center_x_img), int(center_y_img)),
                    'screen_position': (screen_x, screen_y),
                    'bbox': (int(x1), int(y1), int(x2), int(y2)),
                })

                logger.info(f"检测到: {class_name}, 置信度: {confidence:.2f}, "
                      f"位置: ({screen_x}, {screen_y})")

        return detected_targets

    def detect_specific_target(self, target_class, image, model: YOLO=None, confidence_threshold=0.5):
        """
        特定类型的目标
        :param target_class: 目标类别名称
        :param image:
        :param model:
        :param confidence_threshold: 置信度阈值
        :return:
        """
        if isinstance(image, Image.Image):
            img_np = np.array(image)
        else:
            img_np = image

        if isinstance(target_class, (tuple, list)):
            target_classes = target_class
        elif isinstance(target_class, str):
            target_classes = [target_class]
        else:
            raise Exception(f'不支持的类型： {target_class}, type: {type(target_class)}, '
                            f'必须为tuple,list,str。')

        detected_targets = self.detect_capture(img_np, model, confidence_threshold)
        return [target for target in detected_targets
                if target_classes and target['class_name'] in target_classes]