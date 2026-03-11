"""
自动更新模块
负责自动更新README和系统状态
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def update_readme():
    """自动更新README"""
    
    stats = collect_stats()
    content = generate_readme_content(stats)
    
    readme_path = Path("README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("README已更新")
    return True


def collect_stats() -> Dict:
    """收集系统统计信息"""
    
    return {
        "total_policies": count_policies(),
        "total_scenarios": 11,
        "total_workflows": count_workflows(),
        "total_skills": count_skills(),
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def count_policies() -> int:
    """统计政策数量"""
    
    policy_dir = Path("00_政策法规")
    if not policy_dir.exists():
        return 0
    
    count = 0
    for root, dirs, files in os.walk(policy_dir):
        count += len([f for f in files if f.endswith('.md')])
    
    return count


def count_workflows() -> int:
    """统计工作流数量"""
    
    logs_dir = Path("logs/workflows")
    if not logs_dir.exists():
        return 0
    
    return len(list(logs_dir.glob("*.json")))


def count_skills() -> int:
    """统计技能数量"""
    
    registry_path = Path("config/skill_registry.json")
    if not registry_path.exists():
        return 0
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    return len(registry)


def generate_readme_content(stats: Dict) -> str:
    """生成README内容"""
    
    return f"""# 城乡建设政策知识服务系统

> 本系统用于整理、存储城乡建设咨询领域的政策法规，支持项目谋划和资金匹配

---

## 系统状态

| 指标 | 数量 |
|------|------|
| 政策总数 | {stats['total_policies']} |
| 场景总数 | {stats['total_scenarios']} |
| 工作流总数 | {stats['total_workflows']} |
| 技能总数 | {stats['total_skills']} |
| 最后更新 | {stats['last_update']} |

---

## 核心目标

**最终目标**：将政策洞察转化为可执行的项目方案，解锁下游设计和施工合同

**价值链**：
```
政策采集 → 政策解读 → 项目谋划 → 资金匹配 → 方案输出 → 设计合同
```

---

## 快速开始

### 1. 项目谋划

```
/谋划 项目名称
```

或

```
我想谋划一个老旧小区改造项目，投资5000万
```

### 2. 项目筛选

```
/筛选 项目列表
```

### 3. 政策研究

```
/研究 政策关键词
```

### 4. 快速组装

```
/组装 宣讲主题
```

---

## 11个具体场景

| 场景 | 核心需求 | 收入来源 |
|------|---------|----------|
| 场景1：项目全流程谋划 | 精准谋划→设计合同→建设服务 | 设计合同收入 |
| 场景2：多个项目组合谋划 | 多项目组合，提高申报成功率 | 设计合同收入 |
| 场景3：项目打捆申报 | 多项目打包申报，提高成功率 | 设计合同收入 |
| 场景4：政府资金申请项目筛选 | 智能筛选项目，优先级排序 | 咨询费收入 |
| 场景5：未发布/模糊政策深度研究 | 深入研究政策线索和趋势 | 咨询费收入 |
| 场景6：资金政策流程流向指导 | 指导如何拿到资金 | 咨询费收入 |
| 场景7：特殊项目合同依据咨询 | 提供合同依据和合规性分析 | 咨询费收入 |
| 场景8：快速组装宣讲材料 | 快速组装PPT和宣讲材料 | 提高效率 |
| 场景9：城市项目战略规划与拼盘 | 战略规划+拼盘+打捆 | 咨询费收入 |
| 场景10：知识库快速组装 | 快速组装知识库零件 | 提高效率 |
| 场景11：组织架构数据管理 | 管理城市组织架构和联系方式 | 基础资产 |

---

## 系统架构

```
用户交互层（混合触发）
    ↓
意图理解与场景生成层
    ↓
工作流编排层
    ↓
技能执行层（Skills + Rules + Hooks）
    ↓
数据与知识层（政策库 + 案例库 + 模板库）
    ↓
输出与反馈层（文档生成 + 智能归档 + 学习反馈）
```

---

## 目录结构

```
d:\\LMAI\\001工具人mk4\\
├── 00_政策法规/              # 政策知识库（核心资产）
├── core/                     # 核心系统
│   ├── intent_analyzer.py    # 意图分析
│   ├── scenario_generator.py # 场景生成器
│   ├── workflow_engine.py    # 工作流引擎
│   └── skill_scheduler.py    # 技能调度器
├── adapters/                 # 数据适配器
├── knowledge/                # 知识库
├── outputs/                  # 输出目录
├── skills/                   # 自定义skills
├── rules/                    # 自定义rules
├── hooks/                    # 自定义hooks
├── logs/                     # 日志
├── config/                   # 配置
├── agents.md                 # Agents配置
├── claude.md                 # Claude配置
├── trae.md                   # Trae配置
├── main.py                   # 主入口
└── auto_update.py            # 自动更新
```

---

## 核心Skills

| Skill | 功能 | 用途 |
|-------|------|------|
| research-lookup | 政策研究 | 政策匹配、信息检索 |
| perplexity-search | 实时搜索 | 最新政策、新闻 |
| office | 文档生成 | 报告输出 |
| scientific-critical-thinking | 批判性思维 | 风险评估 |
| verification-before-completion | 完成前验证 | 质量检查 |
| policy-knowledge-workflow | 政策工作流 | 政策采集、入库 |

---

## 文档

- [系统设计文档](SYSTEM_DESIGN.md)
- [Agents配置](agents.md)
- [Claude配置](claude.md)
- [Claude本地配置](claude.local.md)
- [Trae配置](trae.md)

---

## Git工作流

```bash
# 日常提交
git add .
git commit -m "feat: 添加新功能"
git push origin main

# 创建版本标签
git tag -a v1.0.0 -m "版本1.0.0"
git push origin main --tags
```

---

## 版本信息

- **版本**: v1.0.0
- **更新时间**: {stats['last_update']}
- **状态**: 运行中
"""


def git_commit(message: str = "docs: 自动更新README"):
    """Git提交"""
    
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"Git提交成功: {message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git提交失败: {e}")
        return False


def git_tag(version: str):
    """创建Git标签"""
    
    try:
        subprocess.run(["git", "tag", "-a", version, "-m", f"版本{version}"], check=True)
        subprocess.run(["git", "push", "--tags"], check=True)
        print(f"Git标签创建成功: {version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git标签创建失败: {e}")
        return False


if __name__ == "__main__":
    update_readme()
