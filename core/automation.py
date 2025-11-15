#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化核心模块
提供通用的自动化功能，如等待、点击、拖拽等
"""

import time
import random
import pyautogui
import cv2
import numpy as np
from typing import Tuple, Optional, List
import logging

class Automation:
    """核心自动化类，提供通用的自动化功能"""
    
    def __init__(self, vision_instance=None, controls_instance=None, default_confidence=0.8):
        """
        初始化自动化器
        :param vision_instance: Vision实例（可选）
        :param controls_instance: Controls实例（可选）
        :param default_confidence: 默认相似度阈值
        """
        self.vision = vision_instance
        self.controls = controls_instance
        self.default_confidence = default_confidence
        self.is_running = False
        
        # 配置pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()
        
        print(f"[Automation] 自动化核心已初始化 (默认相似度: {default_confidence})")
    
    def start_automation(self):
        """开始自动化过程"""
        self.is_running = True
        self.logger.info("自动化开始")
    
    def stop_automation(self):
        """停止自动化过程"""
        self.is_running = False
        self.logger.info("自动化停止")
    
    def wait_and_click_image(self, image_path: str, timeout: int = 10, confidence: float = None) -> bool:
        """等待图像出现并点击它"""
        if confidence is None:
            confidence = self.default_confidence
            
        start_time = time.time()
        
        while time.time() - start_time < timeout and self.is_running:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    self.logger.info(f"点击图片: {image_path} 在位置 {center}")
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.5)
        
        return False
    
    def wait_for_image(self, image_path: str, timeout: int = 10, confidence: float = None) -> bool:
        """等待图像出现"""
        if confidence is None:
            confidence = self.default_confidence
            
        start_time = time.time()
        
        while time.time() - start_time < timeout and self.is_running:
            try:
                if pyautogui.locateOnScreen(image_path, confidence=confidence):
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.5)
        
        return False
    
    def click_at_position(self, x: int, y: int, button: str = 'left'):
        """在特定位置点击"""
        if self.is_running:
            pyautogui.click(x, y, button=button)
            self.logger.info(f"点击位置: ({x}, {y})")
    
    def drag_and_drop(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], duration: float = 0.5):
        """从起始位置拖拽到结束位置"""
        if self.is_running:
            pyautogui.drag(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1], 
                          duration=duration, button='left')
            self.logger.info(f"拖拽从 {start_pos} 到 {end_pos}")
    
    def scroll(self, clicks: int, x: int = None, y: int = None):
        """在位置滚动"""
        if self.is_running:
            pyautogui.scroll(clicks, x, y)
            self.logger.info(f"滚动 {clicks} 次")
    
    def random_delay(self, min_delay: float = 0.5, max_delay: float = 1.5):
        """随机延迟，模拟人类行为"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def press_key(self, key: str):
        """按下键盘按键"""
        if self.is_running:
            pyautogui.press(key)
            self.logger.info(f"按下按键: {key}")
    
    def type_text(self, text: str):
        """输入文本"""
        if self.is_running:
            pyautogui.typewrite(text)
            self.logger.info(f"输入文本: {text}")
    
    def hotkey(self, *keys):
        """组合键"""
        if self.is_running:
            pyautogui.hotkey(*keys)
            self.logger.info(f"组合键: {'+'.join(keys)}")

# --- 测试代码 ---
if __name__ == '__main__':
    print("正在测试 Automation 类...")
    automator = Automation()
    
    # 测试基本功能
    automator.start_automation()
    
    # 测试点击
    automator.click_at_position(100, 100)
    
    # 测试随机延迟
    automator.random_delay(0.1, 0.3)
    
    automator.stop_automation()
    print("测试完成")