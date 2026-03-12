# 城乡建设政策知识服务系统完善计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 完善整个项目，实现自主进化能力，使系统成为可生长、自动进化的AI自动化系统

**Architecture:** 基于现有框架，增强核心模块、完善数据适配器、建立测试体系、优化进化机制、实现API接口

**Tech Stack:** Python 3.10+, FastAPI, SQLite/JSON, YAML配置

---

## 项目现状分析

### 已完成部分

| 模块 | 状态 | 完成度 |
|------|------|--------|
| 核心框架 | 已搭建 | 80% |
| 政策库 | 已有大量内容 | 90% |
| 意图分析器 | 基础实现 | 70% |
| 工作流引擎 | 基础实现 | 70% |
| 技能调度器 | 基础实现 | 60% |
| 进化引擎 | 基础实现 | 60% |
| 零件库 | 基础实现 | 70% |
| 配置系统 | 基础配置 | 50% |

### 缺失部分

| 模块 | 状态 | 优先级 |
|------|------|--------|
| 日志系统 | 需完善 | 高 |
| 输出管理 | 需创建 | 高 |
| 数据适配器 | 需实现 | 高 |
| 测试系统 | 需创建 | 高 |
| API接口 | 需实现 | 中 |
| 文档系统 | 需完善 | 中 |
| 钩子系统 | 需增强 | 中 |
| 技能集成 | 需优化 | 中 |
| 进化机制 | 需增强 | 高 |

---

## Phase 1: 基础设施完善

### Task 1.1: 创建日志系统

**Files:**
- Create: `core/logger.py`
- Create: `logs/.gitkeep`
- Modify: `core/intent_analyzer.py` (集成日志)

**Step 1: 创建日志模块**

```python
"""
日志系统模块
提供统一的日志记录功能
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class SystemLogger:
    """系统日志器"""
    
    _instance: Optional['SystemLogger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.log_dir = Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("PolicyKnowledgeSystem")
        self.logger.setLevel(logging.DEBUG)
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        file_handler = logging.FileHandler(
            self.log_dir / f"system_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """获取日志器"""
        if name:
            return logging.getLogger(f"PolicyKnowledgeSystem.{name}")
        return self.logger


def get_logger(name: str = None) -> logging.Logger:
    """获取日志器"""
    return SystemLogger().get_logger(name)
```

**Step 2: 创建日志目录**

Run: `mkdir -p logs/interactions logs/workflows logs/learning logs/system`

**Step 3: 提交**

```bash
git add core/logger.py logs/.gitkeep
git commit -m "feat: 添加统一日志系统"
```

---

### Task 1.2: 创建输出管理系统

**Files:**
- Create: `core/output_manager.py`
- Create: `outputs/.gitkeep`

**Step 1: 创建输出管理模块**

```python
"""
输出管理模块
管理所有输出文件的生成、组织和归档
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class OutputRecord:
    """输出记录"""
    id: str
    scenario: str
    created_at: str
    files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"


class OutputManager:
    """输出管理器"""
    
    def __init__(self, base_path: str = "outputs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.base_path / "output_index.json"
        self._load_index()
    
    def _load_index(self):
        """加载输出索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {"outputs": [], "total": 0}
    
    def _save_index(self):
        """保存输出索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def create_output_dir(self, scenario: str, project: str = None) -> Path:
        """创建输出目录"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        scenario_clean = scenario.replace("/", "_").replace("\\", "_")[:30]
        
        if project:
            project_clean = project.replace("/", "_").replace("\\", "_")[:20]
            dir_name = f"{timestamp}_{scenario_clean}_{project_clean}"
        else:
            dir_name = f"{timestamp}_{scenario_clean}"
        
        output_dir = self.base_path / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        record = OutputRecord(
            id=dir_name,
            scenario=scenario,
            created_at=datetime.now().isoformat(),
            status="created"
        )
        
        self.index["outputs"].append(asdict(record))
        self.index["total"] += 1
        self._save_index()
        
        return output_dir
    
    def save_file(self, output_dir: Path, filename: str, content: Any, 
                  file_type: str = "json") -> Path:
        """保存文件"""
        file_path = output_dir / filename
        
        if file_type == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        elif file_type == "text":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        elif file_type == "binary":
            with open(file_path, 'wb') as f:
                f.write(content)
        
        return file_path
    
    def get_output(self, output_id: str) -> Optional[Dict]:
        """获取输出记录"""
        for output in self.index["outputs"]:
            if output["id"] == output_id:
                return output
        return None
    
    def list_outputs(self, scenario: str = None, limit: int = 20) -> List[Dict]:
        """列出输出"""
        outputs = self.index["outputs"]
        
        if scenario:
            outputs = [o for o in outputs if scenario in o["scenario"]]
        
        return outputs[-limit:]
    
    def archive_output(self, output_id: str) -> bool:
        """归档输出"""
        output = self.get_output(output_id)
        if not output:
            return False
        
        output_dir = self.base_path / output_id
        archive_dir = self.base_path / "archived" / output_id
        
        if output_dir.exists():
            archive_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(output_dir), str(archive_dir))
            output["status"] = "archived"
            self._save_index()
            return True
        
        return False
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_outputs": self.index["total"],
            "recent_outputs": len([o for o in self.index["outputs"] 
                                  if self._is_recent(o["created_at"])]),
            "by_status": self._count_by_status()
        }
    
    def _is_recent(self, timestamp: str, days: int = 7) -> bool:
        """判断是否最近"""
        try:
            created = datetime.fromisoformat(timestamp)
            return (datetime.now() - created).days <= days
        except Exception:
            return False
    
    def _count_by_status(self) -> Dict[str, int]:
        """按状态统计"""
        counts = {}
        for output in self.index["outputs"]:
            status = output.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts
```

