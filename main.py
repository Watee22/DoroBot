import yaml
import sys
from core.screen import Screen
from core.controls import Controls
from core.vision import Vision
from tasks.test_task import TestTask
from tasks.login_task import LoginTask
from tasks.shop_task import ShopTask
from tasks.arena_task import ArenaTask
from tasks.tower_task import TowerTask
from tasks.simulation_task import SimulationTask
from tasks.interception_task import InterceptionTask
from tasks.event_task import EventTask
from tasks.reward_task import RewardTask
from tasks.cleanup_task import CleanupTask
import pyautogui
# 你将来会在这里导入你真正的任务:
# from tasks.shop_task import ShopTask
# from tasks.arena_task import ArenaTask

class DoroBot:
    def __init__(self, config_path='config.yaml'):
        """
        初始化主机器人。
        """
        print("--- DoroBot 正在启动... ---")
        self.config = self._load_config(config_path)
        
        # 1. 初始化所有核心组件 (机器人的“四肢”)
        try:
            self.screen = Screen()
            self.controls = Controls()
            self.vision = Vision(self.screen, self.config['vision']['default_confidence'])
        except Exception as e:
            print(f"初始化核心组件失败: {e}")
            print("机器人无法启动。")
            sys.exit(1)
            
        # 2. 注册所有可用的任务 (机器人的“大脑”)
        # 我们在这里将 "self" (DoroBot实例) 传递给每个任务
        # 注意：部分任务需要 settings/numeric_settings，本处先以空字典启动，
        # 由各任务内部使用 get(..., 默认值) 保障可运行。
        self.available_tasks = {
            'test_task': TestTask(self),
            'login_task': LoginTask(self, {}, {}),
            'shop_task': ShopTask(self, {}, {}),
            'arena_task': ArenaTask(self, {}, {}),
            'tower_task': TowerTask(self, {}, {}),
            'simulation_task': SimulationTask(self, {}, {}),
            'interception_task': InterceptionTask(self, {}, {}),
            'event_task': EventTask(self, {}, {}),
            'reward_task': RewardTask(self, {}, {}),
            'cleanup_task': CleanupTask(self, {}, {}),
        }
        print("--- DoroBot 初始化完成 ---")

    def _load_config(self, config_path):
        """私有方法，用于加载 YAML 配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                print(f"[Config] 成功加载配置文件: {config_path}")
                return config
        except FileNotFoundError:
            print(f"[Config] 严重错误: 配置文件未找到 {config_path}")
            sys.exit(1)
        except Exception as e:
            print(f"[Config] 严重错误: 解析配置文件失败 {config_path}")
            print(f"错误详情: {e}")
            sys.exit(1)

    def run(self):
        print("\n--- 开始执行任务循环 ---")
        try:
            task_settings = self.config.get('tasks', {})
            runner_opts = self.config.get('task_runner', {})
            break_on_failure = bool(runner_opts.get('break_on_failure', False))

            for task_name, is_enabled in task_settings.items():
                if not is_enabled:
                    print(f"[TaskRunner] --- 跳过任务: {task_name} (已禁用) ---")
                    continue

                if task_name not in self.available_tasks:
                    print(f"[TaskRunner] 警告: 任务 '{task_name}' 在配置中启用，但未在 DoroBot 中注册。")
                    if break_on_failure:
                        print("[TaskRunner] 由于配置错误，终止后续任务。")
                        break
                    continue

                print(f"\n[TaskRunner] === 正在执行任务: {task_name} ===")
                ok = False
                try:
                    ok = bool(self.available_tasks[task_name].run())
                except Exception as e:
                    print(f"[TaskRunner] 任务异常: {task_name}: {e}")
                    ok = False

                if ok:
                    print(f"[TaskRunner] === 任务成功: {task_name} ===")
                else:
                    print(f"[TaskRunner] === 任务失败: {task_name} ===")
                    if break_on_failure:
                        print("[TaskRunner] 失败触发中断，停止后续任务。")
                        break

            print("\n--- 已处理配置中的任务。 ---")

        except KeyboardInterrupt:
            print("\n[DoroBot] 检测到用户中断 (Ctrl+C)。正在退出...")
        except pyautogui.FailSafeException:
            print("\n[DoroBot] 安全模式触发！程序已终止。")
        except Exception as e:
            print(f"\n[DoroBot] 发生未处理的致命错误: {e}")
        finally:
            print("[DoroBot] 正在关闭...")

# --- Python 脚本的主入口点 ---
if __name__ == "__main__":
    # 1. 创建 DoroBot 的实例
    bot = DoroBot(config_path='config.yaml')
    
    # 2. 运行机器人
    bot.run()