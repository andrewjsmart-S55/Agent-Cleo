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

    def __init__(self, action_manager=None, notification_service=None):
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.agent_prompts = {}
        self.conversation_history = {}
        self.action_manager = action_manager
        self.notification_service = notification_service

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

    def create_todoist_task(self, task_details: str, project: str = "Personal", priority: int = 2, due: str = None) -> Dict:
        """Create a task in Todoist"""
        # Parse task details (simple version - can be enhanced)
        lines = task_details.split('\n')
        title = lines[0] if lines else task_details
        description = '\n'.join(lines[1:]) if len(lines) > 1 else ""

        return create_task_for_andrew(
            content=title,
            description=description if description else task_details,
            project=project,
            priority=priority,
            due=due,
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

            # Define tools for Claude to use
            tools = [
                {
                    "name": "create_todoist_task",
                    "description": "Create a task in Andrew's Todoist task manager. Use this when Andrew asks you to create a task, add a task, or remember something for later. You can specify the task content, project, priority, and due date.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "task_details": {
                                "type": "string",
                                "description": "The task title or description. Be clear and actionable."
                            },
                            "project": {
                                "type": "string",
                                "description": "The Todoist project name. Options: Personal, DecideWright, Studio55, SparkwireMedia, ThinTanks, Ascendore, Boxzero. Default is Personal.",
                                "enum": ["Personal", "DecideWright", "Studio55", "SparkwireMedia", "ThinTanks", "Ascendore", "Boxzero"]
                            },
                            "priority": {
                                "type": "integer",
                                "description": "Task priority: 1=normal, 2=medium, 3=high, 4=urgent. Default is 2.",
                                "enum": [1, 2, 3, 4]
                            },
                            "due": {
                                "type": "string",
                                "description": "Due date in natural language like 'today', 'tomorrow', 'Friday', 'next Monday', or a specific date. Leave empty if no due date."
                            }
                        },
                        "required": ["task_details"]
                    }
                },
                {
                    "name": "request_approval",
                    "description": "Request approval from Andrew before taking an action. Use this for important decisions, significant tasks, or anything that should be reviewed before execution. Andrew will receive a notification and can approve, reject, or modify the request.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "action_type": {
                                "type": "string",
                                "description": "Type of action requiring approval (e.g., 'create_task', 'send_email', 'schedule_meeting', 'make_decision')"
                            },
                            "description": {
                                "type": "string",
                                "description": "Clear description of what you want to do and why"
                            },
                            "action_data": {
                                "type": "object",
                                "description": "Data needed to execute the action if approved"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context to help Andrew make the decision"
                            }
                        },
                        "required": ["action_type", "description", "action_data"]
                    }
                },
                {
                    "name": "send_notification",
                    "description": "Send a proactive notification to Andrew. Use this to provide updates, reminders, or important information that Andrew should be aware of.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Notification title"
                            },
                            "message": {
                                "type": "string",
                                "description": "Notification message"
                            },
                            "notification_type": {
                                "type": "string",
                                "description": "Type of notification",
                                "enum": ["info", "warning", "success", "action_required"]
                            },
                            "priority": {
                                "type": "integer",
                                "description": "Priority level (1=high, 2=normal, 3=low)",
                                "enum": [1, 2, 3]
                            }
                        },
                        "required": ["title", "message"]
                    }
                },
                {
                    "name": "schedule_reminder",
                    "description": "Schedule a reminder for Andrew at a specific time in the future.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "reminder_text": {
                                "type": "string",
                                "description": "The reminder message"
                            },
                            "when": {
                                "type": "string",
                                "description": "When to send the reminder (e.g., 'in 1 hour', 'tomorrow at 9am', '2025-11-10 14:00')"
                            }
                        },
                        "required": ["reminder_text", "when"]
                    }
                }
            ]

            # Call Claude API with tools
            response = self.client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=config.MAX_TOKENS,
                system=system_prompt,
                messages=history,
                tools=tools
            )

            # Process response and handle tool calls
            response_text = ""
            tool_results = []

            for content_block in response.content:
                if content_block.type == "text":
                    response_text += content_block.text
                elif content_block.type == "tool_use":
                    # Claude wants to use a tool
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_use_id = content_block.id

                    if tool_name == "create_todoist_task":
                        # Create the task
                        result = self.create_todoist_task(
                            task_details=tool_input.get("task_details"),
                            project=tool_input.get("project", "Personal"),
                            priority=tool_input.get("priority", 2),
                            due=tool_input.get("due")
                        )

                        # Store result for follow-up
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(result)
                        })

                    elif tool_name == "request_approval" and self.action_manager:
                        # Create approval request
                        action_id = self.action_manager.create_action(
                            user_id=user_id,
                            agent_name=agent_name,
                            action_type=tool_input.get("action_type"),
                            description=tool_input.get("description"),
                            action_data=tool_input.get("action_data", {}),
                            context=tool_input.get("context", "")
                        )

                        result = {
                            "success": True,
                            "action_id": action_id,
                            "status": "pending_approval",
                            "message": "Approval request created. User will be notified."
                        }

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(result)
                        })

                    elif tool_name == "send_notification" and self.notification_service:
                        # Create notification
                        notification_id = self.notification_service.create_notification(
                            user_id=user_id,
                            title=tool_input.get("title"),
                            message=tool_input.get("message"),
                            notification_type=tool_input.get("notification_type", "info"),
                            agent_name=agent_name,
                            priority=tool_input.get("priority", 2)
                        )

                        result = {
                            "success": True,
                            "notification_id": notification_id,
                            "message": "Notification queued for delivery"
                        }

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(result)
                        })

                    elif tool_name == "schedule_reminder" and self.notification_service:
                        # Parse when and schedule reminder
                        from datetime import datetime, timedelta
                        import re

                        when_text = tool_input.get("when", "")
                        scheduled_for = None

                        # Simple parsing (can be enhanced)
                        if "hour" in when_text:
                            match = re.search(r'(\d+)\s*hour', when_text)
                            if match:
                                hours = int(match.group(1))
                                scheduled_for = datetime.now() + timedelta(hours=hours)
                        elif "tomorrow" in when_text:
                            scheduled_for = datetime.now() + timedelta(days=1)

                        if scheduled_for:
                            notification_id = self.notification_service.schedule_reminder(
                                user_id=user_id,
                                reminder_text=tool_input.get("reminder_text"),
                                scheduled_for=scheduled_for,
                                agent_name=agent_name
                            )

                            result = {
                                "success": True,
                                "notification_id": notification_id,
                                "scheduled_for": scheduled_for.isoformat()
                            }
                        else:
                            result = {
                                "success": False,
                                "error": "Could not parse when time"
                            }

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(result)
                        })

            # If there were tool calls, get Claude's follow-up response
            if tool_results:
                # Add assistant's tool use to history
                self.add_to_history(user_id, "assistant", str(response.content))

                # Add tool results to history
                for tool_result in tool_results:
                    history.append(tool_result)

                # Get final response from Claude
                follow_up_response = self.client.messages.create(
                    model=config.CLAUDE_MODEL,
                    max_tokens=config.MAX_TOKENS,
                    system=system_prompt,
                    messages=history,
                    tools=tools
                )

                # Extract final response text
                for content_block in follow_up_response.content:
                    if content_block.type == "text":
                        response_text += content_block.text

            # Add final response to history
            if response_text:
                self.add_to_history(user_id, "assistant", response_text)

            return response_text if response_text else "Task created successfully!"

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
