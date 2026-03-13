"""
虾的养成计划 - 数据结构定义
定义所有核心数据模型和常量
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class StageId(Enum):
    """阶段ID枚举"""
    STAGE1 = "stage1"
    STAGE2 = "stage2"
    STAGE3 = "stage3"
    STAGE4 = "stage4"
    STAGE5 = "stage5"


class TaskStatus(Enum):
    """任务状态"""
    LOCKED = "locked"          # 未解锁
    AVAILABLE = "available"    # 可开始
    IN_PROGRESS = "in_progress" # 进行中
    COMPLETED = "completed"     # 已完成
    SKIPPED = "skipped"         # 已跳过


class Difficulty(Enum):
    """任务难度"""
    EASY = "easy"       # 简单
    MEDIUM = "medium"   # 中等
    HARD = "hard"       # 困难
    EXPERT = "expert"   # 专家


class Rarity(Enum):
    """成就稀有度"""
    COMMON = "common"       # 普通
    RARE = "rare"           # 稀有
    EPIC = "epic"           # 史诗
    LEGENDARY = "legendary" # 传说
    SECRET = "secret"       # 隐藏


@dataclass
class UserProgress:
    """
    用户进度数据模型
    
    存储用户的学习进度、成就、经验值等核心数据
    """
    user_id: str
    user_name: str
    current_stage: str = "stage1"
    current_task: str = "task1"
    completed_tasks: List[str] = field(default_factory=list)
    skipped_tasks: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    exp: int = 0
    level: int = 1
    streak_days: int = 0
    total_days: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    last_streak_date: Optional[str] = None
    
    # 设置
    settings: Dict[str, Any] = field(default_factory=lambda: {
        "daily_reminder": True,
        "notification_enabled": True,
        "auto_advance": False
    })
    
    # 统计
    stats: Dict[str, int] = field(default_factory=lambda: {
        "tasks_completed": 0,
        "tasks_skipped": 0,
        "help_requested": 0,
        "hints_viewed": 0,
        "demos_watched": 0
    })
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "current_stage": self.current_stage,
            "current_task": self.current_task,
            "completed_tasks": self.completed_tasks,
            "skipped_tasks": self.skipped_tasks,
            "achievements": self.achievements,
            "exp": self.exp,
            "level": self.level,
            "streak_days": self.streak_days,
            "total_days": self.total_days,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "last_streak_date": self.last_streak_date,
            "settings": self.settings,
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "UserProgress":
        """从字典创建"""
        return cls(
            user_id=data.get("user_id", ""),
            user_name=data.get("user_name", "虾友"),
            current_stage=data.get("current_stage", "stage1"),
            current_task=data.get("current_task", "task1"),
            completed_tasks=data.get("completed_tasks", []),
            skipped_tasks=data.get("skipped_tasks", []),
            achievements=data.get("achievements", []),
            exp=data.get("exp", 0),
            level=data.get("level", 1),
            streak_days=data.get("streak_days", 0),
            total_days=data.get("total_days", 0),
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_active=data.get("last_active", datetime.now().isoformat()),
            last_streak_date=data.get("last_streak_date"),
            settings=data.get("settings", {}),
            stats=data.get("stats", {})
        )


@dataclass
class Stage:
    """
    阶段定义数据模型
    
    定义每个学习阶段的基本信息、任务列表和奖励
    """
    stage_id: str
    name: str
    emoji: str
    description: str
    duration_days: int
    tasks: List[str]
    unlock_requirement: Optional[Dict] = None
    reward: Dict[str, Any] = field(default_factory=dict)
    theme_color: str = "#4A90D9"
    
    def to_dict(self) -> Dict:
        return {
            "stage_id": self.stage_id,
            "name": self.name,
            "emoji": self.emoji,
            "description": self.description,
            "duration_days": self.duration_days,
            "tasks": self.tasks,
            "unlock_requirement": self.unlock_requirement,
            "reward": self.reward,
            "theme_color": self.theme_color
        }


@dataclass
class Task:
    """
    任务定义数据模型
    
    定义每个学习任务的详细信息、验证条件和奖励
    """
    task_id: str
    stage_id: str
    name: str
    description: str
    instructions: str
    hints: List[str] = field(default_factory=list)
    example: Optional[str] = None
    validation: Dict[str, Any] = field(default_factory=dict)
    reward: Dict[str, Any] = field(default_factory=dict)
    estimated_time: str = "10分钟"
    difficulty: str = "easy"
    can_skip: bool = True
    can_demo: bool = True
    prerequisites: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "stage_id": self.stage_id,
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "hints": self.hints,
            "example": self.example,
            "validation": self.validation,
            "reward": self.reward,
            "estimated_time": self.estimated_time,
            "difficulty": self.difficulty,
            "can_skip": self.can_skip,
            "can_demo": self.can_demo,
            "prerequisites": self.prerequisites
        }


@dataclass
class Achievement:
    """
    成就定义数据模型
    
    定义每个成就的解锁条件和展示信息
    """
    achievement_id: str
    name: str
    emoji: str
    description: str
    condition: Dict[str, Any]
    rarity: str = "common"
    secret: bool = False
    hidden_hint: Optional[str] = None  # 隐藏成就的提示
    reward_exp: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "achievement_id": self.achievement_id,
            "name": self.name,
            "emoji": self.emoji,
            "description": self.description,
            "condition": self.condition,
            "rarity": self.rarity,
            "secret": self.secret,
            "hidden_hint": self.hidden_hint,
            "reward_exp": self.reward_exp
        }


@dataclass
class LevelConfig:
    """
    等级配置
    
    定义每个等级的经验值要求和称号
    """
    level: int
    min_exp: int
    title: str
    title_emoji: str = "🦐"
    

# 等级配置表
LEVEL_TABLE = [
    LevelConfig(1, 0, "虾苗", "🥚"),
    LevelConfig(2, 100, "初级虾仔", "🦐"),
    LevelConfig(3, 250, "见习工兵", "🦐"),
    LevelConfig(4, 450, "勤劳工兵", "🦐"),
    LevelConfig(5, 700, "认证建筑师", "🏗️"),
    LevelConfig(6, 1000, "资深建筑师", "🏗️"),
    LevelConfig(7, 1350, "系统架构师", "🎭"),
    LevelConfig(8, 1750, "高级架构师", "🎭"),
    LevelConfig(9, 2200, "准顶级虾", "👑"),
    LevelConfig(10, 2700, "顶级虾", "👑"),
]


# 阶段定义表
STAGES = [
    Stage(
        stage_id="stage1",
        name="孵化期",
        emoji="🥚",
        description="学会和AI对话，完成基础操作",
        duration_days=3,
        tasks=["task1", "task2", "task3"],
        unlock_requirement=None,
        reward={
            "title": "初级虾仔",
            "exp": 100,
            "ability": "批量重命名文件"
        },
        theme_color="#FFD93D"
    ),
    Stage(
        stage_id="stage2",
        name="工兵期",
        emoji="🦐",
        description="搭建个人自动化工作流",
        duration_days=7,
        tasks=["task4", "task5", "task6"],
        unlock_requirement={"stage": "stage1", "type": "complete"},
        reward={
            "title": "勤劳工兵虾",
            "exp": 200,
            "ability": "开发自定义Skill"
        },
        theme_color="#4A90D9"
    ),
    Stage(
        stage_id="stage3",
        name="建筑师期",
        emoji="🏗️",
        description="开发自己的Skill，扩展AI能力",
        duration_days=14,
        tasks=["task7", "task8", "task9"],
        unlock_requirement={"stage": "stage2", "type": "complete"},
        reward={
            "title": "认证建筑师",
            "exp": 350,
            "ability": "多Agent协作"
        },
        theme_color="#6BCB77"
    ),
    Stage(
        stage_id="stage4",
        name="架构师期",
        emoji="🎭",
        description="搭建多Agent团队",
        duration_days=14,
        tasks=["task10", "task11", "task12"],
        unlock_requirement={"stage": "stage3", "type": "complete"},
        reward={
            "title": "系统架构师",
            "exp": 500,
            "ability": "生产环境部署"
        },
        theme_color="#9C51E0"
    ),
    Stage(
        stage_id="stage5",
        name="顶级虾",
        emoji="👑",
        description="成为社区贡献者",
        duration_days=14,
        tasks=["task13", "task14", "task15"],
        unlock_requirement={"stage": "stage4", "type": "complete"},
        reward={
            "title": "OpenClaw大师",
            "exp": 750,
            "ability": "导师资格认证"
        },
        theme_color="#FF6B6B"
    ),
]


# 任务定义表
TASKS = [
    # Stage 1: 孵化期
    Task(
        task_id="task1",
        stage_id="stage1",
        name="破冰对话",
        description="完成第一次与AI的对话",
        instructions="告诉我你的名字，随便说点什么",
        hints=[
            "直接说话就行",
            "比如'你好'或者'今天天气怎样'",
            "不用太正式，就像和朋友聊天"
        ],
        example="你好！我叫小明，我想学习怎么用AI",
        validation={"type": "message_count", "threshold": 1},
        reward={"exp": 20, "achievement": "first_talk"},
        estimated_time="5分钟",
        difficulty="easy"
    ),
    Task(
        task_id="task2",
        stage_id="stage1",
        name="文件小助手",
        description="创建文件并让AI读取它",
        instructions="在你的工作区创建一个txt文件，写点内容，然后让我读取它",
        hints=[
            "创建一个hello.txt文件",
            "里面写点简单的内容",
            "然后对我说：帮我读取hello.txt"
        ],
        example="先创建一个test.txt，然后让我读取它",
        validation={"type": "file_operation", "operation": "read"},
        reward={"exp": 30, "achievement": None},
        estimated_time="10分钟",
        difficulty="easy"
    ),
    Task(
        task_id="task3",
        stage_id="stage1",
        name="第一次自动化",
        description="让AI帮你列出文件夹内容",
        instructions="试试让我帮你列出当前文件夹里的所有文件",
        hints=[
            "可以说：帮我列出当前目录的文件",
            "或者：看看这里有什么文件",
            "观察AI是如何自动帮你完成的"
        ],
        validation={"type": "tool_usage", "tool": "exec"},
        reward={"exp": 50, "achievement": "auto_master"},
        estimated_time="10分钟",
        difficulty="easy"
    ),
    
    # Stage 2: 工兵期
    Task(
        task_id="task4",
        stage_id="stage2",
        name="每日晨报",
        description="使用网络搜索获取信息",
        instructions="让我帮你搜索今天的科技新闻",
        hints=[
            "可以说：帮我搜索今天的科技新闻",
            "或者：查查最近的AI资讯",
            "体验一下AI的信息获取能力"
        ],
        validation={"type": "tool_usage", "tool": "web_search"},
        reward={"exp": 40, "achievement": None},
        estimated_time="10分钟",
        difficulty="easy"
    ),
    Task(
        task_id="task5",
        stage_id="stage2",
        name="文件整理机器人",
        description="让AI帮你整理指定文件夹",
        instructions="指定一个文件夹，让AI按类型整理里面的文件",
        hints=[
            "找一个文件杂乱的文件夹",
            "告诉AI按文件类型分类",
            "比如：把图片放一起，文档放一起"
        ],
        validation={"type": "file_operation", "operation": "batch_organize"},
        reward={"exp": 60, "achievement": "file_master"},
        estimated_time="15分钟",
        difficulty="medium"
    ),
    Task(
        task_id="task6",
        stage_id="stage2",
        name="定时任务",
        description="设置一个自动化定时任务",
        instructions="设置一个定时任务，比如每天早上8点自动执行某个操作",
        hints=[
            "可以是定时备份文件",
            "或者定时发送提醒",
            "使用cron语法设置定时"
        ],
        validation={"type": "tool_usage", "tool": "cron"},
        reward={"exp": 100, "achievement": "scheduler_pro"},
        estimated_time="20分钟",
        difficulty="medium"
    ),
    
    # Stage 3: 建筑师期
    Task(
        task_id="task7",
        stage_id="stage3",
        name="我的第一个Skill",
        description="创建一个简单的Skill",
        instructions="创建一个功能简单的Skill，比如计算器或问候语",
        hints=[
            "从SKILL.md开始",
            "先实现最简单的功能",
            "参考已有的Skill模板"
        ],
        validation={"type": "skill_created", "count": 1},
        reward={"exp": 80, "achievement": "skill_builder"},
        estimated_time="30分钟",
        difficulty="medium"
    ),
    Task(
        task_id="task8",
        stage_id="stage3",
        name="API连接器",
        description="集成外部API到Skill中",
        instructions="连接一个真实的API，比如天气API",
        hints=[
            "找个免费的天气API",
            "学会发送HTTP请求",
            "把返回结果格式化"
        ],
        validation={"type": "api_integration", "count": 1},
        reward={"exp": 120, "achievement": "api_master"},
        estimated_time="40分钟",
        difficulty="hard"
    ),
    Task(
        task_id="task9",
        stage_id="stage3",
        name="智能家居控制",
        description="用AI控制智能设备",
        instructions="如果你有智能家居设备，尝试让AI控制它们",
        hints=[
            "可以是小爱同学、天猫精灵等",
            "通过API或技能控制",
            "注意安全，别误操作"
        ],
        validation={"type": "device_control", "count": 1},
        reward={"exp": 150, "achievement": "smart_home_guru"},
        estimated_time="45分钟",
        difficulty="hard",
        can_skip=True
    ),
    
    # Stage 4: 架构师期
    Task(
        task_id="task10",
        stage_id="stage4",
        name="组建AI团队",
        description="配置多Agent协作",
        instructions="配置至少3个不同角色的Agent",
        hints=[
            "比如研究员、工程师、审计员",
            "给每个Agent明确的职责",
            "测试他们之间的协作"
        ],
        validation={"type": "multi_agent", "count": 3},
        reward={"exp": 150, "achievement": "team_leader"},
        estimated_time="45分钟",
        difficulty="hard"
    ),
    Task(
        task_id="task11",
        stage_id="stage4",
        name="任务委派",
        description="设计工作流让Agent协作",
        instructions="设计一个工作流，让多个Agent分工完成任务",
        hints=[
            "分解任务步骤",
            "明确每个步骤的负责人",
            "设计交接和审核机制"
        ],
        validation={"type": "workflow_created", "count": 1},
        reward={"exp": 180, "achievement": "workflow_designer"},
        estimated_time="50分钟",
        difficulty="hard"
    ),
    Task(
        task_id="task12",
        stage_id="stage4",
        name="复杂项目实战",
        description="用AI团队完成一个真实项目",
        instructions="用多Agent团队完成一个复杂的自动化项目",
        hints=[
            "比如自动周报生成系统",
            "从需求到部署全流程",
            "记录遇到的问题和解决方案"
        ],
        validation={"type": "project_complete", "complexity": "high"},
        reward={"exp": 250, "achievement": "project_master"},
        estimated_time="60分钟",
        difficulty="expert"
    ),
    
    # Stage 5: 顶级虾
    Task(
        task_id="task13",
        stage_id="stage5",
        name="云端部署",
        description="将你的AI部署到服务器",
        instructions="把你的Skill或Agent部署到云服务器",
        hints=[
            "可以是VPS或云函数",
            "学习Docker部署",
            "确保7x24小时可用"
        ],
        validation={"type": "deployment", "environment": "cloud"},
        reward={"exp": 200, "achievement": "cloud_master"},
        estimated_time="60分钟",
        difficulty="expert"
    ),
    Task(
        task_id="task14",
        stage_id="stage5",
        name="分享与传承",
        description="分享你的经验和成果",
        instructions="发布你的Skill，写一篇教程，或帮助其他用户",
        hints=[
            "把你的Skill分享到社区",
            "写一篇学习心得",
            "帮助一个新手完成第一课"
        ],
        validation={"type": "community_contribution", "count": 1},
        reward={"exp": 250, "achievement": "mentor"},
        estimated_time="90分钟",
        difficulty="expert"
    ),
    Task(
        task_id="task15",
        stage_id="stage5",
        name="虾王挑战",
        description="解决一个真实世界的复杂问题",
        instructions="用你所学解决一个工作/生活中的实际问题",
        hints=[
            "选一个你真正需要的自动化场景",
            "从零设计到完整实现",
            "持续优化和维护"
        ],
        validation={"type": "real_world_project", "reviewed": True},
        reward={"exp": 500, "achievement": "shrimp_king"},
        estimated_time="120分钟",
        difficulty="expert"
    ),
]


# 成就定义表
ACHIEVEMENTS = [
    Achievement(
        achievement_id="first_talk",
        name="破壳而出",
        emoji="🥚",
        description="完成第一课",
        condition={"type": "task_complete", "task_id": "task1"},
        rarity="common",
        reward_exp=10
    ),
    Achievement(
        achievement_id="auto_master",
        name="自动化新手",
        emoji="🦐",
        description="完成孵化期所有任务",
        condition={"type": "stage_complete", "stage_id": "stage1"},
        rarity="common",
        reward_exp=20
    ),
    Achievement(
        achievement_id="file_master",
        name="文件整理大师",
        emoji="📁",
        description="完成文件整理任务",
        condition={"type": "task_complete", "task_id": "task5"},
        rarity="common",
        reward_exp=15
    ),
    Achievement(
        achievement_id="scheduler_pro",
        name="时间管理大师",
        emoji="⏰",
        description="成功设置定时任务",
        condition={"type": "task_complete", "task_id": "task6"},
        rarity="common",
        reward_exp=15
    ),
    Achievement(
        achievement_id="skill_builder",
        name="建筑许可证",
        emoji="🏗️",
        description="发布第一个Skill",
        condition={"type": "task_complete", "task_id": "task7"},
        rarity="rare",
        reward_exp=30
    ),
    Achievement(
        achievement_id="api_master",
        name="API魔法师",
        emoji="🔮",
        description="成功集成外部API",
        condition={"type": "task_complete", "task_id": "task8"},
        rarity="rare",
        reward_exp=30
    ),
    Achievement(
        achievement_id="smart_home_guru",
        name="智能家居大师",
        emoji="🏠",
        description="用AI控制智能设备",
        condition={"type": "task_complete", "task_id": "task9"},
        rarity="rare",
        reward_exp=40
    ),
    Achievement(
        achievement_id="team_leader",
        name="团队领袖",
        emoji="👥",
        description="组建3人AI团队",
        condition={"type": "task_complete", "task_id": "task10"},
        rarity="rare",
        reward_exp=50
    ),
    Achievement(
        achievement_id="workflow_designer",
        name="流程设计大师",
        emoji="📊",
        description="设计完整工作流",
        condition={"type": "task_complete", "task_id": "task11"},
        rarity="rare",
        reward_exp=50
    ),
    Achievement(
        achievement_id="project_master",
        name="项目指挥官",
        emoji="🎯",
        description="完成复杂项目实战",
        condition={"type": "task_complete", "task_id": "task12"},
        rarity="epic",
        reward_exp=80
    ),
    Achievement(
        achievement_id="cloud_master",
        name="云端漫步者",
        emoji="☁️",
        description="完成云端部署",
        condition={"type": "task_complete", "task_id": "task13"},
        rarity="epic",
        reward_exp=80
    ),
    Achievement(
        achievement_id="mentor",
        name="传承者",
        emoji="🎓",
        description="帮助其他用户",
        condition={"type": "task_complete", "task_id": "task14"},
        rarity="epic",
        reward_exp=100
    ),
    Achievement(
        achievement_id="shrimp_king",
        name="虾王认证",
        emoji="👑",
        description="完成所有任务，成为顶级虾",
        condition={"type": "stage_complete", "stage_id": "stage5"},
        rarity="legendary",
        reward_exp=200
    ),
    Achievement(
        achievement_id="streak_7",
        name="一周坚持",
        emoji="🔥",
        description="连续7天学习",
        condition={"type": "streak_days", "days": 7},
        rarity="common",
        reward_exp=50
    ),
    Achievement(
        achievement_id="streak_30",
        name="月度达人",
        emoji="📅",
        description="连续30天学习",
        condition={"type": "streak_days", "days": 30},
        rarity="rare",
        reward_exp=150
    ),
    Achievement(
        achievement_id="speed_runner",
        name="速通玩家",
        emoji="⚡",
        description="7天内完成所有阶段",
        condition={"type": "speed_run", "days": 7},
        rarity="epic",
        secret=True,
        hidden_hint="听说有人一周就通关了...",
        reward_exp=300
    ),
    Achievement(
        achievement_id="completionist",
        name="完美主义者",
        emoji="💎",
        description="获得所有成就",
        condition={"type": "all_achievements"},
        rarity="legendary",
        secret=True,
        hidden_hint="这真的可能吗？",
        reward_exp=500
    ),
]


def get_stage_by_id(stage_id: str) -> Optional[Stage]:
    """根据ID获取阶段"""
    for stage in STAGES:
        if stage.stage_id == stage_id:
            return stage
    return None


def get_task_by_id(task_id: str) -> Optional[Task]:
    """根据ID获取任务"""
    for task in TASKS:
        if task.task_id == task_id:
            return task
    return None


def get_achievement_by_id(achievement_id: str) -> Optional[Achievement]:
    """根据ID获取成就"""
    for achievement in ACHIEVEMENTS:
        if achievement.achievement_id == achievement_id:
            return achievement
    return None


def get_tasks_by_stage(stage_id: str) -> List[Task]:
    """获取阶段的所有任务"""
    return [task for task in TASKS if task.stage_id == stage_id]


def get_level_config(level: int) -> Optional[LevelConfig]:
    """获取等级配置"""
    for config in LEVEL_TABLE:
        if config.level == level:
            return config
    return None


def get_next_level_exp(level: int) -> int:
    """获取下一级所需经验"""
    for config in LEVEL_TABLE:
        if config.level == level + 1:
            return config.min_exp
    return LEVEL_TABLE[-1].min_exp + 500