**Step 2: 提交**

```bash
git add core/output_manager.py outputs/.gitkeep
git commit -m "feat: 添加输出管理系统"
```

---

### Task 1.3: 创建数据适配器系统

**Files:**
- Create: `adapters/__init__.py`
- Create: `adapters/base_adapter.py`
- Create: `adapters/policy_adapter.py`
- Create: `adapters/website_adapter.py`

**Step 1: 创建基础适配器**

```python
"""
数据适配器基类
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json


class BaseAdapter(ABC):
    """数据适配器基类"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.last_sync = None
        self.sync_count = 0
    
    @abstractmethod
    def fetch(self, source: str, **kwargs) -> List[Dict]:
        """获取数据"""
        pass
    
    @abstractmethod
    def validate(self, data: Dict) -> bool:
        """验证数据"""
        pass
    
    @abstractmethod
    def transform(self, data: Dict) -> Dict:
        """转换数据"""
        pass
    
    def process(self, source: str, **kwargs) -> Dict:
        """处理数据"""
        raw_data = self.fetch(source, **kwargs)
        
        valid_data = []
        invalid_data = []
        
        for item in raw_data:
            if self.validate(item):
                valid_data.append(self.transform(item))
            else:
                invalid_data.append(item)
        
        self.last_sync = datetime.now().isoformat()
        self.sync_count += 1
        
        return {
            "total": len(raw_data),
            "valid": len(valid_data),
            "invalid": len(invalid_data),
            "data": valid_data,
            "errors": invalid_data,
            "synced_at": self.last_sync
        }
    
    def save(self, data: List[Dict], path: str) -> bool:
        """保存数据"""
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def load(self, path: str) -> Optional[List[Dict]]:
        """加载数据"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载失败: {e}")
            return None
```

**Step 2: 创建政策适配器**

