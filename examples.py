"""
虾的养成计划 - 使用示例
展示如何使用各个功能模块
"""

from shrimp_growth import (
    ShrimpGrowthSkill,
    start_skill,
    get_current_task,
    complete_task,
    show_progress,
    help_user,
    ProgressManager,
    TaskScheduler,
    AchievementSystem,
    ExpCalculator
)


def example_basic_usage():
    """基础使用示例"""
    
    # 方法1：使用快捷函数
    user_id = "user_123"
    
    # 开始Skill
    welcome = start_skill(user_id, user_name="小明")
    print(welcome)
    
    # 获取当前任务
    current_task = get_current_task(user_id)
    print(current_task)
    
    # 完成任务
    feedback = complete_task(user_id)
    print(feedback)
    
    # 查看进度
    progress = show_progress(user_id)
    print(progress)


def example_advanced_usage():
    """高级使用示例"""
    
    # 方法2：使用Skill类
    skill = ShrimpGrowthSkill(user_id="user_456", user_name="小红")
    
    # 开始
    response = skill.start_skill()
    print(response)
    
    # 获取帮助
    help_text = skill.help_user(context="不知道如何创建文件")
    print(help_text)
    
    # 完成任务（指定任务ID）
    feedback = skill.complete_task(task_id="task2")
    print(feedback)
    
    # 切换阶段
    result = skill.switch_stage(stage_id="stage2")
    print(result)
    
    # 查看成就
    achievements = skill.show_achievements()
    print(achievements)


def example_module_usage():
    """模块级使用示例"""
    
    user_id = "user_789"
    
    # 进度管理
    pm = ProgressManager(user_id)
    progress = pm.get_or_create_progress("张三")
    print(f"用户等级：Lv.{progress.level}")
    
    # 更新连续学习天数
    streak = pm.check_and_update_streak()
    print(f"连续学习：{streak}天")
    
    # 任务调度
    ts = TaskScheduler(user_id, pm)
    task = ts.get_current_task()
    print(f"当前任务：{task.name if task else '无'}")
    
    # 成就系统
    ach = AchievementSystem(user_id, pm)
    new_achievements = ach.check_all_achievements()
    print(f"新成就：{len(new_achievements)}个")
    
    # 经验值计算
    calc = ExpCalculator()
    exp_info = calc.get_exp_breakdown(progress.exp)
    print(f"当前等级：{exp_info['level']}")
    print(f"升级进度：{exp_info['progress_bar']}")


def example_custom_task_completion():
    """自定义任务完成流程示例"""
    
    user_id = "user_custom"
    skill = ShrimpGrowthSkill(user_id, "测试用户")
    
    # 1. 获取当前任务
    task_info = skill.get_current_task()
    print("=" * 50)
    print(task_info)
    
    # 2. 模拟用户操作...
    # （这里可以插入实际的任务验证逻辑）
    
    # 3. 完成任务
    result = skill.complete_task()
    print("=" * 50)
    print(result)
    
    # 4. 检查成就
    achievement_result = skill.check_achievements()
    print("=" * 50)
    print(achievement_result)
    
    # 5. 显示更新后的进度
    progress = skill.show_progress()
    print("=" * 50)
    print(progress)


def example_progress_management():
    """进度管理示例"""
    
    user_id = "user_progress_test"
    pm = ProgressManager(user_id)
    
    # 初始化新用户
    progress = pm.init_new_user("测试用户")
    print(f"新用户创建：{progress.user_name}")
    
    # 检查是否是新用户
    is_new = pm.is_new_user(progress)
    print(f"是否新用户：{is_new}")
    
    # 获取进度摘要
    summary = pm.get_progress_summary()
    print(f"进度摘要：{summary}")
    
    # 导出进度
    exported = pm.export_progress()
    print(f"导出数据：{exported[:100]}...")
    
    # 更新统计
    pm.update_stats("tasks_completed", 1)
    pm.update_stats("help_requested")


def example_achievement_management():
    """成就管理示例"""
    
    user_id = "user_achievement_test"
    pm = ProgressManager(user_id)
    pm.init_new_user("成就测试用户")
    
    ach = AchievementSystem(user_id, pm)
    
    # 检查所有可解锁成就
    unlockable = ach.check_all_achievements()
    print(f"可解锁成就：{[a.name for a in unlockable]}")
    
    # 检查特定成就
    can_unlock = ach.check_achievement("first_talk")
    print(f"能否解锁 first_talk：{can_unlock}")
    
    # 获取用户成就列表（包含未解锁的）
    all_achievements = ach.get_user_achievements(include_locked=True)
    print(f"总成就数：{len(all_achievements)}")
    
    # 获取成就统计
    stats = ach.get_achievement_stats()
    print(f"成就统计：{stats}")
    
    # 获取即将解锁的成就提示
    hints = ach.get_next_achievements_hint()
    print(f"即将解锁：{hints}")


def example_exp_calculation():
    """经验值计算示例"""
    
    calc = ExpCalculator()
    
    # 计算任务经验值
    exp1 = calc.calculate_task_exp("easy", is_first_time=True, streak_days=0)
    print(f"简单任务经验：{exp1}")
    
    exp2 = calc.calculate_task_exp("hard", is_first_time=True, streak_days=7)
    print(f"困难任务+7天连续：{exp2}")
    
    # 获取等级信息
    level = calc.get_level(350)
    print(f"350经验 = Lv.{level}")
    
    # 获取等级进度
    current_level, current_exp, next_exp, percentage = calc.get_level_progress(350)
    print(f"Lv.{current_level}: {current_exp}/{next_exp} ({percentage}%)")
    
    # 检查升级
    level_up, old_lvl, new_lvl = calc.check_level_up(280, 350)
    print(f"升级：{level_up} ({old_lvl} -> {new_lvl})")
    
    # 获取经验值详情
    exp_info = calc.get_exp_breakdown(350)
    print(f"经验详情：{exp_info}")
    
    # 模拟经验获取
    preview = calc.simulate_exp_gain(280, 100)
    print(f"升级预览：{preview}")


if __name__ == "__main__":
    print("=" * 60)
    print("虾的养成计划 - 使用示例")
    print("=" * 60)
    
    # 运行示例（选择要运行的示例取消注释）
    
    # example_basic_usage()
    # example_advanced_usage()
    # example_module_usage()
    # example_custom_task_completion()
    # example_progress_management()
    # example_achievement_management()
    # example_exp_calculation()
    
    print("\n请取消注释要运行的示例函数")
