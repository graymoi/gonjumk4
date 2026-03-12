"""
文件整理脚本
用于整理项目文件夹，包括：
1. 查找重复文件
2. 查找空目录
3. 查找临时文件
4. 生成整理报告
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class FileOrganizer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.report = {
            "scan_time": datetime.now().isoformat(),
            "base_path": str(base_path),
            "duplicate_files": [],
            "empty_dirs": [],
            "temp_files": [],
            "large_files": [],
            "file_stats": {}
        }
    
    def get_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def find_duplicates(self) -> list:
        """查找重复文件"""
        print("正在查找重复文件...")
        hash_map = defaultdict(list)
        
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    if file_path.stat().st_size > 0:
                        file_hash = self.get_file_hash(file_path)
                        hash_map[file_hash].append(str(file_path))
                except Exception as e:
                    pass
        
        duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}
        self.report["duplicate_files"] = [
            {"hash": k, "files": v, "count": len(v)}
            for k, v in duplicates.items()
        ]
        return duplicates
    
    def find_empty_dirs(self) -> list:
        """查找空目录"""
        print("正在查找空目录...")
        empty_dirs = []
        
        for dir_path in self.base_path.rglob('*'):
            if dir_path.is_dir():
                try:
                    has_files = any(dir_path.rglob('*.*'))
                    if not has_files:
                        empty_dirs.append(str(dir_path))
                except Exception:
                    pass
        
        self.report["empty_dirs"] = empty_dirs
        return empty_dirs
    
    def find_temp_files(self) -> list:
        """查找临时文件"""
        print("正在查找临时文件...")
        temp_extensions = ['.tmp', '.temp', '.bak', '.backup', '.log', '.swp', '.swo']
        temp_patterns = ['~$', '.DS_Store', 'Thumbs.db', '__pycache__']
        temp_files = []
        
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                if file_path.suffix.lower() in temp_extensions:
                    temp_files.append(str(file_path))
                elif any(pattern in file_path.name for pattern in temp_patterns):
                    temp_files.append(str(file_path))
        
        self.report["temp_files"] = temp_files
        return temp_files
    
    def find_large_files(self, size_mb: float = 10) -> list:
        """查找大文件"""
        print(f"正在查找大于{size_mb}MB的文件...")
        large_files = []
        size_bytes = size_mb * 1024 * 1024
        
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    if file_size > size_bytes:
                        large_files.append({
                            "path": str(file_path),
                            "size_mb": round(file_size / 1024 / 1024, 2)
                        })
                except Exception:
                    pass
        
        self.report["large_files"] = large_files
        return large_files
    
    def get_file_stats(self) -> dict:
        """获取文件统计"""
        print("正在统计文件...")
        stats = defaultdict(lambda: {"count": 0, "size": 0})
        
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower() or "无扩展名"
                try:
                    file_size = file_path.stat().st_size
                    stats[ext]["count"] += 1
                    stats[ext]["size"] += file_size
                except Exception:
                    pass
        
        for ext in stats:
            stats[ext]["size_mb"] = round(stats[ext]["size"] / 1024 / 1024, 2)
        
        self.report["file_stats"] = dict(stats)
        return dict(stats)
    
    def generate_report(self) -> dict:
        """生成整理报告"""
        print("\n" + "="*50)
        print("文件整理报告")
        print("="*50)
        
        self.find_duplicates()
        self.find_empty_dirs()
        self.find_temp_files()
        self.find_large_files()
        self.get_file_stats()
        
        print(f"\n重复文件组数: {len(self.report['duplicate_files'])}")
        print(f"空目录数: {len(self.report['empty_dirs'])}")
        print(f"临时文件数: {len(self.report['temp_files'])}")
        print(f"大文件数: {len(self.report['large_files'])}")
        
        print("\n文件类型统计:")
        for ext, data in sorted(self.report['file_stats'].items(), key=lambda x: x[1]['size'], reverse=True)[:10]:
            print(f"  {ext}: {data['count']}个文件, {data['size_mb']}MB")
        
        return self.report
    
    def save_report(self, output_path: str = None):
        """保存报告"""
        import json
        if output_path is None:
            output_path = self.base_path / "logs" / f"organize_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存: {output_path}")
        return str(output_path)


if __name__ == "__main__":
    organizer = FileOrganizer("d:/LMAI/001工具人mk4")
    report = organizer.generate_report()
    organizer.save_report()
