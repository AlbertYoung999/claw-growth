"""
虾的养成计划 - 经验值计算模块
负责经验值计算、等级管理和升级检测
"""

from typing import Tuple, Optional, Dict, Any
from models import LEVEL_TABLE, get_level_config, get_next_level_exp, UserProgress


class ExpCalculator:
    """
    经验值计算器
    
    负责：
    - 计算任务完成获得的经验值
    - 根据经验值计算等级
    - 检查是否升级
    - 计算等级进度百分比
    """
    
    # 经验值加成系数
    BONUS_MULTIPLIERS = {
        "first_completion": 1.0,     # 首次完成
        "difficulty_easy": 1.0,      # 简单难度
        "difficulty_medium": 1.2,    # 中等难度
        "difficulty_hard": 1.5,      # 困难难度
        "difficulty_expert": 2.0,    # 专家难度
        "streak_bonus": 0.1,         # 每连续一天加成10%
        "max_streak_bonus": 0.5      # 最大连续加成50%
    }
    
    # 基础经验值表
    BASE_EXP = {
        "task_complete": 20,         # 完成任务基础经验
        "stage_complete": 100,       # 完成阶段基础经验
        "achievement_unlock": 10,    # 解锁成就基础经验
        "daily_login": 5,            # 每日登录
        "help_others": 15            # 帮助他人
    }
    
    def __init__(self):
        """初始化经验值计算器"""
        pass
    
    def calculate_task_exp(self, task_difficulty: str, is_first_time: bool = True,
                          streak_days: int = 0, base_exp: int = None) -> int:
        """
        计算任务完成获得的经验值
        
        Args:
            task_difficulty: 任务难度 (easy/medium/hard/expert)
            is_first_time: 是否首次完成
            streak_days: 连续学习天数
            base_exp: 基础经验值，None使用默认值
            
        Returns:
            获得的经验值
        """
        # 基础经验
        if base_exp is None:
            base_exp = self.BASE_EXP["task_complete"]
        
        # 难度加成
        difficulty_multipliers = {
            "easy": self.BONUS_MULTIPLIERS["difficulty_easy"],
            "medium": self.BONUS_MULTIPLIERS["difficulty_medium"],
            "hard": self.BONUS_MULTIPLIERS["difficulty_hard"],
            "expert": self.BONUS_MULTIPLIERS["difficulty_expert"]
        }
        multiplier = difficulty_multipliers.get(task_difficulty, 1.0)
        
        # 连续学习加成
        streak_bonus = min(
            streak_days * self.BONUS_MULTIPLIERS["streak_bonus"],
            self.BONUS_MULTIPLIERS["max_streak_bonus"]
        )
        multiplier += streak_bonus
        
        # 计算最终经验值
        exp = int(base_exp * multiplier)
        
        return exp
    
    def calculate_stage_complete_exp(self, stage_id: str, tasks_count: int) -> int:
        """
        计算阶段完成奖励经验值
        
        Args:
            stage_id: 阶段ID
            tasks_count: 任务数量
            
        Returns:
            奖励经验值
        """
        base = self.BASE_EXP["stage_complete"]
        
        # 阶段加成（越后期奖励越高）
        stage_multipliers = {
            "stage1": 1.0,
            "stage2": 1.5,
            "stage3": 2.0,
            "stage4": 2.5,
            "stage5": 3.0
        }
        multiplier = stage_multipliers.get(stage_id, 1.0)
        
        # 任务数量加成
        task_bonus = tasks_count * 5
        
        return int(base * multiplier) + task_bonus
    
    def calculate_achievement_exp(self, rarity: str) -> int:
        """
        计算成就解锁经验值
        
        Args:
            rarity: 成就稀有度
            
        Returns:
            经验值
        """
        base = self.BASE_EXP["achievement_unlock"]
        
        rarity_multipliers = {
            "common": 1.0,
            "rare": 2.0,
            "epic": 5.0,
            "legendary": 10.0,
            "secret": 15.0
        }
        
        multiplier = rarity_multipliers.get(rarity, 1.0)
        return int(base * multiplier)
    
    def get_level(self, exp: int) -> int:
        """
        根据经验值计算等级
        
        Args:
            exp: 经验值
            
        Returns:
            等级
        """
        for config in reversed(LEVEL_TABLE):
            if exp >= config.min_exp:
                return config.level
        return 1
    
    def get_level_progress(self, exp: int) -> Tuple[int, int, int, int]:
        """
        获取当前等级进度
        
        Args:
            exp: 经验值
            
        Returns:
            (当前等级, 当前等级经验, 下一级所需经验, 进度百分比)
        """
        current_level = self.get_level(exp)
        current_config = get_level_config(current_level)
        next_exp = get_next_level_exp(current_level)
        
        current_level_exp = exp - current_config.min_exp
        exp_to_next = next_exp - current_config.min_exp
        percentage = int((current_level_exp / exp_to_next) * 100) if exp_to_next > 0 else 100
        
        return current_level, current_level_exp, exp_to_next, percentage
    
    def check_level_up(self, old_exp: int, new_exp: int) -> Tuple[bool, int, int]:
        """
        检查是否升级
        
        Args:
            old_exp: 原经验值
            new_exp: 新经验值
            
        Returns:
            (是否升级, 原等级, 新等级)
        """
        old_level = self.get_level(old_exp)
        new_level = self.get_level(new_exp)
        
        level_up = new_level > old_level
        return level_up, old_level, new_level
    
    def get_title_by_level(self, level: int) -> str:
        """
        根据等级获取称号
        
        Args:
            level: 等级
            
        Returns:
            称号
        """
        config = get_level_config(level)
        if config:
            return f"{config.title_emoji} {config.title}"
        return "🦐 虾苗"
    
    def get_exp_breakdown(self, exp: int) -> Dict[str, Any]:
        """
        获取经验值详情
        
        Args:
            exp: 经验值
            
        Returns:
            经验值详情字典
        """
        level, current_exp, next_exp, percentage = self.get_level_progress(exp)
        title = self.get_title_by_level(level)
        next_level_title = self.get_title_by_level(min(level + 1, 10))
        
        return {
            "total_exp": exp,
            "level": level,
            "title": title,
            "current_level_exp": current_exp,
            "exp_to_next": next_exp,
            "next_level": min(level + 1, 10),
            "next_level_title": next_level_title,
            "progress_percentage": percentage,
            "progress_bar": self._render_progress_bar(percentage)
        }
    
    def _render_progress_bar(self, percentage: int, width: int = 20) -> str:
        """
        渲染进度条
        
        Args:
            percentage: 进度百分比
            width: 进度条宽度
            
        Returns:
            进度条字符串
        """
        filled = int(width * percentage / 100)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {percentage}%"
    
    def simulate_exp_gain(self, current_exp: int, gain: int) -> Dict[str, Any]:
        """
        模拟经验值获取，返回升级预览
        
        Args:
            current_exp: 当前经验值
            gain: 将获得的经验值
            
        Returns:
            升级预览信息
        """
        new_exp = current_exp + gain
        level_up, old_level, new_level = self.check_level_up(current_exp, new_exp)
        
        result = {
            "current_exp": current_exp,
            "gain": gain,
            "new_exp": new_exp,
            "level_up": level_up,
            "old_level": old_level,
            "new_level": new_level,
            "old_title": self.get_title_by_level(old_level),
            "new_title": self.get_title_by_level(new_level) if level_up else None
        }
        
        # 如果升级，计算连升几级
        if level_up:
            levels_gained = new_level - old_level
            result["levels_gained"] = levels_gained
            
            # 获取升级奖励
            rewards = []
            for lvl in range(old_level + 1, new_level + 1):
                lvl_config = get_level_config(lvl)
                if lvl_config:
                    rewards.append({
                        "level": lvl,
                        "title": f"{lvl_config.title_emoji} {lvl_config.title}"
                    })
            result["rewards"] = rewards
        
        return result
    
    def calculate_total_exp_for_level(self, target_level: int) -> int:
        """
        计算达到目标等级所需总经验值
        
        Args:
            target_level: 目标等级
            
        Returns:
            所需经验值
        """
        config = get_level_config(target_level)
        return config.min_exp if config else 0
    
    def estimate_remaining_tasks(self, current_exp: int, avg_task_exp: int = 50) -> Dict[str, Any]:
        """
        估算剩余任务数量
        
        Args:
            current_exp: 当前经验值
            avg_task_exp: 平均任务经验值
            
        Returns:
            估算信息
        """
        level = self.get_level(current_exp)
        
        if level >= 10:
            return {"max_level_reached": True}
        
        # 计算到下一级所需任务数
        _, _, exp_to_next, _ = self.get_level_progress(current_exp)
        tasks_to_next = (exp_to_next // avg_task_exp) + (1 if exp_to_next % avg_task_exp > 0 else 0)
        
        # 计算到满级所需任务数
        max_exp = LEVEL_TABLE[-1].min_exp
        exp_to_max = max_exp - current_exp
        tasks_to_max = (exp_to_max // avg_task_exp) + (1 if exp_to_max % avg_task_exp > 0 else 0)
        
        return {
            "current_level": level,
            "tasks_to_next_level": tasks_to_next,
            "tasks_to_max_level": tasks_to_max,
            "avg_task_exp": avg_task_exp
        }


class LevelUpReward:
    """等级提升奖励"""
    
    # 每级奖励
    REWARDS = {
        2: {"title": "初级虾仔", "ability": "基础文件操作"},
        3: {"title": "见习工兵", "ability": "批量文件处理"},
        4: {"title": "勤劳工兵", "ability": "定时任务设置"},
        5: {"title": "认证建筑师", "ability": "Skill开发权限"},
        6: {"title": "资深建筑师", "ability": "API集成能力"},
        7: {"title": "系统架构师", "ability": "多Agent编排"},
        8: {"title": "高级架构师", "ability": "工作流设计"},
        9: {"title": "准顶级虾", "ability": "云部署能力"},
        10: {"title": "顶级虾", "ability": "导师资格认证"}
    }
    
    @classmethod
    def get_reward(cls, level: int) -> Dict[str, str]:
        """获取等级奖励"""
        return cls.REWARDS.get(level, {"title": "", "ability": ""})
    
    @classmethod
    def render_level_up_message(cls, old_level: int, new_level: int) -> str:
        """
        渲染升级消息
        
        Args:
            old_level: 原等级
            new_level: 新等级
            
        Returns:
            升级消息
        """
        old_config = get_level_config(old_level)
        new_config = get_level_config(new_level)
        reward = cls.get_reward(new_level)
        
        message = f"""
🎉 恭喜升级！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lv.{old_level} {old_config.title_emoji} {old_config.title}
        ↓
Lv.{new_level} {new_config.title_emoji} {new_config.title}

🎁 解锁新能力：{reward.get('ability', '暂无')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return message
