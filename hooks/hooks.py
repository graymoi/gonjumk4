"""
钩子系统模块
提供工作流生命周期钩子
"""

import json
import subprocess
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from core.logger import get_system_logger


def load_config() -> Dict:
    """加载系统配置"""
    config_path = Path("config/system_config.yaml")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {"git": {"auto_commit": False}}


class HookManager:
    """钩子管理器"""
    
    def __init__(self):
        self.logger = get_system_logger()
        self.hooks_dir = Path("hooks")
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        
        self.hooks = {
            "pre_workflow": [],
            "post_workflow": [],
            "pre_step": [],
            "post_step": [],
            "on_error": [],
            "on_success": [],
            "on_learning": []
        }
        
        self._load_hooks()
    
    def _load_hooks(self):
        """加载钩子"""
        pass
    
    def register(self, hook_type: str, callback: Callable):
        """注册钩子"""
        if hook_type in self.hooks:
            self.hooks[hook_type].append(callback)
    
    def execute(self, hook_type: str, context: Dict) -> Dict:
        """执行钩子"""
        results = []
        
        for callback in self.hooks.get(hook_type, []):
            try:
                result = callback(context)
                results.append({
                    "hook": callback.__name__,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "hook": callback.__name__,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "hook_type": hook_type,
            "executed_at": datetime.now().isoformat(),
            "results": results
        }


def git_commit(context: Dict) -> Dict:
    """Git自动提交"""
    
    logger = get_system_logger()
    config = load_config()
    git_config = config.get("git", {})
    
    if not git_config.get("auto_commit", False):
        return {"status": "skipped", "reason": "auto_commit disabled"}
    
    try:
        scenario = context.get("workflow_result", {}).get("scenario", "工作流完成")
        message_template = git_config.get("commit_message_template", "feat: 完成{scenario}")
        commit_message = message_template.format(scenario=scenario)
        
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if not result.stdout.strip():
            return {"status": "skipped", "reason": "no changes"}
        
        subprocess.run(["git", "add", "."], cwd=Path.cwd(), check=True)
        
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=Path.cwd(),
            check=True
        )
        
        logger.info(f"Git提交成功: {commit_message}", module="hooks")
        
        if git_config.get("auto_push", False):
            subprocess.run(["git", "push"], cwd=Path.cwd(), check=True)
            logger.info("Git推送成功", module="hooks")
        
        return {
            "status": "committed",
            "message": commit_message,
            "files_changed": len(result.stdout.strip().split('\n'))
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Git提交失败: {e}", module="hooks")
        return {"status": "error", "error": str(e)}
    except Exception as e:
        logger.error(f"Git提交异常: {e}", module="hooks")
        return {"status": "error", "error": str(e)}


def pre_workflow_hook(context: Dict) -> Dict:
    """工作流执行前钩子"""
    
    logger = get_system_logger()
    logger.info(f"工作流开始: {context.get('workflow_name', 'unknown')}", module="hooks")
    
    context["started_at"] = datetime.now().isoformat()
    
    return {"status": "initialized"}


def post_workflow_hook(context: Dict) -> Dict:
    """工作流执行后钩子"""
    
    logger = get_system_logger()
    
    workflow_result = context.get("workflow_result", {})
    scenario = workflow_result.get("scenario", "unknown")
    
    log_path = Path("logs/interactions")
    log_path.mkdir(parents=True, exist_ok=True)
    
    log_file = log_path / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(workflow_result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"工作流完成: {scenario}", module="hooks")
    
    git_result = git_commit(context)
    if git_result.get("status") == "committed":
        logger.info(f"自动提交: {git_result.get('message')}", module="hooks")
    
    return {"status": "logged", "git": git_result}


def on_error_hook(context: Dict) -> Dict:
    """错误处理钩子"""
    
    logger = get_system_logger()
    error = context.get("error", "unknown error")
    workflow = context.get("workflow", {})
    
    logger.error(
        f"工作流错误: {workflow.get('workflow_name', 'unknown')} - {error}",
        module="hooks"
    )
    
    error_log = {
        "timestamp": datetime.now().isoformat(),
        "workflow": workflow.get("workflow_name"),
        "error": str(error),
        "step": context.get("step")
    }
    
    error_path = Path("logs/errors")
    error_path.mkdir(parents=True, exist_ok=True)
    
    error_file = error_path / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(error_file, 'w', encoding='utf-8') as f:
        json.dump(error_log, f, ensure_ascii=False, indent=2)
    
    return {"status": "error_logged"}


def on_learning_hook(context: Dict) -> Dict:
    """学习触发钩子"""
    
    logger = get_system_logger()
    
    interaction_result = context.get("interaction_result", {})
    
    learning_data = {
        "timestamp": datetime.now().isoformat(),
        "scenario": interaction_result.get("scenario"),
        "intent": interaction_result.get("intent"),
        "skills_used": interaction_result.get("skills_used", []),
        "success": interaction_result.get("success", False),
        "user_feedback": interaction_result.get("user_feedback")
    }
    
    learning_path = Path("logs/learning")
    learning_path.mkdir(parents=True, exist_ok=True)
    
    learning_file = learning_path / f"learning_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(learning_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(learning_data, ensure_ascii=False) + '\n')
    
    logger.info("学习数据已记录", module="hooks")
    
    return {"status": "learning_recorded"}


def auto_update_readme(context: Dict) -> Dict:
    """自动更新README"""
    
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        return {"status": "skipped", "reason": "README not found"}
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        update_marker = "<!-- AUTO_UPDATE -->"
        if update_marker in content:
            stats_section = f"""
## 系统统计

- 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 总交互次数: {context.get('total_interactions', 0)}
- 成功输出: {context.get('successful_outputs', 0)}
"""
            
            parts = content.split(update_marker)
            if len(parts) >= 2:
                new_content = parts[0] + update_marker + stats_section + update_marker + parts[-1]
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return {"status": "updated"}
        
        return {"status": "skipped", "reason": "no update marker"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def cleanup_old_logs(context: Dict) -> Dict:
    """清理旧日志"""
    
    from datetime import timedelta
    
    logs_dir = Path("logs")
    retention_days = context.get("retention_days", 30)
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    
    cleaned = 0
    
    for log_type in ["interactions", "workflows", "errors"]:
        log_path = logs_dir / log_type
        if log_path.exists():
            for log_file in log_path.glob("*.json*"):
                try:
                    file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        log_file.unlink()
                        cleaned += 1
                except Exception:
                    pass
    
    return {"status": "cleaned", "files_removed": cleaned}


hook_manager = HookManager()

hook_manager.register("pre_workflow", pre_workflow_hook)
hook_manager.register("post_workflow", post_workflow_hook)
hook_manager.register("on_error", on_error_hook)
hook_manager.register("on_learning", on_learning_hook)
