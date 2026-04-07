#!/usr/bin/env python3
# -*- coding: utf8 -*-
import time
import random
# import pyautogui
import win32gui

from base import Base
from action import AutoClick, click_with_sendinput
from config import CONFIG
from detector import RedDotDetector
# from vision import YoloVision
# from mapping import Target
from utils import remove_duplicate_matches, analyze_match_positions


class BotVision(Base):
    def __init__(self, window_title: str):
        super().__init__(window_title)
        # self.yolo: YoloVision | None = None
        self.clicker = AutoClick()
        self.reddot_detector = RedDotDetector(runner=self)
        self.last_click_time = 0
        self.last_click_pos = (0, 0)
        self.last_click_count = 0
        self.last_click_interval = 0.5
        self.last_click_button = 'left'
        self.last_click_success = False

    def common_click(self, x=None, y=None):
        """无效点击"""
        time.sleep(2)
        if x is None or y is None:
            cx, cy = CONFIG['commonClick']
        else:
            cx, cy = x, y
        offset = random.randint(-10, 10)
        self.clicker.click(self.hwnd, cx + offset, cy)

    def cancel_share(self):
        """取消分享"""
        image = self.capture_full_screen()
        cancel_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['CancelShare'],
            target_img=image,
        )
        if cancel_locations:
            time.sleep(1)
            x, y = cancel_locations[0]['relative_position']
            hwnd = win32gui.GetDesktopWindow()
            click_with_sendinput(hwnd, x, y + 20)
            time.sleep(1)
        self.common_click()

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
        # 取消分享
        self.cancel_share()
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
                break
            try:
                ReceiveRewardLocations = self.reddot_detector.detect_template_in_image(
                    template_img=CONFIG['TaskReceiveReward'],
                    target_img=image,
                )
            except Exception as e:
                self.logger.error(f'检测失败： {e}', exc_info=True)
                continue
            # 任务中无奖励可领取
            if not ReceiveRewardLocations:
                break
            # 点击领取奖励
            self.clicker.click(self.hwnd, *ReceiveRewardLocations[0]['relative_position'])
            time.sleep(1)
            image = self.capture_window_printwindow()
            shareRewardLocations = self.reddot_detector.detect_template_in_image(
                template_img=CONFIG['TaskShareReward'],
                target_img=image,
            )
            # 主任务： 分享/直接领取
            if shareRewardLocations:
                self.clicker.click(self.hwnd, *shareRewardLocations[0]['relative_position'])
                time.sleep(2)
                self.cancel_share()
        # 关闭任务窗口
        time.sleep(1)
        self.clicker.click(self.hwnd, *CONFIG['reward']['task'][2])
        self.common_click()

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
        # 检测未解锁标志
        lock_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['storeSeedlocked'],
            target_img=image,
        )
        if lock_locations:
            sorted_targets = sorted(
                lock_locations,
                key=lambda t: (t['relative_position'][1], t['relative_position'][0]),
                reverse=True
            )
            lock_analyze_result = analyze_match_positions(sorted_targets)
            min_y = lock_analyze_result['min_y']
            min_y_count = lock_analyze_result['y_distribution'][min_y]
            if min_y_count == 4:
                x = sorted_targets[-1]['relative_position'][0] + 100 * 3
                new_seed = {
                    'relative_position': (x, min_y - 95)
                }
            elif 0 < min_y_count < 4:
                x = sorted_targets[-1]['relative_position'][0] - 100
                new_seed = {
                    'relative_position': (x, min_y)
                }
            else:
                new_seed = {
                    'relative_position': (208, 432)
                }
        else:
            unlock_locations = self.reddot_detector.detect_template_in_image(
                template_img=CONFIG['storeSeedUnlocked'],
                target_img=image,
            )
            if not unlock_locations:
                self.logger.warning('未检测到可购买的种子')
                return
            new_seed = unlock_locations[0]

        # 点击种子触发出来购买按钮
        self.clicker.click(self.hwnd, *new_seed['relative_position'])
        time.sleep(2)
        # 购买种子
        self.clicker.click(self.hwnd, *CONFIG['purchase_seed'])
        time.sleep(2)
        # 关闭商店
        self.clicker.click(self.hwnd, *CONFIG['close_store'])
        self.logger.info(f"获取新种子完成，坐标: {new_seed['relative_position']}")

    def get_seed_locations(self, image):
        """获取已有种子坐标"""
        seed1_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['SeedType1'],
            target_img=image
        )
        seed2_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['SeedType2'],
            target_img=image
        )
        seed3_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['SeedType3'],
            target_img=image
        )
        seed_locations = remove_duplicate_matches(
            seed1_locations + seed2_locations + seed3_locations)
        return seed_locations

    def upgrade_land(self, image=None):
        """土地升级"""
        image = image or self.capture_window_printwindow()
        updateSwitch_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['landUpdateSwitch'],
            target_img=image
        )
        if updateSwitch_locations:
            time.sleep(1)
            self.clicker.click(self.hwnd, *updateSwitch_locations[0]['relative_position'])

        time.sleep(0.5)
        image = self.capture_window_printwindow()
        upgrade_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['landUpgrade'],
            target_img=image
        )
        if upgrade_locations:
            time.sleep(1)
            self.clicker.click(self.hwnd, *upgrade_locations[0]['relative_position'])

        time.sleep(0.5)
        image = self.capture_window_printwindow()
        updateButton_locations = self.reddot_detector.detect_template_in_image(
            template_img=CONFIG['landUpgradeButton'],
            target_img=image
        )
        is_update = False
        if updateButton_locations:
            time.sleep(1)
            self.clicker.click(self.hwnd, *updateButton_locations[0]['relative_position'])
            is_update = True
        return is_update

    def start_sowing(self):
        is_sow_seed = False
        self.logger.info('开始土地巡检。。。')
        for x, y, *_ in CONFIG['land']:
            try:
                self.clicker.click(self.hwnd, x, y)
                time.sleep(1)
                image = self.capture_window_printwindow()
                switch_locations = self.reddot_detector.detect_template_in_image(
                    template_img=CONFIG['LandSwitch'],
                    target_img=image
                )
                eradicate_loctions = self.reddot_detector.detect_template_in_image(
                    template_img=CONFIG['SeedEradicate'],
                    target_img=image
                )
                if switch_locations or eradicate_loctions:
                    self.logger.info(f"开始检测土地是否可升级: ({x, y})")
                    status = self.upgrade_land(image)
                    if status:
                        self.logger.info(f"土地已升级结果: ({x, y})")
                    continue
                time.sleep(1)
                seed_locations = self.get_seed_locations(image)
                if not seed_locations:
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
                    seed_locations = self.get_seed_locations(image)
                if seed_locations:
                    self.logger.info(f"开始播种: ({x, y})")
                    x1 = seed_locations[0]['relative_position'][0] + 15
                    y1 = seed_locations[0]['relative_position'][1] + 15
                    self.clicker.click(self.hwnd, x1, y1)
            except Exception as e:
                self.logger.error(f'播种失败: ({x, y}) - {e}')
        self.logger.info('土地巡检结束。。。')
        self.common_click(276, 143)

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
            time.sleep(0.5)
            if action == 'Harvest' and locations:
                self.common_click()
                # 重新巡检
                self.start_sowing()

    def loop(self):
        land_loop = {
            'threshold': 120,
            'last_time': time.time()
        }
        while True:
            self.get_daily_reward()
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

    time.sleep(2)
    bot_vision.scroll_min_window()
    time.sleep(2)
    bot_vision.get_daily_reward()
    time.sleep(1)
    bot_vision.loop()
    # bot_vision.get_new_seed()
    # bot_vision.upgrade_land()


if __name__ == '__main__':
    run()