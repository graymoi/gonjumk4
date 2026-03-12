"""
系统进化引擎

管理系统的持续学习和进化
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict

from .parts_library import PartsLibrary, auto_collect_parts
from .logger import get_system_logger


class EvolutionEngine:
    """系统进化引擎"""
    
    def __init__(self):
        self.logger = get_system_logger()
        self.parts_library = PartsLibrary()
        self.learning_path = Path("logs/learning")
        self.learning_path.mkdir(parents=True, exist_ok=True)
        
        self.evolution_metrics = {
            "total_interactions": 0,
            "successful_outputs": 0,
            "parts_added": 0,
            "quality_improvements": 0,
            "auto_adaptations": 0,
            "pattern_discoveries": 0
        }
        
        self.adaptive_rules = self._load_adaptive_rules()
        self.pattern_memory = defaultdict(list)
        self.feedback_history = []
    
    def _load_adaptive_rules(self) -> Dict:
        """加载自适应规则"""
        rules_file = Path("config/adaptive_rules.json")
        if rules_file.exists():
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "version": "1.0.0",
            "rules": [],
            "auto_apply": True,
            "confidence_threshold": 0.7
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
        
        adaptation_result = self._adaptive_learning(interaction_result)
        if adaptation_result.get("adapted"):
            evolution_result["actions_taken"].append({
                "action": "adaptive_learning",
                "result": adaptation_result
            })
            self.evolution_metrics["auto_adaptations"] += 1
        
        pattern_result = self._detect_patterns(interaction_result)
        if pattern_result.get("new_pattern"):
            evolution_result["actions_taken"].append({
                "action": "pattern_detected",
                "result": pattern_result
            })
            self.evolution_metrics["pattern_discoveries"] += 1
        
        self._save_evolution_metrics()
        
        return evolution_result
    
    def _adaptive_learning(self, interaction_result: Dict) -> Dict:
        """自适应学习"""
        
        result = {
            "adapted": False,
            "changes": []
        }
        
        scenario = interaction_result.get("scenario", "")
        success = interaction_result.get("success", False)
        skills_used = interaction_result.get("skills_used", [])
        user_feedback = interaction_result.get("user_feedback")
        
        if scenario and skills_used:
            key = f"skills_{scenario}"
            self.pattern_memory[key].append({
                "skills": skills_used,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(self.pattern_memory[key]) >= 3:
                success_rate = sum(1 for p in self.pattern_memory[key] if p["success"]) / len(self.pattern_memory[key])
                
                if success_rate >= self.adaptive_rules.get("confidence_threshold", 0.7):
                    rule = {
                        "type": "skill_optimization",
                        "scenario": scenario,
                        "recommended_skills": skills_used,
                        "confidence": success_rate,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    if self.adaptive_rules.get("auto_apply", True):
                        self._apply_adaptive_rule(rule)
                        result["adapted"] = True
                        result["changes"].append(f"自动应用技能优化规则: {scenario}")
        
        if user_feedback:
            self.feedback_history.append({
                "scenario": scenario,
                "feedback": user_feedback,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(self.feedback_history) >= 5:
                feedback_analysis = self._analyze_feedback_patterns()
                if feedback_analysis.get("improvements"):
                    result["adapted"] = True
                    result["changes"].extend(feedback_analysis["improvements"])
        
        return result
    
    def _detect_patterns(self, interaction_result: Dict) -> Dict:
        """检测新模式"""
        
        result = {
            "new_pattern": False,
            "pattern": None
        }
        
        intent = interaction_result.get("intent", "")
        scenario = interaction_result.get("scenario", "")
        keywords = interaction_result.get("keywords", [])
        
        if intent and scenario:
            pattern_key = f"intent_scenario_{intent}_{scenario}"
            
            if pattern_key not in self.pattern_memory:
                self.pattern_memory[pattern_key] = []
            
            self.pattern_memory[pattern_key].append({
                "keywords": keywords,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(self.pattern_memory[pattern_key]) >= 3:
                common_keywords = self._find_common_keywords(pattern_key)
                if common_keywords:
                    result["new_pattern"] = True
                    result["pattern"] = {
                        "type": "intent_scenario_pattern",
                        "intent": intent,
                        "scenario": scenario,
                        "common_keywords": common_keywords,
                        "frequency": len(self.pattern_memory[pattern_key])
                    }
        
        return result
    
    def _find_common_keywords(self, pattern_key: str) -> List[str]:
        """查找共同关键词"""
        
        keyword_counts = defaultdict(int)
        total = len(self.pattern_memory[pattern_key])
        
        for entry in self.pattern_memory[pattern_key]:
            for kw in entry.get("keywords", []):
                keyword_counts[kw] += 1
        
        common = [
            kw for kw, count in keyword_counts.items()
            if count / total >= 0.5
        ]
        
        return common
    
    def _analyze_feedback_patterns(self) -> Dict:
        """分析反馈模式"""
        
        improvements = []
        
        recent_feedback = self.feedback_history[-10:]
        
        negative_feedback = [f for f in recent_feedback if not f["success"]]
        
        if len(negative_feedback) >= 3:
            scenario_counts = defaultdict(int)
            for f in negative_feedback:
                scenario_counts[f["scenario"]] += 1
            
            for scenario, count in scenario_counts.items():
                if count >= 2:
                    improvements.append(f"场景 '{scenario}' 多次失败，需要优化工作流")
        
        return {"improvements": improvements}
    
    def _apply_adaptive_rule(self, rule: Dict):
        """应用自适应规则"""
        
        self.adaptive_rules["rules"].append(rule)
        
        rules_file = Path("config/adaptive_rules.json")
        rules_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.adaptive_rules, f, ensure_ascii=False, indent=2)
        
        self.logger.info(
            f"应用自适应规则: {rule['type']} - {rule.get('scenario', '')}",
            module="evolution_engine"
        )
    
    def _record_learning(self, interaction_result: Dict):
        """记录学习数据"""
        
        learning_data = {
            "timestamp": datetime.now().isoformat(),
            "scenario": interaction_result.get("scenario", ""),
            "intent": interaction_result.get("intent", ""),
            "skills_used": interaction_result.get("skills_used", []),
            "success": interaction_result.get("success", False),
            "user_feedback": interaction_result.get("user_feedback"),
            "parts_extracted": interaction_result.get("parts_extracted", 0),
            "keywords": interaction_result.get("keywords", [])
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
                "feedback_patterns": [],
                "intent_frequency": {},
                "skill_preferences": {}
            }
        
        scenario = interaction_result.get("scenario", "")
        if scenario:
            prefs["common_scenarios"][scenario] = prefs["common_scenarios"].get(scenario, 0) + 1
        
        intent = interaction_result.get("intent", "")
        if intent:
            prefs["intent_frequency"][intent] = prefs["intent_frequency"].get(intent, 0) + 1
        
        for skill in interaction_result.get("skills_used", []):
            prefs["skill_preferences"][skill] = prefs["skill_preferences"].get(skill, 0) + 1
        
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
            "adaptive_rules_count": len(self.adaptive_rules.get("rules", [])),
            "growth_summary": {
                "total_parts": parts_stats["total"],
                "total_interactions": self.evolution_metrics["total_interactions"],
                "average_parts_per_interaction": (
                    self.evolution_metrics["parts_added"] / max(1, self.evolution_metrics["total_interactions"])
                ),
                "auto_adaptations": self.evolution_metrics["auto_adaptations"],
                "pattern_discoveries": self.evolution_metrics["pattern_discoveries"]
            }
        }
    
    def analyze_patterns(self) -> Dict:
        """分析使用模式"""
        
        learning_files = list(self.learning_path.glob("learning_*.jsonl"))
        
        patterns = {
            "common_intents": {},
            "common_scenarios": {},
            "skill_usage": {},
            "success_by_scenario": {},
            "keyword_frequency": {},
            "time_patterns": {}
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
                        
                        for kw in data.get("keywords", []):
                            patterns["keyword_frequency"][kw] = patterns["keyword_frequency"].get(kw, 0) + 1
                        
                        timestamp = data.get("timestamp", "")
                        if timestamp:
                            try:
                                dt = datetime.fromisoformat(timestamp)
                                hour = dt.hour
                                hour_bucket = f"{hour:02d}:00-{hour+1:02d}:00"
                                patterns["time_patterns"][hour_bucket] = patterns["time_patterns"].get(hour_bucket, 0) + 1
                            except Exception:
                                pass
                    
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
        
        high_freq_keywords = [
            kw for kw, count in patterns["keyword_frequency"].items()
            if count >= 5
        ]
        if high_freq_keywords:
            suggestions.append({
                "type": "keyword_optimization",
                "keywords": high_freq_keywords,
                "suggestion": "高频关键词可用于优化意图识别"
            })
        
        return suggestions
    
    def auto_evolve(self) -> Dict:
        """自动进化"""
        
        evolution_result = {
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }
        
        patterns = self.analyze_patterns()
        
        for scenario, stats in patterns["success_by_scenario"].items():
            if stats["total"] >= 5:
                success_rate = stats["success"] / stats["total"]
                if success_rate >= 0.8:
                    rule = {
                        "type": "high_success_scenario",
                        "scenario": scenario,
                        "success_rate": success_rate,
                        "auto_generated": True,
                        "created_at": datetime.now().isoformat()
                    }
                    self._apply_adaptive_rule(rule)
                    evolution_result["actions"].append({
                        "action": "created_high_success_rule",
                        "scenario": scenario
                    })
        
        evolution_result["patterns_analyzed"] = len(patterns["common_scenarios"])
        
        return evolution_result
