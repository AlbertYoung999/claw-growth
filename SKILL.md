# 虾的养成计划 (Shrimp Growth Plan)

一个交互式OpenClaw学习Skill，通过游戏化任务引导用户从小白成长为顶级虾。

## 基本信息

- **名称**: shrimp-growth
- **版本**: 1.0.0
- **描述**: 🦐 游戏化OpenClaw学习系统，5个阶段52个任务，边玩边学成为顶级虾
- **作者**: OpenClaw Team
- **分类**: 教育/入门

## 依赖声明

```yaml
dependencies:
  tools:
    - feishu_im_user_message      # 消息发送
    - feishu_drive_file           # 文件操作
    - feishu_create_doc           # 文档创建
    - feishu_update_doc           # 文档更新
    - feishu_fetch_doc            # 文档读取
    - web_search                  # 网络搜索
    - web_fetch                   # 网页获取
    - exec                        # 命令执行
    - read/write/edit             # 文件操作
  skills:
    - feishu-create-doc           # 飞书文档创建
    - feishu-update-doc           # 飞书文档更新
    - feishu-fetch-doc            # 飞书文档获取
```

## 权限配置

```yaml
permissions:
  file_system:
    - path: memory/shrimp_growth/
      access: read_write
    - path: /tmp/shrimp_growth/
      access: read_write
  network:
    - allow: web_search
    - allow: web_fetch
  user_data:
    - progress_store
    - achievement_store
```

## 路由配置

```yaml
routes:
  # 主入口
  - pattern: "开始养成|虾的养成|我要学习|新手入门"
    action: start_skill
    description: Skill主入口
    
  - pattern: "查看进度|我的进度|成长进度"
    action: show_progress
    description: 展示用户当前进度
    
  - pattern: "当前任务|继续学习|下一步"
    action: get_current_task
    description: 获取当前任务详情
    
  - pattern: "完成任务|任务完成|我做好了"
    action: complete_task
    description: 标记当前任务完成
    
  - pattern: "我的成就|查看成就|徽章"
    action: show_achievements
    description: 展示已获得成就
    
  - pattern: "帮助|我需要帮助|怎么做"
    action: help_user
    description: 获取任务引导帮助
    
  - pattern: "跳过|跳过任务|下一个"
    action: skip_task
    description: 跳过当前任务
    
  - pattern: "重新开始|重置进度|从头开始"
    action: reset_progress
    description: 重置用户进度（需确认）
    
  # 阶段切换
  - pattern: "孵化期|stage1|第一阶段"
    action: switch_stage
    params: { stage: "stage1" }
    
  - pattern: "工兵期|stage2|第二阶段"
    action: switch_stage
    params: { stage: "stage2" }
    
  - pattern: "建筑师期|stage3|第三阶段"
    action: switch_stage
    params: { stage: "stage3" }
    
  - pattern: "架构师期|stage4|第四阶段"
    action: switch_stage
    params: { stage: "stage4" }
    
  - pattern: "顶级虾|stage5|第五阶段"
    action: switch_stage
    params: { stage: "stage5" }
    
  # 默认处理
  - pattern: ".*"
    action: default_handler
    description: 默认处理，尝试理解用户意图
```

## 数据结构

### 用户进度 (UserProgress)

```json
{
  "user_id": "string",
  "user_name": "string",
  "current_stage": "stage1|stage2|stage3|stage4|stage5",
  "current_task": "task_id",
  "completed_tasks": ["task1", "task2"],
  "achievements": ["first_talk", "file_master"],
  "exp": 350,
  "level": 5,
  "streak_days": 3,
  "total_days": 15,
  "created_at": "2026-03-13",
  "last_active": "2026-03-13",
  "settings": {
    "daily_reminder": true,
    "notification_enabled": true
  },
  "stats": {
    "tasks_completed": 12,
    "tasks_skipped": 1,
    "help_requested": 5
  }
}
```

### 阶段定义 (Stage)

```json
{
  "stage_id": "stage1",
  "name": "孵化期",
  "emoji": "🥚",
  "description": "学会和AI对话，完成基础操作",
  "duration_days": 3,
  "tasks": ["task1", "task2", "task3"],
  "unlock_requirement": null,
  "reward": {
    "title": "初级虾仔",
    "exp": 100,
    "ability": "批量重命名文件"
  }
}
```

### 任务定义 (Task)

