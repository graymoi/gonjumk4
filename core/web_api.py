"""
Web API服务
提供商业化API接口
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid

from core.agent_orchestrator import (
    AgentOrchestrator, 
    AgentType, 
    agent_orchestrator
)
from core.vector_memory import PolicyMemory, policy_memory
from core.sandbox_executor import (
    SandboxExecutor, 
    DataAnalysisSandbox,
    PolicyAnalysisSandbox,
    sandbox_executor
)


app = FastAPI(
    title="城乡建设政策知识服务API",
    description="提供政策查询、项目谋划、数据分析等API服务",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PolicyQueryRequest(BaseModel):
    query: str
    top_k: int = 5
    memory_type: Optional[str] = None


class ProjectPlanRequest(BaseModel):
    project_name: str
    project_type: str
    investment: float
    location: str
    description: Optional[str] = None


class CodeExecutionRequest(BaseModel):
    code: str
    context: Optional[Dict] = None
    timeout: int = 60


class DataAnalysisRequest(BaseModel):
    data: Dict
    operations: List[str]


class APIKey:
    """API密钥管理"""
    
    VALID_KEYS = {
        "demo_key": {"tier": "free", "rate_limit": 100},
        "pro_key": {"tier": "pro", "rate_limit": 1000},
        "enterprise_key": {"tier": "enterprise", "rate_limit": 10000}
    }
    
    @classmethod
    def verify(cls, api_key: str) -> Dict:
        if api_key not in cls.VALID_KEYS:
            raise HTTPException(status_code=401, detail="无效的API密钥")
        return cls.VALID_KEYS[api_key]


async def get_api_key(x_api_key: str = Header(...)):
    return APIKey.verify(x_api_key)


@app.get("/")
async def root():
    return {
        "service": "城乡建设政策知识服务API",
        "version": "3.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/v1/policy/query")
async def query_policy(
    request: PolicyQueryRequest,
    api_key: Dict = Depends(get_api_key)
):
    """政策查询接口"""
    try:
        results = policy_memory.recall(
            query=request.query,
            top_k=request.top_k,
            memory_type=request.memory_type
        )
        
        return {
            "success": True,
            "query": request.query,
            "results": results,
            "count": len(results),
            "tier": api_key["tier"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/policy/store")
async def store_policy(
    policy_name: str,
    policy_content: str,
    metadata: Optional[Dict] = None,
    api_key: Dict = Depends(get_api_key)
):
    """存储政策接口"""
    try:
        memory_id = policy_memory.store_policy(
            policy_name=policy_name,
            policy_content=policy_content,
            metadata=metadata or {}
        )
        
        return {
            "success": True,
            "memory_id": memory_id,
            "message": "政策存储成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/project/plan")
async def plan_project(
    request: ProjectPlanRequest,
    api_key: Dict = Depends(get_api_key)
):
    """项目谋划接口"""
    try:
        task = agent_orchestrator.create_task(
            agent_type=AgentType.PROJECT_PLANNER,
            input_data={
                "project_name": request.project_name,
                "project_type": request.project_type,
                "investment": request.investment,
                "location": request.location,
                "description": request.description
            }
        )
        
        result = agent_orchestrator.execute_task(task)
        
        return {
            "success": True,
            "task_id": task.task_id,
            "result": result,
            "tier": api_key["tier"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agent/execute")
async def execute_agent_task(
    agent_type: str,
    input_data: Dict,
    api_key: Dict = Depends(get_api_key)
):
    """执行Agent任务接口"""
    try:
        agent_type_enum = AgentType(agent_type)
        
        task = agent_orchestrator.create_task(
            agent_type=agent_type_enum,
            input_data=input_data
        )
        
        result = agent_orchestrator.execute_task(task)
        
        return {
            "success": True,
            "task_id": task.task_id,
            "agent_type": agent_type,
            "result": result
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的Agent类型: {agent_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/code/execute")
async def execute_code(
    request: CodeExecutionRequest,
    api_key: Dict = Depends(get_api_key)
):
    """代码执行接口（沙箱）"""
    if api_key["tier"] == "free":
        raise HTTPException(status_code=403, detail="免费版不支持代码执行")
    
    try:
        executor = SandboxExecutor(timeout=request.timeout)
        result = executor.execute_code(
            code=request.code,
            context=request.context
        )
        
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/data/analyze")
async def analyze_data(
    request: DataAnalysisRequest,
    api_key: Dict = Depends(get_api_key)
):
    """数据分析接口"""
    try:
        sandbox = DataAnalysisSandbox()
        result = sandbox.generate_statistics(
            data=request.data,
            operations=request.operations
        )
        
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/memory/stats")
async def get_memory_stats(api_key: Dict = Depends(get_api_key)):
    """获取记忆统计接口"""
    try:
        stats = policy_memory.stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agents/list")
async def list_agents():
    """列出所有可用Agent"""
    return {
        "agents": [
            {"type": "policy_collector", "name": "政策采集Agent", "triggers": ["采集", "入库", "归档"]},
            {"type": "project_planner", "name": "项目谋划Agent", "triggers": ["谋划", "包装", "申报"]},
            {"type": "project_filter", "name": "项目筛选Agent", "triggers": ["筛选", "排序", "规划"]},
            {"type": "policy_researcher", "name": "政策研究Agent", "triggers": ["研究", "趋势", "影响"]},
            {"type": "quick_assembler", "name": "快速组装Agent", "triggers": ["组装", "宣讲", "PPT"]},
            {"type": "data_manager", "name": "数据管理Agent", "triggers": ["管理", "更新", "验证"]}
        ]
    }


@app.get("/api/v1/pricing")
async def get_pricing():
    """获取定价信息"""
    return {
        "tiers": [
            {
                "name": "free",
                "price": 0,
                "features": ["政策查询", "记忆统计", "Agent列表"],
                "rate_limit": "100次/天"
            },
            {
                "name": "pro",
                "price": 999,
                "period": "月",
                "features": ["所有免费功能", "项目谋划", "代码执行", "数据分析"],
                "rate_limit": "1000次/天"
            },
            {
                "name": "enterprise",
                "price": 9999,
                "period": "月",
                "features": ["所有Pro功能", "无限调用", "专属支持", "定制开发"],
                "rate_limit": "无限制"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
