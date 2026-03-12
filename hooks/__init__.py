"""
钩子系统
"""

from .hooks import (
    HookManager,
    hook_manager,
    pre_workflow_hook,
    post_workflow_hook,
    on_error_hook,
    on_learning_hook,
    auto_update_readme,
    cleanup_old_logs
)

__all__ = [
    'HookManager',
    'hook_manager',
    'pre_workflow_hook',
    'post_workflow_hook',
    'on_error_hook',
    'on_learning_hook',
    'auto_update_readme',
    'cleanup_old_logs'
]
