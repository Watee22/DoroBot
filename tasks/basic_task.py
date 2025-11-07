class Task:
    """
    所有任务模块的基类。
    """
    def __init__(self, bot_instance):
        """
        初始化任务。
        :param bot_instance: 主 DoroBot 类的实例。
        """
        # 依赖注入：每个任务都可以通过 self.bot 访问
        # 机器人的所有核心组件 (vision, controls, config)
        self.bot = bot_instance
        self.vision = bot_instance.vision
        self.controls = bot_instance.controls
        self.config = bot_instance.config

    def run(self):
        raise NotImplementedError("你必须在子类中实现 run() 方法")