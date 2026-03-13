# 关键场景处理逻辑

本文档描述「虾的养成计划」Skill的关键场景处理逻辑。

## 1. 新用户首次进入

### 场景描述
用户第一次使用Skill，没有任何进度数据。

### 处理流程

```
用户输入："我想学习OpenClaw" / "开始养成"
    ↓
调用 start_skill()
    ↓
检查用户进度（不存在）
    ↓
初始化新用户 ProgressManager.init_new_user()
    ↓
渲染欢迎界面（WELCOME_NEW_USER_TEMPLATE）
    ↓
等待用户选择：
    - [开始第一课] → 调用 get_current_task()
    - [先看看我有什么] → 显示Skill介绍
    - [以后再说] → 结束会话
```

### 关键代码

```python
def start_skill(user_id: str, user_name: str) -> str:
    progress = progress_manager.get_or_create_progress(user_name)
    
    if progress_manager.is_new_user(progress):
        return render_welcome_screen()  # 新用户欢迎
    else:
        return render_main_dashboard()  # 老用户主界面
```

## 2. 用户完成任务

### 场景描述
用户完成当前任务，需要更新进度、计算奖励、检查升级和成就。

### 处理流程

```
用户输入："我完成了" / "任务完成"
    ↓
调用 complete_task(task_id=None)
    ↓
获取当前进度和任务
    ↓
验证任务完成条件 validate_task_completion()
    ↓
更新进度（completed_tasks, current_task）
    ↓
计算经验值 _calculate_task_exp()
    ↓
检查升级 check_level_up()
    ↓
检查新成就 check_all_achievements()
    ↓
解锁新成就 unlock_achievement()
    ↓
检查阶段完成 _check_stage_completion()
    ↓
保存进度 save_progress()
    ↓
渲染完成反馈 _render_completion_feedback()
```

### 经验值计算逻辑

```python
def _calculate_task_exp(self, task: Task, context: Dict = None) -> int:
    base_exp = task.reward.get("exp", 20)
    
    # 难度加成
    difficulty_bonus = {
        "easy": 0,
        "medium": 10,
        "hard": 25,
        "expert": 50
    }
    bonus = difficulty_bonus.get(task.difficulty, 0)
    
    return base_exp + bonus
```

### 升级检测逻辑

```python
# 完成任务后
old_level = progress.level
progress.exp += exp_gain
new_level = exp_calculator.get_level(progress.exp)

if new_level > old_level:
    progress.level = new_level
    level_up_message = LevelUpReward.render_level_up_message(old_level, new_level)
```

## 3. 连续学习天数计算

### 场景描述
用户每天学习，需要计算连续学习天数和奖励。

### 处理流程

```
用户进入Skill
    ↓
调用 check_and_update_streak()
    ↓
获取今天日期和上次记录日期
    ↓
计算日期差：
    - diff == 0: 今天已记录，不操作
    - diff == 1: 连续学习，streak_days += 1
    - diff > 1: 中断，streak_days = 1
    ↓
更新 last_streak_date
    ↓
保存进度
```

### 关键代码

```python
def check_and_update_streak(self) -> int:
    progress = self.get_progress()
    today = datetime.now().date()
    last_date = datetime.fromisoformat(progress.last_streak_date).date()
    
    diff = (today - last_date).days
    
    if diff == 0:
        return progress.streak_days  # 今天已记录
    elif diff == 1:
        progress.streak_days += 1    # 连续学习
        progress.total_days += 1
    else:
        progress.streak_days = 1     # 中断，重新开始
        progress.total_days += 1
    
    progress.last_streak_date = datetime.now().isoformat()
    self.save_progress(progress)
    
    return progress.streak_days
```

## 4. 成就解锁

### 场景描述
用户达成成就条件，需要解锁成就并通知用户。

### 处理流程

```
任务完成/阶段完成/其他条件触发
    ↓
调用 check_all_achievements()
    ↓
遍历所有未解锁成就
    ↓
对每个成就调用 _check_condition()
    ↓
收集满足条件的成就列表
    ↓
逐个解锁 unlock_achievement()
    ↓
添加到用户 progress.achievements
    ↓
发放成就奖励经验值
    ↓
渲染成就解锁提示
```

### 成就条件检查

```python
def _check_condition(self, condition: Dict, progress: UserProgress) -> bool:
    condition_type = condition.get("type", "")
    
    checkers = {
        "task_complete": lambda c, p: c["task_id"] in p.completed_tasks,
        "stage_complete": lambda c, p: all(
            t in p.completed_tasks for t in get_stage_tasks(c["stage_id"])
        ),
        "streak_days": lambda c, p: p.streak_days >= c["days"],
        "all_achievements": lambda c, p: len(p.achievements) >= TOTAL_ACHIEVEMENTS,
        # ... 更多条件
    }
    
    checker = checkers.get(condition_type)
    return checker(condition, progress) if checker else False
```