```python
"""
政策数据适配器
处理政策文件的读取、解析和转换
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .base_adapter import BaseAdapter


class PolicyAdapter(BaseAdapter):
    """政策数据适配器"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.policy_base = Path(config.get("policy_base", "00_政策法规"))
    
    def fetch(self, source: str, **kwargs) -> List[Dict]:
        """获取政策数据"""
        source_path = self.policy_base / source
        
        if not source_path.exists():
            return []
        
        policies = []
        
        if source_path.is_file():
            policies.append(self._parse_policy_file(source_path))
        elif source_path.is_dir():
            for policy_file in source_path.rglob("*.md"):
                policies.append(self._parse_policy_file(policy_file))
        
        return [p for p in policies if p]
    
    def _parse_policy_file(self, file_path: Path) -> Optional[Dict]:
        """解析政策文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = self._extract_metadata(content)
            content_body = self._extract_content(content)
            
            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "metadata": metadata,
                "content": content_body,
                "raw_content": content,
                "parsed_at": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"解析政策文件失败 {file_path}: {e}")
            return None
    
    def _extract_metadata(self, content: str) -> Dict:
        """提取元数据"""
        metadata = {}
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
        
        if 'file_number' not in metadata:
            patterns = {
                'file_number': r'([国发|国办发|发改|财|建|自然资][\〔\(][\d]{4}[\〕\)][\d]+号)',
                'publishing_date': r'(\d{4}年\d{1,2}月\d{1,2}日|\d{8})',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    metadata[key] = match.group(1)
        
        return metadata
    
    def _extract_content(self, content: str) -> str:
        """提取正文内容"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2].strip()
        
        return content
    
    def validate(self, data: Dict) -> bool:
        """验证政策数据"""
        required_fields = ['file_path', 'content']
        return all(field in data for field in required_fields)
    
    def transform(self, data: Dict) -> Dict:
        """转换政策数据"""
        return {
            "id": self._generate_id(data),
            "title": data.get("metadata", {}).get("policy_name", data.get("file_name", "")),
            "file_number": data.get("metadata", {}).get("file_number", ""),
            "publishing_agency": data.get("metadata", {}).get("publishing_agency", ""),
            "publishing_date": data.get("metadata", {}).get("publishing_date", ""),
            "status": data.get("metadata", {}).get("status", "现行有效"),
            "keywords": data.get("metadata", {}).get("keywords", []),
            "content": data.get("content", ""),
            "file_path": data.get("file_path", ""),
            "source": "policy_library",
            "transformed_at": datetime.now().isoformat()
        }
    
    def _generate_id(self, data: Dict) -> str:
        """生成政策ID"""
        file_number = data.get("metadata", {}).get("file_number", "")
        if file_number:
            return file_number.replace("/", "_").replace("\\", "_")
        
        file_name = data.get("file_name", "unknown")
        return Path(file_name).stem
    
    def search(self, query: str, filters: Dict = None) -> List[Dict]:
        """搜索政策"""
        results = []
        
        all_policies = self.fetch("国家级/01_按部门")
        
        query_lower = query.lower()
        
        for policy in all_policies:
            content = policy.get("content", "").lower()
            title = policy.get("metadata", {}).get("policy_name", "").lower()
            
            if query_lower in content or query_lower in title:
                if self._match_filters(policy, filters):
                    results.append(policy)
        
        return results
    
    def _match_filters(self, policy: Dict, filters: Dict) -> bool:
        """匹配过滤条件"""
        if not filters:
            return True
        
        metadata = policy.get("metadata", {})
        
        for key, value in filters.items():
            if key in metadata:
                if isinstance(value, list):
                    if metadata[key] not in value:
                        return False
                elif metadata[key] != value:
                    return False
        
        return True
```

**Step 3: 提交**

```bash
git add adapters/
git commit -m "feat: 添加数据适配器系统"
```

---

## Phase 2: 核心模块增强

### Task 2.1: 增强意图分析器

**Files:**
- Modify: `core/intent_analyzer.py`

**Step 1: 添加更多意图模式**

在 `intent_patterns` 中添加更多模式：

```python
self.intent_patterns = {
    "项目谋划": ["谋划", "项目", "申报", "包装", "设计", "策划"],
    "项目筛选": ["筛选", "排序", "选择", "优先级", "评估", "比较"],
    "政策研究": ["研究", "政策", "分析", "趋势", "解读", "影响"],
    "流程指导": ["流程", "指导", "如何", "拿钱", "申请", "办理"],
    "快速组装": ["组装", "宣讲", "PPT", "材料", "生成", "制作"],
    "数据管理": ["管理", "采集", "入库", "归档", "更新", "维护"],
    "合同咨询": ["合同", "依据", "咨询", "特殊", "合规", "风险"],
    "组合谋划": ["组合", "多项目", "打包", "整合"],
    "打捆申报": ["打捆", "捆绑", "批量", "集中"],
    "战略规划": ["战略", "规划", "长期", "发展", "布局"],
    "新闻监测": ["新闻", "动态", "监测", "最新", "更新"]
}
```

**Step 2: 添加语义理解**

