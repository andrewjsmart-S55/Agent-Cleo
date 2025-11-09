# Agent-Cleo Telegram Bot - Full Interaction Guide

## Overview

The Agent-Cleo Telegram Bot now provides **full agent interaction capabilities**, allowing you to:
- ✅ **Approve or reject** actions proposed by agents
- 📬 **Receive proactive notifications** from agents
- 🎯 **Manage goals** directly via Telegram
- 🚀 **Trigger agent workflows** on-demand
- 💬 **Interact naturally** with all your agents

---

## New Features

### 1. Action Approval System

Agents can now request your approval before taking actions. You'll receive a Telegram message with details and inline buttons to approve or reject.

**How it works:**
1. An agent proposes an action (e.g., "Create a high-priority task for QRA marketing")
2. You receive a notification with action details
3. Click ✅ **Approve** or ❌ **Reject**
4. If approved, the action executes automatically

**Commands:**
- `/pending` - View all pending approvals
- `/history` - View your action history (approved/rejected)

**Example Flow:**
```
Agent-Cleo: I recommend creating a task for the QRA Playbook marketing material.

[Message with Approve/Reject buttons appears]

You: [Click Approve]

Agent-Cleo: ✅ Task created in Todoist!
```

### 2. Goal Management via Telegram

Interact with your Goal Management Framework directly through Telegram.

**Commands:**
- `/goals` or `/goals all` - View all goals
- `/goals weekly` - View weekly goals
- `/goals short` - View short-term (quarterly) goals
- `/goals long` - View long-term (3-5 year) goals
- `/goals stats` - View goal statistics

**Focus & Planning:**
- `/focus` - Get your #1 priority for today
- `/weekly_planning` - Start your weekly planning session with Coach-Cleo
- `/goal_review [daily|weekly|monthly]` - Review goal progress
- `/briefing` - Get your daily briefing

**Example:**
```
You: /focus

Agent-Cleo: 🎯 Your ONE Thing Today

Focus on: Complete QRA Playbook marketing one-pager
Due: Friday

Other Active Goals (2):
• Send proposals to 5 target organizations
• Finish Boxzero code integration

💡 Tip: Complete one goal at a time. Finish before you start something new!
```

### 3. Workflow Triggers

Trigger specific agent workflows on-demand.

**Command:**
```
/agent_run <agent-name> <workflow-type> [context]
```

**Available Workflows:**
- `analyze` - Analyze current situation
- `plan` - Create a detailed plan
- `report` - Get status report
- `brainstorm` - Brainstorm ideas
- `review` - Review and suggest improvements

**Examples:**
```
/agent_run DecideWright-MD analyze
/agent_run Coach-Cleo plan
/agent_run Agent-CMO brainstorm new marketing campaign
```

### 4. Proactive Notifications

Agents can now send you proactive updates, reminders, and alerts.

**Types of Notifications:**
- ℹ️ **Info** - General updates and information
- ⚠️ **Warning** - Important alerts
- ✅ **Success** - Completion confirmations
- 🔔 **Action Required** - Urgent items needing attention

Agents use the `send_notification` tool to keep you informed automatically.

### 5. Daily Briefing & Reviews

**Daily Briefing** (`/briefing`):
- Your weekly goals
- Today's tasks
- Priority recommendations

**Goal Reviews** (`/goal_review [type]`):
- `daily` - Quick daily check-in
- `weekly` - Weekly progress review
- `monthly` - Monthly goal assessment
- `quarterly` - Strategic quarterly review

---

## Agent Tools

Agents now have access to these tools when interacting with you:

### 1. `create_todoist_task`
Create tasks in your Todoist automatically.

**Parameters:**
- `task_details` - Task description
- `project` - Project name (Personal, DecideWright, Studio55, etc.)
- `priority` - Priority level (1-4)
- `due` - Due date (natural language)

### 2. `request_approval`
Request your approval before taking an action.

