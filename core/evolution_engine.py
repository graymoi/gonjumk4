"""
系统进化引擎

管理系统的持续学习和进化
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .parts_library import PartsLibrary, auto_collect_parts


class EvolutionEngine:
    """系统进化引擎"""
    
    def __init__(self):
        self.parts_library = PartsLibrary()
        self.learning_path = Path("logs/learning")
        self.learning_path.mkdir(parents=True, exist_ok=True)
        
        self.evolution_metrics = {
            "total_interactions": 0,
            "successful_outputs": 0,
            "parts_added": 0,
            "quality_improvements": 0
        }
    
    def evolve_after_interaction(self, interaction_result: Dict) -> Dict:
        """交互后进化"""
        
        evolution_result = {
            "timestamp": datetime.now().isoformat(),
            "interaction_id": interaction_result.get("id"),
            "actions_taken": []
        }
        
        new_parts = auto_collect_parts(self.parts_library, interaction_result)
        evolution_result["actions_taken"].append({
            "action": "parts_collection",
            "result": new_parts
        })
        
        self.evolution_metrics["total_interactions"] += 1
        if interaction_result.get("success", False):
            self.evolution_metrics["successful_outputs"] += 1
        self.evolution_metrics["parts_added"] += new_parts.get("added", 0)
        
        self._record_learning(interaction_result)
        evolution_result["actions_taken"].append({
            "action": "learning_recorded",
            "result": "success"
        })
        
        self._update_user_preferences(interaction_result)
        evolution_result["actions_taken"].append({
            "action": "preferences_updated",
            "result": "success"
        })
        
        self._save_evolution_metrics()
        
        return evolution_result
    
    def _record_learning(self, interaction_result: Dict):
        """记录学习数据"""
        
        learning_data = {
            "timestamp": datetime.now().isoformat(),
            "scenario": interaction_result.get("scenario", ""),
            "intent": interaction_result.get("intent", ""),
            "skills_used": interaction_result.get("skills_used", []),
            "success": interaction_result.get("success", False),
            "user_feedback": interaction_result.get("user_feedback"),
            "parts_extracted": interaction_result.get("parts_extracted", 0)
        }
        
        learning_file = self.learning_path / f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(learning_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(learning_data, ensure_ascii=False) + '\n')
    
    def _update_user_preferences(self, interaction_result: Dict):
        """更新用户偏好"""
        
        prefs_file = Path("config/user_preferences.json")
        
        if prefs_file.exists():
            with open(prefs_file, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
        else:
            prefs = {
                "version": "1.0.0",
                "updated_at": datetime.now().isoformat(),
                "preferred_styles": {},
                "common_scenarios": {},
                "feedback_patterns": []
            }
        
        scenario = interaction_result.get("scenario", "")
        if scenario:
            prefs["common_scenarios"][scenario] = prefs["common_scenarios"].get(scenario, 0) + 1
        
        if interaction_result.get("user_feedback"):
            prefs["feedback_patterns"].append({
                "scenario": scenario,
                "feedback": interaction_result["user_feedback"],
                "timestamp": datetime.now().isoformat()
            })
        
        prefs["updated_at"] = datetime.now().isoformat()
        
        with open(prefs_file, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)
    
    def _save_evolution_metrics(self):
        """保存进化指标"""
        
        metrics_file = Path("config/evolution_metrics.json")
        
        metrics = {
            "version": "1.0.0",
            "updated_at": datetime.now().isoformat(),
            "metrics": self.evolution_metrics,
            "parts_stats": self.parts_library.get_stats()
        }
        
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    def get_evolution_report(self) -> Dict:
        """获取进化报告"""
        
        parts_stats = self.parts_library.get_stats()
        
        success_rate = 0
        if self.evolution_metrics["total_interactions"] > 0:
            success_rate = self.evolution_metrics["successful_outputs"] / self.evolution_metrics["total_interactions"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.evolution_metrics,
            "success_rate": f"{success_rate:.2%}",
            "parts_library": parts_stats,
            "growth_summary": {
                "total_parts": parts_stats["total"],
                "total_interactions": self.evolution_metrics["total_interactions"],
                "average_parts_per_interaction": (
                    self.evolution_metrics["parts_added"] / max(1, self.evolution_metrics["total_interactions"])
                )
            }
        }
    
    def analyze_patterns(self) -> Dict:
        """分析使用模式"""
        
        learning_files = list(self.learning_path.glob("learning_*.jsonl"))
        
        patterns = {
            "common_intents": {},
            "common_scenarios": {},
            "skill_usage": {},
            "success_by_scenario": {}
        }
        
        for lf in learning_files:
            with open(lf, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    try:
                        data = json.loads(line)
                        
                        intent = data.get("intent", "")
                        if intent:
                            patterns["common_intents"][intent] = patterns["common_intents"].get(intent, 0) + 1
                        
                        scenario = data.get("scenario", "")
                        if scenario:
                            patterns["common_scenarios"][scenario] = patterns["common_scenarios"].get(scenario, 0) + 1
                            
                            if scenario not in patterns["success_by_scenario"]:
                                patterns["success_by_scenario"][scenario] = {"success": 0, "total": 0}
                            patterns["success_by_scenario"][scenario]["total"] += 1
                            if data.get("success", False):
                                patterns["success_by_scenario"][scenario]["success"] += 1
                        
                        for skill in data.get("skills_used", []):
                            patterns["skill_usage"][skill] = patterns["skill_usage"].get(skill, 0) + 1
                    
                    except json.JSONDecodeError:
                        continue
        
        return patterns
    
    def suggest_improvements(self) -> List[Dict]:
        """建议改进"""
        
        patterns = self.analyze_patterns()
        suggestions = []
        
        for scenario, stats in patterns["success_by_scenario"].items():
            if stats["total"] >= 3:
                success_rate = stats["success"] / stats["total"]
                if success_rate < 0.7:
                    suggestions.append({
                        "type": "workflow_optimization",
                        "scenario": scenario,
                        "current_success_rate": f"{success_rate:.2%}",
                        "suggestion": f"场景 '{scenario}' 成功率较低，建议优化工作流"
                    })
        
        low_usage_skills = [
            skill for skill, count in patterns["skill_usage"].items()
            if count < 2
        ]
        if low_usage_skills:
            suggestions.append({
                "type": "skill_review",
                "skills": low_usage_skills,
                "suggestion": "以下技能使用频率较低，可考虑移除或优化"
            })
        
        return suggestions
