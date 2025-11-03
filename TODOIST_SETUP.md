# Todoist Integration Setup for Agent-Cleo

## Overview
This integration allows Agent-Cleo and all sub-agents to create tasks directly in your Todoist workspace. Agents can create tasks, assign them to projects, set priorities, due dates, and labels.

## Setup Instructions

### 1. Get Your Todoist API Token

1. Log into Todoist at https://todoist.com
2. Go to **Settings** → **Integrations** → **Developer**
3. Scroll down to **API token** section
4. Copy your API token (it looks like: `a1b2c3d4e5f6...`)

### 2. Set Environment Variable

#### Windows (PowerShell)
```powershell
# Temporary (current session only)
$env:TODOIST_API_TOKEN = "your-api-token-here"

# Permanent (user level)
[System.Environment]::SetEnvironmentVariable('TODOIST_API_TOKEN', 'your-api-token-here', 'User')
```

#### Windows (Command Prompt)
```cmd
# Temporary (current session only)
set TODOIST_API_TOKEN=your-api-token-here

# Permanent (user level)
setx TODOIST_API_TOKEN "your-api-token-here"
```

#### macOS/Linux
```bash
# Add to ~/.bashrc or ~/.zshrc
export TODOIST_API_TOKEN="your-api-token-here"

# Then reload
source ~/.bashrc
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `todoist-api-python==2.1.4` along with other dependencies.

### 4. Test the Integration

Run the test script to verify everything works:

```bash
python todoist_integration.py
```

Expected output:
```
Todoist Integration Test
==================================================

Available Projects:
  - DecideWright
  - Studio55
  - SparkwireMedia
  - ThinTanks
  - Ascendore
  - Personal

Creating test task...
✓ Task created successfully!
  - Content: Test task from Agent-Cleo integration
  - Project: Ascendore
  - URL: https://todoist.com/app/task/...
```

### 5. Set Up Todoist Projects (Recommended)

Create projects in Todoist that match your business units:
- **DecideWright** - For DecideWright/RBPM/Predixtive/Greentabula/Greenledger tasks
- **Studio55** - For Studio55/Apportal/Trisingularity tasks
- **SparkwireMedia** - For SparkwireMedia/NoFatSmoker tasks
- **ThinTanks** - For ThinTanks tasks
- **Ascendore** - For general business and personal development tasks
- **Personal** - For personal goals (health, fitness, coaching)

## Usage by Agents

### For Agent-Cleo (Orchestration Tasks)

```python
from todoist_integration import create_task_for_andrew

# Create strategic task
result = create_task_for_andrew(
    content="Review Q4 strategic priorities",
    description="Prepare for strategic review meeting",
    project="Ascendore",
    priority=3,
    due="Friday",
    agent="Agent-Cleo"
)
```

### For Coach-Cleo (Weekly Planning)

```python
from todoist_integration import create_weekly_plan_tasks

# Create tasks from weekly planning session
weekly_tasks = [
    {
        "content": "Create DecideWright one-page offer",
        "description": "Focus on QRA Playbook value proposition",
        "project_name": "DecideWright",
        "priority": 4,
        "due_string": "Wednesday 5pm",
        "labels": ["sales", "closer-mode"]
    },
    {
        "content": "Outreach to 20 target organizations",
        "project_name": "DecideWright",
        "priority": 3,
        "due_string": "Friday",
        "labels": ["sales", "outreach"]
    },
    {
        "content": "Book 5 customer conversations",
        "project_name": "DecideWright",
        "priority": 4,
        "due_string": "Friday"
    }
]

result = create_weekly_plan_tasks(weekly_tasks, agent="Coach-Cleo")
print(result['message'])  # "Created 3 of 3 tasks"
```

### For Worker Agents (Task Execution)

#### Agent-CMO (Marketing Tasks)
```python
from todoist_integration import create_task_for_andrew

