# 系统架构改进方案

> 借鉴 DeerFlow 2.0 设计，打造可商业化的城乡建设政策知识服务系统

---

## 一、架构对比分析

### 1.1 DeerFlow 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    DeerFlow 2.0                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Sub-Agent  │    │   Sandbox   │    │   Memory    │ │
│  │  Orchestr.  │    │   Executor  │    │   System    │ │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘ │
│         │                  │                  │        │
│         └──────────────────┼──────────────────┘        │
│                            │                           │
│                    ┌───────┴───────┐                   │
│                    │ Skills & MCP  │                   │
│                    │   Framework   │                   │
│                    └───────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**核心特性**：
- **Sub-Agents**: 多智能体协作，任务分解与并行执行
- **Sandbox**: 隔离执行环境，安全运行代码
- **Memory**: 长期记忆，上下文持久化
- **Skills**: 可扩展技能系统，MCP协议支持

### 1.2 当前项目架构

```
┌─────────────────────────────────────────────────────────┐
│              城乡建设政策知识服务系统                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Intent    │    │  Workflow   │    │  Knowledge  │ │
│  │  Analyzer   │───▶│   Engine    │───▶│    Base     │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                            │                           │
│                    ┌───────┴───────┐                   │
│                    │ Skill Sched.  │                   │
│                    └───────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**现有优势**：
- 意图分析模块完善
- 工作流引擎可动态生成
- 知识库结构清晰
- 6个专业Agent定义明确

**待改进点**：
- Agent间协作机制简单
- 缺乏隔离执行环境
- 记忆系统仅文件存储
- 无MCP协议支持

---

## 二、架构改进设计

### 2.1 新架构蓝图

```
┌─────────────────────────────────────────────────────────────────┐
│                   城乡建设政策知识服务系统 v3.0                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    用户交互层                            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ Web UI  │ │ CLI     │ │ API     │ │ IM Bot  │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│  ┌─────────────────────────┴───────────────────────────────┐   │
│  │                    智能调度层                            │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │   │
│  │  │  Intent     │ │  Workflow   │ │  Context    │       │   │
│  │  │  Analyzer   │ │  Orchestr.  │ │  Manager    │       │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│  ┌─────────────────────────┴───────────────────────────────┐   │
│  │                    Agent协作层                           │   │
│  │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐     │   │
│  │  │政策采集│ │项目谋划│ │项目筛选│ │政策研究│ │快速组装│     │   │
│  │  │Agent  │ │Agent  │ │Agent  │ │Agent  │ │Agent  │     │   │
│  │  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘     │   │
│  │                    ┌───────┐                            │   │
│  │                    │数据管理│                            │   │
│  │                    │Agent  │                            │   │
│  │                    └───────┘                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│  ┌─────────────────────────┴───────────────────────────────┐   │
│  │                    能力支撑层                            │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │   │
│  │  │   Skills    │ │    MCP      │ │   Sandbox   │       │   │
│  │  │   Engine    │ │   Server    │ │   Executor  │       │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│  ┌─────────────────────────┴───────────────────────────────┐   │
│  │                    数据持久层                            │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │   │
│  │  │  Vector DB  │ │  Policy DB  │ │  Memory DB  │       │   │
│  │  │  (Milvus)   │ │  (SQLite)   │ │  (Redis)    │       │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心模块改进

#### 2.2.1 Agent协作框架

```python
# core/agent_orchestrator.py

from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class AgentType(Enum):
    POLICY_COLLECTOR = "policy_collector"
    PROJECT_PLANNER = "project_planner"
    PROJECT_FILTER = "project_filter"
    POLICY_RESEARCHER = "policy_researcher"
    QUICK_ASSEMBLER = "quick_assembler"
    DATA_MANAGER = "data_manager"

@dataclass
class AgentTask:
    task_id: str
    agent_type: AgentType
    input_data: Dict
    priority: int
    dependencies: List[str]
    status: str = "pending"
    result: Any = None
    created_at: datetime = None

class AgentOrchestrator:
    """Agent协作编排器"""
    
    def __init__(self):
        self.agents = self._init_agents()
        self.task_queue = []
        self.execution_graph = {}
        
    def _init_agents(self) -> Dict[AgentType, 'BaseAgent']:
        """初始化所有Agent"""
        return {
            AgentType.POLICY_COLLECTOR: PolicyCollectorAgent(),
            AgentType.PROJECT_PLANNER: ProjectPlannerAgent(),
            AgentType.PROJECT_FILTER: ProjectFilterAgent(),
            AgentType.POLICY_RESEARCHER: PolicyResearcherAgent(),
            AgentType.QUICK_ASSEMBLER: QuickAssemblerAgent(),
            AgentType.DATA_MANAGER: DataManagerAgent(),
        }
    
    def submit_task(self, task: AgentTask) -> str:
        """提交任务到队列"""
        task.created_at = datetime.now()
        self.task_queue.append(task)
        self._build_execution_graph()
        return task.task_id
    
    def execute_parallel(self, tasks: List[AgentTask]) -> Dict:
        """并行执行多个独立任务"""
        from concurrent.futures import ThreadPoolExecutor
        
        results = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(
                    self.agents[t.agent_type].execute, 
                    t.input_data
                ): t for t in tasks
            }
            for future in futures:
                task = futures[future]
                results[task.task_id] = future.result()
        
        return results
    
    def execute_sequential(self, tasks: List[AgentTask]) -> Dict:
        """串行执行有依赖的任务"""
        results = {}
        for task in tasks:
            if self._check_dependencies(task, results):
                result = self.agents[task.agent_type].execute(task.input_data)
                results[task.task_id] = result
        return results
```

