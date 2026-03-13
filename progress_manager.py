"""
虾的养成计划 - 用户进度管理模块
管理用户的学习进度、数据持久化和状态更新
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from models import UserProgress, Task, get_task_by_id, get_tasks_by_stage


class ProgressManager:
    """
    用户进度管理器
    
    负责：
    - 用户进度的读取和保存
    - 新用户初始化
    - 连续学习天数计算
    - 最后活跃时间更新
    """
    
    def __init__(self, user_id: str, data_dir: str = "memory/shrimp_growth/"):
        """
        初始化进度管理器
        
        Args:
            user_id: 用户唯一标识
            data_dir: 数据存储目录
        """
        self.user_id = user_id
        self.data_dir = data_dir
        self._ensure_data_dir()
    
    def _ensure_data_dir(self) -> None:
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _get_user_file_path(self) -> str:
        """获取用户数据文件路径"""
        return os.path.join(self.data_dir, f"{self.user_id}.json")
    
    def get_progress(self) -> Optional[UserProgress]:
        """
        获取用户进度
        
        Returns:
            UserProgress对象，如果不存在返回None
        """
        file_path = self._get_user_file_path()
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return UserProgress.from_dict(data)
        except (json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Error loading progress for {self.user_id}: {e}")
            return None
    
    def save_progress(self, progress: UserProgress) -> bool:
        """
        保存用户进度
        
        Args:
            progress: 用户进度对象
            
        Returns:
            保存是否成功
        """
        file_path = self._get_user_file_path()
        
        try:
            # 更新最后活跃时间
            progress.last_active = datetime.now().isoformat()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(progress.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Error saving progress for {self.user_id}: {e}")
            return False
    
    def init_new_user(self, user_name: str) -> UserProgress:
        """
        初始化新用户
        
        Args:
            user_name: 用户名称
            
        Returns:
            新创建的用户进度对象
        """
        progress = UserProgress(
            user_id=self.user_id,
            user_name=user_name,
            current_stage="stage1",
            current_task="task1",
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat(),
            last_streak_date=datetime.now().isoformat()
        )
        
        self.save_progress(progress)
        return progress
    
    def update_last_active(self) -> bool:
        """
        更新最后活跃时间
        
        Returns:
            更新是否成功
        """
        progress = self.get_progress()
        if not progress:
            return False
        
        progress.last_active = datetime.now().isoformat()
        return self.save_progress(progress)
    
    def check_and_update_streak(self) -> int:
        """
        检查并更新连续学习天数
        
        Returns:
            当前连续学习天数
        """
        progress = self.get_progress()
        if not progress:
            return 0
        
        today = datetime.now().date()
        last_date = None
        
        if progress.last_streak_date:
            last_date = datetime.fromisoformat(progress.last_streak_date).date()
        
        if last_date:
            diff = (today - last_date).days
            
            if diff == 0:
                # 今天已经记录过
                return progress.streak_days
            elif diff == 1:
                # 连续学习
                progress.streak_days += 1
                progress.total_days += 1
            else:
                # 中断，重新开始
                progress.streak_days = 1
                progress.total_days += 1
        else:
            # 第一次学习
            progress.streak_days = 1
            progress.total_days = 1
        
        progress.last_streak_date = datetime.now().isoformat()
        self.save_progress(progress)
        
        return progress.streak_days
    
    def is_new_day(self) -> bool:
        """
        检查是否是新的一天
        
        Returns:
            是否是新一天
        """
        progress = self.get_progress()
        if not progress or not progress.last_active:
            return True
        
        last_active = datetime.fromisoformat(progress.last_active).date()
        today = datetime.now().date()
        
        return today > last_active
    
    def get_or_create_progress(self, user_name: str = "虾友") -> UserProgress:
        """
        获取或创建用户进度
        
        Args:
            user_name: 默认用户名
            
        Returns:
            用户进度对象
        """
        progress = self.get_progress()
        
        if not progress:
            progress = self.init_new_user(user_name)
        
        # 更新连续学习天数
        self.check_and_update_streak()
        
        return progress
    
    def is_new_user(self, progress: UserProgress) -> bool:
        """
        检查是否为新用户
        
        判断标准：
        - 只完成了0个或极少的任务
        - 创建时间在24小时内
        
        Args:
            progress: 用户进度
            
        Returns:
            是否为新用户
        """
        if len(progress.completed_tasks) == 0:
            return True
        
        # 检查创建时间
        created = datetime.fromisoformat(progress.created_at)
        hours_since = (datetime.now() - created).total_seconds() / 3600
        
        return hours_since < 24 and len(progress.completed_tasks) < 2
    
    def update_stats(self, stat_name: str, increment: int = 1) -> bool:
        """
        更新统计数据
        
        Args:
            stat_name: 统计项名称
            increment: 增加数量
            
        Returns:
            更新是否成功
        """
        progress = self.get_progress()
        if not progress:
            return False
        
        if stat_name not in progress.stats:
            progress.stats[stat_name] = 0
        
        progress.stats[stat_name] += increment
        return self.save_progress(progress)
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """
        获取进度摘要
        
        Returns:
            进度摘要字典
        """
        progress = self.get_progress()
        
        if not progress:
            return {
                "exists": False,
                "is_new_user": True
            }
        
        # 计算总体进度百分比
        total_tasks = 15  # 总共15个任务
        completed = len(progress.completed_tasks)
        overall_percentage = int((completed / total_tasks) * 100)
        
        # 获取当前任务信息
        current_task = get_task_by_id(progress.current_task)
        
        return {
            "exists": True,
            "user_name": progress.user_name,
            "level": progress.level,
            "exp": progress.exp,
            "streak_days": progress.streak_days,
            "total_days": progress.total_days,
            "completed_tasks": len(progress.completed_tasks),
            "skipped_tasks": len(progress.skipped_tasks),
            "achievements": len(progress.achievements),
            "overall_percentage": overall_percentage,
            "current_stage": progress.current_stage,
            "current_task_id": progress.current_task,
            "current_task_name": current_task.name if current_task else "未知",
            "is_new_user": self.is_new_user(progress),
            "created_at": progress.created_at,
            "last_active": progress.last_active
        }
    
    def reset_progress(self, confirm: bool = False) -> bool:
        """
        重置用户进度
        
        Args:
            confirm: 是否确认重置
            
        Returns:
            重置是否成功
        """
        if not confirm:
            return False
        
        file_path = self._get_user_file_path()
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except IOError as e:
            print(f"Error resetting progress for {self.user_id}: {e}")
            return False
    
    def export_progress(self) -> Optional[str]:
        """
        导出进度为JSON字符串
        
        Returns:
            JSON字符串，失败返回None
        """
        progress = self.get_progress()
        if not progress:
            return None
        
        return json.dumps(progress.to_dict(), ensure_ascii=False, indent=2)
    
    def import_progress(self, json_data: str) -> bool:
        """
        从JSON导入进度
        
        Args:
            json_data: JSON字符串
            
        Returns:
            导入是否成功
        """
        try:
            data = json.loads(json_data)
            progress = UserProgress.from_dict(data)
            progress.user_id = self.user_id  # 确保用户ID正确
            return self.save_progress(progress)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error importing progress: {e}")
            return False