## 5. 阶段完成检测

### 场景描述
用户完成一个阶段的所有任务，需要检测并给予阶段奖励。

### 处理流程

```
任务完成
    ↓
调用 _check_stage_completion(stage_id)
    ↓
获取阶段的所有任务
    ↓
检查每个任务状态：
    - 已完成 ✓
    - 已跳过 ✓
    - 未完成 ✗
    ↓
如果全部完成/跳过：
    - 标记阶段完成
    - 发放阶段奖励
    - 解锁下一阶段
```

## 6. 用户请求帮助

### 场景描述
用户在任务中遇到困难，请求帮助。

### 处理流程

```
用户输入："帮助" / "我不会" / 具体问题
    ↓
调用 help_user(context)
    ↓
获取当前任务信息
    ↓
根据上下文过滤相关提示
    ↓
更新 help_requested 统计
    ↓
渲染帮助文本（TASK_HELP_TEMPLATE）
    ↓
提供选项：[开始任务] [跳过] [继续问]
```

## 7. 任务跳过

### 场景描述
用户选择跳过当前任务。

### 处理流程

```
用户输入："跳过" / "跳过此任务"
    ↓
调用 skip_task(task_id)
    ↓
检查任务是否允许跳过 (task.can_skip)
    ↓
添加到 skipped_tasks 列表
    ↓
更新统计
    ↓
获取下一个任务
    ↓
更新 current_task
    ↓
保存进度
    ↓
提示用户已跳过，显示下一任务
```

## 8. 进度重置

### 场景描述
用户想要重置所有进度，重新开始。

### 处理流程

```
用户输入："重置进度" / "重新开始"
    ↓
调用 reset_progress(confirmed=False)
    ↓
显示确认提示
    ↓
用户确认：
    - 取消：返回主界面
    - 确认：调用 reset_progress(confirmed=True)
        ↓
        删除用户数据文件
        ↓
        提示重置成功
        ↓
        回到欢迎界面
```

## 9. 阶段切换

### 场景描述
用户想要切换到其他阶段（复习或查看）。

### 处理流程

```
用户输入："切换到工兵期" / "stage2"
    ↓
调用 switch_stage(stage_id)
    ↓
检查阶段是否存在
    ↓
检查阶段是否已解锁
    （至少完成一个任务或已开始）
    ↓
如果未解锁：
    - 提示需要先完成前置阶段
    ↓
如果已解锁：
    - 找到该阶段第一个未完成任务
    - 更新 current_task 和 current_stage
    - 保存进度
    - 显示该任务
```

## 10. 数据持久化

### 存储结构

```
memory/shrimp_growth/
├── {user_id_1}.json     # 用户1进度
├── {user_id_2}.json     # 用户2进度
└── ...
```

### 存储格式

```json
{
  "user_id": "user_123",
  "user_name": "用户名",
  "current_stage": "stage1",
  "current_task": "task1",
  "completed_tasks": ["task1"],
  "skipped_tasks": [],
  "achievements": ["first_talk"],
  "exp": 50,
  "level": 1,
  "streak_days": 3,
  "total_days": 5,
  "created_at": "2026-03-13T10:00:00",
  "last_active": "2026-03-13T15:30:00",
  "last_streak_date": "2026-03-13T10:00:00",
  "settings": {...},
  "stats": {...}
}
```

## 11. 错误处理

### 常见错误场景

| 错误类型 | 处理方式 |
|---------|---------|
| 用户数据损坏 | 尝试修复或重置为默认 |
| 任务不存在 | 返回友好提示，建议重置 |
| 阶段不存在 | 忽略或返回错误信息 |
| 存储失败 | 重试或提示用户检查权限 |
| 循环依赖 | 在任务定义时检查并报警 |

### 错误处理示例

```python
def get_progress(self) -> Optional[UserProgress]:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return UserProgress.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        # 数据损坏，尝试备份并重建
        self._backup_corrupted_file()
        return None
    except IOError as e:
        # 存储错误，记录日志
        logger.error(f"Failed to load progress: {e}")
        return None
```

## 12. 性能优化

### 缓存策略

```python
class ProgressManager:
    def __init__(self, user_id: str):
        self._cache = None
        self._cache_time = None
    
    def get_progress(self) -> Optional[UserProgress]:
        # 检查缓存有效性
        if self._cache and self._is_cache_valid():
            return self._cache
        
        # 从文件加载
        progress = self._load_from_file()
        self._cache = progress
        self._cache_time = time.time()
        return progress
```

### 批量操作

```python
# 批量解锁成就
def unlock_achievements_batch(self, achievement_ids: List[str]) -> List[AchievementUnlockResult]:
    results = []
    for aid in achievement_ids:
        result = self.unlock_achievement(aid)
        results.append(result)
    
    # 只保存一次
    self.progress_manager.save_progress(progress)
    return results
```
