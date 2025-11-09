# Agent-Cleo Telegram Bot

Connect with your Agent-Cleo coaching and productivity system via Telegram for on-the-go task management, coaching, and business insights.

---

## Features

✅ **Multi-Agent Support** - Automatic routing to Coach-Cleo, DecideWright-MD, and all 26 agents
✅ **Todoist Integration** - Create tasks directly from Telegram
✅ **Action Approval System** - Approve or reject agent actions with inline buttons
✅ **Goal Management** - Full integration with Coach-Cleo's Goal Management Framework
✅ **Workflow Triggers** - Trigger weekly planning, goal reviews, and agent workflows
✅ **Proactive Notifications** - Receive updates, reminders, and alerts from agents
✅ **Conversation Memory** - Context-aware conversations
✅ **Natural Language** - Just message naturally, no complex commands
✅ **Rich Responses** - Formatted text with markdown support

---

## Quick Start

### Step 1: Create Your Telegram Bot (5 minutes)

1. **Open Telegram** and search for `@BotFather`

2. **Start a chat** and type: `/newbot`

3. **Follow the prompts:**
   - Bot name: `Agent-Cleo` (or any name you want)
   - Username: `your_agent_cleo_bot` (must be unique and end with 'bot')

4. **Save your token!** BotFather will give you an API token like:
   ```
   1234567890:ABCdefGHIjklMNOpqrSTUvwxyz
   ```
   Keep this secret!

5. **Optional:** Set bot photo and description via BotFather commands

---

### Step 2: Set Up Environment (5 minutes)

1. **Navigate to Telegram Bot directory:**
   ```bash
   cd "C:\Users\AndrewSmart\Claude_Projects\Agent-Cleo\Telegram Bot"
   ```

2. **Create `.env` file** (copy from example):
   ```bash
   copy .env.example .env
   ```

3. **Edit `.env` file** with your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
   ANTHROPIC_API_KEY=your_anthropic_api_key
   TODOIST_API_TOKEN=your_todoist_token
   ```

   **Where to find these:**
   - `TELEGRAM_BOT_TOKEN`: From @BotFather (Step 1)
   - `ANTHROPIC_API_KEY`: From https://console.anthropic.com/settings/keys
   - `TODOIST_API_TOKEN`: Already set in main Agent-Cleo `.env`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

### Step 3: Run the Bot (1 minute)

```bash
python bot.py
```

You should see:
```
==================================================
🤖 Agent-Cleo Telegram Bot
==================================================
Status: Running
Default Agent: Coach-Cleo
Debug Mode: False

Bot is ready to receive messages!
Press Ctrl+C to stop.

==================================================
```

---

### Step 4: Start Chatting!

1. **Find your bot** in Telegram (search for the username you created)

2. **Start a conversation:** `/start`

3. **Try some commands:**
   - `/help` - See available commands
   - `/agents` - List all agents
   - `/task Update website by Thursday` - Create Todoist task
   - `/coach What should I focus on today?` - Talk to Coach-Cleo

4. **Natural conversation:**
   ```
   You: What are my priorities for tomorrow?
   Coach-Cleo: [Provides coaching response based on your context]
   ```

---

## Available Commands

### Basic Commands
| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message and overview | `/start` |
| `/help` | Show help and commands | `/help` |
| `/agents` | List all available agents | `/agents` |
| `/reset` | Clear conversation history | `/reset` |

### Goal Management
| Command | Description | Example |
|---------|-------------|---------|
| `/goals [type]` | View goals (weekly, short, long, stats, all) | `/goals weekly` |
| `/focus` | Get your #1 priority for today | `/focus` |
| `/weekly_planning` | Start weekly planning with Coach-Cleo | `/weekly_planning` |
| `/goal_review [type]` | Review goals (daily, weekly, monthly) | `/goal_review daily` |
| `/briefing` | Get your daily briefing | `/briefing` |

### Actions & Approvals
| Command | Description | Example |
|---------|-------------|---------|
| `/pending` | View pending approvals | `/pending` |
| `/history` | View action history | `/history` |
| `/task [description]` | Create Todoist task | `/task Complete QRA Playbook` |

### Agent Workflows
| Command | Description | Example |
|---------|-------------|---------|
| `/coach [message]` | Talk to Coach-Cleo | `/coach What should I focus on?` |
| `/agent_run <agent> <workflow>` | Trigger agent workflow | `/agent_run DecideWright-MD analyze` |

**📖 For detailed documentation, see [TELEGRAM_BOT_GUIDE.md](TELEGRAM_BOT_GUIDE.md)**

---

## How Agent Routing Works

The bot automatically detects which agent to use based on keywords in your message:

**Keyword-based routing:**
- "coach", "goal" → Coach-Cleo
- "health", "fitness", "workout" → HealthFit-Agent
- "decidewright", "qra" → DecideWright-MD
- "studio55", "apportal" → S55-MD
- "marketing" → Agent-CMO
- "sales" → Agent-CSO
- "finance" → Agent-FD
- "legal" → Agent-Legal

**No keyword?** Defaults to Coach-Cleo

**Example conversations:**

```
You: What's the best approach for marketing the QRA Playbook?
Bot: [Routes to DecideWright-MD]

You: Help me plan my workout for tomorrow
Bot: [Routes to HealthFit-Agent]

You: What should I focus on today?
Bot: [Routes to Coach-Cleo]
```

---

## Example Use Cases

### Morning Planning
```
You: /coach What are my priorities today?