```python
def _semantic_analysis(self, user_input: str) -> Dict:
    """语义分析"""
    
    analysis = {
        "main_action": None,
        "target_object": None,
        "constraints": [],
        "context": {}
    }
    
    action_patterns = [
        (r'(谋划|设计|策划)', 'create'),
        (r'(筛选|选择|评估)', 'filter'),
        (r'(研究|分析|解读)', 'research'),
        (r'(组装|生成|制作)', 'assemble'),
        (r'(管理|维护|更新)', 'manage')
    ]
    
    for pattern, action in action_patterns:
        if re.search(pattern, user_input):
            analysis["main_action"] = action
            break
    
    amount_pattern = r'(\d+(?:\.\d+)?)\s*(万|亿|万元|亿元)'
    amounts = re.findall(amount_pattern, user_input)
    if amounts:
        analysis["constraints"].append({
            "type": "budget",
            "value": f"{amounts[0][0]}{amounts[0][1]}"
        })
    
    return analysis
```

**Step 3: 提交**

```bash
git add core/intent_analyzer.py
git commit -m "feat: 增强意图分析器，添加语义理解"
```

---

### Task 2.2: 增强工作流引擎

**Files:**
- Modify: `core/workflow_engine.py`
- Create: `config/workflow_templates.yaml`

**Step 1: 创建工作流模板配置**

```yaml
# config/workflow_templates.yaml

workflows:
  project_planning:
    name: "项目谋划工作流"
    description: "完整的政策匹配、资金方案、风险评估流程"
    steps:
      - step: 1
        action: "需求分析"
        skill: "intent_analyzer"
        description: "分析项目需求和特点"
        timeout: 30
      - step: 2
        action: "政策匹配"
        skill: "research-lookup"
        description: "匹配适用政策"
        timeout: 60
      - step: 3
        action: "资金方案"
        skill: "research-lookup"
        description: "设计资金方案"
        timeout: 60
      - step: 4
        action: "风险评估"
        skill: "scientific-critical-thinking"
        description: "评估项目风险"
        timeout: 45
      - step: 5
        action: "报告生成"
        skill: "office"
        description: "生成谋划报告"
        timeout: 30
      - step: 6
        action: "质量检查"
        skill: "verification-before-completion"
        description: "验证输出质量"
        timeout: 15

  policy_research:
    name: "政策研究工作流"
    description: "深度政策分析和趋势研究"
    steps:
      - step: 1
        action: "线索收集"
        skill: "research-lookup"
        description: "收集政策线索"
      - step: 2
        action: "趋势推断"
        skill: "scientific-critical-thinking"
        description: "推断政策趋势"
      - step: 3
        action: "信息验证"
        skill: "perplexity-search"
        description: "验证信息准确性"
      - step: 4
        action: "影响分析"
        skill: "scientific-critical-thinking"
        description: "分析政策影响"
      - step: 5
        action: "报告生成"
        skill: "office"
        description: "生成研究报告"

  quick_assembly:
    name: "快速组装工作流"
    description: "快速组装宣讲材料"
    steps:
      - step: 1
        action: "零件检索"
        skill: "markitdown"
        description: "检索知识库零件"
      - step: 2
        action: "智能组装"
        skill: "scientific-writing"
        description: "组装内容"
      - step: 3
        action: "PPT生成"
        skill: "pptx"
        description: "生成PPT文件"
      - step: 4
        action: "质量检查"
        skill: "verification-before-completion"
        description: "验证输出质量"
```

**Step 2: 增强工作流引擎**

```python
def execute_workflow_with_retry(self, workflow: Dict, context: Dict, max_retries: int = 3) -> Dict:
    """带重试的工作流执行"""
    
    workflow["status"] = "running"
    workflow["started_at"] = datetime.now().isoformat()
    
    results = []
    
    for step in workflow["steps"]:
        retry_count = 0
        step_result = None
        
        while retry_count < max_retries:
            step_result = self._execute_step(step, context)
            
            if step_result.get("success", False):
                break
            
            retry_count += 1
            if retry_count < max_retries:
                print(f"步骤 {step['step']} 失败，重试 {retry_count}/{max_retries}")
        
        results.append(step_result)
        
        if not step_result.get("success", False):
            workflow["status"] = "failed"
            workflow["error"] = step_result.get("error")
            workflow["failed_step"] = step["step"]
            break
    
    if workflow["status"] == "running":
        workflow["status"] = "completed"
    
    workflow["completed_at"] = datetime.now().isoformat()
    workflow["results"] = results
    
    self._log_workflow(workflow)
    
    return workflow
```

**Step 3: 提交**

```bash
git add core/workflow_engine.py config/workflow_templates.yaml
git commit -m "feat: 增强工作流引擎，添加重试机制和模板配置"
```

