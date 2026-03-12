"""
政策数据适配器
处理政策文件的读取、解析和转换
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .base_adapter import BaseAdapter


class PolicyAdapter(BaseAdapter):
    """政策数据适配器"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.policy_base = Path(config.get("policy_base", "00_政策法规")) if config else Path("00_政策法规")
    
    def fetch(self, source: str, **kwargs) -> List[Dict]:
        """获取政策数据"""
        source_path = self.policy_base / source
        
        if not source_path.exists():
            return []
        
        policies = []
        
        if source_path.is_file():
            policy = self._parse_policy_file(source_path)
            if policy:
                policies.append(policy)
        elif source_path.is_dir():
            for policy_file in source_path.rglob("*.md"):
                policy = self._parse_policy_file(policy_file)
                if policy:
                    policies.append(policy)
        
        return policies
    
    def _parse_policy_file(self, file_path: Path) -> Optional[Dict]:
        """解析政策文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = self._extract_metadata(content)
            content_body = self._extract_content(content)
            
            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "metadata": metadata,
                "content": content_body,
                "raw_content": content,
                "parsed_at": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"解析政策文件失败 {file_path}: {e}")
            return None
    
    def _extract_metadata(self, content: str) -> Dict:
        """提取元数据"""
        metadata = {}
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if value.startswith('['):
                            value = [v.strip() for v in value.strip('[]').split(',')]
                        metadata[key] = value
        
        if 'file_number' not in metadata:
            patterns = {
                'file_number': r'([国发|国办发|发改|财|建|自然资][\〔\(][\d]{4}[\〕\)][\d]+号)',
                'publishing_date': r'(\d{4}年\d{1,2}月\d{1,2}日|\d{8})',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    metadata[key] = match.group(1)
        
        return metadata
    
    def _extract_content(self, content: str) -> str:
        """提取正文内容"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2].strip()
        
        return content
    
    def validate(self, data: Dict) -> bool:
        """验证政策数据"""
        required_fields = ['file_path', 'content']
        return all(field in data for field in required_fields)
    
    def transform(self, data: Dict) -> Dict:
        """转换政策数据"""
        return {
            "id": self._generate_id(data),
            "title": data.get("metadata", {}).get("policy_name", data.get("file_name", "")),
            "file_number": data.get("metadata", {}).get("file_number", ""),
            "publishing_agency": data.get("metadata", {}).get("publishing_agency", ""),
            "publishing_date": data.get("metadata", {}).get("publishing_date", ""),
            "status": data.get("metadata", {}).get("status", "现行有效"),
            "keywords": data.get("metadata", {}).get("keywords", []),
            "content": data.get("content", ""),
            "file_path": data.get("file_path", ""),
            "source": "policy_library",
            "transformed_at": datetime.now().isoformat()
        }
    
    def _generate_id(self, data: Dict) -> str:
        """生成政策ID"""
        file_number = data.get("metadata", {}).get("file_number", "")
        if file_number:
            return file_number.replace("/", "_").replace("\\", "_")
        
        file_name = data.get("file_name", "unknown")
        return Path(file_name).stem
    
    def search(self, query: str, filters: Dict = None) -> List[Dict]:
        """搜索政策"""
        results = []
        
        all_policies = self.fetch("国家级/01_按部门")
        
        query_lower = query.lower()
        
        for policy in all_policies:
            content = policy.get("content", "").lower()
            title = policy.get("metadata", {}).get("policy_name", "").lower()
            file_number = policy.get("metadata", {}).get("file_number", "").lower()
            
            if query_lower in content or query_lower in title or query_lower in file_number:
                if self._match_filters(policy, filters):
                    results.append(policy)
        
        return results
    
    def _match_filters(self, policy: Dict, filters: Dict) -> bool:
        """匹配过滤条件"""
        if not filters:
            return True
        
        metadata = policy.get("metadata", {})
        
        for key, value in filters.items():
            if key in metadata:
                if isinstance(value, list):
                    if metadata[key] not in value:
                        return False
                elif metadata[key] != value:
                    return False
        
        return True
    
    def get_by_department(self, department: str) -> List[Dict]:
        """按部门获取政策"""
        return self.fetch(f"国家级/01_按部门/{department}")
    
    def get_by_domain(self, domain: str) -> List[Dict]:
        """按业务领域获取政策"""
        return self.fetch(f"国家级/03_按业务领域/{domain}")
    
    def get_all_departments(self) -> List[str]:
        """获取所有部门"""
        dept_path = self.policy_base / "国家级/01_按部门"
        if not dept_path.exists():
            return []
        return [d.name for d in dept_path.iterdir() if d.is_dir()]
    
    def get_all_domains(self) -> List[str]:
        """获取所有业务领域"""
        domain_path = self.policy_base / "国家级/03_按业务领域"
        if not domain_path.exists():
            return []
        return [d.stem.replace("索引", "") for d in domain_path.glob("*.md")]
