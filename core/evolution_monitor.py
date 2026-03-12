"""
进化监控模块
监控系统进化状态和健康度
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

from core.logger import get_system_logger


class EvolutionMonitor:
    """进化监控器"""
    
    def __init__(self):
        self.logger = get_system_logger()
        self.metrics_path = Path("config/evolution_metrics.json")
        self.learning_path = Path("logs/learning")
        self.alerts_path = Path("logs/alerts")
        self.alerts_path.mkdir(parents=True, exist_ok=True)
        
        self.thresholds = {
            "success_rate_min": 0.7,
            "interaction_count_min": 10,
            "parts_growth_min": 1,
            "error_rate_max": 0.3
        }
    
    def get_system_health(self) -> Dict:
        """获取系统健康状态"""
        
        health = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "metrics": {},
            "alerts": [],
            "recommendations": []
        }
        
        metrics = self._load_metrics()
        health["metrics"] = metrics
        
        success_rate = self._calculate_success_rate(metrics)
        if success_rate < self.thresholds["success_rate_min"]:
            health["status"] = "warning"
            health["alerts"].append({
                "level": "warning",
                "message": f"成功率低于阈值: {success_rate:.2%} < {self.thresholds['success_rate_min']:.2%}",
                "metric": "success_rate"
            })
        
        total_interactions = metrics.get("metrics", {}).get("total_interactions", 0)
        if total_interactions < self.thresholds["interaction_count_min"]:
            health["alerts"].append({
                "level": "info",
                "message": f"交互次数较少: {total_interactions}",
                "metric": "interaction_count"
            })
        
        parts_added = metrics.get("metrics", {}).get("parts_added", 0)
        if parts_added < self.thresholds["parts_growth_min"]:
            health["recommendations"].append({
                "type": "growth",
                "message": "知识库增长缓慢，建议增加交互频率"
            })
        
        return health
    
    def _load_metrics(self) -> Dict:
        """加载指标"""
        if self.metrics_path.exists():
            try:
                with open(self.metrics_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"metrics": {}}
    
    def _calculate_success_rate(self, metrics: Dict) -> float:
        """计算成功率"""
        if isinstance(metrics, str):
            return 1.0
        
        total = metrics.get("total_interactions", 0)
        successful = metrics.get("successful_outputs", 0)
        
        if total == 0:
            return 1.0
        
        return successful / total
    
    def get_evolution_trends(self, days: int = 7) -> Dict:
        """获取进化趋势"""
        
        trends = {
            "period_days": days,
            "interactions": [],
            "success_rates": [],
            "parts_added": [],
            "daily_stats": {}
        }
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        learning_files = list(self.learning_path.glob("learning_*.jsonl"))
        
        daily_data = defaultdict(lambda: {
            "interactions": 0,
            "success": 0,
            "parts": 0
        })
        
        for lf in learning_files:
            try:
                file_date_str = lf.stem.replace("learning_", "")
                file_date = datetime.strptime(file_date_str, "%Y%m%d")
                
                if start_date <= file_date <= end_date:
                    with open(lf, 'r', encoding='utf-8') as f:
                        for line in f:
                            if not line.strip():
                                continue
                            try:
                                data = json.loads(line)
                                date_key = file_date.strftime("%Y-%m-%d")
                                daily_data[date_key]["interactions"] += 1
                                if data.get("success", False):
                                    daily_data[date_key]["success"] += 1
                                daily_data[date_key]["parts"] += data.get("parts_extracted", 0)
                            except json.JSONDecodeError:
                                continue
            except Exception:
                continue
        
        for date_key in sorted(daily_data.keys()):
            data = daily_data[date_key]
            trends["daily_stats"][date_key] = data
            trends["interactions"].append(data["interactions"])
            trends["success_rates"].append(
                data["success"] / data["interactions"] if data["interactions"] > 0 else 0
            )
            trends["parts_added"].append(data["parts"])
        
        return trends
    
    def check_alerts(self) -> List[Dict]:
        """检查告警"""
        
        alerts = []
        health = self.get_system_health()
        
        for alert in health.get("alerts", []):
            if alert["level"] == "warning":
                alerts.append(alert)
        
        if len(alerts) > 0:
            self._save_alerts(alerts)
        
        return alerts
    
    def _save_alerts(self, alerts: List[Dict]):
        """保存告警"""
        alert_file = self.alerts_path / f"alerts_{datetime.now().strftime('%Y%m%d')}.json"
        
        existing_alerts = []
        if alert_file.exists():
            try:
                with open(alert_file, 'r', encoding='utf-8') as f:
                    existing_alerts = json.load(f)
            except Exception:
                pass
        
        existing_alerts.extend(alerts)
        
        with open(alert_file, 'w', encoding='utf-8') as f:
            json.dump(existing_alerts, f, ensure_ascii=False, indent=2)
    
    def get_performance_metrics(self) -> Dict:
        """获取性能指标"""
        
        metrics = self._load_metrics()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_interactions": metrics.get("metrics", {}).get("total_interactions", 0),
            "successful_outputs": metrics.get("metrics", {}).get("successful_outputs", 0),
            "parts_added": metrics.get("metrics", {}).get("parts_added", 0),
            "auto_adaptations": metrics.get("metrics", {}).get("auto_adaptations", 0),
            "pattern_discoveries": metrics.get("metrics", {}).get("pattern_discoveries", 0),
            "success_rate": self._calculate_success_rate(metrics)
        }
    
    def generate_report(self) -> Dict:
        """生成监控报告"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "health": self.get_system_health(),
            "trends": self.get_evolution_trends(),
            "performance": self.get_performance_metrics(),
            "alerts": self.check_alerts()
        }
    
    def get_adaptive_rules_status(self) -> Dict:
        """获取自适应规则状态"""
        
        rules_file = Path("config/adaptive_rules.json")
        
        if not rules_file.exists():
            return {
                "status": "no_rules",
                "count": 0,
                "rules": []
            }
        
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            
            return {
                "status": "active",
                "count": len(rules_data.get("rules", [])),
                "auto_apply": rules_data.get("auto_apply", True),
                "confidence_threshold": rules_data.get("confidence_threshold", 0.7),
                "rules": rules_data.get("rules", [])[-5:]
            }
        except Exception:
            return {
                "status": "error",
                "count": 0,
                "rules": []
            }
    
    def get_user_preferences_summary(self) -> Dict:
        """获取用户偏好摘要"""
        
        prefs_file = Path("config/user_preferences.json")
        
        if not prefs_file.exists():
            return {
                "status": "no_preferences",
                "common_scenarios": {},
                "intent_frequency": {}
            }
        
        try:
            with open(prefs_file, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
            
            top_scenarios = sorted(
                prefs.get("common_scenarios", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            top_intents = sorted(
                prefs.get("intent_frequency", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            return {
                "status": "active",
                "updated_at": prefs.get("updated_at"),
                "top_scenarios": dict(top_scenarios),
                "top_intents": dict(top_intents),
                "total_feedback": len(prefs.get("feedback_patterns", []))
            }
        except Exception:
            return {
                "status": "error",
                "common_scenarios": {},
                "intent_frequency": {}
            }
