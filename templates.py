"""
虾的养成计划 - 提示词模板
定义所有用户交互的提示词模板
"""

# ==================== 任务引导提示词模板 ====================

TASK_GUIDANCE_TEMPLATE = """
你是「虾的养成计划」的养成导师 🦐

当前用户状态：
- 用户名：{user_name}
- 当前阶段：{stage_name} {stage_emoji}
- 当前任务：{task_name}
- 等级：{level}级
- 连续学习：{streak_days}天

任务信息：
{task_description}

指导原则：
1. 用轻松、游戏化的语气引导用户
2. 不要直接给答案，而是引导用户自己完成
3. 提供具体、可操作的步骤
4. 如果用户说不会做，提供示例
5. 保持鼓励和支持的态度

回复格式：
🎯 {task_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{task_intro}

{step_by_step_guidance}

💡 小提示：{hint}

[开始任务] [查看示例] [跳过此任务]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

TASK_INTRO_TEMPLATE = """
欢迎来到【{stage_name}】！
在这个阶段，你将{stage_description}。

准备好了吗？让我们开始吧！
"""

# ==================== 任务完成反馈提示词模板 ====================

TASK_COMPLETION_TEMPLATE = """
✨ 任务完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

太棒了，{user_name}！你完成了「{task_name}」

📈 获得经验值：+{exp_gained}
{level_up_section}
{achievements_section}
{stage_complete_section}

💡 你知道吗？
{fun_fact}

{next_task_section}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

LEVEL_UP_SECTION_TEMPLATE = """
🎉 升级了！Lv.{old_level} → Lv.{new_level}
   新称号：{new_title}
   解锁能力：{new_ability}
"""

ACHIEVEMENT_SECTION_TEMPLATE = """
🏅 解锁成就：
{achievements_list}
"""

ACHIEVEMENT_ITEM_TEMPLATE = """   {emoji} 【{name}】{description}"""

STAGE_COMPLETE_SECTION_TEMPLATE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎊 阶段完成！

你完成了【{stage_name}】！
获得称号：【{reward_title}】
解锁能力：{reward_ability}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

NEXT_TASK_SECTION_TEMPLATE = """
💡 你知道吗？
这个技能可以用来自动整理：
- 下载文件夹
- 照片库
- 项目文档

下一任务：{next_task_name} → [开始] [休息一下]
"""

# ==================== 错误引导提示词模板 ====================

ERROR_GUIDANCE_TEMPLATE = """
{user_name}，看起来遇到了一点小状况 😅

没关系的！错误也是学习的一部分。

问题：{error_description}

让我们来解决它：
{troubleshooting_steps}

💡 记住：
- 随时可以问我"帮助"
- 可以选择"跳过此任务"
- 做错了随时可以重来

需要我演示一下吗？[看演示] [再试一次] [跳过]
"""

COMMON_ERRORS = {
    "file_not_found": {
        "description": "找不到指定的文件",
        "steps": [
            "检查文件名是否拼写正确",
            "确认文件在当前目录",
            "或者提供完整的文件路径"
        ]
    },
    "permission_denied": {
        "description": "没有权限执行操作",
        "steps": [
            "检查文件是否被其他程序占用",
            "确认有足够的权限",
            "尝试换一个文件或目录"
        ]
    },
    "tool_not_available": {
        "description": "所需的工具暂不可用",
        "steps": [
            "先尝试其他任务",
            "联系管理员开启相关权限",
            "或者跳过此任务稍后完成"
        ]
    },
    "network_error": {
        "description": "网络连接问题",
        "steps": [
            "检查网络连接",
            "稍后重试",
            "或者尝试离线任务"
        ]
    }
}

# ==================== 成就解锁提示词模板 ====================

ACHIEVEMENT_UNLOCK_TEMPLATE = """
🏆 成就解锁！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    {achievement_emoji}
  【{achievement_name}】

{achievement_description}

稀有度：{rarity_display}
解锁时间：{unlock_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{secret_note}

你已经解锁了 {unlocked_count}/{total_count} 个成就！
[查看所有成就] [继续学习]
"""

RARITY_DISPLAY = {
    "common": "⭐ 普通",
    "rare": "✨ 稀有", 
    "epic": "🌟 史诗",
    "legendary": "💫 传说",
    "secret": "🔮 隐藏"
}

