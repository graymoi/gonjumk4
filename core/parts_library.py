"""
零件库管理模块

管理生产成果过程中积累的可复用知识单元
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PartsLibrary:
    """零件库管理器"""
    
    def __init__(self, base_path: str = "knowledge/parts"):
        self.base_path = Path(base_path)
        self.index_path = Path("knowledge/index")
        self.metadata_path = Path("knowledge/metadata")
        
        self.parts_types = {
            "policies": "政策零件",
            "templates": "模板零件",
            "cases": "案例零件",
            "data": "数据零件",
            "processes": "流程零件",
            "scripts": "话术零件",
            "risks": "风险零件"
        }
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保目录存在"""
        for part_type in self.parts_types:
            (self.base_path / part_type).mkdir(parents=True, exist_ok=True)
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
    
    def add_part(self, part: Dict) -> Dict:
        """添加零件到零件库"""
        
        part_type = part.get("type")
        if part_type not in self.parts_types:
            return {
                "success": False,
                "error": f"未知零件类型: {part_type}"
            }
        
        part_id = self._generate_part_id(part)
        part["id"] = part_id
        part["created_at"] = datetime.now().isoformat()
        part["updated_at"] = datetime.now().isoformat()
        
        part_path = self.base_path / part_type / f"{part_id}.json"
        
        with open(part_path, 'w', encoding='utf-8') as f:
            json.dump(part, f, ensure_ascii=False, indent=2)
        
        self._update_index(part)
        self._update_metadata("add", part)
        
        return {
            "success": True,
            "part_id": part_id,
            "path": str(part_path)
        }
    
    def get_part(self, part_id: str, part_type: Optional[str] = None) -> Optional[Dict]:
        """获取零件"""
        
        if part_type:
            part_path = self.base_path / part_type / f"{part_id}.json"
            if part_path.exists():
                with open(part_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        else:
            for pt in self.parts_types:
                part_path = self.base_path / pt / f"{part_id}.json"
                if part_path.exists():
                    with open(part_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
        
        return None
    
    def search_parts(self, query: str, part_type: Optional[str] = None) -> List[Dict]:
        """搜索零件"""
        
        results = []
        
        search_types = [part_type] if part_type else list(self.parts_types.keys())
        
        for pt in search_types:
            part_dir = self.base_path / pt
            if not part_dir.exists():
                continue
            
            for part_file in part_dir.glob("*.json"):
                with open(part_file, 'r', encoding='utf-8') as f:
                    part = json.load(f)
                
                if self._match_query(part, query):
                    results.append(part)
        
        return results
    
    def _match_query(self, part: Dict, query: str) -> bool:
        """匹配查询"""
        
        query = query.lower()
        
        searchable_fields = ["name", "description", "content", "keywords", "tags"]
        
        for field in searchable_fields:
            value = part.get(field, "")
            if isinstance(value, str) and query in value.lower():
                return True
            if isinstance(value, list) and any(query in str(v).lower() for v in value):
                return True
        
        return False
    
    def update_part(self, part_id: str, updates: Dict) -> Dict:
        """更新零件"""
        
        part = self.get_part(part_id)
        if not part:
            return {
                "success": False,
                "error": f"零件不存在: {part_id}"
            }
        
        part.update(updates)
        part["updated_at"] = datetime.now().isoformat()
        
        part_path = self.base_path / part["type"] / f"{part_id}.json"
        with open(part_path, 'w', encoding='utf-8') as f:
            json.dump(part, f, ensure_ascii=False, indent=2)
        
        return {
            "success": True,
            "part_id": part_id
        }
    
    def delete_part(self, part_id: str) -> Dict:
        """删除零件"""
        
        part = self.get_part(part_id)
        if not part:
            return {
                "success": False,
                "error": f"零件不存在: {part_id}"
            }
        
        part_path = self.base_path / part["type"] / f"{part_id}.json"
        part_path.unlink()
        
        self._update_metadata("delete", part)
        
        return {
            "success": True,
            "part_id": part_id
        }
    
    def get_stats(self) -> Dict:
        """获取零件库统计"""
        
        stats = {
            "total": 0,
            "by_type": {},
            "recent_added": []
        }
        
        for part_type in self.parts_types:
            part_dir = self.base_path / part_type
            count = len(list(part_dir.glob("*.json")))
            stats["by_type"][part_type] = count
            stats["total"] += count
        
        return stats
    
    def _generate_part_id(self, part: Dict) -> str:
        """生成零件ID"""
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        part_type = part.get("type", "unknown")
        name = part.get("name", "unnamed")[:20]
        
        return f"{part_type}_{name}_{timestamp}"
    
    def _update_index(self, part: Dict):
        """更新索引"""
        
        index_file = self.index_path / "full_index.json"
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {
                "version": "1.0.0",
                "updated_at": datetime.now().isoformat(),
                "parts_count": {},
                "parts": []
            }
        
        index["parts"].append({
            "id": part["id"],
            "type": part["type"],
            "name": part.get("name", ""),
            "created_at": part["created_at"]
        })
        
        index["updated_at"] = datetime.now().isoformat()
        
        for pt in self.parts_types:
            index["parts_count"][pt] = len([p for p in index["parts"] if p["type"] == pt])
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def _update_metadata(self, action: str, part: Dict):
        """更新元数据"""
        
        sources_file = self.metadata_path / "sources.json"
        
        if sources_file.exists():
            with open(sources_file, 'r', encoding='utf-8') as f:
                sources = json.load(f)
        else:
            sources = {
                "version": "1.0.0",
                "updated_at": datetime.now().isoformat(),
                "sources": {},
                "source_records": []
            }
        
        if action == "add":
            source = part.get("source", "unknown")
            if source == "auto_collected":
                sources["sources"]["auto_collected"] = sources["sources"].get("auto_collected", 0) + 1
            else:
                sources["sources"]["user_provided"] = sources["sources"].get("user_provided", 0) + 1
            
            sources["source_records"].append({
                "part_id": part["id"],
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
        
        sources["updated_at"] = datetime.now().isoformat()
        
        with open(sources_file, 'w', encoding='utf-8') as f:
            json.dump(sources, f, ensure_ascii=False, indent=2)


def extract_parts_from_workflow(workflow_result: Dict) -> List[Dict]:
    """从工作流结果中提取零件"""
    
    parts = []
    
    for policy in workflow_result.get("matched_policies", []):
        part = {
            "type": "policies",
            "name": policy.get("name", "未命名政策"),
            "content": policy.get("key_points", ""),
            "source": "auto_extracted",
            "related_scenario": workflow_result.get("scenario", ""),
            "keywords": policy.get("keywords", [])
        }
        parts.append(part)
    
    if workflow_result.get("report_template"):
        part = {
            "type": "templates",
            "name": f"{workflow_result.get('scenario', '未命名')}模板",
            "content": workflow_result["report_template"],
            "source": "auto_generated"
        }
        parts.append(part)
    
    if workflow_result.get("workflow_steps"):
        part = {
            "type": "processes",
            "name": f"{workflow_result.get('scenario', '未命名')}流程",
            "content": workflow_result["workflow_steps"],
            "source": "auto_extracted"
        }
        parts.append(part)
    
    if workflow_result.get("risk_analysis"):
        part = {
            "type": "risks",
            "name": f"{workflow_result.get('scenario', '未命名')}风险",
            "content": workflow_result["risk_analysis"],
            "source": "auto_extracted"
        }
        parts.append(part)
    
    return parts


def auto_collect_parts(library: PartsLibrary, workflow_result: Dict) -> Dict:
    """自动收集零件"""
    
    parts = extract_parts_from_workflow(workflow_result)
    
    results = {
        "total": len(parts),
        "added": 0,
        "failed": 0,
        "details": []
    }
    
    for part in parts:
        result = library.add_part(part)
        if result["success"]:
            results["added"] += 1
        else:
            results["failed"] += 1
        
        results["details"].append({
            "name": part.get("name"),
            "type": part.get("type"),
            "success": result["success"]
        })
    
    return results
