"""
系统进化钩子模块
用于在工作流执行前后触发学习和进化机制
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class EvolutionHooks:
    """进化钩子管理器"""
    
    def __init__(self, base_path: str = "d:/LMAI/001工具人mk4"):
        self.base_path = Path(base_path)
        self.logs_path = self.base_path / "logs"
        self.learning_path = self.logs_path / "learning"
        self.interactions_path = self.logs_path / "interactions"
        self.evolution_path = self.logs_path / "evolution"
        
        self._ensure_directories()
        
        self.evolution_metrics = self._load_evolution_metrics()
    
    def _ensure_directories(self):
        """确保目录存在"""
        for path in [self.learning_path, self.interactions_path, self.evolution_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _load_evolution_metrics(self) -> Dict:
        """加载进化指标"""
        metrics_file = self.evolution_path / "metrics.json"
        if metrics_file.exists():
            with open(metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_interactions": 0,
            "successful_outputs": 0,
            "parts_added": 0,
            "quality_improvements": 0,
            "user_satisfaction": 0.0,
            "level": 1,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def _save_evolution_metrics(self):
        """保存进化指标"""
        self.evolution_metrics["updated_at"] = datetime.now().isoformat()
        metrics_file = self.evolution_path / "metrics.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.evolution_metrics, f, ensure_ascii=False, indent=2)
    
    def pre_workflow(self, workflow_info: Dict) -> Dict:
        """工作流执行前钩子"""
        
        hook_result = {
            "timestamp": datetime.now().isoformat(),
            "hook_type": "pre_workflow",
            "workflow_info": workflow_info,
            "actions": []
        }
        
        context = {
            "user_preferences": self._get_user_preferences(),
            "recent_parts": self._get_recent_parts(5),
            "evolution_level": self.evolution_metrics.get("level", 1)
        }
        
        hook_result["actions"].append({
            "action": "load_context",
            "result": "success"
        })
        
        hook_result["context"] = context
        
        return hook_result
    
    def post_workflow(self, workflow_result: Dict) -> Dict:
        """工作流执行后钩子"""
        
        hook_result = {
            "timestamp": datetime.now().isoformat(),
            "hook_type": "post_workflow",
            "workflow_result": workflow_result,
            "actions": []
        }
        
        self._record_interaction(workflow_result)
        hook_result["actions"].append({
            "action": "record_interaction",
            "result": "success"
        })
        
        parts_result = self._auto_extract_parts(workflow_result)
        hook_result["actions"].append({
            "action": "extract_parts",
            "result": parts_result
        })
        
        self._update_evolution_metrics(workflow_result)
        hook_result["actions"].append({
            "action": "update_metrics",
            "result": "success"
        })
        
        evolution_result = self._check_evolution()
        if evolution_result.get("evolved"):
            hook_result["actions"].append({
                "action": "evolution",
                "result": evolution_result
            })
        
        self._save_evolution_metrics()
        
        return hook_result
    
    def on_learning(self, learning_data: Dict) -> Dict:
        """学习触发钩子"""
        
        hook_result = {
            "timestamp": datetime.now().isoformat(),
            "hook_type": "on_learning",
            "learning_data": learning_data,
            "actions": []
        }
        
        learning_record = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "type": learning_data.get("type"),
            "content": learning_data.get("content"),
            "source": learning_data.get("source"),
            "tags": learning_data.get("tags", [])
        }
        
        learning_file = self.learning_path / f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(learning_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(learning_record, ensure_ascii=False) + '\n')
        
        hook_result["actions"].append({
            "action": "record_learning",
            "result": "success",
            "learning_id": learning_record["id"]
        })
        
        return hook_result
    
    def on_error(self, error_info: Dict) -> Dict:
        """错误处理钩子"""
        
        hook_result = {
            "timestamp": datetime.now().isoformat(),
            "hook_type": "on_error",
            "error_info": error_info,
            "actions": []
        }
        
        error_record = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "error_type": error_info.get("type"),
            "error_message": error_info.get("message"),
            "context": error_info.get("context"),
            "stack_trace": error_info.get("stack_trace")
        }
        
        error_file = self.logs_path / "errors.jsonl"
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_record, ensure_ascii=False) + '\n')
        
        hook_result["actions"].append({
            "action": "record_error",
            "result": "success"
        })
        
        return hook_result
    
    def on_user_feedback(self, feedback: Dict) -> Dict:
        """用户反馈钩子"""
        
        hook_result = {
            "timestamp": datetime.now().isoformat(),
            "hook_type": "on_user_feedback",
            "feedback": feedback,
            "actions": []
        }
        
        if feedback.get("type") == "correction":
            self._learn_from_correction(feedback)
            hook_result["actions"].append({
                "action": "learn_from_correction",
                "result": "success"
            })
        
        if feedback.get("rating"):
            self._update_satisfaction(feedback["rating"])
            hook_result["actions"].append({
                "action": "update_satisfaction",
                "result": "success"
            })
        
        feedback_file = self.logs_path / "feedback.jsonl"
        with open(feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
        
        hook_result["actions"].append({
            "action": "record_feedback",
            "result": "success"
        })
        
        return hook_result
    
    def _record_interaction(self, workflow_result: Dict):
        """记录交互"""
        interaction_record = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "user_input": workflow_result.get("user_input"),
            "intent": workflow_result.get("intent"),
            "scenario": workflow_result.get("scenario"),
            "skills_used": workflow_result.get("skills_used", []),
            "output_files": workflow_result.get("output_files", []),
            "success": workflow_result.get("success", False),
            "duration": workflow_result.get("duration")
        }
        
        interaction_file = self.interactions_path / f"interactions_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(interaction_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(interaction_record, ensure_ascii=False) + '\n')
    
    def _auto_extract_parts(self, workflow_result: Dict) -> Dict:
        """自动提取零件"""
        parts_added = 0
        
        if workflow_result.get("success"):
            output_content = workflow_result.get("output_content", "")
            if output_content:
                parts_added += 1
        
        self.evolution_metrics["parts_added"] += parts_added
        
        return {
            "parts_added": parts_added,
            "total_parts": self.evolution_metrics["parts_added"]
        }
    
    def _update_evolution_metrics(self, workflow_result: Dict):
        """更新进化指标"""
        self.evolution_metrics["total_interactions"] += 1
        
        if workflow_result.get("success"):
            self.evolution_metrics["successful_outputs"] += 1
    
    def _check_evolution(self) -> Dict:
        """检查是否进化"""
        current_level = self.evolution_metrics.get("level", 1)
        new_level = current_level
        
        total = self.evolution_metrics["total_interactions"]
        success = self.evolution_metrics["successful_outputs"]
        parts = self.evolution_metrics["parts_added"]
        satisfaction = self.evolution_metrics.get("user_satisfaction", 0)
        
        if total >= 10 and current_level < 2:
            new_level = 2
        elif parts >= 50 and current_level < 3:
            new_level = 3
        elif success / max(total, 1) >= 0.9 and current_level < 4:
            new_level = 4
        elif satisfaction >= 0.95 and current_level < 5:
            new_level = 5
        
        evolved = new_level > current_level
        if evolved:
            self.evolution_metrics["level"] = new_level
        
        return {
            "evolved": evolved,
            "old_level": current_level,
            "new_level": new_level
        }
    
    def _get_user_preferences(self) -> Dict:
        """获取用户偏好"""
        prefs_file = self.base_path / "config" / "user_preferences.json"
        if prefs_file.exists():
            with open(prefs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "output_format": "markdown",
            "language_style": "专业正式",
            "detail_level": "详细"
        }
    
    def _get_recent_parts(self, limit: int = 5) -> list:
        """获取最近零件"""
        return []
    
    def _learn_from_correction(self, feedback: Dict):
        """从纠正中学习"""
        learning_data = {
            "type": "correction",
            "content": feedback.get("correction"),
            "source": "user_feedback",
            "tags": ["correction", "improvement"]
        }
        self.on_learning(learning_data)
    
    def _update_satisfaction(self, rating: float):
        """更新满意度"""
        current = self.evolution_metrics.get("user_satisfaction", 0)
        total = self.evolution_metrics["total_interactions"]
        
        new_satisfaction = (current * (total - 1) + rating) / total
        self.evolution_metrics["user_satisfaction"] = new_satisfaction


def pre_workflow_hook(workflow_info: Dict) -> Dict:
    """工作流执行前钩子函数"""
    hooks = EvolutionHooks()
    return hooks.pre_workflow(workflow_info)


def post_workflow_hook(workflow_result: Dict) -> Dict:
    """工作流执行后钩子函数"""
    hooks = EvolutionHooks()
    return hooks.post_workflow(workflow_result)


def learning_hook(learning_data: Dict) -> Dict:
    """学习触发钩子函数"""
    hooks = EvolutionHooks()
    return hooks.on_learning(learning_data)


def error_hook(error_info: Dict) -> Dict:
    """错误处理钩子函数"""
    hooks = EvolutionHooks()
    return hooks.on_error(error_info)


def feedback_hook(feedback: Dict) -> Dict:
    """用户反馈钩子函数"""
    hooks = EvolutionHooks()
    return hooks.on_user_feedback(feedback)