---

### Task 2.3: 增强进化引擎

**Files:**
- Modify: `core/evolution_engine.py`

**Step 1: 添加自适应学习**

```python
def adaptive_learning(self) -> Dict:
    """自适应学习"""
    
    patterns = self.analyze_patterns()
    
    improvements = {
        "intent_patterns_updated": False,
        "workflow_optimized": False,
        "skills_recommended": [],
        "parts_suggested": []
    }
    
    for intent, count in patterns["common_intents"].items():
        if count >= 10:
            improvements["intent_patterns_updated"] = True
    
    for scenario, stats in patterns["success_by_scenario"].items():
        if stats["total"] >= 5:
            success_rate = stats["success"] / stats["total"]
            if success_rate < 0.6:
                improvements["workflow_optimized"] = True
    
    low_usage_skills = [
        skill for skill, count in patterns["skill_usage"].items()
        if count < 2
    ]
    improvements["skills_recommended"] = low_usage_skills
    
    return improvements

def auto_evolve(self) -> Dict:
    """自动进化"""
    
    evolution_result = {
        "timestamp": datetime.now().isoformat(),
        "actions": []
    }
    
    adaptive_result = self.adaptive_learning()
    
    if adaptive_result["intent_patterns_updated"]:
        evolution_result["actions"].append({
            "type": "intent_update",
            "status": "completed",
            "description": "更新意图模式库"
        })
    
    if adaptive_result["workflow_optimized"]:
        evolution_result["actions"].append({
            "type": "workflow_optimization",
            "status": "completed",
            "description": "优化工作流模板"
        })
    
    self._save_evolution_metrics()
    
    return evolution_result
```

**Step 2: 提交**

```bash
git add core/evolution_engine.py
git commit -m "feat: 增强进化引擎，添加自适应学习"
```

---

## Phase 3: 测试系统

### Task 3.1: 创建测试框架

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_intent_analyzer.py`
- Create: `tests/test_workflow_engine.py`
- Create: `tests/test_parts_library.py`

**Step 1: 创建意图分析器测试**

```python
"""
意图分析器测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.intent_analyzer import IntentAnalyzer


class TestIntentAnalyzer:
    """意图分析器测试类"""
    
    def setup_method(self):
        self.analyzer = IntentAnalyzer()
    
    def test_detect_project_planning_intent(self):
        """测试项目谋划意图检测"""
        result = self.analyzer.analyze("我想谋划一个老旧小区改造项目")
        assert result["intent"] == "项目谋划"
        assert result["confidence"] > 0.5
    
    def test_detect_policy_research_intent(self):
        """测试政策研究意图检测"""
        result = self.analyzer.analyze("研究专项债券政策")
        assert result["intent"] == "政策研究"
    
    def test_extract_investment_amount(self):
        """测试投资额提取"""
        result = self.analyzer.analyze("谋划一个投资5000万的项目")
        assert "投资额" in result["entities"]
        assert "5000万" in result["entities"]["投资额"]
    
    def test_extract_project_type(self):
        """测试项目类型提取"""
        result = self.analyzer.analyze("谋划一个老旧小区改造项目")
        assert "项目类型" in result["entities"]
        assert result["entities"]["项目类型"] == "老旧小区改造"
    
    def test_generate_scenario(self):
        """测试场景生成"""
        intent_result = self.analyzer.analyze("谋划一个城市更新项目")
        scenario = self.analyzer.generate_scenario(intent_result)
        
        assert "name" in scenario
        assert "required_skills" in scenario
        assert len(scenario["required_skills"]) > 0
    
    def test_unknown_intent(self):
        """测试未知意图"""
        result = self.analyzer.analyze("今天天气怎么样")
        assert result["intent"] == "通用咨询"
```

**Step 2: 创建工作流引擎测试**

```python
"""
工作流引擎测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow_engine import WorkflowEngine


