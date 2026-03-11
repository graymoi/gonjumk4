"""
工作流引擎模块
负责动态生成和执行工作流
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self, config_path: str = "config/workflow_templates.yaml"):
        self.config_path = Path(config_path)
        self.workflows = self._load_workflows()
        self.logs_dir = Path("logs/workflows")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_workflows(self) -> Dict:
        """加载工作流模板"""
        if self.config_path.exists():
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {"workflows": []}
    
    def generate_workflow(self, intent: Dict, scenario: Dict) -> Dict:
        """根据意图和场景生成工作流"""
        
        intent_type = intent.get("intent", "")
        requirements = scenario.get("requirements", {})
        
        workflow = {
            "workflow_name": f"{intent_type}工作流",
            "created_at": datetime.now().isoformat(),
            "steps": self._generate_steps(intent_type, requirements),
            "status": "pending"
        }
        
        return workflow
    
    def _generate_steps(self, intent_type: str, requirements: Dict) -> List[Dict]:
        """生成工作流步骤"""
        
        steps_map = {
            "项目谋划": [
                {"step": 1, "action": "需求分析", "skill": "intent_analyzer", "description": "分析项目需求"},
                {"step": 2, "action": "政策匹配", "skill": "research-lookup", "description": "匹配适用政策"},
                {"step": 3, "action": "资金方案", "skill": "research-lookup", "description": "设计资金方案"},
                {"step": 4, "action": "风险评估", "skill": "scientific-critical-thinking", "description": "评估项目风险"},
                {"step": 5, "action": "报告生成", "skill": "office", "description": "生成谋划报告"},
                {"step": 6, "action": "质量检查", "skill": "verification-before-completion", "description": "验证输出质量"}
            ],
            "项目筛选": [
                {"step": 1, "action": "项目分析", "skill": "intent_analyzer", "description": "分析项目特点"},
                {"step": 2, "action": "筛选标准", "skill": "scientific-critical-thinking", "description": "制定筛选标准"},
                {"step": 3, "action": "智能筛选", "skill": "research-lookup", "description": "执行项目筛选"},
                {"step": 4, "action": "优先级排序", "skill": "xlsx", "description": "排序项目优先级"},
                {"step": 5, "action": "报告生成", "skill": "office", "description": "生成筛选报告"}
            ],
            "政策研究": [
                {"step": 1, "action": "线索收集", "skill": "research-lookup", "description": "收集政策线索"},
                {"step": 2, "action": "趋势推断", "skill": "scientific-critical-thinking", "description": "推断政策趋势"},
                {"step": 3, "action": "信息验证", "skill": "perplexity-search", "description": "验证信息准确性"},
                {"step": 4, "action": "影响分析", "skill": "scientific-critical-thinking", "description": "分析政策影响"},
                {"step": 5, "action": "报告生成", "skill": "office", "description": "生成研究报告"}
            ],
            "流程指导": [
                {"step": 1, "action": "流程分析", "skill": "research-lookup", "description": "分析资金流程"},
                {"step": 2, "action": "指导设计", "skill": "scientific-critical-thinking", "description": "设计指导方案"},
                {"step": 3, "action": "风险预警", "skill": "scientific-critical-thinking", "description": "识别风险点"},
                {"step": 4, "action": "材料清单", "skill": "xlsx", "description": "生成材料清单"},
                {"step": 5, "action": "报告生成", "skill": "office", "description": "生成指导报告"}
            ],
            "快速组装": [
                {"step": 1, "action": "零件检索", "skill": "markitdown", "description": "检索知识库零件"},
                {"step": 2, "action": "智能组装", "skill": "scientific-writing", "description": "组装内容"},
                {"step": 3, "action": "PPT生成", "skill": "pptx", "description": "生成PPT文件"},
                {"step": 4, "action": "质量检查", "skill": "verification-before-completion", "description": "验证输出质量"}
            ],
            "数据管理": [
                {"step": 1, "action": "数据采集", "skill": "agent-browser", "description": "采集数据"},
                {"step": 2, "action": "数据验证", "skill": "verification-before-completion", "description": "验证数据质量"},
                {"step": 3, "action": "元数据提取", "skill": "markitdown", "description": "提取元数据"},
                {"step": 4, "action": "数据存储", "skill": "pandas", "description": "存储数据"},
                {"step": 5, "action": "索引生成", "skill": "xlsx", "description": "生成索引文件"}
            ]
        }
        
        return steps_map.get(intent_type, self._generate_default_steps())
    
    def _generate_default_steps(self) -> List[Dict]:
        """生成默认工作流步骤"""
        return [
            {"step": 1, "action": "需求分析", "skill": "intent_analyzer", "description": "分析用户需求"},
            {"step": 2, "action": "信息检索", "skill": "research-lookup", "description": "检索相关信息"},
            {"step": 3, "action": "内容生成", "skill": "office", "description": "生成输出内容"},
            {"step": 4, "action": "质量检查", "skill": "verification-before-completion", "description": "验证输出质量"}
        ]
    
    def execute_workflow(self, workflow: Dict, context: Dict) -> Dict:
        """执行工作流"""
        
        workflow["status"] = "running"
        workflow["started_at"] = datetime.now().isoformat()
        
        results = []
        for step in workflow["steps"]:
            step_result = self._execute_step(step, context)
            results.append(step_result)
            
            if not step_result.get("success", False):
                workflow["status"] = "failed"
                workflow["error"] = step_result.get("error")
                break
        
        if workflow["status"] == "running":
            workflow["status"] = "completed"
        
        workflow["completed_at"] = datetime.now().isoformat()
        workflow["results"] = results
        
        self._log_workflow(workflow)
        
        return workflow
    
    def _execute_step(self, step: Dict, context: Dict) -> Dict:
        """执行单个步骤"""
        
        return {
            "step": step["step"],
            "action": step["action"],
            "skill": step["skill"],
            "success": True,
            "output": f"完成{step['action']}",
            "timestamp": datetime.now().isoformat()
        }
    
    def _log_workflow(self, workflow: Dict):
        """记录工作流日志"""
        
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, ensure_ascii=False, indent=2)
    
    def get_workflow_stats(self) -> Dict:
        """获取工作流统计"""
        
        log_files = list(self.logs_dir.glob("*.json"))
        
        total = len(log_files)
        completed = 0
        failed = 0
        
        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
                if workflow.get("status") == "completed":
                    completed += 1
                elif workflow.get("status") == "failed":
                    failed += 1
        
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "success_rate": completed / total if total > 0 else 0
        }
