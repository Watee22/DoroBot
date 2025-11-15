#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重构代码测试脚本
验证core和tasks目录中的新功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """测试核心模块导入和基础功能"""
    print("=== 测试核心模块 ===")
    
    try:
        from core import Controls, Screen, Vision, Automation
        print("✓ 核心模块导入成功")
        
        # 测试Controls类
        controls = Controls()
        print("✓ Controls类实例化成功")
        
        # 测试Screen类
        screen = Screen()
        print("✓ Screen类实例化成功")
        
        # 测试Vision类
        vision = Vision(screen)
        print("✓ Vision类实例化成功")
        
        # 测试Automation类
        automation = Automation()
        print("✓ Automation类实例化成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 核心模块测试失败: {e}")
        return False

def test_tasks_modules():
    """测试任务模块导入"""
    print("\n=== 测试任务模块 ===")
    
    try:
        from tasks import (
            Task, TestTask, LoginTask, ShopTask, ArenaTask,
            SimulationTask, TowerTask, InterceptionTask,
            RewardTask, EventTask, CleanupTask
        )
        print("✓ 任务模块导入成功")
        
        # 测试基础任务类
        print("✓ Task基类可用")
        print("✓ TestTask类可用")
        print("✓ LoginTask类可用")
        print("✓ ShopTask类可用")
        print("✓ ArenaTask类可用")
        print("✓ SimulationTask类可用")
        print("✓ TowerTask类可用")
        print("✓ InterceptionTask类可用")
        print("✓ RewardTask类可用")
        print("✓ EventTask类可用")
        print("✓ CleanupTask类可用")
        
        return True
        
    except Exception as e:
        print(f"✗ 任务模块测试失败: {e}")
        return False

def test_new_functionality():
    """测试新添加的功能"""
    print("\n=== 测试新功能 ===")
    
    try:
        from core import Screen, Vision, Controls
        
        # 初始化组件
        screen = Screen()
        vision = Vision(screen)
        controls = Controls()
        
        print("✓ 新功能组件初始化成功")
        
        # 测试Vision的新方法是否存在
        if hasattr(vision, 'wait_and_click') and hasattr(vision, 'wait_for_image'):
            print("✓ Vision新方法存在")
        else:
            print("✗ Vision新方法缺失")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ 新功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始重构代码测试...\n")
    
    tests_passed = 0
    tests_total = 3
    
    # 运行测试
    if test_core_modules():
        tests_passed += 1
    
    if test_tasks_modules():
        tests_passed += 1
    
    if test_new_functionality():
        tests_passed += 1
    
    # 输出测试结果
    print(f"\n=== 测试结果 ===")
    print(f"通过测试: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("🎉 所有测试通过！重构代码功能完整。")
        return True
    else:
        print("⚠️  部分测试失败，请检查代码。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)