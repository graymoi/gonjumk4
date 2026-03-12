"""
自动化系统测试脚本
测试loop、调度和学习功能
"""

import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logger import get_system_logger
from core.auto_loop_engine import AutoLoopEngine, Task
from core.workflow_scheduler import WorkflowScheduler, WorkflowOrchestrator
from core.continuous_learning import ContinuousLearningEngine


class MockSystem:
    """模拟系统"""
    def __init__(self):
        self.logger = get_system_logger()
        
        from core.evolution_monitor import EvolutionMonitor
        from core.continuous_optimizer import ContinuousOptimizer
        
        self.evolution_monitor = EvolutionMonitor()
        self.continuous_optimizer = ContinuousOptimizer()
    
    def process(self, user_input):
        return {
            "status": "completed",
            "user_input": user_input,
            "timestamp": datetime.now().isoformat()
        }


def test_auto_loop_engine():
    """测试自动循环引擎"""
    print("\n" + "="*60)
    print("测试 1: 自动循环引擎")
    print("="*60)
    
    system = MockSystem()
    loop_engine = AutoLoopEngine(system)
    
    print("\n✓ 初始化成功")
    
    print("\n测试添加任务...")
    loop_engine.add_task("test_task_1", "policy_monitor", priority=3)
    loop_engine.add_task("test_task_2", "knowledge_update", priority=5)
    
    status = loop_engine.get_status()
    print(f"  队列大小: {status['queue_size']}")
    assert status['queue_size'] == 2, "任务添加失败"
    print("✓ 任务添加成功")
    
    print("\n测试执行单次循环...")
    loop_engine.run_once()
    print("✓ 单次循环执行成功")
    
    print("\n✅ 自动循环引擎测试通过")
    return True


def test_workflow_scheduler():
    """测试工作流调度器"""
    print("\n" + "="*60)
    print("测试 2: 工作流调度器")
    print("="*60)
    
    system = MockSystem()
    loop_engine = AutoLoopEngine(system)
    scheduler = WorkflowScheduler(loop_engine)
    
    print("\n✓ 初始化成功")
    
    print("\n测试调度任务...")
    schedule_time = datetime.now() + timedelta(seconds=5)
    scheduler.schedule_task(
        task_id="scheduled_test_1",
        task_type="policy_monitor",
        schedule_time=schedule_time,
        priority=3,
        data={"test": True}
    )
    
    pending = scheduler.get_pending_tasks()
    print(f"  待执行任务: {len(pending)}个")
    assert len(pending) == 1, "任务调度失败"
    print("✓ 任务调度成功")
    
    print("\n测试取消任务...")
    result = scheduler.cancel_task("scheduled_test_1")
    assert result, "取消任务失败"
    print("✓ 任务取消成功")
    
    print("\n✅ 工作流调度器测试通过")
    return True


def test_workflow_orchestrator():
    """测试工作流编排器"""
    print("\n" + "="*60)
    print("测试 3: 工作流编排器")
    print("="*60)
    
    system = MockSystem()
    loop_engine = AutoLoopEngine(system)
    scheduler = WorkflowScheduler(loop_engine)
    orchestrator = WorkflowOrchestrator(loop_engine, scheduler)
    
    print("\n✓ 初始化成功")
    
    print("\n测试创建工作流...")
    workflow_id = orchestrator.create_workflow(
        workflow_id="test_workflow_1",
        name="测试工作流",
        steps=[
            {
                "name": "步骤1: 政策监测",
                "type": "task",
                "task_type": "policy_monitor",
                "priority": 3
            },
            {
                "name": "步骤2: 知识更新",
                "type": "task",
                "task_type": "knowledge_update",
                "priority": 5
            }
        ]
    )
    
    workflows = orchestrator.list_workflows()
    print(f"  工作流数量: {len(workflows)}个")
    assert len(workflows) == 1, "工作流创建失败"
    print("✓ 工作流创建成功")
    
    print("\n测试执行工作流...")
    instance_id = orchestrator.execute_workflow(workflow_id, {"test": True})
    status = orchestrator.get_workflow_status(instance_id)
    print(f"  工作流状态: {status['status']}")
    print("✓ 工作流执行成功")
    
    print("\n✅ 工作流编排器测试通过")
    return True


