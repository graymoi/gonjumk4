# Claude Local 配置文件

> 城乡建设政策知识服务系统 - Claude 本地配置

---

## 本地环境配置

### 项目路径

```
项目根目录：d:\LMAI\001工具人mk4\
政策库路径：d:\LMAI\001工具人mk4\00_政策法规\
输出路径：d:\LMAI\001工具人mk4\outputs\
配置路径：d:\LMAI\001工具人mk4\config\
```

### Skills路径

```
Claude Skills：C:\Users\Administrator\.claude\skills\
Agents Skills：C:\Users\Administrator\.agents\skills\
Trae Skills：C:\Users\Administrator\.trae-cn\skills\
```

---

## 知识库配置

### 政策库结构

```
00_政策法规/
├── 国家级/
│   ├── 01_按部门/           # 政策原文存储（单一来源）
│   │   ├── 发改委/
│   │   ├── 财政部/
│   │   ├── 住建部/
│   │   ├── 自然资源部/
│   │   └── ...
│   ├── 02_按效力层级/        # 索引目录
│   │   ├── 行政法规索引.md
│   │   ├── 规范性文件索引.md
│   │   └── 部门规章索引.md
│   ├── 03_按业务领域/        # 索引目录
│   │   ├── 专项债券索引.md
│   │   ├── 中央预算内投资索引.md
│   │   ├── 城市更新索引.md
│   │   └── ...
│   └── 内部资料/             # 内部文件
├── 政策解读/
│   ├── REITs/
│   ├── 专项债券/
│   ├── 城市更新/
│   └── ...
└── 省级/
    ├── 天津市/
    ├── 重庆市/
    └── ...
```

### 政策文件命名规范

**格式**：`[发文号]_[发文机关]_[政策名称]_[发布日期].md`

**示例**：
- `国办发〔2024〕52号_国务院办公厅_关于优化完善地方政府专项债券管理机制的意见_20241225.md`
- `建科〔2023〕45号_住房城乡建设部_关于推进建设工程质量检测机构资质许可工作的通知_20230510.md`

---

## 元数据规范

### 必填字段

| 字段 | 说明 | 示例 |
|------|------|------|
| file_number | 发文号 | 国办发〔2024〕52号 |
| publishing_agency | 发文机关 | 国务院办公厅 |
| policy_name | 政策名称 | 关于优化完善地方政府专项债券管理机制的意见 |
| publishing_date | 发布日期 | 20241225 |
| status | 状态 | 现行有效/已废止 |

### 可选字段

| 字段 | 说明 | 示例 |
|------|------|------|
| effective_date | 生效日期 | 20250101 |
| keywords | 关键词 | 专项债券, 地方政府 |
| business_domain | 业务领域 | 财政金融 |
| policy_type | 政策类型 | 规范性文件 |
| level | 层级 | 国家级/省级/市级 |

### 元数据模板

```yaml
---
file_number: 国办发〔2024〕52号
publishing_agency: 国务院办公厅
policy_name: 关于优化完善地方政府专项债券管理机制的意见
publishing_date: 20241225
effective_date: 20250101
status: 现行有效
keywords:
  - 专项债券
  - 地方政府
business_domain:
  - 财政金融
policy_type: 规范性文件
level: 国家级
---
```

---

## 输出配置

### 输出目录结构

```
outputs/
└── {YYYY-MM-DD}_{场景}_{项目}/
    ├── 项目谋划报告.pdf
    ├── 政策匹配报告.md
    ├── 资金方案.xlsx
    ├── 风险报告.pdf
    └── README.md
```

### 输出格式

| 文档类型 | 格式 | 用途 |
|---------|------|------|
| 正式报告 | PDF | 提交客户 |
| 工作文档 | Word | 内部编辑 |
| 数据分析 | Excel | 数据处理 |
| 宣讲材料 | PPTX | 会议宣讲 |
| 知识库文档 | Markdown | 知识库存储 |

---

## Skills配置

### 核心Skills

```json
{
  "core_skills": [
    {
      "name": "research-lookup",
      "description": "政策研究和信息检索",
      "usage": "政策匹配、资金方案"
    },
    {
      "name": "perplexity-search",
      "description": "实时网络搜索",
      "usage": "最新政策、新闻"
    },
    {
      "name": "office",
      "description": "文档生成",
      "usage": "报告输出"
    },
    {
      "name": "scientific-critical-thinking",
      "description": "批判性思维",
      "usage": "风险评估"
    },
    {
      "name": "verification-before-completion",
      "description": "完成前验证",
      "usage": "质量检查"
    }
  ]
}
```

### 政策相关Skills

