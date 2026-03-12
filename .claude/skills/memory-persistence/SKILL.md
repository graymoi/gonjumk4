---
name: memory-persistence
description: Automatically saves and loads context across sessions. Use when (1) session starts to load previous context, (2) session ends to save state, (3) user wants to remember something for next time. Maintains continuity between work sessions.
version: 1.0.0
---

# Memory Persistence

Automatically persist and restore context across Claude Code sessions.

## Overview

This skill ensures that important context, decisions, and progress are preserved between sessions, enabling seamless continuation of work.

## When to Use

1. **Session Start**: Load previous session context
2. **Session End**: Save current state and progress
3. **User Request**: "Remember this for next time"
4. **After Milestone**: Save progress after completing significant work

## Memory Structure

```
.memory/
├── session/
│   ├── current.json        # Current session state
│   └── history/            # Past sessions
│       └── YYYY-MM-DD_HH-MM-SS.json
├── project/
│   ├── decisions.json      # Architecture decisions
│   ├── progress.json       # Work progress
│   └── context.json        # Project context
└── knowledge/
    ├── learned.json        # Things learned
    └── patterns.json       # Discovered patterns
```

## Save Operations

### Save Session State

```python
def save_session_state():
    state = {
        "timestamp": datetime.now().isoformat(),
        "working_directory": os.getcwd(),
        "active_files": get_open_files(),
        "recent_commands": get_command_history(limit=10),
        "todo_list": get_current_todos(),
        "key_decisions": extract_key_decisions(),
        "next_steps": identify_next_steps()
    }
    
    save_to(".memory/session/current.json", state)
```

### Save Project Context

```python
def save_project_context():
    context = {
        "project_type": detect_project_type(),
        "tech_stack": detect_tech_stack(),
        "recent_changes": get_recent_commits(limit=5),
        "active_branch": get_current_branch(),
        "open_issues": get_open_issues()
    }
    
    save_to(".memory/project/context.json", context)
```

## Load Operations

### Load Previous Session

```python
def load_previous_session():
    if exists(".memory/session/current.json"):
        state = load_from(".memory/session/current.json")
        
        print(f"上次会话: {state['timestamp']}")
        print(f"工作目录: {state['working_directory']}")
        print(f"待办事项: {len(state['todo_list'])} 项")
        
        return state
    return None
```

## Integration with Policy Knowledge System

### Policy Memory

```json
{
  "last_policy_update": "2026-03-13",
  "total_policies": 150,
  "recent_additions": [
    "国办发〔2024〕52号",
    "建科〔2023〕45号"
  ],
  "pending_tasks": [
    "更新专项债券政策索引",
    "添加REITs政策解读"
  ]
}
```

### Project Memory

```json
{
  "active_projects": [
    {
      "name": "河东区城建谋划项目",
      "status": "in_progress",
      "last_work": "2026-03-12",
      "next_step": "生成项目谋划报告"
    }
  ]
}
```

## Hooks Configuration

```json
{
  "hooks": {
    "PreSessionStart": [
      {
        "type": "command",
        "command": "python .claude/hooks/load_memory.py"
      }
    ],
    "PostSessionEnd": [
      {
        "type": "command",
        "command": "python .claude/hooks/save_memory.py"
      }
    ]
  }
}
```

## Best Practices

1. **Save Frequently**: Save after each significant milestone
2. **Be Selective**: Don't save everything, focus on what's reusable
3. **Clean Up**: Periodically archive old sessions
4. **Version Control**: Add .memory/ to .gitignore for sensitive data

## See Also

- continuous-learning - Extract patterns from sessions
- claudeception - Create skills from discoveries