**Parameters:**
- `action_type` - Type of action
- `description` - What the agent wants to do
- `action_data` - Data needed to execute
- `context` - Additional context

### 3. `send_notification`
Send you a proactive notification.

**Parameters:**
- `title` - Notification title
- `message` - Notification message
- `notification_type` - Type (info, warning, success, action_required)
- `priority` - Priority level

### 4. `schedule_reminder`
Schedule a future reminder.

**Parameters:**
- `reminder_text` - Reminder message
- `when` - When to send (e.g., "in 1 hour", "tomorrow at 9am")

---

## Complete Command Reference

### Basic Commands
| Command | Description |
|---------|-------------|
| `/start` | Welcome message and introduction |
| `/help` | Show help message |
| `/agents` | List all available agents |
| `/reset` | Clear conversation history |

### Goal Management
| Command | Description |
|---------|-------------|
| `/goals [type]` | View goals (weekly, short, long, stats, all) |
| `/focus` | Get your #1 priority for today |
| `/weekly_planning` | Start weekly planning with Coach-Cleo |
| `/goal_review [type]` | Review goals (daily, weekly, monthly, quarterly) |
| `/briefing` | Get daily briefing |

### Actions & Approvals
| Command | Description |
|---------|-------------|
| `/pending` | View pending approvals |
| `/history` | View action history |
| `/task [description]` | Create a Todoist task |

### Agent Workflows
| Command | Description |
|---------|-------------|
| `/coach [message]` | Talk to Coach-Cleo |
| `/agent_run <agent> <workflow>` | Trigger agent workflow |

---

## Architecture

### Components

**New Files:**
1. **`action_manager.py`** - Manages action approval workflow
   - Create, approve, reject, modify actions
   - Track history and statistics
   - Persistent storage (JSON)

2. **`notification_service.py`** - Handles proactive notifications
   - Queue and schedule notifications
   - Watch agent Output folders for changes
   - Send reminders at scheduled times

3. **`workflow_triggers.py`** - Agent workflow execution
   - Weekly planning automation
   - Goal reviews (daily/weekly/monthly/quarterly)
   - Daily briefing generation
   - Custom agent workflows

4. **`goal_commands.py`** - Goal management interface
   - Display goals by priority
   - Show statistics
   - Get focus recommendations
   - Create new goals

**Enhanced Files:**
1. **`agent_handler.py`** - Added new Claude tools
   - `request_approval` tool
   - `send_notification` tool
   - `schedule_reminder` tool
   - Integration with action_manager and notification_service

2. **`bot.py`** - Added new commands and handlers
   - All new command handlers
   - Callback handler for inline keyboards
   - Updated help text

### Data Storage

The bot creates a `data/` directory to store:
- `pending_actions.json` - Actions awaiting approval
- `action_history.json` - Historical actions
- `notifications.json` - Notification queue
- `output_watchers.json` - Agent output monitoring

---

## Usage Examples

### Example 1: Weekly Planning
```
You: /weekly_planning

Bot: Starting your weekly planning session with Coach-Cleo...

Coach-Cleo: Let's review your progress from last week and plan for this week.

Last Week:
✅ Completed QRA marketing one-pager
✅ Sent 5 proposals
⏸️ Boxzero integration (in progress)

This Week's Recommendations:
1. Complete Boxzero integration (supports: Launch Apportal by December)
2. Follow up with 5 prospects (supports: £100K revenue by June)
3. Create DecideWright demo video (supports: 100 organizations by Q1)

Each goal is achievable this week and supports your Short Term Goals.
Ready to commit to these?
```

### Example 2: Action Approval
```
[Agent wants to create a task]

Bot: **Action #123456**
Agent: Coach-Cleo
Type: create_task

**Description:**
Create high-priority task for QRA Playbook follow-up with prospects

**Task Details:**
• Task: Follow up with 5 QRA prospects from last week
• Project: DecideWright
• Priority: P2
• Due: Friday

[✅ Approve] [❌ Reject]

You: [Click Approve]

Bot: ✅ Approved and Executed
Task created in Todoist!
```

