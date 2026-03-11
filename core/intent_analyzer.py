"""
意图分析器模块
负责理解用户输入的真实意图
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class IntentAnalyzer:
    """意图分析器"""
    
    def __init__(self):
        self.logs_dir = Path("logs/interactions")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.intent_patterns = {
            "项目谋划": ["谋划", "项目", "申报", "包装"],
            "项目筛选": ["筛选", "排序", "选择", "优先级"],
            "政策研究": ["研究", "政策", "分析", "趋势"],
            "流程指导": ["流程", "指导", "如何", "拿钱"],
            "快速组装": ["组装", "宣讲", "PPT", "材料"],
            "数据管理": ["管理", "采集", "入库", "归档"],
            "合同咨询": ["合同", "依据", "咨询", "特殊"]
        }
    
    def analyze(self, user_input: str) -> Dict:
        """分析用户意图"""
        
        intent_result = {
            "user_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "intent": self._detect_intent(user_input),
            "keywords": self._extract_keywords(user_input),
            "entities": self._extract_entities(user_input),
            "confidence": 0.0
        }
        
        intent_result["confidence"] = self._calculate_confidence(intent_result)
        
        self._log_interaction(intent_result)
        
        return intent_result
    
    def _detect_intent(self, user_input: str) -> str:
        """检测意图类型"""
        
        scores = {}
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for kw in keywords if kw in user_input)
            if score > 0:
                scores[intent] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "通用咨询"
    
    def _extract_keywords(self, user_input: str) -> List[str]:
        """提取关键词"""
        
        keywords = []
        
        project_types = ["老旧小区", "城市更新", "乡村振兴", "基础设施", "水利", "交通"]
        for pt in project_types:
            if pt in user_input:
                keywords.append(pt)
        
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(万|亿|万元|亿元)'
        amounts = re.findall(amount_pattern, user_input)
        if amounts:
            keywords.append(f"{amounts[0][0]}{amounts[0][1]}")
        
        return keywords
    
    def _extract_entities(self, user_input: str) -> Dict:
        """提取实体"""
        
        entities = {}
        
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(万|亿|万元|亿元)'
        amounts = re.findall(amount_pattern, user_input)
        if amounts:
            entities["投资额"] = f"{amounts[0][0]}{amounts[0][1]}"
        
        project_types = {
            "老旧小区": "老旧小区改造",
            "城市更新": "城市更新",
            "乡村振兴": "乡村振兴",
            "基础设施": "基础设施建设",
            "水利": "水利工程",
            "交通": "交通设施"
        }
        for keyword, project_type in project_types.items():
            if keyword in user_input:
                entities["项目类型"] = project_type
                break
        
        return entities
    
    def _calculate_confidence(self, intent_result: Dict) -> float:
        """计算置信度"""
        
        confidence = 0.5
        
        if intent_result["keywords"]:
            confidence += 0.1 * len(intent_result["keywords"])
        
        if intent_result["entities"]:
            confidence += 0.1 * len(intent_result["entities"])
        
        if intent_result["intent"] != "通用咨询":
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _log_interaction(self, intent_result: Dict):
        """记录交互日志"""
        
        log_file = self.logs_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(intent_result, f, ensure_ascii=False, indent=2)
    
    def generate_scenario(self, intent_result: Dict) -> Dict:
        """生成场景描述"""
        
        scenario = {
            "name": self._generate_scenario_name(intent_result),
            "type": intent_result["intent"],
            "requirements": {
                "项目类型": intent_result["entities"].get("项目类型", "未指定"),
                "投资额": intent_result["entities"].get("投资额", "未指定"),
                "关键词": intent_result["keywords"]
            },
            "required_skills": self._get_required_skills(intent_result["intent"]),
            "required_data": self._get_required_data(intent_result),
            "created_at": datetime.now().isoformat()
        }
        
        return scenario
    
    def _generate_scenario_name(self, intent_result: Dict) -> str:
        """生成场景名称"""
        
        project_type = intent_result["entities"].get("项目类型", "")
        intent = intent_result["intent"]
        
        if project_type:
            return f"{project_type}{intent}"
        
        return intent
    
    def _get_required_skills(self, intent: str) -> List[str]:
        """获取所需技能"""
        
        skills_map = {
            "项目谋划": ["research-lookup", "scientific-critical-thinking", "office"],
            "项目筛选": ["research-lookup", "xlsx", "scientific-critical-thinking"],
            "政策研究": ["research-lookup", "perplexity-search", "scientific-critical-thinking"],
            "流程指导": ["research-lookup", "scientific-critical-thinking", "office"],
            "快速组装": ["markitdown", "pptx", "office"],
            "数据管理": ["agent-browser", "pandas", "xlsx"],
            "合同咨询": ["research-lookup", "scientific-critical-thinking", "office"]
        }
        
        return skills_map.get(intent, ["research-lookup", "office"])
    
    def _get_required_data(self, intent_result: Dict) -> List[str]:
        """获取所需数据"""
        
        data = []
        
        project_type = intent_result["entities"].get("项目类型", "")
        if project_type:
            data.append(f"{project_type}政策")
        
        intent = intent_result["intent"]
        if "资金" in intent or "谋划" in intent:
            data.append("专项债券政策")
            data.append("中央预算内投资政策")
        
        return data
