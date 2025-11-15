import pyautogui
import time
import math

class Controls:
    def __init__(self, screen_instance=None):
        """
        初始化鼠标/键盘控制器。
        :param screen_instance: Screen实例，用于坐标转换
        """
        # 启用 pyautogui 的安全特性：将鼠标猛地移到屏幕左上角会中断程序
        pyautogui.FAILSAFE = True
        # 为所有 pyautogui 操作添加一个短暂的通用延迟，使其更稳定
        pyautogui.PAUSE = 0.25 
        self.screen = screen_instance
        print("[Controls] 控制器已初始化 (安全模式: ON, 默认暂停: 0.25s)")
    
    def set_screen(self, screen_instance):
        """设置Screen实例用于坐标转换"""
        self.screen = screen_instance

    def user_click(self, sX, sY, k=1.0):
        """
        点击转换后的坐标，类似AHK的UserClick函数
        :param sX: 源X坐标
        :param sY: 源Y坐标  
        :param k: 缩放因子
        """
        uX = round(sX * k)
        uY = round(sY * k)
        try:
            pyautogui.moveTo(uX, uY, duration=0.1)
            pyautogui.click()
            print(f"[Controls] UserClick at ({uX}, {uY}) from source ({sX}, {sY}) with scale {k}")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            import sys
            sys.exit(1)

    def user_press(self, sX, sY, k=1.0):
        """
        按住鼠标，类似AHK的UserPress函数
        :param sX: 源X坐标
        :param sY: 源Y坐标
        :param k: 缩放因子
        """
        uX = round(sX * k)
        uY = round(sY * k)
        try:
            pyautogui.mouseDown(uX, uY)
            print(f"[Controls] UserPress at ({uX}, {uY}) from source ({sX}, {sY}) with scale {k}")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            import sys
            sys.exit(1)

    def user_move(self, sX, sY, k=1.0):
        """
        移动鼠标，类似AHK的UserMove函数
        :param sX: 源X坐标
        :param sY: 源Y坐标
        :param k: 缩放因子
        """
        uX = round(sX * k)
        uY = round(sY * k)
        try:
            pyautogui.moveTo(uX, uY, duration=0.2)
            print(f"[Controls] UserMove to ({uX}, {uY}) from source ({sX}, {sY}) with scale {k}")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            import sys
            sys.exit(1)

    def is_similar_color(self, target_color, color, threshold=15):
        """
        颜色相似度判断，类似AHK的IsSimilarColor函数
        :param target_color: 目标颜色 (格式: "#RRGGBB")
        :param color: 比较颜色 (格式: "#RRGGBB")
        :param threshold: 相似度阈值
        :return: 是否相似
        """
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        tr, tg, tb = hex_to_rgb(target_color)
        pr, pg, pb = hex_to_rgb(color)
        distance = math.sqrt((tr - pr) ** 2 + (tg - pg) ** 2 + (tb - pb) ** 2)
        return distance < threshold

    def click_at(self, x, y):
        """在指定坐标 (x, y) 执行一次安全的单击。"""
        try:
            # 先移动再点击，更像人类
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.doubleClick()
            print(f"[Controls] Clicked at ({int(x)}, {int(y)})")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            import sys
            sys.exit(1)

    def move_to(self, x, y, duration=0.2):
        """平滑移动鼠标到 (x, y)，用于调试或查看。"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            print(f"[Controls] Moved to ({int(x)}, {int(y)})")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            import sys
            sys.exit(1)

    def press_key(self, key):
        try:
            pyautogui.press(key)
            print(f"[Controls] Pressed key {key}")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            import sys
            sys.exit(1)

    def get_pixel_color(self, x, y):
        """获取指定坐标的像素颜色，返回格式为"#RRGGBB" """
        try:
            r, g, b = pyautogui.pixel(x, y)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception as e:
            print(f"[Controls] 错误: 无法获取像素颜色 at ({x}, {y}): {e}")
            return None

    def wait_for_pixel_color(self, x, y, target_color, timeout=10, interval=0.5, threshold=15):
        """
        等待指定坐标的像素颜色匹配目标颜色。
        :param x: X坐标
        :param y: Y坐标
        :param target_color: 目标颜色 (格式: "#RRGGBB")
        :param timeout: 超时时间（秒）
        :param interval: 检查间隔（秒）
        :param threshold: 颜色相似度阈值
        :return: 是否匹配成功
        """
        print(f"[Controls] 等待像素颜色 at ({x}, {y}) 变为 {target_color} (超时: {timeout}s)")
        start_time = time.time()
        while True:
            current_color = self.get_pixel_color(x, y)
            if current_color and self.is_similar_color(target_color, current_color, threshold):
                print(f"[Controls] 像素颜色匹配成功 at ({x}, {y})")
                return True
            if time.time() - start_time > timeout:
                print(f"[Controls] 超时: {timeout}秒内像素颜色未匹配 at ({x}, {y})")
                return False
            time.sleep(interval)

# --- 测试代码 ---
if __name__ == '__main__':
    print("正在测试 Controls 类...")
    controls = Controls()
    print("测试鼠标移动... 5秒后开始")
    print("将鼠标移到左上角可中断程序")
    time.sleep(5)
    controls.move_to(500, 500)
    time.sleep(1)
    controls.move_to(800, 500)
    print("测试完成")