```json
{
  "task_id": "task1",
  "stage_id": "stage1",
  "name": "破冰对话",
  "description": "完成第一次与AI的对话",
  "instructions": "告诉我你的名字，随便说点什么",
  "hints": ["直接说话就行", "比如'你好'或者'今天天气怎样'"],
  "validation": {
    "type": "message_count",
    "threshold": 1
  },
  "reward": {
    "exp": 20,
    "achievement": "first_talk"
  },
  "estimated_time": "5分钟",
  "difficulty": "easy"
}
```

### 成就定义 (Achievement)

```json
{
  "achievement_id": "first_talk",
  "name": "破壳而出",
  "emoji": "🥚",
  "description": "完成第一课",
  "condition": {
    "type": "task_complete",
    "task_id": "task1"
  },
  "rarity": "common",
  "secret": false
}
```

## 核心模块

### 1. 用户进度管理 (progress_manager.py)

```python
class ProgressManager:
    """管理用户学习进度"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.data_dir = "memory/shrimp_growth/"
        
    def get_progress(self) -> UserProgress:
        """获取用户进度"""
        
    def save_progress(self, progress: UserProgress) -> bool:
        """保存用户进度"""
        
    def init_new_user(self, user_name: str) -> UserProgress:
        """初始化新用户"""
        
    def update_last_active(self):
        """更新最后活跃时间"""
        
    def check_streak(self) -> int:
        """检查连续学习天数"""
```

### 2. 任务调度模块 (task_scheduler.py)

```python
class TaskScheduler:
    """任务调度与管理"""
    
    def get_current_task(self, user_id: str) -> Task:
        """获取当前任务"""
        
    def complete_task(self, user_id: str, task_id: str) -> CompletionResult:
        """完成任务"""
        
    def get_next_task(self, user_id: str) -> Task:
        """获取下一个任务"""
        
    def skip_task(self, user_id: str, task_id: str) -> bool:
        """跳过任务"""
        
    def validate_task_completion(self, task_id: str, context: dict) -> bool:
        """验证任务是否完成"""
```

### 3. 成就系统 (achievement_system.py)

```python
class AchievementSystem:
    """成就检查与解锁"""
    
    def check_achievements(self, user_id: str) -> list[Achievement]:
        """检查可解锁的成就"""
        
    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        """解锁成就"""
        
    def get_user_achievements(self, user_id: str) -> list[Achievement]:
        """获取用户所有成就"""
        
    def check_condition(self, condition: dict, progress: UserProgress) -> bool:
        """检查成就是否满足条件"""
```

### 4. 经验值计算 (exp_calculator.py)

```python
class ExpCalculator:
    """经验值与等级计算"""
    
    LEVELS = {
        1: 0,
        2: 100,
        3: 250,
        4: 450,
        5: 700,
        6: 1000,
        7: 1350,
        8: 1750,
        9: 2200,
        10: 2700
    }
    
    def calculate_exp_gain(self, task: Task, bonus: dict = None) -> int:
        """计算任务完成获得的经验值"""
        
    def get_level(self, exp: int) -> int:
        """根据经验值计算等级"""
        
    def get_level_progress(self, exp: int) -> tuple[int, int, int]:
        """获取当前等级进度 (当前等级, 当前经验, 升级所需)"""
        
    def check_level_up(self, old_exp: int, new_exp: int) -> tuple[bool, int]:
        """检查是否升级"""
```

## 关键函数

### start_skill(user_id: str, user_name: str) -> Response

Skill主入口，根据用户状态返回相应的欢迎界面或任务界面。

```python
def start_skill(user_id: str, user_name: str) -> Response:
    progress = get_or_create_progress(user_id, user_name)
    
    if is_new_user(progress):
        return render_welcome_screen(user_name)
    else:
        return render_main_dashboard(progress)
```

### get_current_task(user_id: str) -> TaskResponse

获取用户当前任务的详细信息和引导。

```python
def get_current_task(user_id: str) -> TaskResponse:
    progress = load_progress(user_id)
    task = task_registry.get(progress.current_task)
    hints = get_contextual_hints(task, progress)
    
    return {
        "task": task,
        "progress": calculate_task_progress(progress),
        "hints": hints,
        "can_skip": can_skip_task(progress, task)
    }
```

### complete_task(user_id: str, task_id: str = None) -> CompletionResponse

标记任务完成，计算奖励，检查成就。

