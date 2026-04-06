#!/usr/bin/env python3
# -*- coding: utf8 -*-
import time

from base import Base
from action import AutoClick
from config import CONFIG
from detector import RedDotDetector
from vision import YoloVision
from mapping import Target


class BotVision(Base):
    def __init__(self, window_title: str):
        super().__init__(window_title)
        self.yolo: YoloVision | None = None
        self.clicker = AutoClick()
        self.reddot_detector = RedDotDetector(runner=self)
        self.last_click_time = 0
        self.last_click_pos = (0, 0)
        self.last_click_count = 0
        self.last_click_interval = 0.5
        self.last_click_button = 'left'
        self.last_click_success = False

    def common_click(self):
        """无效点击"""
        time.sleep(1)
        cx, cy = CONFIG['commonClick']
        self.clicker.click(self.hwnd, cx, cy)

    def get_share_reward(self):
        """获取分享每日奖励"""
        self.logger.info("获取分享奖励")
        # 界面坐标
        x, y = CONFIG['mainscene']['share']['x'], CONFIG['mainscene']['share']['y']
        self.clicker.click(self.hwnd, x, y)
        time.sleep(1)
        # 奖励坐标
        reward_x, reward_y = CONFIG['reward']['share'][1]
        self.clicker.click(self.hwnd, reward_x, reward_y)
        time.sleep(2)
        # esc关闭分享
        self.clicker.send_key(self.hwnd, 'VK_ESCAPE')
        self.common_click()
        # 领取奖励
        self.clicker.click(self.hwnd, reward_x, reward_y)
        time.sleep(1)
        # 退出坐标
        exit_x, exit_y = CONFIG['reward']['share'][2][0], CONFIG['reward']['share'][2][1]
        self.clicker.click(self.hwnd, exit_x, exit_y)
        time.sleep(2)

    def get_shop_reward(self):
        """获取商城每日奖励"""
        self.logger.info("获取商城每日奖励")
        # 界面坐标
        x, y = CONFIG['mainscene']['shoppingMall']['x'], CONFIG['mainscene']['shoppingMall']['y']
        self.clicker.click(self.hwnd, x, y)
        time.sleep(1)
        # 奖励坐标
        reward_x, reward_y = CONFIG['reward']['shop'][1]
        self.clicker.click(self.hwnd, reward_x, reward_y)
        time.sleep(1)
        self.clicker.click(self.hwnd, reward_x, reward_y)
        time.sleep(1)
        # 退出坐标
        exit_x, exit_y = CONFIG['reward']['shop'][2]
        self.clicker.click(self.hwnd, exit_x, exit_y)
        time.sleep(2)

    def get_task_reward(self):
        """获取任务奖励"""
        self.logger.info("获取任务奖励")
        x, y = CONFIG['mainscene']['task']['x'], CONFIG['mainscene']['task']['y']
        self.clicker.click(self.hwnd, x, y)

        while True:
            time.sleep(2)
            image = self.capture_window_printwindow()
            if not image:
                self.logger.error("任务 - 截图图片失败")
                return
            try:
                targets = self.yolo.detect_specific_target(
                    [
                        Target.RECEIVE.value,
                        Target.SHARE_REWARD.value,
                        Target.NORMAL_REWARD.value,
                    ],
                    image,
                )
            except Exception as e:
                self.logger.error(f'检测失败： {e}')
                continue
            receive_targets = [target for target in targets
                               if target['class_name'] == Target.RECEIVE.value]
            if receive_targets:
                self.clicker.click(self.hwnd, *receive_targets[0]['screen_position'])
                self.common_click()

            share_targets = [target for target in targets
                               if target['class_name'] == Target.SHARE_REWARD.value]
            if share_targets:
                self.clicker.click(self.hwnd, *share_targets[0]['screen_position'])
                time.sleep(2)
                # ESC
                self.clicker.send_key(self.hwnd, 'VK_ESCAPE')
                self.common_click()

            normal_targets = [target for target in targets
                               if target['class_name'] == Target.NORMAL_REWARD.value]
            if normal_targets:
                self.clicker.click(self.hwnd, *normal_targets[0]['screen_position'])
                self.common_click()
            if not targets:
                break

    def get_menu_reward(self):
        """获取菜单奖励"""
        self.logger.info("获取菜单奖励")
        # x, y = CONFIG['mainscene']['menu']['x'], CONFIG['mainscene']['menu']['y']
        # self.clicker.click(self.hwnd, x, y)
        # time.sleep(1)

    def get_daily_reward(self):
        rois = {
            # 分享红点
            'share_red_dot': CONFIG['reward']['share'][0],
            # 商城红点
            'shop_red_dot': CONFIG['reward']['shop'][0],
            # 任务红点
            'task_red_dot': CONFIG['reward']['task'][0],
            # 菜单红点
            'menu_red_dot': CONFIG['reward']['menu'][0],
        }
        zh_cn_name = {
            'share_red_dot': '分享',
            'shop_red_dot': '商城',
            'task_red_dot': '任务',
            'menu_red_dot': '菜单',
            'full_image': '全图'
        }

        img = self.capture_window_printwindow()
        if img is None:
            return []

        result = self.reddot_detector.detect_red_dot(image=img, rois=rois)

        for roi_id, step in result.items():
            roi_coords = step['roi']
            dots = step['dots']

            # if dots:
            #     self.logger.info(f"{roi_id} {roi_coords} 检测到 {len(dots)} 个红点:")
            #     for i, (x, y) in enumerate(dots):
            #         logger.info(f"  红点 {i + 1}: ({x}, {y})")
            # else:
            #     logger.warning(f"{roi_id} {roi_coords} 未检测到红点")

            if not dots:
                self.logger.info(f"{zh_cn_name[roi_id]} 没有待领取奖励")
                continue

            # 红点中心坐标
            (x, y) = dots[0]
            if roi_id == 'share_red_dot':
                self.get_share_reward()
            elif roi_id == 'shop_red_dot':
                self.get_shop_reward()
            elif roi_id == 'task_red_dot':
                self.get_task_reward()
            elif roi_id == 'menu_red_dot':
                self.get_menu_reward()

    def scroll_min_window(self):
        """将画面内容最小化，统一界面"""
        self.clicker.scroll_window(self.hwnd, 100000)

    def get_new_seed(self):
        """获取新种子"""
        self.logger.info("获取新种子")
        self.clicker.click(
            self.hwnd,
            CONFIG['mainscene']['store']['x'],
            CONFIG['mainscene']['store']['y']
        )
        time.sleep(2)
        image = self.capture_window_printwindow()
        detected_targets = self.yolo.detect_specific_target(
            [
                Target.LOCK.value,
                Target.UNLOCK.value,
            ],
            image,
        )
        valid_targets = [t for t in detected_targets if t['class_name'] != 'lock']
        sorted_targets = sorted(valid_targets,
                                key=lambda t: (t['screen_position'][1], t['screen_position'][0]),
                                reverse=True)

        new_seed = sorted_targets[0]
        # 点击种子触发出来购买按钮
        self.clicker.click(self.hwnd, *new_seed['screen_position'])
        time.sleep(2)
        # 购买种子
        self.clicker.click(self.hwnd, *CONFIG['purchase_seed'])
        time.sleep(2)
        # 关闭商店
        self.clicker.click(self.hwnd, *CONFIG['close_store'])
        self.logger.info(f"获取新种子完成，坐标: {new_seed['screen_position']}")

    def start_sowing(self):
        is_sow_seed = False
        self.logger.info('开始土地巡检。。。')
        for x, y, x1, y1, dtype, x2, y2, x3, y3 in CONFIG['land']:
            try:
                self.clicker.click(self.hwnd, x, y)
                time.sleep(1)
                image = self.capture_window_printwindow()
                switch_locations = self.reddot_detector.detect_template_in_image(
                    template_img=CONFIG['LandSwitch'],
                    target_img=image
                )
                if switch_locations:
                    continue
                seed_targets = self.yolo.detect_specific_target(Target.SEED.value, image)
                time.sleep(1)
                if not seed_targets and not is_sow_seed:
                    if not is_sow_seed:
                        self.logger.info("没有种子，开始获取新种子")
                        # 购买种子
                        self.get_new_seed()
                        is_sow_seed = True
                        time.sleep(1)
                    self.clicker.click(self.hwnd, x, y)
                    time.sleep(1)
                    # 重新判定
                    image = self.capture_window_printwindow()
                    targets = self.yolo.detect_specific_target(Target.SEED.value, image)
                    seed_targets = [t for t in targets if t['class_name'] == Target.SEED.value]
                if seed_targets:
                    self.logger.info(f"开始播种: ({x, y})")
                    self.clicker.click(self.hwnd, *seed_targets[0]['relative_position'])
            except Exception as e:
                self.logger.error(f'播种失败: ({x, y}) - {e}')
        self.common_click()
        self.logger.info('土地巡检结束。。。')

    def start_xxx_action(self, actions, image):
        """
        开始收获、除草、除虫、浇水
        :param actions: [(action, ZhCn_name)]
        :return:
        """
        for action, zhCn_name in actions:
            locations = self.reddot_detector.detect_template_in_image(
                template_img=CONFIG[action],
                target_img=image
            )
            if locations:
                self.logger.info(f"开始{zhCn_name}")
                self.clicker.click(self.hwnd, *locations[0]['relative_position'])

    def loop(self):
        land_loop = {
            'threshold': 120,
            'last_time': time.time()
        }
        while True:
            t = time.time() - land_loop['last_time']
            if t > land_loop['threshold'] or t < 1:
                land_loop['last_time'] = time.time()
                self.start_sowing()

            image = self.capture_window_printwindow()
            self.start_xxx_action([
                ('Harvest', '收获'),
                ('Weeding', '除草'),
                ('Deinsectzation', '除虫'),
                ('Watering', '浇水'),
                ('Reconnect', '重新连接')
            ], image)
            time.sleep(2)


def run():
    bot_vision = BotVision('QQ经典农场')

    if not bot_vision.find_window():
        bot_vision.logger.error("初始化失败")
        return

    bot_vision.yolo = YoloVision(CONFIG['YOLO_MODEL_PATH'], bot_vision.window_offset)

    time.sleep(2)
    bot_vision.scroll_min_window()
    time.sleep(2)
    bot_vision.get_daily_reward()
    time.sleep(1)
    bot_vision.loop()
    # bot_vision.get_new_seed()


if __name__ == '__main__':
    run()