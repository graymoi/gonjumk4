"""
意图分析器模块
负责理解用户输入的真实意图
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from core.logger import get_system_logger


class IntentAnalyzer:
    """意图分析器"""
    
    def __init__(self):
        self.logger = get_system_logger()
        self.logs_dir = Path("logs/interactions")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.intent_patterns = {
            "项目谋划": ["谋划", "项目", "申报", "包装", "设计", "策划", "立项", "精准谋划"],
            "项目筛选": ["筛选", "排序", "选择", "优先级", "评估", "比较", "排名"],
            "政策研究": ["研究", "政策", "分析", "趋势", "解读", "影响", "理解"],
            "流程指导": ["流程", "指导", "如何", "拿钱", "申请", "办理", "操作"],
            "快速组装": ["组装", "宣讲", "PPT", "材料", "生成", "制作", "报告"],
            "数据管理": ["管理", "采集", "入库", "归档", "更新", "维护", "整理"],
            "合同咨询": ["合同", "依据", "咨询", "特殊", "合规", "风险", "法律"],
            "组合谋划": ["组合", "多项目", "打包", "整合", "统筹"],
            "打捆申报": ["打捆", "捆绑", "批量", "集中", "打包申报"],
            "战略规划": ["战略", "规划", "长期", "发展", "布局", "顶层"],
            "新闻监测": ["新闻", "动态", "监测", "最新", "更新", "资讯"],
            "资金申请": ["资金", "申请", "融资", "贷款", "债券", "预算"]
        }
        
        self.project_types = {
            "老旧小区": "老旧小区改造",
            "城市更新": "城市更新",
            "乡村振兴": "乡村振兴",
            "基础设施": "基础设施建设",
            "水利": "水利工程",
            "交通": "交通设施",
            "管网": "管网改造",
            "地下管网": "地下管网改造",
            "供水": "供水设施",
            "供热": "供热设施",
            "污水处理": "污水处理",
            "垃圾处理": "垃圾处理",
            "公园": "公园绿地",
            "停车场": "停车场建设",
            "充电桩": "充电基础设施",
            "充电基础设施": "充电基础设施",
            "保障房": "保障性住房",
            "棚改": "棚户区改造",
            "电梯更新": "老旧电梯更新",
            "设备更新": "设备更新改造",
            "产业园": "产业园区更新",
            "科创园": "科创园区",
            "养老": "养老设施",
            "医养结合": "医养结合机构"
        }
        
        self.funding_sources = {
            "专项债券": ["专项债", "专项债券", "地方债"],
            "中央预算": ["中央预算", "预算内投资", "中央资金"],
            "超长期特别国债": ["超长期特别国债", "特别国债", "超长期国债"],
            "REITs": ["REITs", "不动产投资信托"],
            "PPP": ["PPP", "政府和社会资本合作"],
            "政策性贷款": ["政策性贷款", "政策银行", "国开行", "农发行"]
        }
    
    def analyze(self, user_input: str) -> Dict:
        """分析用户意图"""
        
        intent_result = {
            "user_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "intent": self._detect_intent(user_input),
            "keywords": self._extract_keywords(user_input),
            "entities": self._extract_entities(user_input),
            "semantic": self._semantic_analysis(user_input),
            "confidence": 0.0
        }
        
        intent_result["confidence"] = self._calculate_confidence(intent_result)
        
        self.logger.log_interaction(intent_result)
        
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
        
        for pt in self.project_types.keys():
            if pt in user_input:
                keywords.append(pt)
        
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(万|亿|万元|亿元)'
        amounts = re.findall(amount_pattern, user_input)
        if amounts:
            keywords.append(f"{amounts[0][0]}{amounts[0][1]}")
        
        for funding, aliases in self.funding_sources.items():
            for alias in aliases:
                if alias in user_input:
                    keywords.append(funding)
                    break
        
        location_pattern = r'([\u4e00-\u9fa5]{2,4}(?:省|市|县|区))'
        locations = re.findall(location_pattern, user_input)
        keywords.extend(locations)
        
        return list(set(keywords))
    
    def _extract_entities(self, user_input: str) -> Dict:
        """提取实体"""
        
        entities = {}
        
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(万|亿|万元|亿元)'
        amounts = re.findall(amount_pattern, user_input)
        if amounts:
            entities["投资额"] = f"{amounts[0][0]}{amounts[0][1]}"
            entities["投资额数值"] = float(amounts[0][0])
            entities["投资额单位"] = amounts[0][1]
        
        for keyword, project_type in self.project_types.items():
            if keyword in user_input:
                entities["项目类型"] = project_type
                entities["项目类型关键词"] = keyword
                break
        
        for funding, aliases in self.funding_sources.items():
            for alias in aliases:
                if alias in user_input:
                    entities["资金来源"] = funding
                    break
        
        location_pattern = r'([\u4e00-\u9fa5]{2,4})(?:省|市|县|区)'
        locations = re.findall(location_pattern, user_input)
        if locations:
            entities["地区"] = locations[0]
        
        year_pattern = r'(20\d{2})年?'
        years = re.findall(year_pattern, user_input)
        if years:
            entities["年份"] = years[0]
        
        return entities
    
    def _semantic_analysis(self, user_input: str) -> Dict:
        """语义分析"""
        
        analysis = {
            "main_action": None,
            "target_object": None,
            "constraints": [],
            "context": {}
        }
        
        action_patterns = [
            (r'(谋划|设计|策划|立项)', 'create'),
            (r'(筛选|选择|评估|比较)', 'filter'),
            (r'(研究|分析|解读)', 'research'),
            (r'(组装|生成|制作)', 'assemble'),
            (r'(管理|维护|更新)', 'manage'),
            (r'(指导|如何|怎么)', 'guide'),
            (r'(咨询|询问)', 'consult')
        ]
        
        for pattern, action in action_patterns:
            if re.search(pattern, user_input):
                analysis["main_action"] = action
                break
        
        for pt in self.project_types.values():
            if pt in user_input:
                analysis["target_object"] = pt
                break
        
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(万|亿|万元|亿元)'
        amounts = re.findall(amount_pattern, user_input)
        if amounts:
            analysis["constraints"].append({
                "type": "budget",
                "value": f"{amounts[0][0]}{amounts[0][1]}"
            })
        
        for funding in self.funding_sources.keys():
            if funding in user_input:
                analysis["constraints"].append({
                    "type": "funding_source",
                    "value": funding
                })
        
        return analysis
    
    def _calculate_confidence(self, intent_result: Dict) -> float:
        """计算置信度"""
        
        confidence = 0.5
        
        if intent_result["keywords"]:
            confidence += 0.05 * len(intent_result["keywords"])
        
        if intent_result["entities"]:
            confidence += 0.05 * len(intent_result["entities"])
        
        if intent_result["intent"] != "通用咨询":
            confidence += 0.2
        
        if intent_result.get("semantic", {}).get("main_action"):
            confidence += 0.1
        
        if intent_result.get("semantic", {}).get("target_object"):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def generate_scenario(self, intent_result: Dict) -> Dict:
        """生成场景描述"""
        
        scenario = {
            "name": self._generate_scenario_name(intent_result),
            "type": intent_result["intent"],
            "requirements": {
                "项目类型": intent_result["entities"].get("项目类型", "未指定"),
                "投资额": intent_result["entities"].get("投资额", "未指定"),
                "资金来源": intent_result["entities"].get("资金来源", "未指定"),
                "地区": intent_result["entities"].get("地区", "未指定"),
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
        funding_source = intent_result["entities"].get("资金来源", "")
        intent = intent_result["intent"]
        
        parts = []
        if funding_source:
            parts.append(funding_source)
        if project_type:
            parts.append(project_type)
        parts.append(intent)
        
        return "".join(parts)
    
    def _get_required_skills(self, intent: str) -> List[str]:
        """获取所需技能"""
        
        skills_map = {
            "项目谋划": ["research-lookup", "scientific-critical-thinking", "office"],
            "项目筛选": ["research-lookup", "xlsx", "scientific-critical-thinking"],
            "政策研究": ["research-lookup", "perplexity-search", "scientific-critical-thinking"],
            "流程指导": ["research-lookup", "scientific-critical-thinking", "office"],
            "快速组装": ["markitdown", "pptx", "office"],
            "数据管理": ["agent-browser", "pandas", "xlsx"],
            "合同咨询": ["research-lookup", "scientific-critical-thinking", "office"],
            "组合谋划": ["research-lookup", "scientific-critical-thinking", "office"],
            "打捆申报": ["research-lookup", "scientific-critical-thinking", "office"],
            "战略规划": ["research-lookup", "scientific-critical-thinking", "office"],
            "新闻监测": ["perplexity-search", "agent-browser"],
            "资金申请": ["research-lookup", "scientific-critical-thinking", "office"]
        }
        
        return skills_map.get(intent, ["research-lookup", "office"])
    
    def _get_required_data(self, intent_result: Dict) -> List[str]:
        """获取所需数据"""
        
        data = []
        
        project_type = intent_result["entities"].get("项目类型", "")
        if project_type:
            data.append(f"{project_type}政策")
        
        funding_source = intent_result["entities"].get("资金来源", "")
        if funding_source:
            data.append(f"{funding_source}政策")
        
        intent = intent_result["intent"]
        if "谋划" in intent or "资金" in intent:
            if "专项债券政策" not in data:
                data.append("专项债券政策")
            if "中央预算内投资政策" not in data:
                data.append("中央预算内投资政策")
        
        return data
    
    def get_intent_suggestions(self, user_input: str) -> List[str]:
        """获取意图建议"""
        
        suggestions = []
        
        detected_intent = self._detect_intent(user_input)
        
        if detected_intent == "通用咨询":
            suggestions.append("您可以尝试：")
            suggestions.append("  - 谋划一个老旧小区改造项目")
            suggestions.append("  - 研究专项债券政策")
            suggestions.append("  - 筛选项目优先级")
        
        return suggestions