#### 2.2.2 向量记忆系统

```python
# core/vector_memory.py

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
from datetime import datetime

@dataclass
class MemoryEntry:
    id: str
    content: str
    embedding: List[float]
    metadata: Dict
    created_at: datetime
    access_count: int = 0

class VectorMemory:
    """向量记忆系统 - 借鉴DeerFlow的长期记忆设计"""
    
    def __init__(self, persist_path: str = "data/memory"):
        self.persist_path = persist_path
        self.memories: List[MemoryEntry] = []
        self._load_memories()
    
    def store(self, content: str, metadata: Dict = None) -> str:
        """存储记忆"""
        entry = MemoryEntry(
            id=self._generate_id(),
            content=content,
            embedding=self._embed(content),
            metadata=metadata or {},
            created_at=datetime.now()
        )
        self.memories.append(entry)
        self._persist()
        return entry.id
    
    def recall(self, query: str, top_k: int = 5) -> List[Dict]:
        """检索相关记忆"""
        query_embedding = self._embed(query)
        scored = [
            (m, self._cosine_similarity(query_embedding, m.embedding))
            for m in self.memories
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for memory, score in scored[:top_k]:
            memory.access_count += 1
            results.append({
                "content": memory.content,
                "metadata": memory.metadata,
                "score": score,
                "created_at": memory.created_at.isoformat()
            })
        
        self._persist()
        return results
    
    def _embed(self, text: str) -> List[float]:
        """生成文本嵌入向量"""
        pass
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        pass
```

#### 2.2.3 Sandbox执行器

```python
# core/sandbox_executor.py

import subprocess
import tempfile
import os
from typing import Dict, Any
from pathlib import Path

class SandboxExecutor:
    """沙箱执行器 - 安全运行用户代码"""
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.allowed_modules = [
            'pandas', 'numpy', 'json', 'datetime',
            'pathlib', 're', 'collections', 'typing'
        ]
    
    def execute_code(self, code: str, context: Dict = None) -> Dict:
        """在沙箱中执行Python代码"""
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = Path(tmpdir) / "user_code.py"
            code_file.write_text(self._wrap_code(code, context))
            
            try:
                result = subprocess.run(
                    ['python', str(code_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tmpdir
                )
                
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None
                }
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": f"执行超时（{self.timeout}秒）"
                }
    
    def _wrap_code(self, code: str, context: Dict) -> str:
        """包装用户代码，添加安全限制"""
        wrapper = f'''
import sys
import os

# 限制模块导入
class RestrictedImporter:
    def __init__(self, allowed):
        self.allowed = allowed
    
    def find_module(self, name, path=None):
        if name.split('.')[0] not in self.allowed:
            raise ImportError(f"模块 {{name}} 不被允许导入")

sys.meta_path.insert(0, RestrictedImporter({self.allowed_modules}))

# 注入上下文
context = {context}

# 用户代码
{code}
'''
        return wrapper
```

---

## 三、经济价值分析

### 3.1 商业化路径