```json
{
  "policy_skills": [
    {
      "name": "policy-knowledge-workflow",
      "description": "政策知识工作流",
      "usage": "政策采集、入库"
    },
    {
      "name": "城乡建设新闻监测",
      "description": "新闻监测",
      "usage": "政策动态"
    }
  ]
}
```

---

## Rules配置

### Rules路径

```
rules/
├── policy_analysis.md      # 政策分析规则
├── project_planning.md     # 项目谋划规则
├── risk_assessment.md      # 风险评估规则
├── document_format.md      # 文档格式规则
└── naming_convention.md    # 命名规范
```

### Rules示例

```markdown
# rules/policy_analysis.md

## 政策分析规则

### 1. 政策识别
- 识别政策类型（法律、行政法规、部门规章、规范性文件）
- 识别发文机关（国务院、部委、地方政府）
- 识别效力层级（国家级、省级、市级）

### 2. 政策解读
- 提取核心内容
- 明确适用范围
- 确定执行标准
- 识别申报条件

### 3. 政策关联
- 分析政策关联性
- 识别配套政策
- 建立政策图谱

### 4. 政策应用
- 评估政策适用性
- 分析申报条件
- 提供应用建议
```

---

## Hooks配置

### Hooks路径

```
hooks/
├── pre_workflow.py         # 工作流执行前钩子
├── post_workflow.py        # 工作流执行后钩子
├── on_error.py             # 错误处理钩子
└── on_learning.py          # 学习触发钩子
```

### Hooks示例

```python
# hooks/post_workflow.py

import json
from datetime import datetime
from pathlib import Path

def after_workflow_execution(workflow_result):
    """工作流执行后的钩子"""
    
    # 1. 记录交互日志
    log_path = Path("logs/interactions")
    log_path.mkdir(parents=True, exist_ok=True)
    
    log_file = log_path / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(workflow_result, f, ensure_ascii=False, indent=2)
    
    # 2. 提取学习数据
    extract_learning_data(workflow_result)
    
    # 3. 更新知识库
    update_knowledge_base(workflow_result)
    
    # 4. 自动更新README
    auto_update_readme()
    
    # 5. Git提交
    import subprocess
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"feat: 完成{workflow_result['scenario']}"])
    subprocess.run(["git", "push"])

def extract_learning_data(workflow_result):
    """提取学习数据"""
    learning_data = {
        "scenario": workflow_result.get("scenario"),
        "skills_used": workflow_result.get("skills_used", []),
        "success_rate": workflow_result.get("success_rate", 0),
        "user_feedback": workflow_result.get("user_feedback"),
        "timestamp": datetime.now().isoformat()
    }
    
    learning_path = Path("logs/learning")
    learning_path.mkdir(parents=True, exist_ok=True)
    
    learning_file = learning_path / f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(learning_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(learning_data, ensure_ascii=False) + '\n')

def update_knowledge_base(workflow_result):
    """更新知识库"""
    pass

def auto_update_readme():
    """自动更新README"""
    from auto_update import update_readme
    update_readme()
```

---

## Git配置

### Git忽略文件

```gitignore
# .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志
logs/
*.log

# 临时文件
*.tmp
*.temp

# 敏感信息
.env
secrets.yaml
credentials.json

# 输出文件（可选）
# outputs/
```

### Git工作流

```bash
# 初始化仓库
git init

# 添加远程仓库
git remote add origin https://github.com/username/repo.git

# 创建开发分支
git checkout -b develop

# 日常提交
git add .
git commit -m "feat: 添加新功能"
git push origin develop

# 创建Pull Request
# 代码审查通过后合并到main

# 发布版本
git checkout main
git merge develop
git tag -a v1.0.0 -m "版本1.0.0"
git push origin main --tags
```

---

## 日志配置

### 日志路径

```
logs/
├── interactions/           # 交互日志
│   └── {YYYYMMDD_HHMMSS}.json
├── workflows/              # 工作流日志
│   └── {YYYYMMDD}.jsonl
└── learning/               # 学习日志
    └── learning_{YYYYMMDD}.jsonl
```

### 日志格式

```json
{
  "timestamp": "2025-03-11T10:30:00",
  "user_input": "我想谋划一个老旧小区改造项目",
  "intent": "项目谋划",
  "scenario": "老旧小区改造项目谋划",
  "workflow": {
    "name": "项目谋划工作流",
    "steps": [...]
  },
  "skills_used": ["research-lookup", "office"],
  "output_files": ["项目谋划报告.pdf"],
  "success_rate": 0.95,
  "user_feedback": null
}
```

---

## 版本信息

- **版本**：v1.0.0
- **更新时间**：2025-03-11
- **状态**：配置完成
