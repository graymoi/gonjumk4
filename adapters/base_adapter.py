"""
数据适配器基类
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json


class BaseAdapter(ABC):
    """数据适配器基类"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.last_sync = None
        self.sync_count = 0
    
    @abstractmethod
    def fetch(self, source: str, **kwargs) -> List[Dict]:
        """获取数据"""
        pass
    
    @abstractmethod
    def validate(self, data: Dict) -> bool:
        """验证数据"""
        pass
    
    @abstractmethod
    def transform(self, data: Dict) -> Dict:
        """转换数据"""
        pass
    
    def process(self, source: str, **kwargs) -> Dict:
        """处理数据"""
        raw_data = self.fetch(source, **kwargs)
        
        valid_data = []
        invalid_data = []
        
        for item in raw_data:
            if self.validate(item):
                valid_data.append(self.transform(item))
            else:
                invalid_data.append(item)
        
        self.last_sync = datetime.now().isoformat()
        self.sync_count += 1
        
        return {
            "total": len(raw_data),
            "valid": len(valid_data),
            "invalid": len(invalid_data),
            "data": valid_data,
            "errors": invalid_data,
            "synced_at": self.last_sync
        }
    
    def save(self, data: List[Dict], path: str) -> bool:
        """保存数据"""
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def load(self, path: str) -> Optional[List[Dict]]:
        """加载数据"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载失败: {e}")
            return None
