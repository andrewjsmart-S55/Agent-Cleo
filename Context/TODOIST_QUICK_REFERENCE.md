# Todoist Quick Reference for Agents

## Quick Start

```python
from todoist_integration import create_task_for_andrew

result = create_task_for_andrew(
    content="Task title",
    description="What needs to be done",
    project="DecideWright",
    priority=3,
    due="Friday",
    agent="Agent-Name"
)
```

## Projects

| Project | Use For |
|---------|---------|
| DecideWright | QRA Playbook, RBPM, Predixtive, Greentabula, Greenledger |
| Studio55 | AI services, Apportal, Trisingularity |
| SparkwireMedia | Content, media, NoFatSmoker |
| ThinTanks | Research and advisory |
| Ascendore | General business operations |
| Personal | Personal development, health, fitness |

## Priorities

| Level | When to Use | Example |
|-------|-------------|---------|
| 4 (Urgent) | Cashflow impact, critical | "Book 5 customer calls by Friday" |
| 3 (High) | Important + time-sensitive | "Review pricing strategy by Wednesday" |
| 2 (Medium) | Important but flexible | "Draft marketing content next week" |
| 1 (Normal) | Routine, no urgency | "Update documentation" |

## Due Date Examples

```python
due="today"           # Due today
due="tomorrow"        # Due tomorrow
due="Friday"          # This Friday
due="next Monday"     # Next Monday
due="Nov 15"          # Specific date
due="in 3 days"       # Relative date
due="every Monday"    # Recurring
```

## Common Labels

**Business Unit**: `decidwright`, `studio55`, `sparkwire`, `thintanks`

**Activity Type**: `sales`, `marketing`, `product`, `finance`, `legal`

**Mode**: `closer-mode`, `builder-mode`, `strategic`, `tactical`

**Status**: `waiting`, `blocked`, `in-review`, `ready`

## Usage by Agent Type

### Coach-Cleo (Weekly Planning)
```python
from todoist_integration import create_weekly_plan_tasks

tasks = [
    {
        "content": "Create one-page offer",
        "project_name": "DecideWright",
        "priority": 4,
        "due_string": "Wednesday"
    }
]
result = create_weekly_plan_tasks(tasks, agent="Coach-Cleo")
```

### Worker Agents (Single Tasks)
```python
create_task_for_andrew(
    content="Review marketing campaign results",
    description="Analysis of Q4 LinkedIn campaign performance",
    project="DecideWright",
    priority=2,
    due="Friday",
    labels=["marketing", "analytics"],
    agent="Agent-CMO"
)
```

### Team MDs (Strategic Tasks)
```python
create_task_for_andrew(
    content="Strategic review: QRA Playbook positioning",
    description="Analyze competitor pricing and refine value prop",
    project="DecideWright",
    priority=3,
    due="next Monday",
    agent="DecideWright-MD"
)
```

## When to Create Tasks

✅ **DO create tasks when:**
- You've completed work that needs Andrew's review
- You need Andrew to make a decision
- You're recommending an action for Andrew
- Weekly planning identifies specific actions
- Something requires Andrew's direct execution

❌ **DON'T create tasks when:**
- You can complete the work yourself
- It's already in progress by another agent
- It's too vague or not actionable
- No clear due date or priority

## Error Handling

```python
result = create_task_for_andrew(...)

if result['success']:
    print(f"✓ Task created: {result['url']}")
else:
    print(f"✗ Failed: {result['error']}")
```

## Full Documentation

- **Setup**: `TODOIST_SETUP.md`
- **Complete Guide**: `TODOIST_INTEGRATION_SUMMARY.md`
- **Main Manifest**: `Prompt Manifest - Agent-Cleo.md`

## Test Integration

```bash
python todoist_integration.py
```

---

**Keep tasks**: Clear, Actionable, Time-bound, Measurable