# Marketing campaign task
create_task_for_andrew(
    content="Launch DecideWright LinkedIn campaign",
    description="10 posts targeting compliance officers and risk managers",
    project="DecideWright",
    priority=2,
    due="next Monday",
    labels=["marketing", "social-media"],
    agent="Agent-CMO"
)
```

#### Agent-CPO (Product Tasks)
```python
# Product development task
create_task_for_andrew(
    content="Review Duncan's Quantitative AI Risk Engine demo",
    description="Scheduled delivery: Nov 14. Test core QRA features.",
    project="DecideWright",
    priority=4,
    due="Nov 14",
    labels=["product", "qra-playbook"],
    agent="Agent-CPO"
)
```

#### Agent-CSO (Sales Tasks)
```python
# Sales task
create_task_for_andrew(
    content="Follow up with 3 DecideWright prospects",
    description="Leads from last week's outreach campaign",
    project="DecideWright",
    priority=3,
    due="today",
    labels=["sales", "follow-up"],
    agent="Agent-CSO"
)
```

## Priority Levels

Use these priority levels consistently:
- **1 (Normal)**: Routine tasks, no urgency
- **2 (Medium)**: Important but not urgent
- **3 (High)**: Important and time-sensitive
- **4 (Urgent)**: Critical, needs immediate attention

## Due Date Formats

Todoist supports natural language for due dates:
- `"today"` - Due today
- `"tomorrow"` - Due tomorrow
- `"next Monday"` - Due next Monday
- `"Friday"` - Due this Friday
- `"Nov 15"` - Due November 15
- `"in 3 days"` - Due in 3 days
- `"every Monday"` - Recurring weekly

## Labels for Organization

Recommended labels to use:
- **Business Unit**: `decidwright`, `studio55`, `sparkwire`, `thintanks`
- **Activity Type**: `sales`, `marketing`, `product`, `finance`, `legal`
- **Priority Type**: `closer-mode`, `builder-mode`, `strategic`, `tactical`
- **Status**: `waiting`, `blocked`, `in-review`, `ready-to-start`

## API Routes (Flask Integration)

The integration is also available via Flask API endpoints (see app.py):

### Create Task
```bash
POST /api/todoist/task
Content-Type: application/json

{
  "content": "Task title",
  "description": "Task description",
  "project": "DecideWright",
  "priority": 3,
  "due": "Friday",
  "labels": ["sales"],
  "agent": "Agent-CMO"
}
```

### Create Multiple Tasks
```bash
POST /api/todoist/tasks/batch
Content-Type: application/json

{
  "tasks": [
    {"content": "Task 1", "project": "DecideWright", "priority": 3},
    {"content": "Task 2", "project": "Studio55", "priority": 2}
  ],
  "agent": "Coach-Cleo"
}
```

### List Projects
```bash
GET /api/todoist/projects
```

## Troubleshooting

### Error: "Todoist API token not provided"
- Make sure you've set the `TODOIST_API_TOKEN` environment variable
- Restart your terminal/IDE after setting the variable
- Verify the variable is set: `echo $env:TODOIST_API_TOKEN` (PowerShell) or `echo $TODOIST_API_TOKEN` (bash)

### Error: "Project not found"
- Check that the project exists in your Todoist workspace
- Project names are case-insensitive but must match exactly
- Use `get_available_projects()` to list all projects

### Tasks Not Appearing
- Check Todoist app/web to verify task was created
- Look in the Inbox if project name wasn't found
- Verify API token has correct permissions

## Best Practices

1. **Always include agent name**: Helps track which agent created the task
2. **Use project names consistently**: Map to business units
3. **Set appropriate priorities**: Don't overuse priority 4 (urgent)
4. **Add descriptive labels**: Makes filtering and searching easier
5. **Use natural due dates**: More flexible than hardcoded dates
6. **Batch create when possible**: More efficient for multiple tasks

## Integration with Weekly Planning

Coach-Cleo can use this integration during weekly planning sessions:

1. **Identify surgical strike priorities**
2. **Break down into specific tasks**
3. **Create tasks in Todoist with:**
   - Clear, actionable content
   - Appropriate project
   - Realistic due dates
   - Priority levels based on cashflow impact
4. **Track completion throughout the week**

Example workflow:
```python
# Coach-Cleo identifies priorities
priorities = [
    "Sell DecideWright QRA Playbook - 5 conversations",
    "Studio55 AI Services - land page + 10 outreach"
]

# Break down into tasks
tasks = [
    {
        "content": "Create DecideWright QRA one-page offer",
        "project_name": "DecideWright",
        "priority": 4,
        "due_string": "Wednesday"
    },
    {
        "content": "List 20 DecideWright target organizations",
        "project_name": "DecideWright",
        "priority": 3,
        "due_string": "Wednesday"
    },
    # ... more tasks
]

# Create in Todoist
result = create_weekly_plan_tasks(tasks, agent="Coach-Cleo")
```

## Security Notes

- **Never commit API tokens** to git repositories
- Use environment variables for API tokens
- Rotate API tokens periodically
- Limit token access to necessary permissions only

## Support

If you encounter issues:
1. Check Todoist API status: https://todoist.com/status
2. Verify API token at: https://todoist.com/prefs/integrations
3. Review error logs in the Flask app
4. Test with `python todoist_integration.py`

---

**Status**: ✅ Ready to use
**Version**: 1.0
**Last Updated**: November 3, 2025
