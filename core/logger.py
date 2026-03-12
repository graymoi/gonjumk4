"""
日志系统模块
提供统一的日志记录功能
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class SystemLogger:
    """系统日志器"""
    
    _instance: Optional['SystemLogger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.log_dir = Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        (self.log_dir / "system").mkdir(parents=True, exist_ok=True)
        (self.log_dir / "interactions").mkdir(parents=True, exist_ok=True)
        (self.log_dir / "workflows").mkdir(parents=True, exist_ok=True)
        (self.log_dir / "learning").mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("PolicyKnowledgeSystem")
        self.logger.setLevel(logging.DEBUG)
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        system_log_dir = self.log_dir / "system"
        file_handler = logging.FileHandler(
            system_log_dir / f"system_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """获取日志器"""
        if name:
            return logging.getLogger(f"PolicyKnowledgeSystem.{name}")
        return self.logger
    
    def info(self, message: str, module: str = None):
        """记录信息"""
        logger = self.get_logger(module)
        logger.info(message)
    
    def debug(self, message: str, module: str = None):
        """记录调试信息"""
        logger = self.get_logger(module)
        logger.debug(message)
    
    def warning(self, message: str, module: str = None):
        """记录警告"""
        logger = self.get_logger(module)
        logger.warning(message)
    
    def error(self, message: str, module: str = None):
        """记录错误"""
        logger = self.get_logger(module)
        logger.error(message)
    
    def log_interaction(self, interaction_data: Dict[str, Any]):
        """记录交互日志"""
        log_dir = self.log_dir / "interactions"
        log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(interaction_data, f, ensure_ascii=False, indent=2)
    
    def log_workflow(self, workflow_data: Dict[str, Any]):
        """记录工作流日志"""
        log_dir = self.log_dir / "workflows"
        log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(workflow_data, f, ensure_ascii=False, indent=2)
    
    def log_learning(self, learning_data: Dict[str, Any]):
        """记录学习日志"""
        log_dir = self.log_dir / "learning"
        log_file = log_dir / f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(learning_data, ensure_ascii=False) + '\n')


_logger_instance: Optional[SystemLogger] = None


def get_logger(name: str = None) -> logging.Logger:
    """获取日志器"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SystemLogger()
    return _logger_instance.get_logger(name)


def get_system_logger() -> SystemLogger:
    """获取系统日志器实例"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SystemLogger()
    return _logger_instance
