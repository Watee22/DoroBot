#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动参与任务模块
处理游戏活动参与相关的自动化任务
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class EventTask(Task):
    """活动参与任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 活动任务图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.event_images = {
            "event_small": f"{self.game_images_path}event_small.png",
            "event_large": f"{self.game_images_path}event_large.png",
            "event_special": f"{self.game_images_path}event_special.png",
            "event_enter": f"{self.game_images_path}event_enter.png",
            "event_confirm": f"{self.game_images_path}event_confirm.png",
            "event_complete": f"{self.game_images_path}event_complete.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "small_event_click": (320, 200),
            "large_event_click": (420, 240),
            "special_event_click": (520, 280),
            "enter_click": (620, 320),
            "confirm_click": (720, 520),
            "complete_click": (670, 470)
        }
    
    def run(self) -> bool:
        """执行活动参与任务，基于AHK活动逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行活动参与任务")
        
        success_count = 0
        
        # 参与小活动
        if self.settings.get("EventSmall", 0):
            if self._participate_event("event_small", self.coordinates["small_event_click"]):
                logger.info("小活动参与成功")
                success_count += 1
        
        # 参与大活动
        if self.settings.get("EventLarge", 0):
            if self._participate_event("event_large", self.coordinates["large_event_click"]):
                logger.info("大活动参与成功")
                success_count += 1
        
        # 参与特殊活动
        if self.settings.get("EventSpecial", 0):
            if self._participate_event("event_special", self.coordinates["special_event_click"]):
                logger.info("特殊活动参与成功")
                success_count += 1
        
        logger.info(f"活动参与任务完成，成功参与{success_count}个活动")
        return success_count > 0
    
    def _participate_event(self, image_key, fallback_coords):
        """
        参与特定类型的活动
        类似AHK的活动参与逻辑
        """
        if self.find_and_click(self.event_images[image_key], fallback_coords, timeout=5):
            self.random_delay(1, 2)
            if self.find_and_click(self.event_images["event_enter"], self.coordinates["enter_click"], timeout=5):
                self.random_delay(2, 3)
                if self._confirm_event_participation():
                    return True
        
        return False
    
    def _confirm_event_participation(self):
        """确认活动参与操作"""
        # 检查是否需要确认参与
        if self.find_and_click(self.event_images["event_confirm"], self.coordinates["confirm_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        # 检查是否有完成按钮
        if self.find_and_click(self.event_images["event_complete"], self.coordinates["complete_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        return True  # 如果没有确认步骤，默认成功
    
    

# 测试代码
if __name__ == '__main__':
    print("EventTask 模块测试")
    # 这里可以添加测试代码