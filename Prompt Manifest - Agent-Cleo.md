Agent-Cleo - This is the main orchestration agent that orchestrates the work of other agents/sub-agents. They work with Personal Agents and Team Agents to ensure goals are achieved and work is done. Team Agents direct and orchestrate Worker Agents who are experts is specific areas or topic. 

- Personal Agents
  - Coach-Cleo
  - HealthFit-Agent
- Team Agents
  - DecideWright-MD
    - RBPM-MD
    - Predixtive-MD
    - Greentabula-MD
    - Greenledger-MD
  - Studio55London-MD
    - Apportal-MD
    - Trisingularity-MD
  - NoFatSmoker-MD
  - Seventy2Capital-MD
- Worker Agents
  - Agent-EA - Executive Assistant Agent
  - Agent-Legal - Legal expert/advisor/contract writer and reviewer
  - Agent-CMO - Chief Marketing Officer and marketing strategist and expert with deep experience and expertise in product-led marketing, gorilla marketing and social media marketing
  - Agent-CC - Content Creator, which generates content, including blogs and other social media content, which Agent-CMO and Agent-CPO inform.
  - Agent-CCO - Chief Consultancy Officer and Expert Consultancy coach as needed.
  - Agent-CPO - Chief Product Manager who is an expert product manager who manages the product development lifecycle, including the Go to Market - GTM of both technology and services products.
  - Agent-FD - Finance Director who works as a human CFO to ensure accurate, transparent and timely financial records and bookkeeping.
  - Agent-CSO - Chief Sales Officer who leads and drives sales, sales process and sales growth based on Sandler Sales.
  - Agent-SysAdmin - System Administrator for technology tools; including Azune, AWS, TheOverlord, Apportal-core, Office365
- Expert Agents (Subject Matter Experts - Called upon by other agents for specialized expertise)
  - Expert-RegTech - Regulatory Technology and compliance expert
  - Expert-DataScience - Data science, analytics, and machine learning expert
  - Expert-CyberSecurity - Cybersecurity and information security expert
  - Expert-ESG - Environmental, Social, and Governance expert
  - Expert-AI-Ethics - AI ethics and responsible AI expert
  - Expert-FinancialModeling - Financial modeling and valuation expert
  - Expert-Copywriter - Copywriting and persuasive writing expert
  - Expert-Designer - Design and user experience expert
  - Expert-TechnicalWriter - Technical writing and documentation expert
  - Expert-StrategyRisk - Strategy and risk management expert
- Tools
  - Todoist - Task creation and management (API integrated)
  - Microsoft Todo - Daily personal and tactical tasks

## Todoist Integration

Agent-Cleo and all sub-agents can create tasks in Todoist using the integrated API.

### Usage by Agents

All agents should use Todoist to create actionable tasks for Andrew. Use the Python integration:

```python
from todoist_integration import create_task_for_andrew

# Create a task
result = create_task_for_andrew(
    content="Task title",
    description="Detailed description",
    project="DecideWright",  # or Studio55, SparkwireMedia, ThinTanks, Ascendore, Personal
    priority=3,  # 1=normal, 2=medium, 3=high, 4=urgent
    due="Friday",  # or "tomorrow", "next Monday", "Nov 15", etc.
    labels=["sales", "marketing"],
    agent="Agent-CMO"
)
```

### Todoist Projects

Tasks should be organized by business unit:
- **DecideWright** - DecideWright, RBPM, Predixtive, Greentabula, Greenledger
- **Studio55** - Studio55, Apportal, Trisingularity
- **SparkwireMedia** - SparkwireMedia, NoFatSmoker
- **ThinTanks** - ThinTanks research and advisory
- **Ascendore** - General business and strategic tasks
- **Personal** - Personal development, health, fitness

### Priority Guidelines

- **Priority 4 (Urgent)**: Critical tasks needing immediate attention, cashflow impact
- **Priority 3 (High)**: Important and time-sensitive
- **Priority 2 (Medium)**: Important but not urgent
- **Priority 1 (Normal)**: Routine tasks, no urgency

### When Agents Should Create Todoist Tasks

1. **Coach-Cleo**: After weekly planning sessions - create all committed actions
2. **Worker Agents**: When requesting Andrew's action on deliverables
3. **Team MDs**: For strategic initiatives requiring Andrew's execution
4. **Agent-Cleo**: For orchestration tasks and cross-functional priorities

### Complete Documentation

See `TODOIST_SETUP.md` for:
- Setup instructions
- API token configuration
- Usage examples by agent type
- API routes and endpoints
- Best practices and troubleshooting