```python
def complete_task(user_id: str, task_id: str = None) -> CompletionResponse:
    progress = load_progress(user_id)
    task = validate_task(progress, task_id)
    
    # 更新进度
    progress.completed_tasks.append(task.id)
    progress.current_task = get_next_task_id(progress)
    
    # 计算奖励
    exp_gain = exp_calculator.calculate_exp_gain(task)
    old_level = progress.level
    progress.exp += exp_gain
    progress.level = exp_calculator.get_level(progress.exp)
    
    # 检查成就
    new_achievements = achievement_system.check_achievements(progress)
    for ach in new_achievements:
        achievement_system.unlock_achievement(user_id, ach.id)
        progress.achievements.append(ach.id)
    
    # 检查阶段完成
    stage_complete = check_stage_completion(progress)
    if stage_complete:
        unlock_next_stage(progress)
    
    save_progress(progress)
    
    return {
        "success": True,
        "exp_gained": exp_gain,
        "level_up": progress.level > old_level,
        "new_level": progress.level if progress.level > old_level else None,
        "new_achievements": new_achievements,
        "stage_completed": stage_complete,
        "next_task": progress.current_task
    }
```

### check_achievements(user_id: str) -> list[Achievement]

检查并返回用户新解锁的成就。

```python
def check_achievements(user_id: str) -> list[Achievement]:
    progress = load_progress(user_id)
    unlocked = []
    
    for achievement in achievement_registry.get_all():
        if achievement.id not in progress.achievements:
            if achievement_system.check_condition(achievement.condition, progress):
                unlocked.append(achievement)
    
    return unlocked
```

### show_progress(user_id: str) -> ProgressView

生成可视化的进度展示。

```python
def show_progress(user_id: str) -> ProgressView:
    progress = load_progress(user_id)
    stages = stage_registry.get_all()
    
    stage_progress = []
    for stage in stages:
        completed = sum(1 for t in stage.tasks if t in progress.completed_tasks)
        stage_progress.append({
            "stage": stage,
            "completed": completed,
            "total": len(stage.tasks),
            "percentage": int(completed / len(stage.tasks) * 100),
            "unlocked": is_stage_unlocked(progress, stage.id)
        })
    
    return {
        "user": progress.user_name,
        "level": progress.level,
        "exp": progress.exp,
        "title": get_title_by_level(progress.level),
        "streak_days": progress.streak_days,
        "total_days": progress.total_days,
        "stage_progress": stage_progress,
        "overall_percentage": calculate_overall_progress(progress),
        "achievements_count": len(progress.achievements)
    }
```

### help_user(user_id: str, context: str = None) -> HelpResponse

根据当前任务提供上下文相关的帮助。

```python
def help_user(user_id: str, context: str = None) -> HelpResponse:
    progress = load_progress(user_id)
    task = task_registry.get(progress.current_task)
    
    hints = task.hints
    if context:
        hints = filter_relevant_hints(task.hints, context)
    
    # 记录帮助请求
    progress.stats.help_requested += 1
    save_progress(progress)
    
    return {
        "task_name": task.name,
        "general_hints": hints,
        "specific_guidance": generate_guidance(task, context),
        "example": task.example if hasattr(task, 'example') else None,
        "can_demo": task.can_demo if hasattr(task, 'can_demo') else False
    }
```

## 提示词模板

### 任务引导提示词 (task_guidance_template)

```markdown
你是「虾的养成计划」的养成导师 🦐

当前用户状态：
- 用户名：{{user_name}}
- 当前阶段：{{stage_name}} {{stage_emoji}}
- 当前任务：{{task_name}}
- 等级：{{level}}级
- 连续学习：{{streak_days}}天

任务信息：
{{task_description}}

指导原则：
1. 用轻松、游戏化的语气引导用户
2. 不要直接给答案，而是引导用户自己完成
3. 提供具体、可操作的步骤
4. 如果用户说不会做，提供示例
5. 保持鼓励和支持的态度

回复格式：
🎯 {{task_name}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{task_intro}}

{{step_by_step_guidance}}

💡 小提示：{{hint}}

[开始任务] [查看示例] [跳过此任务]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 任务完成反馈提示词 (task_completion_template)

```markdown
✨ 任务完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

太棒了，{{user_name}}！你完成了「{{task_name}}」

