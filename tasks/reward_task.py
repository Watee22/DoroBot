#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奖励收集任务模块
处理游戏奖励收集相关的自动化任务
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class RewardTask(Task):
    """奖励收集任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 奖励收集图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.reward_images = {
            "outpost_reward": f"{self.game_images_path}outpost_reward.png",
            "mail_reward": f"{self.game_images_path}mail_reward.png",
            "daily_reward": f"{self.game_images_path}daily_reward.png",
            "weekly_reward": f"{self.game_images_path}weekly_reward.png",
            "friendship_reward": f"{self.game_images_path}friendship_reward.png",
            "manufacture_reward": f"{self.game_images_path}manufacture_reward.png",
            "reward_confirm": f"{self.game_images_path}reward_confirm.png",
            "reward_collect": f"{self.game_images_path}reward_collect.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "outpost_click": (300, 150),
            "mail_click": (400, 200),
            "daily_click": (500, 250),
            "weekly_click": (600, 300),
            "friendship_click": (350, 350),
            "manufacture_click": (450, 400),
            "confirm_click": (700, 500),
            "collect_click": (650, 450)
        }
    
    def run(self) -> bool:
        """执行奖励收集任务，基于AHK奖励收集逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行奖励收集任务")
        
        success_count = 0
        
        # 前哨站奖励收集
        if self.settings.get("RewardOutpost", 0):
            if self._collect_reward("outpost_reward", self.coordinates["outpost_click"]):
                logger.info("收集前哨站奖励成功")
                success_count += 1
        
        # 邮件奖励收集
        if self.settings.get("RewardMail", 0):
            if self._collect_reward("mail_reward", self.coordinates["mail_click"]):
                logger.info("收集邮件奖励成功")
                success_count += 1
        
        # 每日奖励收集
        if self.settings.get("RewardDaily", 0):
            if self._collect_reward("daily_reward", self.coordinates["daily_click"]):
                logger.info("收集每日奖励成功")
                success_count += 1
        
        # 每周奖励收集
        if self.settings.get("RewardWeekly", 0):
            if self._collect_reward("weekly_reward", self.coordinates["weekly_click"]):
                logger.info("收集每周奖励成功")
                success_count += 1
        
        # 友情点收集
        if self.settings.get("RewardFriendship", 0):
            if self._collect_reward("friendship_reward", self.coordinates["friendship_click"]):
                logger.info("收集友情点成功")
                success_count += 1
        
        # 制造奖励收集
        if self.settings.get("RewardManufacture", 0):
            if self._collect_reward("manufacture_reward", self.coordinates["manufacture_click"]):
                logger.info("收集制造奖励成功")
                success_count += 1
        
        logger.info(f"奖励收集任务完成，成功收集{success_count}种奖励")
        return success_count > 0
    
    def _collect_reward(self, image_key, fallback_coords):
        """
        收集特定类型的奖励
        类似AHK的奖励收集逻辑
        """
        if self.find_and_click(self.reward_images[image_key], fallback_coords, timeout=5):
            self.random_delay(1, 2)
            if self._confirm_collection():
                return True
        
        return False
    
    def _confirm_collection(self):
        """确认奖励收集操作"""
        # 检查是否需要确认收集
        if self.find_and_click(self.reward_images["reward_confirm"], self.coordinates["confirm_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        # 检查是否有收集按钮
        if self.find_and_click(self.reward_images["reward_collect"], self.coordinates["collect_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        return True  # 如果没有确认步骤，默认成功
    
    

# 测试代码
if __name__ == '__main__':
    print("RewardTask 模块测试")
    # 这里可以添加测试代码