# Agent-Cleo 🤖

**AI Agent Orchestration System with Todoist Integration**

A comprehensive multi-agent orchestration system featuring a four-tier architecture: Master Orchestration, Personal & Team Agents, Worker Agents, and Expert Agents. Includes integrated Todoist task management for seamless workflow coordination.

---

## 🌟 Features

### Core Capabilities
- **Four-Tier Agent Architecture** - Hierarchical orchestration system
- **28 Specialized Agents** - Personal, Team, Worker, and Expert agents
- **Bidirectional Todoist Integration** - Create and read tasks with automatic date conversion
- **Flask Web Dashboard** - Job management and activity monitoring
- **Context Management** - Each agent maintains its own context and output folders
- **Automated Scheduling** - Daily, weekly, monthly, and custom job schedules

### Agent Types
- **Master Orchestration**: Agent-Cleo (strategic direction)
- **Personal Agents**: Coach-Cleo, HealthFit-Agent
- **Team Agents**: DecideWright-MD, S55-MD, SparkwireMedia-MD, ThinTanks-MD, Ascendore-MD, Boxzero-MD
- **Worker Agents**: 9 specialized execution agents (EA, Legal, CMO, CC, CCO, CPO, FD, CSO, SysAdmin)
- **Expert Agents**: 11 subject matter experts (RegTech, DataScience, CyberSecurity, ESG, AI-Ethics, FinancialModeling, MarketingStrategist, Copywriter, Designer, TechnicalWriter, StrategyRisk)

---

## 📁 Project Structure

```
Agent-Cleo/
├── app.py                              # Main Flask application
├── models.py                           # Database models
├── agent_utils.py                      # Agent discovery and monitoring
├── todoist_integration.py              # Todoist API integration
├── requirements.txt                    # Python dependencies
├── agents.db                           # SQLite database (auto-created)
│
├── Personal Agents/                    # Personal development agents
│   ├── Coach-Cleo/
│   │   ├── Context/                    # Coaching frameworks, goals
│   │   ├── Output/                     # Coaching sessions, plans
│   │   └── Prompt-Manifest.md          # Agent definition
│   └── HealthFit-Agent/
│       ├── Context/
│       ├── Output/
│       └── Prompt-Manifest.md
│
├── Team Agents/                        # Business unit orchestrators
│   ├── DecideWright-MD/
│   ├── S55-MD/
│   ├── SparkwireMedia-MD/
│   ├── ThinTanks-MD/
│   ├── Ascendore-MD/
│   └── Boxzero-MD/
│       ├── Context/
│       ├── Output/
│       └── Prompt-Manifest.md
│
├── Worker Agents/                      # Task execution agents
│   ├── Agent-EA/                       # Executive Assistant
│   ├── Agent-Legal/                    # Legal Expert
│   ├── Agent-CMO/                      # Chief Marketing Officer
│   ├── Agent-CC/                       # Content Creator
│   ├── Agent-CCO/                      # Chief Consultancy Officer
│   ├── Agent-CPO/                      # Chief Product Officer
│   ├── Agent-FD/                       # Finance Director
│   ├── Agent-CSO/                      # Chief Sales Officer
│   └── Agent-SysAdmin/                 # System Administrator
│       ├── Context/
│       ├── Output/
│       └── Prompt-Manifest.md
│
├── Expert Agents/                      # Subject matter experts
│   ├── Expert-RegTech/                 # Regulatory Technology
│   ├── Expert-DataScience/             # Data Science & Analytics
│   ├── Expert-CyberSecurity/           # Cybersecurity
│   ├── Expert-ESG/                     # Environmental, Social, Governance
│   ├── Expert-AI-Ethics/               # AI Ethics
│   ├── Expert-FinancialModeling/       # Financial Modeling
│   ├── Expert-MarketingStrategist/     # Marketing Strategy & Positioning
│   ├── Expert-Copywriter/              # Copywriting
│   ├── Expert-Designer/                # Design & UX
│   ├── Expert-TechnicalWriter/         # Technical Writing
│   └── Expert-StrategyRisk/            # Strategy & Risk Management
│       ├── Context/
│       ├── Output/
│       └── Prompt-Manifest.md
│
├── Context/                            # Global context files
│   └── TODOIST_QUICK_REFERENCE.md
│
├── templates/                          # Flask HTML templates
├── .claude/                            # Claude Code configuration
│
└── Documentation/
    ├── AGENT_STRUCTURE_SUMMARY.md
    ├── EXPERT_AGENTS_SUMMARY.md
    ├── TODOIST_SETUP.md
    ├── TODOIST_INTEGRATION_SUMMARY.md
    └── TODOIST_QUICK_REFERENCE.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Todoist account (optional, for task integration)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Agent-Cleo.git
   cd Agent-Cleo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Todoist (Optional but Recommended):**

   Get your Todoist API token:
   - Go to https://todoist.com → Settings → Integrations → Developer
   - Copy your API token

   Set environment variable:
   ```powershell
   # Windows PowerShell
   [System.Environment]::SetEnvironmentVariable('TODOIST_API_TOKEN', 'your-token-here', 'User')
   ```

   ```bash
   # macOS/Linux
   export TODOIST_API_TOKEN="your-token-here"
   # Add to ~/.bashrc or ~/.zshrc for persistence
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

