"""
持续优化模块
自动检测问题并持续改进系统
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

from core.logger import get_system_logger
from core.evolution_engine import EvolutionEngine
from core.evolution_monitor import EvolutionMonitor
from core.intent_analyzer import IntentAnalyzer
from core.workflow_engine import WorkflowEngine


class ContinuousOptimizer:
    """持续优化器"""
    
    def __init__(self):
        self.logger = get_system_logger()
        self.evolution_engine = EvolutionEngine()
        self.evolution_monitor = EvolutionMonitor()
        self.intent_analyzer = IntentAnalyzer()
        self.workflow_engine = WorkflowEngine()
        
        self.optimization_path = Path("logs/optimization")
        self.optimization_path.mkdir(parents=True, exist_ok=True)
        
        self.optimization_history = []
        self.improvement_queue = []
        
        self.optimization_rules = self._load_optimization_rules()
    
    def _load_optimization_rules(self) -> Dict:
        """加载优化规则"""
        rules_file = Path("config/optimization_rules.json")
        if rules_file.exists():
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "version": "1.0.0",
            "rules": [
                {
                    "name": "low_success_rate",
                    "condition": "success_rate < 0.7",
                    "action": "optimize_workflow",
                    "priority": "high"
                },
                {
                    "name": "low_usage_skill",
                    "condition": "skill_usage < 2",
                    "action": "review_skill",
                    "priority": "medium"
                },
                {
                    "name": "frequent_errors",
                    "condition": "error_rate > 0.3",
                    "action": "fix_errors",
                    "priority": "high"
                },
                {
                    "name": "slow_growth",
                    "condition": "parts_growth < 1",
                    "action": "enhance_collection",
                    "priority": "low"
                }
            ],
            "auto_apply": True,
            "check_interval_hours": 24
        }
    
    def run_optimization_cycle(self) -> Dict:
        """运行优化循环"""
        
        cycle_result = {
            "timestamp": datetime.now().isoformat(),
            "cycle_id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "checks": [],
            "improvements": [],
            "applied": []
        }
        
        health = self.evolution_monitor.get_system_health()
        cycle_result["checks"].append({
            "type": "health_check",
            "status": health["status"],
            "alerts": len(health.get("alerts", []))
        })
        
        patterns = self.evolution_engine.analyze_patterns()
        cycle_result["checks"].append({
            "type": "pattern_analysis",
            "intents": len(patterns["common_intents"]),
            "scenarios": len(patterns["common_scenarios"]),
            "skills": len(patterns["skill_usage"])
        })
        
        improvements = self._detect_improvements(health, patterns)
        cycle_result["improvements"] = improvements
        
        if self.optimization_rules.get("auto_apply", True):
            for improvement in improvements:
                if self._apply_improvement(improvement):
                    cycle_result["applied"].append(improvement)
        
        self._save_optimization_cycle(cycle_result)
        
        return cycle_result
    
    def _detect_improvements(self, health: Dict, patterns: Dict) -> List[Dict]:
        """检测改进点"""
        
        improvements = []
        
        if isinstance(health, str):
            health = {}
        
        if isinstance(patterns, str):
            patterns = {}
        
        success_rate = self.evolution_monitor._calculate_success_rate(
            health.get("metrics", {})
        )
        
        if success_rate < 0.7:
            improvements.append({
                "type": "low_success_rate",
                "priority": "high",
                "current_value": success_rate,
                "target_value": 0.8,
                "action": "optimize_workflow",
                "suggestion": f"成功率 {success_rate:.2%} 低于阈值，需要优化工作流"
            })
        
        for scenario, stats in patterns.get("success_by_scenario", {}).items():
            if stats["total"] >= 3:
                rate = stats["success"] / stats["total"]
                if rate < 0.6:
                    improvements.append({
                        "type": "scenario_optimization",
                        "priority": "high",
                        "scenario": scenario,
                        "current_rate": rate,
                        "action": "redesign_workflow",
                        "suggestion": f"场景 '{scenario}' 成功率仅 {rate:.2%}，需要重新设计工作流"
                    })
        
        low_usage_skills = [
            skill for skill, count in patterns.get("skill_usage", {}).items()
            if count < 2
        ]
        if len(low_usage_skills) > 0:
            improvements.append({
                "type": "skill_cleanup",
                "priority": "medium",
                "skills": low_usage_skills,
                "action": "review_skills",
                "suggestion": f"{len(low_usage_skills)} 个技能使用频率过低，建议审查"
            })
        
        high_freq_keywords = [
            kw for kw, count in patterns.get("keyword_frequency", {}).items()
            if count >= 5
        ]
        if high_freq_keywords:
            improvements.append({
                "type": "keyword_enhancement",
                "priority": "low",
                "keywords": high_freq_keywords,
                "action": "add_to_patterns",
                "suggestion": f"{len(high_freq_keywords)} 个高频关键词可添加到意图识别"
            })
        
        return improvements
    
    def _apply_improvement(self, improvement: Dict) -> bool:
        """应用改进"""
        
        action = improvement.get("action")
        
        if action == "optimize_workflow":
            return self._optimize_workflow(improvement)
        elif action == "redesign_workflow":
            return self._redesign_workflow(improvement)
        elif action == "review_skills":
            return self._review_skills(improvement)
        elif action == "add_to_patterns":
            return self._add_to_patterns(improvement)
        
        return False
    
    def _optimize_workflow(self, improvement: Dict) -> bool:
        """优化工作流"""
        
        self.logger.info(
            f"优化工作流: {improvement.get('suggestion', '')}",
            module="optimizer"
        )
        
        rule = {
            "type": "workflow_optimization",
            "trigger": "low_success_rate",
            "created_at": datetime.now().isoformat(),
            "improvement": improvement
        }
        
        self._save_adaptive_rule(rule)
        
        return True
    
    def _redesign_workflow(self, improvement: Dict) -> bool:
        """重新设计工作流"""
        
        scenario = improvement.get("scenario", "")
        
        self.logger.info(
            f"重新设计工作流: {scenario}",
            module="optimizer"
        )
        
        rule = {
            "type": "workflow_redesign",
            "scenario": scenario,
            "created_at": datetime.now().isoformat(),
            "improvement": improvement
        }
        
        self._save_adaptive_rule(rule)
        
        return True
    
    def _review_skills(self, improvement: Dict) -> bool:
        """审查技能"""
        
        skills = improvement.get("skills", [])
        
        self.logger.info(
            f"审查技能: {skills}",
            module="optimizer"
        )
        
        return True
    
    def _add_to_patterns(self, improvement: Dict) -> bool:
        """添加到模式"""
        
        keywords = improvement.get("keywords", [])
        
        self.logger.info(
            f"添加关键词到模式: {keywords}",
            module="optimizer"
        )
        
        return True
    
    def _save_adaptive_rule(self, rule: Dict):
        """保存自适应规则"""
        
        rules_file = Path("config/adaptive_rules.json")
        
        if rules_file.exists():
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    rules_data = json.load(f)
            except Exception:
                rules_data = {"version": "1.0.0", "rules": []}
        else:
            rules_data = {"version": "1.0.0", "rules": []}
        
        rules_data["rules"].append(rule)
        
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, ensure_ascii=False, indent=2)
    
    def _save_optimization_cycle(self, cycle_result: Dict):
        """保存优化循环结果"""
        
        cycle_file = self.optimization_path / f"cycle_{cycle_result['cycle_id']}.json"
        
        with open(cycle_file, 'w', encoding='utf-8') as f:
            json.dump(cycle_result, f, ensure_ascii=False, indent=2)
        
        self.optimization_history.append(cycle_result)
    
    def get_optimization_stats(self) -> Dict:
        """获取优化统计"""
        
        cycle_files = list(self.optimization_path.glob("cycle_*.json"))
        
        total_cycles = len(cycle_files)
        total_improvements = 0
        total_applied = 0
        
        for cf in cycle_files:
            try:
                with open(cf, 'r', encoding='utf-8') as f:
                    cycle = json.load(f)
                    total_improvements += len(cycle.get("improvements", []))
                    total_applied += len(cycle.get("applied", []))
            except Exception:
                pass
        
        return {
            "total_cycles": total_cycles,
            "total_improvements_detected": total_improvements,
            "total_improvements_applied": total_applied,
            "application_rate": total_applied / total_improvements if total_improvements > 0 else 0
        }
    
    def auto_improve_intent_patterns(self) -> Dict:
        """自动改进意图模式"""
        
        patterns = self.evolution_engine.analyze_patterns()
        
        improvements = {
            "timestamp": datetime.now().isoformat(),
            "new_patterns": [],
            "updated_patterns": []
        }
        
        for intent, count in patterns.get("common_intents", {}).items():
            if count >= 5:
                improvements["updated_patterns"].append({
                    "intent": intent,
                    "frequency": count,
                    "status": "high_frequency"
                })
        
        for keyword, count in patterns.get("keyword_frequency", {}).items():
            if count >= 10:
                improvements["new_patterns"].append({
                    "keyword": keyword,
                    "frequency": count,
                    "suggestion": "可添加到意图关键词"
                })
        
        return improvements
    
    def suggest_new_workflows(self) -> List[Dict]:
        """建议新工作流"""
        
        patterns = self.evolution_engine.analyze_patterns()
        suggestions = []
        
        for scenario, stats in patterns.get("success_by_scenario", {}).items():
            if stats["total"] >= 3 and stats["success"] / stats["total"] >= 0.8:
                suggestions.append({
                    "type": "new_workflow_template",
                    "scenario": scenario,
                    "success_rate": stats["success"] / stats["total"],
                    "suggestion": f"场景 '{scenario}' 成功率高，可创建专用工作流模板"
                })
        
        return suggestions
    
    def cleanup_old_data(self, days: int = 30) -> Dict:
        """清理旧数据"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cleaned = {
            "logs": 0,
            "outputs": 0,
            "cache": 0
        }
        
        for log_type in ["interactions", "workflows", "errors"]:
            log_path = Path("logs") / log_type
            if log_path.exists():
                for log_file in log_path.glob("*.json*"):
                    try:
                        file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                        if file_mtime < cutoff_date:
                            log_file.unlink()
                            cleaned["logs"] += 1
                    except Exception:
                        pass
        
        return cleaned
    
    def generate_improvement_report(self) -> Dict:
        """生成改进报告"""
        
        health = self.evolution_monitor.get_system_health()
        patterns = self.evolution_engine.analyze_patterns()
        stats = self.get_optimization_stats()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": {
                "status": health["status"],
                "alerts": len(health.get("alerts", []))
            },
            "optimization_stats": stats,
            "top_intents": list(patterns.get("common_intents", {}).keys())[:5],
            "top_scenarios": list(patterns.get("common_scenarios", {}).keys())[:5],
            "suggestions": self.suggest_new_workflows()
        }
