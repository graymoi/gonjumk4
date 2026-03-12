# Skills 安装指南

## 已创建的Skills

以下Skills已创建在项目目录 `.claude/skills/` 中：

| Skill | 描述 | 状态 |
|-------|------|------|
| `claudeception` | 持续学习系统，自动从会话提取可复用知识 | ✅ 已创建 |
| `continuous-learning` | 自动提取模式并保存为可复用技能 | ✅ 已创建 |
| `memory-persistence` | 跨会话记忆持久化 | ✅ 已创建 |
| `policy-project-planning` | 政策项目谋划完整工作流 | ✅ 已创建 |

## 手动安装到Trae

由于权限限制，需要手动复制到Trae skills目录：

```powershell
# 在PowerShell中运行

# 源目录
$sourcePath = "d:\LMAI\001工具人mk4\.claude\skills"

# 目标目录
$traePath = "$env:USERPROFILE\.trae-cn\skills"

# 复制所有skills
Copy-Item -Path "$sourcePath\memory-persistence" -Destination $traePath -Recurse -Force
Copy-Item -Path "$sourcePath\policy-project-planning" -Destination $traePath -Recurse -Force

Write-Host "Skills安装完成！" -ForegroundColor Green
```

## Trae Skills 格式说明

Trae使用的SKILL.md格式：

```yaml
---
name: skill-name
description: 简短描述，包含触发条件
version: 1.0.0  # 可选
---

# Skill内容
...
```

## 已安装的核心Skills

Trae目录中已有的相关Skills：

| Skill | 用途 |
|-------|------|
| `claudeception` | 持续学习（已存在） |
| `continuous-learning` | 模式提取（已存在） |
| `brainstorming` | 创意头脑风暴 |
| `writing-plans` | 编写实施计划 |
| `test-driven-development` | 测试驱动开发 |
| `systematic-debugging` | 系统调试 |
| `verification-before-completion` | 完成前验证 |

## everything-claude-code 借鉴内容

从 `everything-claude-code` 仓库中值得借鉴的内容：

### 1. Agents（代理）
- `planner.md` - 功能实现规划
- `architect.md` - 系统设计决策
- `code-reviewer.md` - 代码审查
- `security-reviewer.md` - 安全审查

### 2. Commands（命令）
- `/tdd` - 测试驱动开发
- `/plan` - 实现规划
- `/code-review` - 代码审查
- `/checkpoint` - 保存验证状态
- `/verify` - 运行验证循环

### 3. Hooks（钩子）
- `memory-persistence/` - 会话生命周期钩子
- `strategic-compact/` - 压缩建议

### 4. Rules（规则）
- `common/coding-style.md` - 编码风格
- `common/testing.md` - 测试规范
- `common/security.md` - 安全检查

## 下一步建议

1. **手动复制Skills** - 运行上述PowerShell命令
2. **配置Hooks** - 在 `.trae/settings.json` 中添加钩子配置
3. **测试Skills** - 重启Trae后测试新Skills

## 验证安装

```powershell
# 检查已安装的Skills
Get-ChildItem "$env:USERPROFILE\.trae-cn\skills" -Name | Select-String "memory|policy|continuous"
```

---

*创建时间: 2026-03-13*
