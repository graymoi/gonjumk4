"""
工作流测试
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow_engine import WorkflowEngine
from core.evolution_engine import EvolutionEngine
from core.evolution_monitor import EvolutionMonitor


class TestWorkflows(unittest.TestCase):
    """工作流测试"""
    
    def setUp(self):
        self.engine = WorkflowEngine()
    
    def test_all_intent_workflows(self):
        """测试所有意图类型的工作流"""
        intents = [
            "项目谋划", "项目筛选", "政策研究", "流程指导",
            "快速组装", "数据管理", "组合谋划", "打捆申报",
            "战略规划", "新闻监测", "资金申请"
        ]
        
        for intent in intents:
            workflow = self.engine.generate_workflow(
                {"intent": intent},
                {"requirements": {}}
            )
            
            self.assertGreater(
                len(workflow["steps"]), 0,
                f"意图 {intent} 的工作流步骤为空"
            )
    
    def test_workflow_execution(self):
        """测试工作流执行"""
        workflow = self.engine.generate_workflow(
            {"intent": "项目谋划"},
            {"requirements": {"项目类型": "老旧小区改造"}}
        )
        
        result = self.engine.execute_workflow(workflow, {})
        
        self.assertEqual(result["status"], "completed")
    
    def test_retry_mechanism(self):
        """测试重试机制"""
        self.assertEqual(self.engine.max_retries, 3)


class TestEvolutionEngine(unittest.TestCase):
    """进化引擎测试"""
    
    def setUp(self):
        self.engine = EvolutionEngine()
    
    def test_evolution_metrics(self):
        """测试进化指标"""
        metrics = self.engine.evolution_metrics
        
        self.assertIn("total_interactions", metrics)
        self.assertIn("successful_outputs", metrics)
        self.assertIn("parts_added", metrics)
    
    def test_evolution_after_interaction(self):
        """测试交互后进化"""
        interaction = {
            "id": "test_001",
            "scenario": "测试场景",
            "intent": "项目谋划",
            "skills_used": ["research-lookup"],
            "success": True
        }
        
        result = self.engine.evolve_after_interaction(interaction)
        
        self.assertIn("actions_taken", result)
    
    def test_pattern_analysis(self):
        """测试模式分析"""
        patterns = self.engine.analyze_patterns()
        
        self.assertIn("common_intents", patterns)
        self.assertIn("common_scenarios", patterns)
        self.assertIn("skill_usage", patterns)


class TestEvolutionMonitor(unittest.TestCase):
    """进化监控测试"""
    
    def setUp(self):
        self.monitor = EvolutionMonitor()
    
    def test_system_health(self):
        """测试系统健康检查"""
        health = self.monitor.get_system_health()
        
        self.assertIn("status", health)
        self.assertIn("metrics", health)
    
    def test_performance_metrics(self):
        """测试性能指标"""
        metrics = self.monitor.get_performance_metrics()
        
        self.assertIn("total_interactions", metrics)
        self.assertIn("success_rate", metrics)
    
    def test_alerts_check(self):
        """测试告警检查"""
        alerts = self.monitor.check_alerts()
        
        self.assertIsInstance(alerts, list)


if __name__ == '__main__':
    unittest.main()
