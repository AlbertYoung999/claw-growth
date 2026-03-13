"""
虾的养成计划 - 成就系统模块
负责成就检查、解锁和展示
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from models import (
    UserProgress, Achievement, Stage, Task,
    ACHIEVEMENTS, get_achievement_by_id, get_stage_by_id,
    get_task_by_id, Rarity
)
from progress_manager import ProgressManager


class AchievementUnlockResult:
    """成就解锁结果"""
    def __init__(self, success: bool, achievement: Achievement = None, 
                 already_unlocked: bool = False, reward_exp: int = 0):
        self.success = success
        self.achievement = achievement
        self.already_unlocked = already_unlocked
        self.reward_exp = reward_exp


class AchievementSystem:
    """
    成就系统
    
    负责：
    - 成就条件检查
    - 成就解锁
    - 成就展示
    - 隐藏成就管理
    """
    
    # 稀有度权重（用于排序和展示）
    RARITY_WEIGHTS = {
        "common": 1,
        "rare": 2,
        "epic": 3,
        "legendary": 4,
        "secret": 5
    }
    
    # 稀有度显示名称
    RARITY_NAMES = {
        "common": "普通",
        "rare": "稀有",
        "epic": "史诗",
        "legendary": "传说",
        "secret": "隐藏"
    }
    
    def __init__(self, user_id: str, progress_manager: ProgressManager = None):
        """
        初始化成就系统
        
        Args:
            user_id: 用户ID
            progress_manager: 进度管理器实例
        """
        self.user_id = user_id
        self.progress_manager = progress_manager or ProgressManager(user_id)
    
    def check_all_achievements(self) -> List[Achievement]:
        """
        检查所有可解锁的成就
        
        Returns:
            新解锁的成就列表
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return []
        
        newly_unlocked = []
        
        for achievement in ACHIEVEMENTS:
            if achievement.achievement_id not in progress.achievements:
                if self._check_condition(achievement.condition, progress):
                    newly_unlocked.append(achievement)
        
        return newly_unlocked
    
    def check_achievement(self, achievement_id: str) -> bool:
        """
        检查特定成就是否满足条件
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            是否满足条件
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return False
        
        achievement = get_achievement_by_id(achievement_id)
        if not achievement:
            return False
        
        # 检查是否已解锁
        if achievement_id in progress.achievements:
            return True
        
        return self._check_condition(achievement.condition, progress)
    
    def unlock_achievement(self, achievement_id: str) -> AchievementUnlockResult:
        """
        解锁成就
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            解锁结果
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return AchievementUnlockResult(False)
        
        achievement = get_achievement_by_id(achievement_id)
        if not achievement:
            return AchievementUnlockResult(False)
        
        # 检查是否已解锁
        if achievement_id in progress.achievements:
            return AchievementUnlockResult(
                success=False, 
                achievement=achievement,
                already_unlocked=True
            )
        
        # 检查条件
        if not self._check_condition(achievement.condition, progress):
            return AchievementUnlockResult(False)
        
        # 解锁成就
        progress.achievements.append(achievement_id)
        
        # 保存进度
        self.progress_manager.save_progress(progress)
        
        # 计算奖励经验值
        reward_exp = achievement.reward_exp
        
        return AchievementUnlockResult(
            success=True,
            achievement=achievement,
            reward_exp=reward_exp
        )
    
    def unlock_achievements_batch(self, achievement_ids: List[str]) -> List[AchievementUnlockResult]:
        """
        批量解锁成就
        
        Args:
            achievement_ids: 成就ID列表
            
        Returns:
            解锁结果列表
        """
        results = []
        total_exp = 0
        
        for achievement_id in achievement_ids:
            result = self.unlock_achievement(achievement_id)
            if result.success:
                total_exp += result.reward_exp
            results.append(result)
        
        return results
    
    def get_user_achievements(self, include_locked: bool = False) -> List[Dict[str, Any]]:
        """
        获取用户的成就列表
        
        Args:
            include_locked: 是否包含未解锁的成就
            
        Returns:
            成就详情列表
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return []
        
        results = []
        
        for achievement in ACHIEVEMENTS:
            is_unlocked = achievement.achievement_id in progress.achievements
            
            if not is_unlocked and not include_locked:
                continue
            
            # 隐藏成就处理
            display_name = achievement.name
            display_description = achievement.description
            display_emoji = achievement.emoji
            
            if achievement.secret and not is_unlocked:
                display_name = "???"
                display_description = achievement.hidden_hint or "这是一个隐藏成就"
                display_emoji = "❓"
            
            results.append({
                "achievement_id": achievement.achievement_id,
                "name": display_name,
                "description": display_description,
                "emoji": display_emoji,
                "rarity": achievement.rarity,
                "rarity_name": self.RARITY_NAMES.get(achievement.rarity, "普通"),
                "unlocked": is_unlocked,
                "secret": achievement.secret,
                "reward_exp": achievement.reward_exp if is_unlocked else "?",
                "unlocked_at": self._get_unlock_time(progress, achievement.achievement_id) if is_unlocked else None
            })
        
        # 按稀有度排序（已解锁的在前面）
        results.sort(key=lambda x: (
            not x["unlocked"],  # 未解锁的排在后面
            -self.RARITY_WEIGHTS.get(x["rarity"], 0)  # 稀有度高的在前面
        ))
        
        return results
    
    def get_achievement_stats(self) -> Dict[str, Any]:
        """
        获取成就统计
        
        Returns:
            成就统计信息
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return {}
        
        unlocked = len(progress.achievements)
        total = len(ACHIEVEMENTS)
        
        # 按稀有度统计
        rarity_stats = {}
        for rarity in self.RARITY_NAMES.keys():
            rarity_achievements = [a for a in ACHIEVEMENTS if a.rarity == rarity]
            unlocked_in_rarity = sum(
                1 for a in rarity_achievements 
                if a.achievement_id in progress.achievements
            )
            rarity_stats[rarity] = {
                "unlocked": unlocked_in_rarity,
                "total": len(rarity_achievements),
                "name": self.RARITY_NAMES[rarity]
            }
        
        # 隐藏成就统计
        secret_achievements = [a for a in ACHIEVEMENTS if a.secret]
        unlocked_secrets = sum(
            1 for a in secret_achievements 
            if a.achievement_id in progress.achievements
        )
        
        return {
            "total_unlocked": unlocked,
            "total_achievements": total,
            "completion_percentage": round(unlocked / total * 100, 1),
            "by_rarity": rarity_stats,
            "secret_achievements": {
                "unlocked": unlocked_secrets,
                "total": len(secret_achievements)
            }
        }
    
    def _check_condition(self, condition: Dict, progress: UserProgress) -> bool:
        """
        检查成就是否满足条件
        
        Args:
            condition: 条件字典
            progress: 用户进度
            
        Returns:
            是否满足条件
        """
        condition_type = condition.get("type", "")
        
        condition_checkers = {
            "task_complete": self._check_task_complete,
            "stage_complete": self._check_stage_complete,
            "streak_days": self._check_streak_days,
            "all_achievements": self._check_all_achievements,
            "speed_run": self._check_speed_run,
            "exp_threshold": self._check_exp_threshold,
            "level_reached": self._check_level_reached
        }
        
        checker = condition_checkers.get(condition_type)
        if checker:
            return checker(condition, progress)
        
        return False
    
    def _check_task_complete(self, condition: Dict, progress: UserProgress) -> bool:
        """检查任务是否完成"""
        task_id = condition.get("task_id", "")
        return task_id in progress.completed_tasks
    
    def _check_stage_complete(self, condition: Dict, progress: UserProgress) -> bool:
        """检查阶段是否完成"""
        stage_id = condition.get("stage_id", "")
        stage = get_stage_by_id(stage_id)
        
        if not stage:
            return False
        
        # 检查阶段所有任务是否完成
        for task_id in stage.tasks:
            if (task_id not in progress.completed_tasks and 
                task_id not in progress.skipped_tasks):
                return False
        
        return True
    
    def _check_streak_days(self, condition: Dict, progress: UserProgress) -> bool:
        """检查连续学习天数"""
        required_days = condition.get("days", 0)
        return progress.streak_days >= required_days
    
    def _check_all_achievements(self, condition: Dict, progress: UserProgress) -> bool:
        """检查是否获得所有成就（不包括隐藏成就）"""
        non_secret = [a for a in ACHIEVEMENTS if not a.secret]
        return all(a.achievement_id in progress.achievements for a in non_secret)
    
    def _check_speed_run(self, condition: Dict, progress: UserProgress) -> bool:
        """检查是否速通"""
        required_days = condition.get("days", 7)
        
        # 解析创建时间
        created = datetime.fromisoformat(progress.created_at)
        now = datetime.now()
        days_elapsed = (now - created).days
        
        if days_elapsed > required_days:
            return False
        
        # 检查是否完成所有阶段
        all_stages = ["stage1", "stage2", "stage3", "stage4", "stage5"]
        for stage_id in all_stages:
            stage = get_stage_by_id(stage_id)
            if stage:
                for task_id in stage.tasks:
                    if (task_id not in progress.completed_tasks and 
                        task_id not in progress.skipped_tasks):
                        return False
        
        return True
    
    def _check_exp_threshold(self, condition: Dict, progress: UserProgress) -> bool:
        """检查经验值是否达到阈值"""
        threshold = condition.get("threshold", 0)
        return progress.exp >= threshold
    
    def _check_level_reached(self, condition: Dict, progress: UserProgress) -> bool:
        """检查是否达到指定等级"""
        required_level = condition.get("level", 1)
        return progress.level >= required_level
    
    def _get_unlock_time(self, progress: UserProgress, achievement_id: str) -> Optional[str]:
        """
        获取成就解锁时间
        
        注意：当前实现中我们没有存储每个成就的解锁时间，
        这里返回最后活跃时间作为近似值
        
        Args:
            progress: 用户进度
            achievement_id: 成就ID
            
        Returns:
            解锁时间字符串
        """
        # 实际实现中应该在unlock时记录时间
        # 这里简化处理
        return progress.last_active
    
    def get_next_achievements_hint(self) -> List[Dict[str, Any]]:
        """
        获取即将解锁的成就提示
        
        Returns:
            即将解锁的成就列表
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return []
        
        hints = []
        
        for achievement in ACHIEVEMENTS:
            if achievement.achievement_id in progress.achievements:
                continue
            
            if achievement.secret:
                continue
            
            # 检查是否接近解锁
            condition = achievement.condition
            condition_type = condition.get("type", "")
            
            close_to_unlock = False
            progress_info = ""
            
            if condition_type == "task_complete":
                task_id = condition.get("task_id", "")
                if task_id == progress.current_task:
                    close_to_unlock = True
                    progress_info = "即将完成当前任务"
            
            elif condition_type == "stage_complete":
                stage_id = condition.get("stage_id", "")
                stage = get_stage_by_id(stage_id)
                if stage:
                    completed = sum(
                        1 for t in stage.tasks 
                        if t in progress.completed_tasks
                    )
                    total = len(stage.tasks)
                    if completed >= total - 1:
                        close_to_unlock = True
                        progress_info = f"{completed}/{total} 任务完成"
            
            elif condition_type == "streak_days":
                required = condition.get("days", 0)
                if progress.streak_days >= required - 1:
                    close_to_unlock = True
                    progress_info = f"已连续 {progress.streak_days} 天"
            
            if close_to_unlock:
                hints.append({
                    "name": achievement.name,
                    "emoji": achievement.emoji,
                    "description": achievement.description,
                    "rarity": achievement.rarity,
                    "progress_info": progress_info
                })
        
        return hints
    
    def render_achievement_unlocked(self, achievement_id: str) -> str:
        """
        渲染成就解锁提示词
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            渲染后的文本
        """
        achievement = get_achievement_by_id(achievement_id)
        if not achievement:
            return ""
        
        rarity_display = self.RARITY_NAMES.get(achievement.rarity, "普通")
        rarity_decorator = {
            "common": "",
            "rare": "✨ ",
            "epic": "🌟 ",
            "legendary": "💫 ",
            "secret": "🔮 "
        }.get(achievement.rarity, "")
        
        template = f"""
🏆 成就解锁！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    {achievement.emoji}
  【{achievement.name}】

{achievement.description}

稀有度：{rarity_decorator}{rarity_display}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if achievement.secret:
            template += "\n✨ 这是一个隐藏成就！\n"
        
        return template
