"""
虾的养成计划 (Shrimp Growth Plan)

一个交互式OpenClaw学习Skill，通过游戏化任务引导用户从小白成长为顶级虾。

使用方法:
    from shrimp_growth import ShrimpGrowthSkill, start_skill
    
    # 创建Skill实例
    skill = ShrimpGrowthSkill(user_id="user_123", user_name="张三")
    
    # 开始
    response = skill.start_skill()
    
    # 获取当前任务
    task_info = skill.get_current_task()
    
    # 完成任务
    feedback = skill.complete_task()
    
    # 查看进度
    progress = skill.show_progress()

快捷函数:
    - start_skill(user_id, user_name) - 开始Skill
    - get_current_task(user_id) - 获取当前任务
    - complete_task(user_id, task_id) - 完成任务
    - check_achievements(user_id) - 检查成就
    - show_progress(user_id) - 展示进度
    - help_user(user_id, context) - 帮助引导

作者: OpenClaw Team
版本: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "OpenClaw Team"

# 导入主要类和函数
from .models import (
    UserProgress, Task, Stage, Achievement,
    StageId, TaskStatus, Difficulty, Rarity,
    LEVEL_TABLE, STAGES, TASKS, ACHIEVEMENTS
)

from .progress_manager import ProgressManager
from .task_scheduler import TaskScheduler, CompletionResult, TaskValidationResult
from .achievement_system import AchievementSystem, AchievementUnlockResult
from .exp_calculator import ExpCalculator, LevelUpReward

from .main import (
    ShrimpGrowthSkill,
    start_skill,
    get_current_task,
    complete_task,
    check_achievements,
    show_progress,
    help_user,
    switch_stage,
    show_achievements,
    reset_progress
)

from .templates import (
    # 模板函数
    format_task_guidance,
    format_completion_feedback,
    format_achievement_unlock,
    format_error_guidance,
    # 模板字符串
    TASK_GUIDANCE_TEMPLATE,
    TASK_COMPLETION_TEMPLATE,
    ACHIEVEMENT_UNLOCK_TEMPLATE,
    PROGRESS_DISPLAY_TEMPLATE,
    WELCOME_NEW_USER_TEMPLATE,
    HELP_MENU_TEMPLATE
)

__all__ = [
    # 主类
    "ShrimpGrowthSkill",
    
    # 数据模型
    "UserProgress",
    "Task",
    "Stage", 
    "Achievement",
    "StageId",
    "TaskStatus",
    "Difficulty",
    "Rarity",
    
    # 管理器
    "ProgressManager",
    "TaskScheduler",
    "AchievementSystem",
    "ExpCalculator",
    
    # 结果类
    "CompletionResult",
    "TaskValidationResult",
    "AchievementUnlockResult",
    "LevelUpReward",
    
    # 快捷函数
    "start_skill",
    "get_current_task",
    "complete_task",
    "check_achievements",
    "show_progress",
    "help_user",
    "switch_stage",
    "show_achievements",
    "reset_progress",
    
    # 模板函数
    "format_task_guidance",
    "format_completion_feedback",
    "format_achievement_unlock",
    "format_error_guidance",
    
    # 模板常量
    "TASK_GUIDANCE_TEMPLATE",
    "TASK_COMPLETION_TEMPLATE",
    "ACHIEVEMENT_UNLOCK_TEMPLATE",
    "PROGRESS_DISPLAY_TEMPLATE",
    "WELCOME_NEW_USER_TEMPLATE",
    "HELP_MENU_TEMPLATE",
    
    # 数据常量
    "LEVEL_TABLE",
    "STAGES",
    "TASKS",
    "ACHIEVEMENTS",
]
