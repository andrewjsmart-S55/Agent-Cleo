"""
Agent Handler for Agent-Cleo Telegram Bot
Routes messages to appropriate agents and manages Claude API calls
"""
import sys
from pathlib import Path
from typing import Optional, Dict, List
from anthropic import Anthropic
import config

# Add parent directory to path to import todoist_integration
sys.path.insert(0, str(config.PROJECT_ROOT))
from todoist_integration import create_task_for_andrew


class AgentHandler:
    """Handles agent routing and Claude API integration"""

    def __init__(self):
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.agent_prompts = {}
        self.conversation_history = {}

    def load_agent_prompt(self, agent_name: str) -> Optional[str]:
        """Load agent prompt manifest from file"""
        if agent_name in self.agent_prompts:
            return self.agent_prompts[agent_name]

        # Try to find the agent in different directories
        search_paths = [
            config.PERSONAL_AGENTS_DIR / agent_name / "Prompt-Manifest.md",
            config.TEAM_AGENTS_DIR / agent_name / "Prompt-Manifest.md",
            config.WORKER_AGENTS_DIR / agent_name / "Prompt-Manifest.md",
            config.EXPERT_AGENTS_DIR / agent_name / "Prompt-Manifest.md",
        ]

        for path in search_paths:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    prompt = f.read()
                    self.agent_prompts[agent_name] = prompt
                    return prompt

        return None

    def detect_agent(self, message: str) -> str:
        """Detect which agent should handle the message based on keywords"""
        message_lower = message.lower()

        # Check for explicit agent mentions
        for keyword, agent in config.AGENT_KEYWORDS.items():
            if keyword in message_lower:
                return agent

        # Default to Coach-Cleo for personal/coaching queries
        return config.DEFAULT_AGENT

    def get_conversation_history(self, user_id: int) -> List[Dict]:
        """Get conversation history for a user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]

    def add_to_history(self, user_id: int, role: str, content: str):
        """Add message to conversation history"""
        history = self.get_conversation_history(user_id)
        history.append({"role": role, "content": content})

        # Keep only last 10 messages to avoid token limits
        if len(history) > 10:
            self.conversation_history[user_id] = history[-10:]

    def get_todoist_tasks(self, filter_query: str = "today | tomorrow") -> str:
        """Fetch tasks from Todoist"""
        if not config.TODOIST_API_TOKEN:
            return "Todoist integration not available."

        try:
            from todoist_api_python.api import TodoistAPI
            api = TodoistAPI(config.TODOIST_API_TOKEN)

            # Get all active tasks - API returns paginated results
            tasks_paginator = api.get_tasks()
            # Convert to list - paginator returns list of lists, get first page
            all_tasks = list(tasks_paginator)
            if all_tasks and isinstance(all_tasks[0], list):
                # Flatten the paginated structure
                tasks = []
                for page in all_tasks:
                    tasks.extend(page)
            else:
                tasks = all_tasks

            # Format tasks for display
            if not tasks or len(tasks) == 0:
                return "No tasks found."

            task_list = []
            for task in tasks:
                # Basic formatting - no emojis to avoid encoding issues
                priority_markers = {1: "[P4]", 2: "[P3]", 3: "[P2]", 4: "[P1]"}
                priority_text = priority_markers.get(task.priority, "[P4]")
                due_text = f" (Due: {task.due.date})" if task.due else ""
                task_list.append(f"{priority_text} {task.content}{due_text}")

            return "\n".join(task_list[:20])  # Limit to 20 tasks

        except Exception as e:
            return f"Error fetching tasks: {str(e)}"

    def create_todoist_task(self, task_details: str) -> Dict:
        """Create a task in Todoist"""
        # Parse task details (simple version - can be enhanced)
        lines = task_details.split('\n')
        title = lines[0] if lines else task_details

        return create_task_for_andrew(
            content=title,
            description=task_details,
            project='WORK',
            priority=2,
            agent='Telegram-Bot'
        )

    def process_message(self, user_id: int, message: str, agent_name: Optional[str] = None) -> str:
        """
        Process user message and return agent response

        Args:
            user_id: Telegram user ID
            message: User message
            agent_name: Specific agent to use (optional)

        Returns:
            Agent response text
        """
        try:
            # Detect agent if not specified
            if not agent_name:
                agent_name = self.detect_agent(message)

            # Load agent prompt
            agent_prompt = self.load_agent_prompt(agent_name)

            if not agent_prompt:
                return f"Sorry, I couldn't find the {agent_name} agent. Using default Agent-Cleo mode."

            # Fetch current tasks if message is about tasks/planning
            task_context = ""
            message_lower = message.lower()
            print(f"DEBUG: Checking message for task keywords: {message_lower}")
            if any(keyword in message_lower for keyword in ['task', 'today', 'tomorrow', 'priority', 'focus', 'plan', 'schedule']):
                print("DEBUG: Task keyword detected, fetching tasks...")
                tasks = self.get_todoist_tasks()
                print(f"DEBUG: Fetched tasks: {tasks[:100] if tasks else 'None'}...")
                if tasks and "Error" not in tasks:
                    task_context = f"\n\n**Andrew's Current Tasks from Todoist:**\n{tasks}\n"
                    print(f"DEBUG: Task context added to prompt")

            # Build system prompt
            system_prompt = f"""{agent_prompt}

