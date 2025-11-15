# 交接文档｜DoroBot（d:\PYTHON\DoroBot）

## 1. 项目概述

### 系统功能和业务目标
- 目标：自动化运行 Nikke 等类游戏的日常流程，基于屏幕截图与模板匹配执行点击、按键等操作，按配置依次执行多种“任务”（登录、商店、竞技场、奖励收集、模拟室、拦截战、清理、塔等），并统一返回任务成败状态。
- 特点：
  - 配置驱动：在 `config.yaml` 中按任务名开关选择执行顺序与策略。
  - 任务标准化：所有任务继承 `Task` 基类，统一 `run() -> bool` 入口，提供 `find_and_click`、`random_delay`、`press_escape` 等通用辅助。
  - 稳定与安全：启用 `pyautogui` FAILSAFE（鼠标移到左上角立即中止），加入随机延迟模拟人类操作，统一错误处理与日志打印。

### 技术栈和主要依赖项
- Python 3.x
- 主要依赖（`requirements.txt`）
  - `opencv-python`：模板匹配与图像处理
  - `mss`：屏幕截图
  - `numpy`：数组与图像数据
  - `pyautogui`：鼠标键盘自动化
  - `PyYAML`：YAML 配置解析

### 整体架构图
- 组件交互（ASCII 图）
```
------------------------+
|        main.py         |
|   DoroBot (Runner)     |
| - load config.yaml     |
| - init Screen/Controls |
| - init Vision          |
| - register tasks       |
| - run tasks in order   |
-----------+------------+
            |
            v
------------------------+          +-------------------------+
|         core/          |          |         tasks/          |
| - Screen (mss)         |<-------->| - Task (base)           |
| - Vision (OpenCV)      | controls | - *Task (domain tasks)  |
| - Controls (pyautogui) |----------|   run()->bool, helpers  |
| - Automation (aux)     |   vision +-------------------------+
------------------------+
            ^
            |
-----------+------------+
|        config/         |
| - config.yaml          |
| - config.manager       |
| - schema/migrations    |
------------------------+
```
- 任务执行时序（简化）
  - `DoroBot.run()` 读取 `config.tasks` → 针对启用任务依次执行 `available_tasks[task].run()` → 根据返回值打印成功/失败 → `break_on_failure=false` 时继续下一个任务

> 最后修改人/时间：交付人（AI 助手），2025-11-16

---

## 2. 代码结构说明

### 主要目录结构及职责
- `core/`
  - `screen.py`：基于 mss 的屏幕截图，提供 `capture()` 返回 OpenCV BGR 图像。参考 `core/screen.py:24-35`
  - `vision.py`：模板匹配、等待模板出现、可选点击。参考 `core/vision.py:73-92`（`wait_for_template`）
  - `controls.py`：基于 pyautogui 的点击、移动、按键、像素读取等。参考 `core/controls.py:22-39`（`user_click`）、`core/controls.py:113-121`（`press_key`）
  - `automation.py`：通用自动化封装（备用/可扩展），提供 `wait_and_click_image` 等
  - `__init__.py`：导出核心类
- `tasks/`
  - `basic_task.py`：所有任务基类 `Task`，统一 `run()` 合约与辅助方法。参考 `tasks/basic_task.py:21-65`
  - 各 `*Task`：领域任务，如 `LoginTask`、`ShopTask`、`ArenaTask`、`SimulationTask`、`InterceptionTask`、`EventTask`、`RewardTask`、`CleanupTask`、`TowerTask`，均实现 `run() -> bool`
  - `__init__.py`：导出 `Task` 及各任务类
- `config/`
  - `config.yaml`：项目主配置（视觉参数、任务开关、执行策略）
  - `manager.py`、`schema.py`、`compat.py`、`watch.py`：配置管理与兼容模块（当前主流程未直接使用 `manager.py` 的动态能力，但可扩展）
- `templates/`
  - 存放模板图片，子目录按业务分组（`arena/`、`shop/`、`simulate/` 等）
- `main.py`：程序入口与任务编排。参考 `main.py:72-107`
- `requirements.txt`：依赖清单
- `test_refactored_code.py`：快速导入与基础能力验证脚本

