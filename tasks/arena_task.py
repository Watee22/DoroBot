#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞技场任务模块
处理游戏竞技场战斗相关的自动化任务
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class ArenaTask(Task):
    """竞技场任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 竞技场图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.arena_images = {
            "arena_tab": f"{self.game_images_path}arena_tab.png",
            "battle_button": f"{self.game_images_path}battle_button.png",
            "victory": f"{self.game_images_path}victory.png",
            "defeat": f"{self.game_images_path}defeat.png",
            "arena_rookie": f"{self.game_images_path}arena_rookie.png",
            "arena_award": f"{self.game_images_path}arena_award.png",
            "arena_confirm": f"{self.game_images_path}arena_confirm.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "arena_tab_click": (300, 100),
            "battle_click": (500, 300),
            "rookie_click": (400, 200),
            "award_click": (600, 400),
            "confirm_click": (700, 500)
        }
    
    def run(self) -> bool:
        """执行竞技场任务，基于AHK竞技场脚本逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行竞技场任务")
        
        # 竞技场收菜，类似AHK的AwardArena()函数
        if self._award_arena():
            logger.info("竞技场奖励领取完成")
        
        # 进入竞技场，类似AHK的EnterToArena()函数
        if self._enter_to_arena():
            logger.info("成功进入竞技场")
            
            # 执行新人竞技场，类似AHK的ArenaRookie()函数
            if self._arena_rookie():
                logger.info("新人竞技场任务完成")
                return True
        
        logger.error("竞技场任务失败")
        return False
    
    def _award_arena(self):
        """竞技场收菜，类似AHK的AwardArena()函数"""
        # 检查是否有竞技场奖励
        coords = self.vision.wait_for_template(self.arena_images["arena_award"], timeout=5)
        if coords:
            # 点击领取奖励
            self.controls.user_click(self.coordinates["award_click"][0], self.coordinates["award_click"][1])
            self.random_delay(1, 2)
            
            # 确认领取
            if self._confirm_operation():
                return True
        return False
    
    def _enter_to_arena(self):
        """进入竞技场，类似AHK的EnterToArena()函数"""
        # 点击竞技场标签
        if self.find_and_click(self.arena_images["arena_tab"], self.coordinates["arena_tab_click"], timeout=10):
            self.random_delay(1, 2)
            return True
        return False
    
    def _arena_rookie(self):
        """新人竞技场，类似AHK的ArenaRookie()函数"""
        # 检查是否有新人竞技场
        coords = self.vision.wait_for_template(self.arena_images["arena_rookie"], timeout=5)
        if coords:
            # 点击新人竞技场
            self.controls.user_click(self.coordinates["rookie_click"][0], self.coordinates["rookie_click"][1])
            self.random_delay(1, 2)
            
            # 点击战斗按钮
            if self.find_and_click(self.arena_images["battle_button"], self.coordinates["battle_click"], timeout=10):
                logging.getLogger(__name__).info("点击战斗按钮")
                self.random_delay(2, 3)
                
                # 等待战斗结果
                result_found = False
                for _ in range(60):  # 最多等待60秒战斗完成
                    if not self.bot.is_running:
                        break
                    
                    # 检查胜利或失败
                    if self.vision.wait_for_image(self.arena_images["victory"], timeout=1):
                        logging.getLogger(__name__).info("战斗胜利")
                        result_found = True
                        break
                    elif self.vision.wait_for_image(self.arena_images["defeat"], timeout=1):
                        logging.getLogger(__name__).info("战斗失败")
                        result_found = True
                        break
                    
                    time.sleep(1)
                
                if not result_found:
                    logging.getLogger(__name__).error("战斗超时")
                    return False
                
                # 点击继续
                self.random_delay(2, 3)
                self.press_escape()
                return True
        return False
    
    def _confirm_operation(self):
        """确认操作，类似AHK中的确认逻辑"""
        # 检查是否需要确认
        coords = self.vision.wait_for_template(self.arena_images["arena_confirm"], timeout=3)
        if coords:
            # 点击确认
            self.controls.user_click(self.coordinates["confirm_click"][0], self.coordinates["confirm_click"][1])
            self.random_delay(1, 2)
            return True
        return False

# 测试代码
if __name__ == '__main__':
    print("ArenaTask 模块测试")
    # 这里可以添加测试代码