You are communicating via Telegram with Andrew Smart. Keep responses:
- Concise and actionable (Telegram messages should be brief)
- Friendly and supportive
- Use emojis sparingly for emphasis
- Format with Telegram markdown when helpful

Current context: This is a Telegram conversation. Andrew can ask you questions, request task creation, or seek coaching advice on the go.{task_context}"""

            # Get conversation history
            history = self.get_conversation_history(user_id)

            # Add current message to history
            self.add_to_history(user_id, "user", message)

            # Call Claude API
            response = self.client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=config.MAX_TOKENS,
                system=system_prompt,
                messages=history
            )

            # Extract response text
            response_text = response.content[0].text

            # Add response to history
            self.add_to_history(user_id, "assistant", response_text)

            return response_text

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            if config.DEBUG_MODE:
                print(error_msg)
            return "I encountered an error processing your request. Please try again."

    def handle_command(self, command: str, args: List[str]) -> str:
        """Handle special bot commands"""

        if command == '/start':
            return """Welcome to Agent-Cleo! 👋

I'm your AI coaching and productivity system. I can help with:

🎯 Daily planning and coaching (Coach-Cleo)
📋 Task creation in Todoist
💼 Business strategy (DecideWright-MD, S55-MD, etc.)
💪 Health and fitness (HealthFit-Agent)

Commands:
/help - Show this message
/agents - List available agents
/task [description] - Create a task in Todoist
/coach - Talk to Coach-Cleo
/reset - Clear conversation history

Just message me naturally and I'll route to the right agent!"""

        elif command == '/help':
            return """Agent-Cleo Telegram Bot Help

💬 Natural conversation:
Just message me and I'll detect which agent to use based on your question.

📋 Create tasks:
/task Complete QRA marketing material

🎯 Specific agents:
/coach What should I focus on today?

🔧 Commands:
/agents - List all agents
/reset - Clear conversation history
/help - This message"""

        elif command == '/agents':
            agents_list = """Available Agents:

**Personal Agents:**
• Coach-Cleo - Personal coaching & goal setting
• HealthFit-Agent - Fitness & health guidance

**Team Agents (Managing Directors):**
• DecideWright-MD - QRA Playbook, decision support
• S55-MD - Studio55, Apportal, tech services
• SparkwireMedia-MD - Content & media
• ThinTanks-MD - Research & advisory
• Ascendore-MD - General business ops

**Worker Agents:**
• Agent-CMO - Marketing strategy
• Agent-CSO - Sales (Sandler methodology)
• Agent-FD - Finance
• Agent-Legal - Legal matters
• Agent-EA - Executive assistance

Mention keywords in your message and I'll route to the right agent!"""
            return agents_list

        elif command == '/reset':
            # Will be implemented in bot.py
            return "Conversation history cleared! Starting fresh. 🔄"

        elif command == '/task':
            if not args:
                return "Please provide task description. Example: /task Complete website update"

            task_description = ' '.join(args)
            try:
                result = self.create_todoist_task(task_description)
                if result['success']:
                    return f"✅ Task created in Todoist!\n\n**{result['content']}**\n\nProject: {result['project']}"
                else:
                    return f"❌ Failed to create task: {result.get('error', 'Unknown error')}"
            except Exception as e:
                return f"❌ Error creating task: {str(e)}"

        elif command == '/coach':
            message = ' '.join(args) if args else "What should I focus on today?"
            return self.process_message(user_id=0, message=message, agent_name='Coach-Cleo')

        else:
            return f"Unknown command: {command}\n\nType /help for available commands."
