# Trae 配置文件

> 城乡建设政策知识服务系统 - Trae IDE 配置

---

## Trae IDE 项目配置

### 项目信息

```yaml
project:
  name: 城乡建设政策知识服务系统
  version: 1.0.0
  description: 城乡建设咨询领域的政策知识服务系统
  author: 用户与AI智能体协作
  created: 2025-03-11
```

---

## 目录结构

```
d:\LMAI\001工具人mk4\
├── 00_政策法规/              # 政策知识库（核心资产）
│   ├── 国家级/
│   │   ├── 01_按部门/        # 政策原文存储
│   │   ├── 02_按效力层级/    # 索引目录
│   │   ├── 03_按业务领域/    # 索引目录
│   │   └── 内部资料/         # 内部文件
│   ├── 政策解读/
│   └── 省级/
├── core/                     # 核心系统
│   ├── intent_analyzer.py    # 意图分析
│   ├── scenario_generator.py # 场景生成器
│   ├── workflow_engine.py    # 工作流引擎
│   ├── skill_scheduler.py    # 技能调度器
│   └── learning_system.py    # 学习系统
├── adapters/                 # 数据适配器
│   ├── policy_adapter.py
│   ├── website_adapter.py
│   └── news_adapter.py
├── knowledge/                # 知识库
│   ├── policies/             # 政策文件
│   ├── cases/                # 案例库
│   ├── templates/            # 模板库
│   ├── patterns/             # 模式库
│   └── feedback/             # 反馈数据
├── outputs/                  # 输出目录
│   └── {YYYY-MM-DD}_{场景}_{项目}/
├── skills/                   # 自定义skills
├── rules/                    # 自定义rules
├── hooks/                    # 自定义hooks
├── logs/                     # 日志
│   ├── interactions/         # 交互日志
│   ├── workflows/            # 工作流日志
│   └── learning/             # 学习日志
├── config/                   # 配置
│   ├── system_config.yaml
│   ├── skill_registry.json
│   └── data_sources.yaml
├── agents.md                 # Agents配置
├── claude.md                 # Claude配置
├── claude.local.md           # Claude本地配置
├── trae.md                   # Trae配置
├── main.py                   # 主入口
├── auto_update.py            # 自动更新
├── SYSTEM_DESIGN.md          # 系统设计文档
└── README.md                 # 项目说明
```

---

## Trae IDE 配置

### .trae 目录

```
.trae/
├── rules/
│   └── project_rules.md      # 项目规则
└── settings.json             # IDE设置
```

### 项目规则

```markdown
# .trae/rules/project_rules.md

## 项目规则

### 1. 文件命名规范

#### 政策文件命名
格式：`[发文号]_[发文机关]_[政策名称]_[发布日期].md`

示例：
- `国办发〔2024〕52号_国务院办公厅_关于优化完善地方政府专项债券管理机制的意见_20241225.md`

#### 文档文件命名
格式：`[日期]_[类型]_[标题]_[版本]_[状态].md`

示例：
- `2026-02-21_政策解读_专项债券政策_V1.0_待审核.md`

### 2. 元数据规范

所有政策文件必须包含元数据：

```yaml
---
file_number: 国办发〔2024〕52号
publishing_agency: 国务院办公厅
policy_name: 关于优化完善地方政府专项债券管理机制的意见
publishing_date: 20241225
status: 现行有效
keywords:
  - 专项债券
  - 地方政府
---
```

### 3. 代码规范

- Python代码遵循PEP 8规范
- 使用4空格缩进
- 函数和变量使用snake_case命名
- 类使用PascalCase命名

### 4. Git提交规范

提交信息格式：`<type>: <message>`

类型：
- feat: 新增功能
- fix: 修复bug
- docs: 文档更新
- refactor: 代码重构
- test: 测试相关
- chore: 构建/工具相关

### 5. 工作流规则

- 完成任务后必须运行验证命令
- 重要更改必须更新README
- 使用Git进行版本控制
```

---

## Skills集成

### 可用Skills路径

```
C:\Users\Administrator\.trae-cn\skills\
```

### 核心Skills

| Skill | 功能 | 用途 |
|-------|------|------|
| `research-lookup` | 政策研究 | 政策匹配、信息检索 |
| `perplexity-search` | 实时搜索 | 最新政策、新闻 |
| `office` | 文档生成 | 报告输出 |
| `scientific-critical-thinking` | 批判性思维 | 风险评估 |
| `verification-before-completion` | 完成前验证 | 质量检查 |
| `policy-knowledge-workflow` | 政策工作流 | 政策采集、入库 |
| `城乡建设新闻监测` | 新闻监测 | 政策动态 |

