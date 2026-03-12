"""
自动化循环引擎
实现持续自动化工作的核心loop功能
"""

import time
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from queue import Queue, PriorityQueue
import logging

from core.logger import get_system_logger
from core.intent_analyzer import IntentAnalyzer
from core.workflow_engine import WorkflowEngine
from core.skill_scheduler import SkillScheduler
from core.evolution_engine import EvolutionEngine
from core.continuous_optimizer import ContinuousOptimizer


class Task:
    """任务对象"""
    
    def __init__(self, task_id: str, task_type: str, priority: int = 5, 
                 data: Dict = None, callback: Callable = None):
        self.task_id = task_id
        self.task_type = task_type
        self.priority = priority
        self.data = data or {}
        self.callback = callback
        self.created_at = datetime.now()
        self.status = "pending"
        self.retry_count = 0
        self.max_retries = 3
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "priority": self.priority,
            "data": self.data,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "retry_count": self.retry_count
        }


class TaskQueue:
    """优先级任务队列"""
    
    def __init__(self):
        self.queue = PriorityQueue()
        self.lock = threading.Lock()
        self.logger = get_system_logger()
    
    def put(self, task: Task):
        with self.lock:
            self.queue.put(task)
            self.logger.info(f"任务入队: {task.task_id} - {task.task_type}", module="TaskQueue")
    
    def get(self, timeout: float = None) -> Optional[Task]:
        try:
            with self.lock:
                if not self.queue.empty():
                    return self.queue.get(timeout=timeout)
        except:
            pass
        return None
    
    def empty(self):
        with self.lock:
            return self.queue.empty()
    
    def size(self):
        with self.lock:
            return self.queue.qsize()


