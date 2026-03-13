"""
虾的养成计划 - 主入口模块
整合所有功能模块，提供统一的API接口
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

# 导入所有模块
from models import (
    UserProgress, Task, Stage, Achievement,
    get_task_by_id, get_stage_by_id, get_achievement_by_id,
    STAGES, ACHIEVEMENTS
)
from progress_manager import ProgressManager
from task_scheduler import TaskScheduler, CompletionResult
from achievement_system import AchievementSystem, AchievementUnlockResult
from exp_calculator import ExpCalculator, LevelUpReward


class ShrimpGrowthSkill:
    """
    虾的养成计划 Skill主类
    
    整合所有模块，提供统一的API
    """
    
    def __init__(self, user_id: str, user_name: str = "虾友"):
        """
        初始化Skill
        
        Args:
            user_id: 用户ID
            user_name: 用户名
        """
        self.user_id = user_id
        self.user_name = user_name
        
        # 初始化所有模块
        self.progress_manager = ProgressManager(user_id)
        self.task_scheduler = TaskScheduler(user_id, self.progress_manager)
        self.achievement_system = AchievementSystem(user_id, self.progress_manager)
        self.exp_calculator = ExpCalculator()
    
    # ==================== 主入口函数 ====================
    
    def start_skill(self) -> str:
        """
        Skill主入口
        
        根据用户状态返回相应的欢迎界面或任务界面
        
        Returns:
            欢迎或主界面文本
        """
        progress = self.progress_manager.get_or_create_progress(self.user_name)
        
        if self.progress_manager.is_new_user(progress):
            return self._render_welcome_screen()
        else:
            return self._render_main_dashboard()
    
    def get_current_task(self) -> str:
        """
        获取当前任务详情
        
        Returns:
            当前任务引导文本
        """
        task = self.task_scheduler.get_current_task()
        progress = self.progress_manager.get_progress()
        
        if not task:
            return "任务加载失败，请尝试重新开始。"
        
        # 获取阶段信息
        stage = get_stage_by_id(task.stage_id)
        
        # 构建提示词
        template = f"""