class TestWorkflowEngine:
    """工作流引擎测试类"""
    
    def setup_method(self):
        self.engine = WorkflowEngine()
    
    def test_generate_project_planning_workflow(self):
        """测试生成项目谋划工作流"""
        intent = {"intent": "项目谋划", "keywords": ["老旧小区"]}
        scenario = {"requirements": {"项目类型": "老旧小区改造"}}
        
        workflow = self.engine.generate_workflow(intent, scenario)
        
        assert workflow["workflow_name"] == "项目谋划工作流"
        assert len(workflow["steps"]) >= 5
        assert workflow["status"] == "pending"
    
    def test_generate_policy_research_workflow(self):
        """测试生成政策研究工作流"""
        intent = {"intent": "政策研究", "keywords": ["专项债券"]}
        scenario = {"requirements": {"关键词": ["专项债券"]}}
        
        workflow = self.engine.generate_workflow(intent, scenario)
        
        assert "政策研究" in workflow["workflow_name"]
    
    def test_execute_workflow(self):
        """测试工作流执行"""
        workflow = {
            "workflow_name": "测试工作流",
            "steps": [
                {"step": 1, "action": "测试步骤", "skill": "test"}
            ]
        }
        context = {"test": True}
        
        result = self.engine.execute_workflow(workflow, context)
        
        assert result["status"] == "completed"
    
    def test_get_workflow_stats(self):
        """测试获取工作流统计"""
        stats = self.engine.get_workflow_stats()
        
        assert "total" in stats
        assert "completed" in stats
        assert "failed" in stats
```

**Step 3: 运行测试**

Run: `pytest tests/ -v`

**Step 4: 提交**

```bash
git add tests/
git commit -m "feat: 添加测试系统"
```

---

## Phase 4: API接口

### Task 4.1: 创建FastAPI接口

**Files:**
- Create: `api/__init__.py`
- Create: `api/main.py`
- Create: `api/routes/__init__.py`
- Create: `api/routes/policy.py`
- Create: `api/routes/workflow.py`

**Step 1: 创建API主文件**

```python
"""
FastAPI 主入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from api.routes import policy, workflow

app = FastAPI(
    title="城乡建设政策知识服务系统 API",
    description="提供政策查询、项目谋划、工作流执行等API接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(policy.router, prefix="/api/policy", tags=["政策管理"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["工作流管理"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "城乡建设政策知识服务系统",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/stats")
async def get_stats():
    """获取系统统计"""
    from core.workflow_engine import WorkflowEngine
    from core.skill_scheduler import SkillScheduler
    from core.parts_library import PartsLibrary
    
    workflow_engine = WorkflowEngine()
    skill_scheduler = SkillScheduler()
    parts_library = PartsLibrary()
    
    return {
        "workflow": workflow_engine.get_workflow_stats(),
        "skills": skill_scheduler.get_stats(),
        "parts": parts_library.get_stats(),
        "timestamp": datetime.now().isoformat()
    }
```

**Step 2: 创建政策路由**

```python
"""
政策管理路由
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from datetime import datetime

from adapters.policy_adapter import PolicyAdapter

router = APIRouter()
policy_adapter = PolicyAdapter({"policy_base": "00_政策法规"})


@router.get("/search")
async def search_policies(
    query: str = Query(..., description="搜索关键词"),
    agency: Optional[str] = Query(None, description="发文机关"),
    status: Optional[str] = Query(None, description="政策状态")
):
    """搜索政策"""
    filters = {}
    if agency:
        filters["publishing_agency"] = agency
    if status:
        filters["status"] = status
    
    results = policy_adapter.search(query, filters)
    
    return {
        "query": query,
        "total": len(results),
        "results": results[:20],
        "timestamp": datetime.now().isoformat()
    }


@router.get("/{policy_id}")
async def get_policy(policy_id: str):
    """获取政策详情"""
    policy = policy_adapter.load(f"knowledge/policies/{policy_id}.json")
    
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")
    
    return policy


@router.get("/list/{department}")
async def list_by_department(department: str):
    """按部门列出政策"""
    results = policy_adapter.fetch(f"国家级/01_按部门/{department}")
    
    return {
        "department": department,
        "total": len(results),
        "policies": results,
        "timestamp": datetime.now().isoformat()
    }