### Skills调用

在Trae IDE中，Skills通过Skill工具调用：

```
使用Skill工具调用技能
```

---

## 工作流配置

### 工作流模板

```yaml
# config/workflow_templates.yaml

workflows:
  - name: 项目谋划工作流
    id: project_planning
    triggers:
      - 谋划
      - 项目
    steps:
      - step: 1
        action: 意图分析
        skill: intent_analyzer
      - step: 2
        action: 政策匹配
        skill: research-lookup
      - step: 3
        action: 资金方案
        skill: research-lookup
      - step: 4
        action: 风险评估
        skill: scientific-critical-thinking
      - step: 5
        action: 报告生成
        skill: office
      - step: 6
        action: 质量检查
        skill: verification-before-completion

  - name: 政策研究工作流
    id: policy_research
    triggers:
      - 研究
      - 政策
    steps:
      - step: 1
        action: 意图分析
        skill: intent_analyzer
      - step: 2
        action: 政策检索
        skill: research-lookup
      - step: 3
        action: 深度分析
        skill: scientific-critical-thinking
      - step: 4
        action: 报告生成
        skill: office
```

---

## Hooks配置

### 工作流钩子

```python
# hooks/workflow_hooks.py

def on_workflow_start(workflow):
    """工作流开始时触发"""
    print(f"开始执行工作流: {workflow['name']}")
    log_workflow_start(workflow)

def on_workflow_complete(workflow, result):
    """工作流完成时触发"""
    print(f"工作流完成: {workflow['name']}")
    log_workflow_complete(workflow, result)
    update_readme()

def on_workflow_error(workflow, error):
    """工作流出错时触发"""
    print(f"工作流出错: {workflow['name']}, 错误: {error}")
    log_workflow_error(workflow, error)
    notify_user(error)
```

---

## Git集成

### Git配置

```bash
# 初始化Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/username/policy-knowledge-system.git

# 配置Git用户
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Git工作流

```bash
# 日常开发
git checkout -b feature/new-feature
git add .
git commit -m "feat: 添加新功能"
git push origin feature/new-feature

# 创建Pull Request
# 代码审查通过后合并

# 发布版本
git checkout main
git merge develop
git tag -a v1.0.0 -m "版本1.0.0"
git push origin main --tags
```

---

## 自动更新配置

### README自动更新

```python
# auto_update.py

import os
from datetime import datetime
from pathlib import Path

def update_readme():
    """自动更新README"""
    
    readme_path = Path("README.md")
    
    # 收集系统信息
    stats = {
        "total_policies": count_policies(),
        "total_scenarios": count_scenarios(),
        "total_workflows": count_workflows(),
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 生成README内容
    content = generate_readme_content(stats)
    
    # 写入README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("README已更新")

def count_policies():
    """统计政策数量"""
    policy_dir = Path("00_政策法规")
    count = 0
    for root, dirs, files in os.walk(policy_dir):
        count += len([f for f in files if f.endswith('.md')])
    return count

def count_scenarios():
    """统计场景数量"""
    return 11  # 当前有11个场景

def count_workflows():
    """统计工作流数量"""
    return 6  # 当前有6个工作流

def generate_readme_content(stats):
    """生成README内容"""
    return f"""# 城乡建设政策知识服务系统

> 本系统用于整理、存储城乡建设咨询领域的政策法规，支持项目谋划和资金匹配

---

## 系统状态

- **政策总数**: {stats['total_policies']}
- **场景总数**: {stats['total_scenarios']}
- **工作流总数**: {stats['total_workflows']}
- **最后更新**: {stats['last_update']}

---

## 快速开始

### 1. 项目谋划

```
/谋划 项目名称
```

### 2. 项目筛选

```
/筛选 项目列表
```

### 3. 政策研究

```
/研究 政策关键词
```

---

## 文档

- [系统设计文档](SYSTEM_DESIGN.md)
- [Agents配置](agents.md)
- [Claude配置](claude.md)
- [Trae配置](trae.md)

---

## 版本信息

- **版本**: v1.0.0
- **更新时间**: {stats['last_update']}
"""

if __name__ == "__main__":
    update_readme()
```

---

## 版本信息

- **版本**：v1.0.0
- **更新时间**：2025-03-11
- **状态**：配置完成
