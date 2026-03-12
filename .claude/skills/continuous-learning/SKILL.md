---
name: continuous-learning
description: Automatically extracts patterns from Claude Code sessions and saves them as reusable skills. Use when (1) user says "learn from this", (2) after completing a complex task, (3) when discovering non-obvious solutions, (4) user asks to save knowledge. Creates structured skills with frontmatter, trigger conditions, and solutions.
version: 2.0.0
---

# Continuous Learning

Automatically learn from your work sessions and create reusable skills.

## When to Learn

Invoke this skill when:

1. **Complex Task Completed**: Finished a task that required significant investigation
2. **Non-Obvious Solution Found**: Discovered a solution that wasn't immediately apparent
3. **Error Resolved**: Fixed an error where the root cause was misleading
4. **Pattern Discovered**: Found a reusable pattern or best practice
5. **User Request**: User explicitly asks to "learn from this" or "save this"

## Learning Process

### Step 1: Analyze the Session

Review what was accomplished:

```markdown
## Session Analysis

### Task
[What was the goal?]

### Challenge
[What made this difficult?]

### Solution
[What actually worked?]

### Key Insight
[What would help future sessions?]
```

### Step 2: Extract Knowledge

Identify extractable knowledge:

| Type | Description | Example |
|------|-------------|---------|
| Error Resolution | Specific error → actual fix | "Module not found" → check case sensitivity |
| Workflow Pattern | Reusable process | Policy analysis → extraction → matching |
| Configuration | Project-specific setup | Environment variables, paths |
| Integration | Tool/library usage | How to use a specific API |
| Optimization | Efficiency improvement | Faster way to accomplish task |

### Step 3: Check for Existing Skills

Before creating, search for similar skills:

```bash
# Search existing skills
rg -i "keyword" ~/.claude/skills/ .claude/skills/ 2>/dev/null
```

If found:
- Same issue → Update existing skill
- Similar but different → Create new, cross-reference
- Not found → Create new skill

### Step 4: Create Skill

Structure the skill:

```markdown
---
name: skill-name
description: Brief description with trigger conditions. Use when (1) condition1, (2) condition2.
metadata:
  version: 1.0.0
---

# Skill Title

## Problem
[What problem does this solve?]

## Trigger Conditions
- Condition 1
- Condition 2

## Solution
[Step-by-step solution]

## Example
[Concrete example]

## References
- [Link to documentation]
```

### Step 5: Save and Index

Save location:
- Project-specific: `.claude/skills/skill-name/SKILL.md`
- User-wide: `~/.claude/skills/skill-name/SKILL.md`

Update index:
```bash
# Add to skill index
echo "- skill-name: Brief description" >> .claude/skills/INDEX.md
```

## Quality Criteria

Before saving, verify:

- [ ] **Reusable**: Will this help future tasks?
- [ ] **Specific**: Clear trigger conditions?
- [ ] **Verified**: Solution actually works?
- [ ] **Non-trivial**: Requires discovery, not just docs?

## Learning Triggers

Automatic triggers:

```
After task completion:
├── Time spent > 10 minutes? → Consider learning
├── Multiple attempts needed? → Likely learnable
├── Error message misleading? → Definitely learnable
└── Solution non-obvious? → Extract skill
```

## Session Review Template

Use this template at session end:

```markdown
# Session Review - [Date]

## Tasks Completed
1. [Task 1]
2. [Task 2]

## Knowledge Extracted
1. [Skill name] - [Brief description]
2. [Skill name] - [Brief description]

## Patterns Discovered
- [Pattern 1]
- [Pattern 2]

## Skills Updated
- [Skill name] - [What changed]

## Next Session Notes
- [Reminder for next time]
```

## Integration with Policy Knowledge System

For this project specifically:

### Policy Learning
- Extract policy patterns from successful matches
- Learn from failed funding applications
- Document regulatory changes

### Project Planning Learning
- Record successful project structures
- Note funding source preferences
- Track approval patterns

### Workflow Learning
- Optimize report generation
- Improve data processing
- Streamline policy analysis

## Examples

### Example 1: Error Resolution

```markdown
---
name: policy-file-not-found
description: Resolves policy file not found errors. Use when (1) FileNotFoundError for policy files, (2) policy lookup returns empty.
metadata:
  version: 1.0.0
---

## Problem
Policy files not found despite existing in directory.

## Trigger Conditions
- FileNotFoundError when loading policy
- Policy search returns empty results

## Solution
1. Check file encoding (must be UTF-8)
2. Verify naming convention matches pattern
3. Check for hidden characters in filename
4. Ensure directory is in search path

## Root Cause
Policy adapter expects specific naming format: `[发文号]_[机关]_[名称]_[日期].md`
```

### Example 2: Workflow Pattern

```markdown
---
name: project-planning-workflow
description: Standard workflow for project planning. Use when (1) user requests project planning, (2) creating funding proposals.
metadata:
  version: 1.0.0
---

## Workflow

1. **Gather Requirements**
   - Project name, type, investment
   - Location, timeline
   - Funding preferences

2. **Policy Matching**
   - Search policy database
   - Filter by domain
   - Rank by relevance

3. **Generate Report**
   - Use template
   - Include matched policies
   - Add recommendations

4. **Review & Export**
   - Quality check
   - Export to PDF/Word
```

## See Also

- claudeception - Full continuous learning system
- skill-authoring - How to write skills
- verification-before-completion - Verify before saving