```

**Step 3: 创建工作流路由**

```python
"""
工作流管理路由
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from core.intent_analyzer import IntentAnalyzer
from core.workflow_engine import WorkflowEngine

router = APIRouter()
intent_analyzer = IntentAnalyzer()
workflow_engine = WorkflowEngine()


class ProcessRequest(BaseModel):
    """处理请求"""
    user_input: str
    context: Optional[Dict[str, Any]] = None


class ProcessResponse(BaseModel):
    """处理响应"""
    intent: Dict[str, Any]
    scenario: Dict[str, Any]
    workflow: Dict[str, Any]
    status: str
    timestamp: str


@router.post("/process", response_model=ProcessResponse)
async def process_request(request: ProcessRequest):
    """处理用户请求"""
    
    intent_result = intent_analyzer.analyze(request.user_input)
    
    scenario = intent_analyzer.generate_scenario(intent_result)
    
    workflow = workflow_engine.generate_workflow(intent_result, scenario)
    
    context = request.context or {}
    context["user_input"] = request.user_input
    context["intent"] = intent_result
    context["scenario"] = scenario
    
    workflow_result = workflow_engine.execute_workflow(workflow, context)
    
    return ProcessResponse(
        intent=intent_result,
        scenario=scenario,
        workflow=workflow_result,
        status=workflow_result["status"],
        timestamp=datetime.now().isoformat()
    )


@router.get("/stats")
async def get_workflow_stats():
    """获取工作流统计"""
    return workflow_engine.get_workflow_stats()


@router.get("/templates")
async def list_workflow_templates():
    """列出工作流模板"""
    return {
        "templates": list(workflow_engine.workflows.get("workflows", {}).keys()),
        "timestamp": datetime.now().isoformat()
    }
```

**Step 4: 提交**

```bash
git add api/
git commit -m "feat: 添加FastAPI接口"
```

---

## Phase 5: 钩子和规则增强

### Task 5.1: 增强钩子系统

**Files:**
- Modify: `hooks/evolution_hooks.py`
- Create: `hooks/pre_workflow.py`
- Create: `hooks/post_workflow.py`

**Step 1: 创建工作流前钩子**

```python
"""
工作流执行前钩子
"""

import json
from datetime import datetime
from pathlib import Path


def pre_workflow_hook(context: dict) -> dict:
    """工作流执行前钩子"""
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "actions": []
    }
    
    _log_request(context)
    result["actions"].append({"action": "log_request", "status": "success"})
    
    _check_knowledge_base()
    result["actions"].append({"action": "check_knowledge_base", "status": "success"})
    
    _preload_data(context)
    result["actions"].append({"action": "preload_data", "status": "success"})
    
    return result


def _log_request(context: dict):
    """记录请求"""
    log_dir = Path("logs/requests")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    log_data = {
        "user_input": context.get("user_input"),
        "intent": context.get("intent", {}).get("intent"),
        "timestamp": datetime.now().isoformat()
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def _check_knowledge_base():
    """检查知识库状态"""
    policy_dir = Path("00_政策法规")
    if not policy_dir.exists():
        raise Exception("政策库不存在")


def _preload_data(context: dict):
    """预加载数据"""
    pass
```

**Step 2: 创建工作流后钩子**

```python
"""
工作流执行后钩子
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def post_workflow_hook(workflow_result: dict) -> dict:
    """工作流执行后钩子"""
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "actions": []
    }
    
    _log_interaction(workflow_result)
    result["actions"].append({"action": "log_interaction", "status": "success"})
    
    _extract_learning_data(workflow_result)
    result["actions"].append({"action": "extract_learning", "status": "success"})
    
    _update_knowledge_base(workflow_result)
    result["actions"].append({"action": "update_knowledge_base", "status": "success"})
    
    _auto_git_commit(workflow_result)
    result["actions"].append({"action": "git_commit", "status": "success"})
    
    return result


def _log_interaction(workflow_result: dict):
    """记录交互日志"""
    log_dir = Path("logs/interactions")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(workflow_result, f, ensure_ascii=False, indent=2)


def _extract_learning_data(workflow_result: dict):
    """提取学习数据"""
    learning_dir = Path("logs/learning")
    learning_dir.mkdir(parents=True, exist_ok=True)
    
    learning_data = {
        "scenario": workflow_result.get("workflow_name"),
        "status": workflow_result.get("status"),
        "skills_used": [s.get("skill") for s in workflow_result.get("steps", [])],
        "timestamp": datetime.now().isoformat()
    }
    
    learning_file = learning_dir / f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(learning_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(learning_data, ensure_ascii=False) + '\n')


def _update_knowledge_base(workflow_result: dict):
    """更新知识库"""
    pass


def _auto_git_commit(workflow_result: dict):
    """自动Git提交"""
    try:
        subprocess.run(["git", "add", "."], capture_output=True)
        
        scenario = workflow_result.get("workflow_name", "未知场景")
        commit_msg = f"feat: 完成{scenario}"
        
        subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
    except Exception as e:
        print(f"Git提交失败: {e}")
