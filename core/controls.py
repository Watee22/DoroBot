import pyautogui
import time

class Controls:
    def __init__(self):
        """
        初始化鼠标/键盘控制器。
        """
        # 启用 pyautogui 的安全特性：将鼠标猛地移到屏幕左上角会中断程序
        pyautogui.FAILSAFE = True
        # 为所有 pyautogui 操作添加一个短暂的通用延迟，使其更稳定
        pyautogui.PAUSE = 0.25 
        print("[Controls] 控制器已初始化 (安全模式: ON, 默认暂停: 0.25s)")

    def click_at(self, x, y):
        """在指定坐标 (x, y) 执行一次安全的单击。"""
        try:
            # 先移动再点击，更像人类
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.doubleClick()
            print(f"[Controls] Clicked at ({int(x)}, {int(y)})")
        except pyautogui.FailSafeException:
            print("[Controls] 安全模式触发！程序已由用户中断。")
            # 在实际的机器人中，我们应该在这里干净地退出
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