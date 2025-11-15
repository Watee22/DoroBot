from __future__ import annotations
from typing import Any, Dict, Optional, Tuple
import time
import random

class Task:
    """
    所有任务模块的基类。
    提供与 AHK 脚本常用流程对齐的通用辅助方法。
    """
    def __init__(self, bot_instance: Any) -> None:
        """
        初始化任务。
        :param bot_instance: 主 DoroBot 类的实例。
        """
        self.bot = bot_instance
        self.vision = bot_instance.vision
        self.controls = bot_instance.controls
        self.config = bot_instance.config

    def run(self) -> bool:
        """子类必须实现的任务入口，返回任务是否成功。"""
        raise NotImplementedError("你必须在子类中实现 run() 方法")

    def random_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0) -> float:
        """
        随机延迟，模拟人类行为。
        :param min_seconds: 最小延迟秒数
        :param max_seconds: 最大延迟秒数
        :return: 实际延迟秒数
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay

    def find_and_click(self, image_path: str, fallback_coords: Optional[Tuple[int, int]] = None, timeout: int = 10) -> bool:
        """
        查找模板并点击；找不到时可回退点击备用坐标。
        :param image_path: 模板路径
        :param fallback_coords: 备用坐标 (x, y)
        :param timeout: 超时时间秒
        :return: 是否执行了点击
        """
        coords = self.vision.wait_for_template(image_path, timeout=timeout)
        if coords:
            self.controls.user_click(int(coords[0]), int(coords[1]))
            return True
        if fallback_coords is not None:
            self.controls.user_click(fallback_coords[0], fallback_coords[1])
            return True
        return False

    def press_escape(self) -> None:
        """
        模拟按下 Esc，与 AHK 的 GoBack 中的 Send "{Esc}" 对齐。
        """
        if hasattr(self.controls, "press_key"):
            self.controls.press_key("esc")

    def confirm_click(self, coords: Tuple[int, int]) -> None:
        """
        点击确认位置，与 AHK 的 Confirm() 对齐。
        :param coords: 确认按钮坐标 (x, y)
        """
        self.controls.user_click(coords[0], coords[1])