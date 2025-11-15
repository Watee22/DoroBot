#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录任务模块
处理游戏登录相关的自动化任务
基于AHK脚本逻辑实现
"""

import time
import logging
from typing import Dict, Any
from tasks.basic_task import Task

class LoginTask(Task):
    """登录任务类"""
    
    def __init__(self, bot, settings: Dict[str, Any], numeric_settings: Dict[str, Any]):
        super().__init__(bot)
        self.settings = settings
        self.numeric_settings = numeric_settings
        
        # 游戏特定图片路径，匹配AHK脚本中的图像资源
        self.game_images_path = "templates/"
        self.login_images = {
            "start_button": f"{self.game_images_path}start_button.png",
            "login_button": f"{self.game_images_path}login_button.png",
            "main_menu": f"{self.game_images_path}main_menu.png",
            "sign_reward": f"{self.game_images_path}sign_reward.png",
            "server_confirm": f"{self.game_images_path}server_confirm.png",
            "download_content": f"{self.game_images_path}download_content.png"
        }
        
        # 坐标设置，类似AHK脚本中的坐标定义
        self.coordinates = {
            "start_click": (500, 500),
            "login_click": (600, 400),
            "sign_close": (800, 200),
            "server_ok": (700, 500),
            "download_confirm": (750, 450)
        }
    
    def run(self) -> bool:
        """执行登录任务，基于AHK Login()函数逻辑"""
        logger = logging.getLogger(__name__)
        logger.info("开始执行登录任务")
        
        # 检查游戏是否运行，类似AHK中的窗口检查
        if not self._is_game_running():
            if not self._start_game():
                return False
        
        # 等待开始按钮并点击，类似AHK的FindText和UserClick
        if self.find_and_click(self.login_images["start_button"], self.coordinates["start_click"], timeout=30):
            self.random_delay(1, 2)
            
            # 处理签到奖励，类似AHK中的逻辑
            if self._handle_sign_reward():
                logger.info("签到奖励处理完成")
            
            # 等待登录按钮并点击
            if self.find_and_click(self.login_images["login_button"], self.coordinates["login_click"], timeout=20):
                self.random_delay(2, 3)
                
                # 确认服务器选择，类似AHK中的服务器确认
                if self._confirm_server():
                    logger.info("服务器确认完成")
                
                # 处理下载内容确认
                if self._handle_download():
                    logger.info("下载内容处理完成")
                
                # 等待主菜单出现，表示登录成功
                if self.vision.wait_for_image(self.login_images["main_menu"], timeout=30):
                    logger.info("登录成功")
                    return True
        
        logger.error("登录失败")
        return False
    

    
    def _handle_sign_reward(self):
        """处理签到奖励，类似AHK脚本中的逻辑"""
        # 检查是否有签到奖励
        coords = self.vision.wait_for_template(self.login_images["sign_reward"], timeout=5)
        if coords:
            # 点击关闭签到奖励
            self.controls.user_click(self.coordinates["sign_close"][0], self.coordinates["sign_close"][1])
            self.random_delay(1, 2)
            return True
        return False
    
    def _confirm_server(self):
        """确认服务器选择，类似AHK脚本中的逻辑"""
        # 检查是否需要确认服务器
        coords = self.vision.wait_for_template(self.login_images["server_confirm"], timeout=5)
        if coords:
            # 点击确认服务器
            self.controls.user_click(self.coordinates["server_ok"][0], self.coordinates["server_ok"][1])
            self.random_delay(1, 2)
            return True
        return False
    
    def _handle_download(self):
        """处理下载内容确认，类似AHK脚本中的逻辑"""
        # 检查是否有下载内容需要确认
        coords = self.vision.wait_for_template(self.login_images["download_content"], timeout=5)
        if coords:
            # 点击确认下载
            self.controls.user_click(self.coordinates["download_confirm"][0], self.coordinates["download_confirm"][1])
            self.random_delay(1, 2)
            return True
        return False
    
    
    def _is_game_running(self) -> bool:
        """检查游戏是否在运行"""
        try:
            import psutil
            for process in psutil.process_iter(['name']):
                if 'nikkei' in process.info['name'].lower():
                    return True
        except Exception:
            pass
        return False
    
    def _start_game(self) -> bool:
        """启动游戏"""
        startup_path = self.numeric_settings.get("StartupPath", "")
        if startup_path:
            try:
                import subprocess
                subprocess.Popen([startup_path])
                time.sleep(5)
                return True
            except Exception as e:
                logging.getLogger(__name__).error(f"启动游戏失败: {e}")
                return False
        return False
    


# 测试代码
if __name__ == '__main__':
    print("LoginTask 模块测试")
    # 这里可以添加测试代码