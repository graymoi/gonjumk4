# 城乡建设政策知识服务系统

> 可生长、自动进化的AI自动化系统 - 支持持续自动化工作(Loop功能)

## 系统版本

v3.0.0 - 自动化循环工作版

## 核心特性

### 🔄 自动化循环工作 (Loop功能)
- **持续自动化**: 无需人工干预，自动执行循环任务
- **智能调度**: 优先级任务队列，自动调度执行
- **自我进化**: 从交互中学习，持续优化系统

### 🧠 持续学习引擎
- **模式提取**: 自动从会话中提取可复用模式
- **知识进化**: 模式置信度动态调整，过期模式自动清理
- **技能生成**: 高频模式自动转化为可复用技能

### 📋 智能工作流编排
- **动态工作流**: 根据需求自动生成工作流
- **并行执行**: 多任务并行处理，提升效率
- **依赖管理**: 自动处理任务依赖关系

## 快速开始

```bash
# 交互模式
python main.py

# 启动自动化循环 (推荐)
python main.py /loop start

# 执行单次循环
python main.py /loop once

# 查看循环状态
python main.py /loop status

# 命令模式
python main.py /谋划 老旧小区改造
python main.py /统计
python main.py /健康

# Git操作
python scripts/git_commit.py status
python scripts/git_commit.py sync -m "提交消息"

# 启动API服务
uvicorn core.web_api:app --reload

# 运行测试
python tests/test_auto_system.py
```

## 项目结构

```
d:\LMAI\001工具人mk4\
├── .claude/skills/      # Claude Skills
├── .memory/             # 会话记忆
├── .trae/               # Trae配置
├── 00_政策法规/          # 政策库
├── adapters/            # 数据适配器
├── config/              # 配置文件
├── core/                # 核心模块
│   ├── auto_loop_engine.py      # 自动循环引擎 ⭐
│   ├── workflow_scheduler.py    # 工作流调度器 ⭐
│   ├── continuous_learning.py   # 持续学习引擎 ⭐
│   ├── agent_orchestrator.py    # Agent协作编排
│   ├── vector_memory.py         # 向量记忆系统
│   ├── sandbox_executor.py      # 沙箱执行器
│   └── web_api.py               # Web API服务
├── docs/                # 文档
├── hooks/               # 钩子系统
├── knowledge/           # 知识库
│   └── learning_patterns.json   # 学习模式存储
├── logs/                # 日志
│   ├── loop_state.json          # 循环状态
│   └── scheduler_state.json     # 调度器状态
├── outputs/             # 输出文件
├── parts/               # 可复用零件
├── projects/            # 真实项目
├── rules/               # 业务规则
├── scripts/             # 脚本工具
├── tests/               # 测试文件
│   └── test_auto_system.py      # 自动化系统测试 ⭐
├── main.py              # 主入口
└── README.md            # 项目说明
```

## 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| **自动化循环** | /loop start | 启动持续自动化工作 ⭐ |
| **循环状态** | /loop status | 查看循环运行状态 |
| **任务调度** | /调度 add/list/stats | 智能任务调度 |
| **持续学习** | /学习 report/evolve | 自我进化学习 |
| 项目谋划 | /谋划 | 项目精准谋划 |
| 项目筛选 | /筛选 | 项目智能筛选 |
| 政策研究 | /研究 | 政策趋势分析 |
| 快速组装 | /组装 | 知识库组装 |
| 宣讲材料 | /宣讲 | PPT生成 |
| 新闻监测 | /监测 | 政策动态 |
| 系统统计 | /统计 | 运行统计 |
| 系统进化 | /进化 | 自动进化 |
| 系统优化 | /优化 | 持续优化 |
| 健康检查 | /健康 | 系统状态 |

## 系统能力

- **意图识别**: 13种意图类型
- **工作流引擎**: 11种工作流模板
- **Agent协作**: 多Agent并行/串行执行
- **向量记忆**: 长期知识存储与检索
- **沙箱执行**: 安全代码执行环境
- **Web API**: 商业化API服务
- **自动Git提交**: 工作流完成后自动提交
- **持续学习**: 从会话中提取可复用知识

## Agent系统

| Agent | 职责 |
|-------|------|
| 政策采集Agent | 自动采集政策、监测动态 |
| 项目谋划Agent | 项目精准谋划、包装优化 |
| 项目筛选Agent | 智能筛选、优先级排序 |
| 政策研究Agent | 政策研究、趋势分析 |
| 快速组装Agent | 知识库组装、PPT生成 |
| 数据管理Agent | 数据获取、验证更新 |

## 商业化路径

| 阶段 | 时间 | 目标收入 |
|------|------|---------|
| 内部提效 | 当前 | 节省人力成本 |
| 服务输出 | 3-6个月 | ¥30,000/月 |
| 平台化 | 6-12个月 | ¥215,000/月 |

## 更新日志

### v3.0.0 (2026-03-13)
- 新增Agent协作编排器
- 新增向量记忆系统
- 新增沙箱执行器
- 新增Web API服务
- 新增自动Git提交功能
- 新增持续学习Skills
- 架构改进（借鉴DeerFlow）

### v2.1.0 (2026-03-12)
- 新增持续优化模块
- 新增资金领域与项目类型映射知识库
- 新增项目谋划分析模板
- 扩展项目类型识别（+8种）
- 扩展资金来源识别（+超长期特别国债）

### v2.0.0 (2026-03-11)
- 重构核心模块
- 新增进化引擎
- 新增进化监控
- 新增钩子系统
- 新增测试系统

## 远程仓库

https://github.com/graymoi/LMAI002.git

## 许可证

内部使用
