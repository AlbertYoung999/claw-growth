"""
虾的养成计划 - 测试文件
用于验证核心功能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
    UserProgress, Task, Stage, Achievement,
    get_task_by_id, get_stage_by_id, get_achievement_by_id,
    get_level_config, get_next_level_exp, STAGES, TASKS, ACHIEVEMENTS,
    LEVEL_TABLE
)
from exp_calculator import ExpCalculator


def test_models():
    """测试数据模型"""
    print("=" * 50)
    print("测试数据模型")
    print("=" * 50)
    
    # 测试获取任务
    task = get_task_by_id("task1")
    assert task is not None, "task1 应该存在"
    assert task.name == "破冰对话", f"任务名称错误: {task.name}"
    print(f"✓ 任务获取: {task.name}")
    
    # 测试获取阶段
    stage = get_stage_by_id("stage1")
    assert stage is not None, "stage1 应该存在"
    assert stage.name == "孵化期", f"阶段名称错误: {stage.name}"
    print(f"✓ 阶段获取: {stage.name}")
    
    # 测试获取成就
    achievement = get_achievement_by_id("first_talk")
    assert achievement is not None, "first_talk 应该存在"
    assert achievement.name == "破壳而出", f"成就名称错误: {achievement.name}"
    print(f"✓ 成就获取: {achievement.name}")
    
    # 测试等级配置
    level_config = get_level_config(5)
    assert level_config is not None, "等级5 应该存在"
    assert level_config.min_exp == 700, f"经验值错误: {level_config.min_exp}"
    print(f"✓ 等级配置: Lv.{level_config.level} 需要 {level_config.min_exp} EXP")
    
    print("✓ 数据模型测试通过")


def test_exp_calculator():
    """测试经验值计算"""
    print("\n" + "=" * 50)
    print("测试经验值计算")
    print("=" * 50)
    
    calc = ExpCalculator()
    
    # 测试获取等级 (根据LEVEL_TABLE: Lv.3需要250 EXP，Lv.4需要450 EXP)
    level = calc.get_level(350)
    assert level == 3, f"等级计算错误: 350 EXP 应该是 Lv.3，实际是 Lv.{level}"
    print(f"✓ 等级计算: 350 EXP = Lv.{level}")
    
    # 测试等级进度 (Lv.3: 250-450, 350在中间)
    level, current_exp, next_exp, percentage = calc.get_level_progress(350)
    assert level == 3, f"等级错误: {level}"
    assert percentage == 50, f"进度错误: {percentage}% (期望50%)"
    print(f"✓ 等级进度: Lv.{level} ({current_exp}/{next_exp}, {percentage}%)")
    
    # 测试升级检测 (Lv.4需要450 EXP，从400升到500应该升到Lv.5，因为Lv.5需要700)
    # 修正：400->Lv.3, 500->Lv.3 (因为450才能到Lv.4)
    level_up, old_level, new_level = calc.check_level_up(420, 480)
    assert level_up == True, "应该升级"
    assert old_level == 3, f"旧等级错误: {old_level}"
    assert new_level == 4, f"新等级错误: {new_level}"
    print(f"✓ 升级检测: Lv.{old_level} -> Lv.{new_level}")
    
    # 测试任务经验计算
    exp = calc.calculate_task_exp("easy", is_first_time=True, streak_days=0)
    assert exp > 0, "经验值应该大于0"
    print(f"✓ 任务经验: 简单任务 = {exp} EXP")
    
    exp_hard = calc.calculate_task_exp("hard", is_first_time=True, streak_days=7)
    assert exp_hard > exp, "困难任务经验值应该更多"
    print(f"✓ 任务经验: 困难+7天连续 = {exp_hard} EXP")
    
    print("✓ 经验值计算测试通过")


def test_user_progress():
    """测试用户进度"""
    print("\n" + "=" * 50)
    print("测试用户进度")
    print("=" * 50)
    
    # 创建用户进度
    progress = UserProgress(
        user_id="test_user",
        user_name="测试用户",
        current_stage="stage1",
        current_task="task1",
        completed_tasks=[],
        achievements=[],
        exp=0,
        level=1
    )
    
    assert progress.user_id == "test_user"
    assert progress.level == 1
    print(f"✓ 创建用户: {progress.user_name}")
    
    # 测试转换为字典
    data = progress.to_dict()
    assert data["user_id"] == "test_user"
    print(f"✓ 字典转换: {len(data)} 个字段")
    
    # 测试从字典创建
    progress2 = UserProgress.from_dict(data)
    assert progress2.user_id == "test_user"
    assert progress2.user_name == "测试用户"
    print(f"✓ 从字典创建: {progress2.user_name}")
    
    # 模拟完成任务
    progress.completed_tasks.append("task1")
    progress.exp += 20
    print(f"✓ 完成任务: task1, EXP = {progress.exp}")
    
    print("✓ 用户进度测试通过")


def test_data_integrity():
    """测试数据完整性"""
    print("\n" + "=" * 50)
    print("测试数据完整性")
    print("=" * 50)
    
    # 检查阶段和任务的关联
    for stage in STAGES:
        for task_id in stage.tasks:
            task = get_task_by_id(task_id)
            assert task is not None, f"阶段 {stage.stage_id} 引用了不存在的任务 {task_id}"
            assert task.stage_id == stage.stage_id, f"任务 {task_id} 的阶段不匹配"
        print(f"✓ 阶段 {stage.name}: {len(stage.tasks)} 个任务")
    
    # 检查成就条件引用的任务/阶段存在
    for achievement in ACHIEVEMENTS:
        condition = achievement.condition
        if condition.get("type") == "task_complete":
            task_id = condition.get("task_id")
            assert get_task_by_id(task_id) is not None, f"成就 {achievement.achievement_id} 引用了不存在的任务 {task_id}"
        elif condition.get("type") == "stage_complete":
            stage_id = condition.get("stage_id")
            assert get_stage_by_id(stage_id) is not None, f"成就 {achievement.achievement_id} 引用了不存在的阶段 {stage_id}"
    
    print(f"✓ 检查了 {len(ACHIEVEMENTS)} 个成就")
    
    # 检查等级配置连续性
    for i, config in enumerate(LEVEL_TABLE):
        if i > 0:
            prev_config = LEVEL_TABLE[i - 1]
            assert config.min_exp > prev_config.min_exp, f"等级 {config.level} 的经验值应该大于前一等级"
    
    print(f"✓ 检查了 {len(LEVEL_TABLE)} 个等级配置")
    
    print("✓ 数据完整性测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("虾的养成计划 - 自动化测试")
    print("=" * 60)
    
    try:
        test_models()
        test_exp_calculator()
        test_user_progress()
        test_data_integrity()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