6. **Initialize the system:**
   - Click "Initialize System" on the dashboard
   - All agents will be discovered automatically

---

## 📖 Usage Guide

### Working with Agents

Each agent has a **Prompt-Manifest.md** file that defines:
- Agent type and purpose
- Core responsibilities
- Expertise areas
- Communication style
- Collaboration patterns
- Tools and integrations

### Using Todoist Integration

**Coach-Cleo creating weekly planning tasks:**
```python
from todoist_integration import create_weekly_plan_tasks

tasks = [
    {
        "content": "Create DecideWright one-page offer",
        "project_name": "DecideWright",
        "priority": 4,  # 4=urgent, 3=high, 2=medium, 1=normal
        "due_string": "Wednesday"
    }
]

result = create_weekly_plan_tasks(tasks, agent="Coach-Cleo")
```

**Worker Agent requesting action:**
```python
from todoist_integration import create_task_for_andrew

create_task_for_andrew(
    content="Review QRA Playbook pricing",
    description="Competitor analysis complete, need decision",
    project="DecideWright",
    priority=3,
    due="Friday",
    labels=["sales", "strategic"],
    agent="Agent-CMO"
)
```

### Todoist Projects

Recommended project structure in Todoist:
- **DecideWright** - QRA Playbook, RBPM, Predixtive, Greentabula, Greenledger
- **Studio55** - AI services, Apportal, Trisingularity
- **SparkwireMedia** - Content, media, NoFatSmoker
- **ThinTanks** - Research and advisory
- **Ascendore** - General business operations
- **Personal** - Personal development, health, fitness

---

## 🔧 API Endpoints

### Todoist Integration
**Task Creation:**
- `POST /api/todoist/task` - Create single task
- `POST /api/todoist/tasks/batch` - Create multiple tasks

**Task Reading:**
- `GET /api/todoist/tasks` - Get tasks (optional: ?label=Agent-Cleo)
- `GET /api/todoist/tasks/agent-cleo` - Get all Agent-Cleo labeled tasks

**Task Management:**
- `PUT /api/todoist/task/<id>` - Update a task
- `POST /api/todoist/task/<id>/complete` - Mark task as complete

**Projects & Testing:**
- `GET /api/todoist/projects` - List all projects
- `GET /api/todoist/test` - Test integration health

### Agent Management
- `GET /api/agents` - List all agents
- `GET /api/agents/<id>` - Get agent details
- `GET /api/agents/<id>/context` - Get agent context files
- `POST /api/initialize` - Initialize/refresh agents

### Job Management
- `GET /api/jobs` - List all jobs
- `POST /api/jobs` - Create a job
- `PUT /api/jobs/<id>` - Update a job
- `DELETE /api/jobs/<id>` - Delete a job
- `POST /api/jobs/<id>/run` - Run job manually

### Activity Tracking
- `GET /api/activities` - List activities
- `POST /api/activities` - Create activity entry

### Monitoring
- `POST /api/monitor/scan` - Scan all Output folders

---

## 🏗️ Four-Tier Architecture

### Tier 1: Master Orchestration
**Agent-Cleo** - Orchestrates all agents, provides strategic direction

### Tier 2: Personal & Team Agents
**Personal Agents:**
- Coach-Cleo - Personal development and life coaching
- HealthFit-Agent - Health, fitness, and wellness

