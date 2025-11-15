import time
from tasks.basic_task import Task

class TestTask(Task):
    """
    一个演示任务：查找一个图标并移动鼠标过去。
    """
    def __init__(self, bot_instance):
        # 必须调用父类的 __init__ 来设置 self.bot, self.vision 等
        super().__init__(bot_instance)
        
        # 从配置中获取特定于此任务的设置
        self.icon_to_find = 'templates/test_icon.png'
        self.confidence = self.config['vision']['default_confidence']
        self.timeout = self.config['vision']['default_timeout']

    def run(self) -> bool:
        """任务的执行逻辑，返回是否成功"""
        print("--- 自动化测试任务已启动 ---")
        print(f"将在 {self.timeout} 秒内查找图标: {self.icon_to_find}")
        print("请确保 '画图' 应用已打开且图标在屏幕上可见...")
        print("安全提示: 鼠标将在3秒后开始移动。要中断程序，请将鼠标猛地移到屏幕左上角。")
        
        time.sleep(3) # 给你3秒钟准备时间，松开鼠标

        # 1. 调用我们继承的 'vision' 核心函数
        coords = self.vision.wait_for_template(
            template_path=self.icon_to_find,
            timeout=self.timeout,
            confidence=self.confidence
        )

        # 2. 根据结果执行操作
        if coords:
            print(f"成功: 图标找到! 坐标: ({int(coords[0])}, {int(coords[1])})")
            print("正在将鼠标移动到图标上...")
            
            # 调用我们继承的 'controls' 核心函数
            self.controls.move_to(coords[0], coords[1])
            
            # 如果要点击:
            self.controls.click_at(coords[0], coords[1])
            
            print("--- 测试任务完成 ---")
            return True
        else:
            print(f"失败: 在 {self.timeout} 秒内未找到图标。")
            print("请检查:")
            print(" 1. '画图' 应用是否已打开？")
            print(" 2. 'templates/test_icon.png' 截图是否清晰？")
            print("--- 测试任务失败 ---")
            return False