🎯 当前任务：{task.name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【{stage.name if stage else '未知'}】{stage.emoji if stage else ''}

{task.description}

📋 任务指引：
{task.instructions}

💡 小提示：
{self._format_hints(task.hints)}

⏱️ 预计用时：{task.estimated_time} | 难度：{self._render_difficulty(task.difficulty)}

[开始任务] {"[查看示例]" if task.example else ""} {"[跳过此任务]" if task.can_skip else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return template.strip()
    
    def complete_task(self, task_id: str = None) -> str:
        """
        完成任务并返回反馈
        
        Args:
            task_id: 任务ID，None表示当前任务
            
        Returns:
            完成反馈文本
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return "请先开始学习。"
        
        # 确定任务
        if not task_id:
            task_id = progress.current_task
        
        task = get_task_by_id(task_id)
        if not task:
            return "任务不存在。"
        
        # 完成任务
        result = self.task_scheduler.complete_task(task_id)
        
        if not result.success:
            return f"❌ 任务完成失败：{result.message}"
        
        # 刷新进度
        progress = self.progress_manager.get_progress()
        
        # 检查升级
        old_level = progress.level
        new_level = self.exp_calculator.get_level(progress.exp)
        level_up = new_level > old_level
        
        if level_up:
            progress.level = new_level
            self.progress_manager.save_progress(progress)
        
        # 检查成就
        new_achievements = self.achievement_system.check_all_achievements()
        for ach in new_achievements:
            self.achievement_system.unlock_achievement(ach.achievement_id)
            # 成就也给经验
            progress.exp += ach.reward_exp
        
        if new_achievements:
            self.progress_manager.save_progress(progress)
        
        # 检查阶段完成
        stage_complete = result.stage_completed
        
        # 渲染反馈
        return self._render_completion_feedback(
            task=task,
            exp_gained=result.exp_gained,
            level_up=level_up,
            old_level=old_level,
            new_level=new_level,
            new_achievements=new_achievements,
            stage_complete=stage_complete,
            next_task_id=result.next_task_id
        )
    
    def check_achievements(self) -> str:
        """
        检查成就并返回结果
        
        Returns:
            成就检查反馈文本
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return "请先开始学习。"
        
        new_achievements = self.achievement_system.check_all_achievements()
        
        if not new_achievements:
            return "暂无可解锁的成就，继续加油！💪"
        
        # 解锁成就
        unlocked = []
        total_exp = 0
        
        for achievement in new_achievements:
            result = self.achievement_system.unlock_achievement(achievement.achievement_id)
            if result.success:
                unlocked.append(achievement)
                total_exp += result.reward_exp
                # 成就经验
                progress.exp += result.reward_exp
        
        if unlocked:
            self.progress_manager.save_progress(progress)
        
        # 渲染成就解锁
        messages = []
        for achievement in unlocked:
            msg = self.achievement_system.render_achievement_unlocked(achievement.achievement_id)
            messages.append(msg)
        
        result_text = "\n\n".join(messages)
        
        if total_exp > 0:
            result_text += f"\n\n📈 成就奖励经验值：+{total_exp}"
        
        return result_text
    
    def show_progress(self) -> str:
        """
        展示用户进度
        
        Returns:
            进度展示文本
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return "请先开始学习。"
        
        # 获取经验值详情
        exp_info = self.exp_calculator.get_exp_breakdown(progress.exp)
        
        # 获取阶段进度
        stage_progress = []
        for stage in STAGES:
            sp = self.task_scheduler.get_stage_progress(stage.stage_id)
            stage_progress.append(sp)
        
        # 获取成就统计
        achievement_stats = self.achievement_system.get_achievement_stats()
        
        # 渲染进度展示
        template = f"""
🦐 {progress.user_name} 的成长进度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{exp_info['title']} | Lv.{exp_info['level']} | EXP {exp_info['total_exp']}
{exp_info['progress_bar']}
🔥 连续学习 {progress.streak_days} 天 | 总共学习 {progress.total_days} 天

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
阶段进度：
"""
        
        for sp in stage_progress:
            status_icon = "✓" if sp['is_completed'] else "→" if sp['is_current'] else "🔒"
            bar = self._render_mini_progress_bar(sp['percentage'])
            template += f"\n{sp['emoji']} {sp['name']} {status_icon}\n  {bar} {sp['percentage']}%"
        
        template += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 已获得 {achievement_stats['total_unlocked']}/{achievement_stats['total_achievements']} 个成就
📊 总进度 {sp['overall_percentage'] if stage_progress else 0}%

[继续学习] [查看成就] [今日提示]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return template
    
    def help_user(self, context: str = None) -> str:
        """
        帮助引导
        
        Args:
            context: 用户需要帮助的具体内容
            
        Returns:
            帮助文本
        """
        task = self.task_scheduler.get_current_task()
        if not task:
            return "当前没有进行中的任务。输入「开始养成」开始你的旅程！"
        
        # 更新帮助统计
        self.progress_manager.update_stats("help_requested")
        
        # 根据上下文提供相关帮助
        hints = task.hints
        if context:
            # 简单匹配相关提示
            relevant_hints = [h for h in hints if context.lower() in h.lower()]
            if relevant_hints:
                hints = relevant_hints
        
        # 渲染帮助文本
        template = f"""
💡 任务帮助：{task.name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{task.description}

💬 小贴士：
"""
        for i, hint in enumerate(hints[:3], 1):  # 最多显示3个提示
            template += f"\n{i}. {hint}"
        
        if task.example:
            template += f"""

📝 示例：
{task.example}
"""
        
        template += """

[开始任务] [跳过此任务] [继续问]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return template
    
    # ==================== 辅助函数 ====================
    
    def _render_welcome_screen(self) -> str:
        """渲染欢迎界面"""
        return f"""
🦐 欢迎来到「虾的养成计划」！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你好，{self.user_name}！我是你的养成导师。

我会一步步带你从小白成长为顶级虾。
这不是枯燥的文档，而是一场游戏——
完成任务，解锁新能力，获得成就！

🎯 你将学习：
✓ 和AI有效对话
✓ 自动化日常任务
✓ 开发自己的Skill
✓ 组建AI团队
✓ 部署生产环境

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

准备好了吗？让我们开始第一课！

[开始第一课] [先看看我有什么] [以后再说]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()
    
    def _render_main_dashboard(self) -> str:
        """渲染主界面"""
        progress = self.progress_manager.get_progress()
        task = self.task_scheduler.get_current_task()
        
        if not progress or not task:
            return self._render_welcome_screen()
        
        stage = get_stage_by_id(task.stage_id)
        
        # 今日提示
        daily_tips = [
            "试试让AI帮你整理邮件",
            "设置一个定时任务自动备份文件",
            "探索一下web_search功能",
            "创建一个新文件并用AI读取它",
            "让AI帮你列出当前目录的文件"
        ]
        import random
        tip = random.choice(daily_tips)
        
        template = f"""
🦐 虾的养成计划
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你好，{progress.user_name}！今天想做点什么？

📚 继续学习
   当前：{stage.name if stage else '未知'} - {task.name}
   
📊 查看进度
   Lv.{progress.level} | 🔥 {progress.streak_days}天连续
   
🏆 我的成就
   已获得：{len(progress.achievements)}/20
   
💡 每日提示
   "{tip}"
   
❓ 需要帮助

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输入数字或说出你想做的事
"""
        return template
    
    def _render_completion_feedback(self, task: Task, exp_gained: int,
                                    level_up: bool, old_level: int, new_level: int,
                                    new_achievements: List[Achievement],
                                    stage_complete: bool, next_task_id: str) -> str:
        """渲染任务完成反馈"""
        progress = self.progress_manager.get_progress()
        
        template = f"""
✨ 任务完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

太棒了，{progress.user_name}！
你完成了「{task.name}」

📈 获得经验值：+{exp_gained}
"""
        
        if level_up:
            template += f"""
🎉 升级了！Lv.{old_level} → Lv.{new_level}
   新称号：{self.exp_calculator.get_title_by_level(new_level)}
"""
        
        if new_achievements:
            template += "\n🏅 解锁成就：\n"
            for ach in new_achievements:
                template += f"   {ach.emoji} 【{ach.name}】\n"
        
        if stage_complete:
            stage = get_stage_by_id(task.stage_id)
            if stage:
                template += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎊 阶段完成！

你完成了【{stage.name}】！
获得称号：【{stage.reward.get('title', '')}】
解锁能力：{stage.reward.get('ability', '')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # 下一任务
        if next_task_id:
            next_task = get_task_by_id(next_task_id)
            if next_task:
                template += f"""

💡 下一任务：{next_task.name}
[开始] [休息一下]
"""
        
        template += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        return template
    
    def _format_hints(self, hints: List[str]) -> str:
        """格式化提示"""
        if not hints:
            return "暂无提示"
        return "\n".join(f"• {h}" for h in hints[:3])
    
    def _render_difficulty(self, difficulty: str) -> str:
        """渲染难度"""
        difficulty_map = {
            "easy": "⭐ 简单",
            "medium": "⭐⭐ 中等",
            "hard": "⭐⭐⭐ 困难",
            "expert": "⭐⭐⭐⭐ 专家"
        }
        return difficulty_map.get(difficulty, "⭐ 简单")
    
    def _render_mini_progress_bar(self, percentage: int, width: int = 10) -> str:
        """渲染迷你进度条"""
        filled = int(width * percentage / 100)
        empty = width - filled
        return "█" * filled + "░" * empty
    
    # ==================== 快捷函数 ====================
    
    def switch_stage(self, stage_id: str) -> str:
        """切换到指定阶段"""
        stage = get_stage_by_id(stage_id)
        if not stage:
            return "阶段不存在。"
        
        progress = self.progress_manager.get_progress()
        if not progress:
            return "请先开始学习。"
        
        # 检查是否解锁
        # 简化处理：只允许切换到已开始或已完成的阶段
        stage_tasks = set(stage.tasks)
        completed = set(progress.completed_tasks)
        skipped = set(progress.skipped_tasks)
        
        if not stage_tasks.intersection(completed.union(skipped)):
            return f"🔒 {stage.name} 还未解锁，请先完成前置阶段。"
        
        # 切换到该阶段的第一个未完成任务
        for task_id in stage.tasks:
            if task_id not in progress.completed_tasks and task_id not in progress.skipped_tasks:
                progress.current_task = task_id
                progress.current_stage = stage_id
                self.progress_manager.save_progress(progress)
                return f"已切换到【{stage.name}】\n\n{self.get_current_task()}"
        
        # 该阶段已完成
        return f"【{stage.name}】已完成！使用「查看进度」查看详情。"
    
    def show_achievements(self) -> str:
        """展示所有成就"""
        achievements = self.achievement_system.get_user_achievements(include_locked=True)
        stats = self.achievement_system.get_achievement_stats()
        
        template = f"""
🏆 我的成就
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

已获得：{stats['total_unlocked']}/{stats['total_achievements']} ({stats['completion_percentage']}%)

"""
        
        # 按稀有度分组显示
        for rarity in ["legendary", "epic", "rare", "common"]:
            rarity_achievements = [a for a in achievements if a['rarity'] == rarity]
            if rarity_achievements:
                rarity_name = {"common": "普通", "rare": "稀有", "epic": "史诗", "legendary": "传说"}.get(rarity, rarity)
                template += f"\n【{rarity_name}】\n"
                for a in rarity_achievements[:5]:  # 每种最多显示5个
                    status = "✓" if a['unlocked'] else "○"
                    template += f"  {status} {a['emoji']} {a['name']}\n"
        
        template += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return template
    
    def reset_progress(self, confirmed: bool = False) -> str:
        """重置进度"""
        if not confirmed:
            return """
⚠️ 确认重置进度？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

这将清除你的所有学习进度、成就和经验值。
此操作不可恢复！

确定要重置吗？

[确认重置] [取消]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if self.progress_manager.reset_progress(confirm=True):
            return "进度已重置。输入「开始养成」重新开始你的旅程！"
        return "重置失败，请稍后重试。"


# ==================== 快捷入口函数 ====================

def start_skill(user_id: str, user_name: str = "虾友") -> str:
    """Skill主入口"""
    skill = ShrimpGrowthSkill(user_id, user_name)
    return skill.start_skill()

def get_current_task(user_id: str) -> str:
    """获取当前任务"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.get_current_task()

def complete_task(user_id: str, task_id: str = None) -> str:
    """完成任务"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.complete_task(task_id)

def check_achievements(user_id: str) -> str:
    """检查成就"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.check_achievements()

def show_progress(user_id: str) -> str:
    """展示进度"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.show_progress()

def help_user(user_id: str, context: str = None) -> str:
    """帮助引导"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.help_user(context)

def switch_stage(user_id: str, stage_id: str) -> str:
    """切换阶段"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.switch_stage(stage_id)

def show_achievements(user_id: str) -> str:
    """展示成就"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.show_achievements()

def reset_progress(user_id: str, confirmed: bool = False) -> str:
    """重置进度"""
    skill = ShrimpGrowthSkill(user_id)
    return skill.reset_progress(confirmed)
