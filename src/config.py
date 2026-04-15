#!/usr/bin/env python3
# -*- coding: utf8 -*-
CONFIG = {
    'YOLO_MODEL_PATH': './model/qqfarm-9.pt',
    'RedDot': './static/redDot.png',                    # 红点
    'Watering': './static/water.png',                   # 浇水
    'LandSwitch': './static/switch.png',                # 土地 - 切换
    'SeedEradicate': './static/eradicate.png',          # 土地 - 铲除
    'Weeding': './static/weeding.png',                  # 除草
    'Deinsectzation': './static/deinsectzation.png',    # 除虫
    'Harvest': './static/harvest.png',                  # 收获
    'ExitGame': './static/exitGame.png',                # 退出游戏
    'Reconnect': './static/reconnect.png',              # 重新连接
    'CancelShare': './static/cancelShare.png',          # 取消分享
    'CancelShare2': './static/cancelShare2.png',          # 取消分享
    'CancelShare3': './static/cancelShare3.png',          # 取消分享
    'SeedType1': './static/seed1.png',                  # 种子左上角的数字边框样式1
    'SeedType2': './static/seed2.png',                  # 种子左上角的数字边框样式2
    'SeedType3': './static/seed3.png',                  # 种子左上角的数字边框样式3
    'TaskReceiveReward': './static/taskReceiveReward.png',  # 任务 - 领取
    'TaskShareReward': './static/taskShareReward.png',      # 任务 - 领取 - 分享
    'TaskNormalReceiveReward': './static/taskNormalReceiveReward.png',  # 任务 - 领取 - 直接领取
    'storeSeedlocked': './static/seedLock.png', # 商店 - 种子 - 未解锁 样式1
    'storeSeedlocked2': './static/seedLock2.png', # 商店 - 种子 - 未解锁 样式2
    'storeSeedUnlocked': './static/seedUnlock.png', # 商店 - 种子 - 已解锁
    'landUpdateSwitch': './static/landUpdateSwtich.png',    # 土地升级切换
    'landUpgrade': './static/landUpgrade.png',      # 土地升级
    'landUpgradeButton': './static/landUpgradeButton.png', # 土地升级按钮
    'blankClose': './static/blank_close.png',

    'mainscene': {
        # 仓库
        'warehuse':(55, 825),
        # 商店
        'store':(135, 825),
        # 宠物
        'pet': (217, 825),
        # 图鉴
        'handbook': (300, 825),
        # 好友
        'friend': (425, 825),
        # 菜单
        'menu': (39, 324),
        'menuEmail': (38, 483),
        'menuEmailReward': (337, 762),
        'menuEmailDeleteReward': (152, 762),
        'menuEmailDeleteRewardConfirm': (336, 529),
        # 分享
        'share': (39, 206),
        # 商城
        'shoppingMall': (445, 206),
        # 任务
        'task': (51, 744)
    },
    'reward': {
        'share': [
            # 分享红点
            (63, 171, 78, 185),
            # 分享内部红点
            # (406, 695, 419, 711),
            # 分享奖励
            (350, 722),
            # 返回坐标
            (459, 163),
        ],
        'shop': [
            # 商店红点
            (446, 171, 465, 185),
            # 商店内部红点
            # (158, 820, 169, 834)
            # 每日福利
            (164, 540),
            # 返回坐标
            (61, 150)
        ],
        'task': [
            # 任务红点
            (61, 715, 85, 730),
            # 任务奖励
            (164, 540), # 随便写的，后面改
            # 菜单返回坐标
            (448, 104)
        ],
        'menu': [
            # 菜单红点
            (49, 299, 57, 312),
            # 菜单内部红点
            # (158, 820, 169, 834)
            # 菜单奖励
            (164, 540), # 随便写的，后面改
            # 菜单返回坐标
            (39, 324)   # 随便写的，后面改
        ]
    },
    'land': [
        # x, y, 映射x1, 映射y1, 类型, 土地颜色检测区域（x2, y2, x3, y3）
        #   类型 0: 未开发 1: 普通 2: 红土地 3: 黑土地 4: 金土地 5:
        (277, 482, 0, 0, 0, 216, 423, 226, 435),
        (305, 495, 0, 1, 0, 243, 439, 257, 448),
        (331, 510, 0, 2, 0, 267, 452, 278, 462),
        (358, 523, 0, 3, 0, 296, 465, 306, 474),

        (250, 495, 1, 0, 0, 189, 438, 199, 448),
        (277, 510, 1, 1, 0, 217, 453, 226, 461),
        (305, 523, 1, 2, 0, 240, 466, 255, 477),
        (331, 536, 1, 3, 0, 266, 480, 278, 490),

        (223, 510, 2, 0, 0, 163, 451, 174, 461),
        (250, 523, 2, 1, 0, 191, 464, 200, 474),
        (277, 536, 2, 2, 0, 216, 479, 226, 489),
        (305, 550, 2, 3, 0, 243, 491, 253, 502),

        (196, 523, 3, 0, 0, 138, 464, 147, 476),
        (223, 536, 3, 1, 0, 163, 478, 173, 487),
        (250, 550, 3, 2, 0, 189, 493, 201, 502),
        (277, 563, 3, 3, 0, 217, 507, 227, 517),

        (168, 536, 4, 0, 0, 110, 479, 119, 487),
        (196, 550, 4, 1, 0, 135, 491, 147, 503),
        (223, 563, 4, 2, 0, 163, 505, 174, 515),
        (250, 577, 4, 3, 0, 190, 518, 198, 531),

        (144, 550, 5, 0, 0, 83, 492, 91, 503),
        (168, 563, 5, 1, 0, 110, 504, 119, 515),
        (196, 577, 5, 2, 0, 136, 518, 146, 528),
        (223, 590, 5, 3, 0, 160, 532, 175, 542),
    ],
    'commonClick': (270, 78),
    'purchase_seed': (257, 611),     # 购买种子
    'close_store': (447, 130),
}