def test_continuous_learning():
    """测试持续学习引擎"""
    print("\n" + "="*60)
    print("测试 4: 持续学习引擎")
    print("="*60)
    
    learning_engine = ContinuousLearningEngine()
    
    print("\n✓ 初始化成功")
    
    print("\n测试记录会话...")
    session_data = {
        "scenario": "项目谋划",
        "intent": {
            "intent": "project_planning",
            "keywords": ["老旧小区", "改造"],
            "confidence": 0.85
        },
        "workflow": {
            "workflow_name": "项目谋划工作流",
            "status": "completed",
            "steps": []
        },
        "skills_used": ["research-lookup", "office"],
        "errors": [],
        "optimizations": []
    }
    
    learning_engine.record_session(session_data)
    print("✓ 会话记录成功")
    
    print("\n测试提取模式...")
    patterns = learning_engine.extract_patterns(session_data)
    print(f"  提取模式: {len(patterns)}个")
    assert len(patterns) > 0, "模式提取失败"
    print("✓ 模式提取成功")
    
    print("\n测试查找适用模式...")
    applicable = learning_engine.find_applicable_patterns({
        "intent_type": "project_planning",
        "scenario": "项目谋划",
        "keywords": ["老旧小区"]
    })
    print(f"  适用模式: {len(applicable)}个")
    print("✓ 模式查找成功")
    
    print("\n测试进化模式...")
    learning_engine.evolve_patterns()
    print("✓ 模式进化成功")
    
    print("\n测试生成技能...")
    skills = learning_engine.generate_skill_from_patterns()
    print(f"  可生成技能: {len(skills)}个")
    print("✓ 技能生成检查完成")
    
    print("\n测试学习报告...")
    report = learning_engine.get_learning_report()
    print(f"  总模式数: {report['stats']['total_patterns']}")
    print(f"  学习事件: {report['stats']['learning_events']}")
    print("✓ 学习报告生成成功")
    
    print("\n✅ 持续学习引擎测试通过")
    return True


def test_integration():
    """集成测试"""
    print("\n" + "="*60)
    print("测试 5: 集成测试")
    print("="*60)
    
    system = MockSystem()
    loop_engine = AutoLoopEngine(system)
    scheduler = WorkflowScheduler(loop_engine)
    orchestrator = WorkflowOrchestrator(loop_engine, scheduler)
    learning_engine = ContinuousLearningEngine()
    
    print("\n✓ 所有组件初始化成功")
    
    print("\n测试完整流程...")
    
    print("  1. 创建工作流...")
    workflow_id = orchestrator.create_workflow(
        workflow_id="integration_test",
        name="集成测试工作流",
        steps=[
            {
                "name": "政策监测",
                "type": "task",
                "task_type": "policy_monitor"
            }
        ]
    )
    
    print("  2. 执行工作流...")
    instance_id = orchestrator.execute_workflow(workflow_id)
    
    print("  3. 记录学习...")
    session_data = {
        "scenario": "集成测试",
        "workflow": {
            "workflow_name": "集成测试工作流",
            "status": "completed"
        }
    }
    learning_engine.record_session(session_data)
    learning_engine.extract_patterns(session_data)
    
    print("  4. 检查状态...")
    loop_status = loop_engine.get_status()
    scheduler_stats = scheduler.get_scheduler_stats()
    learning_report = learning_engine.get_learning_report()
    
    print(f"     循环引擎: 迭代 #{loop_status['current_iteration']}")
    print(f"     调度器: {scheduler_stats['total_scheduled']}个任务")
    print(f"     学习引擎: {learning_report['stats']['total_patterns']}个模式")
    
    print("\n✅ 集成测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("自动化系统测试套件")
    print("="*60)
    
    tests = [
        ("自动循环引擎", test_auto_loop_engine),
        ("工作流调度器", test_workflow_scheduler),
        ("工作流编排器", test_workflow_orchestrator),
        ("持续学习引擎", test_continuous_learning),
        ("集成测试", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
            print(f"\n❌ {test_name} 测试失败: {e}")
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result, error in results:
        if result:
            print(f"✅ {test_name}: 通过")
            passed += 1
        else:
            print(f"❌ {test_name}: 失败")
            if error:
                print(f"   错误: {error}")
            failed += 1
    
    print(f"\n总计: {passed}个通过, {failed}个失败")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
        print("\n系统已准备好进行自动化持续工作。")
        print("\n使用方法:")
        print("  python main.py /loop start  - 启动自动化循环")
        print("  python main.py /loop status - 查看循环状态")
        print("  python main.py /学习 report - 查看学习报告")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息。")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
