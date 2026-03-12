"""
适配器模块测试
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.base_adapter import BaseAdapter
from adapters.policy_adapter import PolicyAdapter


class TestBaseAdapter(unittest.TestCase):
    """基础适配器测试"""
    
    def setUp(self):
        class MockAdapter(BaseAdapter):
            def fetch(self, source, **kwargs):
                return [{"id": 1, "name": "test"}]
            
            def validate(self, data):
                return "id" in data
            
            def transform(self, data):
                return {"transformed": True, **data}
        
        self.adapter = MockAdapter()
    
    def test_process(self):
        """测试处理流程"""
        result = self.adapter.process("test_source")
        
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["valid"], 1)
        self.assertEqual(result["invalid"], 0)
    
    def test_save_and_load(self):
        """测试保存和加载"""
        data = [{"id": 1, "name": "test"}]
        path = "tests/test_data.json"
        
        self.assertTrue(self.adapter.save(data, path))
        
        loaded = self.adapter.load(path)
        self.assertEqual(loaded, data)
        
        Path(path).unlink(missing_ok=True)


class TestPolicyAdapter(unittest.TestCase):
    """政策适配器测试"""
    
    def setUp(self):
        self.adapter = PolicyAdapter()
    
    def test_extract_metadata(self):
        """测试元数据提取"""
        content = """---
file_number: 国办发〔2024〕52号
publishing_agency: 国务院办公厅
policy_name: 关于优化完善地方政府专项债券管理机制的意见
publishing_date: 20241225
status: 现行有效
---

# 正文内容
"""
        
        metadata = self.adapter._extract_metadata(content)
        
        self.assertEqual(metadata["file_number"], "国办发〔2024〕52号")
        self.assertEqual(metadata["publishing_agency"], "国务院办公厅")
    
    def test_extract_content(self):
        """测试正文提取"""
        content = """---
title: test
---

这是正文内容"""
        
        body = self.adapter._extract_content(content)
        self.assertEqual(body, "这是正文内容")
    
    def test_validate(self):
        """测试数据验证"""
        valid_data = {"file_path": "test.md", "content": "test"}
        invalid_data = {"file_path": "test.md"}
        
        self.assertTrue(self.adapter.validate(valid_data))
        self.assertFalse(self.adapter.validate(invalid_data))
    
    def test_transform(self):
        """测试数据转换"""
        data = {
            "file_path": "test.md",
            "file_name": "test.md",
            "metadata": {
                "policy_name": "测试政策",
                "file_number": "测试号"
            },
            "content": "测试内容"
        }
        
        result = self.adapter.transform(data)
        
        self.assertEqual(result["title"], "测试政策")
        self.assertEqual(result["file_number"], "测试号")
        self.assertEqual(result["source"], "policy_library")


if __name__ == '__main__':
    unittest.main()
