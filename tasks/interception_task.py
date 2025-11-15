#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拦截战任务模块
处理游戏拦截战相关的自动化任务
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class InterceptionTask(Task):
    """拦截战任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 拦截战任务图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.interception_images = {
            "interception_normal": f"{self.game_images_path}interception_normal.png",
            "interception_abnormal": f"{self.game_images_path}interception_abnormal.png",
            "interception_enter": f"{self.game_images_path}interception_enter.png",
            "interception_confirm": f"{self.game_images_path}interception_confirm.png",
            "interception_complete": f"{self.game_images_path}interception_complete.png",
            "interception_fight": f"{self.game_images_path}interception_fight.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "normal_click": (320, 200),
            "abnormal_click": (420, 240),
            "enter_click": (620, 320),
            "confirm_click": (720, 520),
            "complete_click": (670, 470),
            "fight_click": (580, 380)
        }
    
    def run(self) -> bool:
        """执行拦截战任务，基于AHK拦截战逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行拦截战任务")
        
        success_count = 0
        
        # 执行普通拦截战
        if self.settings.get("InterceptionNormal", 0):
            if self._perform_interception("interception_normal", self.coordinates["normal_click"]):
                logger.info("普通拦截战执行成功")
                success_count += 1
        
        # 执行异常拦截战
        if self.settings.get("InterceptionAbnormal", 0):
            if self._perform_interception("interception_abnormal", self.coordinates["abnormal_click"]):
                logger.info("异常拦截战执行成功")
                success_count += 1
        
        logger.info(f"拦截战任务完成，成功执行{success_count}个拦截战")
        return success_count > 0
    
    def _perform_interception(self, image_key, fallback_coords):
        """
        执行特定类型的拦截战
        类似AHK的拦截战逻辑
        """
        if self.find_and_click(self.interception_images[image_key], fallback_coords, timeout=5):
            self.random_delay(1, 2)
            if self.find_and_click(self.interception_images["interception_enter"], self.coordinates["enter_click"], timeout=5):
                self.random_delay(2, 3)
                if self.find_and_click(self.interception_images["interception_fight"], self.coordinates["fight_click"], timeout=5):
                    self.random_delay(3, 5)
                    if self._confirm_interception_completion():
                        return True
        
        return False
    
    def _confirm_interception_completion(self):
        """确认拦截战完成操作"""
        # 检查是否需要确认完成
        if self.find_and_click(self.interception_images["interception_confirm"], self.coordinates["confirm_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        # 检查是否有完成按钮
        if self.find_and_click(self.interception_images["interception_complete"], self.coordinates["complete_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        return True  # 如果没有确认步骤，默认成功
    
    

# 测试代码
if __name__ == '__main__':
    print("InterceptionTask 模块测试")
    # 这里可以添加测试代码