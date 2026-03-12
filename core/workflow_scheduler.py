"""
智能工作流调度器
实现自动化任务调度和执行
"""

import time
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from collections import defaultdict
import logging

from core.logger import get_system_logger
from core.auto_loop_engine import Task, TaskQueue


class WorkflowScheduler:
    """智能工作流调度器"""
    
    def __init__(self, auto_loop_engine):
        self.auto_loop = auto_loop_engine
        self.logger = get_system_logger()
        
        self.scheduled_tasks: Dict[str, Dict] = {}
        self.task_dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()
        
        self.resource_pool = {
            "cpu": 100,
            "memory": 100,
            "network": 100,
            "api_calls": 1000
        }
        
        self.task_history: List[Dict] = []
        self.max_history = 1000
        
        self.scheduler_thread = None
        self.running = False
        
        self._load_scheduler_state()
    
    def start(self):
        """启动调度器"""
        if self.running:
            self.logger.warning("调度器已在运行", module="WorkflowScheduler")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_worker, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("智能工作流调度器已启动", module="WorkflowScheduler")
        print("✅ 智能工作流调度器已启动")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        self._save_scheduler_state()
        self.logger.info("智能工作流调度器已停止", module="WorkflowScheduler")
        print("✅ 智能工作流调度器已停止")
    
    def _scheduler_worker(self):
        """调度器工作线程"""
        while self.running:
            try:
                self._check_scheduled_tasks()
                self._check_dependencies()
                self._optimize_resources()
                
                time.sleep(30)
                
            except Exception as e:
                self.logger.error(f"调度器错误: {e}", module="WorkflowScheduler")
                time.sleep(10)
    
    def schedule_task(self, task_id: str, task_type: str, schedule_time: datetime,
                      priority: int = 5, data: Dict = None, dependencies: List[str] = None,
                      recurring: bool = False, interval: int = None):
        """调度任务"""
        
        task_info = {
            "task_id": task_id,
            "task_type": task_type,
            "schedule_time": schedule_time.isoformat(),
            "priority": priority,
            "data": data or {},
            "dependencies": dependencies or [],
            "recurring": recurring,
            "interval": interval,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        self.scheduled_tasks[task_id] = task_info
        
        if dependencies:
            self.task_dependencies[task_id] = set(dependencies)
        
        self.logger.info(f"调度任务: {task_id} - {schedule_time}", module="WorkflowScheduler")
        print(f"  📅 调度任务: {task_id} ({schedule_time.strftime('%Y-%m-%d %H:%M')})")
    
    def _check_scheduled_tasks(self):
        """检查调度任务"""
        now = datetime.now()
        
        for task_id, task_info in list(self.scheduled_tasks.items()):
            schedule_time = datetime.fromisoformat(task_info["schedule_time"])
            
            if now >= schedule_time:
                if self._can_execute_task(task_id):
                    self._execute_scheduled_task(task_id)
    
    def _can_execute_task(self, task_id: str) -> bool:
        """检查任务是否可以执行"""
        
        if task_id in self.completed_tasks or task_id in self.failed_tasks:
            return False
        
        dependencies = self.task_dependencies.get(task_id, set())
        for dep_id in dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        return True
    
    def _execute_scheduled_task(self, task_id: str):
        """执行调度任务"""
        task_info = self.scheduled_tasks[task_id]
        
        print(f"\n  ⏰ 执行调度任务: {task_id}")
        
        self.auto_loop.add_task(
            task_id=task_id,
            task_type=task_info["task_type"],
            priority=task_info["priority"],
            data=task_info["data"]
        )
        
        task_info["status"] = "executed"
        task_info["executed_at"] = datetime.now().isoformat()
        
        if task_info["recurring"] and task_info["interval"]:
            next_time = datetime.now() + timedelta(seconds=task_info["interval"])
            self.schedule_task(
                task_id=f"{task_id}_{next_time.strftime('%Y%m%d%H%M%S')}",
                task_type=task_info["task_type"],
                schedule_time=next_time,
                priority=task_info["priority"],
                data=task_info["data"],
                recurring=True,
                interval=task_info["interval"]
            )
        
        self._record_task_history(task_info)
    
    def _check_dependencies(self):
        """检查依赖关系"""
        for task_id, dependencies in list(self.task_dependencies.items()):
            if task_id in self.completed_tasks:
                continue
            
            all_deps_completed = all(
                dep_id in self.completed_tasks 
                for dep_id in dependencies
            )
            
            if all_deps_completed and task_id in self.scheduled_tasks:
                task_info = self.scheduled_tasks[task_id]
                if task_info["status"] == "waiting_for_deps":
                    task_info["status"] = "ready"
                    print(f"  ✅ 任务 {task_id} 依赖已满足，准备执行")
    
    def _optimize_resources(self):
        """优化资源分配"""
        pass
    
    def _record_task_history(self, task_info: Dict):
        """记录任务历史"""
        self.task_history.append({
            "task_id": task_info["task_id"],
            "task_type": task_info["task_type"],
            "executed_at": task_info.get("executed_at"),
            "status": task_info["status"]
        })
        
        if len(self.task_history) > self.max_history:
            self.task_history = self.task_history[-self.max_history:]
    
    def mark_task_completed(self, task_id: str):
        """标记任务完成"""
        self.completed_tasks.add(task_id)
        
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id]["status"] = "completed"
            self.scheduled_tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        self.logger.info(f"任务完成: {task_id}", module="WorkflowScheduler")
    
    def mark_task_failed(self, task_id: str):
        """标记任务失败"""
        self.failed_tasks.add(task_id)
        
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id]["status"] = "failed"
            self.scheduled_tasks[task_id]["failed_at"] = datetime.now().isoformat()
        
        self.logger.error(f"任务失败: {task_id}", module="WorkflowScheduler")
    
    def get_pending_tasks(self) -> List[Dict]:
        """获取待执行任务"""
        pending = []
        for task_id, task_info in self.scheduled_tasks.items():
            if task_info["status"] == "scheduled":
                pending.append(task_info)
        return pending
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        if task_id in self.scheduled_tasks:
            return self.scheduled_tasks[task_id]
        return None
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id]["status"] = "cancelled"
            self.logger.info(f"取消任务: {task_id}", module="WorkflowScheduler")
            print(f"  ❌ 取消任务: {task_id}")
            return True
        return False
    
    def _save_scheduler_state(self):
        """保存调度器状态"""
        state = {
            "scheduled_tasks": self.scheduled_tasks,
            "completed_tasks": list(self.completed_tasks),
            "failed_tasks": list(self.failed_tasks),
            "task_history": self.task_history[-100:],
            "last_update": datetime.now().isoformat()
        }
        
        state_file = Path("logs/scheduler_state.json")
        state_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def _load_scheduler_state(self):
        """加载调度器状态"""
        state_file = Path("logs/scheduler_state.json")
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                self.scheduled_tasks = state.get("scheduled_tasks", {})
                self.completed_tasks = set(state.get("completed_tasks", []))
                self.failed_tasks = set(state.get("failed_tasks", []))
                self.task_history = state.get("task_history", [])
                
                self.logger.info("加载调度器状态成功", module="WorkflowScheduler")
                
            except Exception as e:
                self.logger.error(f"加载调度器状态失败: {e}", module="WorkflowScheduler")
    
    def get_scheduler_stats(self) -> Dict:
        """获取调度器统计"""
        return {
            "total_scheduled": len(self.scheduled_tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "pending": len([t for t in self.scheduled_tasks.values() if t["status"] == "scheduled"]),
            "history_size": len(self.task_history)
        }


class WorkflowOrchestrator:
    """工作流编排器"""
    
    def __init__(self, auto_loop_engine, scheduler):
        self.auto_loop = auto_loop_engine
        self.scheduler = scheduler
        self.logger = get_system_logger()
        
        self.workflows: Dict[str, Dict] = {}
        self.workflow_instances: Dict[str, Dict] = {}
    
    def create_workflow(self, workflow_id: str, name: str, steps: List[Dict]) -> str:
        """创建工作流"""
        workflow = {
            "workflow_id": workflow_id,
            "name": name,
            "steps": steps,
            "created_at": datetime.now().isoformat()
        }
        
        self.workflows[workflow_id] = workflow
        
        self.logger.info(f"创建工作流: {workflow_id} - {name}", module="WorkflowOrchestrator")
        print(f"  📋 创建工作流: {name} ({len(steps)}个步骤)")
        
        return workflow_id
    
    def execute_workflow(self, workflow_id: str, input_data: Dict = None) -> str:
        """执行工作流"""
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        workflow = self.workflows[workflow_id]
        instance_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        instance = {
            "instance_id": instance_id,
            "workflow_id": workflow_id,
            "status": "running",
            "current_step": 0,
            "input_data": input_data or {},
            "output_data": {},
            "started_at": datetime.now().isoformat(),
            "steps_status": []
        }
        
        self.workflow_instances[instance_id] = instance
        
        print(f"\n  🚀 执行工作流: {workflow['name']}")
        
        for i, step in enumerate(workflow["steps"]):
            instance["current_step"] = i
            step_result = self._execute_workflow_step(instance, step)
            instance["steps_status"].append(step_result)
            
            if step_result["status"] == "failed":
                instance["status"] = "failed"
                break
        
        if instance["status"] == "running":
            instance["status"] = "completed"
        
        instance["completed_at"] = datetime.now().isoformat()
        
        print(f"  ✅ 工作流完成: {instance['status']}")
        
        return instance_id
    
    def _execute_workflow_step(self, instance: Dict, step: Dict) -> Dict:
        """执行工作流步骤"""
        step_name = step.get("name", "未命名步骤")
        step_type = step.get("type", "task")
        
        print(f"    ▶️ 步骤: {step_name}")
        
        try:
            if step_type == "task":
                task_id = f"{instance['instance_id']}_step_{instance['current_step']}"
                self.auto_loop.add_task(
                    task_id=task_id,
                    task_type=step.get("task_type", "custom"),
                    priority=step.get("priority", 5),
                    data=step.get("data", {})
                )
                
                return {
                    "step_name": step_name,
                    "status": "completed",
                    "task_id": task_id
                }
            
            elif step_type == "parallel":
                tasks = step.get("tasks", [])
                for task in tasks:
                    self.auto_loop.add_task(
                        task_id=f"{instance['instance_id']}_parallel_{len(self.auto_loop.task_queue.queue)}",
                        task_type=task.get("task_type"),
                        priority=task.get("priority", 5),
                        data=task.get("data", {})
                    )
                
                return {
                    "step_name": step_name,
                    "status": "completed",
                    "parallel_tasks": len(tasks)
                }
            
            elif step_type == "condition":
                condition = step.get("condition")
                if self._evaluate_condition(condition, instance):
                    return self._execute_workflow_step(instance, step.get("then_step", {}))
                else:
                    return self._execute_workflow_step(instance, step.get("else_step", {}))
            
            else:
                return {
                    "step_name": step_name,
                    "status": "skipped",
                    "reason": "unknown_step_type"
                }
                
        except Exception as e:
            self.logger.error(f"步骤执行失败: {step_name} - {e}", module="WorkflowOrchestrator")
            return {
                "step_name": step_name,
                "status": "failed",
                "error": str(e)
            }
    
    def _evaluate_condition(self, condition: Dict, instance: Dict) -> bool:
        """评估条件"""
        if not condition:
            return False
        
        condition_type = condition.get("type")
        
        if condition_type == "data_exists":
            key = condition.get("key")
            return key in instance.get("output_data", {})
        
        elif condition_type == "value_equals":
            key = condition.get("key")
            value = condition.get("value")
            return instance.get("output_data", {}).get(key) == value
        
        return False
    
    def get_workflow_status(self, instance_id: str) -> Optional[Dict]:
        """获取工作流状态"""
        return self.workflow_instances.get(instance_id)
    
    def list_workflows(self) -> List[Dict]:
        """列出所有工作流"""
        return [
            {
                "workflow_id": wf_id,
                "name": wf["name"],
                "steps": len(wf["steps"]),
                "created_at": wf["created_at"]
            }
            for wf_id, wf in self.workflows.items()
        ]
