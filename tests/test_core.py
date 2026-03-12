"""
核心模块测试
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logger import get_system_logger, SystemLogger
from core.output_manager import OutputManager
from core.intent_analyzer import IntentAnalyzer
from core.workflow_engine import WorkflowEngine


class TestLogger(unittest.TestCase):
    """日志系统测试"""
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        logger1 = get_system_logger()
        logger2 = get_system_logger()
        self.assertIs(logger1, logger2)
    
    def test_log_directories_created(self):
        """测试日志目录创建"""
        logger = get_system_logger()
        log_dir = Path("logs")
        self.assertTrue(log_dir.exists())
        self.assertTrue((log_dir / "system").exists())
        self.assertTrue((log_dir / "interactions").exists())


class TestOutputManager(unittest.TestCase):
    """输出管理器测试"""
    
    def setUp(self):
        self.manager = OutputManager()
    
    def test_create_output_dir(self):
        """测试创建输出目录"""
        output_dir = self.manager.create_output_dir("测试场景", "测试项目")
        self.assertTrue(output_dir.exists())
        self.assertIn("测试场景", str(output_dir))
    
    def test_index_created(self):
        """测试索引创建"""
        self.assertTrue(self.manager.index_file.exists())


class TestIntentAnalyzer(unittest.TestCase):
    """意图分析器测试"""
    
    def setUp(self):
        self.analyzer = IntentAnalyzer()
    
    def test_detect_intent(self):
        """测试意图检测"""
        result = self.analyzer.analyze("我想谋划一个老旧小区改造项目")
        self.assertEqual(result["intent"], "项目谋划")
    
    def test_extract_entities(self):
        """测试实体提取"""
        result = self.analyzer.analyze("谋划一个5000万的老旧小区改造项目")
        self.assertEqual(result["entities"]["投资额"], "5000万")
        self.assertEqual(result["entities"]["项目类型"], "老旧小区改造")
    
    def test_extract_keywords(self):
        """测试关键词提取"""
        result = self.analyzer.analyze("专项债券老旧小区改造项目谋划")
        self.assertIn("老旧小区", result["keywords"])
        self.assertIn("专项债券", result["keywords"])


class TestWorkflowEngine(unittest.TestCase):
    """工作流引擎测试"""
    
    def setUp(self):
        self.engine = WorkflowEngine()
    
    def test_generate_workflow(self):
        """测试工作流生成"""
        intent = {"intent": "项目谋划"}
        scenario = {"requirements": {}}
        
        workflow = self.engine.generate_workflow(intent, scenario)
        
        self.assertEqual(workflow["status"], "pending")
        self.assertGreater(len(workflow["steps"]), 0)
    
    def test_workflow_steps(self):
        """测试工作流步骤"""
        intent = {"intent": "项目谋划"}
        scenario = {"requirements": {}}
        
        workflow = self.engine.generate_workflow(intent, scenario)
        
        step_names = [s["action"] for s in workflow["steps"]]
        self.assertIn("需求分析", step_names)
        self.assertIn("报告生成", step_names)


if __name__ == '__main__':
    unittest.main()