**Team Agents (Managing Directors):**
- DecideWright-MD - Decision support and analytics portfolio
- S55-MD - Creative and technology services
- SparkwireMedia-MD - Media and content business
- ThinTanks-MD - Thought leadership and research
- Ascendore-MD - General business unit management
- Boxzero-MD - Strategic business initiative management

### Tier 3: Worker Agents
Task execution specialists:
- Agent-EA - Executive Assistant
- Agent-Legal - Legal Expert
- Agent-CMO - Chief Marketing Officer
- Agent-CC - Content Creator
- Agent-CCO - Chief Consultancy Officer
- Agent-CPO - Chief Product Officer
- Agent-FD - Finance Director
- Agent-CSO - Chief Sales Officer
- Agent-SysAdmin - System Administrator

### Tier 4: Expert Agents
Subject matter experts (consultative, not executors):
- Expert-RegTech - Regulatory Technology
- Expert-DataScience - Data Science & Analytics
- Expert-CyberSecurity - Cybersecurity
- Expert-ESG - Environmental, Social, Governance
- Expert-AI-Ethics - AI Ethics
- Expert-FinancialModeling - Financial Modeling
- Expert-MarketingStrategist - Marketing Strategy & Positioning
- Expert-Copywriter - Copywriting
- Expert-Designer - Design & UX
- Expert-TechnicalWriter - Technical Writing
- Expert-StrategyRisk - Strategy & Risk Management

---

## 📚 Documentation

Comprehensive documentation available:

- **[AGENT_STRUCTURE_SUMMARY.md](AGENT_STRUCTURE_SUMMARY.md)** - Complete agent architecture overview
- **[EXPERT_AGENTS_SUMMARY.md](EXPERT_AGENTS_SUMMARY.md)** - Expert agents implementation details
- **[TODOIST_SETUP.md](TODOIST_SETUP.md)** - Step-by-step Todoist integration setup
- **[TODOIST_INTEGRATION_SUMMARY.md](TODOIST_INTEGRATION_SUMMARY.md)** - Complete integration guide
- **[TODOIST_QUICK_REFERENCE.md](Context/TODOIST_QUICK_REFERENCE.md)** - Quick reference for agents

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (file-based database)
- **Frontend**: HTML + Tailwind CSS + Alpine.js
- **Scheduler**: APScheduler (background job scheduling)
- **Integration**: Todoist API (todoist-api-python)

---

## 🔒 Security

### Important Security Notes

1. **Never commit sensitive data:**
   - API tokens are in environment variables, not code
   - `.gitignore` excludes `.env` files, database, and sensitive folders
   - Review Context folders before committing

2. **Local use recommended:**
   - Designed for localhost use
   - No authentication by default
   - For remote access, implement authentication

3. **API Token Security:**
   - Rotate Todoist API tokens periodically
   - Never share tokens in public repositories
   - Use environment variables only

---

## 🧪 Testing

### Test Todoist Integration
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
  ...

✓ Task created successfully!
```

### Test Flask Application
```bash
python app.py
# Open http://localhost:5000
# Click "Initialize System"
```

---

## 🐛 Troubleshooting

### Todoist Integration Issues

**Error: "Todoist API token not provided"**
- Set `TODOIST_API_TOKEN` environment variable
- Restart terminal/IDE after setting
- Verify: `echo $env:TODOIST_API_TOKEN` (PowerShell)

**Tasks not appearing:**
- Check project name matches Todoist exactly
- Verify API token has correct permissions
- Check Todoist app/web to confirm creation

### Agent Issues

**Agents not showing up:**
- Verify each agent has Context and Output folders
- Click "Initialize System" to refresh
- Check console for error messages

**Jobs not running:**
- Verify job status is "active"
- Check Next Run time
- Ensure Flask app is running

---

## 🤝 Contributing

This is a personal orchestration system, but contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed for personal and commercial use by DecideWright Ltd.

---

## 🙏 Acknowledgments

Built with:
- Flask - Lightweight Python web framework
- Todoist API - Task management integration
- APScheduler - Background job scheduling
- Claude (Anthropic) - AI assistance

---

## 📞 Support

For issues or questions:
1. Check documentation in the `/docs` folder
2. Review this README
3. Check the console output for errors
4. Test Todoist integration: `python todoist_integration.py`

---

**Version**: 1.0.0
**Last Updated**: November 3, 2025
**Status**: ✅ Production Ready

---

Made with ❤️ for productivity and automation
