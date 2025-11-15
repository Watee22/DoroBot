#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无限之塔任务模块
处理游戏无限之塔相关的自动化任务
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class TowerTask(Task):
    """无限之塔任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 无限之塔图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.tower_images = {
            "tower_tab": f"{self.game_images_path}tower_tab.png",
            "company_tower": f"{self.game_images_path}company_tower.png",
            "universal_tower": f"{self.game_images_path}universal_tower.png",
            "challenge_button": f"{self.game_images_path}challenge_button.png",
            "confirm_button": f"{self.game_images_path}confirm_button.png",
            "tower_complete": f"{self.game_images_path}tower_complete.png",
            "tower_retry": f"{self.game_images_path}tower_retry.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "tower_tab": (480, 180),
            "company_tower": (320, 240),
            "universal_tower": (420, 260),
            "challenge_button": (720, 540),
            "confirm_button": (670, 490),
            "tower_complete": (620, 340),
            "tower_retry": (580, 400)
        }
    
    def run(self) -> bool:
        """执行无限之塔任务，基于AHK无限之塔逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行无限之塔任务")
        
        success_count = 0
        
        # 首先导航到无限之塔
        if self._navigate_to_tower():
            # 挑战公司之塔
            if self.settings.get("TowerCompany", 0):
                if self._challenge_tower("company_tower", self.coordinates["company_tower"]):
                    logger.info("公司之塔挑战成功")
                    success_count += 1
            
            # 挑战通用之塔
            if self.settings.get("TowerUniversal", 0):
                if self._challenge_tower("universal_tower", self.coordinates["universal_tower"]):
                    logger.info("通用之塔挑战成功")
                    success_count += 1
        
        logger.info(f"无限之塔任务完成，成功挑战{success_count}个塔")
        return success_count > 0
    
    def _navigate_to_tower(self):
        """导航到无限之塔"""
        # 查找无限之塔标签
        coords = self.vision.wait_for_template(self.tower_images["tower_tab"], timeout=5)
        if coords:
            # 点击进入无限之塔
            self.controls.user_click(coords[0], coords[1])
            self.random_delay(1, 2)
            return True
        else:
            # 使用备用坐标点击
            self.controls.user_click(self.coordinates["tower_tab"][0], self.coordinates["tower_tab"][1])
            self.random_delay(1, 2)
            return True
        
        return False
    
    def _challenge_tower(self, tower_image_key, fallback_coords):
        """
        挑战特定类型的塔
        类似AHK的塔挑战逻辑
        """
        # 查找塔类型图标
        coords = self.vision.wait_for_template(self.tower_images[tower_image_key], timeout=5)
        if coords:
            # 点击进入塔
            self.controls.user_click(coords[0], coords[1])
            self.random_delay(1, 2)
            
            # 执行挑战流程
            if self._perform_challenge():
                return True
        else:
            # 使用备用坐标点击
            self.controls.user_click(fallback_coords[0], fallback_coords[1])
            self.random_delay(1, 2)
            
            # 执行挑战流程
            if self._perform_challenge():
                return True
        
        return False
    
    def _perform_challenge(self):
        """执行挑战流程"""
        # 查找挑战按钮
        coords = self.vision.wait_for_template(self.tower_images["challenge_button"], timeout=5)
        if coords:
            # 点击挑战按钮
            self.controls.user_click(coords[0], coords[1])
            self.random_delay(1, 2)
            
            # 查找确认按钮
            confirm_coords = self.vision.wait_for_template(self.tower_images["confirm_button"], timeout=5)
            if confirm_coords:
                self.controls.user_click(confirm_coords[0], confirm_coords[1])
            else:
                # 使用备用坐标点击确认
                self.controls.user_click(self.coordinates["confirm_button"][0], self.coordinates["confirm_button"][1])
            
            self.random_delay(1, 2)
            
            # 等待挑战完成
            if self._wait_for_challenge_completion():
                return True
        else:
            # 使用备用坐标点击挑战
            self.controls.user_click(self.coordinates["challenge_button"][0], self.coordinates["challenge_button"][1])
            self.random_delay(1, 2)
            
            # 查找确认按钮
            confirm_coords = self.vision.wait_for_template(self.tower_images["confirm_button"], timeout=5)
            if confirm_coords:
                self.controls.user_click(confirm_coords[0], confirm_coords[1])
            else:
                # 使用备用坐标点击确认
                self.controls.user_click(self.coordinates["confirm_button"][0], self.coordinates["confirm_button"][1])
            
            self.random_delay(1, 2)
            
            # 等待挑战完成
            if self._wait_for_challenge_completion():
                return True
        
        return False
    
    def _wait_for_challenge_completion(self):
        """等待挑战完成"""
        import time
        
        # 等待一段时间让挑战完成
        time.sleep(10)
        
        # 检查是否有完成按钮
        coords = self.vision.wait_for_template(self.tower_images["tower_complete"], timeout=5)
        if coords:
            # 点击完成
            self.controls.user_click(self.coordinates["tower_complete"][0], self.coordinates["tower_complete"][1])
            self.random_delay(1, 2)
            return True
        
        # 检查是否需要重试
        coords = self.vision.wait_for_template(self.tower_images["tower_retry"], timeout=3)
        if coords:
            # 点击重试
            self.controls.user_click(self.coordinates["tower_retry"][0], self.coordinates["tower_retry"][1])
            self.random_delay(1, 2)
            return False  # 重试表示挑战失败
        
        return True  # 如果没有特殊按钮，默认挑战成功
    


# 测试代码
if __name__ == '__main__':
    print("TowerTask 模块测试")
    # 这里可以添加测试代码