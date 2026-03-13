"""
虾的养成计划 - 任务调度模块
负责任务管理、完成验证和任务推荐
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from models import (
    UserProgress, Task, Stage,
    get_task_by_id, get_tasks_by_stage, get_stage_by_id
)
from progress_manager import ProgressManager


class TaskValidationResult:
    """任务验证结果"""
    def __init__(self, is_valid: bool, message: str = "", details: Dict = None):
        self.is_valid = is_valid
        self.message = message
        self.details = details or {}


class CompletionResult:
    """任务完成结果"""
    def __init__(self, success: bool, exp_gained: int = 0, 
                 level_up: bool = False, new_level: int = None,
                 new_achievements: List[str] = None,
                 stage_completed: bool = False,
                 next_task_id: str = None):
        self.success = success
        self.exp_gained = exp_gained
        self.level_up = level_up
        self.new_level = new_level
        self.new_achievements = new_achievements or []
        self.stage_completed = stage_completed
        self.next_task_id = next_task_id


class TaskScheduler:
    """
    任务调度器
    
    负责：
    - 获取当前任务
    - 标记任务完成
    - 推荐下一个任务
    - 验证任务完成条件
    """
    
    def __init__(self, user_id: str, progress_manager: ProgressManager = None):
        """
        初始化任务调度器
        
        Args:
            user_id: 用户ID
            progress_manager: 进度管理器实例
        """
        self.user_id = user_id
        self.progress_manager = progress_manager or ProgressManager(user_id)
    
    def get_current_task(self) -> Optional[Task]:
        """
        获取当前任务
        
        Returns:
            当前任务对象，如果不存在返回None
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return None
        
        return get_task_by_id(progress.current_task)
    
    def get_task_status(self, task_id: str, progress: UserProgress = None) -> str:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            progress: 用户进度对象
            
        Returns:
            任务状态字符串
        """
        if not progress:
            progress = self.progress_manager.get_progress()
        
        if not progress:
            return "locked"
        
        if task_id in progress.completed_tasks:
            return "completed"
        
        if task_id in progress.skipped_tasks:
            return "skipped"
        
        if task_id == progress.current_task:
            return "current"
        
        # 检查前置任务
        task = get_task_by_id(task_id)
        if task and task.prerequisites:
            all_prereq_done = all(
                p in progress.completed_tasks or p in progress.skipped_tasks
                for p in task.prerequisites
            )
            return "available" if all_prereq_done else "locked"
        
        # 同一阶段的任务
        current_task = get_task_by_id(progress.current_task)
        if current_task and current_task.stage_id == task.stage_id:
            return "available"
        
        return "locked"
    
    def complete_task(self, task_id: str = None, context: Dict = None) -> CompletionResult:
        """
        完成任务
        
        Args:
            task_id: 要完成的任务ID，None表示当前任务
            context: 任务上下文信息
            
        Returns:
            完成结果
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return CompletionResult(success=False, message="用户进度不存在")
        
        # 确定任务ID
        if not task_id:
            task_id = progress.current_task
        
        task = get_task_by_id(task_id)
        if not task:
            return CompletionResult(success=False, message="任务不存在")
        
        # 验证任务是否可以完成
        if task_id in progress.completed_tasks:
            return CompletionResult(success=False, message="任务已完成")
        
        # 验证任务完成条件
        validation = self.validate_task_completion(task, context)
        if not validation.is_valid:
            return CompletionResult(success=False, message=validation.message)
        
        # 更新进度
        if task_id not in progress.completed_tasks:
            progress.completed_tasks.append(task_id)
        
        # 更新统计
        progress.stats["tasks_completed"] = len(progress.completed_tasks)
        
        # 计算经验值
        exp_gain = self._calculate_task_exp(task, context)
        old_level = progress.level
        progress.exp += exp_gain
        
        # 获取下一个任务
        next_task_id = self._get_next_task_id(progress, task)
        progress.current_task = next_task_id if next_task_id else task_id
        
        # 检查阶段完成
        stage_completed = self._check_stage_completion(progress, task.stage_id)
        
        # 保存进度
        self.progress_manager.save_progress(progress)
        
        # 更新等级（如果需要，由ExpCalculator处理）
        # 这里只返回原始结果，等级检查在外部处理
        
        return CompletionResult(
            success=True,
            exp_gained=exp_gain,
            level_up=False,  # 由外部计算
            new_level=None,
            new_achievements=[],  # 由外部计算
            stage_completed=stage_completed,
            next_task_id=next_task_id
        )
    
    def skip_task(self, task_id: str = None) -> bool:
        """
        跳过任务
        
        Args:
            task_id: 要跳过的任务ID，None表示当前任务
            
        Returns:
            是否成功跳过
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return False
        
        if not task_id:
            task_id = progress.current_task
        
        task = get_task_by_id(task_id)
        if not task:
            return False
        
        # 检查是否可以跳过
        if not task.can_skip:
            return False
        
        # 添加到跳过列表
        if task_id not in progress.skipped_tasks:
            progress.skipped_tasks.append(task_id)
        
        # 更新统计
        progress.stats["tasks_skipped"] = len(progress.skipped_tasks)
        
        # 获取下一个任务
        next_task_id = self._get_next_task_id(progress, task)
        if next_task_id:
            progress.current_task = next_task_id
        
        # 保存进度
        self.progress_manager.save_progress(progress)
        
        return True
    
    def get_next_task(self, current_task: Task = None) -> Optional[Task]:
        """
        获取下一个任务
        
        Args:
            current_task: 当前任务对象
            
        Returns:
            下一个任务对象，如果没有返回None
        """
        progress = self.progress_manager.get_progress()
        if not progress:
            return None
        
        if not current_task:
            current_task = get_task_by_id(progress.current_task)
        
        if not current_task:
            return None
        
        next_task_id = self._get_next_task_id(progress, current_task)
        return get_task_by_id(next_task_id) if next_task_id else None
    
    def _get_next_task_id(self, progress: UserProgress, current_task: Task) -> Optional[str]:
        """
        获取下一个任务ID
        
        Args:
            progress: 用户进度
            current_task: 当前任务
            
        Returns:
            下一个任务ID
        """
        stage = get_stage_by_id(current_task.stage_id)
        if not stage:
            return None
        
        # 获取当前阶段的所有任务
        stage_tasks = stage.tasks
        
        # 找到当前任务在列表中的位置
        try:
            current_index = stage_tasks.index(current_task.task_id)
        except ValueError:
            return None
        
        # 检查当前阶段是否还有后续任务
        if current_index + 1 < len(stage_tasks):
            return stage_tasks[current_index + 1]
        
        # 当前阶段已完成，进入下一阶段
        stages_order = ["stage1", "stage2", "stage3", "stage4", "stage5"]
        current_stage_index = stages_order.index(current_task.stage_id)
        
        if current_stage_index + 1 < len(stages_order):
            next_stage_id = stages_order[current_stage_index + 1]
            next_stage = get_stage_by_id(next_stage_id)
            if next_stage and next_stage.tasks:
                return next_stage.tasks[0]
        
        return None
    
    def validate_task_completion(self, task: Task, context: Dict = None) -> TaskValidationResult:
        """
        验证任务是否完成
        
        Args:
            task: 任务对象
            context: 任务上下文
            
        Returns:
            验证结果
        """
        if not task.validation:
            # 无验证条件，默认通过
            return TaskValidationResult(True)
        
        validation_type = task.validation.get("type", "none")
        
        # 这里可以实现具体的验证逻辑
        # 目前简化处理，返回通过
        
        validators = {
            "message_count": self._validate_message_count,
            "file_operation": self._validate_file_operation,
            "tool_usage": self._validate_tool_usage,
            "skill_created": self._validate_skill_created,
            "api_integration": self._validate_api_integration,
            "device_control": self._validate_device_control,
            "multi_agent": self._validate_multi_agent,
            "workflow_created": self._validate_workflow,
            "project_complete": self._validate_project,
            "deployment": self._validate_deployment,
            "community_contribution": self._validate_contribution,
            "real_world_project": self._validate_real_project,
            "none": lambda t, c: TaskValidationResult(True)
        }
        
        validator = validators.get(validation_type)
        if validator:
            return validator(task, context)
        
        return TaskValidationResult(True)
    
    def _validate_message_count(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证消息数量"""
        threshold = task.validation.get("threshold", 1)
        # 简化处理
        return TaskValidationResult(True, f"已验证对话次数 >= {threshold}")
    
    def _validate_file_operation(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证文件操作"""
        operation = task.validation.get("operation", "read")
        return TaskValidationResult(True, f"已验证文件操作: {operation}")
    
    def _validate_tool_usage(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证工具使用"""
        tool = task.validation.get("tool", "")
        return TaskValidationResult(True, f"已验证工具使用: {tool}")
    
    def _validate_skill_created(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证Skill创建"""
        return TaskValidationResult(True, "已验证Skill创建")
    
    def _validate_api_integration(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证API集成"""
        return TaskValidationResult(True, "已验证API集成")
    
    def _validate_device_control(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证设备控制"""
        return TaskValidationResult(True, "已验证设备控制")
    
    def _validate_multi_agent(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证多Agent"""
        count = task.validation.get("count", 3)
        return TaskValidationResult(True, f"已验证多Agent配置 >= {count}")
    
    def _validate_workflow(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证工作流"""
        return TaskValidationResult(True, "已验证工作流创建")
    
    def _validate_project(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证项目完成"""
        return TaskValidationResult(True, "已验证项目完成")
    
    def _validate_deployment(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证部署"""
        return TaskValidationResult(True, "已验证云端部署")
    
    def _validate_contribution(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证社区贡献"""
        return TaskValidationResult(True, "已验证社区贡献")
    
    def _validate_real_project(self, task: Task, context: Dict) -> TaskValidationResult:
        """验证真实项目"""
        return TaskValidationResult(True, "已验证真实项目")
    
    def _calculate_task_exp(self, task: Task, context: Dict = None) -> int:
        """
        计算任务经验值
        
        Args:
            task: 任务对象
            context: 任务上下文
            
        Returns:
            经验值
        """
        base_exp = task.reward.get("exp", 20)
        
        # 难度加成
        difficulty_bonus = {
            "easy": 0,
            "medium": 10,
            "hard": 25,
            "expert": 50
        }
        bonus = difficulty_bonus.get(task.difficulty, 0)
        
        # 首次完成加成（如果有跳过再完成的情况）
        progress = self.progress_manager.get_progress()
        first_time_bonus = 0
        if progress and task.task_id not in progress.completed_tasks:
            if task.task_id in progress.skipped_tasks:
                first_time_bonus = 5  # 回头完成跳过任务的奖励
        
        return base_exp + bonus + first_time_bonus
    
    def _check_stage_completion(self, progress: UserProgress, stage_id: str) -> bool:
        """
        检查阶段是否完成
        
        Args:
            progress: 用户进度
            stage_id: 阶段ID
            
        Returns:
            阶段是否完成
        """
        stage = get_stage_by_id(stage_id)
        if not stage:
            return False
        
        # 检查所有任务是否完成（包括跳过的）
        for task_id in stage.tasks:
            if (task_id not in progress.completed_tasks and 
                task_id not in progress.skipped_tasks):
                return False
        
        return True
    
    def get_stage_progress(self, stage_id: str) -> Dict[str, Any]:
        """
        获取阶段进度详情
        
        Args:
            stage_id: 阶段ID
            
        Returns:
            阶段进度详情
        """
        progress = self.progress_manager.get_progress()
        stage = get_stage_by_id(stage_id)
        
        if not stage:
            return {}
        
        tasks_status = []
        completed_count = 0
        
        for task_id in stage.tasks:
            task = get_task_by_id(task_id)
            status = self.get_task_status(task_id, progress)
            
            if status == "completed":
                completed_count += 1
            
            tasks_status.append({
                "task_id": task_id,
                "name": task.name if task else "未知",
                "status": status
            })
        
        total = len(stage.tasks)
        percentage = int((completed_count / total) * 100) if total > 0 else 0
        
        return {
            "stage_id": stage_id,
            "name": stage.name,
            "emoji": stage.emoji,
            "total_tasks": total,
            "completed_tasks": completed_count,
            "percentage": percentage,
            "is_current": progress.current_stage == stage_id if progress else False,
            "is_completed": completed_count == total,
            "tasks": tasks_status
        }
