import cv2
import numpy as np
import os
import time

class Vision:
    def __init__(self, screen_instance, default_confidence=0.8):
        """
        初始化视觉处理器。
        :param screen_instance: 一个已经实例化的 Screen 对象 (来自 core.screen)
        :param default_confidence: 默认的相似度阈值
        """
        self.screen = screen_instance # 依赖注入
        self.default_confidence = default_confidence
        self.template_cache = {} # (可选) 用于缓存已加载的模板
        print(f"[Vision] 视觉核心已初始化 (默认相似度: {default_confidence})")

    def _load_template(self, template_path):
        """私有方法，用于加载或从缓存中读取模板。"""
        if template_path in self.template_cache:
            return self.template_cache[template_path]

        if not os.path.exists(template_path):
            print(f"[Vision] 错误: 模板文件未找到 {template_path}")
            return None, (0, 0)
        
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        
        if template is None:
            print(f"[Vision] 错误: 无法使用 OpenCV 读取模板 {template_path}")
            return None, (0, 0)
        
        try:
            h, w = template.shape[:2]
            self.template_cache[template_path] = (template, (w, h))
            return template, (w, h)
        except AttributeError:
            print(f"[Vision] 模板文件 {template_path} 加载失败或格式错误")
            return None, (0, 0)

    def find_template(self, template_path, confidence=None):
        """
        在屏幕上查找模板图像。
        返回: (x, y) 中心坐标 (如果找到) 或 None (如果未找到)。
        """
        if confidence is None:
            confidence = self.default_confidence
            
        template, (template_w, template_h) = self._load_template(template_path)
        if template is None:
            return None

        # 1. 截取屏幕 (通过我们持有的 screen 实例)
        screen = self.screen.capture()

        # 2. 执行模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        # 3. 获取最匹配的位置和相似度
        _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(result)
        
        # 4. 检查相似度是否达到阈值
        if max_val >= confidence:
            # 5. 计算中心点坐标
            center_x = max_loc[0] + template_w / 2
            center_y = max_loc[1] + template_h / 2
            
            return (center_x, center_y)

        # 6. 未找到
        return None

    def wait_for_template(self, template_path, timeout=10, confidence=None, interval=0.5):
        """
        在 'timeout' 秒内循环查找模板，直到找到或超时。
        """
        print(f"[Vision] 正在等待 {os.path.basename(template_path)} (超时: {timeout}s)")
        start_time = time.time()
        
        while True:
            # 在循环中调用我们自己的 find_template 方法
            coords = self.find_template(template_path, confidence)
            if coords:
                print(f"[Vision] 成功找到 {os.path.basename(template_path)} at {coords}")
                return coords
            
            if time.time() - start_time > timeout:
                print(f"[Vision] 超时: {timeout}秒内未找到 {os.path.basename(template_path)}")
                return None
            
            time.sleep(interval)

    def set_controls(self, controls_instance):
        """设置Controls实例用于点击操作"""
        self.controls = controls_instance
        print(f"[Vision] Controls实例已设置: {controls_instance}")

    def wait_and_click(self, template_path, timeout=10, confidence=None, interval=0.5):
        """
        等待模板出现并点击它。
        """
        coords = self.wait_for_template(template_path, timeout, confidence, interval)
        if coords:
            # 使用controls进行点击
            if hasattr(self, 'controls'):
                self.controls.click_at(coords[0], coords[1])
                return True
            else:
                print("[Vision] 警告: 未设置Controls实例，无法执行点击操作")
        return False

    def wait_for_image(self, template_path, timeout=10, confidence=None, interval=0.5):
        """
        等待图像出现，不执行点击。
        """
        coords = self.wait_for_template(template_path, timeout, confidence, interval)
        return coords is not None