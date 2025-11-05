# Todoist Integration Updates - November 4, 2025

## Overview
Enhanced the Todoist integration to fix date issues and add task reading capabilities.

## Changes Made

### 1. Fixed Due Date Issues ✅
**Problem**: Tasks were created with relative dates like "tomorrow" which would shift over time.

**Solution**: Added automatic conversion from relative to absolute dates (YYYY-MM-DD format).

**Examples**:
- "tomorrow" → "2025-11-05"
- "next Monday" → "2025-11-10"
- "Friday" → "2025-11-07"
- "in 3 days" → "2025-11-07"

**Implementation**:
- New function: `convert_relative_to_absolute_date()` in `todoist_integration.py:14`
- Automatically converts dates before sending to Todoist API
- Works in both task creation and updates
- Supports: today, tomorrow, weekdays, "next/this week", "in X days"

### 2. Added Task Reading Functionality ✅
**Feature**: Read tasks from Todoist with "Agent-Cleo" label or any other filter.

**New Functions** (`todoist_integration.py`):
- `get_tasks(label, project_id)` - Get tasks with filters (line 343)
- `get_agent_cleo_tasks(include_completed)` - Get Agent-Cleo labeled tasks (line 385)
- `update_task(task_id, **kwargs)` - Update existing tasks (line 392)
- `close_task(task_id)` - Mark tasks as complete (line 423)

**Convenience Functions**:
- `get_agent_tasks(include_completed)` - Quick access to Agent-Cleo tasks (line 524)
- `get_tasks_by_label(label)` - Get tasks by any label (line 542)

### 3. New API Endpoints ✅
Added to `app.py`:

#### GET `/api/todoist/tasks`
Get tasks filtered by label or project
- Query params: `label` (optional), `include_completed` (default: false)
- Returns: List of tasks with full details

#### GET `/api/todoist/tasks/agent-cleo`
Get all tasks labeled with "Agent-Cleo"
- Query params: `include_completed` (default: false)
- Returns: Agent-Cleo tasks only

#### PUT `/api/todoist/task/<task_id>`
Update an existing task
- Body: `{content, description, due, priority, labels}`
- Returns: Success/error response

#### POST `/api/todoist/task/<task_id>/complete`
Mark a task as complete
- Returns: Success/error response

## Testing Results

### Date Conversion ✅
```
today: 2025-11-04
tomorrow: 2025-11-05
next Monday: 2025-11-10
Friday: 2025-11-07
in 3 days: 2025-11-07
```

### Task Reading ✅
Successfully read 11 Agent-Cleo labeled tasks:
```
1. Complete TT Invoice (Due: 2025-11-05, Priority: 4)
2. Catch-up call: Gary Carpenter (Due: 2025-11-05, Priority: 3)
3. Follow up TT termination payment (Due: 2025-11-05, Priority: 4)
4. Catch-up call: Jimmy Pewtress (Due: 2025-11-05, Priority: 3)
5. Test task - Date conversion test (Due: 2025-11-05, Priority: 1)
...and 6 more
```

### Task Creation ✅
Successfully created test task with absolute date conversion.

## Usage Examples

### Creating Tasks with Relative Dates (Automatically Converted)
```python
from todoist_integration import create_task_for_andrew

# These will all be converted to absolute dates
result = create_task_for_andrew(
    content="Review QRA Playbook",
    due="tomorrow",  # Converts to 2025-11-05
    project="DECIDEWRIGHT",
    priority=3
)

result = create_task_for_andrew(
    content="Weekly team meeting",
    due="next Monday",  # Converts to 2025-11-10
    project="WORK",
    priority=2
)
```

### Reading Agent-Cleo Tasks
```python
from todoist_integration import get_agent_tasks

# Get all active Agent-Cleo tasks
tasks = get_agent_tasks()
for task in tasks:
    print(f"{task['content']} - Due: {task['due']}")

# Include completed tasks
all_tasks = get_agent_tasks(include_completed=True)
```

### Reading Tasks by Custom Label
```python
from todoist_integration import get_tasks_by_label

# Get all sales tasks
sales_tasks = get_tasks_by_label("sales")

# Get all high priority tasks
urgent_tasks = get_tasks_by_label("urgent")
```

### Using API Endpoints
```bash
# Get Agent-Cleo tasks
curl http://localhost:5000/api/todoist/tasks/agent-cleo

# Get tasks by label
curl http://localhost:5000/api/todoist/tasks?label=sales

# Update a task
curl -X PUT http://localhost:5000/api/todoist/task/TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"due": "Friday", "priority": 4}'

# Complete a task
curl -X POST http://localhost:5000/api/todoist/task/TASK_ID/complete
```

## Benefits

### For Task Creation
✅ **Fixed**: Tasks now have concrete dates that don't shift
✅ **Improved**: Natural language still works ("tomorrow", "next Monday")
✅ **Reliable**: Dates are set at creation time, not interpreted later

### For Task Reading
✅ **New**: Can now read tasks created manually in Todoist
✅ **Integration**: Agent-Cleo can see tasks you add with "Agent-Cleo" label
✅ **Bidirectional**: Two-way communication between Agent-Cleo and Todoist
✅ **Visibility**: Agents can see what tasks are pending

## Use Cases

### Coach-Cleo Weekly Planning
1. Creates tasks with specific dates throughout the week
2. Can read back tasks to see what's been completed
3. Reviews progress in next session by checking completed tasks

### Task Delegation
1. You add a task in Todoist with "Agent-Cleo" label
2. Agent-Cleo reads it during next interaction
3. Agent-Cleo can process or delegate to appropriate agent

### Progress Tracking
1. Agents can check completion status of tasks they created
2. Generate weekly reports based on completed tasks
3. Adjust planning based on actual completion rates

## Files Modified

1. **todoist_integration.py**
   - Added: `convert_relative_to_absolute_date()` function
   - Added: `get_tasks()`, `get_agent_cleo_tasks()`, `update_task()`, `close_task()` methods
   - Added: Convenience functions for reading tasks
   - Modified: `create_task()` to use absolute date conversion
   - Fixed: Unicode characters for Windows compatibility

2. **app.py**
   - Added: 4 new API endpoints for reading and updating tasks
   - Line 472-578: New endpoints

## Next Steps

### Immediate
1. ✅ Test task creation with various date formats
2. ✅ Test task reading with Agent-Cleo label
3. ⏳ Update documentation (README, integration guides)

### Short-Term
1. Have Coach-Cleo use absolute dates in weekly planning
2. Set up workflow for reading tasks labeled "Agent-Cleo"
3. Create agent workflows that check task status

### Future Enhancements
1. Add task comments reading/writing
2. Add task attachment support
3. Create recurring task templates
4. Add task search by content/description
5. Implement task analytics and reporting

## Breaking Changes
None - All changes are backward compatible. Relative dates still work, they're just converted to absolute dates automatically.

## Migration Required
None - Existing code continues to work as before.

---

**Status**: ✅ Complete and Tested
**Date**: November 4, 2025
**Version**: 1.1.0
