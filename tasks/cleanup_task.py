#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务清理模块
处理任务执行后的清理工作
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class CleanupTask(Task):
    """任务清理类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 清理任务图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.cleanup_images = {
            "upgrade_loop_room": f"{self.game_images_path}upgrade_loop_room.png",
            "synchronizer": f"{self.game_images_path}synchronizer.png",
            "nikke_enhancement": f"{self.game_images_path}nikke_enhancement.png",
            "equipment_enhancement": f"{self.game_images_path}equipment_enhancement.png",
            "skill_enhancement": f"{self.game_images_path}skill_enhancement.png",
            "bond_level": f"{self.game_images_path}bond_level.png",
            "cleanup_confirm": f"{self.game_images_path}cleanup_confirm.png",
            "cleanup_complete": f"{self.game_images_path}cleanup_complete.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "upgrade_click": (320, 180),
            "synchronizer_click": (420, 220),
            "nikke_click": (520, 260),
            "equipment_click": (620, 300),
            "skill_click": (370, 340),
            "bond_click": (470, 380),
            "confirm_click": (720, 520),
            "complete_click": (670, 470)
        }
    
    def run(self) -> bool:
        """执行任务清理，基于AHK清理逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行任务清理")
        
        success_count = 0
        
        # 升级循环室
        if self.settings.get("CleanupUpgradeLoopRoom", 0):
            if self._perform_cleanup("upgrade_loop_room", self.coordinates["upgrade_click"]):
                logger.info("升级循环室成功")
                success_count += 1
        
        # 同步器处理
        if self.settings.get("CleanupSynchronizer", 0):
            if self._perform_cleanup("synchronizer", self.coordinates["synchronizer_click"]):
                logger.info("同步器处理成功")
                success_count += 1
        
        # 强化妮姬
        if self.settings.get("CleanupNIKKEEnhancement", 0):
            if self._perform_cleanup("nikke_enhancement", self.coordinates["nikke_click"]):
                logger.info("强化妮姬成功")
                success_count += 1
        
        # 强化装备
        if self.settings.get("CleanupEquipmentEnhancement", 0):
            if self._perform_cleanup("equipment_enhancement", self.coordinates["equipment_click"]):
                logger.info("强化装备成功")
                success_count += 1
        
        # 强化技能
        if self.settings.get("CleanupSkillEnhancement", 0):
            if self._perform_cleanup("skill_enhancement", self.coordinates["skill_click"]):
                logger.info("强化技能成功")
                success_count += 1
        
        # 提升羁绊等级
        if self.settings.get("CleanupBondLevel", 0):
            if self._perform_cleanup("bond_level", self.coordinates["bond_click"]):
                logger.info("提升羁绊等级成功")
                success_count += 1
        
        logger.info(f"任务清理完成，成功处理{success_count}项清理工作")
        return success_count > 0
    
    def _perform_cleanup(self, image_key, fallback_coords):
        """
        执行特定类型的清理任务
        类似AHK的清理逻辑
        """
        if self.find_and_click(self.cleanup_images[image_key], fallback_coords, timeout=5):
            self.random_delay(1, 2)
            if self._confirm_cleanup():
                return True
        
        return False
    
    def _confirm_cleanup(self):
        """确认清理操作"""
        # 检查是否需要确认清理
        if self.find_and_click(self.cleanup_images["cleanup_confirm"], self.coordinates["confirm_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        # 检查是否有完成按钮
        if self.find_and_click(self.cleanup_images["cleanup_complete"], self.coordinates["complete_click"], timeout=3):
            self.random_delay(1, 2)
            return True
        
        return True  # 如果没有确认步骤，默认成功
    
    

# 测试代码
if __name__ == '__main__':
    print("CleanupTask 模块测试")
    # 这里可以添加测试代码