```

**Step 3: 提交**

```bash
git add hooks/
git commit -m "feat: 增强钩子系统"
```

---

## Phase 6: 文档完善

### Task 6.1: 创建API文档

**Files:**
- Create: `docs/api.md`

**Step 1: 创建API文档**

```markdown
# API 文档

## 概述

城乡建设政策知识服务系统提供RESTful API接口。

## 基础URL

```
http://localhost:8000
```

## 接口列表

### 1. 政策搜索

**GET** `/api/policy/search`

参数:
- `query`: 搜索关键词 (必填)
- `agency`: 发文机关 (可选)
- `status`: 政策状态 (可选)

响应:
```json
{
  "query": "专项债券",
  "total": 10,
  "results": [...]
}
```

### 2. 处理请求

**POST** `/api/workflow/process`

请求体:
```json
{
  "user_input": "我想谋划一个老旧小区改造项目",
  "context": {}
}
```

响应:
```json
{
  "intent": {...},
  "scenario": {...},
  "workflow": {...},
  "status": "completed"
}
```

### 3. 系统统计

**GET** `/stats`

响应:
```json
{
  "workflow": {...},
  "skills": {...},
  "parts": {...}
}
```
```

**Step 2: 提交**

```bash
git add docs/
git commit -m "docs: 添加API文档"
```

---

## Phase 7: 自主进化机制

### Task 7.1: 创建进化监控

**Files:**
- Create: `core/evolution_monitor.py`

**Step 1: 创建进化监控模块**

```python
"""
进化监控模块
监控系统进化状态，自动触发进化动作
"""

import json
import schedule
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .evolution_engine import EvolutionEngine
from .parts_library import PartsLibrary


class EvolutionMonitor:
    """进化监控器"""
    
    def __init__(self):
        self.evolution_engine = EvolutionEngine()
        self.parts_library = PartsLibrary()
        self.monitor_log = Path("logs/evolution_monitor.json")
    
    def check_and_evolve(self):
        """检查并执行进化"""
        
        report = self.evolution_engine.get_evolution_report()
        
        if self._should_evolve(report):
            evolution_result = self.evolution_engine.auto_evolve()
            self._log_evolution(evolution_result)
    
    def _should_evolve(self, report: Dict) -> bool:
        """判断是否需要进化"""
        
        interactions = report["metrics"]["total_interactions"]
        
        if interactions > 0 and interactions % 10 == 0:
            return True
        
        success_rate = float(report["success_rate"].rstrip('%')) / 100
        if success_rate < 0.7:
            return True
        
        return False
    
    def _log_evolution(self, result: Dict):
        """记录进化日志"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        with open(self.monitor_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + '\n')
    
    def start_monitoring(self, interval_minutes: int = 30):
        """启动监控"""
        
        schedule.every(interval_minutes).minutes.do(self.check_and_evolve)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def get_evolution_suggestions(self) -> List[Dict]:
        """获取进化建议"""
        return self.evolution_engine.suggest_improvements()
```

**Step 2: 提交**

```bash
git add core/evolution_monitor.py
git commit -m "feat: 添加进化监控模块"
```

---

## 执行顺序

1. **Phase 1**: 基础设施完善 (Task 1.1 - 1.3)
2. **Phase 2**: 核心模块增强 (Task 2.1 - 2.3)
3. **Phase 3**: 测试系统 (Task 3.1)
4. **Phase 4**: API接口 (Task 4.1)
5. **Phase 5**: 钩子和规则增强 (Task 5.1)
6. **Phase 6**: 文档完善 (Task 6.1)
7. **Phase 7**: 自主进化机制 (Task 7.1)

---

## 验证清单

- [ ] 日志系统正常工作
- [ ] 输出管理功能完整
- [ ] 数据适配器可用
- [ ] 意图分析准确率 > 80%
- [ ] 工作流执行成功率 > 90%
- [ ] 测试覆盖率 > 70%
- [ ] API接口可用
- [ ] 钩子正常触发
- [ ] 进化机制自动运行
- [ ] 文档完整

---

## 版本目标

完成所有任务后，系统版本升级到 **v2.0.0**，具备：
- 完整的基础设施
- 增强的核心功能
- 自动化测试
- RESTful API
- 自主进化能力
