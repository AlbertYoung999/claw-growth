# 虾的养成计划 (Shrimp Growth Plan)

🦐 一个交互式OpenClaw学习Skill，通过游戏化任务引导用户从小白成长为顶级虾。

## 功能特点

- 🎮 **游戏化学习**：将学习变成游戏，完成任务解锁新能力
- 📊 **进度可视化**：实时查看学习进度和成长轨迹
- 🏆 **成就系统**：丰富的成就等待解锁
- ⬆️ **等级体系**：10个等级，从小白到顶级虾
- 🔥 **连续学习**：连续学习奖励机制
- 💡 **智能引导**：上下文相关的帮助提示

## 快速开始

```python
from shrimp_growth import start_skill, get_current_task, complete_task

# 开始你的养成之旅
user_id = "your_user_id"
response = start_skill(user_id, user_name="你的名字")
print(response)

# 获取当前任务
task_info = get_current_task(user_id)
print(task_info)

# 完成任务
feedback = complete_task(user_id)
print(feedback)
```

## 项目结构

```
shrimp-growth/
├── SKILL.md                 # Skill主配置文件
├── __init__.py             # 包初始化
├── models.py               # 数据模型定义
├── progress_manager.py     # 用户进度管理
├── task_scheduler.py       # 任务调度管理
├── achievement_system.py   # 成就系统
├── exp_calculator.py       # 经验值计算
├── main.py                 # 主入口和API
├── templates.py            # 提示词模板
├── config.example.yaml     # 配置示例
└── examples.py             # 使用示例
```

## 课程结构

### 🥚 阶段1：孵化期 (3个任务)
1. 破冰对话 - 完成第一次对话
2. 文件小助手 - 创建并读取文件
3. 第一次自动化 - 列出文件夹内容

### 🦐 阶段2：工兵期 (3个任务)
4. 每日晨报 - 使用网络搜索
5. 文件整理机器人 - 批量文件操作
6. 定时任务 - 设置自动化任务

### 🏗️ 阶段3：建筑师期 (3个任务)
7. 我的第一个Skill - 创建简单Skill
8. API连接器 - 集成外部API
9. 智能家居控制 - 控制真实设备

### 🎭 阶段4：架构师期 (3个任务)
10. 组建AI团队 - 配置多Agent
11. 任务委派 - 设计工作流
12. 复杂项目实战 - 完成真实项目

### 👑 阶段5：顶级虾 (3个任务)
13. 云端部署 - 服务器部署
14. 分享与传承 - 发布Skill
15. 虾王挑战 - 解决真实问题

## API文档

### 快捷函数

```python
# 开始Skill
start_skill(user_id: str, user_name: str) -> str

# 获取当前任务
def get_current_task(user_id: str) -> str

# 完成任务
def complete_task(user_id: str, task_id: str = None) -> str

# 检查成就
def check_achievements(user_id: str) -> str

# 展示进度
def show_progress(user_id: str) -> str

# 帮助引导
def help_user(user_id: str, context: str = None) -> str

# 切换阶段
def switch_stage(user_id: str, stage_id: str) -> str

# 展示成就
def show_achievements(user_id: str) -> str

# 重置进度
def reset_progress(user_id: str, confirmed: bool = False) -> str
```

### ShrimpGrowthSkill 类

```python
skill = ShrimpGrowthSkill(user_id="xxx", user_name="用户名")

# 开始
response = skill.start_skill()

# 获取当前任务
task_info = skill.get_current_task()

# 完成任务
feedback = skill.complete_task(task_id=None)

# 查看进度
progress = skill.show_progress()

# 获取帮助
help_text = skill.help_user(context="具体问题")

# 切换阶段
result = skill.switch_stage(stage_id="stage2")

# 查看成就
achievements = skill.show_achievements()
```

## 数据模型

### UserProgress

```json
{
  "user_id": "xxx",
  "user_name": "用户名",
  "current_stage": "stage1",
  "current_task": "task1",
  "completed_tasks": ["task1", "task2"],
  "achievements": ["first_talk"],
  "exp": 350,
  "level": 5,
  "streak_days": 3,
  "total_days": 15,
  "created_at": "2026-03-13",
  "last_active": "2026-03-13"
}
```

## 配置

复制 `config.example.yaml` 为 `config.yaml` 并进行自定义配置。

## 路由配置

```yaml
routes:
  - pattern: "开始养成|虾的养成"
    action: start_skill
    
  - pattern: "查看进度|我的进度"
    action: show_progress
    
  - pattern: "当前任务|继续学习"
    action: get_current_task
    
  - pattern: "完成任务|任务完成"
    action: complete_task
    
  - pattern: "我的成就|查看成就"
    action: show_achievements
    
  - pattern: "帮助|我需要帮助"
    action: help_user
```

## 成就列表

| 成就 | 名称 | 条件 |
|------|------|------|
| 🥚 | 破壳而出 | 完成第一课 |
| 🦐 | 自动化新手 | 完成孵化期 |
| 🏗️ | 建筑许可证 | 发布第一个Skill |
| 👥 | 团队领袖 | 组建3人AI团队 |
| 👑 | 虾王认证 | 完成所有任务 |
| 🔥 | 一周坚持 | 连续7天学习 |
| 📅 | 月度达人 | 连续30天学习 |
| ⚡ | 速通玩家 | 7天内完成所有阶段 |

## 开发计划

- [ ] 添加更多任务类型验证
- [ ] 实现真实任务完成检测
- [ ] 添加数据分析功能
- [ ] 支持自定义课程
- [ ] 添加社区排行榜
- [ ] 实现导师-学员配对

## 贡献

欢迎提交Issue和PR！

## 许可证

MIT License