### 核心模块/组件及其交互关系
- DoroBot 构造核心组件与任务（`main.py:21-55`）
  - Screen → Vision 依赖注入（`main.py:31-34`）
  - Controls 提供点击、按键能力
  - `available_tasks` 注册已实现任务实例（`main.py:43-54`）
- 任务通过 `self.vision` 与 `self.controls` 调用核心能力
  - 统一从 `Task` 基类继承，避免重复逻辑

### 重要配置文件和参数说明
- `config.yaml`
  - `vision.default_confidence`：模板匹配阈值（0-1），默认 0.8（`config.yaml:3`）
  - `vision.default_timeout/interval`：等待超时与轮询间隔（`config.yaml:4-5`）
  - `tasks`：任务开关（true/false），按登记名执行（`config.yaml:8-18`）
  - `task_runner.break_on_failure`：任务失败是否中断剩余任务。当前为 `false`（`config.yaml:20-21`）
- `config/schema.py`
  - `DEFAULT_CONFIG` 与 JSON Schema，提供更丰富“`toggles`/`numeric_settings`”结构（`config/schema.py:130-236, 238-260`）

> 最后修改人/时间：交付人（AI 助手），2025-11-16

---

## 3. 关键代码解析

### 统一任务基类与契约
- `Task.run() -> bool`：所有任务均需返回成功/失败（`tasks/basic_task.py:21-24`）
- 通用辅助：
```python
# tasks/basic_task.py
def random_delay(self, min_seconds=0.5, max_seconds=2.0) -> float: ...
def find_and_click(self, image_path, fallback_coords=None, timeout=10) -> bool: ...
def press_escape(self) -> None: ...
def confirm_click(self, coords: Tuple[int, int]) -> None: ...
```
- `find_and_click` 先用 `Vision.wait_for_template` 定位元素，找不到则点击 fallback 坐标（`tasks/basic_task.py:36-51`）

### 视觉识别与等待
- `Vision.wait_for_template`：在 `timeout` 内轮询模板匹配，返回坐标或 `None`（`core/vision.py:73-92`）
- `Vision.wait_and_click`：封装等待与点击（`core/vision.py:98-110`）

### 控制层关键接口
- `Controls.user_click`：坐标转换+移动+点击，带 FAILSAFE（`core/controls.py:22-39`）
- `Controls.press_key`：按键封装（`core/controls.py:113-121`）

### 任务编排主循环
```python
# main.py
def run(self):
    task_settings = self.config.get('tasks', {})
    break_on_failure = bool(self.config.get('task_runner', {}).get('break_on_failure', False))
    for task_name, is_enabled in task_settings.items():
        if not is_enabled: continue
        if task_name not in self.available_tasks:
            ... # 可配置选择是否中断
            continue
        ok = False
        try:
            ok = bool(self.available_tasks[task_name].run())
        except Exception as e:
            ok = False
        if not ok and break_on_failure:
            break
```
参考 `main.py:72-107`

### 代表性任务流程（示例：登录任务）
- 步骤：
  - 启动或检测游戏进程（`_is_game_running`/`_start_game`）`tasks/login_task.py:116-139`
  - 找“开始”按钮→点击→随机延迟→处理签到→找“登录”→确认服务器→处理下载→等待主菜单出现→`True`（`tasks/login_task.py:52-78`）
- 片段：
```python
if self.find_and_click(self.login_images["start_button"], self.coordinates["start_click"], timeout=30):
    self.random_delay(1, 2)
    if self._handle_sign_reward(): ...
    if self.find_and_click(self.login_images["login_button"], self.coordinates["login_click"], timeout=20):
        self.random_delay(2, 3)
        if self._confirm_server(): ...
        if self._handle_download(): ...
        if self.vision.wait_for_image(self.login_images["main_menu"], timeout=30):
            return True
return False
```

### 特殊处理或注意点
- FAILSAFE：移动鼠标到屏幕左上角触发 `pyautogui.FailSafeException`，程序会优雅退出（`core/controls.py:12, 35-39`；`main.py:111-116`）
- 模板路径与资源：`templates` 目录需包含对应 `png`，否则 Vision 会打印错误并找不到模板（`core/vision.py:23-39`）
- 返回值契约：所有任务 `run()` 必须返回 `bool`；主循环依赖此值决定日志与是否（可选）中断
- 备用坐标回退：`find_and_click` 支持 fallback 坐标，适配分辨率或识别不稳定场景