SECRET_ACHIEVEMENT_NOTE = """
✨ 这是一个隐藏成就！
{hidden_hint}
"""

# ==================== 进度展示提示词模板 ====================

PROGRESS_DISPLAY_TEMPLATE = """
🦐 {user_name} 的成长进度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{title} | Lv.{level} | {exp}/{next_level_exp} EXP
{exp_bar}
🔥 连续学习 {streak_days} 天 | 总共学习 {total_days} 天

{stages_section}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 已获得 {achievement_count} 个成就
📊 总进度 {overall_percentage}%

[继续学习] [查看成就] [今日提示]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

STAGE_PROGRESS_TEMPLATE = """
{emoji} {name} {status_icon}
{progress_bar} {percentage}%
{completed}/{total} 任务
"""

STAGE_STATUS_ICONS = {
    "completed": "✓",
    "current": "→",
    "locked": "🔒",
    "available": "○"
}

# ==================== 欢迎界面提示词模板 ====================

WELCOME_NEW_USER_TEMPLATE = """
🦐 欢迎来到「虾的养成计划」！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你好，{user_name}！我是你的养成导师。

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
"""

WELCOME_RETURNING_USER_TEMPLATE = """
🦐 欢迎回来，{user_name}！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

好久不见！你已连续学习 {streak_days} 天 🔥

📚 当前进度：
   阶段：{stage_name} {stage_emoji}
   任务：{task_name}
   等级：Lv.{level} {title}

💡 今天想做什么？

[继续学习] [查看进度] [查看成就]
[换个任务] [今日提示] [帮助]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ==================== 帮助引导提示词模板 ====================