📈 获得经验值：+{{exp_gained}}
{{#if level_up}}
🎉 升级了！Lv.{{old_level}} → Lv.{{new_level}}
{{/if}}
{{#each new_achievements}}
🏅 解锁成就：【{{name}}】{{emoji}}
{{/each}}
{{#if stage_complete}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎊 阶段完成！

你完成了【{{stage_name}}】！
获得称号：【{{new_title}}】
解锁能力：{{new_ability}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{/if}}

💡 你知道吗？
{{fun_fact}}

{{#if next_task}}
下一任务：{{next_task_name}} → [开始] [休息一下]
{{/if}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 错误引导提示词 (error_guidance_template)

```markdown
{{user_name}}，看起来遇到了一点小状况 😅

没关系的！错误也是学习的一部分。

问题：{{error_description}}

让我们来解决它：
{{troubleshooting_steps}}

💡 记住：
- 随时可以问我"帮助"
- 可以选择"跳过此任务"
- 做错了随时可以重来

需要我演示一下吗？[看演示] [再试一次] [跳过]
```

### 成就解锁提示词 (achievement_unlock_template)

```markdown
🏆 成就解锁！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    {{achievement_emoji}}
  【{{achievement_name}}】

{{achievement_description}}

稀有度：{{rarity}}
解锁时间：{{unlock_time}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{#if is_secret}}
✨ 这是一个隐藏成就！
{{/if}}

你已经解锁了 {{unlocked_count}}/{{total_count}} 个成就！
[查看所有成就] [继续学习]
```

### 进度展示提示词 (progress_display_template)

```markdown
🦐 {{user_name}} 的成长进度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{user_title}} | Lv.{{level}} | {{exp}}/{{next_level_exp}} EXP
🔥 连续学习 {{streak_days}} 天 | 总共学习 {{total_days}} 天

{{#each stages}}
{{emoji}} {{name}} {{#if is_current}}→{{/if}}
{{progress_bar}}
{{completed}}/{{total}} 任务 {{#if locked}}🔒{{/if}}
{{/each}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 已获得 {{achievement_count}} 个成就
📊 总进度 {{overall_percentage}}%

[继续学习] [查看成就] [今日提示]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 课程结构

### Stage 1: 孵化期 🥚 (3个任务)
1. **破冰对话** - 完成第一次对话
2. **文件小助手** - 创建并读取文件
3. **第一次自动化** - 列出文件夹内容

### Stage 2: 工兵期 🦐 (3个任务)
4. **每日晨报** - 使用网络搜索
5. **文件整理机器人** - 批量文件操作
6. **定时任务** - 设置自动化任务

### Stage 3: 建筑师期 🏗️ (3个任务)
7. **我的第一个Skill** - 创建简单Skill
8. **API连接器** - 集成外部API
9. **智能家居控制** - 控制真实设备

### Stage 4: 架构师期 🎭 (3个任务)
10. **组建AI团队** - 多Agent配置
11. **任务委派** - 工作流编排
12. **复杂项目实战** - 完成真实项目

### Stage 5: 顶级虾 👑 (3个任务)
13. **云端部署** - 服务器部署
14. **分享与传承** - 发布Skill
15. **虾王挑战** - 解决真实问题

## 成就列表

| 成就ID | 名称 | 条件 | 稀有度 |
|--------|------|------|--------|
| first_talk | 破壳而出 | 完成task1 | 普通 |
| auto_master | 自动化新手 | 完成stage1 | 普通 |
| skill_builder | 建筑许可证 | 完成task7 | 稀有 |
| team_leader | 团队领袖 | 完成task10 | 稀有 |
| shrimp_king | 虾王认证 | 完成所有任务 | 传说 |
| streak_7 | 一周坚持 | 连续7天学习 | 普通 |
| streak_30 | 月度达人 | 连续30天学习 | 稀有 |
| helper | 热心虾 | 帮助其他用户 | 稀有 |
| creator | 创造者 | 发布3个Skill | 史诗 |
| speed_runner | 速通玩家 | 7天内完成 | 史诗 |

## 使用示例

```
用户：我想学习OpenClaw
AI：欢迎加入「虾的养成计划」！我是你的养成导师 🦐

我会一步步带你从小白成长为顶级虾。
现在，让我们开始第一课？

[开始第一课] [先看看我有什么] [以后再说]

---

用户：查看进度
AI：🦐 Albert 的成长进度
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【孵化期】■■■■■■■■■■ 100% ✓
【工兵期】■■■■■■□□□□ 60%  →
【建筑师】🔒 未解锁
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

用户：当前任务
AI：🎯 当前任务：让AI帮你整理桌面文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

任务说明：
把你桌面上乱七八糟的文件按类型整理好

步骤：
1. 告诉AI你的桌面路径
2. 定义分类规则（按日期？按类型？）
3. 执行整理

[开始任务] [查看示例] [跳过此任务]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
