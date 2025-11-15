#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务模块包
包含所有自动化任务类
"""

from tasks.basic_task import Task
from tasks.test_task import TestTask
from tasks.login_task import LoginTask
from tasks.shop_task import ShopTask
from tasks.arena_task import ArenaTask
from tasks.simulation_task import SimulationTask
from tasks.tower_task import TowerTask
from tasks.interception_task import InterceptionTask
from tasks.reward_task import RewardTask
from tasks.event_task import EventTask
from tasks.cleanup_task import CleanupTask

__all__ = [
    'Task',
    'TestTask', 
    'LoginTask',
    'ShopTask',
    'ArenaTask',
    'SimulationTask',
    'TowerTask',
    'InterceptionTask',
    'RewardTask',
    'EventTask',
    'CleanupTask'
]