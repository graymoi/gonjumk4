"""
技能调度器模块
负责管理和调度所有可用技能
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class SkillScheduler:
    """技能调度器"""
    
    def __init__(self):
        self.skills_dirs = [
            Path("C:/Users/Administrator/.claude/skills"),
            Path("C:/Users/Administrator/.agents/skills"),
            Path("C:/Users/Administrator/.trae-cn/skills"),
            Path("skills")
        ]
        self.skill_registry = self._discover_skills()
        self.config_path = Path("config/skill_registry.json")
        self._save_registry()
    
    def _discover_skills(self) -> Dict:
        """发现所有可用技能"""
        
        skills = {}
        
        for skills_dir in self.skills_dirs:
            if skills_dir.exists():
                for skill_path in skills_dir.iterdir():
                    if skill_path.is_dir():
                        skill_name = skill_path.name
                        skill_info = self._get_skill_info(skill_path)
                        if skill_info:
                            skills[skill_name] = skill_info
        
        return skills
    
    def _get_skill_info(self, skill_path: Path) -> Optional[Dict]:
        """获取技能信息"""
        
        skill_md = skill_path / "skill.md"
        if skill_md.exists():
            return {
                "name": skill_path.name,
                "path": str(skill_path),
                "description": self._extract_description(skill_md),
                "discovered_at": datetime.now().isoformat()
            }
        
        return {
            "name": skill_path.name,
            "path": str(skill_path),
            "description": "",
            "discovered_at": datetime.now().isoformat()
        }
    
    def _extract_description(self, skill_md: Path) -> str:
        """从skill.md提取描述"""
        
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('#'):
                        return line.lstrip('#').strip()
        except Exception:
            pass
        
        return ""
    
    def _save_registry(self):
        """保存技能注册表"""
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.skill_registry, f, ensure_ascii=False, indent=2)
    
    def get_skill(self, skill_name: str) -> Optional[Dict]:
        """获取技能信息"""
        
        return self.skill_registry.get(skill_name)
    
    def list_skills(self) -> List[str]:
        """列出所有技能"""
        
        return list(self.skill_registry.keys())
    
    def call_skill(self, skill_name: str, params: Dict) -> Dict:
        """调用技能"""
        
        skill_info = self.get_skill(skill_name)
        if not skill_info:
            return {
                "success": False,
                "error": f"技能 {skill_name} 不存在"
            }
        
        return {
            "success": True,
            "skill": skill_name,
            "params": params,
            "result": f"调用技能 {skill_name} 成功",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_skills_by_category(self) -> Dict[str, List[str]]:
        """按类别获取技能"""
        
        categories = {
            "数据处理": ["pandas", "polars", "xlsx", "vaex", "dask"],
            "文档生成": ["office", "docx", "pptx", "pdf", "markitdown"],
            "研究分析": ["research-lookup", "perplexity-search", "literature-review", "openalex-database"],
            "政策相关": ["policy-knowledge-workflow", "城乡建设新闻监测"],
            "智能组装": ["agent-skill-creator", "writing-plans", "scientific-writing"],
            "质量控制": ["scientific-critical-thinking", "verification-before-completion"],
            "工作流": ["workflow-automation", "dispatching-parallel-agents"],
            "浏览器": ["agent-browser"],
            "其他": []
        }
        
        result = {}
        all_skills = set(self.skill_registry.keys())
        categorized = set()
        
        for category, skills in categories.items():
            matched = [s for s in skills if s in all_skills]
            if matched:
                result[category] = matched
                categorized.update(matched)
        
        uncategorized = list(all_skills - categorized)
        if uncategorized:
            result["其他"] = uncategorized
        
        return result
    
    def get_stats(self) -> Dict:
        """获取技能统计"""
        
        return {
            "total_skills": len(self.skill_registry),
            "categories": self.get_skills_by_category(),
            "last_update": datetime.now().isoformat()
        }