```
┌─────────────────────────────────────────────────────────────┐
│                    商业化路径规划                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  阶段一：内部提效（当前）                                     │
│  ├── 自动化政策采集，节省人力成本                            │
│  ├── 智能项目谋划，提高申报成功率                            │
│  └── 知识库积累，降低培训成本                                │
│                                                             │
│  阶段二：服务输出（3-6个月）                                  │
│  ├── 政策咨询服务（按次收费）                                │
│  ├── 项目谋划报告（按项目收费）                              │
│  └── 政策培训服务（按人次收费）                              │
│                                                             │
│  阶段三：平台化（6-12个月）                                   │
│  ├── SaaS订阅服务（月费/年费）                               │
│  ├── API开放服务（按调用收费）                               │
│  └── 定制开发服务（项目制）                                  │
│                                                             │
│  阶段四：生态建设（12个月+）                                  │
│  ├── 行业解决方案（垂直领域）                                │
│  ├── 合作伙伴生态（渠道分成）                                │
│  └── 数据资产变现（数据服务）                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 收入模型

| 服务类型 | 定价模式 | 预估收入/月 | 目标客户 |
|---------|---------|-----------|---------|
| 政策查询 | 免费+增值 | ¥5,000 | 个人用户 |
| 项目谋划报告 | ¥500-2000/份 | ¥30,000 | 中小企业 |
| 政策咨询服务 | ¥200/次 | ¥10,000 | 咨询公司 |
| SaaS订阅 | ¥999/月起 | ¥50,000 | 政府部门 |
| API调用 | ¥0.1/次 | ¥20,000 | 开发者 |
| 定制开发 | ¥50,000起 | ¥100,000 | 大型企业 |

**预估月收入：¥215,000**

### 3.3 成本结构

| 成本项目 | 月成本 | 说明 |
|---------|--------|------|
| 服务器 | ¥3,000 | 云服务器+数据库 |
| API调用 | ¥5,000 | LLM API费用 |
| 运维 | ¥2,000 | 监控+备份 |
| 人力 | ¥30,000 | 1人维护 |
| **合计** | **¥40,000** | |

**预估月利润：¥175,000**

---

## 四、实施路线图

### 4.1 第一阶段：核心能力增强（1-2个月）

```
Week 1-2: Agent协作框架
├── 实现AgentOrchestrator
├── 添加并行/串行执行
└── 集成到现有工作流

Week 3-4: 向量记忆系统
├── 集成向量数据库
├── 实现记忆存储/检索
└── 添加到知识库

Week 5-6: Sandbox执行器
├── 实现安全沙箱
├── 添加代码执行能力
└── 集成数据分析功能

Week 7-8: Web界面
├── 开发前端界面
├── 实现用户认证
└── 部署测试环境
```

### 4.2 第二阶段：服务产品化（2-3个月）

```
Month 3: MVP上线
├── 政策查询功能
├── 项目谋划报告生成
└── 用户反馈收集

Month 4: 付费功能
├── 会员体系
├── 支付集成
└── 订单管理

Month 5: API开放
├── API文档
├── 开发者控制台
└── 调用统计
```

### 4.3 第三阶段：规模化（3-6个月）

```
Month 6-8: 市场推广
├── SEO优化
├── 内容营销
└── 合作渠道

Month 9-11: 产品迭代
├── 功能优化
├── 性能提升
└── 用户体验改进
```

---

## 五、技术选型

### 5.1 核心技术栈

| 层级 | 技术选型 | 说明 |
|-----|---------|------|
| 前端 | Next.js + Tailwind | 现代化Web框架 |
| 后端 | FastAPI | 高性能Python框架 |
| 数据库 | PostgreSQL + Redis | 关系+缓存 |
| 向量库 | Milvus | 开源向量数据库 |
| LLM | 本地部署/云API | 灵活切换 |
| 部署 | Docker + K8s | 容器化部署 |

### 5.2 开源依赖

```python
# requirements.txt

# Web框架
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0

# 数据处理
pandas>=2.0.0
numpy>=1.24.0

# 向量数据库
pymilvus>=2.3.0

# LLM
langchain>=0.1.0
openai>=1.0.0

# 工具
python-docx>=0.8.11
openpyxl>=3.1.0
reportlab>=4.0.0

# 异步
aiohttp>=3.8.0
httpx>=0.24.0
```

---

## 六、风险与应对

| 风险 | 概率 | 影响 | 应对措施 |
|-----|------|------|---------|
| 政策变化 | 高 | 中 | 持续更新知识库 |
| 竞品出现 | 中 | 高 | 差异化定位 |
| 技术瓶颈 | 中 | 高 | 持续技术投入 |
| 用户接受度 | 低 | 高 | MVP快速验证 |
| 合规风险 | 低 | 高 | 法务审核 |

---

## 七、总结

本方案借鉴DeerFlow的优秀架构设计，结合城乡建设政策知识服务的业务场景，设计了：

1. **Agent协作框架** - 多智能体并行/串行执行
2. **向量记忆系统** - 长期记忆与智能检索
3. **Sandbox执行器** - 安全代码执行环境
4. **商业化路径** - 从内部提效到平台化运营

预期实现月收入¥215,000，月利润¥175,000的投资回报。

---

*文档版本：v1.0*
*创建时间：2026-03-13*
*作者：AI助手*
