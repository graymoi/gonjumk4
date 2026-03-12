"""
Agent协作编排器
借鉴DeerFlow的Sub-Agent设计，实现多智能体协作
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
import json

from core.logger import get_system_logger


class AgentType(Enum):
    POLICY_COLLECTOR = "policy_collector"
    PROJECT_PLANNER = "project_planner"
    PROJECT_FILTER = "project_filter"
    POLICY_RESEARCHER = "policy_researcher"
    QUICK_ASSEMBLER = "quick_assembler"
    DATA_MANAGER = "data_manager"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentTask:
    task_id: str
    agent_type: AgentType
    input_data: Dict
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "agent_type": self.agent_type.value,
            "input_data": self.input_data,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class ExecutionPlan:
    plan_id: str
    tasks: List[AgentTask]
    execution_order: List[List[str]]
    status: TaskStatus = TaskStatus.PENDING
    results: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class BaseAgent:
    """Agent基类"""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.logger = get_system_logger()
    
    def execute(self, input_data: Dict) -> Dict:
        raise NotImplementedError("子类必须实现execute方法")
    
    def validate_input(self, input_data: Dict) -> bool:
        return True


class PolicyCollectorAgent(BaseAgent):
    """政策采集Agent"""
    
    def __init__(self):
        super().__init__(AgentType.POLICY_COLLECTOR)
        self.triggers = ["采集", "入库", "归档", "新闻", "监测"]
    
    def execute(self, input_data: Dict) -> Dict:
        self.logger.info(f"政策采集Agent执行: {input_data}")
        
        return {
            "success": True,
            "action": "policy_collection",
            "collected_count": 0,
            "message": "政策采集完成"
        }


class ProjectPlannerAgent(BaseAgent):
    """项目谋划Agent"""
    
    def __init__(self):
        super().__init__(AgentType.PROJECT_PLANNER)
        self.triggers = ["谋划", "包装", "组合", "打捆", "申报"]
    
    def execute(self, input_data: Dict) -> Dict:
        self.logger.info(f"项目谋划Agent执行: {input_data}")
        
        return {
            "success": True,
            "action": "project_planning",
            "project_name": input_data.get("project_name"),
            "funding_plan": {},
            "message": "项目谋划完成"
        }


class ProjectFilterAgent(BaseAgent):
    """项目筛选Agent"""
    
    def __init__(self):
        super().__init__(AgentType.PROJECT_FILTER)
        self.triggers = ["筛选", "排序", "规划", "战略"]
    
    def execute(self, input_data: Dict) -> Dict:
        self.logger.info(f"项目筛选Agent执行: {input_data}")
        
        return {
            "success": True,
            "action": "project_filtering",
            "filtered_projects": [],
            "message": "项目筛选完成"
        }


class PolicyResearcherAgent(BaseAgent):
    """政策研究Agent"""
    
    def __init__(self):
        super().__init__(AgentType.POLICY_RESEARCHER)
        self.triggers = ["研究", "趋势", "影响", "流程", "指导"]
    
    def execute(self, input_data: Dict) -> Dict:
        self.logger.info(f"政策研究Agent执行: {input_data}")
        
        return {
            "success": True,
            "action": "policy_research",
            "research_result": {},
            "message": "政策研究完成"
        }


class QuickAssemblerAgent(BaseAgent):
    """快速组装Agent"""
    
    def __init__(self):
        super().__init__(AgentType.QUICK_ASSEMBLER)
        self.triggers = ["组装", "宣讲", "PPT", "方案"]
    
    def execute(self, input_data: Dict) -> Dict:
        self.logger.info(f"快速组装Agent执行: {input_data}")
        
        return {
            "success": True,
            "action": "quick_assembly",
            "output_files": [],
            "message": "快速组装完成"
        }


class DataManagerAgent(BaseAgent):
    """数据管理Agent"""
    
    def __init__(self):
        super().__init__(AgentType.DATA_MANAGER)
        self.triggers = ["管理", "更新", "验证", "组织"]
    
    def execute(self, input_data: Dict) -> Dict:
        self.logger.info(f"数据管理Agent执行: {input_data}")
        
        return {
            "success": True,
            "action": "data_management",
            "updated_count": 0,
            "message": "数据管理完成"
        }


class AgentOrchestrator:
    """Agent协作编排器"""
    
    def __init__(self, max_workers: int = 4):
        self.logger = get_system_logger()
        self.max_workers = max_workers
        
        self.agents = self._init_agents()
        self.task_registry: Dict[str, AgentTask] = {}
        self.plan_registry: Dict[str, ExecutionPlan] = {}
    
    def _init_agents(self) -> Dict[AgentType, BaseAgent]:
        """初始化所有Agent"""
        return {
            AgentType.POLICY_COLLECTOR: PolicyCollectorAgent(),
            AgentType.PROJECT_PLANNER: ProjectPlannerAgent(),
            AgentType.PROJECT_FILTER: ProjectFilterAgent(),
            AgentType.POLICY_RESEARCHER: PolicyResearcherAgent(),
            AgentType.QUICK_ASSEMBLER: QuickAssemblerAgent(),
            AgentType.DATA_MANAGER: DataManagerAgent(),
        }
    
    def create_task(
        self,
        agent_type: AgentType,
        input_data: Dict,
        priority: int = 0,
        dependencies: List[str] = None
    ) -> AgentTask:
        """创建任务"""
        task = AgentTask(
            task_id=str(uuid.uuid4())[:8],
            agent_type=agent_type,
            input_data=input_data,
            priority=priority,
            dependencies=dependencies or []
        )
        self.task_registry[task.task_id] = task
        return task
    
    def create_plan(self, tasks: List[AgentTask]) -> ExecutionPlan:
        """创建执行计划"""
        execution_order = self._build_execution_order(tasks)
        
        plan = ExecutionPlan(
            plan_id=str(uuid.uuid4())[:8],
            tasks=tasks,
            execution_order=execution_order
        )
        self.plan_registry[plan.plan_id] = plan
        return plan
    
    def _build_execution_order(self, tasks: List[AgentTask]) -> List[List[str]]:
        """构建执行顺序（拓扑排序）"""
        task_map = {t.task_id: t for t in tasks}
        in_degree = {t.task_id: 0 for t in tasks}
        graph = {t.task_id: [] for t in tasks}
        
        for task in tasks:
            for dep in task.dependencies:
                if dep in task_map:
                    graph[dep].append(task.task_id)
                    in_degree[task.task_id] += 1
        
        order = []
        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        
        while queue:
            level = queue[:]
            order.append(level)
            queue = []
            
            for tid in level:
                for next_tid in graph[tid]:
                    in_degree[next_tid] -= 1
                    if in_degree[next_tid] == 0:
                        queue.append(next_tid)
        
        return order
    
    def execute_task(self, task: AgentTask) -> Dict:
        """执行单个任务"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        
        try:
            agent = self.agents[task.agent_type]
            result = agent.execute(task.input_data)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            return result
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            
            self.logger.error(f"任务执行失败: {task.task_id}, 错误: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_parallel(self, tasks: List[AgentTask]) -> Dict[str, Dict]:
        """并行执行多个独立任务"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {
                executor.submit(self.execute_task, task): task
                for task in tasks
            }
            
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    results[task.task_id] = future.result()
                except Exception as e:
                    results[task.task_id] = {"success": False, "error": str(e)}
        
        return results
    
    def execute_plan(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """执行完整计划"""
        plan.status = TaskStatus.RUNNING
        
        for level in plan.execution_order:
            level_tasks = [t for t in plan.tasks if t.task_id in level]
            
            for task in level_tasks:
                for dep_id in task.dependencies:
                    if dep_id in plan.results:
                        task.input_data.update(plan.results[dep_id])
            
            level_results = self.execute_parallel(level_tasks)
            plan.results.update(level_results)
        
        plan.status = TaskStatus.COMPLETED
        return plan.results
    
    def get_agent_by_trigger(self, text: str) -> Optional[AgentType]:
        """根据触发词匹配Agent"""
        for agent_type, agent in self.agents.items():
            if hasattr(agent, 'triggers'):
                for trigger in agent.triggers:
                    if trigger in text:
                        return agent_type
        return None
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        if task_id in self.task_registry:
            return self.task_registry[task_id].to_dict()
        return None


agent_orchestrator = AgentOrchestrator()
