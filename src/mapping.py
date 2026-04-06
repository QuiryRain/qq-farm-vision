#!/usr/bin/env python3
# -*- coding: utf8 -*-
from enum import Enum


class Target(Enum):
    LOCK = 'lock'                       # 种子 - 未解锁
    UNLOCK = 'unlock'                   # 种子 - 已解锁
    HARVEST = 'harvest'                 # 收获
    WATERING = 'watering'               # 浇水
    WEEDING = 'weeding'                 # 除草
    DEINSECTZATION = 'deinsectzation'   # 除虫
    DONE = 'done'                       # 任务 - 已完成
    GOTO = 'goto'                       # 任务 - 前往
    RECONNECTION = 'reconnection'       # 重新连接
    RECEIVE = 'receive'                 # 任务 - 领取
    SHARE_REWARD = 'share_reward'       # 任务 - 分享领取
    NORMAL_REWARD = 'normal_reward'     # 任务 - 直接领取
    UNLOCK_LAND = 'unlock_land'         # 土地未解锁
    LAND_SWITCH = 'land_switch'         # 土地 - 切换
    LAND_UPGRADE = 'land_upgrade'       # 土地 - 升级
    SEED = 'seed'                       # 种子
    LAND_NO_UPGRADE = 'land_no_upgrade' # 土地 - 无法升级
