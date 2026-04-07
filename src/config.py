#!/usr/bin/env python3
# -*- coding: utf8 -*-
CONFIG = {
    'YOLO_MODEL_PATH': './model/qqfarm-9.pt',
    'Watering': './static/water.png',                   # 浇水
    'LandSwitch': './static/switch.png',                # 土地 - 切换
    'SeedEradicate': './static/eradicate.png',          # 土地 - 铲除
    'Weeding': './static/weeding.png',                  # 除草
    'Deinsectzation': './static/deinsectzation.png',    # 除虫
    'Harvest': './static/harvest.png',                  # 收获
    'ExitGame': './static/exitGame.png',                # 退出游戏
    'Reconnect': './static/reconnect.png',              # 重新连接
    'CancelShare': './static/cancelShare2.png',          # 取消分享
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

    'mainscene': {
        'warehuse':{
            'x': 55,
            'y': 825,
            'name': '仓库',
        },
        'store':{
            'x': 135,
            'y': 825,
            'name': '商店',
        },
        'pet': {
            'x': 217,
            'y': 825,
            'name': '宠物',
        },
        'handbook': {
            'x': 300,
            'y': 825,
            'name': '图鉴',
        },
        'friend': {
            'x': 425,
            'y': 825,
            'name': '好友',
        },
        'menu': {
            'x': 39,
            'y': 324,
            'name': '菜单',
        },
        'share': {
            'x': 39,
            'y': 206,
            'name': '分享',
        },
        'shoppingMall': {
            'x': 445,
            'y': 206,
            'name': '商城',
        },
        'task': {
            'x': 51,
            'y': 744,
            'name': '任务',
        }
    },
    'reward': {
        'share': [
            # 分享红点
            (69, 183, 83, 197),
            # 分享内部红点
            # (406, 695, 419, 711),
            # 分享奖励
            (350, 722),
            # 返回坐标
            (459, 163),
        ],
        'shop': [
            # 商店红点
            (460, 184, 475, 200),
            # 商店内部红点
            # (158, 820, 169, 834)
            # 每日福利
            (164, 540),
            # 返回坐标
            (61, 150)
        ],
        'task': [
            # 任务红点
            (68,723, 82, 737),
            # 任务奖励
            (164, 540), # 随便写的，后面改
            # 菜单返回坐标
            (436, 128)
        ],
        'menu': [
            # 菜单红点
            (54, 306, 67, 320),
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
        (271, 488, 0, 0, 0, 216, 423, 226, 435),
        (298, 501, 0, 1, 0, 243, 439, 257, 448),
        (324, 514, 0, 2, 0, 267, 452, 278, 462),
        (349, 529, 0, 3, 0, 296, 465, 306, 474),

        (244, 501, 1, 0, 0, 189, 438, 199, 448),
        (271, 514, 1, 1, 0, 217, 453, 226, 461),
        (298, 529, 1, 2, 0, 240, 466, 255, 477),
        (324, 541, 1, 3, 0, 266, 480, 278, 490),

        (216, 514, 2, 0, 0, 163, 451, 174, 461),
        (244, 529, 2, 1, 0, 191, 464, 200, 474),
        (271, 541, 2, 2, 0, 216, 479, 226, 489),
        (298, 555, 2, 3, 0, 243, 491, 253, 502),

        (189, 529, 3, 0, 0, 138, 464, 147, 476),
        (216, 541, 3, 1, 0, 163, 478, 173, 487),
        (244, 555, 3, 2, 0, 189, 493, 201, 502),
        (271, 569, 3, 3, 0, 217, 507, 227, 517),

        (163, 541, 4, 0, 0, 110, 479, 119, 487),
        (189, 555, 4, 1, 0, 135, 491, 147, 503),
        (216, 569, 4, 2, 0, 163, 505, 174, 515),
        (244, 582, 4, 3, 0, 190, 518, 198, 531),

        (136, 555, 5, 0, 0, 83, 492, 91, 503),
        (163, 569, 5, 1, 0, 110, 504, 119, 515),
        (189, 582, 5, 2, 0, 136, 518, 146, 528),
        (216, 596, 5, 3, 0, 160, 532, 175, 542),
    ],
    'targets': [
        'lock',             # 种子 - 未解锁
        'unlock',           # 种子 - 已解锁
        'harvest',          # 收获
        'watering',         # 浇水
        'weeding',          # 除草
        'deinsectzation',   # 除虫
        'done',             # 任务 - 已完成
        'goto',             # 任务 - 前往
        'reconnection',     # 重新连接
        'receive',          # 任务 - 领取
        'share_reward',     # 任务 - 分享领取
        'normal_reward',    # 任务 - 直接领取
    ],
    'commonClick': (270, 78),
    'purchase_seed': (257, 611),     # 购买种子
    'close_store': (447, 130),
}