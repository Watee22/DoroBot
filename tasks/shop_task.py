#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商店购买任务模块
处理游戏商店购买相关的自动化任务
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class ShopTask(Task):
    """商店购买任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 商店图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.shop_images = {
            "shop_tab": f"{self.game_images_path}shop_tab.png",
            "cash_shop": f"{self.game_images_path}cash_shop.png",
            "general_shop": f"{self.game_images_path}general_shop.png",
            "arena_shop": f"{self.game_images_path}arena_shop.png",
            "recycle_shop": f"{self.game_images_path}recycle_shop.png",
            "buy_button": f"{self.game_images_path}buy_button.png",
            "confirm_button": f"{self.game_images_path}confirm_button.png",
            "purchase_button": f"{self.game_images_path}purchase_button.png",
            "shop_confirm": f"{self.game_images_path}shop_confirm.png",
            "shop_complete": f"{self.game_images_path}shop_complete.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "shop_tab": (380, 180),
            "cash_shop": (320, 220),
            "general_shop": (420, 240),
            "arena_shop": (520, 260),
            "recycle_shop": (620, 280),
            "buy_button": (720, 540),
            "confirm_button": (670, 490),
            "purchase_button": (580, 400),
            "shop_confirm": (620, 340),
            "shop_complete": (670, 490)
        }
    
    def run(self) -> bool:
        """执行商店购买任务，基于AHK商店购买逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行商店购买任务")
        
        success_count = 0
        
        # 首先导航到商店
        if self._navigate_to_shop():
            # 购买现金商店物品
            if self.settings.get("ShopCash", 1):
                if self._purchase_from_shop("cash_shop", self.coordinates["cash_shop"]):
                    logger.info("现金商店购买成功")
                    success_count += 1
            
            # 购买普通商店物品
            if self.settings.get("ShopGeneral", 1):
                if self._purchase_from_shop("general_shop", self.coordinates["general_shop"]):
                    logger.info("普通商店购买成功")
                    success_count += 1
            
            # 购买竞技场商店物品
            if self.settings.get("ShopArena", 1):
                if self._purchase_from_shop("arena_shop", self.coordinates["arena_shop"]):
                    logger.info("竞技场商店购买成功")
                    success_count += 1
            
            # 购买回收商店物品
            if self.settings.get("ShopRecycle", 1):
                if self._purchase_from_shop("recycle_shop", self.coordinates["recycle_shop"]):
                    logger.info("回收商店购买成功")
                    success_count += 1
        
        logger.info(f"商店购买任务完成，成功购买{success_count}个商店物品")
        return success_count > 0
    
    def _navigate_to_shop(self):
        """导航到商店"""
        # 查找商店标签
        coords = self.vision.wait_for_template(self.shop_images["shop_tab"], timeout=5)
        if coords:
            # 点击进入商店
            self.controls.user_click(coords[0], coords[1])
            self.random_delay(1, 2)
            return True
        else:
            # 使用备用坐标点击
            self.controls.user_click(self.coordinates["shop_tab"][0], self.coordinates["shop_tab"][1])
            self.random_delay(1, 2)
            return True
        
        return False
    
    def _purchase_from_shop(self, shop_image_key, fallback_coords):
        """
        从特定商店购买物品
        类似AHK的商店购买逻辑
        """
        # 查找商店类型图标
        coords = self.vision.wait_for_template(self.shop_images[shop_image_key], timeout=5)
        if coords:
            # 点击进入商店
            self.controls.user_click(coords[0], coords[1])
            self.random_delay(1, 2)
            
            # 执行购买流程
            if self._perform_purchase():
                return True
        else:
            # 使用备用坐标点击
            self.controls.user_click(fallback_coords[0], fallback_coords[1])
            self.random_delay(1, 2)
            
            # 执行购买流程
            if self._perform_purchase():
                return True
        
        return False
    
    def _perform_purchase(self):
        """执行购买流程"""
        # 查找购买按钮
        coords = self.vision.wait_for_template(self.shop_images["buy_button"], timeout=5)
        if coords:
            # 点击购买按钮
            self.controls.user_click(coords[0], coords[1])
            self.random_delay(1, 2)
            
            # 查找确认按钮
            confirm_coords = self.vision.wait_for_template(self.shop_images["confirm_button"], timeout=5)
            if confirm_coords:
                self.controls.user_click(confirm_coords[0], confirm_coords[1])
            else:
                # 使用备用坐标点击确认
                self.controls.user_click(self.coordinates["confirm_button"][0], self.coordinates["confirm_button"][1])
            
            self.random_delay(1, 2)
            
            # 确认购买完成
            if self._confirm_purchase_completion():
                return True
        else:
            # 使用备用坐标点击购买
            self.controls.user_click(self.coordinates["buy_button"][0], self.coordinates["buy_button"][1])
            self.random_delay(1, 2)
            
            # 查找确认按钮
            confirm_coords = self.vision.wait_for_template(self.shop_images["confirm_button"], timeout=5)
            if confirm_coords:
                self.controls.user_click(confirm_coords[0], confirm_coords[1])
            else:
                # 使用备用坐标点击确认
                self.controls.user_click(self.coordinates["confirm_button"][0], self.coordinates["confirm_button"][1])
            
            self.random_delay(1, 2)
            
            # 确认购买完成
            if self._confirm_purchase_completion():
                return True
        
        return False
    
    def _confirm_purchase_completion(self):
        """确认购买完成操作"""
        # 检查是否需要确认购买
        coords = self.vision.wait_for_template(self.shop_images["shop_confirm"], timeout=3)
        if coords:
            # 点击确认
            self.controls.user_click(self.coordinates["shop_confirm"][0], self.coordinates["shop_confirm"][1])
            self.random_delay(1, 2)
            return True
        
        # 检查是否有完成按钮
        coords = self.vision.wait_for_template(self.shop_images["shop_complete"], timeout=3)
        if coords:
            # 点击完成
            self.controls.user_click(self.coordinates["shop_complete"][0], self.coordinates["shop_complete"][1])
            self.random_delay(1, 2)
            return True
        
        # 购买竞技场商店物品（如果启用）
        if self.settings.get("ShopArena", 1):
            self._purchase_shop_items("arena")
        
        # 购买回收商店物品（如果启用）
        if self.settings.get("ShopRecycling", 1):
            self._purchase_shop_items("recycling")
        
        logging.getLogger(__name__).info("商店购买任务完成")
        return True
    
    def _purchase_shop_items(self, shop_type: str):
        """购买特定商店类型的物品"""
        logging.getLogger(__name__).info(f"购买{shop_type}商店物品")
        
        # 模拟点击购买按钮
        for i in range(5):  # 模拟购买5个物品
            if not self.bot.is_running:
                break
            
            if self.vision.wait_and_click(self.shop_images["buy_button"], timeout=3):
                self.random_delay(0.5, 1)
                if self.vision.wait_and_click(self.shop_images["confirm_button"], timeout=3):
                    self.random_delay(0.5, 1)
    
 
# 测试代码
if __name__ == '__main__':
    print("ShopTask 模块测试")
    # 这里可以添加测试代码