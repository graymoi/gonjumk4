"""
输出管理模块
管理所有输出文件的生成、组织和归档
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class OutputRecord:
    """输出记录"""
    id: str
    scenario: str
    created_at: str
    files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"


class OutputManager:
    """输出管理器"""
    
    def __init__(self, base_path: str = "outputs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.base_path / "output_index.json"
        self._load_index()
    
    def _load_index(self):
        """加载输出索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {"outputs": [], "total": 0}
    
    def _save_index(self):
        """保存输出索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def create_output_dir(self, scenario: str, project: str = None) -> Path:
        """创建输出目录"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        scenario_clean = scenario.replace("/", "_").replace("\\", "_")[:30]
        
        if project:
            project_clean = project.replace("/", "_").replace("\\", "_")[:20]
            dir_name = f"{timestamp}_{scenario_clean}_{project_clean}"
        else:
            dir_name = f"{timestamp}_{scenario_clean}"
        
        output_dir = self.base_path / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        record = OutputRecord(
            id=dir_name,
            scenario=scenario,
            created_at=datetime.now().isoformat(),
            status="created"
        )
        
        self.index["outputs"].append(asdict(record))
        self.index["total"] += 1
        self._save_index()
        
        return output_dir
    
    def save_file(self, output_dir: Path, filename: str, content: Any, 
                  file_type: str = "json") -> Path:
        """保存文件"""
        file_path = output_dir / filename
        
        if file_type == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        elif file_type == "text" or file_type == "md":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        elif file_type == "binary":
            with open(file_path, 'wb') as f:
                f.write(content)
        
        return file_path
    
    def save_report(self, output_dir: Path, report_name: str, 
                    content: str, metadata: Dict = None) -> Path:
        """保存报告"""
        file_path = output_dir / f"{report_name}.md"
        
        full_content = content
        if metadata:
            frontmatter = "---\n"
            for key, value in metadata.items():
                frontmatter += f"{key}: {value}\n"
            frontmatter += "---\n\n"
            full_content = frontmatter + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return file_path
    
    def get_output(self, output_id: str) -> Optional[Dict]:
        """获取输出记录"""
        for output in self.index["outputs"]:
            if output["id"] == output_id:
                return output
        return None
    
    def list_outputs(self, scenario: str = None, limit: int = 20) -> List[Dict]:
        """列出输出"""
        outputs = self.index["outputs"]
        
        if scenario:
            outputs = [o for o in outputs if scenario in o["scenario"]]
        
        return outputs[-limit:]
    
    def archive_output(self, output_id: str) -> bool:
        """归档输出"""
        output = self.get_output(output_id)
        if not output:
            return False
        
        output_dir = self.base_path / output_id
        archive_dir = self.base_path / "archived" / output_id
        
        if output_dir.exists():
            archive_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(output_dir), str(archive_dir))
            output["status"] = "archived"
            self._save_index()
            return True
        
        return False
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_outputs": self.index["total"],
            "recent_outputs": len([o for o in self.index["outputs"] 
                                  if self._is_recent(o["created_at"])]),
            "by_status": self._count_by_status()
        }
    
    def _is_recent(self, timestamp: str, days: int = 7) -> bool:
        """判断是否最近"""
        try:
            created = datetime.fromisoformat(timestamp)
            return (datetime.now() - created).days <= days
        except Exception:
            return False
    
    def _count_by_status(self) -> Dict[str, int]:
        """按状态统计"""
        counts = {}
        for output in self.index["outputs"]:
            status = output.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def cleanup_old_outputs(self, days: int = 30) -> int:
        """清理旧输出"""
        cleaned = 0
        for output in self.index["outputs"][:]:
            try:
                created = datetime.fromisoformat(output["created_at"])
                if (datetime.now() - created).days > days:
                    output_dir = self.base_path / output["id"]
                    if output_dir.exists():
                        shutil.rmtree(output_dir)
                    self.index["outputs"].remove(output)
                    cleaned += 1
            except Exception:
                pass
        
        if cleaned > 0:
            self.index["total"] -= cleaned
            self._save_index()
        
        return cleaned