HELP_MENU_TEMPLATE = """
❓ 帮助中心
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你好！我是虾的养成计划的养成导师。

📚 常用指令：
   开始养成 - 进入Skill主界面
   当前任务 - 查看当前任务
   查看进度 - 查看学习进度
   我的成就 - 查看已获得成就
   帮助 - 显示此帮助信息

💡 学习技巧：
   • 每个任务都有小提示，可以输入「帮助」查看
   • 任务可以跳过，但建议尽量完成
   • 连续学习有额外经验值奖励
   • 完成阶段有额外奖励

❓ 遇到问题？
   在当前任务中输入「帮助」获取具体指导
   或者告诉我你遇到了什么困难

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

TASK_HELP_TEMPLATE = """
💡 任务帮助：{task_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{task_description}

📋 任务指引：
{instructions}

💬 小贴士：
{hints}

{example_section}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[开始任务] [跳过此任务] [继续问]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

EXAMPLE_SECTION_TEMPLATE = """
📝 示例：
{example}
"""

# ==================== 每日提示提示词模板 ====================

DAILY_TIPS = [
    "试试让AI帮你整理邮件，使用 read 工具读取邮件内容",
    "设置一个定时任务，每天早上自动获取天气信息",
    "创建一个文件模板，让AI帮你填充内容",
    "用 web_search 查找最新资讯，制作每日简报",
    "尝试用 exec 执行一些常用命令，观察输出",
    "创建一个简单的 todo 列表，让AI帮你管理",
    "试试让AI帮你格式化文本或转换文件格式",
    "探索一下你的 workspace，看看有什么可以整理的",
    "创建一个简单的 markdown 文档，练习文档操作",
    "用 edit 工具修改文件，体验自动化编辑的威力"
]

DAILY_TIP_TEMPLATE = """
💡 每日提示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{tip}

试试输入相关的指令，开始你的练习！

[开始任务] [查看更多提示] [返回主菜单]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ==================== 系统消息模板 ====================

STREAK_BROKEN_TEMPLATE = """
💔 连续学习中断了
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

哎呀，你昨天没有来学习。
连续 {previous_streak} 天的记录重置了。

不过没关系！今天就重新开始吧。
每一小步都是进步 💪

[继续学习] [查看进度]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

STREAK_CONTINUE_TEMPLATE = """
🔥 连续学习第 {streak_days} 天！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

继续保持！连续学习有额外经验值奖励。

当前加成：+{bonus_percentage}%

[继续学习]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

LEVEL_UP_NOTIFICATION_TEMPLATE = """
🎉 恭喜升级！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lv.{old_level} {old_title}
        ↓
Lv.{new_level} {new_title}

🎁 解锁新能力：{new_ability}

继续加油，顶级虾在等着你！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ==================== 工具函数 ====================

def format_task_guidance(user_name: str, stage_name: str, stage_emoji: str,
                         task_name: str, level: int, streak_days: int,
                         task_description: str, hints: list) -> str:
    """格式化任务引导"""
    return TASK_GUIDANCE_TEMPLATE.format(
        user_name=user_name,
        stage_name=stage_name,
        stage_emoji=stage_emoji,
        task_name=task_name,
        level=level,
        streak_days=streak_days,
        task_description=task_description,
        task_intro="",
        step_by_step_guidance="",
        hint=hints[0] if hints else "相信自己，你可以的！"
    )

def format_completion_feedback(user_name: str, task_name: str, exp_gained: int,
                               level_up: bool = False, old_level: int = None,
                               new_level: int = None, new_title: str = "",
                               new_ability: str = "", achievements: list = None,
                               stage_complete: bool = False, stage_name: str = "",
                               reward_title: str = "", reward_ability: str = "",
                               next_task_name: str = "") -> str:
    """格式化完成反馈"""
    level_up_section = ""
    if level_up:
        level_up_section = LEVEL_UP_SECTION_TEMPLATE.format(
            old_level=old_level,
            new_level=new_level,
            new_title=new_title,
            new_ability=new_ability
        )
    
    achievements_section = ""
    if achievements:
        ach_list = "\n".join([
            ACHIEVEMENT_ITEM_TEMPLATE.format(
                emoji=a.get('emoji', '🏅'),
                name=a.get('name', '未知成就'),
                description=a.get('description', '')
            ) for a in achievements
        ])
        achievements_section = ACHIEVEMENT_SECTION_TEMPLATE.format(
            achievements_list=ach_list
        )
    
    stage_section = ""
    if stage_complete:
        stage_section = STAGE_COMPLETE_SECTION_TEMPLATE.format(
            stage_name=stage_name,
            reward_title=reward_title,
            reward_ability=reward_ability
        )
    
    next_section = ""
    if next_task_name:
        next_section = NEXT_TASK_SECTION_TEMPLATE.format(
            next_task_name=next_task_name
        )
    
    return TASK_COMPLETION_TEMPLATE.format(
        user_name=user_name,
        task_name=task_name,
        exp_gained=exp_gained,
        level_up_section=level_up_section,
        achievements_section=achievements_section,
        stage_complete_section=stage_section,
        fun_fact="完成任务的乐趣在于学习和成长！",
        next_task_section=next_section
    )

def format_achievement_unlock(achievement_name: str, achievement_emoji: str,
                              description: str, rarity: str, unlocked_count: int,
                              total_count: int, is_secret: bool = False,
                              hidden_hint: str = "") -> str:
    """格式化成就解锁"""
    rarity_display = RARITY_DISPLAY.get(rarity, "⭐ 普通")
    secret_note = ""
    if is_secret:
        secret_note = SECRET_ACHIEVEMENT_NOTE.format(hidden_hint=hidden_hint)
    
    return ACHIEVEMENT_UNLOCK_TEMPLATE.format(
        achievement_emoji=achievement_emoji,
        achievement_name=achievement_name,
        achievement_description=description,
        rarity_display=rarity_display,
        unlock_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
        secret_note=secret_note,
        unlocked_count=unlocked_count,
        total_count=total_count
    )

def format_error_guidance(user_name: str, error_type: str) -> str:
    """格式化错误引导"""
    error_info = COMMON_ERRORS.get(error_type, {
        "description": "发生了未知错误",
        "steps": ["请稍后再试", "或者联系管理员"]
    })
    
    steps_text = "\n".join(f"{i+1}. {step}" for i, step in enumerate(error_info["steps"]))
    
    return ERROR_GUIDANCE_TEMPLATE.format(
        user_name=user_name,
        error_description=error_info["description"],
        troubleshooting_steps=steps_text
    )

# 导入datetime用于时间格式化
from datetime import datetime