### Example 3: Daily Focus
```
You: /focus

Bot: 🎯 Your ONE Thing Today

**Focus on:** Complete Boxzero integration

Due: Friday

**Other Active Goals (2):**
• Follow up with QRA prospects
• Create demo video

...and 1 more

💡 Tip: Complete one goal at a time. Finish before you start something new!
```

### Example 4: Goal Stats
```
You: /goals stats

Bot: 📊 Goal Statistics

**Overall:**
• Total Goals: 15
• Long Term (3-5yr): 3
• Short Term (Quarterly): 5
• Weekly: 7

**This Week:**
• Active Weekly Goals: 3
• Completed: 4
• Completion Rate: 57%

**Performance:**
📈 Making progress. Focus on finishing!
```

---

## Integration with Goal Management Framework

The Telegram bot is fully integrated with Coach-Cleo's Goal Management Framework:

### 4-Tier Goal Hierarchy
1. **Priority 1: Weekly Goals** - This week's focus (due Friday)
2. **Priority 2: Short Term Goals** - Quarterly/Annual (3-12 months)
3. **Priority 3: Long Term Goals** - Strategic vision (3-5 years)
4. **Priority 4: Someday Goals** - Future possibilities

### Alignment
- All weekly goals must support short-term goals
- The bot prevents setting too many goals (max 3-5 weekly)
- "Finish Before Start" principle enforced
- Completion tracking and celebration

---

## Best Practices

### 1. Daily Routine
**Morning:**
```
/briefing          # Get your daily briefing
/focus             # Identify your ONE thing
```

**Evening:**
```
/goal_review daily # Quick progress check
```

### 2. Weekly Routine
**Sunday/Monday:**
```
/weekly_planning   # Plan the week with Coach-Cleo
/goals weekly      # Review new weekly goals
```

**Friday:**
```
/goals stats       # Check completion rate
/goal_review weekly # Reflect on the week
```

### 3. Managing Approvals
- Check `/pending` regularly (1-2x per day)
- Review action context before approving
- Use `/history` to track patterns

### 4. Agent Interaction
- Ask natural questions - the bot routes to the right agent
- Use `/agent_run` for specific workflows
- Let agents request approval for important actions

---

## Future Enhancements (Possible)

- **Voice Messages:** Process voice notes
- **Document Upload:** Share files with agents
- **Scheduled Workflows:** Auto-trigger weekly planning
- **Goal Progress Tracking:** Visual progress charts
- **Team Notifications:** Multi-user support
- **Advanced Reminders:** Recurring reminders
- **Agent Collaboration:** Multiple agents working together

---

## Troubleshooting

### No pending actions showing
- Agents need to use the `request_approval` tool
- Check if actions were auto-approved

### Goals not loading
- Ensure `goal_helper.py` is properly configured
- Check Todoist API connection
- Verify "Agent-Cleo-Goals" label exists in Todoist

### Agent not responding
- Check `Prompt-Manifest.md` exists for the agent
- Verify agent is in correct directory (Personal/Team/Worker/Expert Agents)
- Review bot logs for errors

### Notifications not appearing
- Check notification queue: pending notifications may be scheduled
- Verify notification_service is initialized

---

## Technical Details

### Data Persistence
- All data stored in JSON files in `data/` directory
- Actions and history preserved across restarts
- Conversation history per user (last 10 messages)

### Security
- User ID verification for all actions
- Action approval requires same user who received request
- No cross-user data access

### Performance
- Async/await for all Telegram operations
- Lazy loading of agent prompts
- Efficient conversation history management

---

## Support

For issues or questions:
1. Check `/help` in Telegram
2. Review this guide
3. Check bot logs for errors
4. Verify environment variables in `.env`

---

**Version:** 2.0
**Last Updated:** November 9, 2025
**Author:** Agent-Cleo Development Team