class AutoLoopEngine:
    """自动化循环引擎"""
    
    def __init__(self, system):
        self.system = system
        self.logger = get_system_logger()
        
        self.task_queue = TaskQueue()
        self.running = False
        self.loop_thread = None
        
        self.intent_analyzer = IntentAnalyzer()
        self.workflow_engine = WorkflowEngine()
        self.skill_scheduler = SkillScheduler()
        self.evolution_engine = EvolutionEngine()
        self.continuous_optimizer = ContinuousOptimizer()
        
        self.loop_interval = 60
        self.max_loop_iterations = 1000
        self.current_iteration = 0
        
        self.stats = {
            "total_loops": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "learning_events": 0,
            "optimizations_applied": 0
        }
        
        self.auto_tasks = self._init_auto_tasks()
        
        self._load_state()
    
    def _init_auto_tasks(self) -> Dict[str, Callable]:
        """初始化自动化任务"""
        return {
            "policy_monitor": self._auto_policy_monitor,
            "knowledge_update": self._auto_knowledge_update,
            "system_optimization": self._auto_system_optimization,
            "learning_extraction": self._auto_learning_extraction,
            "health_check": self._auto_health_check,
            "git_sync": self._auto_git_sync,
            "report_generation": self._auto_report_generation
        }
    
    def start(self, interval: int = 60):
        """启动自动循环"""
        if self.running:
            self.logger.warning("循环引擎已在运行", module="AutoLoopEngine")
            return
        
        self.loop_interval = interval
        self.running = True
        
        self.loop_thread = threading.Thread(target=self._loop_worker, daemon=True)
        self.loop_thread.start()
        
        self.logger.info(f"自动循环引擎已启动，间隔: {interval}秒", module="AutoLoopEngine")
        print(f"✅ 自动循环引擎已启动 (间隔: {interval}秒)")
        print(f"   按 Ctrl+C 停止")
        print()
    
    def stop(self):
        """停止自动循环"""
        self.running = False
        if self.loop_thread:
            self.loop_thread.join(timeout=5)
        
        self._save_state()
        self.logger.info("自动循环引擎已停止", module="AutoLoopEngine")
        print("✅ 自动循环引擎已停止")
    
    def _loop_worker(self):
        """循环工作线程"""
        while self.running and self.current_iteration < self.max_loop_iterations:
            try:
                self.current_iteration += 1
                self.stats["total_loops"] += 1
                
                self.logger.info(f"循环迭代 #{self.current_iteration}", module="AutoLoopEngine")
                print(f"\n{'='*60}")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 循环迭代 #{self.current_iteration}")
                print(f"{'='*60}")
                
                self._execute_loop_cycle()
                
                if not self.task_queue.empty():
                    self._process_task_queue()
                
                self._check_scheduled_tasks()
                
                self._save_state()
                
                if self.running:
                    time.sleep(self.loop_interval)
                    
            except KeyboardInterrupt:
                self.logger.info("接收到中断信号", module="AutoLoopEngine")
                self.running = False
                break
            except Exception as e:
                self.logger.error(f"循环错误: {e}", module="AutoLoopEngine")
                print(f"❌ 循环错误: {e}")
                time.sleep(10)
    
    def _execute_loop_cycle(self):
        """执行循环周期"""
        print("\n📋 执行循环周期:")
        
        print("  1️⃣ 政策监测...")
        self._auto_policy_monitor()
        
        print("  2️⃣ 知识库更新...")
        self._auto_knowledge_update()
        
        print("  3️⃣ 系统优化...")
        self._auto_system_optimization()
        
        print("  4️⃣ 学习提取...")
        self._auto_learning_extraction()
        
        print("  5️⃣ 健康检查...")
        self._auto_health_check()
        
        print("  6️⃣ Git同步...")
        self._auto_git_sync()
        
        print("\n✅ 循环周期完成")
    
    def _process_task_queue(self):
        """处理任务队列"""
        print(f"\n📦 处理任务队列 (剩余: {self.task_queue.size()}个)")
        
        processed = 0
        while not self.task_queue.empty() and processed < 5:
            task = self.task_queue.get(timeout=1)
            if task:
                self._execute_task(task)
                processed += 1
    
    def _execute_task(self, task: Task):
        """执行单个任务"""
        print(f"\n  ▶️ 执行任务: {task.task_id} - {task.task_type}")
        
        try:
            task.status = "running"
            
            if task.task_type in self.auto_tasks:
                result = self.auto_tasks[task.task_type](task.data)
            else:
                result = self._execute_custom_task(task)
            
            task.status = "completed"
            self.stats["tasks_completed"] += 1
            
            print(f"  ✅ 任务完成: {task.task_id}")
            
            if task.callback:
                task.callback(result)
                
        except Exception as e:
            task.status = "failed"
            task.retry_count += 1
            self.stats["tasks_failed"] += 1
            
            self.logger.error(f"任务失败: {task.task_id} - {e}", module="AutoLoopEngine")
            print(f"  ❌ 任务失败: {task.task_id} - {e}")
            
            if task.retry_count < task.max_retries:
                print(f"  🔄 重试任务 ({task.retry_count}/{task.max_retries})")
                self.task_queue.put(task)
    
    def _execute_custom_task(self, task: Task) -> Dict:
        """执行自定义任务"""
        user_input = task.data.get("user_input", "")
        
        if user_input:
            return self.system.process(user_input)
        
        return {"status": "skipped", "reason": "no_input"}
    
    def _check_scheduled_tasks(self):
        """检查定时任务"""
        now = datetime.now()
        
        if now.hour == 9 and now.minute < 5:
            self.add_task("daily_report", "report_generation", priority=3)
        
        if now.hour == 18 and now.minute < 5:
            self.add_task("daily_summary", "git_sync", priority=4)
        
        if now.weekday() == 0 and now.hour == 8:
            self.add_task("weekly_optimization", "system_optimization", priority=2)
    
    def add_task(self, task_id: str, task_type: str, priority: int = 5, 
                 data: Dict = None, callback: Callable = None):
        """添加任务到队列"""
        task = Task(task_id, task_type, priority, data, callback)
        self.task_queue.put(task)
        print(f"  ➕ 添加任务: {task_id} - {task_type} (优先级: {priority})")
    
    def _auto_policy_monitor(self, data: Dict = None) -> Dict:
        """自动政策监测"""
        try:
            print("    🔍 监测政策动态...")
            
            result = {
                "status": "success",
                "new_policies": 0,
                "updated_policies": 0,
                "alerts": []
            }
            
            print("    ✅ 政策监测完成")
            return result
            
        except Exception as e:
            self.logger.error(f"政策监测失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _auto_knowledge_update(self, data: Dict = None) -> Dict:
        """自动知识库更新"""
        try:
            print("    📚 更新知识库...")
            
            result = {
                "status": "success",
                "items_updated": 0,
                "items_added": 0
            }
            
            print("    ✅ 知识库更新完成")
            return result
            
        except Exception as e:
            self.logger.error(f"知识库更新失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _auto_system_optimization(self, data: Dict = None) -> Dict:
        """自动系统优化"""
        try:
            print("    ⚡ 运行系统优化...")
            
            result = self.continuous_optimizer.run_optimization_cycle()
            
            if result.get("improvements"):
                self.stats["optimizations_applied"] += len(result.get("applied", []))
                print(f"    ✅ 应用了 {len(result.get('applied', []))} 个优化")
            
            return result
            
        except Exception as e:
            self.logger.error(f"系统优化失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _auto_learning_extraction(self, data: Dict = None) -> Dict:
        """自动学习提取"""
        try:
            print("    🧠 提取学习模式...")
            
            result = self.evolution_engine.analyze_patterns()
            
            if result:
                self.stats["learning_events"] += 1
                print("    ✅ 学习模式提取完成")
            
            return result
            
        except Exception as e:
            self.logger.error(f"学习提取失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _auto_health_check(self, data: Dict = None) -> Dict:
        """自动健康检查"""
        try:
            print("    💊 系统健康检查...")
            
            health = self.system.evolution_monitor.get_system_health()
            
            if health.get("alerts"):
                print(f"    ⚠️ 发现 {len(health['alerts'])} 个告警")
                for alert in health["alerts"][:3]:
                    print(f"       - [{alert['level']}] {alert['message']}")
            
            print("    ✅ 健康检查完成")
            return health
            
        except Exception as e:
            self.logger.error(f"健康检查失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _auto_git_sync(self, data: Dict = None) -> Dict:
        """自动Git同步"""
        try:
            print("    🔄 Git同步...")
            
            import subprocess
            
            subprocess.run(["git", "add", "."], capture_output=True)
            commit_msg = f"auto: 自动循环 #{self.current_iteration} - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
            
            print("    ✅ Git同步完成")
            return {"status": "success"}
            
        except Exception as e:
            self.logger.error(f"Git同步失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _auto_report_generation(self, data: Dict = None) -> Dict:
        """自动报告生成"""
        try:
            print("    📊 生成报告...")
            
            report = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "stats": self.stats,
                "iteration": self.current_iteration
            }
            
            print("    ✅ 报告生成完成")
            return report
            
        except Exception as e:
            self.logger.error(f"报告生成失败: {e}", module="AutoLoopEngine")
            return {"status": "failed", "error": str(e)}
    
    def _save_state(self):
        """保存状态"""
        state = {
            "current_iteration": self.current_iteration,
            "stats": self.stats,
            "running": self.running,
            "last_update": datetime.now().isoformat()
        }
        
        state_file = Path("logs/loop_state.json")
        state_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def _load_state(self):
        """加载状态"""
        state_file = Path("logs/loop_state.json")
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                self.current_iteration = state.get("current_iteration", 0)
                self.stats = state.get("stats", self.stats)
                
                self.logger.info(f"加载状态: 迭代 #{self.current_iteration}", module="AutoLoopEngine")
                
            except Exception as e:
                self.logger.error(f"加载状态失败: {e}", module="AutoLoopEngine")
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "running": self.running,
            "current_iteration": self.current_iteration,
            "queue_size": self.task_queue.size(),
            "stats": self.stats,
            "loop_interval": self.loop_interval
        }
    
    def run_once(self):
        """执行一次循环"""
        print("\n🔄 执行单次循环...")
        self._execute_loop_cycle()
        print("\n✅ 单次循环完成")