> 最后修改人/时间：交付人（AI 助手），2025-11-16

---

## 4. 开发环境

### 本地开发设置指南（Windows）
- 建议 Python 3.10/3.11
- 安装依赖
```powershell
cd d:\PYTHON\DoroBot
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
- 显示器与权限
  - 确保 Windows 桌面可见，避免远程桌面图像加速导致截图异常
  - 以具有屏幕读取与输入模拟权限的用户运行

### 构建和部署流程
- 本项目为脚本型运行，无需打包即可执行：
```powershell
python main.py
```
- 可选：使用 PyInstaller 打包为 exe（不在当前仓库内）

### 测试方法和验证要点
- 快速验证脚本：`test_refactored_code.py`
```powershell
python test_refactored_code.py
```
  - 验证导入与核心组件可实例化（`test_refactored_code.py:14-42`）
  - 验证 tasks 模块可导入（`test_refactored_code.py:44-73`）
- 交互式验证
  - 在屏幕可见时运行 `TestTask`（确保 `templates/test_icon.png` 可被识别）
- 验证要点
  - 模板路径有效、识别阈值合适
  - FAILSAFE 有效（安全中断）
  - 配置任务开关生效、`run()` 返回值正确传递到主循环

> 最后修改人/时间：交付人（AI 助手），2025-11-16

---

## 5. 运维信息

### 运行与监控
- 启动：
```powershell
python main.py
```
- 关键日志输出：
  - 配置加载成功与错误（`main.py:57-71`）
  - 任务循环开始/结束（`main.py:72-107`）
  - 任务执行结果 Success/Fail（`main.py:99-105`）
  - Vision 等待日志与匹配结果（`core/vision.py:77-89`）
- 建议监控指标（可在后续引入 logger + 结构化输出）：
  - 单任务成功率、平均执行时长
  - 模板识别超时次数
  - FAILSAFE 触发次数

### 常见问题排查指南
- 模板无法识别/超时
  - 核对模板路径与文件是否存在（`core/vision.py:23-39`）
  - 调整 `config.yaml` 中 `default_confidence`（过高会导致识别失败），或补充更清晰模板
  - 检查分辨率/缩放变化导致坐标偏差，适当使用 fallback 坐标
- 程序被立刻中断
  - 检查 `pyautogui` FAILSAFE：鼠标是否位于左上角（`core/controls.py:12`；`main.py:111-116`）
- 权限/显示器问题
  - `mss` 初始化失败时会打印显示器信息（`core/screen.py:16-22`），确认显示器编号
- 任务未执行
  - 检查 `config.yaml` 的 `tasks` 开关（`config.yaml:8-18`）
  - 检查任务是否已在 `available_tasks` 注册（`main.py:43-54`）

### 已知问题和待优化项
- 日志改进：部分地方使用 `print`/f-string，建议统一到 `logging` 且采用参数化日志
- Docstring 与导入顺序：若引入代码规范工具（如 `pylint/ruff`），需按提示完善
- Vision/Controls 更强健抽象：可增加统一的点击重试、识别区域裁切与多尺度匹配
- 配置热更新：`config/manager.py` + `watch.py` 可扩展为运行时监听配置变更并动态生效
- 模板资源完整性：当前仓库模板为示例结构，需补全实际业务模板文件

> 最后修改人/时间：交付人（AI 助手），2025-11-16

---

## 附录

### 关键代码片段索引（文件:行号）
- 任务调度主循环：`main.py:72-107`
- 组件初始化与任务注册：`main.py:21-55`
- 统一任务基类与辅助：`tasks/basic_task.py:21-65`
- Controls 按键：`core/controls.py:113-121`
- Vision 等待模板：`core/vision.py:73-92`
- TestTask 任务示例：`tasks/test_task.py:17-45`

### 运行示例
```yaml
# 在 config.yaml 中启用所需任务
tasks:
  test_task: true
  login_task: true
  shop_task: false
  # ...

# 运行
# powershell
action: |
  python main.py
```

### 联系人与参考资料
- 交付人：AI 助手
- 项目位置：`d:\PYTHON\DoroBot`
- 参考资料：
  - OpenCV 模板匹配文档
  - pyautogui 官方文档（FAILSAFE 与按键/鼠标 API）
  - mss 屏幕截图库使用说明
  - YAML 配置（PyYAML）