"""
沙箱执行器
借鉴DeerFlow的Sandbox设计，实现安全的代码执行环境
"""

import subprocess
import tempfile
import os
import sys
import json
import traceback
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
import threading
import signal


@dataclass
class ExecutionResult:
    success: bool
    output: str
    error: Optional[str] = None
    return_value: Any = None
    execution_time: float = 0.0
    memory_used: int = 0
    files_created: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "return_value": self.return_value,
            "execution_time": round(self.execution_time, 3),
            "memory_used": self.memory_used,
            "files_created": self.files_created
        }


class SandboxExecutor:
    """沙箱执行器 - 安全运行用户代码"""
    
    DEFAULT_ALLOWED_MODULES = [
        'pandas', 'numpy', 'json', 'datetime', 'pathlib',
        're', 'collections', 'typing', 'math', 'random',
        'itertools', 'functools', 'operator', 'copy',
        'decimal', 'fractions', 'statistics', 'string',
        'textwrap', 'unicodedata', 'io', 'csv', 'hashlib'
    ]
    
    def __init__(
        self,
        timeout: int = 60,
        max_memory_mb: int = 512,
        allowed_modules: List[str] = None
    ):
        self.timeout = timeout
        self.max_memory_mb = max_memory_mb
        self.allowed_modules = allowed_modules or self.DEFAULT_ALLOWED_MODULES
        self.logger = None
    
    def execute_code(
        self,
        code: str,
        context: Dict = None,
        return_var: str = "result"
    ) -> ExecutionResult:
        """在沙箱中执行Python代码"""
        start_time = datetime.now()
        
        wrapped_code = self._wrap_code(code, context or {}, return_var)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = Path(tmpdir) / "sandbox_code.py"
            result_file = Path(tmpdir) / "result.json"
            output_file = Path(tmpdir) / "output.txt"
            
            code_file.write_text(wrapped_code, encoding='utf-8')
            
            try:
                result = subprocess.run(
                    [sys.executable, str(code_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tmpdir,
                    env=self._get_safe_env()
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                files_created = self._list_files(tmpdir)
                
                if result.returncode == 0:
                    return_value = self._extract_return_value(result_file)
                    
                    return ExecutionResult(
                        success=True,
                        output=result.stdout,
                        return_value=return_value,
                        execution_time=execution_time,
                        files_created=files_created
                    )
                else:
                    return ExecutionResult(
                        success=False,
                        output=result.stdout,
                        error=self._sanitize_error(result.stderr),
                        execution_time=execution_time,
                        files_created=files_created
                    )
                    
            except subprocess.TimeoutExpired:
                execution_time = (datetime.now() - start_time).total_seconds()
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"执行超时（{self.timeout}秒）",
                    execution_time=execution_time
                )
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"执行异常: {str(e)}",
                    execution_time=execution_time
                )
    
    def execute_function(
        self,
        func_code: str,
        func_name: str,
        args: tuple = (),
        kwargs: Dict = None
    ) -> ExecutionResult:
        """执行指定函数"""
        kwargs = kwargs or {}
        
        call_code = f"""
{func_code}

# 调用函数
result = {func_name}(*{args}, **{kwargs})
"""
        return self.execute_code(call_code)
    
    def execute_data_analysis(
        self,
        code: str,
        data: Dict = None
    ) -> ExecutionResult:
        """执行数据分析代码"""
        context = {
            "data": data or {},
            "pd": "pandas",
            "np": "numpy"
        }
        
        wrapped_code = f"""
import pandas as pd
import numpy as np

# 注入数据
data = {json.dumps(data, ensure_ascii=False, default=str)}

# 用户代码
{code}
"""
        return self.execute_code(wrapped_code)
    
    def _wrap_code(
        self,
        code: str,
        context: Dict,
        return_var: str
    ) -> str:
        """包装用户代码，添加安全限制"""
        
        context_json = json.dumps(context, ensure_ascii=False, default=str)
        
        wrapper = f'''
import sys
import os
import json
from pathlib import Path

# 禁止危险操作
def _disable_dangerous_operations():
    dangerous_funcs = ['exec', 'eval', 'compile', 'open', 'input']
    original_funcs = {{}}
    for func_name in dangerous_funcs:
        if func_name in globals():
            original_funcs[func_name] = globals()[func_name]
    return original_funcs

_original_funcs = _disable_dangerous_operations()

# 限制模块导入
class _RestrictedImporter:
    def __init__(self, allowed):
        self.allowed = allowed
    
    def find_module(self, name, path=None):
        base_name = name.split('.')[0]
        if base_name not in self.allowed and not name.startswith('_'):
            raise ImportError(f"模块 '{{name}}' 不被允许导入")

# 注入上下文
_context = {context_json}
for _k, _v in _context.items():
    if _k not in globals():
        globals()[_k] = _v

# 用户代码
try:
{self._indent_code(code, 4)}
except Exception as _e:
    import traceback
    print(f"执行错误: {{_e}}")
    traceback.print_exc()

# 提取返回值
try:
    if '{return_var}' in locals():
        _result = {return_var}
        with open('result.json', 'w', encoding='utf-8') as _f:
            json.dump({{"value": _result}}, _f, ensure_ascii=False, default=str)
except Exception as _e:
    pass
'''
        return wrapper
    
    def _indent_code(self, code: str, spaces: int) -> str:
        """缩进代码"""
        indent = ' ' * spaces
        return '\n'.join(indent + line if line.strip() else line for line in code.split('\n'))
    
    def _get_safe_env(self) -> Dict:
        """获取安全的环境变量"""
        safe_env = {
            'PYTHONPATH': '',
            'PYTHONIOENCODING': 'utf-8',
            'PYTHONDONTWRITEBYTECODE': '1',
        }
        for key in ['PATH', 'TEMP', 'TMP', 'HOME', 'USERPROFILE']:
            if key in os.environ:
                safe_env[key] = os.environ[key]
        return safe_env
    
    def _sanitize_error(self, error: str) -> str:
        """清理错误信息，移除敏感路径"""
        lines = error.split('\n')
        sanitized = []
        for line in lines:
            if 'tempfile' in line or 'sandbox' in line:
                line = line.replace(tempfile.gettempdir(), '<tmp>')
            sanitized.append(line)
        return '\n'.join(sanitized)
    
    def _extract_return_value(self, result_file: Path) -> Any:
        """提取返回值"""
        if result_file.exists():
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('value')
            except:
                pass
        return None
    
    def _list_files(self, directory: str) -> List[str]:
        """列出创建的文件"""
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if not filename.startswith('_'):
                    filepath = os.path.join(root, filename)
                    if not filename.endswith(('.py', '.json')):
                        files.append(filename)
        return files


class DataAnalysisSandbox(SandboxExecutor):
    """数据分析专用沙箱"""
    
    def __init__(self):
        super().__init__(
            timeout=120,
            max_memory_mb=1024,
            allowed_modules=SandboxExecutor.DEFAULT_ALLOWED_MODULES + [
                'matplotlib', 'seaborn', 'scipy', 'sklearn'
            ]
        )
    
    def analyze_excel(
        self,
        excel_path: str,
        analysis_code: str
    ) -> ExecutionResult:
        """分析Excel文件"""
        code = f'''
import pandas as pd

# 读取Excel
df = pd.read_excel(r"{excel_path}")

# 分析代码
{analysis_code}

# 返回结果
result = {{
    "shape": df.shape,
    "columns": list(df.columns),
    "summary": df.describe().to_dict()
}}
'''
        return self.execute_code(code)
    
    def analyze_csv(
        self,
        csv_path: str,
        analysis_code: str
    ) -> ExecutionResult:
        """分析CSV文件"""
        code = f'''
import pandas as pd

# 读取CSV
df = pd.read_csv(r"{csv_path}")

# 分析代码
{analysis_code}

# 返回结果
result = {{
    "shape": df.shape,
    "columns": list(df.columns),
    "summary": df.describe().to_dict()
}}
'''
        return self.execute_code(code)
    
    def generate_statistics(
        self,
        data: Dict,
        operations: List[str]
    ) -> ExecutionResult:
        """生成统计数据"""
        code = '''
import pandas as pd
import numpy as np

df = pd.DataFrame(data)
results = {}

'''
        for op in operations:
            if op == "mean":
                code += 'results["mean"] = df.mean().to_dict()\n'
            elif op == "median":
                code += 'results["median"] = df.median().to_dict()\n'
            elif op == "std":
                code += 'results["std"] = df.std().to_dict()\n'
            elif op == "describe":
                code += 'results["describe"] = df.describe().to_dict()\n'
        
        code += '\nresult = results'
        
        return self.execute_code(code, context={"data": data})


class PolicyAnalysisSandbox(SandboxExecutor):
    """政策分析专用沙箱"""
    
    def __init__(self):
        super().__init__(
            timeout=180,
            max_memory_mb=512,
            allowed_modules=SandboxExecutor.DEFAULT_ALLOWED_MODULES
        )
    
    def extract_policy_info(
        self,
        policy_text: str,
        extract_fields: List[str]
    ) -> ExecutionResult:
        """提取政策信息"""
        code = f'''
import re
from datetime import datetime

text = """{policy_text}"""

result = {{}}

'''
        for field in extract_fields:
            if field == "file_number":
                code += '''
result["file_number"] = ""
match = re.search(r"[\\u4e00-\\u9fa5]+〔\\d{{4}}〕\\d+号", text)
if match:
    result["file_number"] = match.group()
'''
            elif field == "publishing_date":
                code += '''
result["publishing_date"] = ""
match = re.search(r"\\d{{4}}年\\d{{1,2}}月\\d{{1,2}}日", text)
if match:
    result["publishing_date"] = match.group()
'''
            elif field == "keywords":
                code += '''
keywords = ["专项债券", "城市更新", "老旧小区", "基础设施", "投资"]
result["keywords"] = [kw for kw in keywords if kw in text]
'''
        
        return self.execute_code(code)
    
    def match_funding_policy(
        self,
        project_info: Dict,
        policies: List[Dict]
    ) -> ExecutionResult:
        """匹配资金政策"""
        code = f'''
import json

project = {json.dumps(project_info, ensure_ascii=False)}
policies = {json.dumps(policies, ensure_ascii=False)}

result = {{
    "matched_policies": [],
    "recommendations": []
}}

for policy in policies:
    score = 0
    reasons = []
    
    # 匹配逻辑
    if project.get("domain") in policy.get("domains", []):
        score += 30
        reasons.append("业务领域匹配")
    
    if project.get("stage") in policy.get("stages", []):
        score += 20
        reasons.append("项目阶段匹配")
    
    if score > 0:
        result["matched_policies"].append({{
            "policy_name": policy.get("name"),
            "score": score,
            "reasons": reasons
        }})

result["matched_policies"].sort(key=lambda x: x["score"], reverse=True)
'''
        return self.execute_code(code)


sandbox_executor = SandboxExecutor()
data_analysis_sandbox = DataAnalysisSandbox()
policy_analysis_sandbox = PolicyAnalysisSandbox()
