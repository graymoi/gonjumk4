"""
持续学习引擎
从交互中自动提取可复用模式并进化
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
import logging

from core.logger import get_system_logger


class LearningPattern:
    """学习模式"""
    
    def __init__(self, pattern_id: str, pattern_type: str, content: str,
                 confidence: float = 0.5, usage_count: int = 0):
        self.pattern_id = pattern_id
        self.pattern_type = pattern_type
        self.content = content
        self.confidence = confidence
        self.usage_count = usage_count
        self.created_at = datetime.now()
        self.last_used = None
        self.success_rate = 0.0
        self.tags = []
    
    def to_dict(self) -> Dict:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "content": self.content,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "success_rate": self.success_rate,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LearningPattern':
        pattern = cls(
            pattern_id=data["pattern_id"],
            pattern_type=data["pattern_type"],
            content=data["content"],
            confidence=data.get("confidence", 0.5),
            usage_count=data.get("usage_count", 0)
        )
        pattern.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("last_used"):
            pattern.last_used = datetime.fromisoformat(data["last_used"])
        pattern.success_rate = data.get("success_rate", 0.0)
        pattern.tags = data.get("tags", [])
        return pattern


class ContinuousLearningEngine:
    """持续学习引擎"""
    
    def __init__(self):
        self.logger = get_system_logger()
        
        self.patterns: Dict[str, LearningPattern] = {}
        self.session_data: List[Dict] = []
        self.max_session_data = 10000
        
        self.learning_rules = self._init_learning_rules()
        self.pattern_extractors = self._init_pattern_extractors()
        
        self.stats = {
            "total_patterns": 0,
            "patterns_applied": 0,
            "learning_events": 0,
            "improvements": 0
        }
        
        self._load_patterns()
    
    def _init_learning_rules(self) -> Dict:
        """初始化学习规则"""
        return {
            "min_confidence": 0.3,
            "confidence_boost": 0.1,
            "confidence_decay": 0.05,
            "min_usage_for_skill": 5,
            "success_threshold": 0.7,
            "pattern_expiry_days": 90
        }
    
    def _init_pattern_extractors(self) -> Dict:
        """初始化模式提取器"""
        return {
            "intent_pattern": self._extract_intent_pattern,
            "workflow_pattern": self._extract_workflow_pattern,
            "skill_pattern": self._extract_skill_pattern,
            "error_pattern": self._extract_error_pattern,
            "optimization_pattern": self._extract_optimization_pattern,
            "user_correction": self._extract_user_correction
        }
    
    def record_session(self, session_data: Dict):
        """记录会话数据"""
        session_data["recorded_at"] = datetime.now().isoformat()
        self.session_data.append(session_data)
        
        if len(self.session_data) > self.max_session_data:
            self.session_data = self.session_data[-self.max_session_data:]
        
        self.logger.info(f"记录会话: {session_data.get('scenario', 'unknown')}", module="ContinuousLearning")
    
    def extract_patterns(self, session_data: Dict) -> List[LearningPattern]:
        """从会话中提取模式"""
        patterns = []
        
        for pattern_type, extractor in self.pattern_extractors.items():
            try:
                extracted = extractor(session_data)
                if extracted:
                    patterns.extend(extracted)
            except Exception as e:
                self.logger.error(f"提取模式失败 [{pattern_type}]: {e}", module="ContinuousLearning")
        
        for pattern in patterns:
            self._add_pattern(pattern)
        
        self.stats["learning_events"] += 1
        
        return patterns
    
    def _extract_intent_pattern(self, session_data: Dict) -> List[LearningPattern]:
        """提取意图模式"""
        patterns = []
        
        intent = session_data.get("intent", {})
        if not intent:
            return patterns
        
        intent_type = intent.get("intent")
        keywords = intent.get("keywords", [])
        
        if intent_type and keywords:
            pattern_id = f"intent_{intent_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="intent_recognition",
                content=json.dumps({
                    "intent_type": intent_type,
                    "keywords": keywords,
                    "confidence": intent.get("confidence", 0.5)
                }),
                confidence=0.6
            )
            pattern.tags = ["intent", intent_type]
            
            patterns.append(pattern)
        
        return patterns
    
    def _extract_workflow_pattern(self, session_data: Dict) -> List[LearningPattern]:
        """提取工作流模式"""
        patterns = []
        
        workflow = session_data.get("workflow", {})
        if not workflow:
            return patterns
        
        workflow_name = workflow.get("workflow_name")
        steps = workflow.get("steps", [])
        
        if workflow_name and steps:
            pattern_id = f"workflow_{workflow_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="workflow_template",
                content=json.dumps({
                    "workflow_name": workflow_name,
                    "steps_count": len(steps),
                    "success": workflow.get("status") == "completed"
                }),
                confidence=0.7 if workflow.get("status") == "completed" else 0.4
            )
            pattern.tags = ["workflow", workflow_name]
            
            patterns.append(pattern)
        
        return patterns
    
    def _extract_skill_pattern(self, session_data: Dict) -> List[LearningPattern]:
        """提取技能模式"""
        patterns = []
        
        skills_used = session_data.get("skills_used", [])
        if not skills_used:
            return patterns
        
        for skill in skills_used:
            pattern_id = f"skill_{skill}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="skill_usage",
                content=json.dumps({
                    "skill_name": skill,
                    "context": session_data.get("scenario", "unknown")
                }),
                confidence=0.6
            )
            pattern.tags = ["skill", skill]
            
            patterns.append(pattern)
        
        return patterns
    
    def _extract_error_pattern(self, session_data: Dict) -> List[LearningPattern]:
        """提取错误模式"""
        patterns = []
        
        errors = session_data.get("errors", [])
        if not errors:
            return patterns
        
        for error in errors:
            pattern_id = f"error_{hash(error.get('message', ''))}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="error_resolution",
                content=json.dumps({
                    "error_type": error.get("type"),
                    "error_message": error.get("message"),
                    "resolution": error.get("resolution")
                }),
                confidence=0.5
            )
            pattern.tags = ["error", error.get("type", "unknown")]
            
            patterns.append(pattern)
        
        return patterns
    
    def _extract_optimization_pattern(self, session_data: Dict) -> List[LearningPattern]:
        """提取优化模式"""
        patterns = []
        
        optimizations = session_data.get("optimizations", [])
        if not optimizations:
            return patterns
        
        for opt in optimizations:
            pattern_id = f"opt_{opt.get('type')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="optimization",
                content=json.dumps({
                    "optimization_type": opt.get("type"),
                    "description": opt.get("description"),
                    "impact": opt.get("impact")
                }),
                confidence=0.7
            )
            pattern.tags = ["optimization", opt.get("type", "general")]
            
            patterns.append(pattern)
        
        return patterns
    
    def _extract_user_correction(self, session_data: Dict) -> List[LearningPattern]:
        """提取用户纠正模式"""
        patterns = []
        
        corrections = session_data.get("user_corrections", [])
        if not corrections:
            return patterns
        
        for correction in corrections:
            pattern_id = f"correction_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            pattern = LearningPattern(
                pattern_id=pattern_id,
                pattern_type="user_correction",
                content=json.dumps({
                    "original": correction.get("original"),
                    "corrected": correction.get("corrected"),
                    "reason": correction.get("reason")
                }),
                confidence=0.8
            )
            pattern.tags = ["correction", "user_feedback"]
            
            patterns.append(pattern)
        
        return patterns
    
    def _add_pattern(self, pattern: LearningPattern):
        """添加模式"""
        if pattern.pattern_id in self.patterns:
            existing = self.patterns[pattern.pattern_id]
            existing.usage_count += 1
            existing.confidence = min(1.0, existing.confidence + self.learning_rules["confidence_boost"])
            existing.last_used = datetime.now()
        else:
            self.patterns[pattern.pattern_id] = pattern
            self.stats["total_patterns"] += 1
        
        self.logger.info(f"添加模式: {pattern.pattern_id} (置信度: {pattern.confidence:.2f})", module="ContinuousLearning")
    
    def find_applicable_patterns(self, context: Dict) -> List[LearningPattern]:
        """查找适用的模式"""
        applicable = []
        
        intent_type = context.get("intent_type")
        scenario = context.get("scenario")
        keywords = context.get("keywords", [])
        
        for pattern in self.patterns.values():
            if pattern.confidence < self.learning_rules["min_confidence"]:
                continue
            
            if intent_type and intent_type in pattern.tags:
                applicable.append(pattern)
            elif scenario and scenario in pattern.tags:
                applicable.append(pattern)
            elif any(kw in pattern.tags for kw in keywords):
                applicable.append(pattern)
        
        applicable.sort(key=lambda p: p.confidence, reverse=True)
        
        return applicable[:10]
    
    def apply_pattern(self, pattern_id: str, context: Dict) -> Optional[Dict]:
        """应用模式"""
        if pattern_id not in self.patterns:
            return None
        
        pattern = self.patterns[pattern_id]
        pattern.usage_count += 1
        pattern.last_used = datetime.now()
        
        self.stats["patterns_applied"] += 1
        
        self.logger.info(f"应用模式: {pattern_id}", module="ContinuousLearning")
        
        return {
            "pattern_id": pattern_id,
            "pattern_type": pattern.pattern_type,
            "content": json.loads(pattern.content),
            "confidence": pattern.confidence
        }
    
    def update_pattern_success(self, pattern_id: str, success: bool):
        """更新模式成功率"""
        if pattern_id not in self.patterns:
            return
        
        pattern = self.patterns[pattern_id]
        
        if success:
            pattern.success_rate = (pattern.success_rate * pattern.usage_count + 1) / (pattern.usage_count + 1)
            pattern.confidence = min(1.0, pattern.confidence + self.learning_rules["confidence_boost"])
        else:
            pattern.success_rate = (pattern.success_rate * pattern.usage_count) / (pattern.usage_count + 1)
            pattern.confidence = max(0.0, pattern.confidence - self.learning_rules["confidence_decay"])
        
        self.logger.info(f"更新模式成功率: {pattern_id} - {pattern.success_rate:.2%}", module="ContinuousLearning")
    
    def evolve_patterns(self):
        """进化模式"""
        print("\n🧠 进化学习模式...")
        
        expired_patterns = []
        for pattern_id, pattern in self.patterns.items():
            if pattern.last_used:
                days_since_use = (datetime.now() - pattern.last_used).days
                if days_since_use > self.learning_rules["pattern_expiry_days"]:
                    expired_patterns.append(pattern_id)
            
            if pattern.confidence < self.learning_rules["min_confidence"] * 0.5:
                expired_patterns.append(pattern_id)
        
        for pattern_id in expired_patterns:
            del self.patterns[pattern_id]
            print(f"  🗑️ 移除过期模式: {pattern_id}")
        
        if expired_patterns:
            self.stats["total_patterns"] = len(self.patterns)
        
        self._save_patterns()
        
        print(f"✅ 进化完成: {len(self.patterns)}个活跃模式")
    
    def generate_skill_from_patterns(self) -> List[Dict]:
        """从模式生成技能"""
        skills_to_create = []
        
        pattern_groups = defaultdict(list)
        for pattern in self.patterns.values():
            if pattern.pattern_type == "workflow_template":
                workflow_name = json.loads(pattern.content).get("workflow_name")
                if workflow_name:
                    pattern_groups[workflow_name].append(pattern)
        
        for workflow_name, patterns in pattern_groups.items():
            if len(patterns) >= self.learning_rules["min_usage_for_skill"]:
                avg_success = sum(p.success_rate for p in patterns) / len(patterns)
                
                if avg_success >= self.learning_rules["success_threshold"]:
                    skill = {
                        "skill_name": f"auto_{workflow_name}",
                        "skill_type": "workflow",
                        "patterns": [p.pattern_id for p in patterns],
                        "confidence": avg_success,
                        "usage_count": sum(p.usage_count for p in patterns)
                    }
                    
                    skills_to_create.append(skill)
                    self.stats["improvements"] += 1
        
        if skills_to_create:
            print(f"\n🎯 发现可生成技能: {len(skills_to_create)}个")
            for skill in skills_to_create:
                print(f"  - {skill['skill_name']} (置信度: {skill['confidence']:.2%})")
        
        return skills_to_create
    
    def get_learning_report(self) -> Dict:
        """获取学习报告"""
        pattern_types = Counter(p.pattern_type for p in self.patterns.values())
        
        return {
            "stats": self.stats,
            "pattern_types": dict(pattern_types),
            "top_patterns": [
                {
                    "pattern_id": p.pattern_id,
                    "type": p.pattern_type,
                    "confidence": p.confidence,
                    "usage": p.usage_count
                }
                for p in sorted(
                    self.patterns.values(),
                    key=lambda x: (x.confidence, x.usage_count),
                    reverse=True
                )[:10]
            ],
            "recent_patterns": [
                p.to_dict()
                for p in sorted(
                    self.patterns.values(),
                    key=lambda x: x.created_at,
                    reverse=True
                )[:5]
            ]
        }
    
    def _save_patterns(self):
        """保存模式"""
        patterns_file = Path("knowledge/learning_patterns.json")
        patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "patterns": {pid: p.to_dict() for pid, p in self.patterns.items()},
            "stats": self.stats,
            "last_update": datetime.now().isoformat()
        }
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_patterns(self):
        """加载模式"""
        patterns_file = Path("knowledge/learning_patterns.json")
        
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.patterns = {
                    pid: LearningPattern.from_dict(pdata)
                    for pid, pdata in data.get("patterns", {}).items()
                }
                self.stats = data.get("stats", self.stats)
                
                self.logger.info(f"加载 {len(self.patterns)} 个学习模式", module="ContinuousLearning")
                
            except Exception as e:
                self.logger.error(f"加载模式失败: {e}", module="ContinuousLearning")