Coach-Cleo: Good morning Andrew! Based on your recent planning session:

🎯 Priority 1: TT Invoice (cash flow)
🎯 Priority 2: QRA marketing material
🎯 Priority 3: Website update

Start with the TT items to secure cash flow, then dive into the QRA work. You've got this! 💪
```

### Quick Task Creation
```
You: /task Email client proposal by Friday

Bot: ✅ Task created in Todoist!

**Email client proposal by Friday**

Project: WORK
```

### On-the-Go Coaching
```
You: I'm feeling overwhelmed with all the tasks today

Coach-Cleo: I hear you Andrew. Let's break this down:

1️⃣ Which task is causing the most stress?
2️⃣ What's the next smallest action you can take?
3️⃣ Can any tasks be delegated or deferred?

Take a 5-minute break, then tackle one thing at a time. You don't have to do everything perfectly - just make progress.
```

---

## Troubleshooting

### Bot doesn't respond

**Check:**
1. Is `bot.py` running? (Should see "Running" status)
2. Is TELEGRAM_BOT_TOKEN correct in `.env`?
3. Did you message the right bot username?

**Fix:**
```bash
# Restart the bot
Ctrl+C  (to stop)
python bot.py  (to start again)
```

### "Configuration Error" on startup

**Check:**
- `.env` file exists (copy from `.env.example`)
- All required tokens are set
- No extra spaces or quotes around tokens

### Claude API errors

**Check:**
- ANTHROPIC_API_KEY is valid
- You have API credits remaining
- Internet connection is working

### Todoist tasks not creating

**Check:**
- TODOIST_API_TOKEN is set in `.env`
- Token is valid (test with main todoist_integration.py)
- Project name exists in your Todoist

---

## Running as a Background Service

### Windows (run on startup)

Create a batch file `start_bot.bat`:
```batch
@echo off
cd "C:\Users\AndrewSmart\Claude_Projects\Agent-Cleo\Telegram Bot"
python bot.py
pause
```

Right-click → Send to → Desktop (create shortcut)

Double-click to start bot anytime!

### Keep Running 24/7 (optional)

For always-on bot, deploy to:
- **Railway.app** (free tier)
- **Heroku** (free tier)
- **DigitalOcean** ($5/month droplet)
- **Your home server/Raspberry Pi**

---

## Security Notes

⚠️ **Keep these secret:**
- TELEGRAM_BOT_TOKEN
- ANTHROPIC_API_KEY
- TODOIST_API_TOKEN

✅ **Best practices:**
- Don't commit `.env` file to Git (already in .gitignore)
- Don't share your bot token publicly
- Regenerate tokens if compromised (via @BotFather for Telegram)

---

## Advanced Configuration

### Change Default Agent

Edit `.env`:
```env
DEFAULT_AGENT=DecideWright-MD
```

### Enable Debug Mode

Edit `.env`:
```env
DEBUG_MODE=True
```

Shows detailed logs for troubleshooting.

### Custom Agent Keywords

Edit `config.py` → `AGENT_KEYWORDS` dictionary to add/modify routing keywords.

---

## Project Structure

```
Telegram Bot/
├── bot.py                      # Main bot application
├── agent_handler.py            # Agent routing and Claude integration
├── action_manager.py           # Action approval workflow
├── notification_service.py     # Proactive notifications
├── workflow_triggers.py        # Agent workflow execution
├── goal_commands.py            # Goal management interface
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .env                        # Your credentials (not in Git)
├── README.md                   # Quick start guide
├── TELEGRAM_BOT_GUIDE.md       # Complete feature documentation
└── data/                       # Data storage (created automatically)
    ├── pending_actions.json    # Actions awaiting approval
    ├── action_history.json     # Historical actions
    ├── notifications.json      # Notification queue
    └── output_watchers.json    # Agent output monitoring
```

---

## What's Next?

### Phase 1 ✅ Complete
- [x] Basic message handling
- [x] Agent routing
- [x] Todoist integration
- [x] Coach-Cleo support

### Phase 2 ✅ Complete
- [x] Inline buttons for action approvals
- [x] Goal Management Framework integration
- [x] Weekly planning workflows
- [x] Daily briefing and goal reviews
- [x] Agent workflow triggers
- [x] Proactive notifications

### Phase 3 (Future)
- [ ] Scheduled daily check-ins (automated)
- [ ] Voice message support
- [ ] File/document uploads and processing
- [ ] Visual goal progress charts
- [ ] Calendar integration
- [ ] Multi-user/team support
- [ ] Agent Output monitoring (automatic notifications)

---

## Support

**Issues?**
1. Check troubleshooting section above
2. Review logs in terminal where bot is running
3. Test individual components (todoist_integration.py, agent prompts)

**Feature requests?**
Add to Agent-Cleo project roadmap!

---

## Version

**Current Version:** 2.0.0
**Last Updated:** November 9, 2025
**Agent-Cleo Version:** 1.0.0

**Version 2.0 Features:**
- ✅ Action Approval System with inline buttons
- ✅ Full Goal Management integration
- ✅ Workflow Triggers (weekly planning, goal reviews, briefing)
- ✅ Proactive Notifications
- ✅ Enhanced agent tools (request_approval, send_notification, schedule_reminder)

---

**You're all set! Start the bot and message yourself via Telegram.** 🚀
